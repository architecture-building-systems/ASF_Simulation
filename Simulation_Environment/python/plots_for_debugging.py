# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 20:16:42 2016

debugging plots

@author: Assistenz
"""

import matplotlib.pyplot as plt
import numpy as np
from auxFunctions import calculate_sum_for_index

#plt.plot(angle45_25-angle45_49)
#plt.plot(angle45_25)
#plt.plot(angle45_49)

#plt.figure()
#plt.plot(PV_electricity_results['Ins_avg'])
#plt.plot(PV_electricity_results['theoreticalMaxRad'])


R_max_ind = np.argmax(monthlyData['R_avg'],axis=0)
R_range = np.asarray(range(len(R_max_ind)))


shading = 1-monthlyData['R_avg'][R_max_ind, range(len(R_max_ind))]/monthlyData['R_theo'][R_max_ind, range(len(R_max_ind))]

where_are_NaNs = np.isnan(shading)
shading[where_are_NaNs] = 0

plt.figure()
#calculate_sum_for_index(monthly,Hind)
plt.subplot(3,1,1)
plt.plot(monthlyData['R_avg'][R_max_ind, range(len(R_max_ind))])
plt.plot(monthlyData['R_theo'][R_max_ind, range(len(R_max_ind))])

plt.subplot(3,1,2)
plt.plot(monthlyData['R_theo'][R_max_ind, range(len(R_max_ind))] - monthlyData['R_avg'][R_max_ind, range(len(R_max_ind))])

plt.subplot(3,1,3)
plt.plot(shading)

#plt.figure()

#for i in range(12):
#    plt.subplot(2,12,i+1)
#    plt.plot(monthlyData['R_avg'][R_max_ind[i*24:i*24+24], R_range[i*24:i*24+24]])
#    plt.plot(monthlyData['R_theo'][R_max_ind[i*24:i*24+24], R_range[i*24:i*24+24]])
#    
#    plt.subplot(2,12,i+13)
#    plt.plot(1-monthlyData['R_avg'][R_max_ind[i*24:i*24+24], R_range[i*24:i*24+24]]/monthlyData['R_theo'][R_max_ind[i*24:i*24+24], R_range[i*24:i*24+24]])
#    
