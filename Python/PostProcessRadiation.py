# -*- coding: utf-8 -*-
"""
Created on Tue Jan 05 17:25:56 2016

Analyse Radiation Results

@author: Jeremias Schmidli
"""

import numpy as np
import math
import matplotlib.pyplot as plt

#define if data should be imported, set False if desired radiation data is already in workspace:
importDataFlag = True

if importDataFlag:
    from ImportRadiationResults import import_radiation
    
    # define path and filename:
    path = "C:/Users/Assistenz/Documents/MT_Jeremias/Simulation_Data/RadiationEvaluation/"
    filename = 'RadiationResults.csv'
    
    # load simulation data:
    Radiation, total_radiation, panel_size = import_radiation(path, filename) 

averageRadiation = []
for i in Radiation:
    averageRadiation.append(np.sum(i)/len(i))

#plot average radiation for each panel:
#plt.rc('text', usetex=False)
#plt.rc('font', family='serif')
plt.plot(range(0,len(averageRadiation)),averageRadiation, 'bo')
plt.title('Average Radiation on Panels', size = 20)
plt.xticks(range(0,len(averageRadiation)),range(1,len(averageRadiation)+1))
plt.xlabel(r'panel number',size=16)
plt.ylabel(r'average radiation on panel $\left[\frac{kWh}{m^2 year}\right]$', size=16)
plt.grid(b=True, which='both')

#calculate total radiation:
totRadCal=sum(averageRadiation)*(panel_size/1000)**2

#compare ladybug total radiation with own calculation:
print 'total radiation calculated by ladybug:', total_radiation, 'kWh/year'
print 'total radiation calculated based on evaluation of all results: ',  totRadCal, 'kWh/year'