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

def initializeSimulation(geoLocation, Save, optimization_Types):
    
    # specify the location used for the analysis
    #this name must be the same as a folder in the directory .../ASF_Simulation/Simulation_Environment/data/geographical_location
    # new locations can be added with the grasshopper main script for any .epw weather
    
    
    #set True if you want to save the results
     
    
    #set optimization type: (Angles plots can only be created, if all types are chosen)
    # 'E_total' is needed, minimize the overall energy consumption
    
    optimization_Types = ['E_total'] #
    
    #optimization_Types = ['E_total','Heating']
    #optimization_Types = ['E_total','Cooling']
    #optimization_Types = ['E_total','SolarEnergy']
    #optimization_Types = ['E_total','E_HCL']
    #optimization_Types = ['E_total','Lighting']
    
    return geoLocation, Save, optimization_Types

def initializeASF(XANGLES, YANGLES, NoClusters, ActuationEnergy):

    #Set Solar Panel Angles 
    #Set Number of Clusters, for the moment only = 1 is working

    #Set panel data
    panel_data={"XANGLES": XANGLES ,
    "YANGLES" : YANGLES,
    "NoClusters":NoClusters,
    "numberHorizontal":6,#6,
    "numberVertical":9,#9,
    "panelOffset":400,
    "panelSize":400,
    "panelSpacing":500,
    }
    
    #Save parameters to be imported into grasshopper
    with open('panel.json','w') as f:
        f.write(json.dumps(panel_data))
        
    #Option to integrate the actuation energy consumption, 'yes' = energy consumption is included (not included yet)
    #ActuationEnergy = True # False
    
    return panel_data

def setBuildingParameters(room_width, room_height, room_depth, glazing_percentage_w, glazing_percentage_h):
    
    #Set Building Parameters
    building_data={"room_width":room_width,     
    "room_height":room_height,
    "room_depth":room_depth,
    "glazing_percentage_w": glazing_percentage_w,
    "glazing_percentage_h": glazing_percentage_h
    }
    #Save parameters to be imported into grasshopper
    with open('building.json','w') as f:
        f.write(json.dumps(building_data))
    
    roomFloorArea = building_data['room_width']/1000.0 * building_data['room_depth']/1000.0 #[m^2] floor area
    
    return building_data, roomFloorArea
    
    
def initializeBuildingSimulation(building_data,glass_solar_transmitance,glass_light_transmitance, \
                            lighting_load,lighting_control,Lighting_Utilisation_Factor, Lighting_MaintenanceFactor,U_em,U_w, \
                            ACH_vent, ACH_infl, ventilation_efficiency, c_m_A_f, theta_int_h_set, theta_int_c_set, phi_c_max_A_f, \
                            phi_h_max_A_f, setBackTemp, Occupancy):
    #set building properties for the RC-Model analysis 
    BuildingProperties={
            "Fenst_A": building_data['room_width']/1000.0*building_data['room_height']/1000.0*building_data['glazing_percentage_h']*building_data['glazing_percentage_w'],
            "Room_Depth": building_data['room_depth']/1000.0,
            "Room_Width": building_data['room_width']/1000.0,
            "Room_Height":building_data['room_height']/1000.0,
            "glass_solar_transmitance" : glass_solar_transmitance ,
            "glass_light_transmitance" : glass_light_transmitance ,
            "lighting_load" : lighting_load ,
            "lighting_control" : lighting_control,
            "Lighting_Utilisation_Factor" : Lighting_Utilisation_Factor,
            "Lighting_MaintenanceFactor" : Lighting_MaintenanceFactor,
            "U_em" : U_em, 
            "U_w" : U_w,
            "ACH_vent" : ACH_vent,
            "ACH_infl" :ACH_infl,
            "ventilation_efficiency" : ventilation_efficiency,
            "c_m_A_f" : c_m_A_f, #capcitance of the building dependent on building type: medium = 165'000, heavy = 260'000, light = 110'000, very heavy = 370'000
            "theta_int_h_set" : theta_int_h_set,
            "theta_int_c_set" : theta_int_c_set,
            "phi_c_max_A_f": phi_c_max_A_f, #-np.inf,
            "phi_h_max_A_f":phi_h_max_A_f #np.inf
            }     
                 
    #Temperature in what range the heating can become warmer or colder, if there ar no people in the building
  
    #set the occupancy profil, dependent on the building utilisation type
    # add csv. file to the following folder:...New_SimulationEnvironment\5R1C_ISO_simulator\data, and change variable Occupancy to the filename
       
    #building_stystem = capacitive heating/ cooling  
    
    return BuildingProperties, setBackTemp, Occupancy
    
    
