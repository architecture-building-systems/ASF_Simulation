# -*- coding: utf-8 -*-
"""
Created on Fri Apr 01 10:57:20 2016

Create Figures Functions

@author: Jeremias
"""

#import numpy as np
import matplotlib.pyplot as plt
import numpy as np

#from average_monthly import sum_monthly, average_monthly, daysPassedMonth
##from PostProcessThermal_functions import pcolorMonths, pcolorEnergyMonths
#from try_nan_values import createMonthsNan
from plotDataFunctions import pcolorMonths, pcolorEnergyMonths, pcolorDays, pcolorEnergyDays,\
                              plotDataForIndices, plotResultsComparison, plotEnergiesOpt




def createDIVAcarpetPlots(plotFunction, DIVA_results, *arg):
    """
    Function that creates carpet plots with optimal x- and y-angle combinations
    for every hour of the year
    """
    
    if not len(arg) == 0:
        rotation_axis = arg[0]
        if arg[0] == 'xy':
            angles = DIVA_results['angles']['allAngles'][0]   
        elif arg[0] == 'x':
            angles = DIVA_results['angles']['x_angles']    
        elif arg[0] == 'y':
            angles = DIVA_results['angles']['y_angles']    
        else:
            raise ValueError('rotation_axis does not exist')
    else:
        rotation_axis = np.nan
    
    #set max/min for energy plot:
    z_min = 0
    z_max = np.max(np.min(DIVA_results['E'], axis=0))
    
    fig = plt.figure(figsize=(16, 8))
#    plt.suptitle("Optimum Altitude and Azimuth Orientation", size=16)
    plt.subplot(2,2,1)
    arg1 = ['min','H', rotation_axis, 'DIVA', z_min, z_max]
    plotFunction(DIVA_results, arg1)
    if DIVA_results['efficienciesChanged']:
        plt.title("Heating Demand COP=" + str(DIVA_results['efficiencyChanges']['H_COP']))
    else:
        plt.title("Heating Demand COP=" + str(DIVA_results['efficiencies']['H_COP']))
    plt.ylabel("Hour of the Day",size=14)
    plt.subplot(2,2,2)
    arg1 = ['min','C', rotation_axis, 'DIVA', z_min, z_max]
    plotFunction(DIVA_results, arg1)
    if DIVA_results['efficienciesChanged']:
        plt.title("Cooling Demand COP=" + str(DIVA_results['efficiencyChanges']['C_COP']))
    else:
        plt.title("Cooling Demand COP=" + str(DIVA_results['efficiencies']['C_COP']))
    plt.subplot(2,2,3)
    arg1 = ['min','L', rotation_axis, 'DIVA', z_min, z_max]
    plotFunction(DIVA_results, arg1)
    if DIVA_results['efficienciesChanged']:
        plt.title("Lighting Demand Load=" + str(DIVA_results['efficiencyChanges']['L_Load']) + " W/m2")
    else:
        plt.title("Lighting Demand Load=" + str(DIVA_results['efficiencies']['L_Load']) + " W/m2")
    plt.xlabel("Day of the Year",size=14)
    plt.ylabel("Hour of the Day",size=14)
    plt.subplot(2,2,4)
    arg1 = ['min','E', rotation_axis, 'DIVA', z_min, z_max]
    plotFunction(DIVA_results, arg1)
    plt.title("Total Thermal/Lighting Demand")
    plt.xlabel("Day of the Year",size=14)
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
            cbart = plt.title("Altitude", fontsize=14)
        elif arg[0] == 'y':
            plt.suptitle("Optimum Azimuth Orientation", size=16)
            cbart = plt.title("Azimuth", fontsize=14)
        cbart.set_position((1.1,1.02))
        cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(angles)))
        cbar.ax.set_yticklabels(angles)
    elif plotFunction == pcolorEnergyMonths:
        plt.suptitle("Energy Demand at Optimum Orientation", size=16)
        cbar = plt.colorbar(cax=cbar_ax)
        cbart = plt.title("Net Energy [kWh]", fontsize=14)
        cbart.set_position((1.1,1.02))
    elif plotFunction == pcolorDays:
        if arg[0] == 'xy':
            plt.suptitle("Optimum Altitude and Azimuth Orientation", size=16)
            cbart = plt.title("Altitude / Azimuth", fontsize=14)
        elif arg[0] == 'x':
            plt.suptitle("Optimum Altitude Orientation", size=16)
            cbart = plt.title("Altitude", fontsize=14)
        elif arg[0] == 'y':
            plt.suptitle("Optimum Azimuth Orientation", size=16)
            cbart = plt.title("Azimuth", fontsize=14)
        cbart.set_position((1.1,1.02))
        cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(angles)))
        cbar.ax.set_yticklabels(angles)
    elif plotFunction == pcolorEnergyDays:
        plt.suptitle("Energy Demand at Optimum Orientation", size=16)
        cbar = plt.colorbar(cax=cbar_ax)
        cbart = plt.title("Net Energy [kWh]", fontsize=14)
        cbart.set_position((1.1,1.02))
