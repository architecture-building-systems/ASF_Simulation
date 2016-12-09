import pandas as pd
import datetime
import numpy as np
import re as re
import csv
import os,sys

from j_paths import PATHS
from buildingSystem import *  

paths = PATHS()

lighting_ontrol_d ={ #arbitrary, since online sources only provide ranges
"MULTI_RES":250.,
"SINGLE_RES":200.,
"HOTEL":300.,
"OFFICE":350.,
"RETAIL":400.,
"FOODSTORE":400.,
"RESTAURANT":250.,
"INDUSTRIAL":300.,
"SCHOOL":350.,
"HOSPITAL":400.,
"GYM":300.	
}

mean_occupancy_d = { #calculated  from the occupancy files 
"MULTI_RES": 0.014355,
"SINGLE_RES": 0.009570,
"HOTEL": 0.034377,
"OFFICE": 0.009951,
"RETAIL": 0.033507,
"FOODSTORE": 0.055845,
"RESTAURANT": 0.072592,
"INDUSTRIAL": 0.030994,
"SCHOOL": 0.010913,
"HOSPITAL": 0.073750,
"GYM": 0.070977,
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

	b_props['setBackTempC'] = b_props['Tcs_setb_C']-b_props['Tcs_set_C']
	b_props['setBackTempH'] = b_props['Ths_set_C']-b_props['Ths_setb_C']
	
	volume = (BuildingData['room_width']/1000)*(BuildingData['room_depth']/1000)*(BuildingData['room_height']/1000)
	area = (BuildingData['room_width']/1000)*(BuildingData['room_depth']/1000)
	
	b_props['ACH_vent_p'] = b_props['Ve_lps']*3.6/volume
	
	#Assign values for Cm from ISO13790:2008, Table 12, based on archetypes
	th_mass = b_props['th_mass']
	c_m = []
	for i in range(0,len(th_mass)):
		#c_m.append(165.0*10**3) just testing default value
		if th_mass[i] == "T1":
			c_m.append(110.0*10**3) #Light
		elif th_mass[i] == "T2":
			c_m.append(165.0*10**3) #Medium
		elif th_mass[i] == "T3":
			c_m.append(260.0*10**3) #Heavy
	b_props['c_m_A_f'] = pd.DataFrame(c_m)

#declare variables
	occupancy = []
	lighting_control = []
	mean_occupancy = []
#declare constants
	glass_solar_transmitance = []
	glass_light_transmitance = []
	Lighting_Utilisation_Factor = []
	Lighting_MaintenanceFactor = [] 
	ACH_vent = []
	ACH_infl = [] 
	ventilation_efficiency = [] 
	phi_c_max_A_f = [] 
	phi_h_max_A_f = [] 
	heatingSystem = []  
	coolingSystem = [] 
	heatingEfficiency = []  
	coolingEfficiency = [] 
	ActuationEnergy = []   
	COP_H = []
	COP_C = []

	for code in b_props['code1']:
		#variables
		occupancy.append('schedules_occ_%s.csv'%code)
		lighting_control.append(lighting_ontrol_d.get(code))
		mean_occupancy.append(mean_occupancy_d.get(code))
		glass_solar_transmitance.append(0.687)
		glass_light_transmitance.append(0.744)
		Lighting_Utilisation_Factor.append(0.45) 
		Lighting_MaintenanceFactor.append(0.9) 
		ACH_vent.append(1.5)
		ACH_infl.append(0.5) 
		ventilation_efficiency.append(0.6)
		phi_c_max_A_f.append(-np.inf)  
		phi_h_max_A_f.append(np.inf) 
		heatingSystem.append(DirectHeater) #DirectHeater, #ResistiveHeater #HeatPumpHeater
		coolingSystem.append(DirectCooler) #DirectCooler, #HeatPumpCooler
		heatingEfficiency.append(1.0)
		coolingEfficiency.append(1.0)
		ActuationEnergy.append(False)
		COP_H.append(1.0)
		COP_C.append(1.0)
		
	b_props['lighting_control'] = lighting_control
	b_props['mean_occupancy'] = mean_occupancy
	b_props['Qs_Wm2'] = b_props['mean_occupancy']*b_props['Qs_Wp'] # occupancy: p/m2, qs_wp: W/p 
	b_props['Occupancy'] = occupancy
	b_props['ActuationEnergy'] = ActuationEnergy  
	b_props['glass_solar_transmitance'] = glass_solar_transmitance
	b_props['glass_light_transmitance'] = glass_light_transmitance
	b_props['Lighting_Utilisation_Factor'] = Lighting_Utilisation_Factor
	b_props['Lighting_MaintenanceFactor'] = Lighting_MaintenanceFactor
	b_props['ACH_vent'] = ACH_vent
	b_props['ACH_infl'] = ACH_infl
	b_props['ventilation_efficiency'] = ventilation_efficiency
	b_props['phi_c_max_A_f'] = phi_c_max_A_f
	b_props['phi_h_max_A_f'] = phi_h_max_A_f
	b_props['heatingSystem'] = heatingSystem
	b_props['coolingSystem'] = coolingSystem
	b_props['heatingEfficiency'] = heatingEfficiency
	b_props['coolingEfficiency'] = coolingEfficiency
	b_props['COP_H'] = COP_H
	b_props['COP_C'] = COP_C
	return b_props

#Create dictionaries for Archetypes:
def MakeDicts(b_props):
 
	bp_df = b_props[['Code_x',
						  'El_Wm2',
						  'lighting_control',
						  'U_wall',
						  'U_win',
						  'Ths_set_C',
						  'Tcs_set_C',
						  'c_m_A_f',
						  'Qs_Wp',    #Sensible heat gain due to occupancy [W/p]
						  'Ea_Wm2',    #Maximum electrical consumption due to appliances per unit of gross floor area [W/m2]
						  'glass_solar_transmitance',
						  'glass_light_transmitance',
						  'Lighting_Utilisation_Factor',
						  'Lighting_MaintenanceFactor',
						  'ACH_vent',
						  'ACH_infl',
						  'ventilation_efficiency',
						  'phi_c_max_A_f',
						  'phi_h_max_A_f',
						  'heatingSystem',
						  'coolingSystem',
						  'heatingEfficiency',
						  'coolingEfficiency',
						  'COP_H',
						  'COP_C']]
	
	bp_df = bp_df.rename(index=str,columns={'Code_x':'Code',
														'El_Wm2':'lighting_load',
														'U_win':'U_w',
														'c_m_A_f':'c_m_A_f',
														'U_wall':'U_em',
														'Ths_set_C':'theta_int_h_set',
														'Tcs_set_C':'theta_int_c_set',
														})
	bp_df = bp_df.set_index(['Code'])
	BP_dict = bp_df.to_dict(orient='index')

	so_df = b_props[['Code_x','setBackTempC','setBackTempH','Occupancy','ActuationEnergy']]
	so_df = so_df.set_index(['Code_x'])
	
	SO_dict = so_df.to_dict(orient='index')       
	return BP_dict, SO_dict
	
def sort_dicts(to_sort,sorted):
	newdict = {}
	for key in sorted:
		newdict[key] = to_sort[key]
	return newdict

##test
BuildingData={
	"room_width": 4900,     
	"room_height":3100,
	"room_depth":7000,
	"glazing_percentage_w": 0.92,
	"glazing_percentage_h": 0.97}

b_data = ArchT_build_df(BuildingData).Qs_Wm2
print b_data