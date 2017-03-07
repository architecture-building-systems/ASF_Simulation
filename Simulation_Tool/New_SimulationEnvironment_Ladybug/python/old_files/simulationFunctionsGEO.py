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

def initializeSimulation(SimulationData, building_data, BuildingProperties):
           
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
    

    #set building properties for the RC-Model analysis 
    BuildingProperties.update({
            "Fenst_A": building_data['room_width']/1000.0*building_data['room_height']/1000.0*building_data['glazing_percentage_h']*building_data['glazing_percentage_w'],
            "Room_Depth": building_data['room_depth']/1000.0,
            "Room_Width": building_data['room_width']/1000.0,
            "Room_Height":building_data['room_height']/1000.0})                
     
    now = time.time()
    
    return BuildingProperties,FolderName, now
    
    
def setPaths(geoLocation, Occupancy, FolderName):
    
    # create dictionary to write all paths:
    paths = {}
    
    # find path of current folder (simulation_environment)
    paths['main'] = os.path.abspath(os.path.dirname(sys.argv[0]))
    
    # define paths of subfolders:
    paths['data'] =os.path.join(paths['main'], 'data')
    paths['python'] = os.path.join(paths['main'], 'python')
    paths['aux_files'] = os.path.join(paths['python'], 'aux_files')
    
#    paths['radiation_results'] = os.path.join(paths['main'],'radiation_results_' + FolderName['DataNamePV'])
#    paths['radiation_wall'] = os.path.join(paths['main'],  'radiation_wall_' + FolderName['DataNamePV'])
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
#    if not os.path.isdir(paths['radiation_results']):
#            os.makedirs(paths['radiation_results'])
#    
#    if not os.path.isdir(paths['radiation_wall']):
#            os.makedirs(paths['radiation_wall'])
    
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
    
    from hourRadiation import hourRadiation
    hourRadiation = hourRadiation(hour_in_month, daysPerMonth)
    

    #Make a list of all angle combinations
    ANGLES= [(x, y) for x in XANGLES for y in YANGLES]
    
    #append to more ANGLES combination option for the angle carpetplot
    ANGLES.append((np.nan,np.nan)) # no sun
    #ANGLES.append((-100.,-100.)) # no movement
    
    #create a dicitionary with all angle combinations
    combinationAngles = {}
    
    for i in range(0,len(ANGLES)):
        combinationAngles[i] = ANGLES[i]
    
    
    NumberCombinations = len(XANGLES)*len(YANGLES) #*NoClusters
    
    return ANGLES, hour_in_month, NumberCombinations, combinationAngles, daysPerMonth, hourRadiation
    


    
def runBuildingSimulation(geoLocation, paths, optimization_Types, building_data, weatherData, hourRadiation, \
                            NumberCombinations, combinationAngles, BuildingProperties, setBackTemp, daysPerMonth, ANGLES,\
                            start, end, Temp_start, SimulationPeriod):
                                
