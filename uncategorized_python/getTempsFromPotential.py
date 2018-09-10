import numpy as np
import matplotlib.pyplot as plt

b=100

#get temps
old_temps = np.loadtxt("temps.txt")

reps = len(old_temps)

#get potentials
pot_avgs = []
for i in range(0,reps):
	poti = np.loadtxt("potential_files/potential_" + str(i) + ".xvg",comments=("#","@","@TYPE"))
	poti_avg = np.mean(poti[b:,1])
	pot_avgs.append(poti_avg)

pot_avgs = np.array(pot_avgs)
pot_avgs = np.column_stack((old_temps,pot_avgs))

#plt.plot(pot_avgs[:,0],pot_avgs[:,1])
#plt.show()

pot_min = np.min(pot_avgs[:,1])
pot_max = np.max(pot_avgs[:,1])
pot_step = (pot_max - pot_min)/float(reps-1)

new_pots = np.array(range(0,reps))*pot_step + pot_min
xp = pot_avgs[:,0]
fp = pot_avgs[:,1]

#print pot_max
#print new_pots[-1]

new_temps = np.interp(new_pots,fp,xp) #we are actually interpolating for x
np.savetxt("new_temps.txt",new_temps,fmt='%.3f')

# plt.plot(old_temps)
# plt.plot(new_temps)
# plt.show()

