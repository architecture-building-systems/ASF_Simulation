"""
Sandbox Code for testing planar projection code for solar analysis 

Author: Prageeth Jayathissa
Date: 27.01.2017


"""

import math
import numpy as np


def calcShadow(P0,sunAz,sunAlt,panelAz,panelAlt,h,d):
	

	#Calculate Centre of Shadow
	S0=[0,0] #initialise Centre of Shadow
	S0[0]=P0[0]+d*math.tan(sunAz)
	S0[1]=P0[1]-d*math.tan(sunAlt)


	#Calcuate the contraction or expansion of the shadow in the x and y directions due to the actuation
	#The difference is relative to the flat panel position
	y=(math.sin(sunAlt-panelAlt/2)/(math.sin(math.pi/2-sunAlt)))*h*math.sin(panelAlt/2) 

	x=(math.sin(sunAz-panelAz/2)/(math.sin(math.pi/2-sunAz)))*h*math.sin(panelAz/2)


	"""
	     S1
	    /\
	   /S0\
	S4 \' / S2
	    \/
	    S3  
	"""
	
	S1=S0[1]+h/2+y 
	S2=S0[0]+h/2+x
	S3=S0[1]-h/2-y
	S4=S0[0]-h/2-x


	return S0,S1,S2,S3,S4

	#Old Alternative Equations
	#shadowDistanceAlt= -h/2 -(d +  h * math.sin(panelAlt/2)*math.cos(panelAlt/2))*math.tan(sunAlt) + (h * math.sin(panelAlt/2) * math.sin(panelAlt/2) ) 

	#shadowDistanceAz= -h/2 -(d +  h * math.sin(panelAz/2)*math.cos(panelAz/2))*math.tan(sunAz) + (h * math.sin(panelAz/2) * math.sin(panelAz/2) ) 

if __name__ == "__main__":


	#The adaptive solar facade is represented by an array of coordinates and panel size
	panelSpacing=700 # in x y dirction[mm]

	xArray=4
	yArray=3
	ASFArray=[]
	for ii in range(0,yArray):
		ASFArray.append([])
		for jj in range (0,xArray):
			if ii%2==0:
				ASFArray[ii].append([ii*panelSpacing/2,jj*panelSpacing])
			else:
				if jj==xArray-1:
					pass
				else:
					ASFArray[ii].append([ii*panelSpacing/2,jj*panelSpacing+panelSpacing/2])
		

	print ASFArray

	P0=[0,0];
		#Sun Position

	sunAz=math.radians(40)
	sunAlt=math.radians(0)

	#Panel Position
	panelAz=math.radians(-10)
	panelAlt=math.radians(00)

	h=math.sqrt(2*(400/2)**2) #distance from centre of panel to corner [mm]
	d=300 #Distance from the Glazed Surface

	shadowData=[]
	for ii,row in enumerate(ASFArray):
		shadowData.append([])
		for jj,P in enumerate(row):
			S0,S1,S2,S3,S4=calcShadow(P,sunAz,sunAlt,panelAz,panelAlt,h,d)
			shadowData[ii].append([S0,S1,S2,S3,S4])
			
	print shadowData

	#S0,S1,S2,S3,S4=calcShadow(P0,sunAz,sunAlt,panelAz,panelAlt,h,d)



