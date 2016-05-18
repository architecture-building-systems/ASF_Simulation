# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 09:10:58 2016

Plots for thesis

@author: Jeremias
"""

import matplotlib.pyplot as plt
import numpy as np
import sys, os
from mpl_toolkits.mplot3d import Axes3D

from plotDataFunctions import create3Dplot, pcolorMonths, pcolorEnergyMonths, plotTotEfixedY, plotTotEfixedX, plotAngleSavings, plotMaxMinDiff
from createFigures import compareResultsFigure
from Tradeoffs import compareTotalEnergyForThesis

#


# load data:
resultsFolder1 = 'Kloten_19x_1y'

resultsFolder2 = 'Kloten_1x_19y'

results49comb = 'Kloten_49comb'

roomSize = 34.3



def createCarpetPlots(plotFunction, monthlyData, *arg):
    """
    Function that creates carpet plots of the optimal x- and y-angle combinations
    for monthly data
    """
    
    if not len(arg) == 0:
        rotation_axis = arg[0]
        if arg[0] == 'xy':
            angles = monthlyData['angles']['allAngles'][0]   
        elif arg[0] == 'x':
            anglesTuple = monthlyData['angles']['x_angles'] 
            angles = []
            for i in anglesTuple:
                angles.append(str(i[0]))
        elif arg[0] == 'y':
            anglesTuple = monthlyData['angles']['y_angles']    
            angles = []
            for i in anglesTuple:
                angles.append(str(i[0]))
        else:
            raise ValueError('rotation_axis does not exist')
    else:
        rotation_axis = np.nan

    # assign what efficiencies were used for evaluation:  
    if monthlyData['changedEfficiency'] == True:
        usedEfficiencies = monthlyData['efficiencyChanges']
    else:
        usedEfficiencies = monthlyData['efficiencies']
    
    #set max/min for energy plot:
    z_min = np.min(monthlyData['PV'])
    z_max = np.max(np.min(monthlyData['E_HCL'], axis=0))
    
    fig = plt.figure(figsize=(16, 8))
#    plt.suptitle("Optimum Altitude and Azimuth Orientation", size=16)
    plt.subplot(2,3,1)
    arg1 = ['min','H', rotation_axis, 'DIVA', z_min, z_max]
    plotFunction(monthlyData, arg1)
    plt.title("Heating Demand")
    plt.ylabel("Hour of the Day",size=14)
    plt.subplot(2,3,2)
    arg1 = ['min','C', rotation_axis, 'DIVA', z_min, z_max]
    plotFunction(monthlyData, arg1)
    plt.title("Cooling Demand")
    plt.subplot(2,3,3)
    arg1 = ['min','L', rotation_axis, 'DIVA', z_min, z_max]
    plotFunction(monthlyData, arg1)
    plt.title("Lighting Demand")
    plt.subplot(2,3,4)
    arg1 = ['min','PV', rotation_axis, 'LB', z_min, z_max]
    plotFunction(monthlyData, arg1)
    if usedEfficiencies['PV'] == 1 or not monthlyData['changedEfficiency'] :
        plt.title("PV Supply")
    else:
        plt.title("PV Supply (multiplied by factor " + str(usedEfficiencies['PV']) + ")")
    plt.xlabel("Month of the Year",size=14)
    plt.ylabel("Hour of the Day",size=14)
    plt.subplot(2,3,5)
    arg1 = ['min','E_HCL', rotation_axis, 'DIVA', z_min, z_max]
    plotFunction(monthlyData, arg1)
    plt.title("Total Thermal/Lighting Demand")
    plt.xlabel("Month of the Year",size=14)
    plt.subplot(2,3,6)
    arg1 = ['min','E_tot', rotation_axis, 'DIVA', z_min, z_max]
    plotFunction(monthlyData, arg1)
    plt.title("Net Demand including PV")
    plt.xlabel("Month of the Year",size=14)
    fig.subplots_adjust(right=0.8)
    #cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    cbar_ax = fig.add_axes([0.85, 0.1, 0.05, 0.78])
    #cbart = plt.title("Altitude / Azimuth", fontsize=14, loc='left', verticalalignment = 'bottom')
    
    if plotFunction == pcolorMonths:
        if arg[0] == 'xy':
            plt.suptitle("Optimum Altitude and Azimuth Orientation", size=16)
            cbart = plt.title("Altitude / Azimuth", fontsize=14)
        elif arg[0] == 'x':
            plt.suptitle("Optimum Altitude Orientation", size=16)
            cbart = plt.title("Altitude Angle [deg]", fontsize=14)
        elif arg[0] == 'y':
            plt.suptitle("Optimum Azimuth Orientation", size=16)
            cbart = plt.title("Azimuth Angle [deg]", fontsize=14)
        cbart.set_position((1.1,1.02))
        cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(angles)))
        cbar.ax.set_yticklabels(angles)
    elif plotFunction == pcolorEnergyMonths:
        plt.suptitle("Energy Demand at Optimum Orientation", size=16)
        cbar = plt.colorbar(cax=cbar_ax)
        cbart = plt.title("Net Energy [kWh]", fontsize=14)
        cbart.set_position((1.1,1.02))
#        cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(allAngles[0])))
        #cbar.ax.set_yticklabels(AnglesString)
    cbar.ax.tick_params(labelsize=14)
    plt.show()   
    return fig




# paths dict:
paths = {}

paths['main'] = os.path.dirname(os.path.dirname(sys.argv[0]))
paths['results'] = paths['main'] + '\\results'
paths['aux_functions'] = paths['main'] + '\\python\\aux_files'

# add python_path to system path, so that all files are available:
sys.path.insert(0, paths['aux_functions'])




# load results
results1 = np.load(paths['results'] + '\\' + resultsFolder1 + '\\all_results.npy').item()
results2 = np.load(paths['results'] + '\\' + resultsFolder2 + '\\all_results.npy').item()
results49 =  np.load(paths['results'] + '\\' + results49comb + '\\all_results.npy').item()
#
#plotAngleSavings(results1['monthlyData'], xy = 'x')
#
#
#plotAngleSavings(results2['monthlyData'], xy = 'y')
#
#plotAngleSavings(monthlyData, xy = None)

if False:
    fig = plt.figure(figsize=(16, 5))
    ax = fig.add_subplot(131, projection='3d')
    create3Dplot(results1['monthlyData'], 'E_tot', 'diffMinAltitude', startMonth = 3, endMonth = 3, fig=fig, ax=ax)
    plt.title('March')
    ax = fig.add_subplot(132, projection='3d')
    create3Dplot(results1['monthlyData'], 'E_tot', 'diffMinAltitude', startMonth = 6, endMonth = 6, fig=fig, ax=ax)
    plt.title('June')
    ax = fig.add_subplot(133, projection='3d')
    create3Dplot(results1['monthlyData'], 'E_tot', 'diffMinAltitude', startMonth = 9, endMonth = 9, fig=fig, ax=ax)
    plt.title('September')
#ax = fig.add_subplot(224, projection='3d')
#create3Dplot(results1['monthlyData'], 'E_tot', 'diffMinAltitude', startMonth = 12, endMonth = 12, fig=fig, ax=ax)
#plt.title('December')

# # plot the optimum angles of the monthly data:
##createCarpetPlots(pcolorMonths, results49['monthlyData'], 'xy')
#fig1 = createCarpetPlots(pcolorMonths, results49['monthlyData'], 'x')
#fig2 = createCarpetPlots(pcolorMonths, results49['monthlyData'], 'y')
#
## plot the energy use at the corresponding optimum orientation:
#fig3 = createCarpetPlots(pcolorEnergyMonths, results49['monthlyData'])
#    

compareTotalEnergyForThesis(results49['monthlyData'], True, {'enabled':False}, {'combineResults':True}, roomSize)