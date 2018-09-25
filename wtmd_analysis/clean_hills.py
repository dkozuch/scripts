#!/tigress/dkozuch/programs/conda/bin/python

import numpy as np
import os
from joblib import Parallel, delayed

#some hills files have repeated time points
#this file replaces old times with newest repeated time

nsims=28
os.system("mkdir hills_clean")

def clean_file(i):
	print "Loading file..."
	hills = np.loadtxt("hills."+str(i),comments=("#","@","!"))
	length = len(hills[:,0])
	print "Length of file: "+str(length)

	print "Cleaning file..."
	old_time = 0
	hills_clean = np.zeros((np.shape(hills)[0]+100,np.shape(hills)[1])) #add empty space at end, we delete the zeros anyways
	for j in hills:
		time = int(np.floor(j[0]))
		hills_clean[time] = j
		#check continuous
		if time != old_time + 1:
			print "Non-continuous time at time: "+str(time)
		old_time = time
		if time % 1000000 == 0:
			print str((time/float(length))*100)+" %"
	print "Removing zeros..."
	hills_clean = hills_clean[~np.all(hills_clean == 0, axis=1)]

	print "Saving file..."
	np.savetxt("hills_clean/hills_clean."+str(i),hills_clean,fmt='%23s %22s %22d %22s %22d', 
		   header="FIELDS time ene sigma_ene height biasf\nSET multivariate false",comments="#! ")

#inputs = range(0,nsims)
#Parallel(n_jobs=nsims)(delayed(clean_file)(i) for i in inputs)

clean_file(9)
