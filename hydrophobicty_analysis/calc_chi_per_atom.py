#!/tigress/dkozuch/programs/conda/bin/python

print "Loading packages..."
import numpy as np
#import matplotlib.pyplot as plt

cutoff = 0.3 #nm
t = 300 #K
bulk_chi = 0.00223

def filename(i):
	filename = "count_0.3nm_id"+str(i)+".xvg"
	return filename

def get_sasa_a(sasa_filename):
	sasa_a = np.loadtxt(sasa_filename,comments=("#","@"))
	return sasa_a

def calc_chi(i, count, sasa_a, t, cutoff):
	'''calculated compressibilit/hydrophobity paramter chi
	from Acharya2010'''
	var = np.var(count)
	mean = np.mean(count)
	chi1 = var/(mean**2)
	sasa_ai = sasa_a[sasa_a[:,0] == i][0,1]
	v = sasa_ai*cutoff
	kt = 0.008314*t
	chi2 = (float(v)/float(kt))*chi1
	chi3 = float(chi2)/bulk_chi
	#print [chi1, chi2, chi3]
	return chi3

def calc_chi_list(num):

	print "Calculating chi for: "+str(num)+" atoms"
	block_size =	10000
	begin = 	20000
	end =		100000
	chi_list = []
	for i in range(1,num+1):
		print str(round((float(i)/num)*100,3))+" % ("+str(i)+"/"+str(num)+")"
		chi_listi = []
		counti = np.loadtxt(filename(i),comments=("#","@"))[:,1]
		for j in range(begin,end,block_size):
			countij = counti[j:j+block_size]
			chi = calc_chi(i,countij,sasa_a,t,cutoff)
			chi_listi.append(chi)
		chi_list.append(chi_listi)
	chi_list = np.array(chi_list)
	chi_list_avg = np.mean(chi_list,axis=1)
	chi_list_std = np.std(chi_list,axis=1)
	chi_list_num = np.array(range(1,len(chi_list_avg)+1))
	chi_final = np.column_stack((chi_list_num,chi_list_avg,chi_list_std))
	#print chi_final
	return chi_final	

def get_sasa_adj_chi(chi_list,sasa_a,cutoff):
	sasa_adj_chi_list = []
	for i in chi_list:
		index = int(i[0])
		sasa = sasa_a[sasa_a[:,0] == index][0,1]
		if sasa >= cutoff:
			sasa_adj_chi_list.append(i)
	return sasa_adj_chi_list

sasa_a = get_sasa_a("sasa_a.xvg")
num_atoms = len(sasa_a)
chi_list = calc_chi_list(num_atoms)
np.savetxt("chi.txt",chi_list,header="Atom index, Average Chi, Chi Error")
#chi_list = np.loadtxt("chi.txt")
clean_chi_list = np.nan_to_num(chi_list) #replace nan with zero, but need to keep rows so in line with sasa
chi_mean = np.mean(clean_chi_list[clean_chi_list[:,1] != 0][:,1]) #dont count zeros in mean
chi_error = np.mean(clean_chi_list[clean_chi_list[:,1] != 0][:,2])
print "Mean chi: "+str(chi_mean)+", Error: "+str(chi_error)

sasa_adjusted_chi = get_sasa_adj_chi(clean_chi_list,sasa_a,0.05)
sasa_adjusted_chi_mean = np.mean(sasa_adjusted_chi)
print "SASA adjusted chi: "+str(sasa_adjusted_chi_mean)





