#26.10.2015
#Prageeth Jayathissa


#Function to read in .csv files and process data to obtain optimum angles

#Status: Under development

#Bugs: partition is not working, compare the results of this with a sort funciton




import numpy as np
import math
import matplotlib.pyplot as plt

path = "C:/Users/Assistenz/Documents/MT_Jeremias/Simulation_Data/Simulation_141216_729_comb_rectangular/"

#Function that takes a number from 0-2400 and outputs x and y angles

def decompose2Darray(m):
	a1=int(math.floor(m/49))
	a2=m%49
	(x1,y1)=convertTo_xy(a1)
	(x2,y2)=convertTo_xy(a2)
	return x1,y1,x2,y2


#Function that takes in a number from 0-48 and outputs x and y angles
def convertTo_xy(a):
	#Decompose angle index into x and y coordinates
	x=int(math.floor(a/7))*15
	y=(a%7)*15-45
	return (x,y)

#rewrite funciton for vector analysis
vecconvertTo_xy=np.vectorize(convertTo_xy)


def CheckMinEng(X,Xcolour='b'):
	for xx in X:
		Xind=range(0,X.shape[1])


		plt.scatter(Xind,xx, alpha=0.5, color=Xcolour)
	plt.scatter(Xind,minEng, alpha=0.5, color='r')
	plt.show()

def compareAngles(X):
	totalEng=np.sum(X, axis=1)
	bestStatic=np.argmin(totalEng)
	print convertTo_xy(bestStatic)
	print np.min(totalEng)

	Xind=range(0,X.shape[0])
	plt.scatter(Xind,totalEng)
	plt.show()
 
# this function finds minimum energy use at a fixed angle
def compareCHL(C,H,L):
    
	cool=np.sum(C,axis=1)
	heat=np.sum(H,axis=1)
	light=np.sum(L,axis=1)
	print 'cool ',np.amin(cool)
	print 'heat', np.amin(heat)
	print 'light', np.amin(light)





#Upload data from csv
C=np.genfromtxt(path + 'cooling.csv',delimiter=',')
H=np.genfromtxt(path + 'heating.csv',delimiter=',')
L=np.genfromtxt(path + 'lighting.csv',delimiter=',')

#Calculate the total Energy Consumption
E=C+H+L






minEng=np.amin(E,axis=0)
minInd=np.argmin(E,axis=0)
xy_ind=vecconvertTo_xy(minInd)

print C
print 'the sum is ', sum(minEng)

compareCHL(C,H,L)

compareAngles(E)





