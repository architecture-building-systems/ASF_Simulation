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

sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), '5R1C_ISO_simulator'))    
    
from buildingPhysics import Building #Importing Building Class
from supplySystem import *  
from emissionSystem import *

class ASF_Simulation(object):
    #initilize ASF_simulation class

    def __init__(self,
            SimulationData= {
            'optimizationTypes' : ['E_total'], 'DataFolderName' : 'ZH13_49comb_WinterSunnyDay', 'FileName' : 'ZH13_49comb_WinterSunnyDay','geoLocation' : 'Zuerich_Kloten_2013', 'EPWfile': 'Zuerich_Kloten_2013.epw','Save' : True, 'ShowFig': False, 'timePeriod': None},  
            SimulationPeriod = {
            'FromMonth': 1, 'ToMonth': 1, 'FromDay': 8, 'ToDay': 8, 'FromHour': 5, 'ToHour': 20},
            PanelData = 
            {"XANGLES": [0, 15, 30, 45, 60, 75, 90],"YANGLES" : [-45, -30,-15,0, 15, 30, 45],"NoClusters":1,"numberHorizontal":6,"numberVertical":9,"panelOffset":400,"panelSize":400,"panelSpacing":500, "panelGridSize" : 25},
            BuildingData = 
            {"room_width": 4900, "room_height":3100, "room_depth":7000, "glazing_percentage_w": 0.92,"glazing_percentage_h": 0.97, "WindowGridSize": 200, "BuildingOrientation" : 0},
            BuildingProperties = 
            {"glass_solar_transmittance" : 0.691,"glass_light_transmittance" : 0.744,"lighting_load" : 11.74,"lighting_control" : 300,"Lighting_Utilisation_Factor" :  0.6,\
            "Lighting_Maintenance_Factor" : 0.9,"U_em" : 0.2,"U_w" : 1.1,"ACH_vent" : 1.5,"ACH_infl" :0.5,"ventilation_efficiency" : 0.6 ,"c_m_A_f" : 165 * 10**3,"theta_int_h_set" : 22,\
            "theta_int_c_set" : 26,"phi_c_max_A_f": -np.inf,"phi_h_max_A_f":np.inf,"heatingSupplySystem" : DirectHeater,"coolingSupplySystem" : DirectCooler, "heatingEmissionSystem" : AirConditioning,"coolingEmissionSystem" : AirConditioning,},
            SimulationOptions= 
            {'setBackTempH' : 4.,'setBackTempC' : 4., 'Occupancy' : 'Occupancy_COM.csv','ActuationEnergy' : False, 'Temp_start' : 20, 'human_heat_emission' : 0.12}):
                     
                            
            #define varibales of object
		self.SimulationData=SimulationData
		self.PanelData=PanelData
		self.BuildingData=BuildingData
		self.BuildingProperties=BuildingProperties
		self.SimulationOptions=SimulationOptions
		self.SimulationPeriod = SimulationPeriod
		
		self.XANGLES=self.PanelData['XANGLES']
		self.YANGLES = self.PanelData['YANGLES']		
		self.createPlots=False
		self.geoLocation = SimulationData['geoLocation']
		self.now = time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
		self.optimization_Types = self.SimulationData['optimizationTypes']
  

    

		#Set folder name and chosen epw-file
		self.FolderName={
		"DataFolderName": SimulationData['DataFolderName'],
		"EPW" : SimulationData['EPWfile']  
		}
		
		#Save parameters to be imported into grasshopper
		with open('FolderName.json','w') as f:
			f.write(json.dumps(self.FolderName))    
				


    
    def initializeASF(self):
      
        #Save parameters to be imported into grasshopper
        with open('panel.json','w') as f:
            f.write(json.dumps(self.PanelData))
            
    
    def setBuildingParameters(self):
        
        #Save parameters to be imported into grasshopper
        with open('building.json','w') as f:
            f.write(json.dumps(self.BuildingData))
        
        self.roomFloorArea = self.BuildingData['room_width']/1000.0 * self.BuildingData['room_depth']/1000.0 #[m^2] floor area
        
 
        
    def initializeBuildingSimulation(self):
        #set building properties for the RC-Model analysis 
        self.BuildingProperties.update({
                "Fenst_A": self.BuildingData['room_width']/1000.0*self.BuildingData['room_height']/1000.0*self.BuildingData['glazing_percentage_h']*self.BuildingData['glazing_percentage_w'],
                "Room_Depth": self.BuildingData['room_depth']/1000.0,
                "Room_Width": self.BuildingData['room_width']/1000.0,
                "Room_Height":self.BuildingData['room_height']/1000.0})                
            
        
    def setPaths(self):
        

        #set the occupancy file, which will be used for the evaluation
        Occupancy = self.SimulationOptions['Occupancy']

        
        # create dictionary to write all paths:
        self.paths = {}
        
        # find path of current folder (simulation_environment)
        self.paths['main'] = os.path.abspath(os.path.dirname(sys.argv[0]))
        
        # define paths of subfolders:
        self.paths['data'] =os.path.join(self.paths['main'], 'data')
        self.paths['python'] = os.path.join(self.paths['main'], 'python')
        self.paths['RadiationData'] = os.path.join(self.paths['main'], 'RadiationData')
        
        # add python_path to system path, so that all files are available:
        sys.path.insert(0, self.paths['python'])
        
        from create_lookup_table import lookUpTableFunction
        from epwreader import epw_reader
        from SunAnglesTrackingAndTemperatureFunction import SunAnglesTackingAndTemperature
        
        
        self.paths['radiation_results'] = os.path.join(self.paths['RadiationData'],'radiation_results_' + self.SimulationData['DataFolderName'])
        self.paths['radiation_wall'] = os.path.join(self.paths['RadiationData'],  'radiation_wall_' + self.SimulationData['DataFolderName'])
        self.paths['PV'] = os.path.join(self.paths['main'], 'PV_results')
        self.paths['save_results_path'] = self.paths['PV']
        self.paths['weather_folder']= os.path.join(os.path.dirname(self.paths['main']), 'WeatherData')
        
        
        # define path of weather file:
        self.paths['weather_folder']= os.path.join(os.path.dirname(self.paths['main']), 'WeatherData')
        self.paths['weather'] = os.path.join(self.paths['weather_folder'], self.geoLocation + '.epw')
        print self.geoLocation        
        
        
        #read epw file of needed destination
        self.weatherData = epw_reader(self.paths['weather'])
        
        if not os.path.isdir(self.paths['PV']):
		os.makedirs(self.paths['PV']) 
        
        
        if not os.path.isdir(self.paths['RadiationData']):
            os.makedirs(self.paths['RadiationData'])
        #radiation subfolder is created, there the radiation_results are saved
        if not os.path.isdir(self.paths['radiation_results']):
            os.makedirs(self.paths['radiation_results'])
        
        if not os.path.isdir(self.paths['radiation_wall']):
            os.makedirs(self.paths['radiation_wall'])
        
        # define path of geographical location:
        self. paths['geo_location'] = os.path.join(self.paths['data'], 'geographical_location')
        self.paths['geo'] = os.path.join(self.paths['geo_location'], self.geoLocation)
        
        #define paths of the RC-Model    
        self.paths['5R1C_ISO_simulator'] = os.path.join(self.paths['main'], '5R1C_ISO_simulator')
        self.paths['5R1C_ISO_simulator_data'] = os.path.join(self.paths['5R1C_ISO_simulator'], 'data')    
        self.paths['Occupancy'] = os.path.join(self.paths['5R1C_ISO_simulator_data'], Occupancy) 
        
        
        # create sun data based on grasshopper file, this is only possible with the ladybug component SunPath
        self.SunTrackingData = SunAnglesTackingAndTemperature(paths = self.paths,
                                                              weatherData = self.weatherData)  
        
        # calculate and save lookup table if it does not yet exist:
        self.paths['data_python'] = os.path.join(self.paths['data'], 'python')
        self.paths['electrical_simulation'] = os.path.join(self.paths['data_python'], 'electrical_simulation') 
       
        
        if not os.path.isfile(os.path.join(self.paths['electrical_simulation'], 'curr_model_submod_lookup.npy')): 
            if not os.path.isdir(self.paths['electrical_simulation']):
                os.makedirs(self.paths['electrical_simulation'])
            lookUpTableFunction(self.paths)
        else:
            print 'lookup table not created as it already exists'
        
        
        # load sunTrackingData used for the LadyBug simulation:
        with open(os.path.join(self.paths['geo'], 'SunTrackingData.json'), 'r') as fp:
            self.SunTrackingData = json.load(fp)
            fp.close()
        
        
    
        
  
	
        
        
    def CalculateVariables(self):
        
        from calculateHOY import calcHOY
        # Calculate start and end hour of year dependent on simulaiton period
        self.start =calcHOY(month =  self.SimulationPeriod['FromMonth'], day =  self.SimulationPeriod['FromDay'], hour =  self.SimulationPeriod['FromHour'])
        self.end = calcHOY(month =  self.SimulationPeriod['ToMonth'], day =  self.SimulationPeriod['ToDay'], hour =  self.SimulationPeriod['ToHour'])  
        self.TotalHOY = range(self.start, self.end + 1)

        from hourRadiation import hourRadiation, hourRadiation_calculated, sumHours
        #Calculate variables
        
        #hour_in_month is dependent on the location, this dict is for ZH
        hours = self.SunTrackingData['HoursInMonth']
        self.hour_in_month={}
        
        #adjust shape of hour_in_month dictionary
        for item in range(0,len(hours)):
            self.hour_in_month[item+1]= hours[item]
        
        
        self.daysPerMonth = np.array([31,28,31,30,31,30,31,31,30,31,30,31])
        self.hourRadiation = hourRadiation(self.hour_in_month, self.daysPerMonth)
        self.hourRadiation_calculated = hourRadiation_calculated(self.hour_in_month, self.daysPerMonth)
        self.sumHours = sumHours(self.daysPerMonth)
    
        
        #Make a list of all angle combinations
        self.ANGLES= [(x, y) for x in self.XANGLES for y in self.YANGLES]
        
        #append to more ANGLES combination option for the angle carpetplot
        self.ANGLES.append((np.nan,np.nan)) # no sun
        #ANGLES.append((-100.,-100.)) # no movement
        
        #create a dicitionary with all angle combinations
        self.combinationAngles = {}
        
        for i in range(0,len(self.ANGLES)):
            self.combinationAngles[i] = self.ANGLES[i]
        
        
        self.NumberCombinations = len(self.XANGLES)*len(self.YANGLES) #*NoClusters
        
        
    
        
    def runRadiationCalculation(self):
         # Start the simulation
        
    
        from asf_electricity_production_hourly import asf_electricity_production
        from RadiationCalculation_hourly import CalculateRadiationData
        #Calculate the Radiation on the solar panels and window with ladybug
        self.HourlyRadiation = CalculateRadiationData(SimulationPeriode = self.SimulationPeriod,
                                                        XANGLES = self.XANGLES, 
                                                        YANGLES = self.YANGLES, 
                                                        paths = self.paths, 
                                                        FolderName = self.SimulationData)
        
        
        
        
       
        
        #if there are no panels vertical and horizontal
        if self.PanelData['numberHorizontal'] == 0 and self.PanelData['numberVertical'] == 0:
            self.PV_electricity_results = {}
            self.PV_electricity_results['Pmpp_sum'] = np.array(self.NumberCombinations * (self.end - self.start) * [0])
            print "PV_electricity_results is zero"
            
        else:
            #with the radiation_results the Pv_results are calcualted, make sure you know where the results are saved, otherwise they will just be loaded
            if not os.path.isfile(os.path.join(self.paths['PV'], 'HourlyPV_electricity_results_' + self.SimulationData['FileName'] + '.npy')): 
                if not os.path.isdir(self.paths['PV']):
                    os.makedirs(self.paths['PV'])
                    
                            
                print '\nCalculating PV electricity production'     
                
                
                if self.createPlots:
                    self.PV_electricity_results, self.PV_detailed_results, fig1, fig2 = \
                    asf_electricity_production(
                                       createPlots = self.createPlots, 
                                       lb_radiation_path = self.paths['radiation_results'],
                                       panelsize = self.PanelData['panelSize'], 
                                       pvSizeOption = 0,
                                       save_results_path = self.paths['PV'], 
                                       lookup_table_path = self.paths['electrical_simulation'], 
                                       geo_path = self.paths['geo'],
                                       flipOrientation= False, 
                                       XANGLES = self.XANGLES, 
                                       YANGLES= self.YANGLES, 
                                       hour_in_month = self.hour_in_month, 
                                       paths = self.paths, 
                                       DataNamePV = self.SimulationData['FileName'],
                                       SimulationPeriode = self.SimulationPeriod, 
                                       weatherData = self.weatherData)
                                       
                else:
                    self.PV_electricity_results, self.PV_detailed_results = \
                    asf_electricity_production(
                                       createPlots = self.createPlots, 
                                       lb_radiation_path = self.paths['radiation_results'],
                                       panelsize = self.PanelData['panelSize'], 
                                       pvSizeOption = 0,
                                       save_results_path = self.paths['PV'], 
                                       lookup_table_path = self.paths['electrical_simulation'], 
                                       geo_path = self.paths['geo'],
                                       flipOrientation= False, 
                                       XANGLES = self.XANGLES, 
                                       YANGLES= self.YANGLES, 
                                       hour_in_month = self.hour_in_month,
                                       paths = self.paths, 
                                       DataNamePV = self.SimulationData['FileName'],
                                       SimulationPeriode = self.SimulationPeriod, 
                                       weatherData = self.weatherData)
            
            else: 
                self.PV_electricity_results = np.load(os.path.join(self.paths['PV'], 'HourlyPV_electricity_results_' + self.SimulationData['FileName'] + '.npy')).item()
                self.PV_detailed_results = np.load(os.path.join(self.paths['PV'], 'HourlyPV_detailed_results_' + self.SimulationData['FileName'] + '.npy')).item()
                print '\nLadyBug data loaded from Folder:'
                print 'radiation_results_' + self.FolderName['DataFolderName']  
                print 'File: ', self.SimulationData['FileName'] 

      
     
    def PrepareRadiationData(self):
        
        from calculateHOY import calcHOY
        
               
        #add the radiation data to the specific HOY
        self.PV={}
        self.BuildingRadiationHOY= {}
        passedHours = 0
        count = 0
        
        for monthi in range(self.SimulationPeriod['FromMonth'], self.SimulationPeriod['ToMonth'] + 1):
           for day in range(self.SimulationPeriod['FromDay'], self.SimulationPeriod['ToDay'] + 1):
                for hour in range(self.SimulationPeriod['FromHour'], self.SimulationPeriod['ToHour']+1):        
                    
                    #HOY = start + passedHours
                    HOY = calcHOY(month= monthi, day = day, hour= hour)
                    self.BuildingRadiationHOY[HOY] = self.HourlyRadiation[monthi][day][hour] #W
                    
                    #print 'HOY: ' + str(HOY) + ' of ' + str(end)
    
                    self.PV[HOY] = self.PV_electricity_results['Pmpp_sum'][count:count+ self.NumberCombinations] #Watts
                    count += self.NumberCombinations               
                   
                    passedHours += 1
        
        
    
    
        
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
        
                
         
        #people/m2/h, W    
        occupancy, Q_human = read_occupancy(myfilename = self.paths['Occupancy'], human_heat_emission = self.SimulationOptions['human_heat_emission'], floor_area = self.roomFloorArea)      
                
        #run the RC-Model for the needed optimization Type and save RC-Model results in dictionaries for every optimization type analysed
        for optimizationType in self.optimization_Types:
                
            self.hourlyData[optimizationType], self.ResultsBuildingSimulation[optimizationType], self.UncomfortableH[optimizationType] = RC_Model (
                                                                          optimization_type = optimizationType, 
                                                                          paths = self.paths,
                                                                          building_data = self.BuildingData, 
                                                                          weatherData = self.weatherData, 
                                                                          BuildingRadiationData_HOY = self.BuildingRadiationHOY, 
                                                                          PV = self.PV, 
                                                                          combinationAngles = self.combinationAngles,
                                                                          BuildingProperties = self.BuildingProperties,
                                                                          SimulationOptions = self.SimulationOptions,
                                                                          occupancy = occupancy,
                                                                          Q_human = Q_human, 
                                                                          start = self.start, 
                                                                          end = self.end 
                                                                          )
                                                                          
               
            
            
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
            
            
    
            self.BuildingProperties["heatingSupplySystem"] = str(self.BuildingProperties["heatingSupplySystem"])
            self.BuildingProperties["coolingSupplySystem"] = str(self.BuildingProperties["coolingSupplySystem"])
            self.BuildingProperties["heatingEmissionSystem"] = str(self.BuildingProperties["heatingEmissionSystem"])
            self.BuildingProperties["coolingEmissionSystem"] = str(self.BuildingProperties["coolingEmissionSystem"])
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
		

        self.initializeASF()
        self.setBuildingParameters()		
        self.initializeBuildingSimulation()
        self.setPaths()				
        self.CalculateVariables()
        self.runRadiationCalculation()		  		 
        self.PrepareRadiationData()													   
        self.runBuildingSimulation()

        if self.SimulationData['ShowFig'] == True and self.SimulationData['Save'] != True:   
        	self.createPlotsFunction()
        
        if self.SimulationData['Save']== True and self.SimulationData['Save']== True:
        	self.createPlotsFunction()
        	self.SaveResults()
         
