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

	def __init__(self,
            SimulationData = 
            {'optimizationTypes' : ['E_total'],'DataName' : 'ZH13_49comb','geoLocation' : 'Zuerich_Kloten_2013', 'EPWfile': 'Zuerich_Kloten_2013.epw','Save' : False, 'ShowFig': False},
            PanelData = 
            {"XANGLES": [0, 15, 30, 45, 60, 75, 90],"YANGLES" : [-45, -30,-15,0, 15, 30, 45],"NoClusters":1,"numberHorizontal":6,"numberVertical":9,"panelOffset":400,"panelSize":400,"panelSpacing":500},
            BuildingData = 
            {"room_width": 4900, "room_height":3100, "room_depth":7000, "glazing_percentage_w": 0.92,"glazing_percentage_h": 0.97, "WindowGridSize": 150},
            BuildingProperties = 
            {"glass_solar_transmitance" : 0.687,"glass_light_transmitance" : 0.744,"lighting_load" : 11.74,"lighting_control" : 300,"Lighting_Utilisation_Factor" :  0.45,\
            "Lighting_MaintenanceFactor" : 0.9,"U_em" : 0.2,"U_w" : 1.2,"ACH_vent" : 1.5,"ACH_infl" :0.5,"ventilation_efficiency" : 0.6 ,"c_m_A_f" : 165 * 10**3,"theta_int_h_set" : 20,\
            "theta_int_c_set" : 26,"phi_c_max_A_f": -np.inf,"phi_h_max_A_f":np.inf,"heatingSystem" : DirectHeater,"coolingSystem" : DirectCooler, "heatingEfficiency" : 1,"coolingEfficiency" :1},
            SimulationOptions= 
            {'setBackTempH' : 4.,'setBackTempC' : 4., 'Occupancy' : 'Occupancy_COM.csv','ActuationEnergy' : False}):
                            
                            

		self.SimulationData=SimulationData
		self.PanelData=PanelData
		self.BuildingData=BuildingData
		self.BuildingProperties=BuildingProperties
		self.SimulationOptions=SimulationOptions

		
		self.XANGLES=self.PanelData['XANGLES']
		self.YANGLES = self.PanelData['YANGLES']		
		self.createPlots=False
		self.geoLocation = SimulationData['geoLocation']
		self.now = time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
		self.optimization_Types = self.SimulationData['optimizationTypes']


		#Set panel data
		self.FolderName={
		"DataName": SimulationData['DataName'],
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
		Occupancy = self.SimulationOptions['Occupancy']

		# create dictionary to write all paths:
		self.paths = {}
		
		# find path of current folder (simulation_environment)
		self.paths['main'] = os.path.abspath(os.path.dirname(sys.argv[0]))
		
		# define self.paths of subfolders:
		self.paths['data'] =os.path.join(self.paths['main'], 'data')
		self.paths['python'] = os.path.join(self.paths['main'], 'python')
		self.paths['aux_files'] = os.path.join(self.paths['python'], 'aux_files')
		
		self.paths['radiation_results'] = os.path.join(self.paths['main'],'radiation_results_' + self.FolderName['DataName'])
		self.paths['radiation_wall'] = os.path.join(self.paths['main'],  'radiation_wall_' + self.FolderName['DataName'])
		self.paths['PV'] = os.path.join(self.paths['main'], 'PV_results')

		self.paths['save_results_path'] = self.paths['PV']
		self.paths['weather_folder']= os.path.join(os.path.dirname(self.paths['main']), 'WeatherData')
		
		
		# define path of weather file:
		self.paths['weather_folder']= os.path.join(os.path.dirname(self.paths['main']), 'WeatherData')
		print self.geoLocation
		self.paths['weather'] = os.path.join(self.paths['weather_folder'], self.geoLocation + '.epw')
		
		# add python_path to system path, so that all files are available:
		sys.path.insert(0, self.paths['aux_files'])
		sys.path.insert(0, self.paths['python'])
		
		
		from epwreader import epw_reader
		#read epw file of needed destination
		self.weatherData = epw_reader(self.paths['weather'])
		
		
		#radiation subfolder is created, there the radiation_results are saved
		if not os.path.isdir(self.paths['radiation_results']):
				os.makedirs(self.paths['radiation_results'])
		
		if not os.path.isdir(self.paths['radiation_wall']):
				os.makedirs(self.paths['radiation_wall'])
		
		# define path of geographical location:
		self.paths['geo_location'] = os.path.join(self.paths['data'], 'geographical_location')
		self.paths['geo'] = os.path.join(self.paths['geo_location'], self.geoLocation)
		
		#define self.paths of the RC-Model    
		self.paths['5R1C_ISO_simulator'] = os.path.join(self.paths['main'], '5R1C_ISO_simulator')
		self.paths['5R1C_ISO_simulator_data'] = os.path.join(self.paths['5R1C_ISO_simulator'], 'data')    
		self.paths['Occupancy'] = os.path.join(self.paths['5R1C_ISO_simulator_data'], Occupancy) 
		
		from SunAnglesTrackingAndTemperatureFunction import SunAnglesTackingAndTemperature
		# create sun data based on grasshopper file, this is only possible with the ladybug component SunPath
		self.SunTrackingData = SunAnglesTackingAndTemperature(paths = self.paths,
														 weatherData = self.weatherData)    
		#execfile(os.path.join(self.paths['aux_files'], 'SunAngles_Tracking_and_temperature.py'))
		
		# calculate and save lookup table if it does not yet exist:
		self.paths['data_python'] = os.path.join(self.paths['data'], 'python')
		self.paths['electrical_simulation'] = os.path.join(self.paths['data_python'], 'electrical_simulation') 
	   
		
		if not os.path.isfile(os.path.join(self.paths['electrical_simulation'], 'curr_model_submod_lookup.npy')): 
			if not os.path.isdir(self.paths['electrical_simulation']):
				os.makedirs(self.paths['electrical_simulation'])
			execfile(os.path.join(self.paths['aux_files'], 'create_lookup_table.py'))
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
		
		from hourRadiation import hourRadiation, hourRadiation_calculated, sumHours
		
		
		self.hourRadiation = hourRadiation(self.hour_in_month, self.daysPerMonth)
		self.hourRadiation_calculated = hourRadiation_calculated(self.hour_in_month,self.daysPerMonth)
		self.sumHours = sumHours(self.daysPerMonth)

		
		#Make a list of all angle combinations
		self.ANGLES= [(x, y) for x in self.XANGLES for y in self.YANGLES]
		
		#append to more ANGLES combination option for the angle carpetplot
		self.ANGLES.append((0.1111,0.1111)) # no sun
	   
		
		#create a dicitionary with all angle combinations
		self.combinationAngles = {}
		
		for i in range(0,len(self.ANGLES)):
			self.combinationAngles[i] = self.ANGLES[i]
		
		
		self.NumberCombinations = len(self.XANGLES)*len(self.YANGLES) #*NoClusters
		
		

		
	def runRadiationCalculation(self):
		 
		from RadiationCalculation import CalculateRadiationData     
				
		
		
		#Calculate the Radiation on the solar panels and window with ladybug
		self.BuildingRadiationData_HOD = CalculateRadiationData(XANGLES = self.XANGLES, 
                                                                    YANGLES = self.YANGLES, 
												paths = self.paths, 
												daysPerMonth = self.daysPerMonth, 
												hour_in_month = self.hour_in_month,
												DataNamePV = self.FolderName['DataName'],
												DataNameWin = self.FolderName['DataName'])
			
		
		#if there are no panels vertical and horizontal
		if self.PanelData['numberHorizontal'] == 0 and self.PanelData['numberVertical'] == 0:
			self.PV_electricity_results = {}
			
			self.PV_electricity_results['Pmpp_sum'] = np.array(self.NumberCombinations * len(self.hour_in_month) * [0])
			print "PV_electricity_results is zero"
			
		
		#with the radiation_results the Pv_results are calcualted, make sure you know where the results are saved, otherwise they will just be loaded
		if not os.path.isfile(os.path.join(self.paths['PV'], 'PV_electricity_results_' + self.FolderName['DataName'] + '.npy')): 
			if not os.path.isdir(self.paths['PV']):
				os.makedirs(self.paths['PV'])
				
			from asf_electricity_production_mauro_3 import asf_electricity_production
			
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
								   simulationOption =None,
								   XANGLES = self.XANGLES, YANGLES= self.YANGLES, 
								   hour_in_month = self.hour_in_month, 
								   paths = self.paths, DataNamePV = self.FolderName['DataName'])
								   
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
								   simulationOption =None,
								   XANGLES = self.XANGLES, YANGLES= self.YANGLES, 
								   hour_in_month = self.hour_in_month,
								   paths = self.paths, DataNamePV = self.FolderName['DataName'])
		
		else: 
			self.PV_electricity_results = np.load(os.path.join(self.paths['PV'], 'PV_electricity_results_' + self.FolderName['DataName'] + '.npy')).item()
			self.PV_detailed_results = np.load(os.path.join(self.paths['PV'], 'PV_detailed_results_' + self.FolderName['DataName'] + '.npy')).item()
			print '\nLadyBug data loaded from Folder:'
			print 'radiation_results_' + self.FolderName['DataName']  
			
   
	   
	 
	def PrepareRadiationData(self):
		
		from hourRadiation import hourRadiation, hourRadiation_calculated, sumHours

		
		
		hourRadiation = hourRadiation(self.hour_in_month, self.daysPerMonth)
		hourRadiation_calculated = hourRadiation_calculated(self.hour_in_month,self.daysPerMonth)
		sumHours = sumHours(self.daysPerMonth)
		
				  
		#add the radiation data to the specific HOY
		self.PV={}
		self.BuildingRadiationData_HOY= {}
		passedHours = 0
		
		for monthi in range(1,13):
			if monthi == 1:
				passedHours = 0
			else:
				passedHours = sumHours[monthi-2]     
			
			for HOD in self.hour_in_month[monthi]:
				for ii in range(0,self.daysPerMonth[monthi-1]):             
					DAY = ii*24 + int(HOD)   
					self.BuildingRadiationData_HOY[passedHours + DAY] = self.BuildingRadiationData_HOD[monthi][DAY] #W
		
		
		for hour_of_year in range(0,8760):
			self.PV[hour_of_year]= {}
			self.PV[hour_of_year]['PV']= []
			
			  
		count = 0
		DAY = 0
		
		for monthi in range(1,13):
			if monthi == 1:
				passedHours = 0
			else:
				passedHours = sumHours[monthi-2]
				
			for HOD in self.hour_in_month[monthi]:
					for jj in range(0,self.daysPerMonth[monthi-1]):
						DAY = jj*24 + HOD     
						self.PV[passedHours + DAY]['PV'] = self.PV_electricity_results['Pmpp_sum'][count:count+self.NumberCombinations] #Watts
					count +=self.NumberCombinations
					
		for hour_of_year in range(0,8760):
			if hour_of_year not in hourRadiation:
					self.BuildingRadiationData_HOY[int(hour_of_year)] = np.asarray([0]* self.NumberCombinations, dtype = np.float64)
					self.PV[int(hour_of_year)]['PV'] = np.asarray([0]* self.NumberCombinations, dtype = np.float64)
		   
		
		
	def runBuildingSimulation(self):

           
           
            # add python_path to system path, so that all files are available:
            sys.path.insert(0, self.paths['5R1C_ISO_simulator'])
            self.setBackTempH = self.SimulationOptions['setBackTempH']
            self.setBackTempC = self.SimulationOptions['setBackTempC']     
            		
            from energy_minimization import RC_Model
            from prepareDataMain import prepareAngles, prepareResults, prepareResultsELEC
            from read_occupancy import read_occupancy
            		
            #create dicitionaries to save the results
            self.hourlyData = {}
            self.monthlyData = {}
            self.yearlyData = {}
            self.ResultsBuildingSimulation = {}
            self.BuildingSimulationELEC = {}
            			
            self.x_angles = {} #optimized x-angles
            self.y_angles = {} #optimized y-angles
            self.BestKey_df = {} #optimized keys of the ANGLES dictionary
            		
            		
            #set parameters
            human_heat_emission=0.12 #[kWh] heat emitted by a human body per hour. Source: HVAC Engineers Handbook, F. Porges
            roomFloorArea = self.BuildingData['room_width']/1000.0 * self.BuildingData['room_depth']/1000.0 #[m^2] floor area
            		 
            				
            #people/m2/h, W    
            occupancy, Q_human = read_occupancy(myfilename = self.paths['Occupancy'], human_heat_emission = human_heat_emission, floor_area = roomFloorArea)    
            		
            				
            #run the RC-Model for the needed optimization Type and save RC-Model results in dictionaries for every optimization type analysed
            for optimizationType in self.optimization_Types:

				

			self.hourlyData[optimizationType], self.ResultsBuildingSimulation[optimizationType], \
                 self.BuildingSimulationELEC[optimizationType] = RC_Model (
                                                                         optimization_type = optimizationType, 
                                                                         paths = self.paths,
                                                                         building_data = self.BuildingData, 
                                                                         weatherData = self.weatherData, 
                                                                         hourRadiation = self.hourRadiation, 
                                                                         BuildingRadiationData_HOY = self.BuildingRadiationData_HOY, 
                                                                         PV = self.PV, 
                                                                         NumberCombinations = self.NumberCombinations, 
                                                                         combinationAngles = self.combinationAngles,
                                                                         BuildingProperties = self.BuildingProperties,

                                                                         setBackTempH = self.setBackTempH,
                                                                         setBackTempC = self.setBackTempC,

                                                                         occupancy = occupancy,
                                                                         Q_human = Q_human
                                                                         )
			
			#prepareAngles creates two arrays with x- and y-angles for the respective optimization type and a dataFrame with all the keys stored  
			self.BestKey_df[optimizationType], self.x_angles[optimizationType], self.y_angles[optimizationType] = prepareAngles(
																				Building_Simulation_df = self.ResultsBuildingSimulation[optimizationType], 
																				daysPerMonth = self.daysPerMonth,
																				ANGLES = self.ANGLES)   
		   
			
		
			if optimizationType == ('E_total' or 'Heating' or 'Cooling' or 'E_HCL' or 'SolarEnergy' or 'Lighting'):
				# prepare Building simulation Data into final form, monthly Data [kWh/DaysPerMonth], self.yearlyData [kWh/year]
				self.monthlyData[optimizationType], self.yearlyData[optimizationType] = prepareResults(Building_Simulation_df = self.ResultsBuildingSimulation[optimizationType])
			
			elif optimizationType == ('E_total_elec' or 'Heating_elec' or 'Cooling_elec'  or 'E_HCL_elec' ):                                                           
				self.monthlyData[optimizationType], self.yearlyData[optimizationType] = prepareResultsELEC(Building_Simulation_df = self.BuildingSimulationELEC[optimizationType])
			
	   

	def createAllPlots(self):
		
		from createCarpetPlot import createCarpetPlot, createCarpetPlotXAngles, createCarpetPlotYAngles
		
		self.fig = {}    
		
		if ('E_total') in self.optimization_Types:    
			#create the carpet plots detailing the net energy consumption, set only monthlyData['E_total']
			print '\nFigure: total energy demand'    
			
			fig0 = createCarpetPlot (monthlyData = self.monthlyData['E_total'], roomFloorArea = self.roomFloorArea,  H = 'H', C = 'C', E = 'E', E_HCL = 'E_HCL')
			
			self.fig.update({'fig0': fig0})
		
		if ('E_total_elec') in self.optimization_Types:
			
			print 'Figure: total electrical energy demand'
			
			figA = createCarpetPlot (monthlyData = self.monthlyData['E_total_elec'], roomFloorArea = self.roomFloorArea,  H = 'H_elec', C = 'C_elec', E = 'E_elec', E_HCL = 'E_HCL_elec')
			self.fig.update({'figA' : figA})
		
		
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




	def SaveResults(self):
		
		Save = self.SimulationData['Save']
		self.monthlyData = pd.DataFrame(self.monthlyData)
		self.yearlyData = pd.DataFrame(self.yearlyData)
		#BestKeyDF = pd.DataFrame(self.BestKey_df)    
		
		if Save == True: 
			
			# create folder where results will be saved:
			self.paths['result_folder'] = os.path.join(self.paths['main'], 'Results') 
			self.paths['result']= os.path.join(self.paths['result_folder'], 'Results_' + self.geoLocation + '_date_' + self.now)
			
			if not os.path.isdir(self.paths['result']):
				os.makedirs(self.paths['result'])    
			
			#create folder to save figures as svg and png:
			self.paths['pdf'] = os.path.join(self.paths['result'], 'png')
			
			os.makedirs(self.paths['pdf'])
			
			 
			self.fig['fig0'].savefig(os.path.join(self.paths['pdf'], 'figure0' + '.pdf'))
			
			if ('E_total_elec') in self.optimization_Types:
				self.fig['figA'].savefig(os.path.join(self.paths['pdf'], 'figureA' + '.pdf'))        
			
			
			if ('E_total' and 'Heating' and 'Cooling' and 'E_HCL') in self.optimization_Types: 
				if ('SolarEnergy' and 'Lighting') in self.optimization_Types:                          
					#save figures
					self.fig['fig1'].savefig(os.path.join(self.paths['pdf'], 'figure1' + '.pdf'))
					self.fig['fig2'].savefig(os.path.join(self.paths['pdf'], 'figure2' + '.pdf'))
				
				
			if ('E_total_elec' and 'Heating_elec' and 'Cooling_elec'  and 'E_HCL_elec' ) in self.optimization_Types:
				if ('SolarEnergy' and 'Lighting') in self.optimization_Types:           
					#save figures
					self.fig['figB'].savefig(os.path.join(self.paths['pdf'], 'figureB' + '.pdf'))
					self.fig['figC'].savefig(os.path.join(self.paths['pdf'], 'figureC' + '.pdf'))
					

			for ii in self.optimization_Types:
				if ii == ('E_total' or 'Heating' or 'Cooling' or 'E_HCL' or 'SolarEnergy' or 'Lighting'):
					# save results 
					self.ResultsBuildingSimulation[ii].to_csv(os.path.join(self.paths['result'], 'BuildingSimulation_'+ ii + '.csv'))
				elif ii == ('E_total_elec' or 'Heating_elec' or 'Cooling_elec'  or 'E_HCL_elec' ):
					self.BuildingSimulationELEC[ii].to_csv(os.path.join(self.paths['result'], 'BuildingSimulationELEC_'+ ii + '.csv'))
			
			x_angles_df = pd.DataFrame(self.x_angles)
			y_angles_df = pd.DataFrame(self.y_angles)           
			
			#hourlyData['E_total'].to_csv(os.path.join(self.paths['result'], 'hourlyData.csv'))
			#BestKeyDF.to_csv(os.path.join(self.paths['result'], 'BestKeys.csv'))
			self.monthlyData.to_csv(os.path.join(self.paths['result'], 'monthlyData.csv'))
			self.yearlyData.to_csv(os.path.join(self.paths['result'], 'yearlyData.csv'))
			x_angles_df.to_csv(os.path.join(self.paths['result'], 'X-Angles.csv'))
			y_angles_df.to_csv(os.path.join(self.paths['result'], 'Y-Angles.csv'))
			
			
			self.BuildingProperties["heatingSystem"] = str(self.BuildingProperties["heatingSystem"])
			self.BuildingProperties["coolingSystem"] = str(self.BuildingProperties["coolingSystem"])
			
				 
			#save building properties
			with open(os.path.join(self.paths['result'], 'BuildingProperties.json'), 'w') as f:
				f.write(json.dumps(self.BuildingProperties))
		
			print '\nResults are saved!'    
		
		print "\nSimulation end: " + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
		

	def SolveASF(self):
		

		self.initializeASF()
		self.setBuildingParameters()		
		self.initializeBuildingSimulation()
		self.setPaths()				
		self.CalculateVariables()
		self.runRadiationCalculation()		  		 
		#rearrange the Radiation Data on PV and Window into HOY form
		self.PrepareRadiationData()													   
		self.runBuildingSimulation()

		if self.SimulationData['ShowFig'] or self.SimulationData['Save']:   
			self.createAllPlots()
		else:

			self.fig = None #?

		   			
		self.SaveResults()
								

			
