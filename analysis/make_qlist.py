#!/usr/bin/env python

#makes q (contact list) file
#use the following for post processing
#	awk 'BEGIN{c=1}{print "ATOMS"c"="$1","$2, " SWITCH"c"={Q R_0=0.01 BETA=50.0 LAMBDA=1.5 REF="$3/10"} WEIGHT"c"=0.00315457413249211"; c++}' q.dat > template

import sys,os,math,string

if len(sys.argv) == 3:
        aa_pdblines = open(sys.argv[1]).readlines()
        outfile = open(sys.argv[2], 'w')
else:
        print("Usage: ./make_qlist.py structurefile.pdb outfilename.dat")
        sys.exit(0)

 
#this has no error checking 
fudge = float(raw_input("Fudge Factor:  "))
cutoff = float(raw_input("Cutoff (Angstroms):  "))
excl = float(raw_input("Minimum number of bonds between atoms to be counted: "))
listtype=str.strip(raw_input( "Please respond with one of the letter options below\n(Note that trplists are only useful when more than one TRP is present):\n\tAll-Atom (aa)\n\tBackbone (bb)\n\tSide-Chain (sc) \n\tNative Hydrogen Bond (hb)\n\tNon-native Hydrogen Bond (nn)\n\tTryptophan residues, native (trp)\n\tTryptophan residues, nonnative (trpnn)\n\tTurn List (Hydrogen Bonds) (tlh)\n\tTurn list (all atom) (tla) :"))

#Turn List details
if listtype.strip() == "tla" or listtype.strip() == "tlh":
	#defines turn as 4 central residues in peptide of user given length
	peplength = int(raw_input("How many residues are in your peptide (turn will be assumed to be 4 residues and symmetric "))
	turnstart = (peplength/2) - 1	

#TRP List Details
if listtype.strip() in ["trp", "trpnn"]:
	trptype = str.strip(raw_input("Create list for all TRP contacts (all) or residue pairs (pairs)?\n\t:"))
	if trptype =="pairs":
		trpres1 = int(raw_input("First TRP residue number: "))
		trpres2 = int(raw_input("Second TRP residue number: "))

xyz = []
res = []
ind = []
donor_list = []
acceptor_list = []
hblist = []

#these could be altered to search for any specific residue's side chains (or any other choice by residue) 
#as is done for the trp case


#create list of all possible Qlist atoms
for line in aa_pdblines:
	if line[0:6] != "ATOM  ":
		continue
	atom = line[12:16].strip()
	resid = line[17:20].strip()
	resnum = int(line[22:26].strip())

	if listtype == "aa": 
		if atom.strip()[0] != "H":
			X = float(line[30:38])
			Y = float(line[38:46])
			Z = float(line[46:54])
			xyz.append((X,Y,Z))
			ind.append(int(line[6:11]))
			res.append(int(line[22:26]))
	elif listtype == "bb":
		if atom.strip() in [ "CA", "C", "N", "O" ]:
	                X = float(line[30:38])
 			Y = float(line[38:46])
			Z = float(line[46:54])
	                xyz.append((X,Y,Z))
              		ind.append(int(line[6:11]))
		        res.append(int(line[22:26]))
	elif listtype == "sc":
	        if atom.strip() not in [ "CA", "C", "N", "O" ]:
			X = float(line[30:38])
		        Y = float(line[38:46])
	                Z = float(line[46:54])
	                xyz.append((X,Y,Z))
               		ind.append(int(line[6:11]))
	                res.append(int(line[22:26]))
        elif listtype in ["trp", "trpnn"]:
                if resid.strip() in ["TRP"] and atom.strip() not in [ "CA", "C", "N", "O" ]:
       	                X = float(line[30:38])
               	        Y = float(line[38:46])
                       	Z = float(line[46:54])
			resnum = int(line[23:26])
			if trptype=="pairs":
				if resnum in [trpres1, trpres2]:
		               	        xyz.append((X,Y,Z))
               		        	ind.append(int(line[6:11]))
	               	        	res.append(int(line[22:26]))
			elif trptype=="all":
			       xyz.append((X,Y,Z))
                               ind.append(int(line[6:11]))
                               res.append(int(line[22:26]))

	elif listtype == "tla":
		if resnum in range(turnstart,(turnstart+4)):
			if atom.strip()[0] != "H":
	                        X = float(line[30:38])
        	                Y = float(line[38:46])
               	 	        Z = float(line[46:54])
                        	xyz.append((X,Y,Z))
	                        ind.append(int(line[6:11]))
        	                res.append(int(line[22:26]))
	elif listtype == "tlh":
                if resnum in range(turnstart,(turnstart+4)):
	                if atom in [ "H", "HN" ]:
	                        X = float(line[30:38])
	                        Y = float(line[38:46])
	                        Z = float(line[46:54])
	                        ind = int(line[6:11])
	       	                res = int(line[22:26])
       		                donor_list.append((ind,res,X,Y,Z))
	                elif atom in [ "O" ]:
	                        X = float(line[30:38])
	                        Y = float(line[38:46])
	                        Z = float(line[46:54])
	                        ind = int(line[6:11])
	                        res = int(line[22:26])
	                        acceptor_list.append((ind,res,X,Y,Z))

