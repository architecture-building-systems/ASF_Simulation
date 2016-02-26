# -*- coding: utf-8 -*-
"""
Analyse ASF thermal and lighting simulation results - master script

based on DIVA analysis results

Created on Wed Dec 30 14:59:53 2015

@author: Jeremias Schmidli
"""

import math, sys, copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab

from sortAngles import CalcXYAnglesAndLocation, unique
from calculate_angles_function import create_ASF_angles  
from PostProcessThermal_functions import scatterResults, pcolorDays, AngleHistogram, pcolorEnergyDays

#define if data should be imported, set False if desired evaluation data is already in workspace:
importDataFlag = True

#define if plots should be created
createPlotsFlag = False
#define options used for creating plots "xy_separate", "xy_together"
createPlotsOptions = "xy_separate"

#only single angle result flag (not yet complete)
oneDimensionalFlag = True

if importDataFlag:
    # set path to folder containing .csv files to analyse
    path = "C:/Users/Assistenz/Documents/MT_Jeremias/Simulation_Data/Simulation_noASF_Frankfurt/"
#    path = "C:/Users/Assistenz/Documents/MT_Jeremias/Simulation_Data/Simulation_324_comb_rect_Frankfurt/delete_NONE_line_191/"
#    path = "C:/Users/Assistenz/Documents/MT_Jeremias/Simulation_Data/Simulation_324_comb_rect_Madrid/"
#    path = "C:/Users/Assistenz/Documents/MT_Jeremias/Simulation_Data/Simulation_noASF_Madrid/"
    #path = "C:/Users/Assistenz/Documents/MT_Jeremias/Simulation_Data/Simulation_160108_noshade/"
    #path = "C:/Users/Assistenz/Documents/MT_Jeremias/Simulation_Data/Simulation_160108_noshade_1stepPerHour/"
    #path = "C:/Users/Assistenz/Documents/MT_Jeremias/Simulation_Data/Simulation_141216_729_comb_rectangular/"
    #path = "C:/Users/Assistenz/Documents/MT_Jeremias/Simulation_Data/Simulation_160125_diamond_25com_2/"
    #path = "C:/Users/Assistenz/Documents/MT_Jeremias/Simulation_Data/Simulation_160128_diamond_25comb_newReflection/"
    
    #Import data from csv
    C=np.genfromtxt(path + 'cooling.csv',delimiter=',')
    H=np.genfromtxt(path + 'heating.csv',delimiter=',')
    L=np.genfromtxt(path + 'lighting.csv',delimiter=',')
    
    #Calculate the total Energy Consumption
    E=C+H+L
    
    #import parameters used for simulation:
    with open(path + 'LayoutAndCombinations.txt', 'rb') as f:
        parameters = f.readlines()
        f.close()
    
    for i in range(len(parameters)):
        exec parameters[i]
        
    del parameters
    
    # calculate angle combinations and their location:
    allAngles, x_angles, x_angles_full, x_angle_location, y_angles, y_angles_full, y_angle_location = CalcXYAnglesAndLocation(ASFarray, XANGLES, YANGLES, NoClusters)