#        cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(allAngles[0])))
        #cbar.ax.set_yticklabels(AnglesString)
    cbar.ax.tick_params(labelsize=14)
    plt.show()   
    
    return fig




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
            angles = monthlyData['angles']['x_angles']    
        elif arg[0] == 'y':
            angles = monthlyData['angles']['y_angles']    
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
    plt.title("Heating Demand COP=" + str(usedEfficiencies['H_COP']))
    plt.ylabel("Hour of the Day",size=14)
    plt.subplot(2,3,2)
    arg1 = ['min','C', rotation_axis, 'DIVA', z_min, z_max]
    plotFunction(monthlyData, arg1)
    plt.title("Cooling Demand COP=" + str(usedEfficiencies['C_COP']))
    plt.subplot(2,3,3)
    arg1 = ['min','L', rotation_axis, 'DIVA', z_min, z_max]
    plotFunction(monthlyData, arg1)
    plt.title("Lighting Demand Load=" + str(usedEfficiencies['L_Load']) + " W/m2")
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
            cbart = plt.title("Altitude", fontsize=14)
        elif arg[0] == 'y':
            plt.suptitle("Optimum Azimuth Orientation", size=16)
            cbart = plt.title("Azimuth", fontsize=14)
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

def plotEnergyUsage(monthlyData, auxVar):
    """
    Function that plots the energy usage for the monthly data
    """
    
    # assign data:
    H = monthlyData['H']
    C = monthlyData['C']
    L = monthlyData['L']
    PV = monthlyData['PV']

     # assign what efficiencies were used for evaluation:  
    if monthlyData['changedEfficiency'] == True:
        usedEfficiencies = monthlyData['efficiencyChanges']
    else:
        usedEfficiencies = monthlyData['efficiencies']
    
    # sum individual data
    E_HCL = H+C+L
    
    if auxVar['combineResults']:
        E_tot = E_HCL+PV
    else:
        E_tot = E_HCL*np.nan
    
    # find indices
    Hind = np.argmin(H,axis=0)
    Cind = np.argmin(C,axis=0)
    Lind = np.argmin(L,axis=0)
    PVind = np.argmin(PV,axis=0)
    E_HCLind = np.argmin(E_HCL,axis=0)
    PVCind = np.argmin(C+PV,axis=0)
    
    if auxVar['combineResults']:
        E_totind = np.argmin(E_tot,axis=0)
        ind_0_0 =  monthlyData['angles']['allAngles'][0].index((0,0))
        ind_45_0 =  monthlyData['angles']['allAngles'][0].index((45,0))
        ind_90_0 =  monthlyData['angles']['allAngles'][0].index((90,0))
    else:
        ind_0_0 =  monthlyData['divaAngles']['allAngles'][0].index((0,0))
        ind_45_0 =  monthlyData['divaAngles']['allAngles'][0].index((45,0))
        ind_90_0 =  monthlyData['divaAngles']['allAngles'][0].index((90,0))

    indices = {'H':Hind, 'C':Cind, 'L':Lind, 'PV':PVind, 'E_HCL':E_HCLind, 'E_tot':E_totind, 'PVC':PVCind, '0':ind_0_0, '45':ind_45_0, '90':ind_90_0}    
    
    figures = {}
    
    # create figures
    figures['H'] = plotDataForIndices(monthlyData,indices, usedEfficiencies, ['H'])
    figures['C'] = plotDataForIndices(monthlyData,indices, usedEfficiencies, ['C'])
    figures['L'] = plotDataForIndices(monthlyData,indices, usedEfficiencies, ['L'])
    figures['PV'] = plotDataForIndices(monthlyData,indices, usedEfficiencies, ['PV'])
    figures['E_HCL'] = plotDataForIndices(monthlyData,indices, usedEfficiencies, ['E_HCL'])
    figures['E_tot'] = plotDataForIndices(monthlyData,indices, usedEfficiencies, ['E_tot'])
    figures['compare'] =  plotEnergiesOpt(monthlyData, indices['E_tot'])
    
    # add titles to figures
    figures['H'].suptitle('Heating Demand (COP=' + str(usedEfficiencies['H_COP']) + ')')
    figures['C'].suptitle('Cooling Demand (COP=' + str(usedEfficiencies['C_COP']) + ')')
    figures['L'].suptitle('Lighting Demand (Load=' + str(usedEfficiencies['L_Load']) + ' W/m2)')
    figures['PV'].suptitle('PV Generation')
    figures['E_HCL'].suptitle('Thermal/Lighting Demand')
    figures['E_tot'].suptitle('Total Demand')
    
    return figures

