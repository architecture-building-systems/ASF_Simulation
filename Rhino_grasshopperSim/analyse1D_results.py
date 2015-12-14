#23.10.2015
#Prageeth Jayathissa


#Function to read in .csv files and process data to obtain optimum angles

#Status: Under development

#Bugs: partition is not working, compare the results of this with a sort funciton




import numpy as np
import math
import matplotlib.pyplot as plt





#Function that takes in a number from 0-48 and outputs x and y angles
def convertTo_xy(a):
	#Decompose angle index into x and y coordinates
	x=int(math.floor(a/7))*15
	y=(a%7)*15-45
	return (x,y)

#rewrite funciton for vector analysis
vecconvertTo_xy=np.vectorize(convertTo_xy)


#Takes in the data, finds the minumum and plots it in a scatter plot
def scatterResults(X, Xcolour,offset):
	#ind=np.argpartition(X, 4, axis=0)[:4]
	ind=np.argmin(X,axis=0)
	xy_ind=vecconvertTo_xy(ind)
	xy_ind=np.add(xy_ind,offset)
	plt.scatter(xy_ind[0],xy_ind[1], alpha=0.01, color=Xcolour)

#Takes the data, finds the m number of minimum vales and plots
def scattermin4(X,Xcolour,offset=0,m=4):
	for ii in range(0, X.shape[1]):
		mintemp=np.partition(X[:,ii],m)[:m]
		tempind=np.argpartition(X[:,ii],m)[:m]
		xy_ind=vecconvertTo_xy(tempind)
		xy_ind=np.add(xy_ind,offset)
		plt.scatter(xy_ind[0],xy_ind[1], alpha=0.05, color=Xcolour, s=mintemp)
		# for label,x,y in zip(mintemp,xy_ind[0],xy_ind[1]):

		# 	plt.annotate(int(label), xy=(x,y), xytext=(x+ii/2,y+ii/2))


#Upload data from csv
C=np.genfromtxt('cooling.csv',delimiter=',')
H=np.genfromtxt('heating.csv',delimiter=',')
L=np.genfromtxt('lighting.csv',delimiter=',')



#Run the functions written above
scatterResults(C,'b',0)
scatterResults(H,'r',1)
scatterResults(L,'g',2)
#scatterResults(C+H+L,'k',3)
# m=1
# scattermin4(C,'b',0,m)
# scattermin4(H,'r',1,m)
# scattermin4(L,'g',2,m)

#Make the plot readable, and add axis labels
plt.xlim(-10,90)
plt.ylim(-50,50)
plt.ylabel('Y axis Angle')
plt.xlabel('X axis Angle')
plt.show()






















#Some extra code for debugging the results. Delete from here down
Cmin=np.amin(C, axis=0)
Cmax=np.amax(C, axis=0)

print np.size(Cmin)

xvals=np.arange(8761)

fig2, ax=plt.subplots()
width=.1

rects1=ax.bar(xvals,Cmin,width=width, color='r')
rects2=ax.bar(xvals+width,Cmax,width=width, color='b')

#plt.show()


