%matplotlib inline
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
import cdecimal as dec
import re as re
import csv
import os, sys
from buildingSystem import *  
from mainSimulation import MainCalculateASF


weather_path = 'C:\Users\Zghiru\Documents\GitHub\RC_BuildingSimulator\Justin_Semseter_Project\data\Zurich-Kloten_2013.epw'
occupancy_path = 'C:\Users\Zghiru\Documents\GitHub\RC_BuildingSimulator\Justin_Semseter_Project\data\Occupancy_COM.csv'
radiation_path = r'C:\Users\Zghiru\Documents\GitHub\RC_BuildingSimulator\Justin_Semseter_Project\data\radiation_Building_Zh.csv'
archetypes_properties_path = "C:\Users\Zghiru\Documents\GitHub\RC_BuildingSimulator\Justin_Semseter_Project\data\CH\Archetypes\Archetypes_properties.xlsx"
archetypes_schedules_path = "C:\Users\Zghiru\Documents\GitHub\RC_BuildingSimulator\Justin_Semseter_Project\data\CH\Archetypes\Archetypes_schedules.xlsx"
occ_path = 'C:\Users\Zghiru\Documents\GitHub\RC_BuildingSimulator\Justin_Semseter_Project\schedules_occ.csv'

##Constants

SimulationData= {
'optimizationTypes' : ['E_total', 'E_total_elec'], #'Heating','Cooling', 'E_HCL', 'Heating_elec','Cooling_elec', 'E_HCL_elec', 'SolarEnergy', 'Lighting'],
'DataName' : 'ZH05_49comb',#'ZH13_49comb', #'ZH05_49comb', #,
'geoLocation' : 'Zuerich_Kloten_2005', #'Zuerich_Kloten_2013', #'Zuerich_Kloten_2005',
'Save' : True}

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

##
#to replace:
BuildingProperties={
"glass_solar_transmitance" : 0.687 ,
"glass_light_transmitance" : 0.744 ,
"lighting_load" : 11.74 ,
"lighting_control" : 300,
"Lighting_Utilisation_Factor" :  0.45,
"Lighting_MaintenanceFactor" : 0.9,
"U_em" : 0.2, 
"U_w" : 1.2,
"ACH_vent" : 1.5,
"ACH_infl" :0.5,
"ventilation_efficiency" : 0.6 ,
"c_m_A_f" : 165 * 10**3,
"theta_int_h_set" : 20,
"theta_int_c_set" : 26,
"phi_c_max_A_f": -np.inf,
"phi_h_max_A_f":np.inf,
"heatingSystem" : DirectHeater, #DirectHeater, #ResistiveHeater #HeatPumpHeater
"coolingSystem" : DirectCooler, #DirectCooler, #HeatPumpCooler
"heatingEfficiency" : 1,
"coolingEfficiency" :1,
}

#Set DEFAULTsimulation Properties
SimulationOptions= {
'setBackTemp' : 4.,
'Occupancy' : 'Occupancy_COM.csv',
'ActuationEnergy' : False}

######################################


def organiselist():
	pass


for ii in dictionarz:
	 ResultsBuildingSimulation, monthlyData, yearlyData, x_angles = MainCalculateASF(SimulationData, PanelData, BuildingData, ii, jj)

