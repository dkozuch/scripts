#!/tigress/dkozuch/programs/conda/bin/python

print "Loading packages..."
import numpy as np
import matplotlib.pyplot as plt
import sys

print "Loading data..."
x_file = sys.argv[1]
y_file = sys.argv[2]
window = int(sys.argv[3])
x = np.loadtxt(x_file+".xvg",comments=("#","@"))
y = np.loadtxt(y_file+".xvg",comments=("#","@"))

#esnure x and y are same size
length = np.min([len(x),len(y)])
x = x[:length]
y = y[:length]

print "Smoothing data..."
def movingaverage(data, window_size):
	avg = [ np.mean(data[i:i+window_size]) for i in range(0,len(data)-window_size) ]
	return avg

x_avg = movingaverage(x[:,1],window)
y_avg = movingaverage(y[:,1],window)

print "Plotting data..."
plt.scatter(x[:,1],y[:,1],s=5)
plt.scatter(x_avg, y_avg,s=5)
plt.xlabel(x_file)
plt.ylabel(y_file)
plt.show()

print "Saving average..."
np.savetxt(x_file+"_v_"+y_file+"_avg.txt",np.column_stack((x_avg,y_avg)))

