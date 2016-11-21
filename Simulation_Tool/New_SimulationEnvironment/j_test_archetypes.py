import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
#import cdecimal as dec
import re as re
import itertools
import csv
import os, sys
from buildingSystem import *  
from mainSimulation import MainCalculateASF
from j_build_schedules import build_schedules
import j_epw_import_tools as epw_tools

paths = {}
paths['main'] = os.path.abspath(os.path.dirname(sys.argv[0]))
paths['CEA_folder'] = os.path.join(paths['main'], 'CEA_Archetypes_CH') 
paths['Archetypes'] = os.path.join(paths['CEA_folder'], 'Archetypes') 
paths['Archetypes_properties'] = os.path.join(paths['Archetypes'],'Archetypes_properties.xlsx')
paths['Archetypes_schedules'] = os.path.join(paths['Archetypes'],'Archetypes_schedules.xlsx')
#weather_path = 'C:\Users\Zghiru\Documents\GitHub\RC_BuildingSimulator\Justin_Semseter_Project\data\Zurich-Kloten_2013.epw'
#occupancy_path = 'C:\Users\Zghiru\Documents\GitHub\RC_BuildingSimulator\Justin_Semseter_Project\data\Occupancy_COM.csv'
#radiation_path = r'C:\Users\Zghiru\Documents\GitHub\RC_BuildingSimulator\Justin_Semseter_Project\data\radiation_Building_Zh.csv'
#archetypes_properties_path = "C:\Users\Zghiru\Documents\GitHub\RC_BuildingSimulator\Justin_Semseter_Project\data\CH\Archetypes\Archetypes_properties.xlsx"
#archetypes_schedules_path = "C:\Users\Zghiru\Documents\GitHub\RC_BuildingSimulator\Justin_Semseter_Project\data\CH\Archetypes\Archetypes_schedules.xlsx"
#occ_path = 'C:\Users\Zghiru\Documents\GitHub\RC_BuildingSimulator\Justin_Semseter_Project\schedules_occ.csv'

##Constants

SimulationData= {
'optimizationTypes' : ['E_total'], #'Heating','Cooling', 'E_HCL', 'Heating_elec','Cooling_elec', 'E_HCL_elec', 'SolarEnergy', 'Lighting'],
'DataName' : 'ZH05_49comb',#'ZH13_49comb', #'ZH05_49comb', #,
'geoLocation' : 'Zuerich_Kloten_2005', #'Zuerich_Kloten_2013', #'Zuerich_Kloten_2005',
'Save' : False}

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

################################################################################################################
lighting_ontrol_d ={
"MULTI_RES":250,
"SINGLE_RES":200,
"HOTEL":300,
"OFFICE":350,
"RETAIL":400,
"FOODSTORE":400,
"RESTAURANT":250,
"INDUSTRIAL":300,
"SCHOOL":350,
"HOSPITAL":400,
"GYM":300
	
}

def ArchT_build_df(BuildingData):
	arch = pd.read_excel(paths['Archetypes_properties'],sheetname='THERMAL')
	r = re.compile("([a-zA-Z_]+)")
	m = r.match(arch["Code"][1])
	
	arch["code1"] = pd.DataFrame([r.match(string).groups() for string in arch.Code])
	arch = arch.set_index(['code1'])  
	arch = arch.drop(['SERVERROOM','PARKING','SWIMMING','COOLROOM'])
	arch = arch.reset_index(drop=False)
	arch = arch.drop('Es',axis=1)
	arch = arch.drop('Hs',axis=1)
	arch = arch.drop('U_roof',axis=1)
	arch = arch.drop('U_base',axis=1)
	
	int_loads = pd.read_excel(paths['Archetypes_properties'],sheetname='INTERNAL_LOADS')
	int_loads = int_loads.set_index(['Code'])
	int_loads = int_loads[['Qs_Wp','Ea_Wm2','El_Wm2']]
	int_loads = int_loads.reset_index(drop=False)

	T_sp = pd.read_excel(paths['Archetypes_properties'],sheetname='INDOOR_COMFORT')

	b_props = arch.merge(int_loads,how='left', left_on='code1', right_on='Code')
	b_props = b_props.merge(T_sp,how='left', left_on='code1', right_on='Code')
	b_props = b_props.drop('Code_y',axis=1)
	b_props = b_props.drop('Code',axis=1)
	b_props['CoolingSetBackTemp'] = b_props['Tcs_setb_C']-b_props['Tcs_set_C']
	b_props['HeatingSetBackTemp'] = b_props['Ths_set_C']-b_props['Ths_setb_C']
	
	volume = (BuildingData['room_width']/1000)*(BuildingData['room_depth']/1000)*(BuildingData['room_height']/1000)
	area = (BuildingData['room_width']/1000)*(BuildingData['room_depth']/1000)
	
	b_props['ACH'] = b_props['Ve_lps']*3.6/volume
	
	#Assign values for Cm from ISO13790:2008, Table 12, based on archetypes
	th_mass = b_props['th_mass']
	c_m = []
	for i in range(0,len(th_mass)):
		if th_mass[i] == "T1":
			c_m.append(110*10**3) #Light
		elif th_mass[i] == "T2":
			c_m.append(165 * 10**3) #Medium
		elif th_mass[i] == "T3":
			c_m.append(260*10**3) #Heavy
	b_props['c_m_A_f'] = pd.DataFrame(c_m)

