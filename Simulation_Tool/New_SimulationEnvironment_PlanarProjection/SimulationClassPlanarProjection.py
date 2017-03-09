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
from buildingSystem import *  

class ASF_Simulation(object):
    #initilize ASF_simulation class

    def __init__(self,
            SimulationPeriod = {
            'FromMonth': 7, 'ToMonth': 7, 'FromDay': 6, 'ToDay': 6, 'FromHour': 5, 'ToHour': 20},
            PlanarProjectionSettings = {
            'ShadingCase' : ['1','2','3'], 'reflectance' : 0, 'DistWindow' : 300, 'shadingPV' : True },
            SimulationData= {
            'optimizationTypes' : ['E_total'], 'FileName' : 'ZH13_49comb_SummerSunnyDay_PP','geoLocation' : 'Zuerich_Kloten_2013', 'Save' : True, 'ShowFig': False, 'timePeriod': None},  
            PanelData = 
            {"XANGLES": [0, 15, 30, 45, 60, 75, 90],"YANGLES" : [-45, -30,-15,0, 15, 30, 45],"NoClusters":1,"numberHorizontal":6,"numberVertical":9,"panelSize":400,"panelSpacing":500},
            BuildingData = 
            {"room_width": 4900, "room_height":3100, "room_depth":7000, "glazing_percentage_w": 0.92,"glazing_percentage_h": 0.97,  "BuildingOrientation" : 0},
            BuildingProperties = 
            {"glass_solar_transmitance" : 0.691,"glass_light_transmitance" : 0.744,"lighting_load" : 11.74,"lighting_control" : 300,"Lighting_Utilisation_Factor" :  0.6,\
            "Lighting_MaintenanceFactor" : 0.9,"U_em" : 0.2,"U_w" : 1.1,"ACH_vent" : 1.5,"ACH_infl" :0.5,"ventilation_efficiency" : 0.6 ,"c_m_A_f" : 165 * 10**3,"theta_int_h_set" : 22,\
            "theta_int_c_set" : 26,"phi_c_max_A_f": -np.inf,"phi_h_max_A_f":np.inf,"heatingSystem" : DirectHeater,"coolingSystem" : DirectCooler, "heatingEfficiency" : 1,"coolingEfficiency" :1,
            'COP_H': 3, 'COP_C':3},
            SimulationOptions= 
            {'setBackTempH' : 4.,'setBackTempC' : 4., 'Occupancy' : 'Occupancy_COM.csv','ActuationEnergy' : False, 'Temp_start' : 20, 'human_heat_emission' : 0.12}):
                     
                            
            #define varibales of object
		self.SimulationData=SimulationData
		self.PanelData=PanelData
		self.BuildingData=BuildingData
		self.BuildingProperties=BuildingProperties
		self.SimulationOptions=SimulationOptions
		self.SimulationPeriod = SimulationPeriod
		self.PlanarProjectionSettings = PlanarProjectionSettings
		
		self.XANGLES=self.PanelData['XANGLES']
		self.YANGLES = self.PanelData['YANGLES']		
		self.createPlots=False
		self.geoLocation = SimulationData['geoLocation']
		self.now = time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
		self.optimization_Types = self.SimulationData['optimizationTypes']

		
            #set building properties for the RC-Model analysis 
		self.BuildingProperties.update({
                    "Fenst_A": self.BuildingData['room_width']/1000.0*self.BuildingData['room_height']/1000.0*self.BuildingData['glazing_percentage_h']*self.BuildingData['glazing_percentage_w'],
                    "Room_Depth": self.BuildingData['room_depth']/1000.0,
                    "Room_Width": self.BuildingData['room_width']/1000.0,
                    "Room_Height":self.BuildingData['room_height']/1000.0})                
            
        
    def setPaths(self):
        

        

        
        # create dictionary to write all paths:
        self.paths = {}
        
        # find path of current folder (simulation_environment)
        self.paths['main'] = os.path.abspath(os.path.dirname(sys.argv[0]))
        
        # define paths of subfolders:
        self.paths['data'] =os.path.join(self.paths['main'], 'data')
        self.paths['python'] = os.path.join(self.paths['main'], 'python')
        self.paths['RadiationData'] = os.path.join(self.paths['main'], 'RadiationData')
        
        
        
        
               
        
        self.paths['RadModel'] = os.path.join(self.paths['main'], 'RadiationModel')        
        self.paths['SunAngles'] = os.path.join(self.paths['data'], 'SunAngles.csv')
        
        
        # add python_path to system path, so that all files are available:
        sys.path.insert(0, self.paths['python'])
        sys.path.insert(0, self.paths['RadModel'])
        
        self.SunAngles = pd.read_csv(self.paths['SunAngles'])        
        
        
        self.paths['PV'] = os.path.join(self.paths['main'], 'PV_results')
        self.paths['save_results_path'] = self.paths['PV']
        self.paths['weather_folder']= os.path.join(os.path.dirname(self.paths['main']), 'WeatherData')
        
        from epwreader import epw_reader
        # define path of weather file:
        self.paths['weather_folder']= os.path.join(os.path.dirname(self.paths['main']), 'WeatherData')
        self.paths['weather'] = os.path.join(self.paths['weather_folder'], self.geoLocation + '.epw')
        print self.geoLocation        
        
        
        #read epw file of needed destination
        self.weatherData = epw_reader(self.paths['weather'])
        
        
        if not os.path.isdir(self.paths['RadiationData']):
            os.makedirs(self.paths['RadiationData'])
        
        
        # define path of geographical location:
        self. paths['geo_location'] = os.path.join(self.paths['data'], 'geographical_location')
        self.paths['geo'] = os.path.join(self.paths['geo_location'], self.geoLocation)
        
        #define paths of the RC-Model    
        self.paths['5R1C_ISO_simulator'] = os.path.join(self.paths['main'], '5R1C_ISO_simulator')
        self.paths['5R1C_ISO_simulator_data'] = os.path.join(self.paths['5R1C_ISO_simulator'], 'data')
        
        #set the occupancy file, which will be used for the evaluation
        Occupancy = self.SimulationOptions['Occupancy']
        self.paths['Occupancy'] = os.path.join(self.paths['5R1C_ISO_simulator_data'], Occupancy) 
        
        
        
    
        
	
        
        
    def CalculateVariables(self):
        
        from calculateHOY import calcHOY

        # Calculate start and end hour of year dependent on simulaiton period
        self.start =calcHOY(month =  self.SimulationPeriod['FromMonth'], day =  self.SimulationPeriod['FromDay'], hour =  self.SimulationPeriod['FromHour'])
        self.end = calcHOY(month =  self.SimulationPeriod['ToMonth'], day =  self.SimulationPeriod['ToDay'], hour =  self.SimulationPeriod['ToHour'])  
        self.TotalHOY = range(self.start, self.end + 1)
    
        #Make a list of all angle combinations
        self.ANGLES= [(x, y) for x in self.XANGLES for y in self.YANGLES]
        
        #append to more ANGLES combination option for the angle carpetplot
        self.ANGLES.append((np.nan,np.nan)) # no sun
        
        #create a dicitionary with all angle combinations
        self.combinationAngles = {}
        
        for i in range(0,len(self.ANGLES)):
            self.combinationAngles[i] = self.ANGLES[i]
        
        
        self.NumberCombinations = len(self.XANGLES)*len(self.YANGLES) #*NoClusters
        

        
    def runRadiationCalculation(self):
         # Start the simulation
        
        
    
        from PlanarProjection import PlanarProjectionFunction, pvProductionPlanarProjection
        
        if not os.path.isfile(os.path.join(self.paths['RadiationData'], 'ResultsPlanarProjection_' + self.SimulationData['FileName'] + '.npy')):
            self.ResultsPlanarProjection = PlanarProjectionFunction (start = self.start, 
                                                                   end = self.end, 
                                                                   PanelData = self.PanelData,
                                                                   BuildingData = self.BuildingData,          
                                                                   weatherData = self.weatherData, 
                                                                   SunAngles = self.SunAngles,
                                                                   PlanarProjectionSettings = self.PlanarProjectionSettings)

            np.save(os.path.join(self.paths['RadiationData'], 'ResultsPlanarProjection_' + self.SimulationData['FileName'] + '.npy'), self.ResultsPlanarProjection)
            print '\nResultsPlanarProjection_' + self.SimulationData['FileName'] + ' saved!'
        else:
            self.ResultsPlanarProjection = np.load(os.path.join(self.paths['RadiationData'], 'ResultsPlanarProjection_' + self.SimulationData['FileName'] + '.npy')).item()
            print '\nResultsPlanarProjection_' + self.SimulationData['FileName'] + ' loaded from folder!'
            
       
       
        
        #if there are no panels vertical and horizontal
        if self.PanelData['numberHorizontal'] == 0 and self.PanelData['numberVertical'] == 0:
            self.PV_electricity_results = {}
            self.PV_electricity_results['Pmpp_sum'] = np.array(self.NumberCombinations * (self.end - self.start) * [0])
            print "PV_electricity_results is zero"
            
        else:
            #with the radiation_results the Pv_results are calcualted, make sure you know where the results are saved, otherwise they will just be loaded
            if not os.path.isfile(os.path.join(self.paths['PV'], 'PlanarProjection_PV_results_' + self.SimulationData['FileName'] + '.npy')): 
                if not os.path.isdir(self.paths['PV']):
                    os.makedirs(self.paths['PV'])
                    
                            
                print '\nCalculating PV electricity production'     
                self.PV_results, self.WindowRadiation_results, self.shading_loss = pvProductionPlanarProjection(start = self.start, 
                                                                                  end = self.end, 
                                                                                  PanelData = self.PanelData, 
                                                                                  ResultsPlanarProjection = self.ResultsPlanarProjection , 
                                                                                  PlanarProjectionSettings = self.PlanarProjectionSettings, 
                                                                                  paths = self.paths) 
                                                                                  
                np.save(os.path.join(self.paths['save_results_path'], 'PlanarProjection_PV_results_'  + self.SimulationData['FileName'] + '.npy'), self.PV_results)    
                np.save(os.path.join(self.paths['save_results_path'], 'PlanarProjection_WindowRadiation_'  + self.SimulationData['FileName'] + '.npy'), self.WindowRadiation_results)
                print '\nPlanarProjection_PV_results_'  + self.SimulationData['FileName'] + ' saved!'
                print 'PlanarProjection_WindowRadiation_' + self.SimulationData['FileName'] + ' saved!'
                            
            else: 
                self.PV_results = np.load(os.path.join(self.paths['PV'], 'PlanarProjection_PV_results_' + self.SimulationData['FileName'] + '.npy')).item()
                self.WindowRadiation_results = np.load(os.path.join(self.paths['PV'], 'PlanarProjection_WindowRadiation_' + self.SimulationData['FileName'] + '.npy')).item()                
                print 'PlanarProjection_PV_results_' +  self.SimulationData['FileName'] + ' loaded!'
                print 'PlanarProjection_WindowRadiation_' +  self.SimulationData['FileName'] + ' loaded!' 

      
     
    
        
    def runBuildingSimulation(self):
        
        # add python_path to system path, so that all files are available:
        sys.path.insert(0, self.paths['5R1C_ISO_simulator'])     
        
        from energy_minimization_hourly import RC_Model
        from prepareDataMain_hourly import prepareAngles
        from read_occupancy import read_occupancy
        
        #create dicitionaries to save the results
        self.hourlyData = {}
        self.ResultsBuildingSimulation = {}
        self.UncomfortableH = {}    
        
        self.x_angles = {} #optimized x-angles
        self.y_angles = {} #optimized y-angles
        self.BestKey = {} #optimized keys of the ANGLES dictionary
        self.TotalHourlyData = {}
        self.TotalHourlyDataELEC = {}
        
        human_heat_emission= self.SimulationOptions['human_heat_emission']
        
        self.roomFloorArea = self.BuildingData['room_width']/1000.0 * self.BuildingData['room_depth']/1000.0 #[m^2] floor area

        #people/m2/h, W    
        occupancy, Q_human = read_occupancy(myfilename = self.paths['Occupancy'], human_heat_emission = human_heat_emission, floor_area = self.roomFloorArea)      
                
        #run the RC-Model for the needed optimization Type and save RC-Model results in dictionaries for every optimization type analysed
        for optimizationType in self.optimization_Types:
                
            self.hourlyData[optimizationType], self.ResultsBuildingSimulation[optimizationType], self.UncomfortableH[optimizationType] = RC_Model (
                                                                          optimization_type = optimizationType, 
                                                                          paths = self.paths,
                                                                          building_data = self.BuildingData, 
                                                                          weatherData = self.weatherData, 
                                                                          BuildingRadiationData_HOY = self.WindowRadiation_results, 
                                                                          PV = self.PV_results,  
                                                                          combinationAngles = self.combinationAngles,
                                                                          BuildingProperties = self.BuildingProperties,
                                                                          SimulationOptions = self.SimulationOptions,
                                                                          occupancy = occupancy,
                                                                          Q_human = Q_human, 
                                                                          start = self.start, 
                                                                          end = self.end) 
                                                  
               
            
            
            #prepareAngles creates two arrays with x- and y-angles for the respective optimization type and a dataFrame with all the keys stored  
            self.BestKey[optimizationType], self.x_angles[optimizationType], self.y_angles[optimizationType],  self.TotalHourlyData[optimizationType], self.TotalHourlyDataELEC[optimizationType] = prepareAngles(
                                                                                Building_Simulation_df = self.ResultsBuildingSimulation[optimizationType], 
                                                                                ANGLES = self.ANGLES,
                                                                                start = self.start, 
                                                                                end = self.end,
                                                                                TotalHOY = self.TotalHOY)   
        
            
        self.hourlyData = pd.DataFrame(self.hourlyData['E_total'].T)
        self.TotalHourlyData = pd.DataFrame(self.TotalHourlyData)
        self.RBS_ELEC = {}
        
        #rearrange dataframes and split them
        for ii in self.optimization_Types:    
        
            self.ResultsBuildingSimulation[ii]  = self.ResultsBuildingSimulation[ii].T   
            
            ELEC_df = pd.DataFrame(self.ResultsBuildingSimulation[ii], index = ['PV', 'L','C_elec', 'H_elec', 'E_HCL_elec', 'E_tot_elec']  ,columns= self.TotalHOY)
        
            self.RBS_ELEC[ii] = ELEC_df.T
            
            self.ResultsBuildingSimulation[ii] = self.ResultsBuildingSimulation[ii].T 
            del self.ResultsBuildingSimulation[ii]['C_elec']
            del self.ResultsBuildingSimulation[ii]['H_elec']
            del self.ResultsBuildingSimulation[ii]['E_tot_elec']
            del self.ResultsBuildingSimulation[ii]['E_HCL_elec']
    
        print "\nSimulation end: " + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
        
    def createPlotsFunction(self):
        
        from hourlyPlotFunction import PlotHour 
                
        self.fig = {}
          
        for ii in self.optimization_Types:
            
            
            self.fig[ii] = PlotHour(E = self.ResultsBuildingSimulation[ii]['E_tot'], PV = self.ResultsBuildingSimulation[ii]['PV'], L = self.ResultsBuildingSimulation[ii]['L'], 
                           H = self.ResultsBuildingSimulation[ii]['H'], C = self.ResultsBuildingSimulation[ii]['C'], x_angle = self.x_angles[ii], y_angle = self.y_angles[ii], 
                            start = self.start, end = self.end, title = ii, TotalHOY = self.TotalHOY)
        
       
        
    def SaveResults(self): 
            
            # create folder where results will be saved:
            self.paths['result_folder'] = os.path.join(self.paths['main'], 'Results') 
            self.paths['result']= os.path.join(self.paths['result_folder'], 'Results_' + self.geoLocation + '_date_' + self.now + '_name_' + self.SimulationData['FileName'])
            
            
            if not os.path.isdir(self.paths['result']):
                os.makedirs(self.paths['result'])    
            
            for ii in self.optimization_Types:
                # save results 
                
                self.ResultsBuildingSimulation[ii].to_csv(os.path.join(self.paths['result'], 'BuildingSimulation_'+ ii + '.csv'))
                self.RBS_ELEC[ii].to_csv(os.path.join(self.paths['result'], 'BuildingSimulationELEC_'+ ii + '.csv'))
                self.fig[ii].savefig(os.path.join(self.paths['result'], 'figure_' + ii + '.pdf'))

                
   
            
            self.hourlyData.to_csv(os.path.join(self.paths['result'], 'hourlyData_E.csv'))            
            self.TotalHourlyData.to_csv(os.path.join(self.paths['result'], 'HourlyTotalData.csv'))
            
            
    
            self.BuildingProperties["heatingSystem"] = str(self.BuildingProperties["heatingSystem"])
            self.BuildingProperties["coolingSystem"] = str(self.BuildingProperties["coolingSystem"])
            self.BuildingProperties["start"] = self.start
            self.BuildingProperties["end"] = self.end
            self.BuildingProperties["T_start"] = self.SimulationOptions['Temp_start'] 
            self.BuildingProperties["SetBack_H"] = self.SimulationOptions['setBackTempH']
            self.BuildingProperties["SetBack_C"] = self.SimulationOptions['setBackTempC']
            
                 
            #save building properties
            with open(os.path.join(self.paths['result'], 'BuildingProperties.json'), 'w') as f:
                f.write(json.dumps(self.BuildingProperties))
            
        
            print '\nResults are saved!'
        
            
        
    def SolveASF(self):
        #main method which calls all sub-methods
		

        
        self.setPaths()				
        self.CalculateVariables()
        self.runRadiationCalculation()		  		 
        												   
        self.runBuildingSimulation()

        if self.SimulationData['ShowFig'] == True and self.SimulationData['Save'] != True:   
        	self.createPlotsFunction()
        
        if self.SimulationData['Save']== True and self.SimulationData['Save']== True:
        	self.createPlotsFunction()
        	self.SaveResults()
         