#    PV = np.load(r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RadiationModel\PV_geo2.npy').item()
#    BuildingRadiationData_HOY = np.load(r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RadiationModel\Window_geo2.npy').item()
#    
#    PV = np.load(r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RadiationModel\PV_geo2no_powerloss.npy').item()
#    BuildingRadiationData_HOY = np.load(r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RadiationModel\Window_geo2no_powerloss.npy').item()
    
   
    
    PV = np.load(r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RadiationModel\PV_Final.npy').item()
    BuildingRadiationData_HOY = np.load(r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RadiationModel\Window_Final.npy').item()
    
    print PV
    
    # add python_path to system path, so that all files are available:
    sys.path.insert(0, paths['5R1C_ISO_simulator'])     
    
    from energy_minimization_hourly import RC_Model
    from prepareDataMain_hourly import prepareAngles
    from read_occupancy import read_occupancy
    
    #create dicitionaries to save the results
    hourlyData = {}
    ResultsBuildingSimulation = {}
    UncomfortableH = {}    
    
    x_angles = {} #optimized x-angles
    y_angles = {} #optimized y-angles
    BestKey = {} #optimized keys of the ANGLES dictionary
    TotalHourlyData = {}
    
    #set parameters
    human_heat_emission=0.12 #[kWh] heat emitted by a human body per hour. Source: HVAC Engineers Handbook, F. Porges
    roomFloorArea = building_data['room_width']/1000.0 * building_data['room_depth']/1000.0 #[m^2] floor area
     
    #people/m2/h, W    
    occupancy, Q_human = read_occupancy(myfilename = paths['Occupancy'], human_heat_emission = human_heat_emission, floor_area = roomFloorArea)      
            
    #run the RC-Model for the needed optimization Type and save RC-Model results in dictionaries for every optimization type analysed
    for optimizationType in optimization_Types:
            
        hourlyData[optimizationType], ResultsBuildingSimulation[optimizationType], UncomfortableH[optimizationType], TotalHOY = RC_Model (
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
                                                                      setBackTemp = setBackTemp,
                                                                      occupancy = occupancy,
                                                                      Q_human = Q_human, 
                                                                      start = start, end = end, Temp_start = Temp_start,
                                                                      SimulationPeriod = SimulationPeriod
                                                                      )
                                                                      
           
        
        
        #prepareAngles creates two arrays with x- and y-angles for the respective optimization type and a dataFrame with all the keys stored  
        BestKey[optimizationType], x_angles[optimizationType], y_angles[optimizationType],  TotalHourlyData[optimizationType] = prepareAngles(
                                                                            Building_Simulation_df = ResultsBuildingSimulation[optimizationType], 
                                                                            ANGLES = ANGLES,
                                                                            start = start, end = end,
                                                                            TotalHOY = TotalHOY)   
    
        
    return hourlyData, ResultsBuildingSimulation, BestKey, x_angles, y_angles, UncomfortableH, TotalHOY, TotalHourlyData
    
    



def SaveResults(hourlyData,now, Save, geoLocation, paths, optimization_Types,  ResultsBuildingSimulation, BuildingProperties, x_angles, y_angles, SimulationData, start, end, TotalHOY, TotalHourlyData):
    
    from hourlyPlotFunction import PlotHour 
#    from Function3dPlot import create3Dplot, create3Dplot2       
    
    fig = {}
      
#    fig = plt.figure(figsize=(4, 20))
    
    #count = 1
    for ii in optimization_Types:
        
#        plt.subplot(6,1,count)
        fig[ii] = PlotHour(E = ResultsBuildingSimulation[ii]['E_tot'], PV = ResultsBuildingSimulation[ii]['PV'], L = ResultsBuildingSimulation[ii]['L'], 
                           H = ResultsBuildingSimulation[ii]['H'], C = ResultsBuildingSimulation[ii]['C'], x_angle = x_angles[ii], y_angle = y_angles[ii], 
                           start = start, end = end, title = ii, TotalHOY = TotalHOY)
        #count += 1
   
   
    RBS_ELEC = {}
    
    #rearrange dataframes and split them
    for ii in optimization_Types:    
    
        ResultsBuildingSimulation[ii]  = ResultsBuildingSimulation[ii].T   
        
        ELEC_df = pd.DataFrame(ResultsBuildingSimulation[ii], index = ['PV', 'L','C_elec', 'H_elec', 'E_HCL_elec', 'E_tot_elec']  ,columns= TotalHOY)
    
        RBS_ELEC[ii] = ELEC_df.T
        
        ResultsBuildingSimulation[ii] = ResultsBuildingSimulation[ii].T 
        del ResultsBuildingSimulation[ii]['C_elec']
        del ResultsBuildingSimulation[ii]['H_elec']
        del ResultsBuildingSimulation[ii]['E_tot_elec']
        del ResultsBuildingSimulation[ii]['E_HCL_elec']
    
    
    if Save == True: 
        
        # create folder where results will be saved:
        paths['result_folder'] = os.path.join(paths['main'], 'Results') 
        paths['result']= os.path.join(paths['result_folder'], 'Results_' + geoLocation + '_date_' + str(now) + '_name_' + SimulationData['DataName'])
        
        
        
        if not os.path.isdir(paths['result']):
            os.makedirs(paths['result'])    
        
       
        for ii in optimization_Types:
            # save results 
            #ResultsBuildingSimulation[ii] = ResultsBuildingSimulation[ii].T
            ResultsBuildingSimulation[ii].to_csv(os.path.join(paths['result'], 'BuildingSimulation_'+ ii + '.csv'))
            RBS_ELEC[ii].to_csv(os.path.join(paths['result'], 'BuildingSimulationELEC_'+ ii + '.csv'))
            
            fig[ii].savefig(os.path.join(paths['result'], 'figure_' + ii + '.pdf'))
            fig[ii].savefig(os.path.join(paths['result'], 'figure_' + ii +  '.png'))
            

            np.save(os.path.join(os.path.join(paths['result'], 'BuildingSimulation_'+ ii + '.npy')), ResultsBuildingSimulation[ii])
            
#       np.save(os.path.join(os.path.join(paths['result'], 'hourlyData_' + ii + '.npy')), hourlyData[ii].T)
        hourlyData = pd.DataFrame(hourlyData['E_total'].T)
        hourlyData.to_csv(os.path.join(paths['result'], 'hourlyData_E.csv'))
            
            
        
        
        TotalHourlyData = pd.DataFrame(TotalHourlyData)
        TotalHourlyData.to_csv(os.path.join(paths['result'], 'HourlyTotalData.csv'))
         
        
        BuildingProperties["heatingSystem"] = str(BuildingProperties["heatingSystem"])
        BuildingProperties["coolingSystem"] = str(BuildingProperties["coolingSystem"])
        
        BuildingProperties["start"] = start
        BuildingProperties["end"] = end
        
             
        #save building properties
        with open(os.path.join(paths['result'], 'BuildingProperties.json'), 'w') as f:
            f.write(json.dumps(BuildingProperties))
        
    
        print '\nResults are saved!'
    
    
    print "\nSimulation end: " + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
    
    return ResultsBuildingSimulation, RBS_ELEC

     