if createPlotsFlag:
    figcounter=0
    plt.style.use('ggplot')
    
    if createPlotsOptions == "xy_separate":
        
        # Optimal x-angle combinations for every hour of the year
        figcounter+=1
        fig = plt.figure(num = figcounter, figsize=(16, 12))
        plt.suptitle("Angle Distribution around x-axis", size=16)
        p1 = plt.subplot(2,2,1)
        pcolorDays(H, 'x', x_angle_location, y_angle_location, allAngles)
        plt.title("Heating Demand")
        p1 = plt.subplot(2,2,2)
        pcolorDays(C, 'x', x_angle_location, y_angle_location, allAngles)
        plt.title("Cooling Demand")
        p1 = plt.subplot(2,2,3)
        pcolorDays(L, 'x', x_angle_location, y_angle_location, allAngles)
        #pcolorDays(R_tot, 'x', x_angle_location, y_angle_location, allAngles,'max')
        plt.title("Lighting Demand")
        p1 = plt.subplot(2,2,4)
        pcolorDays(E, 'x', x_angle_location, y_angle_location, allAngles)
        #pcolorDays(R_week, 'x', x_angle_location, y_angle_location, allAngles, 'max')
        plt.title("Total Energy Demand")
        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
        cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(x_angles)))
        cbar.ax.set_yticklabels(x_angles)
        plt.show()
        
        # Optimal y-angle combinations for every hour of the year
        figcounter+=1
        fig = plt.figure(num = figcounter, figsize=(16, 12))
        plt.suptitle("Angle Distribution around y-axis", size=16)
        plt.subplot(2,2,1)
        pcolorDays(H, 'y', x_angle_location, y_angle_location, allAngles)
        plt.title("Heating Demand")
        plt.subplot(2,2,2)
        pcolorDays(C, 'y', x_angle_location, y_angle_location, allAngles)
        plt.title("Cooling Demand")
        plt.subplot(2,2,3)
        pcolorDays(L, 'y', x_angle_location, y_angle_location, allAngles)
        #pcolorDays(R_tot, 'y', x_angle_location, y_angle_location, allAngles,'max')
        plt.title("Lighting Demand")
        plt.subplot(2,2,4)
        pcolorDays(E, 'y', x_angle_location, y_angle_location, allAngles)
        #pcolorDays(R_week, 'y', x_angle_location, y_angle_location, allAngles, 'max')
        plt.title("Total Energy Demand")
        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
        cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(y_angles)))
        cbar.ax.set_yticklabels(y_angles)
        plt.show()
        
        # histograms of x-angle combinations
        figcounter+=1
        fig = plt.figure(num = figcounter, figsize=(16, 12))
        plt.suptitle("Histograms of Angle Distribution around x-axis", size=16)
        plt.subplot(2,2,1)
        AngleHistogram(H, 'x', x_angles, x_angle_location, y_angles, y_angle_location, allAngles)
        plt.title("Heating Demand")
        plt.subplot(2,2,2)
        AngleHistogram(C, 'x', x_angles, x_angle_location, y_angles, y_angle_location, allAngles)
        plt.title("Cooling Demand")
        plt.subplot(2,2,3)
        AngleHistogram(L, 'x', x_angles, x_angle_location, y_angles, y_angle_location, allAngles)
        plt.title("Lighting Demand")
        plt.subplot(2,2,4)
        AngleHistogram(E, 'x', x_angles, x_angle_location, y_angles, y_angle_location, allAngles)
        plt.title("Total Energy Demand")
        plt.subplots_adjust(hspace=0.45, bottom=0.11)
        plt.show()
        
        # histograms of y-angle combinations
        figcounter+=1
        fig = plt.figure(num = figcounter, figsize=(16, 12))
        plt.suptitle("Histograms of Angle Distribution around y-axis", size=16)
        plt.subplot(2,2,1)
        AngleHistogram(H, 'y', x_angles, x_angle_location, y_angles, y_angle_location, allAngles)
        plt.title("Heating Demand")
        plt.subplot(2,2,2)
        AngleHistogram(C, 'y', x_angles, x_angle_location, y_angles, y_angle_location, allAngles)
        plt.title("Cooling Demand")
        plt.subplot(2,2,3)
        AngleHistogram(L, 'y', x_angles, x_angle_location, y_angles, y_angle_location, allAngles)
        plt.title("Lighting Demand")
        plt.subplot(2,2,4)
        AngleHistogram(E, 'y', x_angles, x_angle_location, y_angles, y_angle_location, allAngles)
        plt.title("Total Energy Demand")
        plt.subplots_adjust(hspace=0.45, bottom=0.11)
        plt.show()
        
    elif createPlotsOptions == "xy_together":
        
        # Optimal angle combinations for every hour of the year
        figcounter+=1
        fig = plt.figure(num = figcounter, figsize=(16, 12))
        #plt.suptitle("Angle Distribution", size=16)
        p1 = plt.subplot(3,2,1)
        pcolorDays(H, 'xy', x_angle_location, y_angle_location, allAngles)
        plt.title("a) Heating Demand")
        plt.ylabel("Hour of the Day")
        p1 = plt.subplot(3,2,2)
        pcolorDays(C, 'xy', x_angle_location, y_angle_location, allAngles)
        plt.title("b) Cooling Demand")
        p1 = plt.subplot(3,2,3)
        pcolorDays(L, 'xy', x_angle_location, y_angle_location, allAngles)
        plt.title("c) Lighting Demand")
#        plt.ylabel("Hour of the Day")
#        p1 = plt.subplot(3,2,4)
#        #pcolorDays(E, 'xy', x_angle_location, y_angle_location, allAngles)
#        pcolorDays(R_tot, 'xy', x_angle_location, y_angle_location, allAngles, 'max')
#        plt.title("d) PV Electricity Production")
        p1 = plt.subplot(3,2,5)
        pcolorDays(E, 'xy', x_angle_location, y_angle_location, allAngles)
        plt.title("e) Total Energy Demand for Heating, Cooling and Lighting")
        plt.xlabel("Day of the Year")
        plt.ylabel("Hour of the Day")
#        p1 = plt.subplot(3,2,6)
#        pcolorDays(E_withPV, 'xy', x_angle_location, y_angle_location, allAngles)
#        plt.title("f) Total Energy Demand including PV")
#        plt.xlabel("Day of the Year")
        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
        plt.title("(x-angle, y-angle)", fontsize=12, loc='left', verticalalignment = 'bottom')
        cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(allAngles[0])))
        cbar.ax.set_yticklabels(allAngles[0])
        plt.show()
        
        
        # histograms ofangle combinations
        figcounter+=1
        fig = plt.figure(num = figcounter, figsize=(16, 12))
        plt.suptitle("Histograms of Angle Distribution", size=16)
        plt.subplot(2,2,1)
        AngleHistogram(H, 'xy', x_angles, x_angle_location, y_angles, y_angle_location, allAngles)
        plt.title("Heating Demand")
        plt.subplot(2,2,2)
        AngleHistogram(C, 'xy', x_angles, x_angle_location, y_angles, y_angle_location, allAngles)
        plt.title("Cooling Demand")
        plt.subplot(2,2,3)
        AngleHistogram(L, 'xy', x_angles, x_angle_location, y_angles, y_angle_location, allAngles)
        plt.title("Lighting Demand")
        plt.subplot(2,2,4)
        AngleHistogram(E, 'xy', x_angles, x_angle_location, y_angles, y_angle_location, allAngles)
        plt.title("Total Energy Demand")
        plt.subplots_adjust(hspace=0.45, bottom=0.11)
        plt.show()
        

