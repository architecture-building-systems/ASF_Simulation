# -*- coding: utf-8 -*-
"""
Created on Tue Nov 08 11:42:45 2016

@author: Mauro
"""

import os, sys
import numpy as np
import json
import time
import warnings
import csv
import matplotlib.pyplot as plt
import pandas as pd

def initializeSimulation(SimulationData):
           
    #check if E_total is selcted
    count = 0
    for ii in SimulationData['optimizationTypes']:  
        if ii == 'E_total':
            pass
        elif ii != 'E_total':
            count +=1
    if count == len(SimulationData['optimizationTypes']):       
        print '\nE_total is needed as default!'
        print 'Change the optimizationTypes.\n'
        sys.exit()
    else:
        pass
    
    
    #Set panel data
    FolderName={
    "DataNamePV": SimulationData['DataName'],
    "DataNameWin": SimulationData['DataName']  
    }
    
    #Save parameters to be imported into grasshopper
    with open('FolderName.json','w') as f:
        f.write(json.dumps(FolderName))    
            
    
    return FolderName

def initializeASF(panel_data):
  
    #Save parameters to be imported into grasshopper
    with open('panel.json','w') as f:
        f.write(json.dumps(panel_data))
        

def setBuildingParameters(building_data):
    
    #Save parameters to be imported into grasshopper
    with open('building.json','w') as f:
        f.write(json.dumps(building_data))
    
    roomFloorArea = building_data['room_width']/1000.0 * building_data['room_depth']/1000.0 #[m^2] floor area
    
    return roomFloorArea
    
    
def initializeBuildingSimulation(building_data, BuildingProperties):
    #set building properties for the RC-Model analysis 
    BuildingProperties.update({
            "Fenst_A": building_data['room_width']/1000.0*building_data['room_height']/1000.0*building_data['glazing_percentage_h']*building_data['glazing_percentage_w'],
            "Room_Depth": building_data['room_depth']/1000.0,
            "Room_Width": building_data['room_width']/1000.0,
            "Room_Height":building_data['room_height']/1000.0})                
        
    return BuildingProperties
    
    
def setPaths(geoLocation, Occupancy, FolderName):
    
    # create dictionary to write all paths:
    paths = {}
    
    # find path of current folder (simulation_environment)
    paths['main'] = os.path.abspath(os.path.dirname(sys.argv[0]))
    
    # define paths of subfolders:
    paths['data'] =os.path.join(paths['main'], 'data')
    paths['python'] = os.path.join(paths['main'], 'python')
    paths['aux_files'] = os.path.join(paths['python'], 'aux_files')
    
    paths['radiation_results'] = os.path.join(paths['main'],'radiation_results_' + FolderName['DataNamePV'])
    paths['radiation_wall'] = os.path.join(paths['main'],  'radiation_wall_' + FolderName['DataNamePV'])
    paths['PV'] = os.path.join(paths['main'], 'PV_results')

    paths['save_results_path'] = paths['PV']
    paths['weather_folder']= os.path.join(os.path.dirname(paths['main']), 'WeatherData')
    
    
    # define path of weather file:
    paths['weather_folder']= os.path.join(os.path.dirname(paths['main']), 'WeatherData')
    paths['weather'] = os.path.join(paths['weather_folder'], geoLocation + '.epw')
    
    # add python_path to system path, so that all files are available:
    sys.path.insert(0, paths['aux_files'])
    sys.path.insert(0, paths['python'])
    
    
    from epwreader import epw_reader
    #read epw file of needed destination
    weatherData = epw_reader(paths['weather'])
    
    
    #radiation subfolder is created, there the radiation_results are saved
    if not os.path.isdir(paths['radiation_results']):
            os.makedirs(paths['radiation_results'])
    
    if not os.path.isdir(paths['radiation_wall']):
            os.makedirs(paths['radiation_wall'])
    
    # define path of geographical location:
    paths['geo_location'] = os.path.join(paths['data'], 'geographical_location')
    paths['geo'] = os.path.join(paths['geo_location'], geoLocation)
    
    #define paths of the RC-Model    
    paths['5R1C_ISO_simulator'] = os.path.join(paths['main'], '5R1C_ISO_simulator')
    paths['5R1C_ISO_simulator_data'] = os.path.join(paths['5R1C_ISO_simulator'], 'data')    
    paths['Occupancy'] = os.path.join(paths['5R1C_ISO_simulator_data'], Occupancy) 
    
    from SunAnglesTrackingAndTemperatureFunction import SunAnglesTackingAndTemperature
    # create sun data based on grasshopper file, this is only possible with the ladybug component SunPath
    SunTrackingData = SunAnglesTackingAndTemperature(paths = paths,
                                                     weatherData = weatherData)    
    #execfile(os.path.join(paths['aux_files'], 'SunAngles_Tracking_and_temperature.py'))
    
    # calculate and save lookup table if it does not yet exist:
    paths['data_python'] = os.path.join(paths['data'], 'python')
    paths['electrical_simulation'] = os.path.join(paths['data_python'], 'electrical_simulation') 
   
    
    if not os.path.isfile(os.path.join(paths['electrical_simulation'], 'curr_model_submod_lookup.npy')): 
        if not os.path.isdir(paths['electrical_simulation']):
            os.makedirs(paths['electrical_simulation'])
        execfile(os.path.join(paths['aux_files'], 'create_lookup_table.py'))
    else:
        print 'lookup table not created as it already exists'
    
    
    # load sunTrackingData used for the LadyBug simulation:
    with open(os.path.join(paths['geo'], 'SunTrackingData.json'), 'r') as fp:
        SunTrackingData = json.load(fp)
        fp.close()
    
    return paths, weatherData, SunTrackingData
    
    
