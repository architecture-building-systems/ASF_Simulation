
"""
===========================
Script for Handling Inputs (Weather files etc)
===========================
File history and credits:
Prageeth Jayathissa
Mario Frei
Jeremias Schmidli
Amr Elesawy 
"""

import sys, os
import numpy as np
import math
import csv
import pandas as pd
import matplotlib.pyplot as plt


#Constants.  FIX THIS: Bring the building properties before the input data and then read off building data
human_heat_emission=0.12 #[kWh] heat emitted by a human body per hour. Source: HVAC Engineers Handbook, F. Porges
floor_area=30 #[m^2] floor area


def read_EWP(epw_name):
	#Should be done later with Pandas, but for some reason I'ts not working

	
	T_out=[] #Open empty matrix for storing dry bulb temperature values
	glbRad=[] #Global radiation values
	glbIll=[]
	with open(epw_name, 'rb') as csvfile:
		weatherfile = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in weatherfile:
			if row[0].isdigit():
				T_out.append(row[6])
				glbRad.append(float(row[13]))
				glbIll.append(float(row[16]))
	return np.asarray(T_out),np.asarray(glbRad), np.asarray(glbIll)

def read_transmittedMonthlyR(myfilename='data/radiation_combination2.csv'):
	incRad=[] #Incident radiation through the window
	with open(my_filename, 'rb') as csvfile:
		radvalues= csvfile.read().split(',')

		#Some stupid script to convert the monthly data into yearly data
		#Its  however incorrect as it adds a day to february and subtracts one from August for simplification
		for ii in range(12):
		
			newlist=radvalues[24*ii:24*(ii+1)]
			if ii%2==0:
				incRad+=newlist*31
			else:
				if ii==1:
					incRad += newlist*29
				else:
					incRad += newlist*30
		incRad=np.asarray(incRad)	
		incRad=incRad.astype(np.float)
		incRad=incRad/30 #Approximately convert it back from the monthly average to a daily average
		Q_fenstRad=pd.DataFrame(incRad)


	return Q_fenstRad

def read_transmittedR(myfilename1):
	Q_fenstRad=pd.read_csv(myfilename1, header=None)
	Q_fenstRad= Q_fenstRad.transpose()
	return Q_fenstRad


def read_occupancy(myfilename2):
	#People: Average number of people per hour per m2
	#tintH_set: Temperature set point of the heating season, if negative then heating is disabled
	#tintC_set: Temperature set point for cooling season. Error: When does this turn on and off
	occupancy=pd.read_csv(myfilename2, nrows=8760)
	#print occupancy['tintH_set'].iat[100]
	Q_human=occupancy['People']*human_heat_emission*floor_area
	return occupancy, Q_human.transpose()



def Equate_Ill(epw_name):
	''' 
	Equation relating elluminance to irradiation.
	Input: epw weather file
	Output: eq, a vector of coefficients for a linear polynomial 
	'''

	To,glbRad, glbIll=read_EWP(epw_name) #Read EPW

	
	#Measured data for plotting
	X=glbRad
	Y=glbIll

	#Aquire best fit vector of coefficients. 1st order
	eq = np.polyfit(X,Y,1)

	#Vector for plotting the best fit
	x=np.arange(0,1000)


	#Plot results
	# fig=plt.figure()
	# plt.plot(glbRad,glbIll, 'o',x,x*eq[0]+eq[1],'r.')
	# plt.xlabel('Global Radiation (W/m2)')
	# plt.ylabel('Global Illuminance (lx)')
	#plt.show()

	return eq

#read_transmittedR(myfilename='data/radiation_Building_Madrid.csv')





	

