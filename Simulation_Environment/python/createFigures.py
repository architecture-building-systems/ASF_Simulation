# -*- coding: utf-8 -*-
"""
Created on Fri Apr 01 10:57:20 2016

Create Figures Functions

@author: Assistenz
"""

#import numpy as np
import matplotlib.pyplot as plt

#from average_monthly import sum_monthly, average_monthly, daysPassedMonth
##from PostProcessThermal_functions import pcolorMonths, pcolorEnergyMonths
#from try_nan_values import createMonthsNan
#from plotDataFunctions import pcolorMonths



def createCarpetPlots(plotFunction, monthlyData, rotation_axis):
     # Optimal x- and y-angle combinations for every hour of the year
    
    if rotation_axis == 'xy':
        angles = monthlyData['angles']['allAngles'][0]    
    elif rotation_axis == 'x':
        angles = monthlyData['angles']['x_angles']    
    elif rotation_axis == 'y':
        angles = monthlyData['angles']['y_angles']    
    else:
        raise ValueError('rotation_axis does not exist')
        
    
    fig = plt.figure(figsize=(16, 8))
    plt.suptitle("(a) Optimum Altitude and Azimuth Orientation", size=16)
    plt.subplot(2,3,1)
    arg = ['min','H', rotation_axis, 'DIVA']
    plotFunction(monthlyData, arg)
    plt.title("Heating Demand")
    plt.ylabel("Hour of the Day",size=14)
    plt.subplot(2,3,2)
    arg = ['min','C', rotation_axis, 'DIVA']
    plotFunction(monthlyData, arg)
    plt.title("Cooling Demand")
    plt.subplot(2,3,3)
    arg = ['min','L', rotation_axis, 'DIVA']
    plotFunction(monthlyData, arg)
    plt.title("Lighting Demand")
    plt.subplot(2,3,4)
    arg = ['min','PV', rotation_axis, 'LB']
    plotFunction(monthlyData, arg)
    plt.title("PV Supply")
    plt.xlabel("Month of the Year",size=14)
    plt.ylabel("Hour of the Day",size=14)
    plt.subplot(2,3,5)
    arg = ['min','E_HCL', rotation_axis, 'DIVA']
    plotFunction(monthlyData, arg)
    plt.title("Total Thermal/Lighting Demand")
    plt.xlabel("Month of the Year",size=14)
    plt.subplot(2,3,6)
    arg = ['min','E_tot', rotation_axis, 'DIVA']
    plotFunction(monthlyData, arg)
    plt.title("Net Demand including PV")
    plt.xlabel("Month of the Year",size=14)
    fig.subplots_adjust(right=0.8)
    #cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    cbar_ax = fig.add_axes([0.85, 0.1, 0.05, 0.78])
    #cbart = plt.title("Altitude / Azimuth", fontsize=14, loc='left', verticalalignment = 'bottom')
    cbart = plt.title("Altitude / Azimuth", fontsize=14)
    cbart.set_position((1.1,1.02))
    cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(angles)))
    cbar.ax.set_yticklabels(angles)
    #cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(allAngles[0])))
    #cbar.ax.set_yticklabels(AnglesString)
    cbar.ax.tick_params(labelsize=14)
    plt.show()   
