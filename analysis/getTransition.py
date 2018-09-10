#See following reference for explanation
#Comparison of two adaptive temperature-based replica exchange methods applied to a sharp phase transition of protein unfolding-folding 
#Lee, M. S.; Olson, M. A. J. Chem. Phys. 2011, 134 (24), 244111.

visual=False

import numpy as np
import os
if visual:
	import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

b=1000
new_reps=28
delmin=0.5
delmax_spacing=1.5
tmin=160.0
tmax=400.0

replica_file = "replica_temp.npy"
#prepFile = "prepare_remd.sh"
#newPrepFile = "prepare_remd_new.sh"

def editprepFile(filein,newfile,newTemps):
	
	#make new line
	newLine = "rep_temps=("
	for i in newTemps:
		newLine = newLine + str(round(i,3)) + " "
	newLine = newLine + ") \n"
	#print newLine
	
	#write new file
	if os.path.isfile(newfile):
		os.system("rm " + newfile)
	with open(filein,"r") as f:
		for line in f:
			if line[0:9] == "rep_temps":
				with open(newfile,"a") as w:
					w.write(newLine)
			else:
				with open(newfile,"a") as w:
					w.write(line)
	
	#replace old file	
	#os.system("mv " + newfile + " " + filein)

print("Importing replica data ...")
replica_mat = np.load(replica_file)
print("Number of replica exchange attempts: " + str(np.shape(replica_mat)[0]))
replica_mat = replica_mat[b:,1:]

reps=np.shape(replica_mat)[1]
print("Number of replicas analyzed: " + str(reps))

print("Assigning replicas as cold or hot...")
#find replica assignment as either cold (1) or hot (2) or none (0) based on last visiting max or min
replica_assignment = np.zeros(np.shape(replica_mat))
round_trip_times = []
for i in range(0,len(replica_mat[0,:])):
	label = 0
	counter = 0
	for j in range(0,len(replica_mat[:,0])):
		if replica_mat[j,i] in [0]: #first replica(s)
			if label == 2: #update list of round trip times
				round_trip_times.append(counter)
				counter = 0
			label = 1
		elif replica_mat[j,i] in [reps-1]: #last replica(s)
			if label == 1: #update round trip times
				round_trip_times.append(counter)
				counter = 0
			label = 2
		replica_assignment[j,i] = label
		counter = counter + 1
	#if i % 1 == 0:
		#print("Percent complete: " + str((i/float(len(replica_mat[0,:])))*100) + "%")
		#print i
		
print round_trip_times
np.savetxt("round_trip_times.txt",np.array(round_trip_times))
print("Mean round trip time: " + str(np.mean(round_trip_times)))

print("Getting round trips per replica...")
replica_transition = np.diff(replica_assignment,axis=0)
print np.shape(replica_transition)
round_trips_per_replica = np.sum(np.absolute(replica_transition),axis=0)
np.savetxt("round_trips_per_replica.txt",round_trips_per_replica)

print("Determine which replicas belong to each temperature")
#make matrix that tracks which replicas are in which temperature
temp_mat = np.empty(replica_mat.shape)
for i in range(0,len(replica_mat[:,0])):
	for j in range(0,len(replica_mat[0,:])):
		temp_mat[i,int(replica_mat[i,j])] = j

print("Find cold and hot histograms")	
#calculate histograms for ncold and nhot
#count whether a hot or cold replica (from getReplicaAssignment) has vistited Ti using temp_mat
ncold = np.zeros(reps)
nhot = np.zeros(reps)
for i in range(0,len(temp_mat[:,0])):
	for j in range(0,reps):
		if replica_assignment[i,int(temp_mat[i,j])] == 1:
			ncold[j] = ncold[j] + 1
		elif replica_assignment[i,int(temp_mat[i,j])] == 2:
			nhot[j] = nhot[j] + 1

print ncold
print
print np.array(nhot)