def CalculateVariables(SunTrackingData, building_data, XANGLES, YANGLES):
    #Calculate variables
    
    #hour_in_month is dependent on the location, this dict is for ZH
    hours = SunTrackingData['HoursInMonth']
    hour_in_month={}
    
    #adjust shape of hour_in_month dictionary
    for item in range(0,len(hours)):
        hour_in_month[item+1]= hours[item]
    
    
    daysPerMonth = np.array([31,28,31,30,31,30,31,31,30,31,30,31])
    
    from hourRadiation import hourRadiation, hourRadiation_calculated, sumHours
    
    
    hourRadiation = hourRadiation(hour_in_month, daysPerMonth)
    hourRadiation_calculated = hourRadiation_calculated(hour_in_month,daysPerMonth)
    sumHours = sumHours(daysPerMonth)

    
    #Make a list of all angle combinations
    ANGLES= [(x, y) for x in XANGLES for y in YANGLES]
    
    #append to more ANGLES combination option for the angle carpetplot
    ANGLES.append((np.nan,np.nan)) # no sun
    ANGLES.append((-100.,-100.)) # no movement
    
    #create a dicitionary with all angle combinations
    combinationAngles = {}
    
    for i in range(0,len(ANGLES)):
        combinationAngles[i] = ANGLES[i]
    
    
    NumberCombinations = len(XANGLES)*len(YANGLES) #*NoClusters
    
    return ANGLES, hour_in_month, NumberCombinations, combinationAngles, daysPerMonth, hourRadiation, hourRadiation_calculated, sumHours
    

    
def runRadiationCalculation(paths, XANGLES, YANGLES, daysPerMonth, hour_in_month, FolderName, panel_data, NumberCombinations, createPlots, simulationOption):
     
    from RadiationCalculation import CalculateRadiationData     
     
     # Start the simulation   
    now = time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
