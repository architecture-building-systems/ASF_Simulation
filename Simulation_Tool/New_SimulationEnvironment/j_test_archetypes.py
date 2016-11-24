import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
import re as re
import itertools
import csv
import os,sys

from j_paths import PATHS
from buildingSystem import *  
from SimulationClass import ASF_Simulation as ASF
from j_build_schedules import build_schedules
from j_build_dictionaries import  ArchT_build_df, MakeDicts, sort_dicts
import j_epw_import_tools as epw_tools

#Constants
#---------

SimulationData= {
	'optimizationTypes' : ['E_total'],
	'DataName' : 'ZH05_49comb',
	'geoLocation' : 'Zuerich_Kloten_2005',
	'EPWfile' : 'Zuerich_Kloten_2005.epw',
	'Save' : False,
	'ShowFig': False}

#Set panel data
PanelData={
	"XANGLES": [0, 15, 30, 45, 60, 75, 90],
	"YANGLES" : [-45, -30,-15,0, 15, 30, 45],
	"NoClusters":1,
	"numberHorizontal":6,
	"numberVertical":9,
	"panelOffset":400,
	"panelSize":400,
	"panelSpacing":500}
		
		#Set Building Parameters in [mm]
BuildingData={
	"room_width": 4900,     
	"room_height":3100,
	"room_depth":7000,
	"glazing_percentage_w": 0.92,
	"glazing_percentage_h": 0.97}

#Set Default Values (For testing and sorting purposes)
BuildingProperties_default = {
	"glass_solar_transmitance" : 0.687,
	"glass_light_transmitance" : 0.744,
	"lighting_load" : 11.74,
	"lighting_control" : 300,
	"Lighting_Utilisation_Factor" :  0.45,
	"Lighting_MaintenanceFactor" : 0.9,
	"U_em" : 0.2,"U_w" : 1.2,
	"ACH_vent" : 1.5,
	"ACH_infl" :0.5,
	"ventilation_efficiency" : 0.6,
	"c_m_A_f" : 165 * 10**3,
	"theta_int_h_set" : 20,
	"theta_int_c_set" : 26,
	"phi_c_max_A_f": -np.inf,
	"phi_h_max_A_f":np.inf,
	"heatingSystem" : DirectHeater,
	"coolingSystem" : DirectCooler, 
	"heatingEfficiency" : 1,
	"coolingEfficiency" :1
	}

SimulationOptions_default = {
	'setBackTempH' : 4.,
	'setBackTempC' : 4., 
	'Occupancy' : 'schedules_occ_OFFICE.csv',
	'ActuationEnergy' : False}
 
paths = PATHS()

b_props = ArchT_build_df(BuildingData)

#build_schedules(b_props,paths['Archetypes_schedules']) goes here. Currently still broken, schedules were generated using jupyter notebooks code. If the set remains the same, the existing scehdules will be sufficient.

#Select subset of b_props:
b_props = b_props[b_props.interval =='2005-2020']
b_props = b_props[b_props.type == 'construction']
BP_dict, SO_dict = MakeDicts(b_props)

print b_props.Ths_set_C
#Generate list of building names for iteration:
keylist = []
for key,item in BP_dict.iteritems():
	k = """%s"""%key
	keylist.append(k)

#Runlist can be a subset of keylist:
runlist = keylist

#Create new dictionary as subsets of BP_dict and SO_dict with runlist as keys:
BP_dict_run = { key:value for key,value in BP_dict.items() if key in runlist }
SO_dict_run = { key:value for key,value in SO_dict.items() if key in runlist }

#Run for default values
"""
ASF_archetypes=ASF(SimulationData = SimulationData, PanelData = PanelData, BuildingData = BuildingData, BuildingProperties = BuildingProperties_default, SimulationOptions = SimulationOptions_default)
ASF_archetypes.SolveASF()
all_results = ASF_archetypes.yearlyData.T
all_results['Name'] = 'Default'
all_results = all_results.set_index(['Name'])
"""
print BuildingProperties_default
#loop through building properties and simulation options dictionaries:
for i in range(0,len(runlist)):
	BP = sort_dicts(BP_dict_run[runlist[i]],BuildingProperties_default)
	SO = sort_dicts(SO_dict_run[runlist[i]],SimulationOptions_default)
	print BP
	"""ASF_archetypes=ASF(SimulationData = SimulationData, PanelData = PanelData, BuildingData = BuildingData, BuildingProperties = BP, SimulationOptions = SO)
	ASF_archetypes.SolveASF()
	current_result = ASF_archetypes.yearlyData.T
	current_result['Name'] = runlist[i]
	current_result = current_result.set_index(['Name'])
	if i == 0:
		all_results = current_result
	else:
		temp_list = [all_results,current_result]
		all_results = pd.concat(temp_list)
print '--simulations complete--'

#write results to csv:
all_results.to_csv(os.path.join(paths['CEA_folder'],'all_results.csv'))"""