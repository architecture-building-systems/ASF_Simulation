# -*- coding: utf-8 -*-
"""
Created on Wed Mar 09 16:07:51 2016

@author: Assistenz
"""

import numpy as np
import matplotlib.pyplot as plt
import json

from average_monthly import average_monthly, daysPassedMonth


path = "C:/Users/Assistenz/Documents/MT_Jeremias/Simulation_Data/RadiationEvaluation/"

Temperature=np.genfromtxt(path + 'Temperature.csv',delimiter=',', skiprows = 2)
Temperature = Temperature[np.newaxis, :]

daysPassedMonth, daysPerMonth = daysPassedMonth()
    
Temp_month = average_monthly(Temperature, daysPassedMonth, daysPerMonth)

plt.figure()
plt.plot(range(len(Temp_month[0])),Temp_month[0])