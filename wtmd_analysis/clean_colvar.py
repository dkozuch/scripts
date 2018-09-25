#!/tigress/dkozuch/programs/conda/bin/python

import numpy as np
import os
from joblib import Parallel, delayed

#some colvar files have repeated time points
#this file replaces old times with newest repeated time

nsims=28
os.system("mkdir colvar_clean")

def clean_file(i):
	print "Loading file..."
	colvar = np.loadtxt("colvar."+str(i),comments=("#","@","!","^@"))
	length = len(colvar[:,0])
	print "Length of file: "+str(length)

	print "Cleaning file..."
	time = -1
	colvar_clean = np.zeros(np.shape(colvar))
	for j in colvar:
		time = int(np.floor(j[0]))
		colvar_clean[time] = j
		if time % 1000000 == 0:
			print str((time/float(length))*100)+" %"
	print "Removing zeros..."
	colvar_clean = colvar_clean[~np.all(colvar_clean == 0, axis=1)]

	print "Saving file..."
	np.savetxt("colvar_clean/colvar_clean."+str(i),colvar_clean)

inputs = range(0,nsims)
Parallel(n_jobs=nsims)(delayed(clean_file)(i) for i in inputs)

#clean_file(12)
