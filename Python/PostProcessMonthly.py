# -*- coding: utf-8 -*-
"""
Created on Tue Feb 02 15:58:24 2016

master file for monthly evaluation of simulation data

imports data using most other py scripts

creates plots based on thermal/lighting/radiation data

@author: Jeremias
"""
import numpy as np
import matplotlib.pyplot as plt

from average_monthly import average_monthly, daysPassedMonth
from PostProcessThermal_functions import pcolorMonths, pcolorEnergyMonths
from try_nan_values import createMonthsNan

importData = False

if importData:
    
    #make sure that this file is set to "monthly":
    execfile("PostProcessRadiation.py")
    
    #imports yearly results:
    execfile("PostProcessThermal.py")
    
    daysPassedMonth=daysPassedMonth()
    
    #PV_month=PV_month
    
    C_month = average_monthly(C,daysPassedMonth)
    H_month = average_monthly(H,daysPassedMonth)
    L_month = average_monthly(L,daysPassedMonth)
    E_month = average_monthly(E,daysPassedMonth)
    E_month_withPV = C_month+H_month+L_month-PV_month
    
    sunMask = createMonthsNan(L_month, R_month, allAngles)

    
 # Optimal x-angle combinations for every hour of the year
figcounter+=1
fig = plt.figure(num = figcounter, figsize=(16, 12))
plt.suptitle("Angle Distribution around x-axis", size=16)
p1 = plt.subplot(2,3,1)
pcolorMonths(H_month, 'x', x_angle_location, y_angle_location, allAngles, sunMask)
plt.title("Heating Demand")
p1 = plt.subplot(2,3,2)
pcolorMonths(C_month, 'x', x_angle_location, y_angle_location, allAngles, sunMask)
plt.title("Cooling Demand")
p1 = plt.subplot(2,3,3)
pcolorMonths(L_month, 'x', x_angle_location, y_angle_location, allAngles, sunMask)
plt.title("Lighting Demand")
p1 = plt.subplot(2,3,4)
pcolorMonths(R_month, 'x', x_angle_location, y_angle_location, allAngles, sunMask, 'max')
plt.title("PV Electricity Production")
p1 = plt.subplot(2,3,5)
pcolorMonths(E_month, 'x', x_angle_location, y_angle_location, allAngles, sunMask)
plt.title("Total Thermal/Lighting Demand")
p1 = plt.subplot(2,3,6)
pcolorMonths(E_month_withPV, 'x', x_angle_location, y_angle_location, allAngles, sunMask)
plt.title("Net Demand with PV")
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(x_angles)))
cbar.ax.set_yticklabels(x_angles)
plt.show()   
    
    
 # Optimal y-angle combinations for every hour of the year
figcounter+=1
fig = plt.figure(num = figcounter, figsize=(16, 12))
plt.suptitle("Angle Distribution around y-axis", size=16)
p1 = plt.subplot(2,3,1)
pcolorMonths(H_month, 'y', x_angle_location, y_angle_location, allAngles, sunMask)
plt.title("Heating Demand")
p1 = plt.subplot(2,3,2)
pcolorMonths(C_month, 'y', x_angle_location, y_angle_location, allAngles, sunMask)
plt.title("Cooling Demand")
p1 = plt.subplot(2,3,3)
pcolorMonths(L_month, 'y', x_angle_location, y_angle_location, allAngles, sunMask)
plt.title("Lighting Demand")
p1 = plt.subplot(2,3,4)
pcolorMonths(R_month, 'y', x_angle_location, y_angle_location, allAngles, sunMask, 'max')
plt.title("PV Electricity Production")
p1 = plt.subplot(2,3,5)
pcolorMonths(E_month, 'y', x_angle_location, y_angle_location, allAngles, sunMask)
plt.title("Total Thermal/lighting Demand")
p1 = plt.subplot(2,3,6)
pcolorMonths(E_month_withPV, 'y', x_angle_location, y_angle_location, allAngles, sunMask)
plt.title("Net Demand with PV")
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(y_angles)))
cbar.ax.set_yticklabels(y_angles)
plt.show()   

 # Optimal x- and y-angle combinations for every hour of the year
