#!/tigress/dkozuch/programs/conda/bin/python

import numpy as np
import os
import sys

mol = sys.argv[1]

def pad(l,n):
        '''l is a list of a string, n is the allowed length of the resulting string'''
        if len(l) == n:
                return l
        if len(l) < n:
                pads = " "*(n - len(l))
                return pads + l
        if len(l) > n:
                print "Error: string longer that allotted space"
                return "Error: string longer that allotted space"

def round_special(n,l):
        '''n is the number being rounded, l is the number of characters allowed in the number'''
        length = len(list(str(int(round(n,0)))))
        if n > -1 and n < 0: #account for fact that -0.42 rounds to 0 instead of -0
                dec = l - length - 2
        else:
                dec = l - length - 1
        return "".join(list(str(round(n,dec)))[:l])

def edit_pdb(pdb_file,atom_type,data,tag):
        '''edit pdb file with occupancy column from data'''
        fileout = mol + "_" + tag + ".pdb"
        if os.path.isfile(fileout): 
		os.remove(fileout)

        with open(pdb_file, "r") as f:
                for line in f:
                        if line.split()[0] == atom_type:
                                atom_num = int(line.split()[1])
                                if atom_num in data[:,0]:
                                        tag = data[np.where(data[:,0] == atom_num)[0][0],1]
                                        if np.isnan(tag):
						tag = -1
					tag = round_special(tag,5)
                                else:
                                        tag = round_special(-1,5)
                                linelist=list(line)
                                linelist[56:59] = list(pad(tag,5))
                                newline = "".join(linelist)
                                with open(fileout,"a") as w:
                                        w.write(newline)
                        else:
                                with open(fileout,"a") as w:
                                        w.write(line)

chi = np.loadtxt("chi.txt")
edit_pdb(mol+"_min.pdb","ATOM",chi,"chi")
