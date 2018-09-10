#!/tigress/dkozuch/programs/conda/bin/python

print "Loading packages..."
import numpy as np
import matplotlib
matplotlib.rcParams.update({'errorbar.capsize': 2}) #add caps to error bars
import matplotlib.pyplot as plt
import sys
print "Packages loaded..."

nsims = 28
property = "rmsd"
cutoff = 0.3
r = 0.008314 #J/mol

stride=100.0 #ns
#takes user arguments for start and stop time in ns
stride_start = int(np.floor(float(sys.argv[1])/stride))-1
stride_end = int(np.floor(float(sys.argv[2])/stride))-1

print("Using files "+str(stride_start)+"-"+str(stride_end)+" for user time "+sys.argv[1]+"-"+sys.argv[2]+"ns") 

def prop_filename(i,v):
	folder = "reweighted_" + property + "_stride"
	name = "reweighted_" + property
	filename = folder + "/" + name + "." + str(i) + "." + str(v)
	return filename

def get_frac_folded(fes_prop_file,temp,folded_prop):
	fes_prop = np.loadtxt(fes_prop_file)	
	kt = temp*r
	prob = np.exp(-fes_prop[:,1]/float(kt))
	prob_norm = prob/np.sum(prob) #normalize probabilty
	prob_prop = np.column_stack((fes_prop[:,0],prob_norm))
	
	prob_folded = prob_prop[prob_prop[:,0] < folded_prop] #keep rows where prop </>folded_prop
	frac_folded = np.sum(prob_folded[:,1])
	
	return frac_folded

def get_frac_curve(cutoff,v):
	temps = np.loadtxt("temps.txt")
	frac_folded_list = temps[:nsims]
	#print "Performing calculation for prop cutoff of " + str(cutoff) + " and version " + str(v)
	frac_folded_listj = []
	for i in range(0,nsims):
		frac_foldedij = get_frac_folded(prop_filename(i,v),temps[i],cutoff)
		frac_folded_listj.append(frac_foldedij)
	#print np.shape(frac_folded_listj)
	frac_folded_list = np.column_stack((frac_folded_list,np.array(frac_folded_listj)))
	return frac_folded_list


#get average
print "Getting average..."
vList = range(stride_start,stride_end+1)
temps = np.loadtxt("temps.txt")
curve_list = []
for i in vList:
	curve = get_frac_curve(cutoff,i)
	curve_list.append(curve[:,1])
curve_list = np.array(curve_list)
curve_mean = np.column_stack((temps,np.mean(curve_list,axis=0)))
curve_mean_error = np.column_stack((temps,np.mean(curve_list,axis=0),np.std(curve_list,axis=0)))

np.savetxt(property + "_fraction_folded_"+sys.argv[1]+"t"+sys.argv[2]+"ns.txt",curve_mean_error)

# plot different fes versions
if True:
	print "Plotting..."
	colors = plt.cm.Spectral(np.linspace(0,1,len(vList)))
	count = 0
	for i in vList:
		curve = get_frac_curve(cutoff,i)
		plt.plot(curve[:,0],curve[:,1],'-',color=colors[count])
		count = count + 1
	legends = [ str((x+1)*100) + " ns" for x in vList]
	legends.append("Mean")
	plt.plot(curve_mean[:,0],curve_mean[:,1],'-o',color='black')
	plt.errorbar(curve_mean_error[:,0],curve_mean_error[:,1], yerr=curve_mean_error[:,2],color='black')
	plt.legend(legends)
	plt.xlabel("T (K)")
	plt.ylabel("Fraction Folded")
	plt.show()