figcounter+=1
fig = plt.figure(num = figcounter, figsize=(16, 12))
plt.suptitle("(a) optimal altitude and azimuth orientation", size=16)
p1 = plt.subplot(2,3,1)
pcolorMonths(H_month, 'xy', x_angle_location, y_angle_location, allAngles, sunMask)
plt.title("Heating Demand")
p1 = plt.subplot(2,3,2)
pcolorMonths(C_month, 'xy', x_angle_location, y_angle_location, allAngles, sunMask)
plt.title("Cooling Demand")
p1 = plt.subplot(2,3,3)
pcolorMonths(L_month, 'xy', x_angle_location, y_angle_location, allAngles, sunMask)
plt.title("Lighting Demand")
p1 = plt.subplot(2,3,4)
pcolorMonths(R_month, 'xy', x_angle_location, y_angle_location, allAngles, sunMask, 'max')
plt.title("PV Electricity Production")
p1 = plt.subplot(2,3,5)
pcolorMonths(E_month, 'xy', x_angle_location, y_angle_location, allAngles, sunMask)
plt.title("Total Thermal/lighting Demand")
p1 = plt.subplot(2,3,6)
pcolorMonths(E_month_withPV, 'xy', x_angle_location, y_angle_location, allAngles, sunMask)
plt.title("Net Demand with PV")
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(allAngles[0])))
cbar.ax.set_yticklabels(allAngles[0])
plt.show()   


#
## Optimal x-angle combinations for every hour of the year
#figcounter+=1
#fig = plt.figure(num = figcounter, figsize=(16, 12))
#plt.suptitle("Angle Distribution around x-axis", size=16)
#p1 = plt.subplot(2,2,1)
#pcolorMonths(H_month, 'x', x_angle_location, y_angle_location, allAngles)
#plt.title("Heating Demand")
#p1 = plt.subplot(2,2,2)
#pcolorMonths(C_month, 'x', x_angle_location, y_angle_location, allAngles)
#plt.title("Cooling Demand")
#p1 = plt.subplot(2,2,3)
#pcolorMonths(L_month, 'x', x_angle_location, y_angle_location, allAngles)
#plt.title("Lighting Demand")
#p1 = plt.subplot(2,2,4)
#pcolorMonths(E_month, 'x', x_angle_location, y_angle_location, allAngles)
#plt.title("Total Energy Demand")
#fig.subplots_adjust(right=0.8)
#cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(x_angles)))
#cbar.ax.set_yticklabels(x_angles)
#plt.show()
#
## Optimal y-angle combinations for every hour of the year
#figcounter+=1
#fig = plt.figure(num = figcounter, figsize=(16, 12))
#plt.suptitle("Angle Distribution around y-axis", size=16)
#plt.subplot(2,2,1)
#pcolorMonths(H_month, 'y', x_angle_location, y_angle_location, allAngles)
#plt.title("Heating Demand")
#plt.subplot(2,2,2)
#pcolorMonths(C_month, 'y', x_angle_location, y_angle_location, allAngles)
#plt.title("Cooling Demand")
#plt.subplot(2,2,3)
#pcolorMonths(L_month, 'y', x_angle_location, y_angle_location, allAngles)
#plt.title("Lighting Demand")
#plt.subplot(2,2,4)
#pcolorMonths(E_month, 'y', x_angle_location, y_angle_location, allAngles)
#plt.title("Total Energy Demand")
#fig.subplots_adjust(right=0.8)
#cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(y_angles)))
#cbar.ax.set_yticklabels(y_angles)
#plt.show()
#
#figcounter+=1
#fig = plt.figure(num = figcounter, figsize=(16, 12))
#plt.suptitle("Angle Distribution around x and y axis", size=16)
#p1 = plt.subplot(2,2,1)
#pcolorMonths(H_month, 'xy', x_angle_location, y_angle_location, allAngles)
#plt.title("Heating Demand")
#p1 = plt.subplot(2,2,2)
#pcolorMonths(C_month, 'xy', x_angle_location, y_angle_location, allAngles)
#plt.title("Cooling Demand")
#p1 = plt.subplot(2,2,3)
#pcolorMonths(L_month, 'xy', x_angle_location, y_angle_location, allAngles)
#plt.title("Lighting Demand")
#p1 = plt.subplot(2,2,4)
#pcolorMonths(E_month, 'xy', x_angle_location, y_angle_location, allAngles)
#plt.title("Total Energy Demand")
#fig.subplots_adjust(right=0.8)
#cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#plt.title("(x-angle, y-angle)", fontsize=12, loc='left', verticalalignment = 'bottom')
#cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(allAngles[0])))
#cbar.ax.set_yticklabels(allAngles[0])
#plt.show()