def setPaths(geoLocation, Occupancy):
    
    # create dictionary to write all paths:
    paths = {}
    
    # find path of current folder (simulation_environment)
    paths['main'] = os.path.abspath(os.path.dirname(sys.argv[0]))
    
    # define paths of subfolders:
    paths['data'] =os.path.join(paths['main'], 'data')
    paths['python'] = os.path.join(paths['main'], 'python')
    paths['aux_files'] = os.path.join(paths['python'], 'aux_files')
    paths['radiation_results'] = os.path.join(paths['main'],'radiation_results')
    paths['radiation_wall'] = os.path.join(paths['main'],  'radiation_wall')
    paths['PV'] = os.path.join(paths['main'], 'PV_results')
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
    
    
    # create sun data based on grasshopper file, this is only possible with the ladybug component SunPath
    execfile(os.path.join(paths['aux_files'], 'SunAngles_Tracking_and_temperature.py'))
    
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
    
def runRadiationCalculation(paths, XANGLES, YANGLES, daysPerMonth, hour_in_month, DataName, panel_data, NumberCombinations, createPlots, simulationOption):
     # Start the simulation
    
    now = time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
    print "simulation start: " + now    
    
    from RadiationCalculation import CalculateRadiationData
    
    
    #Calculate the Radiation on the solar panels and window with ladybug
    BuildingRadiationData_HOD = CalculateRadiationData( XANGLES = XANGLES, 
                                                        YANGLES = YANGLES, 
                                                        paths = paths, 
                                                        daysPerMonth = daysPerMonth, 
                                                        hour_in_month = hour_in_month,
                                                        DataName = None)
    
    #option used for simulations, for example if radiation analysis was only done for 
    #4 months ('4months'), not yet working in all cases, set 'timePeriod' to None
    #for regular simulations
    #simulationOption = {'timePeriod' : None}
    #simulationOption = {'timePeriod' : '4months'} #not fully implemented
    #simulationOption = {'timePeriod' : '1h'} #not fully implemented    
    
    #PV production plots
    
    
    PV_electricity_results = {}
    PV_detailed_results = {}
    
    #if there are no panels vertical and horizontal
    if panel_data['numberHorizontal'] == 0 and panel_data['numberVertical'] == 0:
        PV_electricity_results['Pmpp_sum'] = np.array(NumberCombinations * 145 * [0])
        print "PV_electricity_results is zero"
        
    
    #with the radiation_results the Pv_results are calcualted, make sure you know where the results are saved, otherwise they will just be loaded
    if not os.path.isfile(os.path.join(paths['PV'], 'PV_electricity_results.npy')): 
        if not os.path.isdir(paths['PV']):
            os.makedirs(paths['PV'])
            
        from asf_electricity_production_mauro_3 import asf_electricity_production
        print '\ncalculating PV electricity production'     
        
        
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
                               paths = paths, DataName = None)
                               
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
                               paths = paths, DataName = None)
    
    else: 
        PV_electricity_results = np.load(os.path.join(paths['PV'], 'PV_electricity_results.npy')).item()
        PV_detailed_results = np.load(os.path.join(paths['PV'], 'PV_detailed_results.npy')).item()
        print '\nPV_electricity_results loaded from folder'
        
    print "\npreparing data\n"
    
    return PV_electricity_results, PV_detailed_results, BuildingRadiationData_HOD, now
    
