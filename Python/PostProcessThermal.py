# -*- coding: utf-8 -*-
"""
Analyse ASF thermal and lighting simulation results - master script

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
importDataFlag = False
createPlotsFlag = True

if importDataFlag:
    # set path to folder containing .csv files to analyse
    path = "C:/Users/Assistenz/Documents/MT_Jeremias/Simulation_Data/Simulation_141216_729_comb_rectangular/"
    
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
    x_angles, x_angles_full, x_angle_location, y_angles, y_angles_full, y_angle_location = CalcXYAnglesAndLocation(ASFarray, XANGLES, YANGLES, NoClusters)


if createPlotsFlag:
    
    plt.style.use('ggplot')
    
    # Optimal x-angle combinations for every hour of the year
    fig = plt.figure(num = 1, figsize=(16, 12))
    plt.suptitle("Angle Distribution around x-axis", size=16)
    p1 = plt.subplot(2,2,1)
    pcolorDays(H, 'x', x_angle_location, y_angle_location)
    plt.title("Heating Demand")
    p1 = plt.subplot(2,2,2)
    pcolorDays(C, 'x', x_angle_location, y_angle_location)
    plt.title("Cooling Demand")
    p1 = plt.subplot(2,2,3)
    pcolorDays(L, 'x', x_angle_location, y_angle_location)
    plt.title("Lighting Demand")
    p1 = plt.subplot(2,2,4)
    pcolorDays(E, 'x', x_angle_location, y_angle_location)
    plt.title("Total Energy Demand")
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(x_angles)))
    cbar.ax.set_yticklabels(x_angles)
    plt.show()
    
    # Optimal y-angle combinations for every hour of the year
    fig = plt.figure(num = 2, figsize=(16, 12))
    plt.suptitle("Angle Distribution around y-axis", size=16)
    plt.subplot(2,2,1)
    pcolorDays(H, 'y', x_angle_location, y_angle_location)
    plt.title("Heating Demand")
    plt.subplot(2,2,2)
    pcolorDays(C, 'y', x_angle_location, y_angle_location)
    plt.title("Cooling Demand")
    plt.subplot(2,2,3)
    pcolorDays(L, 'y', x_angle_location, y_angle_location)
    plt.title("Lighting Demand")
    plt.subplot(2,2,4)
    pcolorDays(E, 'y', x_angle_location, y_angle_location)
    plt.title("Total Energy Demand")
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(y_angles)))
    cbar.ax.set_yticklabels(y_angles)
    plt.show()
    
    
    # Energy Use at opmtimum angle combination for the hole year:
    fig = plt.figure(num = 3, figsize=(16, 12))
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
    cbar.set_label('Power Use in kW', rotation=270, labelpad=20)
    plt.show()
    
    
    # histograms of x-angle combinations
    fig = plt.figure(num = 4, figsize=(16, 12))
    plt.suptitle("Histograms of Angle Distribution around x-axis", size=16)
    plt.subplot(2,2,1)
    AngleHistogram(H, 'x', x_angles, x_angle_location, y_angles, y_angle_location)
    plt.title("Heating Demand")
    plt.subplot(2,2,2)
    AngleHistogram(C, 'x', x_angles, x_angle_location, y_angles, y_angle_location)
    plt.title("Cooling Demand")
    plt.subplot(2,2,3)
    AngleHistogram(L, 'x', x_angles, x_angle_location, y_angles, y_angle_location)
    plt.title("Lighting Demand")
    plt.subplot(2,2,4)
    AngleHistogram(E, 'x', x_angles, x_angle_location, y_angles, y_angle_location)
    plt.title("Total Energy Demand")
    plt.subplots_adjust(hspace=0.45, bottom=0.11)
    plt.show()
    
    # histograms of y-angle combinations
    fig = plt.figure(num = 5, figsize=(16, 12))
    plt.suptitle("Histograms of Angle Distribution around y-axis", size=16)
    plt.subplot(2,2,1)
    AngleHistogram(H, 'y', x_angles, x_angle_location, y_angles, y_angle_location)
    plt.title("Heating Demand")
    plt.subplot(2,2,2)
    AngleHistogram(C, 'y', x_angles, x_angle_location, y_angles, y_angle_location)
    plt.title("Cooling Demand")
    plt.subplot(2,2,3)
    AngleHistogram(L, 'y', x_angles, x_angle_location, y_angles, y_angle_location)
    plt.title("Lighting Demand")
    plt.subplot(2,2,4)
    AngleHistogram(E, 'y', x_angles, x_angle_location, y_angles, y_angle_location)
    plt.title("Total Energy Demand")
    plt.subplots_adjust(hspace=0.45, bottom=0.11)
    plt.show()

# frequencies of x and y angle combinations
    fig = plt.figure(num = 6, figsize=(16, 12))
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