## Energy Use at opmtimum angle combination for the hole year:
#figcounter+=1
#fig = plt.figure(num = figcounter, figsize=(16, 12))
#plt.suptitle("Energy Use at optimum angle combination", size=16)
#plt.subplot(2,2,1)
#pcolorEnergyMonths(H_month)
#plt.title("Heating Demand")
#plt.subplot(2,2,2)
#pcolorEnergyMonths(C_month)
#plt.title("Cooling Demand")
#plt.subplot(2,2,3)
#pcolorEnergyMonths(L_month)
#plt.title("Lighting Demand")
#plt.subplot(2,2,4)
#pcolorEnergyMonths(E_month)
#plt.title("Total Energy Demand")
#fig.subplots_adjust(right=0.8)
#cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#cbar = plt.colorbar(cax=cbar_ax, ticks=np.asarray(range(0,int(E_month.max()))))
#cbar.set_label('Power Use in kWh', rotation=270, labelpad=20)
#plt.show()

# Energy Use at opmtimum angle combination for the hole year:
figcounter+=1
fig = plt.figure(num = figcounter, figsize=(16, 12))
plt.suptitle("Net Energy Use at optimum angle combination", size=16)
plt.subplot(2,3,1)
pcolorEnergyMonths(H_month,'min')
plt.title("Heating Demand")
plt.ylabel("Hour of the Day")
plt.subplot(2,3,2)
pcolorEnergyMonths(C_month,'min')
plt.title("Cooling Demand")
plt.subplot(2,3,3)
pcolorEnergyMonths(L_month,'min')
plt.title("Lighting Demand")
plt.subplot(2,3,4)
pcolorEnergyMonths(-PV_month,'min')
plt.title("PV Production")
plt.xlabel("Month of the Year")
plt.ylabel("Hour of the Day")
plt.subplot(2,3,5)
pcolorEnergyMonths(E_month,'min')
plt.title("Thermal/Lighting Demand")
plt.xlabel("Month of the Year")
plt.subplot(2,3,6)
pcolorEnergyMonths(E_month_withPV,'min')
plt.title("Net Energy Demand")
plt.xlabel("Month of the Year")
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#cbar = plt.colorbar(cax=cbar_ax, ticks=np.asarray(range(0,int(E_month.max()))))
#○cbar = plt.colorbar(cax=cbar_ax, ticks=np.asarray(range(0,30)))
cbar = plt.colorbar(cax=cbar_ax)
cbar.set_label('Net Energy Use in kWh', rotation=270, labelpad=20)
plt.show()

