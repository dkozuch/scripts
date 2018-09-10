#!/tigress/dkozuch/programs/conda/bin/python

import numpy as np
import sys
import os
from joblib import Parallel, delayed

property=sys.argv[1]
dir = property + "_colvar"
nsims=28
os.system("mkdir " + dir)

#make new colvar file for rewighting variables

def make_colvar(i):
	print("Loading data for system: " + str(i) + " and property: " + str(property))
	colvar = np.loadtxt("colvar_clean/colvar_clean." + str(i),comments=("#","@","@TYPE"))
	prop = np.loadtxt(property+"_files/"+property+"_"+str(i) + ".xvg",comments=("#","@","@TYPE"))
	length = min(len(prop[:,0]),len(colvar[:,0]))
	print("Printing " + str(length) + " lines...")
	#save times from prop file and colvar file so you can check things are matched correctly later
	out = np.column_stack((prop[:length,0],prop[:length,1],colvar[:length,0],colvar[:length,2])) #bias in third column of colvar file
	np.savetxt(property + "_colvar." + str(i),out, fmt='%.8e')
	os.system("mv " + property + "_colvar." + str(i) + " " + dir)
	
inputs = range(0,nsims)
Parallel(n_jobs=nsims)(delayed(make_colvar)(i) for i in inputs)
#for i in range(0,28):
#	make_colvar(i)	
	
	