#    print "simulation start: " + now    
    
            
    
    #Calculate the Radiation on the solar panels and window with ladybug
    BuildingRadiationData_HOD = CalculateRadiationData( XANGLES = XANGLES, 
                                                        YANGLES = YANGLES, 
                                                        paths = paths, 
                                                        daysPerMonth = daysPerMonth, 
                                                        hour_in_month = hour_in_month,
                                                        DataNamePV = FolderName['DataNamePV'],
                                                        DataNameWin = FolderName['DataNameWin'])
        
    
    #if there are no panels vertical and horizontal
    if panel_data['numberHorizontal'] == 0 and panel_data['numberVertical'] == 0:
        PV_electricity_results = {}
        
        PV_electricity_results['Pmpp_sum'] = np.array(NumberCombinations * len(hour_in_month) * [0])
        print "PV_electricity_results is zero"
        
    
    #with the radiation_results the Pv_results are calcualted, make sure you know where the results are saved, otherwise they will just be loaded
    if not os.path.isfile(os.path.join(paths['PV'], 'PV_electricity_results_' + FolderName['DataNamePV'] + '.npy')): 
        if not os.path.isdir(paths['PV']):
            os.makedirs(paths['PV'])
            
        from asf_electricity_production_mauro_3 import asf_electricity_production
        
        print '\nCalculating PV electricity production'     
        
        
        if createPlots:
            PV_electricity_results, PV_detailed_results, fig1, fig2 = \
            asf_electricity_production(
                               createPlots = createPlots, 
                               lb_radiation_path = paths['radiation_results'],
                               panelsize = panel_data['panelSize'], 
                               pvSizeOption = 0,
                               save_results_path = paths['PV'], 
                               lookup_table_path = paths['electrical_simulation'], 
                               geo_path = paths['geo'],
                               flipOrientation= False, 
                               simulationOption = simulationOption,
                               XANGLES = XANGLES, YANGLES= YANGLES, 
                               hour_in_month = hour_in_month, 
                               paths = paths, DataNamePV = FolderName['DataNamePV'])
                               
        else:
            PV_electricity_results, PV_detailed_results = \
            asf_electricity_production(
                               createPlots = createPlots, 
                               lb_radiation_path = paths['radiation_results'],
                               panelsize = panel_data['panelSize'], 
                               pvSizeOption = 0,
                               save_results_path = paths['PV'], 
                               lookup_table_path = paths['electrical_simulation'], 
                               geo_path = paths['geo'],
                               flipOrientation= False, 
                               simulationOption = simulationOption,
                               XANGLES = XANGLES, YANGLES= YANGLES, 
                               hour_in_month = hour_in_month,
                               paths = paths, DataNamePV = FolderName['DataNamePV'])
    
    else: 
        PV_electricity_results = np.load(os.path.join(paths['PV'], 'PV_electricity_results_' + FolderName['DataNamePV'] + '.npy')).item()
        PV_detailed_results = np.load(os.path.join(paths['PV'], 'PV_detailed_results_' + FolderName['DataNamePV'] + '.npy')).item()
        print '\nLadyBug data loaded from Folder:'
        print 'radiation_results_' + FolderName['DataNamePV']  
        
    return PV_electricity_results, PV_detailed_results, BuildingRadiationData_HOD, now
   
   
 
def PrepareRadiationData(hour_in_month, daysPerMonth, BuildingRadiationData_HOD, PV_electricity_results, NumberCombinations):
    
    from hourRadiation import hourRadiation, hourRadiation_calculated, sumHours

    
    
    hourRadiation = hourRadiation(hour_in_month, daysPerMonth)
    hourRadiation_calculated = hourRadiation_calculated(hour_in_month,daysPerMonth)
    sumHours = sumHours(daysPerMonth)
    
              
    #add the radiation data to the specific HOY
    PV={}
    BuildingRadiationData_HOY= {}
    passedHours = 0
    
    for monthi in range(1,13):
        if monthi == 1:
            passedHours = 0
        else:
            passedHours = sumHours[monthi-2]     
        
        for HOD in hour_in_month[monthi]:
            for ii in range(0,daysPerMonth[monthi-1]):             
                DAY = ii*24 + int(HOD)   
                BuildingRadiationData_HOY[passedHours + DAY] = BuildingRadiationData_HOD[monthi][DAY] #W
    
    
    for hour_of_year in range(0,8760):
        PV[hour_of_year]= {}
        PV[hour_of_year]['PV']= []
        
          
    count = 0
    DAY = 0
    
    for monthi in range(1,13):
        if monthi == 1:
            passedHours = 0
        else:
            passedHours = sumHours[monthi-2]
            
        for HOD in hour_in_month[monthi]:
                for jj in range(0,daysPerMonth[monthi-1]):
                    DAY = jj*24 + HOD     
                    PV[passedHours + DAY]['PV'] = PV_electricity_results['Pmpp_sum'][count:count+NumberCombinations] #Watts
                count +=NumberCombinations
                
    for hour_of_year in range(0,8760):
        if hour_of_year not in hourRadiation:
                BuildingRadiationData_HOY[int(hour_of_year)] = np.asarray([0]* NumberCombinations, dtype = np.float64)
                PV[int(hour_of_year)]['PV'] = np.asarray([0]* NumberCombinations, dtype = np.float64)
       
    
    return PV, BuildingRadiationData_HOY


    