#
#if not (('figcounter' in locals()) or ('figcounter' in globals())):
#    figcounter = 0
#    
#
# # Optimal x-angle combinations for every hour of the year
#figcounter+=1
#fig = plt.figure(num = figcounter, figsize=(16, 12))
#plt.suptitle("Angle Distribution around x-axis", size=16)
#p1 = plt.subplot(2,3,1)
#pcolorMonths(H_month, 'x', x_angle_location, y_angle_location, allAngles, sunMask)
#plt.title("Heating Demand")
#p1 = plt.subplot(2,3,2)
#pcolorMonths(C_month, 'x', x_angle_location, y_angle_location, allAngles, sunMask)
#plt.title("Cooling Demand")
#p1 = plt.subplot(2,3,3)
#pcolorMonths(L_month, 'x', x_angle_location, y_angle_location, allAngles, sunMask)
#plt.title("Lighting Demand")
#p1 = plt.subplot(2,3,4)
#pcolorMonths(R_month, 'x', x_angle_location, y_angle_location, allAngles, sunMask, 'max')
#plt.title("PV Electricity Production")
#p1 = plt.subplot(2,3,5)
#pcolorMonths(E_month, 'x', x_angle_location, y_angle_location, allAngles, sunMask)
#plt.title("Total Thermal/Lighting Demand")
#p1 = plt.subplot(2,3,6)
#pcolorMonths(E_month_withPV, 'x', x_angle_location, y_angle_location, allAngles, sunMask)
#plt.title("Net Demand with PV")
#fig.subplots_adjust(right=0.8)
#cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(x_angles)))
#cbar.ax.set_yticklabels(x_angles)
#plt.show()   
#    
#    
# # Optimal y-angle combinations for every hour of the year
#figcounter+=1
#fig = plt.figure(num = figcounter, figsize=(16, 12))
#plt.suptitle("Angle Distribution around y-axis", size=16)
#p1 = plt.subplot(2,3,1)
#pcolorMonths(H_month, 'y', x_angle_location, y_angle_location, allAngles, sunMask)
#plt.title("Heating Demand")
#p1 = plt.subplot(2,3,2)
#pcolorMonths(C_month, 'y', x_angle_location, y_angle_location, allAngles, sunMask)
#plt.title("Cooling Demand")
#p1 = plt.subplot(2,3,3)
#pcolorMonths(L_month, 'y', x_angle_location, y_angle_location, allAngles, sunMask)
#plt.title("Lighting Demand")
#p1 = plt.subplot(2,3,4)
#pcolorMonths(R_month, 'y', x_angle_location, y_angle_location, allAngles, sunMask, 'max')
#plt.title("PV Electricity Production")
#p1 = plt.subplot(2,3,5)
#pcolorMonths(E_month, 'y', x_angle_location, y_angle_location, allAngles, sunMask)
#plt.title("Total Thermal/lighting Demand")
#p1 = plt.subplot(2,3,6)
#pcolorMonths(E_month_withPV, 'y', x_angle_location, y_angle_location, allAngles, sunMask)
#plt.title("Net Demand with PV")
#fig.subplots_adjust(right=0.8)
#cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(y_angles)))
#cbar.ax.set_yticklabels(y_angles)
#plt.show()   
#
# # Optimal x- and y-angle combinations for every hour of the year
#figcounter+=1
#fig = plt.figure(num = figcounter, figsize=(16, 12))
#plt.suptitle("(a) optimal altitude and azimuth orientation", size=16)
#p1 = plt.subplot(2,3,1)
#pcolorMonths(H_month, 'xy', x_angle_location, y_angle_location, allAngles, sunMask)
#plt.title("Heating Demand")
#p1 = plt.subplot(2,3,2)
#pcolorMonths(C_month, 'xy', x_angle_location, y_angle_location, allAngles, sunMask)
#plt.title("Cooling Demand")
#p1 = plt.subplot(2,3,3)
#pcolorMonths(L_month, 'xy', x_angle_location, y_angle_location, allAngles, sunMask)
#plt.title("Lighting Demand")
#p1 = plt.subplot(2,3,4)
#pcolorMonths(R_month, 'xy', x_angle_location, y_angle_location, allAngles, sunMask, 'max')
#plt.title("PV Electricity Production")
#p1 = plt.subplot(2,3,5)
#pcolorMonths(E_month, 'xy', x_angle_location, y_angle_location, allAngles, sunMask)
#plt.title("Total Thermal/lighting Demand")
#p1 = plt.subplot(2,3,6)
#pcolorMonths(E_month_withPV, 'xy', x_angle_location, y_angle_location, allAngles, sunMask)
#plt.title("Net Demand with PV")
#fig.subplots_adjust(right=0.8)
#cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(allAngles[0])))
#cbar.ax.set_yticklabels(allAngles[0])
#plt.show()   
#
#
##
### Optimal x-angle combinations for every hour of the year
##figcounter+=1
##fig = plt.figure(num = figcounter, figsize=(16, 12))
##plt.suptitle("Angle Distribution around x-axis", size=16)
##p1 = plt.subplot(2,2,1)
##pcolorMonths(H_month, 'x', x_angle_location, y_angle_location, allAngles)
##plt.title("Heating Demand")
##p1 = plt.subplot(2,2,2)
##pcolorMonths(C_month, 'x', x_angle_location, y_angle_location, allAngles)
##plt.title("Cooling Demand")
##p1 = plt.subplot(2,2,3)
##pcolorMonths(L_month, 'x', x_angle_location, y_angle_location, allAngles)
##plt.title("Lighting Demand")
##p1 = plt.subplot(2,2,4)
##pcolorMonths(E_month, 'x', x_angle_location, y_angle_location, allAngles)
##plt.title("Total Energy Demand")
##fig.subplots_adjust(right=0.8)
##cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
##cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(x_angles)))
##cbar.ax.set_yticklabels(x_angles)
##plt.show()
##
### Optimal y-angle combinations for every hour of the year
##figcounter+=1
##fig = plt.figure(num = figcounter, figsize=(16, 12))
##plt.suptitle("Angle Distribution around y-axis", size=16)
##plt.subplot(2,2,1)
##pcolorMonths(H_month, 'y', x_angle_location, y_angle_location, allAngles)
##plt.title("Heating Demand")
##plt.subplot(2,2,2)
##pcolorMonths(C_month, 'y', x_angle_location, y_angle_location, allAngles)
##plt.title("Cooling Demand")
##plt.subplot(2,2,3)
##pcolorMonths(L_month, 'y', x_angle_location, y_angle_location, allAngles)
##plt.title("Lighting Demand")
##plt.subplot(2,2,4)
##pcolorMonths(E_month, 'y', x_angle_location, y_angle_location, allAngles)
##plt.title("Total Energy Demand")
##fig.subplots_adjust(right=0.8)
##cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
##cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(y_angles)))
##cbar.ax.set_yticklabels(y_angles)
##plt.show()
##
##figcounter+=1
##fig = plt.figure(num = figcounter, figsize=(16, 12))
##plt.suptitle("Angle Distribution around x and y axis", size=16)
##p1 = plt.subplot(2,2,1)
##pcolorMonths(H_month, 'xy', x_angle_location, y_angle_location, allAngles)
##plt.title("Heating Demand")
##p1 = plt.subplot(2,2,2)
##pcolorMonths(C_month, 'xy', x_angle_location, y_angle_location, allAngles)
##plt.title("Cooling Demand")
##p1 = plt.subplot(2,2,3)
##pcolorMonths(L_month, 'xy', x_angle_location, y_angle_location, allAngles)
##plt.title("Lighting Demand")
##p1 = plt.subplot(2,2,4)
##pcolorMonths(E_month, 'xy', x_angle_location, y_angle_location, allAngles)
##plt.title("Total Energy Demand")
##fig.subplots_adjust(right=0.8)
##cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
##plt.title("(x-angle, y-angle)", fontsize=12, loc='left', verticalalignment = 'bottom')
##cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(allAngles[0])))
##cbar.ax.set_yticklabels(allAngles[0])
##plt.show()
#
### Energy Use at opmtimum angle combination for the hole year:
##figcounter+=1
##fig = plt.figure(num = figcounter, figsize=(16, 12))
##plt.suptitle("Energy Use at optimum angle combination", size=16)
##plt.subplot(2,2,1)
##pcolorEnergyMonths(H_month)
##plt.title("Heating Demand")
##plt.subplot(2,2,2)
##pcolorEnergyMonths(C_month)
##plt.title("Cooling Demand")
##plt.subplot(2,2,3)
##pcolorEnergyMonths(L_month)
##plt.title("Lighting Demand")
##plt.subplot(2,2,4)
##pcolorEnergyMonths(E_month)
##plt.title("Total Energy Demand")
##fig.subplots_adjust(right=0.8)
##cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
##cbar = plt.colorbar(cax=cbar_ax, ticks=np.asarray(range(0,int(E_month.max()))))
##cbar.set_label('Power Use in kWh', rotation=270, labelpad=20)
##plt.show()
#
## Energy Use at opmtimum angle combination for the hole year:
#figcounter+=1
#fig = plt.figure(num = figcounter, figsize=(16, 12))
#plt.suptitle("Net Energy Use at optimum angle combination", size=16)
#plt.subplot(2,3,1)
#pcolorEnergyMonths(H_month,'min')
#plt.title("Heating Demand")
#plt.ylabel("Hour of the Day")
#plt.subplot(2,3,2)
#pcolorEnergyMonths(C_month,'min')
#plt.title("Cooling Demand")
#plt.subplot(2,3,3)
#pcolorEnergyMonths(L_month,'min')
#plt.title("Lighting Demand")
#plt.subplot(2,3,4)
#pcolorEnergyMonths(-PV_month,'min')
#plt.title("PV Production")
#plt.xlabel("Month of the Year")
#plt.ylabel("Hour of the Day")
#plt.subplot(2,3,5)
#pcolorEnergyMonths(E_month,'min')
#plt.title("Thermal/Lighting Demand")
#plt.xlabel("Month of the Year")
#plt.subplot(2,3,6)
#pcolorEnergyMonths(E_month_withPV,'min')
#plt.title("Net Energy Demand")
#plt.xlabel("Month of the Year")
#fig.subplots_adjust(right=0.8)
#cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
##cbar = plt.colorbar(cax=cbar_ax, ticks=np.asarray(range(0,int(E_month.max()))))
##○cbar = plt.colorbar(cax=cbar_ax, ticks=np.asarray(range(0,30)))
#cbar = plt.colorbar(cax=cbar_ax)
#cbar.set_label('Net Energy Use in kWh', rotation=270, labelpad=20)
#plt.show()
#
## Energy Use at fixed angle combination for the hole year:
#combination=12
#figcounter+=1
#fig = plt.figure(num = figcounter, figsize=(16, 12))
#plt.suptitle("Energy Use at combination " + str(combination), size=16)
#plt.subplot(2,3,1)
#pcolorEnergyMonths(H_month,'min',combination)
#plt.title("Heating Demand")
#plt.subplot(2,3,2)
#pcolorEnergyMonths(C_month,'min',combination)
#plt.title("Cooling Demand")
#plt.subplot(2,3,3)
#pcolorEnergyMonths(L_month,'min',combination)
#plt.title("Lighting Demand")
#plt.subplot(2,3,4)
#pcolorEnergyMonths(-PV_month,'max',combination)
#plt.title("PV Production")
#plt.subplot(2,3,5)
#pcolorEnergyMonths(E_month,'min',combination)
#plt.title("Thermal/Lighting Demand")
#plt.subplot(2,3,6)
#pcolorEnergyMonths(E_month_withPV,'min',combination)
#plt.title("Net Energy Demand")
#fig.subplots_adjust(right=0.8)
#cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
##cbar = plt.colorbar(cax=cbar_ax, ticks=np.asarray(range(0,int(E_month.max()))))
#cbar = plt.colorbar(cax=cbar_ax, ticks=np.asarray(range(0,30)))
#cbar.set_label('Energy Use in kWh', rotation=270, labelpad=20)
#plt.show()
#
## Energy Use at fixed angle combination for the hole year:
#combination=0
#figcounter+=1
#fig = plt.figure(num = figcounter, figsize=(16, 12))
#plt.suptitle("Energy Use at combination " + str(combination), size=16)
#plt.subplot(2,3,1)
#pcolorEnergyMonths(H_month,'min',combination)
#plt.title("Heating Demand")
#plt.subplot(2,3,2)
#pcolorEnergyMonths(C_month,'min',combination)
#plt.title("Cooling Demand")
#plt.subplot(2,3,3)
#pcolorEnergyMonths(L_month,'min',combination)
#plt.title("Lighting Demand")
#plt.subplot(2,3,4)
#pcolorEnergyMonths(-PV_month,'max',combination)
#plt.title("PV Production")
#plt.subplot(2,3,5)
#pcolorEnergyMonths(E_month,'min',combination)
#plt.title("Thermal/Lighting Demand")
#plt.subplot(2,3,6)
#pcolorEnergyMonths(E_month_withPV,'min',combination)
#plt.title("Net Energy Demand")
#fig.subplots_adjust(right=0.8)
#cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
##cbar = plt.colorbar(cax=cbar_ax, ticks=np.asarray(range(0,int(E_month.max()))))
#cbar = plt.colorbar(cax=cbar_ax, ticks=np.asarray(range(0,30)))
#cbar.set_label('Energy Use in kWh', rotation=270, labelpad=20)
#plt.show()
#
##abstract figures:
#
##create strings for angle ticks:
#AnglesString=[]
#for i in range(len(allAngles[0])):
#    AnglesString.append(str(allAngles[0][i][0])+'/'+str(allAngles[0][i][1]))
#    
#    
# # Optimal x- and y-angle combinations for every hour of the year
#figcounter+=1
#fig = plt.figure(num = figcounter, figsize=(16, 8))
#plt.suptitle("(a) Optimum Altitude and Azimuth Orientation", size=16)
#p1 = plt.subplot(2,3,1)
#pcolorMonths(H_month, 'xy', x_angle_location, y_angle_location, allAngles, sunMask)
#plt.title("Heating Demand")
#plt.ylabel("Hour of the Day",size=14)
#p1 = plt.subplot(2,3,2)
#pcolorMonths(C_month, 'xy', x_angle_location, y_angle_location, allAngles, sunMask)
#plt.title("Cooling Demand")
#p1 = plt.subplot(2,3,3)
#pcolorMonths(L_month, 'xy', x_angle_location, y_angle_location, allAngles, sunMask)
#plt.title("Lighting Demand")
#p1 = plt.subplot(2,3,4)
#pcolorMonths(R_month, 'xy', x_angle_location, y_angle_location, allAngles, sunMask, 'max')
#plt.title("Irradiation on Panels")
#plt.xlabel("Month of the Year",size=14)
#plt.ylabel("Hour of the Day",size=14)
#p1 = plt.subplot(2,3,5)
#pcolorMonths(E_month, 'xy', x_angle_location, y_angle_location, allAngles, sunMask)
#plt.title("Total Thermal/Lighting Demand")
#plt.xlabel("Month of the Year",size=14)
#p1 = plt.subplot(2,3,6)
#pcolorMonths(E_month_withPV, 'xy', x_angle_location, y_angle_location, allAngles, sunMask)
#plt.title("Net Demand including PV")
#plt.xlabel("Month of the Year",size=14)
#fig.subplots_adjust(right=0.8)
##cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#cbar_ax = fig.add_axes([0.85, 0.1, 0.05, 0.78])
##cbart = plt.title("Altitude / Azimuth", fontsize=14, loc='left', verticalalignment = 'bottom')
#cbart = plt.title("Altitude / Azimuth", fontsize=14)
#cbart.set_position((1.1,1.02))
#cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(allAngles[0])))
#cbar.ax.set_yticklabels(AnglesString)
#cbar.ax.tick_params(labelsize=14)
#plt.show()   
#
#
## Energy Use at opmtimum angle combination for the hole year:
#figcounter+=1
#fig = plt.figure(num = figcounter, figsize=(16, 8))
##plt.suptitle("(b) Net Energy Use at Optimum Orientation", size=16)
#plt.subplot(2,3,1)
#pcolorEnergyMonths(H_month,'min')
#plt.title("Heating Demand")
#plt.ylabel("Hour of the Day",size=14)
#plt.subplot(2,3,2)
#pcolorEnergyMonths(C_month,'min')
#plt.title("Cooling Demand")
#plt.subplot(2,3,3)
#pcolorEnergyMonths(L_month,'min')
#plt.title("Lighting Demand")
#plt.subplot(2,3,4)
#pcolorEnergyMonths(-PV_month,'min')
#plt.title("PV Production")
#plt.xlabel("Month of the Year",size=14)
#plt.ylabel("Hour of the Day",size=14)
#plt.subplot(2,3,5)
#pcolorEnergyMonths(E_month,'min')
#plt.title("Total Thermal/Lighting Demand")
#plt.xlabel("Month of the Year",size=14)
#plt.subplot(2,3,6)
#pcolorEnergyMonths(E_month_withPV,'min')
#plt.title("Net Demand including PV")
#plt.xlabel("Month of the Year",size=14)
#fig.subplots_adjust(right=0.8)
#cbar_ax = fig.add_axes([0.85, 0.1, 0.05, 0.78])
#cbart = plt.title("Net Energy [kWh]", fontsize=14)
#cbart.set_position((1.1,1.02))
##cbar = plt.colorbar(cax=cbar_ax, ticks=np.asarray(range(0,int(E_month.max()))))
##○cbar = plt.colorbar(cax=cbar_ax, ticks=np.asarray(range(0,30)))
#cbar = plt.colorbar(cax=cbar_ax)
#cbar.ax.tick_params(labelsize=14)
##cbar.set_label('Net Energy Use in kWh', rotation=270, labelpad=20, size=14)
#plt.show()