#!/tigress/dkozuch/programs/conda/bin/python

print "Loading packages..."
import numpy as np
import sys

filename = sys.argv[1]
print "Loading file: "+filename
data = np.loadtxt(filename,comments=("#","@"))
length = len(data)
print "File has: "+str(length)+" values"
print ""

print "Checking file..."
time = -1
error_count = 0
for i in data:
	newTime = int(i[0])
        delta = newTime - time
	if delta != 1 and delta != 0:
		print "Error: time "+str(newTime)+" is not consistent (delta) = "+str(delta)
		error_count = error_count +1 
	time = newTime
	if time % 100000 == 0:
		print str((time/float(length))*100)+" %"
	if error_count > 10:
		break
