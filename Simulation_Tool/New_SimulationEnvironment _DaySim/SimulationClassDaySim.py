# -*- coding: utf-8 -*-
"""
Created on Tue Nov 08 11:42:45 2016

@author: PJ
@credits: Mauro
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
            SimulationData = 
            {'optimizationTypes' : ['E_total'],'DataFolderName' : 'ZH13_49comb', 'FileName' : 'ZH13_49comb', 'Save' : True, 'ShowFig': False, 'Temp_start' : 20,'start':0 , 'end': 0, 'ProjectName' : 'Mat02', 'SubFolder': '2ASF'},
            PanelData = 
            {"XANGLES": [0, 15, 30, 45, 60, 75, 90],"YANGLES" : [-45, -30,-15,0, 15, 30, 45]},
            Material = 
            {'ASF' : 0.2, 'Window': 0.2},
            BuildingProperties = 
            {"glass_solar_transmitance" : 0.691,"glass_light_transmitance" : 0.744,"lighting_load" : 11.74,"lighting_control" : 300,"Lighting_Utilisation_Factor" :  0.6,\
            "Lighting_MaintenanceFactor" : 0.9,"U_em" : 0.2,"U_w" : 1.1,"ACH_vent" : 1.5,"ACH_infl" :0.5,"ventilation_efficiency" : 0.6 ,"c_m_A_f" : 165 * 10**3,"theta_int_h_set" : 22,\
            "theta_int_c_set" : 26,"phi_c_max_A_f": -np.inf,"phi_h_max_A_f":np.inf,"heatingSystem" : DirectHeater,"coolingSystem" : DirectCooler, "heatingEfficiency" : 1,"coolingEfficiency" :1,
            'COP_H': 3, 'COP_C':3},
            SimulationOptions= 
            {'setBackTempH' : 4.,'setBackTempC' : 4., 'Occupancy' : 'Occupancy_COM.csv','ActuationEnergy' : False, 'human_heat_emission' : 0.12,'Temp_start' : 20}):
            

            BuildingData = {
            "room_width": 4900, 
            "room_height":3100, 
            "room_depth":7000, 
            "glazing_percentage_w": 0.92,
            "glazing_percentage_h": 0.97, 
            "WindowGridSize": 200,
            "BuildingOrientation" : 0}  #building orientation of 0 corresponds to south facing, 90 is east facing, -90 is west facing

                
            #define varibales of object
            self.SimulationData=SimulationData
            self.PanelData=PanelData
            self.BuildingData=BuildingData
            self.BuildingProperties=BuildingProperties
            self.SimulationOptions=SimulationOptions
            self.Material = Material
  
            self.PanelData.update({		  
            "NoClusters":1,
            "numberHorizontal":6,
            "numberVertical":9,
            "panelOffset":400,
            "panelSize":400,
            "panelSpacing":500,
            "PanelGridSize": 25})  
            
            self.SimulationData.update({
            'geoLocation' : 'Zuerich_Kloten_2013',
            'EPWfile': 'Zuerich_Kloten_2013.epw'})
            

        
            self.start = SimulationData['start']
            self.end = SimulationData['end']
            self.XANGLES=self.PanelData['XANGLES']
            self.YANGLES = self.PanelData['YANGLES']		
            self.createPlots=False
            self.geoLocation = SimulationData['geoLocation']
            self.now = time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
            self.optimization_Types = self.SimulationData['optimizationTypes']            
            self.fig = {}
            
		#Set folder name and chosen epw-file
            self.FolderName={
		"DataFolderName": SimulationData['DataFolderName'],
		"EPW" : SimulationData['EPWfile']}
		
		
	def setPaths(self): 
             
           #set the occupancy file, which will be used for the evaluation
		Occupancy = self.SimulationOptions['Occupancy']

		# create dictionary to write all paths:
		self.paths = {}
		
		# find path of current folder (simulation_environment)
		self.paths['main'] = os.path.abspath(os.path.dirname(sys.argv[0]))
		
		# define self.paths of subfolders:
		self.paths['data'] =os.path.join(self.paths['main'], 'data')
		self.paths['python'] = os.path.join(self.paths['main'], 'python')
		self.paths['DaySim'] = os.path.join(self.paths['main'], 'DaySimData')  
		
		#folder where radiaton results are going to be stored
		self.paths['PV'] = os.path.join(self.paths['main'], 'PV_results')
		self.paths['save_results_path'] = self.paths['PV']
		self.paths['saveDaySim'] = os.path.join(self.paths['DaySim'], self.SimulationData['ProjectName'])

		self.paths['weather_folder']= os.path.join(os.path.dirname(self.paths['main']), 'WeatherData')
		
		
		self.project_folder = os.path.join(os.path.dirname(self.paths['main']),'DaySimFolder')
		self.project_folder = os.path.join(self.project_folder,self.SimulationData['ProjectName'])
		print 'Project Folder', self.project_folder
  
		
  
		self.path_script = os.path.join(self.paths['main'], 'RadiationModel')
  
		if not os.path.isdir(self.paths['DaySim']):
			os.makedirs(self.paths['DaySim'])
   
		if not os.path.isdir(self.paths['saveDaySim']):
			os.makedirs(self.paths['saveDaySim'])
            
            
		# define path of weather file:
		self.paths['weather_folder']= os.path.join(os.path.dirname(self.paths['main']), 'WeatherData')
		print self.geoLocation
		self.paths['weather'] = os.path.join(self.paths['weather_folder'], self.geoLocation + '.epw')
		
		# add python_path to system path, so that all files are available:
		sys.path.insert(0, self.paths['python'])
		sys.path.insert(0, self.path_script)
		
		
		from epwreader import epw_reader
		from SunAnglesTrackingAndTemperatureFunction import SunAnglesTackingAndTemperature # used?
		from create_lookup_table import lookUpTableFunction
  
		#read epw file of needed destination
		self.weatherData = epw_reader(self.paths['weather'])
		self.radiation = self.weatherData[['year', 'month', 'day', 'hour','dirnorrad_Whm2', 'difhorrad_Whm2','glohorrad_Whm2','totskycvr_tenths']]
		
		self.TotalHour = []  
		for hour in range(self.start, self.end):
			self.TotalHour.append(self.radiation['hour'][hour])
				
		# define path of geographical location:
		self.paths['geo_location'] = os.path.join(self.paths['data'], 'geographical_location')
		self.paths['geo'] = os.path.join(self.paths['geo_location'], self.geoLocation)
		
		#define self.paths of the RC-Model    
		self.paths['5R1C_ISO_simulator'] = os.path.join(self.paths['main'], '5R1C_ISO_simulator')
		self.paths['5R1C_ISO_simulator_data'] = os.path.join(self.paths['5R1C_ISO_simulator'], 'data')    
		self.paths['Occupancy'] = os.path.join(self.paths['5R1C_ISO_simulator_data'], Occupancy) 
		
		
		# create sun data based on grasshopper file, this is only possible with the ladybug component SunPath
		self.SunTrackingData = SunAnglesTackingAndTemperature(paths = self.paths,
                                                                weatherData = self.weatherData)    
  
		# calculate and save lookup table if it does not yet exist:
		self.paths['data_python'] = os.path.join(self.paths['data'], 'python')
		self.paths['electrical_simulation'] = os.path.join(self.paths['data_python'], 'electrical_simulation') 
	   
		#check if look up table is already created
		if not os.path.isfile(os.path.join(self.paths['electrical_simulation'], 'curr_model_submod_lookup.npy')): 
			if not os.path.isdir(self.paths['electrical_simulation']):
				os.makedirs(self.paths['electrical_simulation'])
			lookUpTableFunction(self.paths)
		else:
			print 'lookup table not created as it already exists'
		
		
		# load self.sunTrackingData used for the LadyBug simulation:
		with open(os.path.join(self.paths['geo'], 'SunTrackingData.json'), 'r') as fp:
			self.SunTrackingData = json.load(fp)
			fp.close()
		
		
		
	def CalculateVariables(self):
		#Calculate variables
		
            
            #hour_in_month is dependent on the location, this dict is for ZH
		hours = self.SunTrackingData['HoursInMonth']
		self.hour_in_month={}
		
		#adjust shape of self.hour_in_month dictionary
		for item in range(0,len(hours)):
			self.hour_in_month[item+1]= hours[item]
   
		self.daysPerMonth = np.array([31,28,31,30,31,30,31,31,30,31,30,31])
			
		#Make a list of all angle combinations
		self.ANGLES= [(x, y) for x in self.XANGLES for y in self.YANGLES]
		
		#append ANGLES combination option, for the case, the ASF is not moving and there is no sunlight
		self.ANGLES.append((0.1111,0.1111)) # no sun
	   
		#create a dicitionary with all angle combinations
		self.combinationAngles = {}
		
		for i in range(0,len(self.ANGLES)):
			self.combinationAngles[i] = self.ANGLES[i]
		
		
		self.NumberCombinations = len(self.XANGLES)*len(self.YANGLES) #*NoClusters
		
		self.roomFloorArea = self.BuildingData['room_width']/1000.0 * self.BuildingData['room_depth']/1000.0 #[m^2] floor area
  
		self.BuildingProperties.update({
				"Fenst_A": self.BuildingData['room_width']/1000.0*self.BuildingData['room_height']/1000.0*self.BuildingData['glazing_percentage_h']*self.BuildingData['glazing_percentage_w'],
				"Room_Depth": self.BuildingData['room_depth']/1000.0,
				"Room_Width": self.BuildingData['room_width']/1000.0,
				"Room_Height":self.BuildingData['room_height']/1000.0})              

		
	def runRadiationCalculation(self):
		 
     
         from asf_electricity_production_daysim import asf_electricity_production
         from DaySimData import ShapeData

                     
         for x_angle in self.XANGLES:
             for y_angle in self.YANGLES:
                    
                
                project_name = self.SimulationData['SubFolder'] + '_' + str(x_angle) + '_' + str(y_angle)
                
                print project_name
                #check if file is there, if not create and save it
                
                if not os.path.isfile(os.path.join(self.paths['saveDaySim'], project_name) + '_' + str(self.start) + '_' + str(self.end-1) + '_' + str(self.Material['ASF']) + '.npy'):     
                    #reshape data after radiaiton calculation
                    ShapeData(project_folder = self.project_folder, project_name = project_name, path_save = self.paths['saveDaySim'], \
                                start = self.start, end = self.end, x_angle = x_angle, y_angle = y_angle, MatDict = self.Material)
                else:
                    print 'File already Saved'
	
	
	   #if there are no panels vertical and horizontal
         if self.PanelData['numberHorizontal'] == 0 and self.PanelData['numberVertical'] == 0:
			self.PV_electricity_results = {}
			
			self.PV_electricity_results['Pmpp_sum'] = np.array(self.NumberCombinations * len(self.end-self.start) * [0])
			print "PV_electricity_results is zero"
			
		
	   #with the radiation_results the Pv_results are calcualted, make sure you know where the results are saved, otherwise they will just be loaded
         else:
    		if not os.path.isfile(os.path.join(self.paths['PV'], 'HourlyPV_electricity_results_' + self.SimulationData['FileName'] + '.npy')): 
    			if not os.path.isdir(self.paths['PV']):
    				os.makedirs(self.paths['PV'])
    			print '\nCalculating PV electricity production'     
    			
    			
    			if self.createPlots:
    				self.PV_electricity_results, self.PV_detailed_results, fig1, fig2 = \
    				asf_electricity_production(
    								   createPlots = self.createPlots, 
								   panelsize = self.PanelData['panelSize'], 
    								   pvSizeOption = 0,
    								   save_results_path = self.paths['PV'], 
    								   lookup_table_path = self.paths['electrical_simulation'], 
    								   geo_path = self.paths['geo'],
    								   flipOrientation= False, 
								   XANGLES = self.XANGLES, YANGLES= self.YANGLES, 
								   paths = self.paths, DataNamePV = self.SimulationData['FileName'],
								   weatherData = self.weatherData,
								   start = self.start, end = self.end,
								   SimulationData = self.SimulationData,
								   MatDict = self.Material)
    								   
    			else:
                       #option the show plots of PV-production calculation
    				self.PV_electricity_results, self.PV_detailed_results = \
    				asf_electricity_production(
    								   createPlots = self.createPlots, 
    								   panelsize = self.PanelData['panelSize'], 
    								   pvSizeOption = 0,
    								   save_results_path = self.paths['PV'], 
    								   lookup_table_path = self.paths['electrical_simulation'], 
    								   geo_path = self.paths['geo'],
    								   flipOrientation= False, 
    								   XANGLES = self.XANGLES, YANGLES= self.YANGLES, 
    								   paths = self.paths, DataNamePV = self.SimulationData['FileName'],
								   weatherData = self.weatherData,
    								   start = self.start, end = self.end,
								   SimulationData = self.SimulationData,
								   MatDict = self.Material)
    		
    		else: 
                  #if PV-results are available, they will be loaded from folder
    			self.PV_electricity_results = np.load(os.path.join(self.paths['PV'], 'HourlyPV_electricity_results_' + self.SimulationData['FileName'] + '.npy')).item()
    			self.PV_detailed_results = np.load(os.path.join(self.paths['PV'], 'HourlyPV_detailed_results_' + self.SimulationData['FileName'] + '.npy')).item()
    			print '\nRadiation data loaded from Folder!'
    			
   
	   
	 
	def PrepareRadiationData(self):
            #rearrange radiation data into the correct form, so it can be used for the RC-model calculation
     
            print '\n'          
            #add the radiation data to the specific HOY
            self.PV={}
            self.BuildingRadiationHOY= {}
            
            count = 0
            hour = 0
            WindowData = {}
            for x_angle in self.XANGLES:
                for y_angle in self.YANGLES:        
                    fileName = 'Window_' + str(x_angle) + '_' + str(y_angle) + '_' + str(self.start) + '_' + str(self.end-1) + '_' + str(self.Material['Window'])
                    path = os.path.join(self.paths['saveDaySim'], fileName + '.npy')
                    dataWindow = np.load(path)
                    WindowData[str(x_angle) + str(y_angle)] = np.asarray(dataWindow)
            
            for HOY in range(self.start, self.end):  
        
                self.BuildingRadiationHOY[HOY] = np.array([])
                
                for x_angle in self.XANGLES:
                    for y_angle in self.YANGLES:
                        self.BuildingRadiationHOY[HOY] = np.append(self.BuildingRadiationHOY[HOY], WindowData[str(x_angle) + str(y_angle)][hour]) 
                hour += 1
                
            if self.start == 0 and self.end == 8760:
                
                #initilize dictionary
                for hour_of_year in range(0,8760):
                    self.PV[hour_of_year]= []
            	  
                count = 0
                passedHours = 0
                 #check if no panels are selected, if so, than PV-Production is zero
                for monthi in range(12):
                    for HOD in range(24):
                        for jj in range(0,self.daysPerMonth[monthi]):
                               timeHour = passedHours + jj*24 + HOD     
                               self.PV[timeHour]= self.PV_electricity_results['Pmpp_sum'][count:count+self.NumberCombinations] #Watts
         
                        count +=self.NumberCombinations
                    passedHours += self.daysPerMonth[monthi] * 24
       
            else:
                for HOY in range(self.start, self.end):   
                    self.PV[HOY] = []
                    self.PV[HOY] = self.PV_electricity_results['Pmpp_sum'][count:count+self.NumberCombinations] #Watts
                    count += self.NumberCombinations               

     
		
	def runBuildingSimulation(self):
           #method which calls the RC-Model and runs the building energy simulation
           
            # add python_path to system path, so that all files are available:
            sys.path.insert(0, self.paths['5R1C_ISO_simulator'])
            self.setBackTempH = self.SimulationOptions['setBackTempH']
            self.setBackTempC = self.SimulationOptions['setBackTempC']     
            		
            from energy_minimization_daysim import RC_Model
            
            from read_occupancy import read_occupancy
            		
            #create dicitionaries to save the results
            self.hourlyData = {}
            self.monthlyData = {}
            self.yearlyData = {}
            self.ResultsBuildingSimulation = {} #total energy building simulation results
            
            
            		
            		
            #set parameters
            human_heat_emission= self.SimulationOptions['human_heat_emission']
            roomFloorArea = self.BuildingData['room_width']/1000.0 * self.BuildingData['room_depth']/1000.0 #[m^2] floor area
            		 
            				
            #people/m2/h, W    
            self.occupancy, self.Q_human = read_occupancy(myfilename = self.paths['Occupancy'], human_heat_emission = human_heat_emission, floor_area = roomFloorArea)    
            		
            				
            #run the RC-Model for the needed optimization Type and save RC-Model results in dictionaries for every optimization type analysed
            for optimizationType in self.optimization_Types:
				
			self.hourlyData[optimizationType], self.ResultsBuildingSimulation[optimizationType], \
                 self.TotalHOY = RC_Model (
                                                                         optimization_type = optimizationType, 
                                                                         paths = self.paths,
                                                                         building_data = self.BuildingData,
                                                                         SimulationOptions = self.SimulationOptions,
                                                                         weatherData = self.weatherData, 
                                                                         BuildingRadiationData_HOY = self.BuildingRadiationHOY, 
                                                                         PV = self.PV, 
                                                                         combinationAngles = self.combinationAngles,
                                                                         BuildingProperties = self.BuildingProperties,
                                                                         occupancy = self.occupancy,
                                                                         Q_human = self.Q_human,
                                                                         start = self.start, 
                                                                         end = self.end) 
                                                                         
                                                                         
        def PrepareYearlyResults(self):

            from prepareDataMain import prepareAngles, prepareResults, prepareResultsELEC                                                                 
            
            self.x_angles = {} #optimized x-angles
            self.y_angles = {} #optimized y-angles
            self.BestKey = {} #optimized keys of the ANGLES dictionary
            
            for optimizationType in self.optimization_Types:    
                                             
			#prepareAngles creates two arrays with x- and y-angles for the respective optimization type and a dataFrame with all the keys stored  
			self.BestKey[optimizationType], self.x_angles[optimizationType], self.y_angles[optimizationType] = prepareAngles(
																				Building_Simulation_df = self.ResultsBuildingSimulation[optimizationType], 
																				daysPerMonth = self.daysPerMonth,
																				ANGLES = self.ANGLES)   
                  #calculate the monthlyData dependet on which opimization is chosen
			if optimizationType == 'E_total' or optimizationType =='Heating' or optimizationType =='Cooling' or optimizationType =='E_HCL' or optimizationType =='SolarEnergy' or optimizationType =='Lighting':
			
                      # prepare Building simulation Data into final form, monthly Data [kWh/DaysPerMonth], self.yearlyData [kWh/year]
				self.monthlyData[optimizationType], self.yearlyData[optimizationType] = prepareResults(Building_Simulation_df = self.ResultsBuildingSimulation[optimizationType])
				#print self.yearlyData[optimizationType]
			
			if optimizationType == 'E_total_elec' or optimizationType =='Heating_elec' or optimizationType =='Cooling_elec'  or optimizationType =='E_HCL_elec':                                                           
				self.monthlyData[optimizationType], self.yearlyData[optimizationType] = prepareResultsELEC(Building_Simulation_df = self.ResultsBuildingSimulation[optimizationType])
    
        def PrepareHourlyResults(self):
            
            from prepareDataMain_hourlyDaySim import prepareAngles
    
            self.x_angles = {} #optimized x-angles
            self.y_angles = {} #optimized y-angles
            self.BestKey = {} #optimized keys of the ANGLES dictionary
            self.HourlyTotalData = {}
    
            #run the RC-Model for the needed optimization Type and save RC-Model results in dictionaries for every optimization type analysed
            for optimizationType in self.optimization_Types:
           
                #prepareAngles creates two arrays with x- and y-angles for the respective optimization type and a dataFrame with all the keys stored  
                self.BestKey[optimizationType], self.x_angles[optimizationType], self.y_angles[optimizationType], self.HourlyTotalData[optimizationType] = prepareAngles(
                                                                            Building_Simulation_df = self.ResultsBuildingSimulation[optimizationType], 
                                                                            ANGLES = self.ANGLES,
                                                                            start = self.start, 
                                                                            end = self.end,
                                                                            TotalHOY = self.TotalHOY)   
			

	def createAllPlots(self):
            #create energy- and angle- carpet plots
		
		from createCarpetPlot import createCarpetPlot, createCarpetPlotXAngles, createCarpetPlotYAngles
		
		
            # carpet plot for total energy values
		if ('E_total') in self.optimization_Types:    
			#create the carpet plots detailing the net energy consumption, set only monthlyData['E_total']
			print '\nFigure: total energy demand'    
			
			fig0 = createCarpetPlot (monthlyData = self.monthlyData['E_total'], roomFloorArea = self.roomFloorArea,  H = 'H', C = 'C', E = 'E', E_HCL = 'E_HCL')
			
			self.fig.update({'fig0': fig0})
		# carpet plots for electricity demand
		if ('E_total_elec') in self.optimization_Types:
			
			print 'Figure: total electrical energy demand'
			
			figA = createCarpetPlot (monthlyData = self.monthlyData['E_total_elec'], roomFloorArea = self.roomFloorArea,  H = 'H_elec', C = 'C_elec', E = 'E_elec', E_HCL = 'E_HCL_elec')
			self.fig.update({'figA' : figA})
		
		# angle-carpet plots
		if ('E_total' and 'Heating' and 'Cooling' and 'E_HCL') in self.optimization_Types: 
			if ('SolarEnergy' and 'Lighting') in self.optimization_Types:
				#create the angles carpet plots for the opimised simulation option, this option needs all simulation types
				fig1 = createCarpetPlotXAngles(self.x_angles, self.hour_in_month, H = 'Heating', C = 'Cooling', E = 'E_total', E_HCL = 'E_HCL')
				fig2 = createCarpetPlotYAngles(self.y_angles, self.hour_in_month, H = 'Heating', C = 'Cooling', E = 'E_total', E_HCL = 'E_HCL')
				
				self.fig.update({'fig1' : fig1, 'fig2' : fig2})
		
		if ('E_total_elec' and 'Heating_elec' and 'Cooling_elec'  and 'E_HCL_elec' ) in self.optimization_Types:
			if ('SolarEnergy' and 'Lighting') in self.optimization_Types:
			
				#create the angles carpet plots for the opimised simulation option, this option needs all simulation types
				figB = createCarpetPlotXAngles(self.x_angles, self.hour_in_month, H = 'Heating_elec', C = 'Cooling_elec', E = 'E_total_elec', E_HCL = 'E_HCL_elec')
				figC = createCarpetPlotYAngles(self.y_angles, self.hour_in_month, H = 'Heating_elec', C = 'Cooling_elec', E = 'E_total_elec', E_HCL = 'E_HCL_elec')
				
				self.fig.update({'figB' : figB, 'figC' : figC})
		
		return self.fig
  
  
	def createHourlyPlots(self):
    
            from hourlyPlotFunction import PlotHour 

            for ii in self.optimization_Types:
                
                figProxy = PlotHour(E = self.ResultsBuildingSimulation[ii]['E_tot'], PV = self.ResultsBuildingSimulation[ii]['PV'], L = self.ResultsBuildingSimulation[ii]['L'], 
                               H = self.ResultsBuildingSimulation[ii]['H'], C = self.ResultsBuildingSimulation[ii]['C'], x_angle = self.x_angles[ii], y_angle = self.y_angles[ii], 
                                start = self.start, end = self.end, title = ii, TotalHOY = self.TotalHour)
                self.fig.update({ii : figProxy})
            
            
           
           

	def SaveResults(self):
           #method which saves the data and plots 
              
          if self.start == 0 and self.end == 8760:
                    
                    self.monthlyData = pd.DataFrame(self.monthlyData)
                    self.yearlyData = pd.DataFrame(self.yearlyData)

                    
          else:
                    self.HourlyTotalData = pd.DataFrame(self.HourlyTotalData)
                    
          
          
		
          if self.SimulationData['Save']: 
			
			# create folder where results will be saved:
                self.paths['result_folder'] = os.path.join(self.paths['main'], 'Results') 
                self.paths['result']= os.path.join(self.paths['result_folder'], 'Results_' + self.SimulationData['FileName'] + '_date_' + self.now)
        			
                if not os.path.isdir(self.paths['result']):
    				os.makedirs(self.paths['result'])    
        			
        		#create folder to save figures as svg and png:
                self.paths['pdf'] = os.path.join(self.paths['result'], 'Figures')
                os.makedirs(self.paths['pdf'])
                
                if self.start == 0 and self.end == 8760:
			
                    self.fig['fig0'].savefig(os.path.join(self.paths['pdf'], 'figure0.pdf'))
                    self.fig['fig0'].savefig(os.path.join(self.paths['pdf'], 'figure0.png'))
    			
                    if ('E_total_elec') in self.optimization_Types:
                        self.fig['figA'].savefig(os.path.join(self.paths['pdf'], 'figureA.pdf'))
                        self.fig['figA'].savefig(os.path.join(self.paths['pdf'], 'figureA.png'))
                        
                    if ('E_total' and 'Heating' and 'Cooling' and 'E_HCL') in self.optimization_Types: 
                        if ('SolarEnergy' and 'Lighting') in self.optimization_Types:                          
					#save figures
                            self.fig['fig1'].savefig(os.path.join(self.paths['pdf'], 'figure1.pdf'))
                            self.fig['fig2'].savefig(os.path.join(self.paths['pdf'], 'figure2.pdf'))
                            self.fig['fig1'].savefig(os.path.join(self.paths['pdf'], 'figure1.png'))
                            self.fig['fig2'].savefig(os.path.join(self.paths['pdf'], 'figure2.png'))
               
                
                    if ('E_total_elec' and 'Heating_elec' and 'Cooling_elec'  and 'E_HCL_elec' ) in self.optimization_Types:
				if ('SolarEnergy' and 'Lighting') in self.optimization_Types:           
					#save figures
					self.fig['figB'].savefig(os.path.join(self.paths['pdf'], 'figureB.pdf'))
					self.fig['figC'].savefig(os.path.join(self.paths['pdf'], 'figureC.pdf'))
					self.fig['figB'].savefig(os.path.join(self.paths['pdf'], 'figureB.png'))
					self.fig['figC'].savefig(os.path.join(self.paths['pdf'], 'figureC.png'))
                    
                else:
                    for ii in self.optimization_Types: 
                        self.fig[ii].savefig(os.path.join(self.paths['pdf'], 'figure_' + ii + '.pdf'), transparent=True)
                    

                 
                for ii in self.optimization_Types:
				if ii == 'E_total' or ii =='Heating' or ii =='Cooling' or ii =='E_HCL' or ii =='SolarEnergy' or ii =='Lighting':
					# save results 
					self.ResultsBuildingSimulation[ii].to_csv(os.path.join(self.paths['result'], 'BuildingSimulation_'+ ii + '.csv'))
     
				elif ii == 'E_total_elec' or ii == 'Heating_elec' or ii == 'Cooling_elec'  or ii == 'E_HCL_elec':
					self.ResultsBuildingSimulation[ii].to_csv(os.path.join(self.paths['result'], 'BuildingSimulationELEC_'+ ii + '.csv'))
				else:
					pass
                       

                       
                
                x_angles_df = pd.DataFrame(self.x_angles)
                y_angles_df = pd.DataFrame(self.y_angles)           
                
                if self.start == 0 and self.end == 8760:
                    
                    self.monthlyData.to_csv(os.path.join(self.paths['result'], 'monthlyData.csv'))
                    self.yearlyData.to_csv(os.path.join(self.paths['result'], 'yearlyData.csv'))
                else:
                    
                    self.HourlyTotalData.to_csv(os.path.join(self.paths['result'], 'HourlyTotalData.csv'))
                    
                #BestKeyDF.to_csv(os.path.join(self.paths['result'], 'BestKeyMonthly.csv'))                
                x_angles_df.to_csv(os.path.join(self.paths['result'], 'X-Angles.csv'))
                y_angles_df.to_csv(os.path.join(self.paths['result'], 'Y-Angles.csv'))
                			
                #convert heating/cooling system variables into strings			
                self.BuildingProperties["heatingSystem"] = str(self.BuildingProperties["heatingSystem"])
                self.BuildingProperties["coolingSystem"] = str(self.BuildingProperties["coolingSystem"])
                self.BuildingProperties["start"] = self.start
                self.BuildingProperties["end"] = self.end
                self.BuildingProperties["T_start"] = self.SimulationOptions['Temp_start']
                self.BuildingProperties["SetBack_H"] = self.SimulationOptions['setBackTempH']
                self.BuildingProperties["SetBack_C"] = self.SimulationOptions['setBackTempC']
                				        
                 
                #save building properties in json files
                with open(os.path.join(self.paths['result'], 'BuildingProperties.json'), 'w') as f:
                				f.write(json.dumps(self.BuildingProperties))
                		
                print '\nResults are saved!'    
		
          print "\nSimulation end: " + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
		

	def SolveASF(self):
         #main method which calls all sub-methods
		
            self.setPaths()				
            self.CalculateVariables()
            self.runRadiationCalculation()		  		 
            self.PrepareRadiationData()													   
            self.runBuildingSimulation()
            
            
            if (self.SimulationData['ShowFig'] or self.SimulationData['Save']) and self.start == 0 and self.end == 8760:
                 self.PrepareYearlyResults()
                 self.createAllPlots()
            
            elif (self.SimulationData['ShowFig'] or self.SimulationData['Save']) and (self.start != 0 or self.end != 8760):
                 self.PrepareHourlyResults()
                 self.createHourlyPlots()
            
            else:
            	self.fig = None 
               
               			
            self.SaveResults()
            
            #print self.yearlyData

								

			