# frequencies of x and y angle combinations
    figcounter+=1
    fig = plt.figure(num = figcounter, figsize=(16, 12))
    plt.suptitle("Angle Combination Distribution", size=16)
    plt.subplot(2,2,1)
    scatterResults(H, 'r', 0, x_angles, x_angle_location, y_angles, y_angle_location)
    plt.title("Heating Demand")
    plt.subplot(2,2,2)
    scatterResults(C, 'b', 1, x_angles, x_angle_location, y_angles, y_angle_location)
    plt.title("Cooling Demand")
    plt.subplot(2,2,3)
    scatterResults(L, 'g', 2, x_angles, x_angle_location, y_angles, y_angle_location)
    plt.title("Lighting Demand")
    plt.subplot(2,2,4)
    scatterResults(E, 'c', 3, x_angles, x_angle_location, y_angles, y_angle_location)
    plt.title("Angle Combination")
    plt.subplots_adjust(hspace=0.45, wspace=0.3, bottom=0.11)
    #plt.locator_params(nbins=30)
    #fig.ax.set_yticklabels(y_angles)
    #fig.ax.set_xticklabels(x_angles)
    plt.show()
    
# Energy Use at opmtimum angle combination for the hole year:
    figcounter+=1
    fig = plt.figure(num = figcounter, figsize=(16, 12))
    plt.suptitle("Energy Use at optimum angle combination", size=16)
    plt.subplot(2,2,1)
    pcolorEnergyDays(H)
    plt.title("Heating Demand")
    plt.subplot(2,2,2)
    pcolorEnergyDays(C)
    plt.title("Cooling Demand")
    plt.subplot(2,2,3)
    pcolorEnergyDays(L)
    plt.title("Lighting Demand")
    plt.subplot(2,2,4)
    pcolorEnergyDays(E)
    plt.title("Total Energy Demand")
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    cbar = plt.colorbar(cax=cbar_ax, ticks=np.asarray(range(0,int(E.max()*10)))/10.)
    cbar.set_label('Power Use in kWh', rotation=270, labelpad=20)
    plt.show()
# calculate energy use at optimal angle combination
if not oneDimensionalFlag:
    TotalHeating = np.round(np.sum(np.min(H, axis=0)), decimals=1)
    TotalCooling = np.round(np.sum(np.min(C, axis=0)), decimals=1)
    TotalLighting = np.round(np.sum(np.min(L, axis=0)), decimals=1)
    TotalEnergy = np.round(np.sum(np.min(E, axis=0)), decimals=1)
#    TotalPV = np.round(np.sum(np.max(PV, axis=0)), decimals=1)
#    TotalEnergy_withPV = np.round(np.sum(np.min(E_withPV, axis=0)), decimals=1)
    TradeoffLosses = np.round(TotalEnergy-TotalLighting-TotalCooling-TotalHeating, decimals=2)
else:
    TotalHeating = np.round(np.sum(H), decimals=1)
    TotalCooling = np.round(np.sum(C), decimals=1)
    TotalLighting = np.round(np.sum(L), decimals=1)
    TotalEnergy = np.round(np.sum(E), decimals=1)
    TradeoffLosses = np.round(TotalEnergy-TotalLighting-TotalCooling-TotalHeating , decimals=2)
    
#convert from kWh to GJ
TotalHeatingGJ = TotalHeating*0.0036
TotalCoolingGJ = TotalCooling*0.0036
TotalLightingGJ = TotalLighting*0.0036
TotalEnergyGJ = TotalEnergy*0.0036

#define COPs of heating and cooling
HeatingCOP = 5
CoolingCOP = 3

#calculate net energy demand of room
NetHeating = TotalHeatingGJ*HeatingCOP
NetCooling = TotalCoolingGJ*CoolingCOP


print 'total heating energy at optimum heating angles:'
print TotalHeating, 'kWh \n'
print 'total cooling energy at optimum cooling angles:'
print TotalCooling, 'kWh \n'
print 'total lighting energy at optimum lighting angles:'
print TotalLighting, 'kWh \n'
print 'total energy use at overall optimum angles:'
print TotalEnergy, 'kWh \n'
print 'losses caused by tradeoffs between Heating, Cooling and Lighting:'
print TradeoffLosses, 'kWh \n'