def runBuildingSimulation(geoLocation, paths, optimization_Types, building_data, weatherData, hourRadiation, BuildingRadiationData_HOY, PV, NumberCombinations, combinationAngles, BuildingProperties, setBackTemp, daysPerMonth, ANGLES):
    
    from energy_minimization import RC_Model
    from prepareDataMain import prepareAngles, prepareResults
    
    #create dicitionaries to save the results
    hourlyData = {}
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
        
    
        # prepare Building simulation Data into final form, monthly Data [kWh/DaysPerMonth], yearlyData [kWh/year]
        monthlyData, yearlyData = prepareResults(Building_Simulation_df = ResultsBuildingSimulation['E_total'], 
                                                 geoLocation = geoLocation)
        
    return hourlyData, monthlyData, yearlyData, ResultsBuildingSimulation, BestKey_df, x_angles, y_angles

def createAllPlots(monthlyData, roomFloorArea, x_angles, y_angles, hour_in_month, optimization_Types):
    
    from createCarpetPlot import createCarpetPlot, createCarpetPlotXAngles, createCarpetPlotYAngles
    
    #create the carpet plots detailing the net energy consumption, set only monthlyData['E_total']
    fig0 = createCarpetPlot (monthlyData = monthlyData, roomFloorArea = roomFloorArea)
    
    if optimization_Types == ['E_total','Heating','Cooling', 'SolarEnergy', 'E_HCL', 'Lighting']:    
        #create the angles carpet plots for the opimised simulation option, this option needs all simulation types
        fig1 = createCarpetPlotXAngles(x_angles, hour_in_month)
        fig2 = createCarpetPlotYAngles(y_angles, hour_in_month)
    
    return fig0, fig1, fig2

def SaveResults(now, Save, geoLocation, paths, fig0, fig1, fig2, optimization_Types,  monthlyData, yearlyData, ResultsBuildingSimulation, BuildingProperties):
    
    if Save == True: 
        
        # create folder where results will be saved:
        paths['result_folder'] = os.path.join(paths['main'], 'Results') 
        paths['result']= os.path.join(paths['result_folder'], 'Results_' + geoLocation + '_date_' + now)
        
        if not os.path.isdir(paths['result']):
            os.makedirs(paths['result'])    
        
        #create folder to save figures as svg and png:
        paths['pdf'] = os.path.join(paths['result'], 'png')
        
        os.makedirs(paths['pdf'])
        
         
        fig0.savefig(os.path.join(paths['pdf'], 'figure0' + '.pdf'))
        
        if optimization_Types == ['E_total','Heating','Cooling', 'SolarEnergy', 'E_HCL', 'Lighting']:    
                       
            #save figures
            fig1.savefig(os.path.join(paths['pdf'], 'figure1' + '.pdf'))
            fig2.savefig(os.path.join(paths['pdf'], 'figure2' + '.pdf'))
              
                
        monthlyData = pd.DataFrame(monthlyData)
        
        # save results of overall energy demand, in kWh
        ResultsBuildingSimulation['E_total'].to_csv(os.path.join(paths['result'], 'Building_Simulation.csv'))
        #hourlyData['E_total'].to_csv(os.path.join(paths['result'], 'hourlyData.csv'))
        monthlyData.to_csv(os.path.join(paths['result'], 'monthlyData.csv'))
        yearlyData.to_csv(os.path.join(paths['result'], 'yearlyData.csv'))
        
        
        #save building properties
        with open(os.path.join(paths['result'], 'BuildingProperties.json'), 'w') as f:
            f.write(json.dumps(BuildingProperties))
    
        print '\nResults are saved!'    
    
    print "\nSimulation end: " + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
    
    return ResultsBuildingSimulation['E_total'], monthlyData, yearlyData
  