#declare variables
	occupancy = []
	lighting_control = []
#declare constants
	glass_solar_transmitance = []
	glass_light_transmitance = []
	Lighting_Utilisation_Factor = []
	Lighting_MaintenanceFactor = [] 
	ACH_infl = [] 
	ventilation_efficiency = [] 
	phi_c_max_A_f = [] 
	phi_h_max_A_f = [] 
	heatingSystem = []  
	coolingSystem = [] 
	heatingEfficiency = []  
	coolingEfficiency = [] 
	ActuationEnergy = []    

	for code in b_props['code1']:
		#variables
		occupancy.append('schedules_occ_%s.csv'%code)
		lighting_control.append(lighting_ontrol_d.get(code))
		
		glass_solar_transmitance.append(0.687)
		glass_light_transmitance.append(0.744)
		Lighting_Utilisation_Factor.append(0.45) 
		Lighting_MaintenanceFactor.append(0.9) 
		ACH_infl.append(0.5) 
		ventilation_efficiency.append(0.6)
		phi_c_max_A_f.append(-np.inf)  
		phi_h_max_A_f.append(np.inf) 
		heatingSystem.append(DirectHeater) #DirectHeater, #ResistiveHeater #HeatPumpHeater
		coolingSystem.append(DirectCooler) #DirectCooler, #HeatPumpCooler
		heatingEfficiency.append(1)
		coolingEfficiency.append(1)
		ActuationEnergy.append(False)
		
	b_props['lighting_control'] = lighting_control
	b_props['Occupancy'] = occupancy
	b_props['ActuationEnergy'] = ActuationEnergy  
	
	b_props['glass_solar_transmitance'] = glass_solar_transmitance
	b_props['glass_light_transmitance'] = glass_light_transmitance
	b_props['Lighting_Utilisation_Factor'] = Lighting_Utilisation_Factor
	b_props['Lighting_MaintenanceFactor'] = Lighting_MaintenanceFactor
	b_props['ACH_infl'] = ACH_infl
	b_props['ventilation_efficiency'] = ventilation_efficiency
	b_props['phi_c_max_A_f'] = phi_c_max_A_f
	b_props['phi_h_max_A_f'] = phi_h_max_A_f
	b_props['heatingSystem'] = heatingSystem
	b_props['coolingSystem'] = coolingSystem
	b_props['heatingEfficiency'] = heatingEfficiency
	b_props['coolingEfficiency'] = coolingEfficiency
	return b_props

# j_build_schedules(b_props,paths['Archetypes_schedules'])
# If the set remains the same, the existing scehdules will be sufficient.

#Create dictionaries for Archetypes:
def MakeDicts(b_props):
 
	bp_df = b_props[['Code_x',
						  'El_Wm2',
						  'lighting_control',
						  'U_wall',
						  'U_win',
						  'Ths_set_C',
						  'Tcs_set_C',
						  'ACH',
						  'c_m_A_f',
						  'Qs_Wp',    #[W/p]
						  'Ea_Wm2',    #[W/m2]
						  'glass_solar_transmitance',
						  'glass_light_transmitance',
						  'Lighting_Utilisation_Factor',
						  'Lighting_MaintenanceFactor',
						  'ACH_infl',
						  'ventilation_efficiency',
						  'phi_c_max_A_f',
						  'phi_h_max_A_f',
						  'heatingSystem',
						  'coolingSystem',
						  'heatingEfficiency',
						  'coolingEfficiency']]
	
	bp_df = bp_df.rename(index=str,columns={'Code_x':'Code',
														'El_Wm2':'lighting_load',
														'U_win':'U_w',
														'c_m_A_f':'c_m_A_f',
														'U_wall':'U_em',
														'Ths_set_C':'theta_int_h_set',
														'Tcs_set_C':'theta_int_c_set'})
	bp_df = bp_df.set_index(['Code'])
	BP_dict = bp_df.to_dict(orient='index')

	sd_df = b_props[['Code_x','CoolingSetBackTemp','HeatingSetBackTemp','Occupancy','ActuationEnergy']]
	sd_df = sd_df.set_index(['Code_x'])
	
	SD_dict = sd_df.to_dict(orient='index')       
	return BP_dict, SD_dict
					  
b_props = ArchT_build_df(BuildingData)

BP_dict,SD_dict = MakeDicts(b_props)

######################################

resultsBS = []
resultsYD = []

print BP_dict['GYM1']
print SD_dict['GYM1']

ResultsBuildingSimulation, monthlyData, yearlyData, x_angles = MainCalculateASF(SimulationData, PanelData, BuildingData, BP_dict["GYM1"], SD_dict["GYM1"])


#print yearlyData
"""
for key in BP_dict.iterkeys():
	print key
	ResultsBuildingSimulation, monthlyData, yearlyData, x_angles = MainCalculateASF(SimulationData, PanelData, BP_dict["GYM1"], SD_dict["GYM1"])
	resultsYD.append(yearlyData)



#for BP,SD in itertools.izip(BP_dict,SD_dict):
	print BP[key]
#	ResultsBuildingSimulation, monthlyData, yearlyData, x_angles = MainCalculateASF(SimulationData, PanelData, BD, SD)
	#resultsBS.append(ResultsBuildingSimulation)
#	resultsYD.append(yearlyData)
print resultsBS
print resultsYD
"""