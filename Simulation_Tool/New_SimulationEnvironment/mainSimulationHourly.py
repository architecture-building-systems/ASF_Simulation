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
- Open the main_new_mauro.GH file in Grasshopper
- Set the location in the Grasshopper file to same Location as defined in geoLoaction in this script
- Set both red framed boolean toggles to true 
- Set all needed values for evaluation at the beginning of the main.py script

if LadyBug once has calculated all the radiation data, they will be stored in the folder with the corresponding DataName. 
Also the Data of the PV producation and radiation hitting the window will be saved and can be loaded again, with the same DataName.


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




import numpy as np
import pandas as pd
from buildingSystem import *  
from SimulationClassHourly import ASF_Simulation

#
#SimulationPeriod = {
#'FromMonth': 7,
#'ToMonth': 7,
#'FromDay': 6,
#'ToDay': 6, 
#'FromHour': 5,
#'ToHour': 20}


##Set simulation data 
#SimulationData= {
#'optimizationTypes' : ['E_total', 'Cooling'], 
#'DataFolderName' : 'ZH13_49comb_Notcloudy_6_7', 
#'FileName' : 'ZH13_49comb_Notcloudy_6_7',
#'geoLocation' : 'Zuerich_Kloten_2013', 
#'EPWfile': 'Zuerich_Kloten_2013.epw',
#'Save' : True, 
#'ShowFig': True, 
#'timePeriod': None} # asf_electricity_function  
    
SimulationPeriod = {
'FromMonth': 1, #7, #1,
'ToMonth': 1,#7, #1,
'FromDay': 8, #6, #8,
'ToDay': 8, #8,
'FromHour': 6,#5
'ToHour': 18}#20
#
#
#Set simulation data 
SimulationData= {
'optimizationTypes' : ['E_total'], 
'DataFolderName' : 'ZH13_49comb_WinterSunnyDay', 
'FileName' : 'ZH13_49comb_WinterSunnyDayNew7',
'geoLocation' : 'Zuerich_Kloten_2013', 
'EPWfile': 'Zuerich_Kloten_2013.epw',
'Save' : True, 
'ShowFig': False, 
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
"BuildingOrientation" : 0} #building orientation of 0 corresponds to south facing, 90 is east facing, -90 is west facing


BuildingProperties={
"glass_solar_transmitance" : 0.691 ,
"glass_light_transmitance" : 0.744 ,
"lighting_load" : 11.74 ,
"lighting_control" : 300,
"Lighting_Utilisation_Factor" :  0.45, # 0.75
"Lighting_MaintenanceFactor" : 0.9,
"U_em" : 0.2, 
"U_w" : 1.1,
"ACH_vent" : 1.5,
"ACH_infl" : 0.5,
"ventilation_efficiency" : 0.6,
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
'ActuationEnergy' : False,
'Temp_start' : 18,
'human_heat_emission' : 0.12} #[kWh] heat emitted by a human body per hour. Source: HVAC Engineers Handbook, F. Porges
   
if __name__=='__main__':
    
    ASFtest = ASF_Simulation(SimulationPeriod = SimulationPeriod, 
                             SimulationData = SimulationData, 
                             PanelData = PanelData,
                             BuildingData = BuildingData,
                             BuildingProperties = BuildingProperties, 
                             SimulationOptions = SimulationOptions)
    ASFtest.SolveASF()
    print ASFtest.TotalHourlyData
        
        
