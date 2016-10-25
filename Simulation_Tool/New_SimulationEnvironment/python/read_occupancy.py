# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 10:28:53 2016

@author: PJ
@credits: Mauro

"""

import pandas as pd
import numpy as np

#human_heat_emission=0.12 #[kWh] heat emitted by a human body per hour. Source: HVAC Engineers Handbook, F. Porges
#floor_area=30 #[m^2] floor area

def read_occupancy(myfilename, human_heat_emission, floor_area):
    
	#People: Average number of people per hour per m2
	#tintH_set: Temperature set point of the heating season, if negative then heating is disabled
	#tintC_set: Temperature set point for cooling season. Error: When does this turn on and off
	occupancy=pd.read_csv(myfilename, nrows=8760)
	#print occupancy['tintH_set'].iat[100]
	Q_human=occupancy['People']*human_heat_emission*floor_area*1000 #W
	return occupancy, Q_human.transpose()
 
 

def Equate_Ill(weatherData):
    ''' 
    Equation relating elluminance to irradiation.
    Input: epw weather file
    Output: eq, a vector of coefficients for a linear polynomial 
    '''
    glbRad = weatherData['glohorrad_Whm2']
    glbIll = weatherData['glohorillum_lux']
    #Measured data for plotting
    X=glbRad
    Y=glbIll

    #Aquire best fit vector of coefficients. 1st order
    eq = np.polyfit(X,Y,1)

    #Vector for plotting the best fit
    x=np.arange(0,1000)

    return eq
    
def BuildingData(R_extWall, R_window, FreshAir,People, roomFloorArea, roomVolume):
      
    U_exWall = 1/R_extWall #W/(m2*K)
    U_window = 1/R_window #W/(m2*K)        
    
    Ventilation = FreshAir * People *3600 * roomFloorArea #m3/h 
    Ventilation_per_hour = Ventilation/roomVolume # 1/m3
    
    return U_exWall,U_window, Ventilation_per_hour  
  
 


 