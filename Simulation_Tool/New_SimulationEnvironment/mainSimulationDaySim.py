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
from SimulationClassDaySim import ASF_Simulation

Analysis = {
'DaySimSunnySommer_6_7' : 4465 - 4485, #Temp_start = 22
'DaySimSunnyWinter_8_1' :  170 -  190 #Temp_start = 18
}


SimulationData = {
'optimizationTypes' : ['E_total', 'Cooling', 'Heating', 'Lighting', 'SolarEnergy', 'E_HCL'],
'DataFolderName' : 'DaySimZH13Year', #'DaySimSunnyWinter_8_1', #DaySim9comb', 
'FileName': 'DaySimZH13Year', #'DaySimSunnyWinter_8_1', #'DaySim9comb',
'Save' : True,
'ShowFig': True,

'Temp_start' : 18,
'start' : 0,
'end': 8760} #8760

PanelData = {
"XANGLES": [0,15,30,45,60,75,90],#[0,45],
"YANGLES" : [-45,-30,-15,0,15,30,45]}

BuildingProperties = {
"glass_solar_transmitance" : 0.687,
"glass_light_transmitance" : 0.744,
"lighting_load" : 11.74,
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
"heatingSystem" : DirectHeater,
"coolingSystem" : DirectCooler, 
"heatingEfficiency" : 1,
"coolingEfficiency" :1,
"COP_H": 3, 
"COP_C":3}

	
if __name__=='__main__':
    ASFtest=ASF_Simulation(SimulationData = SimulationData, PanelData = PanelData, BuildingProperties = BuildingProperties)
    ASFtest.SolveASF()
    #yearlyData = ASFtest.yearlyData
    results = ASFtest.ResultsBuildingSimulation
    rad = ASFtest.radiation
    
    #print yearlyData 
 
"""
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


df = results['E_total']
df1 = df['PV']
df2 = rad['dirnorrad_Whm2'][SimulationData['start']:SimulationData['end']]
df3 = rad['difhorrad_Whm2'][SimulationData['start']:SimulationData['end']]
df4 = rad['glohorrad_Whm2'][SimulationData['start']:SimulationData['end']]

test = plt.figure().gca(projection='3d')
test.scatter(df.index, df['PV'], df2)
test.set_xlabel('Index')
test.set_ylabel('PV')
test.set_zlabel('directRad')
plt.show() 

#
#test = plt.figure().gca(projection='3d')
#test.scatter(df.index, df3, df2, color='k')
#test.set_xlabel('Index')
#test.set_ylabel('diffuseRad')
#test.set_zlabel('directRad')
#plt.show() 

test = plt.figure().gca(projection='3d')
test.scatter(df['PV'], df3, df2, color='r')
test.set_xlabel('PV')
test.set_ylabel('diffuseRad')
test.set_zlabel('directRad')
plt.show() 

test = plt.figure().gca(projection='3d')
test.scatter(df.index, df4, df1, color='m')
test.set_xlabel('index')
test.set_ylabel('gloRad')
test.set_zlabel('PV')
plt.show() 
"""