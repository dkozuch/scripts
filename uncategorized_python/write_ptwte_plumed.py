#!/usr/bin/env python

import sys,os,math,random
import numpy as np

Tlist = np.loadtxt("temps.txt")
NT = len(Tlist)

grid_min_ene = np.loadtxt("grid_min_potential.txt")
grid_max_ene = np.loadtxt("grid_max_potential.txt")

#grid_min_2 = 0
#grid_max_2 = 3

mdp_dir = "plumed"

if not os.path.exists(mdp_dir):
	os.mkdir(mdp_dir)

for i in range(NT):
	T = Tlist[i]
	filename = os.path.join("plumed/","plumed_PT."+str(i)+".dat")
	with open(filename,"w") as w:
		#w.write("WHOLEMOLECULES ENTITY0=1-304\n")
		w.write("ene: ENERGY\n")
		#w.write("d1: DISTANCE ATOMS=95,211 NOPBC\n")
		#w.write("rmsd: RMSD REFERENCE=1l2y_ref.pdb TYPE=OPTIMAL\n")
		w.write("METAD ...\n")
		w.write("LABEL=metad ARG=ene PACE=500 HEIGHT=1 SIGMA=200 FILE=hills BIASFACTOR=25.0\n")
		w.write("TEMP=" + str(T) + "\n")
		w.write("GRID_MIN=" + str(grid_min_ene[i]) + "\n")
		w.write("GRID_MAX=" + str(grid_max_ene[i]) + "\n")
		w.write("... METAD \n")
		w.write("PRINT STRIDE=500 ARG=ene,metad.bias FILE=colvar\n")