#calculate fraction
print("Calculating cold fraction...")
f_list = []
for i in range(0,len(ncold)):
	#avoid dividing by zero
	if float(ncold[i]) + float(nhot[i]) == 0:
		f_list.append(0)
	else:
		f_list.append(float(ncold[i])/(float(ncold[i]) + float(nhot[i])))

#get temperatures used in sim files
temps=[]
for i in range(0,reps):
	with open("run_files/sim_files/sim_" + str(i) + ".mdp","r") as f:
		for line in f:
			if len(line.split()) > 0 and line.split()[0] == "ref-t":
				temps.append(float(line.split()[2]))

if visual:
	plt.scatter(range(0,reps),f_list)
	#plt.scatter(temps,f_list)
	plt.show()

f_out = np.column_stack((np.arange(0,reps),np.array(temps),np.array(f_list)))
np.savetxt("f_list.txt",f_out)

#print old temps to file
fileout="old_temps.txt"
if os.path.isfile(fileout):
	print("Error: " + fileout + " already exists. Please rename and rerun.")
else:
	with open(fileout,"w") as w:
		for i in temps:
			w.write(str(i)+"\n")

#interpolate to find linear f
print("Determining new temperatures...")
interp = interp1d(f_list[::-1],range(0,reps)[::-1]) #interp1d has stupid bounds error rules, reverse both lists
#interp = interp1d(f_list[::-1],temps[::-1]) #interp1d has stupid bounds error rules, reverse both lists
interp_temp = interp1d(range(0,reps),temps)
new_temps = [tmin]
targets = [ (1 - (float(i)/(new_reps))) for i in range(0,new_reps) ]
#print targets

for i in range(1,len(targets)):
	max_tempi = new_temps[i-1]*(tmax/tmin)**(delmax_spacing/float(new_reps))
	#check if outside interp range
	if targets[i] >= np.max(f_list):
		tempi = np.min(temps)
	elif targets[i] <= np.min(f_list):
		tempi = max_tempi
	else:
		#print targets[i]
		target_index = float(interp(targets[i]))
		if target_index >= new_reps:
			tempi = tmax
		elif target_index <= 1:
			tempi = tmin
		else:
			tempi = float(interp_temp(target_index))
	
	#check if delt too high or too low
	if tempi - new_temps[i-1] < delmin:
		tempi = new_temps[i-1] + delmin
	elif tempi > max_tempi:
		tempi = max_tempi
	new_temps.append(tempi)

#delete closest temperatures until max temp above max temp
while new_temps[-1] < tmax:
	#find which pair of temps is closest
	diffs = [ new_temps[i+1] - new_temps[i] for i in range(0,len(new_temps)-1) ]
	#print diffs[:10]
	diff_min = np.argmin(diffs)
	#only delete temperatures above the theoretical transition
	new_temps.pop(diff_min+1)
	max_temp = new_temps[-1]*(tmax/tmin)**(delmax_spacing/float(new_reps))
	new_temps.append(max_temp)
	

if visual:
	plt.scatter(range(0,reps),temps,c="b")
	plt.scatter(range(0,new_reps),new_temps,c="r")
	plt.show()

#save new temps
with open("new_temps.txt","w") as w:
	for item in new_temps:
		w.write(str(int(item)) + "\n")	

#editprepFile(prepFile,newPrepFile,new_temps)

print("Done")



################################################

# def getReplicaAssignment(replica_mat,step):
	# #determine which replicas are cold and which are hot
	# #print("Identifying cold/hot replicas...")
	# replica_assignment = np.zeros(reps)
	# for i in range(0,reps):
		# for j in range(len(replica_mat[:,i])-step,len(replica_mat[:,i])+1):
			# if int(replica_mat[-j,i]) == 0:
				# #print [i,-j,replica_mat[-j,i]]
				# replica_assignment[i] = 1
				# break
			# elif int(replica_mat[-j,i]) == len(replica_mat[0,:]) - 1:
				# #print [i,-j,replica_mat[-j,i]]
				# replica_assignment[i] = 2
				# break
	# return replica_assignment
	



		