# Energy Use at fixed angle combination for the hole year:
combination=12
figcounter+=1
fig = plt.figure(num = figcounter, figsize=(16, 12))
plt.suptitle("Energy Use at combination " + str(combination), size=16)
plt.subplot(2,3,1)
pcolorEnergyMonths(H_month,'min',combination)
plt.title("Heating Demand")
plt.subplot(2,3,2)
pcolorEnergyMonths(C_month,'min',combination)
plt.title("Cooling Demand")
plt.subplot(2,3,3)
pcolorEnergyMonths(L_month,'min',combination)
plt.title("Lighting Demand")
plt.subplot(2,3,4)
pcolorEnergyMonths(-PV_month,'max',combination)
plt.title("PV Production")
plt.subplot(2,3,5)
pcolorEnergyMonths(E_month,'min',combination)
plt.title("Thermal/Lighting Demand")
plt.subplot(2,3,6)
pcolorEnergyMonths(E_month_withPV,'min',combination)
plt.title("Net Energy Demand")
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#cbar = plt.colorbar(cax=cbar_ax, ticks=np.asarray(range(0,int(E_month.max()))))
cbar = plt.colorbar(cax=cbar_ax, ticks=np.asarray(range(0,30)))
cbar.set_label('Energy Use in kWh', rotation=270, labelpad=20)
plt.show()

# Energy Use at fixed angle combination for the hole year:
combination=0
figcounter+=1
fig = plt.figure(num = figcounter, figsize=(16, 12))
plt.suptitle("Energy Use at combination " + str(combination), size=16)
plt.subplot(2,3,1)
pcolorEnergyMonths(H_month,'min',combination)
plt.title("Heating Demand")
plt.subplot(2,3,2)
pcolorEnergyMonths(C_month,'min',combination)
plt.title("Cooling Demand")
plt.subplot(2,3,3)
pcolorEnergyMonths(L_month,'min',combination)
plt.title("Lighting Demand")
plt.subplot(2,3,4)
pcolorEnergyMonths(-PV_month,'max',combination)
plt.title("PV Production")
plt.subplot(2,3,5)
pcolorEnergyMonths(E_month,'min',combination)
plt.title("Thermal/Lighting Demand")
plt.subplot(2,3,6)
pcolorEnergyMonths(E_month_withPV,'min',combination)
plt.title("Net Energy Demand")
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#cbar = plt.colorbar(cax=cbar_ax, ticks=np.asarray(range(0,int(E_month.max()))))
cbar = plt.colorbar(cax=cbar_ax, ticks=np.asarray(range(0,30)))
cbar.set_label('Energy Use in kWh', rotation=270, labelpad=20)
plt.show()

#abstract figures:

#create strings for angle ticks:
AnglesString=[]
for i in range(len(allAngles[0])):
    AnglesString.append(str(allAngles[0][i][0])+'/'+str(allAngles[0][i][1]))
    
    
 # Optimal x- and y-angle combinations for every hour of the year
figcounter+=1
fig = plt.figure(num = figcounter, figsize=(16, 8))
plt.suptitle("(a) Optimum Altitude and Azimuth Orientation", size=16)
p1 = plt.subplot(2,3,1)
pcolorMonths(H_month, 'xy', x_angle_location, y_angle_location, allAngles, sunMask)
plt.title("Heating Demand")
plt.ylabel("Hour of the Day",size=14)
p1 = plt.subplot(2,3,2)
pcolorMonths(C_month, 'xy', x_angle_location, y_angle_location, allAngles, sunMask)
plt.title("Cooling Demand")
p1 = plt.subplot(2,3,3)
pcolorMonths(L_month, 'xy', x_angle_location, y_angle_location, allAngles, sunMask)
plt.title("Lighting Demand")
p1 = plt.subplot(2,3,4)
pcolorMonths(R_month, 'xy', x_angle_location, y_angle_location, allAngles, sunMask, 'max')
plt.title("Irradiation on Panels")
plt.xlabel("Month of the Year",size=14)
plt.ylabel("Hour of the Day",size=14)
p1 = plt.subplot(2,3,5)
pcolorMonths(E_month, 'xy', x_angle_location, y_angle_location, allAngles, sunMask)
plt.title("Total Thermal/Lighting Demand")
plt.xlabel("Month of the Year",size=14)
p1 = plt.subplot(2,3,6)
pcolorMonths(E_month_withPV, 'xy', x_angle_location, y_angle_location, allAngles, sunMask)
plt.title("Net Demand including PV")
plt.xlabel("Month of the Year",size=14)
fig.subplots_adjust(right=0.8)
#cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
cbar_ax = fig.add_axes([0.85, 0.1, 0.05, 0.78])
#cbart = plt.title("Altitude / Azimuth", fontsize=14, loc='left', verticalalignment = 'bottom')
cbart = plt.title("Altitude / Azimuth", fontsize=14)
cbart.set_position((1.1,1.02))
cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(allAngles[0])))
cbar.ax.set_yticklabels(AnglesString)
cbar.ax.tick_params(labelsize=14)
plt.show()   


