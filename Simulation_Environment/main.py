# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:14:42 2016

main file for simulation environment

@author: Jeremias
"""

import os, sys
import numpy as np


######### -----USER INTERACTION------ #############

# set mode of this main script ('initialize', 'post_processing')
mainMode = 'post_processing' #'initialize'

# specify the location used for the analysis - this name must be the same as a
# folder in the directory .../ASF_Simulation/Simulation_Environment/data/geographical_location
# new locations can be added with the grasshopper main script for any .epw weather data
geoLocation = 'Zuerich-Kloten' # 'Zuerich-Kloten', 'MADRID_ESP'

# set folder name of DIVA simulation data (in data\grasshopper\DIVA):
diva_folder = 'Simulation_Kloten_25comb'


# set the number of combinations used for the analysis
numCombDIVA = 25


# set folder name of LadyBug simulation data (in data\grasshopper\LadyBug). 
# This folder has the same name as the generated folder for the electrical 
# results in data\python\electrical:
radiation_folder = 'Radiation_electrical_monthly_25comb'

# set the number of combinations and hours used for the LadyBug analysis:
numCombLB = 25
numHoursLB = 145

# set option to change the size of the PV area for the electrical simulation, 
# this is done in steps of 2 times the radiation gridsize, so 0 corresponds a 
# PV-size of 400mm, 1 corresponds to PV-size of 350mm, 2 corresponds to 300mm 
# etc.:
pvSizeOption = 0


# specify if  plots should be created (True or False):
createPlots = True



######### -----END OF USER INTERACTION------ #############






# find path of current folder (simulation_environment)
main_path = os.path.abspath(os.path.dirname(sys.argv[0]))

# define paths of subfolders:
data_path = main_path + '\data'
python_path = main_path + '\python'
gh_path = main_path + '\grasshopper'

# add python_path to system path, so that all files are available:
sys.path.insert(0, python_path)

# define paths of data_folders:
diva_path = os.path.join(( data_path + "\grasshopper\DIVA"), diva_folder)
lb_path = os.path.join(( data_path + "\grasshopper\LadyBug"), radiation_folder)
electrical_path = os.path.join(( data_path + "\python\electrical_simulation"), radiation_folder)

if mainMode == 'initialize':
    # define path of geographical location:
    geo_path = os.path.join(( data_path + "\geographical_location"), geoLocation)
    # create sun data based on grasshopper file
    execfile(python_path + "\SunAngles_Tracking_and_temperature.py")

    # calculate and save lookup table if it does not yet exist:
    if not os.path.isfile(data_path + '\python\electrical_simulation\curr_model_submod_lookup.npy'): 
        execfile(python_path + '\create_lookup_table.py')
    else:
        print 'lookup table not created as it already exists'
    
# calculate and save PV electricity production:
if mainMode == 'post_processing':
    
    from prepareData import prepareMonthlyRadiatonData, importDIVAresults, readLayoutAndCombinations, CalcXYAnglesAndLocation, sum_monthly
    
    # create dictionary to save monthly data:
    monthlyData = {}
    
    # set panelsize used for simulations (sidelength in mm):
    panelsize = 400
    
    # calculate aperturesize according to pvSizeOption:
    aperturesize = panelsize - pvSizeOption*50
    
    # check if pv results already exist, if not, create them, else load them
    if not os.path.isfile(electrical_path + '\\aperturesize_' + str(aperturesize) + '\PV_electricity_results.npy'): 
        if not os.path.isdir(electrical_path + '\\aperturesize_' + str(aperturesize)):
            os.makedirs(electrical_path + '\\aperturesize_' + str(aperturesize))
        from asf_electricity_production import asf_electricity_production
        print 'calculating PV electricity production'        
        PV_electricity_results, PV_detailed_results, fig1, fig2= asf_electricity_production(numHours=numHoursLB, numComb=numCombLB, createPlots=createPlots, lb_radiation_path=lb_path, panelsize=panelsize, pvSizeOption=pvSizeOption, save_results_path = electrical_path + '\\aperturesize_' + str(aperturesize), lookup_table_path = data_path + '\python\electrical_simulation')
    else: 
        PV_electricity_results = np.load(electrical_path + '\\aperturesize_' + str(aperturesize) + '\PV_electricity_results.npy').item()
        print 'PV_electricity_results loaded from folder'
        
    # prepare monthly PV and Radiation data and write it to the monthlyData dictionary:
    monthlyData['PV'], monthlyData['R']  = prepareMonthlyRadiatonData(PV_electricity_results)
    
    # import DIVA results:
    DIVA_results = importDIVAresults(diva_path)    
    
    # import DIVA LayoutAndCombinations and write to DIVA_results dict.:
    DIVA_results['LayoutAndCombinations'] = readLayoutAndCombinations(diva_path)

    # import LadyBug LayoutAndCombinations and write to PV_electricity_results dict.:
    PV_electricity_results['LayoutAndCombinations'] = readLayoutAndCombinations(lb_path)
    
    # check if the two LayoutAndCombinations files are the same
    if DIVA_results['LayoutAndCombinations'] == PV_electricity_results['LayoutAndCombinations']:
        # calculate angles corresponding to the layoutAndCombination file:
        monthlyData['angles'] = CalcXYAnglesAndLocation(DIVA_results['LayoutAndCombinations'])
    else:
        raise ValueError('LayoutAndCombination of DIVA and LadyBug files are not the same, check the data-folders!')
        
    # sum up data for every month:
    monthlyData['H'] = sum_monthly(DIVA_results['H'])
    monthlyData['C'] = sum_monthly(DIVA_results['C'])
    monthlyData['L'] = sum_monthly(DIVA_results['L'])
    monthlyData['E_HCL'] = sum_monthly(DIVA_results['E'])
    monthlyData['E_tot'] = monthlyData['E_HCL'] - monthlyData['PV']
    
    if createPlots:
        from createMasks import createDIVAmask, createLBmask
        from createFigures import createCarpetPlots
        from plotDataFunctions import pcolorMonths
        
        # create masks for plotting:
        monthlyData['DIVAmask'] = createDIVAmask(monthlyData['L'])
        monthlyData['LBmask'] = createLBmask(monthlyData['R'])
        
        # plot the monthly data
        createCarpetPlots(pcolorMonths, monthlyData, 'xy')
        createCarpetPlots(pcolorMonths, monthlyData, 'x')
        createCarpetPlots(pcolorMonths, monthlyData, 'y')
        


    
    # prepare monthly DIVA data and write it to the monthlyData dictionary:

       #execfile(python_path + "\PostProcessRadiation.py")