def runBuildingSimulation(geoLocation, paths, optimization_Types, building_data, weatherData, hourRadiation, BuildingRadiationData_HOY, PV, NumberCombinations, combinationAngles, BuildingProperties, setBackTemp, daysPerMonth, ANGLES):
    
    from energy_minimization import RC_Model
    from prepareDataMain import prepareAngles, prepareResults
    
    #create dicitionaries to save the results
    hourlyData = {}
    monthlyData = {}
    yearlyData = {}
    ResultsBuildingSimulation = {}
        
    x_angles = {} #optimized x-angles
    y_angles = {} #optimized y-angles
    BestKey_df = {} #optimized keys of the ANGLES dictionary
    
    
            
    #run the RC-Model for the needed optimization Type and save RC-Model results in dictionaries for every optimization type analysed
    for optimizationType in optimization_Types:
            
        hourlyData[optimizationType], ResultsBuildingSimulation[optimizationType] = RC_Model (
                                                                      optimization_type = optimizationType, 
                                                                      paths = paths,
                                                                      building_data = building_data, 
                                                                      weatherData = weatherData, 
                                                                      hourRadiation = hourRadiation, 
                                                                      BuildingRadiationData_HOY = BuildingRadiationData_HOY, 
                                                                      PV = PV, 
                                                                      NumberCombinations = NumberCombinations, 
                                                                      combinationAngles = combinationAngles,
                                                                      BuildingProperties = BuildingProperties,
                                                                      setBackTemp = setBackTemp
                                                                      )
        
        #prepareAngles creates two arrays with x- and y-angles for the respective optimization type and a dataFrame with all the keys stored  
        BestKey_df[optimizationType], x_angles[optimizationType], y_angles[optimizationType] = prepareAngles(
                                                                            Building_Simulation_df = ResultsBuildingSimulation[optimizationType], 
                                                                            daysPerMonth = daysPerMonth,
                                                                            ANGLES = ANGLES)   
        
    """ this has to be adjusted """
    # prepare Building simulation Data into final form, monthly Data [kWh/DaysPerMonth], yearlyData [kWh/year]
    monthlyData['E_total'], yearlyData['E_total'] = prepareResults(Building_Simulation_df = ResultsBuildingSimulation['E_total'],
                                                                        ETOT = 'E_tot', H = 'H', C = 'C', EHCL = 'E_HCL')
    monthlyData['E_total_elec'], yearlyData['E_total_elec'] = prepareResults(Building_Simulation_df = ResultsBuildingSimulation['E_total_elec'],
                                                                        ETOT = 'E_tot_elec', H = 'H_elec', C = 'C_elec', EHCL = 'E_HCL_elec')
        
    return hourlyData, monthlyData, yearlyData, ResultsBuildingSimulation, BestKey_df, x_angles, y_angles
    
    
    

def createAllPlots(monthlyData, roomFloorArea, x_angles, y_angles, hour_in_month, optimization_Types):
    
    from createCarpetPlot import createCarpetPlot, createCarpetPlotXAngles, createCarpetPlotYAngles, createCarpetPlotXAnglesELEC, createCarpetPlotYAnglesELEC
    
    #create the carpet plots detailing the net energy consumption, set only monthlyData['E_total']
    print '\nFigure: total energy demand'    
    
    fig0 = createCarpetPlot (monthlyData = monthlyData['E_total'], roomFloorArea = roomFloorArea)
    
    fig = {'fig0': fig0}
    
    if ('E_total_elec') in optimization_Types:
        
        print 'Figure: total electrical energy demand'
        
        figA = createCarpetPlot (monthlyData = monthlyData['E_total_elec'], roomFloorArea = roomFloorArea)
        fig.update({'figA' : figA})
    
    
    if ('E_total' and 'Heating' and 'Cooling' and 'SolarEnergy' and 'E_HCL' and 'Lighting') in optimization_Types:    
        #create the angles carpet plots for the opimised simulation option, this option needs all simulation types
        fig1 = createCarpetPlotXAngles(x_angles, hour_in_month)
        fig2 = createCarpetPlotYAngles(y_angles, hour_in_month)
        
        fig.update({'fig1' : fig1, 'fig2' : fig2})
    
    if ('E_total_elec' and 'Heating_elec' and 'Cooling_elec' and 'SolarEnergy' and 'E_HCL_elec' and 'Lighting') in optimization_Types:  
        
        #create the angles carpet plots for the opimised simulation option, this option needs all simulation types
        figB = createCarpetPlotXAnglesELEC(x_angles, hour_in_month)
        figC = createCarpetPlotYAnglesELEC(y_angles, hour_in_month)
        
        fig.update({'figB' : figB, 'figC' : figC})
    
    return fig