# Energy Use at opmtimum angle combination for the hole year:
figcounter+=1
fig = plt.figure(num = figcounter, figsize=(16, 8))
#plt.suptitle("(b) Net Energy Use at Optimum Orientation", size=16)
plt.subplot(2,3,1)
pcolorEnergyMonths(H_month,'min')
plt.title("Heating Demand")
plt.ylabel("Hour of the Day",size=14)
plt.subplot(2,3,2)
pcolorEnergyMonths(C_month,'min')
plt.title("Cooling Demand")
plt.subplot(2,3,3)
pcolorEnergyMonths(L_month,'min')
plt.title("Lighting Demand")
plt.subplot(2,3,4)
pcolorEnergyMonths(-PV_month,'min')
plt.title("PV Production")
plt.xlabel("Month of the Year",size=14)
plt.ylabel("Hour of the Day",size=14)
plt.subplot(2,3,5)
pcolorEnergyMonths(E_month,'min')
plt.title("Total Thermal/Lighting Demand")
plt.xlabel("Month of the Year",size=14)
plt.subplot(2,3,6)
pcolorEnergyMonths(E_month_withPV,'min')
plt.title("Net Demand including PV")
plt.xlabel("Month of the Year",size=14)
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.1, 0.05, 0.78])
cbart = plt.title("Net Energy [kWh]", fontsize=14)
cbart.set_position((1.1,1.02))
#cbar = plt.colorbar(cax=cbar_ax, ticks=np.asarray(range(0,int(E_month.max()))))
#○cbar = plt.colorbar(cax=cbar_ax, ticks=np.asarray(range(0,30)))
cbar = plt.colorbar(cax=cbar_ax)
cbar.ax.tick_params(labelsize=14)
#cbar.set_label('Net Energy Use in kWh', rotation=270, labelpad=20, size=14)
plt.show()


# claculate energy values:

TotalHeating = np.round(np.sum(np.min(H_month, axis=0)), decimals=1)
TotalCooling = np.round(np.sum(np.min(C_month, axis=0)), decimals=1)
TotalLighting = np.round(np.sum(np.min(L_month, axis=0)), decimals=1)
TotalEnergy = np.round(np.sum(np.min(E_month, axis=0)), decimals=1)
TotalPV = np.round(np.sum(np.max(PV_month, axis=0)), decimals=1)
TotalR = np.round(np.sum(np.max(R_month, axis=0)), decimals=1)
TotalR_LB = np.round(np.sum(np.max(R_monthlyLB, axis=0)), decimals=1)
TotalEnergy_withPV = np.round(np.sum(np.min(E_month_withPV, axis=0)), decimals=1)
TradeoffLosses = np.round(TotalEnergy-TotalLighting-TotalCooling-TotalHeating, decimals=2)

TotalR_comb = []
for i in range(len(R_month)):
    TotalR_comb.append([])
    TotalR_comb[i] =  np.round(np.sum(R_month[i]), decimals=1)
    
figcounter+=1
fig = plt.figure(num = figcounter, figsize=(16, 8))
plt.bar(range(len(TotalR_comb)),TotalR_comb)