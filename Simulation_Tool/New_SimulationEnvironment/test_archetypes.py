%matplotlib inline
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
import cdecimal as dec
import re as re
import itertools
import csv
import os, sys
from buildingSystem import *  
from mainSimulation import MainCalculateASF
import j_epw_import_tools as epw_tools


#weather_path = 'C:\Users\Zghiru\Documents\GitHub\RC_BuildingSimulator\Justin_Semseter_Project\data\Zurich-Kloten_2013.epw'
#occupancy_path = 'C:\Users\Zghiru\Documents\GitHub\RC_BuildingSimulator\Justin_Semseter_Project\data\Occupancy_COM.csv'
#radiation_path = r'C:\Users\Zghiru\Documents\GitHub\RC_BuildingSimulator\Justin_Semseter_Project\data\radiation_Building_Zh.csv'
archetypes_properties_path = "C:\Users\Zghiru\Documents\GitHub\RC_BuildingSimulator\Justin_Semseter_Project\data\CH\Archetypes\Archetypes_properties.xlsx"
archetypes_schedules_path = "C:\Users\Zghiru\Documents\GitHub\RC_BuildingSimulator\Justin_Semseter_Project\data\CH\Archetypes\Archetypes_schedules.xlsx"
occ_path = 'C:\Users\Zghiru\Documents\GitHub\RC_BuildingSimulator\Justin_Semseter_Project\schedules_occ.csv'

##Constants

SimulationData= {
'optimizationTypes' : ['E_total', 'E_total_elec'], #'Heating','Cooling', 'E_HCL', 'Heating_elec','Cooling_elec', 'E_HCL_elec', 'SolarEnergy', 'Lighting'],
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
#to replace:
#Set DEFAULTsimulation Properties

BuildingProperties={
"glass_solar_transmitance" : 0.687 , 
"glass_light_transmitance" : 0.744 ,
#"lighting_load" : 11.74 , 
"lighting_control" : 300,
"Lighting_Utilisation_Factor" :  0.45,
"Lighting_MaintenanceFactor" : 0.9,
#"U_em" : 0.2, 
#"U_w" : 1.2,
#"ACH_vent" : 1.5,
"ACH_infl" :0.5,
"ventilation_efficiency" : 0.6 ,
#"c_m_A_f" : 165 * 10**3,
#"theta_int_h_set" : 20,
#"theta_int_c_set" : 26,
"phi_c_max_A_f": -np.inf,
"phi_h_max_A_f":np.inf,
"heatingSystem" : DirectHeater, #DirectHeater, #ResistiveHeater #HeatPumpHeater
"coolingSystem" : DirectCooler, #DirectCooler, #HeatPumpCooler
"heatingEfficiency" : 1,
"coolingEfficiency" :1,
}
#Arbitrary estimates based on ranges in https://www.archtoolbox.com/materials-systems/electrical/recommended-lighting-levels-in-buildings.html
lighting_ontrol_d ={
"MULTI_RES":250
"SINGLE_RES":200
"HOTEL":300
"OFFICE":350
"RETAIL":400
"FOODSTORE":400
"RESTAURANT":250
"INDUSTRIAL":300
"SCHOOL":350
"HOSPITAL":400
"GYM":300
}

SimulationOptions= {
'setBackTemp' : 4.,
'Occupancy' : 'Occupancy_COM.csv',
'ActuationEnergy' : False}




#ArchT_df = ArchT_build_df(BuildingData)
#ArchT_dict = At_Dict_Building_properties(ArchT_df)
#ArchT_typologies = ArchT_df.code1.unique()

def ArchT_build_df(BuildingData):
    arch = pd.read_excel(archetypes_properties_path,sheetname='THERMAL')
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
    
    int_loads = pd.read_excel(archetypes_properties_path,sheetname='INTERNAL_LOADS')
    int_loads = int_loads.set_index(['Code'])
    int_loads = int_loads[['Qs_Wp','Ea_Wm2','El_Wm2']]
    int_loads = int_loads.reset_index(drop=False)

    T_sp = pd.read_excel(archetypes_properties_path,sheetname='INDOOR_COMFORT')

    b_data = arch.merge(int_loads,how='left', left_on='code1', right_on='Code')
    b_data = b_data.merge(T_sp,how='left', left_on='code1', right_on='Code')
    b_data = b_data.drop('Code_y',axis=1)
    b_data = b_data.drop('Code',axis=1)
    b_data['Tcs_setb'] = b_data['Tcs_setb_C']-b_data['Tcs_set_C']
    b_data['Ths_setb'] = b_data['Ths_set_C']-b_data['Ths_setb_C']
    b_data['lighting_control']
    b_data['Ths_setb']
    b_data['Ths_setb']
    
    volume = (BuildingData['room_width']/1000)*(BuildingData['room_depth']/1000)*(BuildingData['room_height']/1000)
    area = (BuildingData['room_width']/1000)*(BuildingData['room_depth']/1000)
    people = 
    b_data['ACH'] = b_data['Ve_lps']*3.6/volume*(occupancy*area)
    
    #Assign values for Cm from ISO13790:2008, Table 12, based on archetypes
    th_mass = b_data['th_mass']
    c_m = []
    for i in range(0,len(th_mass)):
        if th_mass[i] == "T1":
            c_m.append(110*10**3) #Light
        elif th_mass[i] == "T2":
            c_m.append(165 * 10**3) #Medium
        elif th_mass[i] == "T3":
            c_m.append(260*10**3) #Heavy
    b_data['c_m_A_f'] = pd.DataFrame(c_m)
    return b_data


#Create dictionaries for Archetypes:
def At_Dict_Building_properties(b_data):
 
    bp_df = b_data[['Code_x',
                          'El_Wm2',
                          'U_wall',
                          'U_win',
                          'Ths_set_C',
                          'Ths_setb',
                          'Tcs_set_C',
                          'ACH',
                          'c_m_A_f'
                          'Qs_Wp',    #[W/p]
                          'Ea_Wm2']]  #[W/m2]
    
    bp_df = bp_df.rename(index=str,columns={'Code_x':'Code',
                                                        'El_Wm2':'lighting_load',
                                                        'U_win':'U_w',
                                                        'c_m_A_f':'c_m_A_f',
                                                        'U_wall':'U_em',
                                                        'Ths_set_C':'theta_int_h_set',
                                                        'Tcs_set_C':'theta_int_c_set'})
    bp_df = b_data_dict.set_index(['Code'])
    BP_dict = b_data_dict.to_dict(orient='index')
    occupancy = get_occ(occ,b_data)
    SD_dict = b_data[['Tcs_setb','Ths_setb','code1']]
    return bp_dict, s_data 

occ = epw_tools.occupancy(occupancy_path)
def get_occ(occ,AD):
    occ_code = AD['code1']
    building_occ = [] #list of occupancy profiles for each case, to be appended to Simulation_Options
    for i in occ_code:
        building_occ.append(occ[i])
    return building_occ

######################################
BP_dict,SD_dict = At_Dict_Building_properties(b_data)

for BP,SD in itertools.izip(BP_dict,SD_dict):
	 ResultsBuildingSimulation, monthlyData, yearlyData, x_angles = MainCalculateASF(SimulationData, PanelData, BD, SD)

