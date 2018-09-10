#!/tigress/dkozuch/programs/conda/bin/python

print "Loading pacakges..."
import numpy as np
import sys
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Options for calculating average values from FES')
parser.add_argument('-s','--sims',help="Number of simulations to consider (int)",required=False,default=28,type=int)
parser.add_argument('-n','--name',help="Property to calculate avaerage for (string)",required=True,type=str)
parser.add_argument('-b','--begin',help="Part to begin sampling (int)",required=True,type=int)
parser.add_argument('-e','--end',help="Part to end sampling (int)",required=True,type=int)
parser.add_argument('--visual',help="Whether to plot property as function of temperature (True/False)",required=False,default=False,type=bool)

parsed = parser.parse_args()
print "Property selected: "+parsed.name
print "Plotting: "+str(parsed.visual)
nsims = parsed.sims
property = parsed.name
v_begin = parsed.begin
v_end = parsed.end
nv = v_end - v_begin +1


def load_file(i,v):
	folder = "reweighted_" + property + "_stride"
	name = "reweighted_" + property
	filename = folder + "/" + name + "." + str(i) + "." + str(v)
	data = np.loadtxt(filename,comments=("@","#","!"))
	return data
	
def avg_from_fes(i,v):
	fes = load_file(i,v)
	prob = np.exp(-fes[:,1]) #data should be in kT, doesn't matter because will normalize
	prob_norm = prob/np.sum(prob) #normalize probabilty
	avg = np.sum(fes[:,0]*prob_norm)
	return avg

print "Loading data..."
avg_array = np.zeros((nsims,nv)) #array to hold all sampling values
for i in range(0, nsims):
        for v in range(v_begin,v_end+1):
                avg_array[i,v-v_begin] = avg_from_fes(i,v)

print "Processing data..."
avg_mean = np.mean(avg_array,axis=1)
temps = np.loadtxt("temps.txt")
avg_temps = np.column_stack((temps,avg_mean))
np.savetxt(property+"_avg_from_fes_v"+str(v_begin)+"t"+str(v_end)+".txt",avg_temps)

if parsed.visual:
	print "Plotting..."
	plt.plot(avg_temps[:,0],avg_temps[:,1],'-o')
	plt.xlabel("T (K)")
	plt.ylabel(property)
	plt.show()
