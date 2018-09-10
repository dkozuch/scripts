#!/tigress/dkozuch/programs/conda/bin/python

import numpy as np
import sys
import os
from joblib import Parallel, delayed

property1=sys.argv[1]
property2=sys.argv[2]
dir = property1 + "_" + property2 + "_colvar"
#nsims=1
os.system("mkdir " + dir)

#make new colvar file for rewighting variables

def make_colvar_2D(i):
	print("Loading data for system: " + str(i) + " and properties: " + property1+", "+property2)
	colvar = np.loadtxt("colvar_clean/colvar_clean." + str(i),comments=("#","@","@TYPE"))
	prop1 = np.loadtxt(property1+"_files/"+property1+"_"+str(i) + ".xvg",comments=("#","@","@TYPE"))
	prop2 = np.loadtxt(property2+"_files/"+property2+"_"+str(i) + ".xvg",comments=("#","@","@TYPE"))
        length = min(len(prop1[:,0]),len(prop2[:,0]),len(colvar[:,0]))
	print("Printing " + str(length) + " lines...")
	#save times from prop file and colvar file so you can check things are matched correctly later
	out = np.column_stack((prop1[:length,0],prop1[:length,1],prop2[:length,0],prop2[:length,1],colvar[:length,0],colvar[:length,2])) #bias in third column of colvar file
	np.savetxt(property1+"_"+property2+"_colvar."+str(i),out, fmt='%.8e')
	os.system("mv "+property1 + "_"+property2+"_colvar."+str(i)+" "+dir)
	
inputs = [22]
Parallel(n_jobs=len(inputs))(delayed(make_colvar_2D)(i) for i in inputs)	
	
