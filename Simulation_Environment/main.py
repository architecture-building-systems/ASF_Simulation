# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:14:42 2016

main file for simulation environment

@author: Jeremias
"""

import os, sys
import numpy as np
import json
import time
import warnings


######### -----USER INTERACTION------ #############

# set mode of this main script ('initialize', 'post_processing'):

mainMode = 'post_processing' #'initialize'
#mainMode = 'post_processing' #'initialize'

# specify the location used for the analysis - this name must be the same as a
# folder in the directory .../ASF_Simulation/Simulation_Environment/data/geographical_location
# new locations can be added with the grasshopper main script for any .epw weather data

geoLocation = 'Zuerich-Kloten' # 'Zuerich-Kloten', 'MADRID_ESP', 'SINGAPORE_SGP'
#geoLocation = 'MADRID_ESP' # 'Zuerich-Kloten', 'MADRID_ESP'
#geoLocation = 'SINGAPORE_SGP' # 'Zuerich-Kloten', 'MADRID_ESP', 'SINGAPORE_SGP'


# set folder name of DIVA simulation data (in data\grasshopper\DIVA):

#diva_folder = 'Simulation_Madrid_25comb' #'Simulation_Kloten_25comb'
diva_folder = 'DIVA_Kloten_25comb_1Infilt'
#diva_folder = 'DIVA_Kloten_25comb_W'
#diva_folder = 'DIVA_Kloten_49comb_1Infilt'
#diva_folder = 'DIVA_Kloten_noShade_E'
#diva_folder = 'DIVA_Kloten_2clust_5x_1y'
#diva_folder = 'DIVA_Kloten_7x_13y'
#diva_folder = 'DIVA_Kloten_1x_19y'
#diva_folder = 'DIVA_Kloten_1x_19y_1Infilt'
#diva_folder = 'DIVA_Singapore_25comb'


# set folder name of LadyBug simulation data (in data\grasshopper\LadyBug). 
# This folder has the same name as the generated folder for the electrical 
# results in data\python\electrical:

#radiation_folder = 'Radiation_Kloten_25comb'
radiation_folder = 'Radiation_Kloten_25comb_largeContext'
#radiation_folder = 'Radiation_Kloten_25comb_W'
#radiation_folder = 'Radiation_Kloten_tracking'
#radiation_folder = 'Radiation_Kloten_49comb'
#radiation_folder = 'Radiation_Dummy_NoShade'
#radiation_folder = 'Radiation_Kloten_2clust_5x_1y'
#radiation_folder = 'Radiation_Kloten_7x_13y'
#radiation_folder = 'Radiation_Kloten_1x_19y'
#radiation_folder = 'Radiation_Kloten_1x_19y'
#radiation_folder = 'Radiation_electrical_monthly_25comb_Madrid'
#radiation_folder = 'Radiation_Singapore_25comb'


# set option to change the size of the PV area for the electrical simulation, 
# this is done in steps of 2 times the radiation gridsize, so 0 corresponds a 
# PV-size of 400mm, 1 corresponds to PV-size of 350mm, 2 corresponds to 300mm 
# etc.:
pvSizeOption = 0

# set option to flip orientation of PV cells on the panels. False means the cells 
# are parallel to the edge from the left to the upper corner, True means the cells 
# are parallel to the edge from the upper to the right corner:
pvFlipOrientation = True


# specify if  plots should be created (True or False):
createPlots = True

# only tradeoffs flag, set true if general data plots should not be evaluated:
onlyTradeoffs = False

# specify if detailed DIVA results should be shown (hourly values for the whole year):
showDetailedDIVA = False

# post processing options: change efficiencies of heating(COP)/
# cooling(COP)/lighting(Lighting Load)/PV(Factor by which results are multiplied)
# set changeEfficiency to True if data should be changed, set False if simulation efficiencies should be used:
efficiencyChanges = {'changeEfficiency':False, 'H_COP': 4, 'C_COP': 3, 'L_Load': 11.74, 'PV': 0}


# define tradeoff period and if it should be enabled, startHour and endHour are
# inclusive, so startHour=1 and endHour=24 corresponds to a time period from 
# 0:00-24:00. month is defined in the classical sense, so month=1 corresponds to 
# january. Currently, only one month at a time can be selected.
tradeoffPeriod = {'enabled':False, 'month':7, 'startHour':1, 'endHour':24}

# options to specify what results should be saved:
#saveResults = {'csvSummary':True, 'figures':True, 'npyData':True}
saveResults = {'csvSummary':True, 'figures':False, 'npyData':True}


#setting to only evaluate certain configurations available in the total monthly
#data set, use this setting with care, as it is not fully tested yet and you 
#must be sure that you know what combinations you are extracting. The 'rows' list
#corresponds to the rows in the monthlyData structure (starting with 0). The setting
#does not yet have any effect on the DIVA data, so only combined evaluation will be affected.
#especially the results csv file will still show all angles, even though only some
#are evaluated.
changeMonthlyData = {'enabled':False, 'rows':[2,7,12,17,22]}
#changeMonthlyData = {'enabled':True, 'rows':[5,6,7,8,9]}
#changeMonthlyData = {'enabled':True, 'rows':[10,11,12,13,14]}
#changeMonthlyData = {'enabled':True, 'rows':[0,2,4,10,12,14,20,22,24]}
#changeMonthlyData = {'enabled':True, 'rows':[12]}


    
    
    
######### -----END OF USER INTERACTION------ ############
    
    
    
# get current time
now = time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
print "simulation start: " + now

print "variables set"

# create empty dictionary with auxiliary variables
auxVar = {}

# create dictionary to write all paths:
paths = {}

# find path of current folder (simulation_environment)
paths['main'] = os.path.abspath(os.path.dirname(sys.argv[0]))

# define paths of subfolders:
paths['data'] = paths['main'] + '\\data'
paths['python'] = paths['main'] + '\\python'
paths['gh'] = paths['main'] + '\\grasshopper'
paths['results'] = paths['main'] + '\\results'

# add python_path to system path, so that all files are available:
sys.path.insert(0, paths['python'] + '\\aux_files')

# define paths of data_folders:
paths['diva'] = os.path.join(( paths['data'] + "\grasshopper\DIVA"), diva_folder)
paths['lb'] = os.path.join(( paths['data'] + "\grasshopper\LadyBug"), radiation_folder)
paths['electrical'] = os.path.join(( paths['data'] + "\python\electrical_simulation"), radiation_folder)


print "paths defined"

if mainMode == 'initialize':
    
    print "start initializing"
    

    
    # define path of geographical location:
    paths['geo'] = os.path.join(( paths['data'] + "\geographical_location"), geoLocation)
    # create sun data based on grasshopper file
    execfile(paths['python'] + "\\aux_files\\SunAngles_Tracking_and_temperature.py")

    # calculate and save lookup table if it does not yet exist:
    if not os.path.isfile(paths['data'] + '\python\electrical_simulation\curr_model_submod_lookup.npy'): 
        if not os.path.isdir(paths['data'] + '\python\electrical_simulation'):
            os.makedirs(paths['data'] + '\python\electrical_simulation')
        execfile(paths['python'] + '\\aux_files\\create_lookup_table.py')
    else:
        print 'lookup table not created as it already exists'
    
# calculate and save PV electricity production:
if mainMode == 'post_processing':
    
    print "start post processing"
    
    from prepareData import prepareMonthlyRadiatonData, importDIVAresults, \
        readLayoutAndCombinations, CalcXYAnglesAndLocation, sum_monthly, changeDIVAresults
        
    from auxFunctions import changeMonthlyDataFunction
    
    # create dictionary to save monthly data:
    monthlyData = {}
    
    # create dictionary with ladybug simulation settings:
    lbSettings = {}
    
    # panelsize used for simulation:
    lbSettings['panelsize'] = readLayoutAndCombinations(paths['lb'])['panelSize']  
    
    # desired grid point size used for simulation:
    lbSettings['desiredGridPointSize'] = readLayoutAndCombinations(paths['lb'])['desiredGridPointSize']  
    
    # actual grid point size used for simulation:
    lbSettings['actualGridPointSize'] = lbSettings['panelsize']/(round(lbSettings['panelsize']/float(lbSettings['desiredGridPointSize'])))
    
    # calculate aperturesize according to pvSizeOption:
    lbSettings['aperturesize'] = int(lbSettings['panelsize'] - pvSizeOption*2*lbSettings['actualGridPointSize'])
    
    # define path of geographical location:
    paths['geo'] = os.path.join(( paths['data'] + "\geographical_location"), geoLocation)
    
    # load sunTrackingData used for the LadyBug simulation:
    with open(paths['geo'] + '\SunTrackingData.json', 'r') as fp:
        SunTrackingData = json.load(fp)
        fp.close()
        
    # find the number of hours analysed by ladybug:
    lbSettings['numHoursLB'] = np.shape(SunTrackingData['HOY'])[0]
    
    # find the number of combinations analysed by ladybug:
    lbSettings['numCombLB'] = len(CalcXYAnglesAndLocation(readLayoutAndCombinations(paths['lb']))['allAngles'][0])
    
    # define path of pv results folder for specified settings:
    if not pvFlipOrientation:
        paths['PV'] = paths['electrical'] + '\\aperturesize_' + str(lbSettings['aperturesize'])
    elif pvFlipOrientation:
        paths['PV'] = paths['electrical'] + '\\aperturesize_' + str(lbSettings['aperturesize']) + '_oppositeOrientation'
    else:
        print 'setting for pvFlipOrientation is wrong'


    # check if pv results already exist, if not, create them, else load them
    if not os.path.isfile(paths['PV'] + '\PV_electricity_results.npy'): 
        if not os.path.isdir(paths['PV']):
            os.makedirs(paths['PV'])
        from asf_electricity_production import asf_electricity_production
        print 'calculating PV electricity production'     
        
        if createPlots:
            PV_electricity_results, PV_detailed_results, fig1, fig2 = \
            asf_electricity_production(createPlots=createPlots, 
                                       lb_radiation_path=paths['lb'], 
                                       panelsize=lbSettings['panelsize'], 
                                       pvSizeOption=pvSizeOption, 
                                       save_results_path = paths['PV'],
                                       lookup_table_path = paths['data'] + '\python\electrical_simulation',
                                       geo_path=paths['geo'],
                                       flipOrientation = pvFlipOrientation)
        else:
            PV_electricity_results, PV_detailed_results= \
            asf_electricity_production(createPlots=createPlots, 
                                       lb_radiation_path=paths['lb'], 
                                       panelsize=lbSettings['panelsize'], 
                                       pvSizeOption=pvSizeOption, 
                                       save_results_path = paths['PV'],
                                       lookup_table_path = paths['data'] + '\python\electrical_simulation',
                                       geo_path=paths['geo'],
                                       flipOrientation = pvFlipOrientation)
    else: 
        PV_electricity_results = np.load(paths['PV'] + '\PV_electricity_results.npy').item()
        PV_detailed_results = np.load(paths['PV'] + '\PV_detailed_results.npy').item()
        print 'PV_electricity_results loaded from folder'
        
    print "preparing data"
    
    # prepare monthly PV and Radiation data and write it to the monthlyData dictionary:
    monthlyData['efficiencies'] = {}
    monthlyData['PV'], monthlyData['R'], monthlyData['efficiencies']['PV'],  monthlyData['R_avg'],\
    monthlyData['R_theo'], monthlyData['PV_avg'], monthlyData['PV_eff'] \
                                        = prepareMonthlyRadiatonData(PV_electricity_results)
    
    # make pv data negative to be consistent with H,C and L:    
    monthlyData['PV'] = -monthlyData['PV']
    monthlyData['R'] = monthlyData['R']
    
    # change PV data if demanded:
    if efficiencyChanges['changeEfficiency']:
        if not efficiencyChanges['PV']==1:
            print 'multiplying PV electricity data by a factor of: ' + str(efficiencyChanges['PV'])
        monthlyData['PV'] = monthlyData['PV'] * efficiencyChanges['PV']
        monthlyData['changedEfficiency'] = True
        monthlyData['efficiencyChanges'] = efficiencyChanges
    else:
        monthlyData['changedEfficiency'] = False
        
        
    # import DIVA results:
    DIVA_results = importDIVAresults(paths['diva'])    
    
    # change efficiencies of DIVA results if demanded:
    if efficiencyChanges['changeEfficiency']:
        DIVA_results = changeDIVAresults(DIVA_results, efficiencyChanges)
    
    # import DIVA LayoutAndCombinations and write to DIVA_results dict.:
    DIVA_results['LayoutAndCombinations'] = readLayoutAndCombinations(paths['diva'])
    
    # calculate angles of DIVA_results
    DIVA_results['angles'] = CalcXYAnglesAndLocation(DIVA_results['LayoutAndCombinations'])

    # import LadyBug LayoutAndCombinations and write to PV_electricity_results dict.:
    PV_electricity_results['LayoutAndCombinations'] = readLayoutAndCombinations(paths['lb'])
    
    # check if the two LayoutAndCombinations files are the same
    if DIVA_results['LayoutAndCombinations'] == PV_electricity_results['LayoutAndCombinations']:
        # calculate angles corresponding to the layoutAndCombination file:
        monthlyData['angles'] = CalcXYAnglesAndLocation(DIVA_results['LayoutAndCombinations'])
        # set variable that allows combined analysis of DIVA and LB results:
        auxVar['combineResults'] = True
    else:
        warnings.warn('LayoutAndCombination of DIVA and LadyBug files are not the same, check the data-folders!')
        
        # assign layout and combinations seperately:
        monthlyData['divaAngles'] =  CalcXYAnglesAndLocation(DIVA_results['LayoutAndCombinations'])
        monthlyData['lbAngles'] =  CalcXYAnglesAndLocation(PV_electricity_results['LayoutAndCombinations'])
        
        # set variable that prevents combined analysis of DIVA and LB:
        auxVar['combineResults'] = False
        
    # sum up data for every month:
    monthlyData['H'] = sum_monthly(DIVA_results['H'])
    monthlyData['C'] = sum_monthly(DIVA_results['C'])
    monthlyData['L'] = sum_monthly(DIVA_results['L'])
    monthlyData['E_HCL'] = sum_monthly(DIVA_results['E'])
    
    if auxVar['combineResults']:
        monthlyData['E_tot'] = monthlyData['E_HCL'] + monthlyData['PV']
    
    # add DIVA efficiencies to monthly data dictionary:
    #monthlyData['efficiencies']['L_load'] = DIVA_results['efficiencies'][] 
    monthlyData['efficiencies'].update(DIVA_results['efficiencies'])
    
    if changeMonthlyData['enabled']:
        monthlyData = changeMonthlyDataFunction(monthlyData,changeMonthlyData['rows'])
        
    # create figure handle dictionary:
    figureHandles = {}
    
    if createPlots and not onlyTradeoffs:
        
        print "creating plots"
        

        from createMasks import createDIVAmask, createLBmask
        from createFigures import createCarpetPlots, createDIVAcarpetPlots
        from plotDataFunctions import pcolorMonths, pcolorEnergyMonths, pcolorDays, pcolorEnergyDays
        
        if showDetailedDIVA:
            # plot detailed DIVA Results:
            figureHandles['DIVAxy'] = createDIVAcarpetPlots(pcolorDays, DIVA_results, 'xy')
            figureHandles['DIVAx'] = createDIVAcarpetPlots(pcolorDays, DIVA_results, 'x')
            figureHandles['DIVAy'] = createDIVAcarpetPlots(pcolorDays, DIVA_results, 'y')
            figureHandles['DIVAe'] = createDIVAcarpetPlots(pcolorEnergyDays, DIVA_results)        
        
        # create masks for plotting:
        monthlyData['DIVAmask'] = createDIVAmask(monthlyData['L'])
        monthlyData['LBmask'] = createLBmask(monthlyData['R'])
        
        if auxVar['combineResults']:
            # plot the optimum angles of the monthly data:
            figureHandles['CarpetXY'] = createCarpetPlots(pcolorMonths, monthlyData, 'xy')
            figureHandles['CarpetX'] = createCarpetPlots(pcolorMonths, monthlyData, 'x')
            figureHandles['CarpetY'] = createCarpetPlots(pcolorMonths, monthlyData, 'y')
        
            # plot the energy use at the corresponding optimum orientation:
            figureHandles['CarpetE'] = createCarpetPlots(pcolorEnergyMonths, monthlyData)
    
    
    from auxFunctions import create_evalList
    from Tradeoffs import compareTotalEnergy
    from createFigures import plotEnergyUsage
    
    if tradeoffPeriod['enabled']:
        tradeoffPeriod['evalList'] = create_evalList('monthly', tradeoffPeriod['month'], tradeoffPeriod['startHour'], tradeoffPeriod['endHour'])
    else:
        tradeoffPeriod['evalList'] = []
    
    # evaluate tradeoffs:
    TradeoffResults, figureHandles['Tradeoffs'] = compareTotalEnergy(monthlyData, createPlots, tradeoffPeriod, auxVar)
    
    
    print 'Heating Energy Demand:' + str(TradeoffResults['energy_opttot']['H'])
    print 'Cooling Energy Demand:' + str(TradeoffResults['energy_opttot']['C'])
    print 'Lighting Energy Demand:' + str(TradeoffResults['energy_opttot']['L'])
    print 'PV Energy Production:' + str(TradeoffResults['energy_opttot']['PV'])
    print 'Total Energy Demand:' + str(TradeoffResults['energy_opttot']['E_tot'])
    
    if createPlots:
        # plot figures for each energy usage:    
        figureHandles.update(plotEnergyUsage(monthlyData, auxVar))

    monthList = ['January','February','March','April','May','June','July','August','September','November','October','December']
    
    # create folder where results will be saved:
    os.makedirs(paths['results'] + '\\' + now )
    
    if auxVar['combineResults'] and saveResults['csvSummary']:
        # write csv file that summarizes results  
        with open(paths['results'] + '\\' + now + '\\summary.csv', 'w') as f:
            f.write('Simulation Results\n\n')
            f.write('Location\n' + geoLocation + '\n\n')
            f.write('Number of Combinations\n' + str(lbSettings['numCombLB']) + '\n\n')
            f.write('Azimuth Angles\n')
            [f.write('{0};'.format(value)) for value in PV_electricity_results['LayoutAndCombinations']['Yangles']]
            f.write('\n\nAltitude Angles\n')
            [f.write('{0};'.format(value)) for value in PV_electricity_results['LayoutAndCombinations']['Xangles']]
            f.write('\n\nNumber of Clusters\n')
            f.write(str(int(PV_electricity_results['LayoutAndCombinations']['NoClusters'])) + '\n\n')
            f.write('Panel Size [mm]\n')
            f.write(str(int(PV_electricity_results['LayoutAndCombinations']['panelSize'])) + '\n\n')
            f.write('Aperture Size [mm]\n')
            f.write(str(int(lbSettings['aperturesize'])) + '\n\n')
            f.write('Panel Spacing [mm] (shortest midpoint to midpoint distance)\n')
            f.write(str(int(PV_electricity_results['LayoutAndCombinations']['panelSpacing'])) + '\n\n')
            f.write('Number of Panels\n')
            f.write(str(int(np.shape(PV_detailed_results['Ins_ap'])[1])) + '\n\n')
            f.write('Evaluation Period\n')
            if tradeoffPeriod['enabled']:
                f.write('Energy Usage evaluated for the cumulative hours ' + 
                        str(tradeoffPeriod['startHour']-1) + ':00-' + 
                        str(tradeoffPeriod['endHour']) + ':00 in ' + 
                        monthList[tradeoffPeriod['month']-1] +'\n\n')
            else:
                f.write('Energy Usage evaluated for the whole year\n\n')
                
            if efficiencyChanges['changeEfficiency']:
                f.write('Heating COP\n')
                f.write(str(efficiencyChanges['H_COP']) + '\n\n')
                f.write('Cooling COP\n')
                f.write(str(efficiencyChanges['C_COP']) + '\n\n')
                f.write('Lighting Load [W/m2]\n')
                f.write(str(efficiencyChanges['L_Load']) + '\n\n')
                f.write('Average PV Efficiency [%]\n')
                f.write(str(np.round(efficiencyChanges['PV']*monthlyData['efficiencies']['PV']*100, decimals = 1)) + '\n\n')
            else:
                f.write('Heating COP\n')
                f.write(str(monthlyData['efficiencies']['H_COP']) + '\n\n')
                f.write('Cooling COP\n')
                f.write(str(monthlyData['efficiencies']['C_COP']) + '\n\n')
                f.write('Lighting Load [W/m2]\n')
                f.write(str(monthlyData['efficiencies']['L_Load']) + '\n\n')
                f.write('Average PV Efficiency [%]\n')
                f.write(str(np.round(monthlyData['efficiencies']['PV']*100, decimals = 1)) + '\n\n')
            
            f.write('PV Elongation\n')            
            if pvFlipOrientation:
                f.write('parallel to upper right edge\n\n')
            else:
                f.write('parallel to upper left edge\n\n')
            
            f.write('Net Energy Demand [kWh]\n')
            f.write(';optimized;fixed at 90 deg;fixed at 45 deg;fixed at 0 deg\n')
            f.write('Heating;'+str(TradeoffResults['energy_opttot']['H'])+';'+str(TradeoffResults['energy_90']['H'])+';'+str(TradeoffResults['energy_45']['H'])+';'+str(TradeoffResults['energy_0']['H']) +'\n')
            f.write('Cooling;'+str(TradeoffResults['energy_opttot']['C'])+';'+str(TradeoffResults['energy_90']['C'])+';'+str(TradeoffResults['energy_45']['C'])+';'+str(TradeoffResults['energy_0']['C'])+'\n')
            f.write('Lighting;'+str(TradeoffResults['energy_opttot']['L'])+';'+str(TradeoffResults['energy_90']['L'])+';'+str(TradeoffResults['energy_45']['L'])+';'+str(TradeoffResults['energy_0']['L'])+'\n')
            f.write('PV;'+str(TradeoffResults['energy_opttot']['PV'])+';'+str(TradeoffResults['energy_90']['PV'])+';'+str(TradeoffResults['energy_45']['PV'])+';'+str(TradeoffResults['energy_0']['PV'])+'\n')
            f.write('Total;'+str(TradeoffResults['energy_opttot']['E_tot'])+';'+str(TradeoffResults['energy_90']['E_tot'])+';'+str(TradeoffResults['energy_45']['E_tot'])+';'+str(TradeoffResults['energy_0']['E_tot'])+'\n')
    
            f.close()
    
    if saveResults['npyData']:
        
        if auxVar['combineResults']:
            # bundle all results into one dictionary
            all_results = {'DIVA_results':DIVA_results, 'PV_detailed_results':PV_detailed_results, 
                           'PV_electricity_results':PV_electricity_results, 'SunTrackingData':SunTrackingData, 
                           'TradeoffResults':TradeoffResults, 'diva_folder':diva_folder, 'efficiencyChanges':efficiencyChanges,
                           'geoLocation':geoLocation, 'lbSettings':lbSettings, 'monthlyData':monthlyData, 
                           'radiation_folder':radiation_folder, 'tradeoffPeriod':tradeoffPeriod}
        else:
            # bundle all results into one dictionary
            all_results = {'DIVA_results':DIVA_results, 'PV_detailed_results':PV_detailed_results, 
                           'PV_electricity_results':PV_electricity_results, 'SunTrackingData':SunTrackingData, 
                           'diva_folder':diva_folder, 'efficiencyChanges':efficiencyChanges,
                           'geoLocation':geoLocation, 'lbSettings':lbSettings, 'monthlyData':monthlyData, 
                           'radiation_folder':radiation_folder}
        # save all results
        np.save(paths['results'] + '\\' + now + '\\all_results.npy', all_results)
        
        # save energy results
        np.save(paths['results'] + '\\' + now + '\\energy_results.npy', TradeoffResults)
        
        print 'saved numpy data'
        
    if saveResults['figures'] and createPlots:
        
        # create folder to save figures as png:
        os.makedirs(paths['results'] + '\\' + now + '\\png' )
        [figureHandles[i].savefig(paths['results'] + '\\' + now + '\\png\\' + i + '.png')  for i in figureHandles]
        
        # create folder to save figures as svg:
        os.makedirs(paths['results'] + '\\' + now + '\\svg' )
        [figureHandles[i].savefig(paths['results'] + '\\' + now + '\\svg\\' + i + '.svg')  for i in figureHandles]
        
        print 'saved figures'
print "simulation end: " + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())