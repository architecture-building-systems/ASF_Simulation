import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np
import csv
import os,sys

from j_paths import PATHS
from buildingSystem import *  
from SimulationClass import ASF_Simulation as ASF
from j_build_schedules import build_schedules
from j_build_dictionaries import  ArchT_build_df, MakeDicts, sort_dicts
import j_epw_import_tools as epw_tools

paths = PATHS()

#Constants
#---------

SimulationData= {
	'optimizationTypes' : ['E_total'],
	'DataName' : 'ZH13_49comb',
	'geoLocation' : 'Zuerich_Kloten_2013',
	'EPWfile' : 'Zuerich_Kloten_2013.epw',
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
 
b_props = ArchT_build_df(BuildingData)

#build_schedules(b_props) goes here. Currently still broken, schedules were generated using jupyter notebooks code. If the set remains the same, the existing scehdules will be sufficient.

#Select subset of b_props:
#b_props = b_props[b_props.interval =='2005-2020']
#b_props = b_props[b_props.type == 'construction']

#Generate dictionaries from dataframes
BP_dict, SO_dict = MakeDicts(b_props)

#Generate list of building names for iteration:
keylist = []
for key,item in BP_dict.iteritems():
	keylist.append(key)

#Runlist can be a subset of keylist:
runlist = keylist

#Create new dictionary as subsets of BP_dict and SO_dict with runlist as keys:
BP_dict_run = { key:value for key,value in BP_dict.items() if key in runlist }
SO_dict_run = { key:value for key,value in SO_dict.items() if key in runlist }

#Empty lists for recording BP and SO dictionaries
bp_list=[]
so_list=[]

#loop through building properties and simulation options dictionaries:
for i in range(0,len(runlist)):
	print 'simulation %i/%i:' %(i,len(runlist))
	#preprocessing 1: sort dictionaries to match defaults. Not sure if this makes any difference but it makes things more legible.
	BP = sort_dicts(BP_dict_run[runlist[i]],BuildingProperties_default)
	SO = sort_dicts(SO_dict_run[runlist[i]],SimulationOptions_default)
	#preprocessing 2: convert setpoints to float. Doing this here avoids loops in other parts of the program
	BP['theta_int_c_set'] = float(BP['theta_int_c_set'])
	BP['theta_int_h_set'] = float(BP['theta_int_h_set'])
	
	#append this iteration's dictionaries to the dictionary list
	bp_list.append(BP)
	so_list.append(SO)
	
	#Run ASF simulation
	
	ASF_archetypes=ASF(SimulationData = SimulationData, PanelData = PanelData, BuildingData = BuildingData, BuildingProperties = BP, SimulationOptions = SO)
	ASF_archetypes.SolveASF()

	#Add building name to dataframe and append subsequent iterations:
	current_result = ASF_archetypes.yearlyData.T
	current_result['Name'] = runlist[i]
	current_result = current_result.set_index(['Name'])
	if i == 0:
		all_results = current_result
	else:
		temp_list = [all_results,current_result]
		all_results = pd.concat(temp_list)
	print ASF_archetypes.yearlyData
	
print '--simulations complete--'

#write results to csv:
timestr = time.strftime("%d%m%Y_%H%M")
name = 'Archetypes_'+SimulationData.get('DataName')+'_'+timestr+'.csv'
all_results.to_csv(os.path.join(paths['CEA_folder'],name))

#convert simulation parameters to dataframe and write to csv (ovrrides previous simulation)
bp_f = pd.DataFrame(bp_list)
so_f = pd.DataFrame(so_list)
#bp_f.to_csv(os.path.join(paths['CEA_folder'],timestr+'_BP.csv'))
#so_f.to_csv(os.path.join(paths['CEA_folder'],timestr+'_SO.csv'))
