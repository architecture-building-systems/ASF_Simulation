"""
Sandbox Code for testing planar projection code for solar analysis 

Author: Prageeth Jayathissa
Date: 27.01.2017


"""

import math
import numpy as np
import matplotlib.pyplot as plt
import time


def calcShadow(P0,sunAz,sunAlt,panelAz,panelAlt,h,d):
	"""
	Cacluates the shadow of a single panel 
	Takes the Sun position (Azimuth and Altitude angles)
		and panel orientation (Azimuth and Altitude angles) as an input
	Returns the coordinates of the ASF corner in (x,y) coordinate space
	"""

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


	return S0,S1,S2,S3,S4


def calcASFGeo(panelSpacing,xArray,yArray):
	"""
	Calcuates the coordinates of the centre of each ASF panel
	Input: Spacing between panels in the x,y direction, 
			number of panels in the x direction
			number of panels in the y direction
	Output: Nested List of (x,y) coordinates 
	"""
	#Calculate ASF Geometry
	#The adaptive solar facade is represented by an array of coordinates and panel size

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
	return ASFArray

def calcShadedPattern(ASFArray,sunAz,sunAlt,panelAz,panelAlt):
	"""
	Calculates the Shadow of the entire ASF array 
	Input: Sun position (Altitude and Azimuth angles)
			angles of all panels (Altitude and Azimuth)
			Array of ASF Geometry
	Calls: calcShadow 
	Returns: Array of corner positions that can then be plotted
	"""		

	#Calculate Shadow Pattern
	shadowData=[]
	for ii,row in enumerate(ASFArray):
		shadowData.append([])
		for jj,P in enumerate(row):
			S0,S1,S2,S3,S4=calcShadow(P,sunAz,sunAlt,panelAz,panelAlt,h,d)
			shadowData[ii].append([S1,S2,S3,S4])
	return shadowData


if __name__ == "__main__":


	#Set Panel Properties
	h=math.sqrt(2*(400/2)**2) #distance from centre of panel to corner [mm]
	d=300 #Distance from the Glazed Surface

	#Generate ASF Array
	ASFArray= calcASFGeo(panelSpacing=600, xArray=4, yArray=3)

	#Calculate array of Shadow Data
	shadowData=calcShadedPattern(ASFArray=ASFArray,
									sunAz=math.radians(00),
									sunAlt=math.radians(0),
									panelAz=math.radians(0),
									panelAlt=math.radians(45))

			
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




