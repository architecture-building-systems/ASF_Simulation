# -*- coding: utf-8 -*-
"""
Created on Tue Nov 01 16:05:31 2016

@author: Assistenz
"""

#Equation relating illuminance to irradiation.


import os, sys
import numpy as np
import json
import time
import warnings
import csv
import matplotlib.pyplot as plt
import pandas as pd

paths= {}

# define path of weather file:
paths['weather'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\WeatherData\Zuerich_Kloten_2013.epw' #paths['epw_name']

paths['main'] = os.path.abspath(os.path.dirname(sys.argv[0]))

# define paths of subfolders:
paths['data'] =os.path.join(paths['main'], 'data')
paths['python'] = os.path.join(paths['main'], 'python')
paths['aux_files'] = os.path.join(paths['python'], 'aux_files')
paths['radiation_wall'] = os.path.join(paths['main'],  'radiation_wall_illuminance')

# add python_path to system path, so that all files are available:
sys.path.insert(0, paths['python'] + '\\aux_files')
sys.path.insert(0, paths['python'])

from epwreader import epw_reader
#read epw file of needed destination
weatherData = epw_reader(paths['weather'])

  
glbRad = weatherData['glohorrad_Whm2']
glbIll = weatherData['glohorillum_lux']
#Measured data for plotting
X=glbRad
Y=glbIll

#Aquire best fit vector of coefficients. 1st order
Ill_Eq= np.polyfit(X,Y,1)
print Ill_Eq

monthi = 1
HOD = 12

RadiationData = {}
for x_angle in [0,45,90]:
    RadiationData [x_angle] = {}
    
    for y_angle in [-45,0,45]:
        RadiationData[x_angle][y_angle]= {}
 
        BuildingRadiationData = np.array([])


        with open(os.path.join(paths['radiation_wall'], 'RadiationWall' + '_' + str(int(HOD)) +'_'+ str(monthi) + '_'+ str(x_angle) + '_' + str(y_angle) + '.csv'), 'r') as csvfile:
           reader = csv.reader(csvfile)
           for idx,line in enumerate(reader):
               if idx == 1:
                   BuildingRadiationData = np.append(BuildingRadiationData, [float(line[0])])
                   break
        
        RadiationData[x_angle][y_angle]= BuildingRadiationData       

#
#fig = plt.figure()   
#with pd.plot_params.use('x_compat', True):
#     glbRad.plot(color='y')
#     
#plt.legend(loc='best')
#plt.xlabel('Hour of the year', fontsize=18)
#plt.ylabel('Rad', fontsize=16)
#
#
#fig = plt.figure()   
#with pd.plot_params.use('x_compat', True):
#     glbIll.plot(color='r')
#plt.legend(loc='best')
#plt.xlabel('Hour of the year', fontsize=18)
#plt.ylabel('ILL', fontsize=16)
#
#




x,y = [],[]

x.append (weatherData['glohorrad_Whm2'])
y.append (weatherData['glohorillum_lux'])
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(y,x,'o-')
plt.show()

#x1,y2 = [],[]
#x1.append (weatherData['dirnorrad_Whm2'])
#y2.append (weatherData['dirnorillum_lux'])
#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.plot(y,x,'o-')
#plt.show()
#


#Vector for plotting the best fit
x=np.arange(0,1000)

#data[xangle][month][HOD]

##Calculate Illuminance in the room. 
#fenstIll=BuildingRadiationData_HOY[hour_of_year][comb]*Ill_Eq[0] #Lumens.  Note that the constant has been ignored because it should be 0
#
##Illuminance after transmitting through the window 
#glass_light_transmittance = 0.744 # visible light transmittance window        
#TransIll=fenstIll*glass_light_transmittance

