"""
Sandbox Code for testing planar projection code for solar analysis 

Author: Prageeth Jayathissa
Date: 27.01.2017


"""

import math
import numpy as np
import matplotlib.pyplot as plt


def calcShadow(P0,sunAz,sunAlt,panelAz,panelAlt,h,d):
	

	#Calculate Centre of Shadow
	S0=[0,0] #initialise Centre of Shadow
	S0[0]=P0[0]+d*math.tan(sunAz)
	S0[1]=P0[1]-d*math.tan(sunAlt)


	#Calcuate the contraction or expansion of the shadow in the x and y directions due to the actuation
	#The difference is relative to the flat panel position
	y=(math.sin(sunAlt-panelAlt/2)/(math.sin(math.pi/2-sunAlt)))*h*math.sin(panelAlt/2) 
	print y
	x=(math.sin(sunAz-panelAz/2)/(math.sin(math.pi/2-sunAz)))*h*math.sin(panelAz/2)
	print x

	"""
	     S1
	    /\
	   /S0\
	S4 \' / S2
	    \/
	    S3  
	"""
	S1=[S0[0], S0[1]+h/2+y ]
	S2=[S0[0]+h/2+x,S0[1]]
	S3=[S0[0],S0[1]-h/2-y]
	S4=[S0[0]-h/2-x,S0[1]]

	# S1=S0[1]+h/2+y 
	# S2=S0[0]+h/2+x
	# S3=S0[1]-h/2-y
	# S4=S0[0]-h/2-x




	return S0,S1,S2,S3,S4

	#Old Alternative Equations
	#shadowDistanceAlt= -h/2 -(d +  h * math.sin(panelAlt/2)*math.cos(panelAlt/2))*math.tan(sunAlt) + (h * math.sin(panelAlt/2) * math.sin(panelAlt/2) ) 

	#shadowDistanceAz= -h/2 -(d +  h * math.sin(panelAz/2)*math.cos(panelAz/2))*math.tan(sunAz) + (h * math.sin(panelAz/2) * math.sin(panelAz/2) ) 

if __name__ == "__main__":

	#Set Panel Properties
	h=math.sqrt(2*(400/2)**2) #distance from centre of panel to corner [mm]
	d=300 #Distance from the Glazed Surface

	#Calculate ASF Geometry
	#The adaptive solar facade is represented by an array of coordinates and panel size
	panelSpacing=600 # in x y dirction[mm]

	xArray=4
	yArray=3
	ASFArray=[]
	for ii in range(0,yArray):
		ASFArray.append([])
		for jj in range (0,xArray):
			if ii%2==0:
				ASFArray[ii].append([jj*panelSpacing,ii*panelSpacing/2])
			else:
				if jj==xArray-1:
					pass
				else:
					ASFArray[ii].append([jj*panelSpacing+panelSpacing/2,ii*panelSpacing/2])
		
	#Set Sun Position
	sunAz=math.radians(20)
	sunAlt=math.radians(0)

	#Set Panel Position (note that this should be an array in the future)
	panelAz=math.radians(20)
	panelAlt=math.radians(0)



	#Calculate Shadow Pattern
	shadowData=[]
	for ii,row in enumerate(ASFArray):
		shadowData.append([])
		for jj,P in enumerate(row):
			S0,S1,S2,S3,S4=calcShadow(P,sunAz,sunAlt,panelAz,panelAlt,h,d)
			shadowData[ii].append([S1,S2,S3,S4])
			


	#Plot Data
	for ii,row in enumerate(shadowData):
		print 'new row'
		for jj, Shadow in enumerate(row):
			print Shadow
			x,y = zip(*Shadow)
			plt.scatter(x,y, c=np.random.rand(3,1))
			plt.axis('equal')

	
	plt.show()



	#S0,S1,S2,S3,S4=calcShadow([0,0],sunAz,sunAlt,panelAz,panelAlt,h,d)




