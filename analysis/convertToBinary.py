import numpy as np

filein = "replica_temp.xvg"
fileout = "replica_temp.npy"

print("Loading file...")
m = np.loadtxt(filein)
print("Writing file...")
np.save(fileout,m)
