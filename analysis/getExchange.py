import numpy as np

#Used for calculating replica exchage rates from gromacs log file
#log file must be static (cannot be writing to log file while this is running as arrays are preallocated)
	
#filein is directory location of log file
#fileout is where the exchange matrix will get saved
filein = "1l2y_sim_tmp.log"
fileout = "replicaExchange.txt"
#number of replicas
reps = 28
#time to start at
start = 50000

#function returns 1:reps array with a one where exchange happended and zero where it did not
def readLogLine(lineSplit,reps):
	#Find position of "x" which indicates exchange
	xpos = [i for i, x in enumerate(lineSplit) if x == "x"]
	#Convert position of x to replica exchange index (i.e. value of 3 indicates exchange between replicas 3 and 4)
	xpos = [int(lineSplit[i-1]) for i in xpos]
			
	#Make array with ones where exchange happended
	exchange = np.zeros(reps - 1)
	for i in xpos:
		exchange[i] = 1
	return exchange

#count how many exchange lines - necessary to pre-allocate
lineCount = 0
time = 0
with open(filein,"r") as f:
	for line in f:
		lineSplit = line.split()
		#get time
		if len(lineSplit) > 1 and lineSplit[0:4] == ["Replica","exchange","at","step"]:
			time = float(lineSplit[6])
		#Read lines that star with "Repla ex"
		if time >= start:
			if len(lineSplit) > 1 and lineSplit[0] == "Repl" and lineSplit[1] == "ex":
				lineCount = lineCount + 1
			
print("Total number of exchanges: " + str(lineCount))
print("Calculating exchange probabilities...")

#pre-allocate array
exM = np.zeros((lineCount,reps-1))
time = 0
index = 0
with open(filein,"r") as f:
	for line in f:
		lineSplit = line.split()
		#get time
		if len(lineSplit) > 1 and lineSplit[0:4] == ["Replica","exchange","at","step"]:
			time = float(lineSplit[6])
		if time >= start:
			#Read lines that star with "Repla ex"
			if len(lineSplit) > 1 and lineSplit[0] == "Repl" and lineSplit[1] == "ex":
			
				#Build matrix of exchange arrays
				exM[index,:] = readLogLine(lineSplit,reps)
				index = index + 1
				
				if time % 10000 == 0:
					print time

#Remove any rows of zeros added for padding
exM = exM[~np.all(exM == 0, axis=1)]
#Find exchange ratios by summing columns (have to divide total by 2 since exchange are attempted on even/odd scheme)
exMS = np.sum(exM,axis=0)/(np.shape(exM)[0]/2)
print(exMS)
np.savetxt("exchange_prop.txt",exMS)
			

			