def compareResultsFigure(monthlyData1, monthlyData2):
    """ 
    function that plots the energy of two different monthlyData files
    """
    
    ############ data 1    
    
    # assign data:
    H1 = monthlyData1['H']
    C1 = monthlyData1['C']
    L1 = monthlyData1['L']
    PV1 = monthlyData1['PV']

     # assign what efficiencies were used for evaluation:  
    if monthlyData1['changedEfficiency'] == True:
        usedEfficiencies1 = monthlyData1['efficiencyChanges']
    else:
        usedEfficiencies1 = monthlyData1['efficiencies']
    
    # sum individual data
    E_HCL1 = H1+C1+L1
    E_tot1 = E_HCL1+PV1
    
    # find indices
    E_totind1 = np.argmin(E_tot1,axis=0)
    
    
    
    ################## data 2
    
     # assign data:
    H2 = monthlyData2['H']
    C2 = monthlyData2['C']
    L2 = monthlyData2['L']
    PV2 = monthlyData2['PV']

     # assign what efficiencies were used for evaluation:  
#    if monthlyData2['changedEfficiency'] == True:
#        usedEfficiencies2 = monthlyData2['efficiencyChanges']
#    else:
#        usedEfficiencies2 = monthlyData2['efficiencies']
        
    # sum individual data
    E_HCL2 = H2+C2+L2
    E_tot2 = E_HCL2+PV2
    
    # find indices
    E_totind2 = np.argmin(E_tot2,axis=0)

    indices = {'E_tot1':E_totind1, 'E_tot2':E_totind2 }    
    
#    if usedEfficiencies1 == usedEfficiencies2:
#        usedEfficiencies = usedEfficiencies1
    
    figures = {}
    
    # create figures
    figures['H'] = plotResultsComparison(monthlyData1, monthlyData2, indices, ['H'])
    figures['C'] = plotResultsComparison(monthlyData1, monthlyData2, indices, ['C'])
    figures['L'] = plotResultsComparison(monthlyData1, monthlyData2, indices, ['L'])
    figures['PV'] = plotResultsComparison(monthlyData1, monthlyData2, indices, ['PV'])
    figures['E_HCL'] = plotResultsComparison(monthlyData1, monthlyData2, indices, ['E_HCL'])
    figures['E_tot'] = plotResultsComparison(monthlyData1, monthlyData2, indices, ['E_tot'])
    
    # add titles to figures
    figures['H'].suptitle('Heating Demand')
    figures['C'].suptitle('Cooling Demand')
    figures['L'].suptitle('Lighting Demand')
    figures['PV'].suptitle('PV Generation')
    figures['E_HCL'].suptitle('Thermal/Lighting Demand')
    figures['E_tot'].suptitle('Total Demand')
    
    return figures
