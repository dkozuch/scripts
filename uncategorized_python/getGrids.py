import numpy as np
import sys

print "Running..."

filename=sys.argv[1]

n_temps = 28
begin = 50
dev_multiplier=50

#get mean, standard deviation for each potential energy
stats = np.zeros([n_temps,2])
for i in range(0,n_temps):
	listi = np.loadtxt(filename + "_files/" + filename+ "_" + str(i) + ".xvg",skiprows=begin+24)
	dev = np.max(listi[:,1]) - np.min(listi[:,1])
	stats[i,:] = [np.mean(listi[:,1]),dev]

#calculate/write grid values
grid_min = stats[:,0]-dev_multiplier*stats[:,1]
grid_max = stats[:,0]+dev_multiplier*stats[:,1]

np.savetxt("grid_mean_" + filename + ".txt",stats[:,0])
np.savetxt("grid_min_" + filename + ".txt",grid_min)
np.savetxt("grid_max_" + filename + ".txt",grid_max)	

