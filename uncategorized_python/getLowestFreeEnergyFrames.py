import numpy as np
import os
import subprocess
print "Packages loaded..."

gmx = "gmx_164_gpu_pd"
protein = "1l2y"
folder = "optimal_frames"
fes_index = 20
nsims = 28
delta = 1

def getFrame(xtc,tpr,time,name,sel=0):
	string = gmx+" trjconv -f "+xtc+" -s "+tpr+" -b "+str(time)+" -e "+str(time)+" -o "+name+" <<EOF \n"+str(sel)+"\nEOF"
	print string
	subprocess.check_output(string, shell=True)

if os.path.isdir(folder):
	os.system("rm -r " + folder)
	os.system("mkdir " + folder)
else:
	os.system("mkdir " + folder)

#collect prop where lowest free energy observed
print "Collecting property for lowest free energy observation..."
prop = []
for i in range(0,nsims):
	fesi = np.loadtxt("fes_files_potential/fes_ene." + str(i) + "." + str(fes_index) + ".dat",comments=("#","#!"))
	pi = fesi[np.argmin(fesi[:,1]),0]
	prop.append(pi)
prop = np.array(prop)
np.savetxt("tmp_prop.txt",prop)
print prop

#collect corresponding times and frames
print "Collecting times/frames for lowest free energy observation..."
times = []
for i in range(0,nsims):
	with open("potential_files/potential_" + str(i) +".xvg",'r') as f:
		for line in f:
			if line.split()[0] not in ["#","@","@TYPE"]:
				p = float(line.split()[1])
				if prop[i] - delta <= p <= prop[i] + delta:
					ti = float(line.split()[0])
					#break - don't break, use latest time frame with lowest free energy volume
	print [i,ti]
	times.append(ti)
	getFrame(protein + "_sim_" + str(i),"TOPO_SIM/" + protein + "_sim_" + str(i),ti,protein + "_sim_" + str(i) + ".gro")
	os.system("mv " + protein + "_sim_" + str(i) + ".gro " + folder + "/")
times = np.array(times)
print times

#
