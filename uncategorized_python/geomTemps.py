#import matplotlib.pyplot as plt

tmin = 170
tmax = 450
k = 1
temps = 72

def makeGeomList(k):
	tList = [tmin]
	while tList[-1] < tmax:
		newT = tList[-1]*(tmax/tmin)**k
		tList.append(newT)
	return tList

tList = makeGeomList(k)
while len(tList) < temps:
	k = k - 0.0001
	tList = makeGeomList(k)
	print len(tList)
	
print [k,tList]
for t in tList:
	if t == tmin:
		with open("tList.txt","w") as w:
                	w.write(str(round(t,3)) + " ")
	else:
		with open("tList.txt","a") as w:
			w.write(str(round(t,3)) + " ")

#plt.scatter(range(0,len(tList)), tList)
#plt.title('WTREMD Temperatures')
#plt.xlabel('Index')
#plt.ylabel('Temperature')
#plt.show()
