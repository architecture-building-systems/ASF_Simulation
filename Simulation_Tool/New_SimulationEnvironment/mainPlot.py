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
import pandas as pd
from buildingSystem import *  
from SimulationClass import ASF_Simulation
import numpy as np
import matplotlib.pyplot as plt


SimulationData = {
'optimizationTypes' : ['E_total'],
'DataFolderName' : 'ZH13_49comb',
'FileName': 'ZH13_49comb',
'geoLocation' : 'Zuerich_Kloten_2013',
'EPWfile': 'Zuerich_Kloten_2013.epw',
'Save' : False,
'ShowFig': False,
'timePeriod': None}

##Set building properties for RC-Model simulator
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
"heatingSystem" : DirectHeater, #DirectHeater, #DirectHeater, #ResistiveHeater #HeatPumpHeater
"coolingSystem" : DirectCooler, #DirectCooler, #DirectCooler, #HeatPumpCooler
"heatingEfficiency" : 1,
"coolingEfficiency" :1,
'COP_H': 1,
'COP_C':1}
#
#
##Set simulation Properties
#SimulationOptions= {
#'setBackTempH' : 4.,
#'setBackTempC' : 4.,
#'Occupancy' : 'Occupancy_COM.csv',
#'ActuationEnergy' : False}

	
if __name__=='__main__':
    ASFtest=ASF_Simulation(SimulationData = SimulationData, BuildingProperties = BuildingProperties)
    ASFtest.SolveASF()
    print ASFtest.yearlyData
    #print ASFtest.ResultsBuildingSimulation['E_total']['BestCombKey']  
    
    



x,y = [],[]
x2,y2 = [],[]
    
x = range(0,8760)
y.append (ASFtest.ResultsBuildingSimulation['E_total']['BestCombKey'])
y = y[0]

for ii in x:
    if y[ii] != 49:
        
        x2.append(ii)
        y2.append(y[ii])

"""        
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x2,y2,'o')

#plt.title('Zurich 2013')

plt.xlabel('Hour of year', fontsize=12)
plt.ylabel('Angle Key', fontsize=12)
plt.tight_layout()


fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.plot(x2, y2, 'm-')
ax1.set_xlabel('Angle degree', fontsize = 16)


plt.legend(['Comb'], loc = 2)

plt.tight_layout()
plt.show()
 
""" 


print ASFtest.ResultsBuildingSimulation['E_total']['OptAngles'][0][0]
print ASFtest.ResultsBuildingSimulation['E_total']['OptAngles'][0][1]

Xangle = []
Yangle = []

for ii in x2:      
    Xangle.append(ASFtest.ResultsBuildingSimulation['E_total']['OptAngles'][ii][0])
    Yangle.append(ASFtest.ResultsBuildingSimulation['E_total']['OptAngles'][ii][1])

"""

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x2,Xangle,'o')

#plt.title('Zurich 2013')

plt.xlabel('Hour of year', fontsize=12)
plt.ylabel('XAngle', fontsize=12)
plt.yticks(range(0,105,15))
plt.xticks(range(0,10000,2000))
plt.tight_layout()



fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x2,Yangle,'o')

#plt.title('Zurich 2013')

plt.xlabel('Hour of year', fontsize=12)
plt.ylabel('YAngle', fontsize=12)
plt.yticks(range(-45,60,15))
plt.xticks(range(0,10000,2000))
plt.tight_layout()

"""

Yangle_Count = {}
Xangle_Count = {}
CombAngle_Count = {}

Yangle_List = []
Xangle_List = []
CombAngle_List = []

sumX = 0
sumY = 0
sumComb = 0

xAngle = range(0,105,15)
yAngle = range(-45,60,15)

CombAngle = y2
Comb = range(49)

for jj in Comb:
    count = 0
    for ii in range(len(x2)):
        if CombAngle[ii] == jj:
            count += 1
    CombAngle_Count[jj] = count
    CombAngle_List.append(count)
    sumComb += count

for jj in yAngle:
    count = 0
    for ii in range(len(x2)):
        if Yangle[ii] == jj:
            count += 1
    Yangle_Count[jj] = count
    Yangle_List.append(count)
    sumY += count
    


for jj in xAngle:
    count = 0
    for ii in range(len(x2)):
        if Xangle[ii] == jj:
            count += 1
    Xangle_Count[jj] = count
    Xangle_List.append(count)
    sumX += count
    
"""
fig = plt.figure()
ax1 = fig.add_subplot(111)

#ax1.set_title('(d) Summer Cooling Optimization', fontsize = 18)

ax1.plot(xAngle, Xangle_List, 'm-')
ax1.plot(yAngle, Yangle_List, 'c-')
ax1.set_xlabel('Angle degree', fontsize = 16)
ax1.set_ylabel('Counts per Year', fontsize = 16)
#ax1.set_yticks([-800,-400,0,400,800])
#ax1.set_xticks(range(6,24,3))

plt.legend(['Xangle', 'Yangle'], loc = 2)


#ax2 = ax1.twinx()
#
#ax2.plot(range(49), CombAngle_List, 'k--')
#
#ax2.set_ylabel('[comb]', fontsize = 16)
#ax2.set_yticks(range(49))
#plt.legend(['Comb'], loc = 3)

plt.tight_layout()
plt.show()
""" 
 
ListComb= []

for x in range(0,105,15):
    for y in range(-45,60,15):
        ListComb.append((x,y))
 
fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.plot(Comb, CombAngle_List, 'k-')
#ax1.set_xticks(ListComb)
ax1.set_xlabel('Combination', fontsize = 16)
ax1.set_ylabel('Counts per Year', fontsize = 16)


#ax1.set_xticks(range(6,24,3))


plt.legend(['Comb'], loc = 2)
plt.tight_layout()
plt.show() 


fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(Comb,CombAngle_List,'o')

#plt.xticks(ListComb)
plt.ylabel('Counts per Year', fontsize=12)
plt.xlabel('Comb', fontsize=12)
plt.tight_layout()


percX = np.array(Xangle_List) /float(sumX) *100
percY = np.array(Yangle_List) /float(sumY) *100
percComb = np.array(CombAngle_List) /float(sumX) *100

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(Comb,percComb,'o')

#plt.title('Zurich 2013')

plt.ylabel('Percentage', fontsize=12)
plt.xlabel('Comb', fontsize=12)
plt.tight_layout()

Comb_df = pd.DataFrame(
    {'CombCounts': CombAngle_List,
     'Combination': ListComb,
     'Percentage': percComb})

#chose what condition a value has to fullfil     
df = Comb_df[Comb_df.Percentage >= 1]

Summe = df.sum()