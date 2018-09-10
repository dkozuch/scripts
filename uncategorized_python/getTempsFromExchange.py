import numpy as np
import matplotlib.pyplot as plt

ex_goal = 0.3
w = 4

#import
old_temps = np.loadtxt("temps.txt")
old_delta_temps = np.diff(old_temps)

#get old and new deltas
exchange = np.loadtxt("exchange_prop.txt")
new_delta_temps = []
for i in range(0,len(exchange)):
	miss = w*(exchange[i] - ex_goal)
	mult = 1 + miss
	new_delta = old_delta_temps[i]*mult
	new_delta_temps.append([old_temps[i],new_delta])
new_delta_temps = np.array(new_delta_temps)

#get new temps	
new_temps = [old_temps[0]]
for i in range(0,len(new_delta_temps)):
	new_deltai = np.interp(new_temps[i],new_delta_temps[:,0],new_delta_temps[:,1])
	new_temp = new_temps[i] + new_deltai
	new_temps.append(new_temp)
	
plt.plot(old_temps)
plt.plot(new_temps)
plt.show()

