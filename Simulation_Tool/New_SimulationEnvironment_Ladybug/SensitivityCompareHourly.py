# -*- coding: utf-8 -*-
"""
Created on 17 March 2017 11:53:33 

@author: PJ
"""
import os, sys

import numpy as np
import pandas as pd
from buildingSystem import *  
from SimulationClassHourly import ASF_Simulation

sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), '5R1C_ISO_simulator'))    
	
from buildingPhysics import Building #Importing Building Class
from supplySystem import *  
from emissionSystem import *


for sens in np.arange(0.1,3.0,0.5):

	# SimulationPeriod = {
	# 'FromMonth': 7, #7, #1,
	# 'ToMonth': 7,#7, #1,
	# 'FromDay': 6, #6, #8,
	# 'ToDay': 6, #8,
	# 'FromHour': 5,#5
	# 'ToHour': 20}#20



	# #Set simulation data 
	# SimulationData= {
	# 'optimizationTypes' : ['E_total'], 
	# 'DataFolderName' : 'ZH13test', 
	# 'FileName' : 'ZH13test',
	# 'geoLocation' : 'Zuerich_Kloten_2013', 
	# 'EPWfile': 'Zuerich_Kloten_2013.epw',
	# 'Save' : True, 
	# 'ShowFig': True
	# }   

	SimulationPeriod = {
	'FromMonth': 1, #7, #1,
	'ToMonth': 1,#7, #1,
	'FromDay': 8, #6, #8,
	'ToDay': 8, #8,
	'FromHour': 5,#5
	'ToHour': 20}#20
	
	
	#Set simulation data 
	SimulationData = {
	'optimizationTypes' : ['E_total'], 
	'DataFolderName' : 'ZH13_49comb_WinterSunnyDay', 
	'FileName' : 'ZH13_49comb_WinterSunnyDay',
	'geoLocation' : 'Zuerich_Kloten_2013', 
	'EPWfile': 'Zuerich_Kloten_2013.epw',
	'Save' : False, 
	'ShowFig': True, 
		'timePeriod': None} # asf_electricity_function  


	PanelData = {
	"XANGLES": [0, 15, 30, 45, 60, 75, 90],
	"YANGLES" : [-45, -30,-15,0, 15, 30, 45],
	"NoClusters":1,
	"numberHorizontal":6,
	"numberVertical":9,
	"panelOffset":400,
	"panelSize":400,
	"panelSpacing":500, 
	"panelGridSize" : 25}

	#Set Building Parameters in [mm]
	BuildingData={
	"room_width": 4900,     
	"room_height":3100,
	"room_depth":7000,
	"glazing_percentage_w": 0.92,
	"glazing_percentage_h": 0.97,
	"WindowGridSize" : 200,
	"BuildingOrientation" : 0} 

	##@Michael: This will need to be modified to fit your model
	BuildingProperties={
	"glass_solar_transmittance" : 0.691 ,
	"glass_light_transmittance" : 0.744 ,
	"lighting_load" : 11.74 ,
	"lighting_control" : 300,
	"Lighting_Utilisation_Factor" :  0.45, # 0.75
	"Lighting_Maintenance_Factor" : 0.9,
	"U_em" : 0.2, 
	"U_w" : sens, #1.1,
	"ACH_vent" : 1.5,
	"ACH_infl" : 0.5,
	"ventilation_efficiency" : 0.6,
	"c_m_A_f" : 165 * 10**3,
	"theta_int_h_set" : 22,
	"theta_int_c_set" : 26,
	"phi_c_max_A_f": -np.inf,
	"phi_h_max_A_f":np.inf,
	"heatingSupplySystem" : DirectHeater,
	"coolingSupplySystem" : DirectCooler,
	"heatingEmissionSystem" : AirConditioning,
	"coolingEmissionSystem" : AirConditioning,}
	#
	#Set simulation Properties
	SimulationOptions= {
	'setBackTempH' : 4.,
	'setBackTempC' : 4.,
	'Occupancy' : 'Occupancy_COM.csv',
	'ActuationEnergy' : False,
	'Temp_start' : 22,
	'human_heat_emission' : 0.12} #[kWh] heat emitted by a human body per hour. Source: HVAC Engineers Handbook, F. Porges
	   

		
	ASFtest = ASF_Simulation(SimulationPeriod = SimulationPeriod, 
							 SimulationData = SimulationData, 
							 PanelData = PanelData,
							 BuildingData = BuildingData,
							 BuildingProperties = BuildingProperties, 
							 SimulationOptions = SimulationOptions)
	ASFtest.SolveASF()

	print ASFtest.TotalHourlyData
