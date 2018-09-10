print("Loading packages...")
import numpy as np
import sys
from scipy.interpolate import UnivariateSpline
# from scipy.signal import savgol_filter
# from scipy.ndimage.filters import gaussian_filter1d as gf
#import matplotlib.pyplot as plt
#from math import factorial
print("All packages loaded")


name = sys.argv[1]
if len(sys.argv) > 2:
	ver = sys.argv[2]

temps = np.loadtxt("temps.txt")
n = len(temps)
print("Number of sims: "  + str(n))
results = []

#get averages and error
for i in range(0,n):

	if len(sys.argv) > 2:
		file=name + "." + str(i) + "." + ver + ".dat"
	else:
		file=name + "." + str(i)
	data = np.loadtxt(file)
	x = data[:,0]
	y = data[:,1]

	probRaw = np.exp(-y)
	prob = probRaw/np.sum(probRaw)
	mean = np.sum(prob*x)
	std = np.sum(prob*((x - np.mean(x))**2))**(0.5)
	results.append([temps[i],mean,std])
results = np.array(results)

if len(sys.argv) > 2:	
	np.savetxt(name+"."+ver+"_temp.txt",results)
else:
	np.savetxt(name+"_temp.txt",results)
#x = results[:,0]
#y = results[:,1]
#z = np.polyfit(x,y,6)
#p = np.poly1d(z)
#xp = np.arange(np.min(x),np.max(x))
#plt.plot(x, y, '.', xp, p(xp),'-')
#plt.show()

#p2 = np.polyder(p)
#plt.plot(xp, p2(xp),'-')
#plt.show()

#get spline and plot
#x = results[:,0]
#y = results[:,1]
#yg = gf(y,1)
#us = UnivariateSpline(x,y,k=1)
#xs = np.arange(np.min(x),np.max(x))
#plt.plot(x,y,'.')
#plt.plot(xs,us(xs))
#plt.show()

# #get derivative
#usd = us.derivative(1)
# np.savetxt(name+"_der.txt",np.column_stack((x,usd(x))))

# #fit derivative
#plt.plot(xs,usd(xs),'o',xs,usd(xs),'-')
#plt.show()


