#!/tigress/dkozuch/programs/conda/bin/python

print "Loading packages..."
import numpy as np
#import matplotlib.pyplot as plt
import sys

cutoff = float(sys.argv[1]) #nm
t = 300 #K
bulk_chi = 0.00223

print "Cutoff = "+str(cutoff)+" (nm)"
print "T = "+str(t)+" (K)"

def calc_chi(count, sasa, t, cutoff):
	'''calculated compressibilit/hydrophobity paramter chi
	from Acharya2010'''
	mean = np.mean(count)
	var = np.var(count)
	chi1 = var/(mean**2)
	v = sasa*cutoff
	kt = 0.008314*t
	chi2 = (float(v)/float(kt))*chi1
	chi3 = float(chi2)/bulk_chi
	#print [chi1, chi2, chi3]
	return chi3	

def chi_block_avg(counts,sasa,begin,block):
	chi_list = []
	for i in range(begin,len(counts),block):
		block_i = counts[i:i+block]
		if len(block_i) != block:
			continue
		else:
			chi_i = calc_chi(block_i, sasa, t, cutoff)
			chi_list.append(chi_i)
	return np.array(chi_list)
	
sasa_time = np.loadtxt("sasa.xvg",comments=("#","@"))
sasa_mean = np.mean(sasa_time[:,1])
print "SASA: "+str(round(sasa_mean,3))+" (nm^2)"
counts = np.loadtxt("count_0.3nm.xvg",comments=("#","@"))[:,1]

begin = 10000 #discard first 10 ns
block = 10000 #10 ns blocks

print "Count mean: "+str(round(np.mean(counts[begin:]),3))
print "Count std.: "+str(round(np.std(counts[begin:]),3))

chi_list = chi_block_avg(counts,sasa_mean,begin,block)
#print "Chi list: "+str(chi_list)
chi_mean = round(np.mean(chi_list),3)
chi_error = round(np.std(chi_list),3)
print "Chi mean: "+str(chi_mean)
print "Chi std: "+str(chi_error)