def SaveResults(now, Save, geoLocation, paths, fig, optimization_Types,  monthlyData, yearlyData, ResultsBuildingSimulation, BuildingProperties, x_angles, y_angles):
    
    monthlyData = pd.DataFrame(monthlyData)
    yearlyData = pd.DataFrame(yearlyData)    
    
    if Save == True: 
        
        # create folder where results will be saved:
        paths['result_folder'] = os.path.join(paths['main'], 'Results') 
        paths['result']= os.path.join(paths['result_folder'], 'Results_' + geoLocation + '_date_' + now)
        
        if not os.path.isdir(paths['result']):
            os.makedirs(paths['result'])    
        
        #create folder to save figures as svg and png:
        paths['pdf'] = os.path.join(paths['result'], 'png')
        
        os.makedirs(paths['pdf'])
        
         
        fig['fig0'].savefig(os.path.join(paths['pdf'], 'figure0' + '.pdf'))
        
        if ('E_total_elec') in optimization_Types:
            fig['figA'].savefig(os.path.join(paths['pdf'], 'figureA' + '.pdf'))        
        
        
        if ('E_total' and 'Heating' and 'Cooling' and 'SolarEnergy' and 'E_HCL' and 'Lighting') in optimization_Types:                           
            #save figures
            fig['fig1'].savefig(os.path.join(paths['pdf'], 'figure1' + '.pdf'))
            fig['fig2'].savefig(os.path.join(paths['pdf'], 'figure2' + '.pdf'))
            
            
        if ('E_total_elec' and 'Heating_elec' and 'Cooling_elec' and 'SolarEnergy' and 'E_HCL_elec' and 'Lighting') in optimization_Types:            
            #save figures
            fig['figB'].savefig(os.path.join(paths['pdf'], 'figureB' + '.pdf'))
            fig['figC'].savefig(os.path.join(paths['pdf'], 'figureC' + '.pdf'))

        for ii in optimization_Types:
            # save results 
            ResultsBuildingSimulation[ii].to_csv(os.path.join(paths['result'], 'Building_Simulation_'+ ii + '.csv'))
        
        x_angles_df = pd.DataFrame(x_angles)
        y_angles_df = pd.DataFrame(y_angles)           
        
        #hourlyData['E_total'].to_csv(os.path.join(paths['result'], 'hourlyData.csv'))
        monthlyData.to_csv(os.path.join(paths['result'], 'monthlyData.csv'))
        yearlyData.to_csv(os.path.join(paths['result'], 'yearlyData.csv'))
        x_angles_df.to_csv(os.path.join(paths['result'], 'X-Angles.csv'))
        y_angles_df.to_csv(os.path.join(paths['result'], 'Y-Angles.csv'))
        
        
        BuildingProperties["heatingSystem"] = str(BuildingProperties["heatingSystem"])
        BuildingProperties["coolingSystem"] = str(BuildingProperties["coolingSystem"])
        
             
        #save building properties
        with open(os.path.join(paths['result'], 'BuildingProperties.json'), 'w') as f:
            f.write(json.dumps(BuildingProperties))
    
        print '\nResults are saved!'    
    
    print "\nSimulation end: " + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
    
    return ResultsBuildingSimulation['E_total'], monthlyData, yearlyData

        