# define native hydrogen bonds using NH--OC distance (usually < 2.8 Angstrom)

#for Hydrogen bonds, create donor and acceptor lists
	elif listtype in ["hb", "nn"]:
	        if atom in [ "H", "HN" ]:
	                X = float(line[30:38])
              		Y = float(line[38:46])
	                Z = float(line[46:54])
               		ind = int(line[6:11])
 	                res = int(line[22:26])
	                donor_list.append((ind,res,X,Y,Z))
	        elif atom in [ "O" ]:
             		X = float(line[30:38])
		        Y = float(line[38:46])
                	Z = float(line[46:54])
	                ind = int(line[6:11])
	                res = int(line[22:26])
	                acceptor_list.append((ind,res,X,Y,Z))

if donor_list:
	print str(len(donor_list)) + " h"
else:
	print str(len(ind))

#For hydrogen bond lists check to see if all possible donors/acceptors are within cutoff or for nonnative if outside cutoff
if listtype in ["hb","nn","tlh"]:	
	for d in donor_list:
	        ind_don,res_don,X_don,Y_don,Z_don = d
	        for a in acceptor_list:
	                ind_acc,res_acc,X_acc,Y_acc,Z_acc = a
       		        if abs(res_don-res_acc)>excl:
	                        dX = X_don-X_acc;
	                        dY = Y_don-Y_acc;
	                        dZ = Z_don-Z_acc;
	                        r_da = math.sqrt(dX**2+dY**2+dZ**2)
		     	        if listtype =="hb" or listtype =="tlh":   
					if r_da < cutoff:
       		 	                        outfile.write("%5i %5i %8.3f\n"%(ind_don,ind_acc,cutoff*fudge))
				elif listtype=="nn":
					if r_da > cutoff*fudge:
 						outfile.write("%5i %5i %8.3f 1.0\n"%(ind_don,ind_acc,cutoff*fudge))

#For other lists calculate distance between all pairs of residue atoms 
else:
	natom = len(xyz)

	for i in range(natom-1):
		iX,iY,iZ = xyz[i]
		iind = ind[i]
		ires = res[i]
		for j in range(i+1,natom):
			jX,jY,jZ = xyz[j]
			jind = ind[j]
			jres = res[j]
			if abs(ires-jres)>excl:
				dX = iX-jX
				dY = iY-jY
				dZ = iZ-jZ
				rij = math.sqrt(dX**2+dY**2+dZ**2)
				if listtype=="trpnn":
					if rij > cutoff:
	                                        outfile.write("%5i %5i %8.3f\n"	%(iind,jind,rij*fudge))
				else:
					if rij < cutoff:
						outfile.write("%5i %5i %8.3f\n"%(iind,jind,rij*fudge))


outfile.close()
