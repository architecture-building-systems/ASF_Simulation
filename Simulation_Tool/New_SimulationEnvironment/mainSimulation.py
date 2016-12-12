"""
=========================================
main file for simulation environment
=========================================
"""


"""
@author: Mauro Luzzatto 
@credits: Prageeth Jayathissa, Jerimias Schmidli

02.11.2016
"""


"""
Description of the code 


HOW TO USE:
- Open the main_new.GH file in Grasshopper
- Set both red framed boolean toggles to true 
- Set all needed values for evaluation at the beginning of the main.py script
- start simulation, for a new loaction an error with ..SunPosition.csv not found, just wait 1 min for GH to create it, then start simulation again
- after all radiation files are calculated (radiaion_results and radtion_wall) - the number should be equal comb*hour_in_month - close GH to avoid interaction with it 

if LadyBug once has calculated all the radiation data, they will be stored in the folder with the corresponding DataName. 
Also the Data of the PV producation and radiation hitting the window will be saved and can be loaded again, with the same DataName.

- Calculation without the ASF, set XANGLES and YANGLES equal [0], set numberHorizontal and numberVertical to 0 in the PanelData settings


VARIABLE DEFINITION

   geoLocation: set the location which should be evaluated, make sure the correspoding .epw file is saved in the WeatherData folder
   Save: decide weather you want to save (True) or not save (False) the results
   optimization_Types: Decide for which energy demand type, you want to do the optimisation for
   DataName: choose the name for the stored data
   XANGLES = set the X-Angles of the ASF = [0, 15, 30, 45, 60, 75, 90] , 0 = closed, 90 = open
   YANGLES = set the Y-Angles of the ASF = [-45, -30,-15,0, 15, 30, 45] 
   NoClusters = option for using different multiple clusters
   ActuationEnergy = choose weather you want to include the the needed actuation energy for the ASF adjustment
   room_width =     
   room_height =
   room_depth = 
   glazing_percentage_w = perecentage of glazing of the total room width
   glazing_percentage_h =  perecentage of glazing of the total room height


	
INPUT PARAMETER DEFINITION 

	Fenst_A: Area of the Glazed Surface  [m2]
	Room_Depth=7.0 Depth of the modeled room [m]
	Room_Width=4.9 Width of the modeled room [m]
	Room_Height=3.1 Height of the modeled room [m]
	glass_solar_transmitance: Fraction of Radiation transmitting through the window []
	glass_light_transmitance: Fraction of visible light (luminance) transmitting through the window []
	lighting_load: Lighting Load [W/m2] 
	lighting_control: Lux threshold at which the lights turn on [Lx]
	U_em: U value of opaque surfaces  [W/m2K]
	U_w: U value of glazed surfaces [W/m2K]
	ACH_vent: Air changes per hour through ventilation [Air Changes Per Hour]
	ACH_infl: Air changes per hour through infiltration [Air Changes Per Hour]
	ventilation_efficiency: The efficiency of the heat recovery system for ventilation. Set to 0 if there is no heat recovery []
	c_m_A_f: Thermal capacitance of the room per floor area [J/m2K] #capcitance of the building dependent on building type: medium = 165'000, heavy = 260'000, light = 110'000, very heavy = 370'000
	theta_int_h_set : Thermal heating set point [C]
	theta_int_c_set: Thermal cooling set point [C]
	phi_c_max_A_f: Maximum cooling load. Set to -np.inf for unresctricted cooling [C]
	phi_h_max_A_f: Maximum heating load. Set to no.inf for unrestricted heating [C]

"""



import os, sys
import numpy as np
import pandas as pd
from buildingSystem import *  
from SimulationClass import ASF_Simulation


SimulationData = {
'optimizationTypes' : ['E_total', 'Lighting','SolarEnergy','Heating', 'Cooling', 'E_HCL'],
'DataFolderName' : 'ZH13_49combHorizont',
'FileName': 'ZH13_49combMitHorizont',
'geoLocation' : 'Zuerich_Kloten_2013',
'EPWfile': 'Zuerich_Kloten_2013.epw',
'Save' : True,
'ShowFig': True,
'timePeriod': None}

#SimulationData = {
#'optimizationTypes' : ['E_total'],
#'DataFolderName' : 'ZH05_49comb',
#'FileName': 'ZH05_49comb',
#'geoLocation' : 'Zuerich_Kloten_2005',
#'EPWfile': 'Zuerich_Kloten_2005.epw',
#'Save' : True,
#'ShowFig': True,
#'timePeriod': None}


##Set building properties for RC-Model simulator
BuildingProperties={
"glass_solar_transmitance" : 0.691 ,
"glass_light_transmitance" : 0.744 ,
"lighting_load" : 11.74 ,
"lighting_control" : 300,
"Lighting_Utilisation_Factor" :  0.64,
"Lighting_MaintenanceFactor" : 1,
"U_em" : 0.277, 
"U_w" : 1.71,
"ACH_vent" : 1.5,
"ACH_infl" : 0.5,
"ventilation_efficiency" : 0.6 ,#0.6
"c_m_A_f" : 165 * 10**3,
"theta_int_h_set" : 22,
"theta_int_c_set" : 26,
"phi_c_max_A_f": -np.inf,
"phi_h_max_A_f":np.inf,
"heatingSystem" : DirectHeater, #DirectHeater, #DirectHeater, #ResistiveHeater #HeatPumpHeater
"coolingSystem" : DirectCooler, #DirectCooler, #DirectCooler, #HeatPumpCooler
"heatingEfficiency" : 1,
"coolingEfficiency" :1,
'COP_H': 3,
'COP_C':3}

#
#Set simulation Properties
SimulationOptions= {
'setBackTempH' : 4.,
'setBackTempC' : 4.,
'Occupancy' : 'Occupancy_COM.csv',
'ActuationEnergy' : False}

	
if __name__=='__main__':
    ASFtest=ASF_Simulation(SimulationData = SimulationData, BuildingProperties = BuildingProperties, SimulationOptions = SimulationOptions)
    ASFtest.SolveASF()
    print ASFtest.yearlyData
    
 
