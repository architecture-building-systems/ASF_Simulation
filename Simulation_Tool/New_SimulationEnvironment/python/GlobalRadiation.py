# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 15:35:22 2016

@author: Mauro
"""

import os, sys
import matplotlib.pyplot as plt
import pandas as pd
import math

# create dictionary to write all paths:
paths = {}

# find path of current folder (simulation_environment)
paths['main'] = os.path.abspath(os.path.dirname(sys.argv[0]))


# define path of weather file:
paths['ZH2013'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\WeatherData\Zuerich-Kloten_2013.epw'
paths['ZH2005'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\WeatherData\Zuerich-Kloten_2005.epw'
paths['GE'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\WeatherData\CHE_Geneva.067000_IWEC.epw'
paths['FR'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\WeatherData\DEU_Frankfurt.am.Main.106370_IWEC.epw'


from epwreader import epw_reader
#read epw file of needed destination
weatherDataZH13 = epw_reader(paths['ZH2013'])
weatherDataZH05 = epw_reader(paths['ZH2005'])
weatherDataGE = epw_reader(paths['GE'])
weatherDataFR = epw_reader(paths['FR'])



fig = plt.figure() 
fig.suptitle('GlobalRadiation', fontsize=20)
        
with pd.plot_params.use('x_compat', True):
    weatherDataZH13['drybulb_C'].plot(color='r')
    weatherDataZH05['drybulb_C'].plot(color='g') 


plt.legend(loc='best')
plt.xlabel('Hour of the year', fontsize=18)
plt.ylabel('Temperatur [°C]', fontsize=16)
"""
weatherDataZH['dirnorrad_Whm2']
weatherDataZH['difhorrad_Whm2']
sumDir = 0
sumDif = 0

sumHours = [  744.,  1416.,  2160.,  2880.,  3624.,  4344.,  5088.,  5832.,  6552.,  7296., 8016.,  8760.]


for HOD in range(12,13):
    for ii in range(0,31):             
        DAY = ii*24 + HOD 
        sumDir += weatherDataZH['dirnorrad_Whm2'][DAY]
        sumDif += weatherDataZH['difhorrad_Whm2'][DAY]
        
angle = (19.2 +24.5)/2
print angle
RadAngle = math.radians(angle)
resultAngle = math.cos(RadAngle)

PI = 3.141

Radiation = (sumDir*resultAngle + sumDif)/1000 #kWh/m2 
Radiation2 = (sumDir*math.cos(RadAngle)/math.sin(RadAngle) + sumDif*0.5)/1000 #kWh/m2

area = 48 * 0.4* 0.4 #m2

print "Jan", Radiation*area, "kWh"
print "Jan", Radiation2 * area, "kWh, methode from script"

#
#passedHours = 1416 # Jan and Feb are passed
#for HOD in range(12,13):
#    for ii in range(0,31):             
#        DAY = ii*24 + HOD + passedHours   
#        sumDir += weatherDataZH['dirnorrad_Whm2'][DAY]
#        sumDif += weatherDataZH['difhorrad_Whm2'][DAY]
#        
#angle = (34.25 +46.16)/2 #solar altitude anlge
#RadAngle = math.radians(angle)
#resultAngle = math.cos(RadAngle)
#
#Radiation = (sumDir*resultAngle + sumDif)/1000 #kWh/m2
#
#area = 48 * 0.4* 0.4 #m2
#
#print "März", Radiation*area, "kWh"
"""