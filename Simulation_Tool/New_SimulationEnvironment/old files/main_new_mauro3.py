# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:14:42 2016

main file for simulation environment

@author: Prageeth Jayathissa
@credits: Jerimias Schmidli

21.09.2016
"""

import os, sys
import numpy as np
import json
import time
import warnings
import csv


# specify the location used for the analysis ‐ this name must be the same as a
# folder in the directory .../ASF_Simulation/Simulation_Environment/data/geographica
# new locations can be added with the grasshopper main script for any .epw weather
geoLocation = 'Zuerich‐Kloten'

# Time: Which our of the year should be evaluated?
hour_of_year = 4000 # 0? to 8760 hour



## Hier könnte man HOY definieren für die Berechnung:  simulationOption = {'timePeriod' : HOY}          
#simulationOption = {'timePeriod' : '1h'}


# create dictionary to write all paths:
paths = {}


# find path of current folder (simulation_environment)
paths['main'] = os.path.abspath(os.path.dirname(sys.argv[0]))


# define paths of subfolders:
paths['data'] = paths['main'] + '\\data'
paths['python'] = paths['main'] + '\\python'

paths['radiation_results'] = paths['main'] + '\\radiation_results'
paths['PV'] = paths['main'] + '\\PV_results'

# define path of geographical location:
paths['geo'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\data\geographical_location\Zuerich-Kloten' 


#paths['electrical'] = os.path.join(( paths['data'] + "\python\electrical_simulation"), radiation_folder)



#radiation subfolder is created, there the radiation_results are saved

if not os.path.isdir(paths['radiation_results']):
        os.makedirs(paths['radiation_results'])


# add python_path to system path, so that all files are available:
sys.path.insert(0, paths['python'] + '\\aux_files')

    

# create sun data based on grasshopper file
#execfile(paths['python'] + "\\aux_files\\SunAngles_Tracking_and_temperature.py")

# calculate and save lookup table if it does not yet exist:
if not os.path.isfile(paths['data'] + '\python\electrical_simulation\curr_model_submod_lookup.npy'): 
    if not os.path.isdir(paths['data'] + '\python\electrical_simulation'):
        os.makedirs(paths['data'] + '\python\electrical_simulation')
    execfile(paths['python'] + '\\aux_files\\create_lookup_table.py')
else:
    print 'lookup table not created as it already exists'


#Option for integration of the actuation energy consumption, 'yes' = energy consumption is included
#Actuation = 'Yes' # 'No'



#Set Solar Panel Properties
#XANGLES=[0,22.5,45,67.5,90]
#YANGLES= [-45,-22.5,0,22.5,45]

XANGLES=[22.5,67.5]
YANGLES= [-22.5,22.5]

panel_data={"XANGLES": XANGLES ,
"YANGLES" : YANGLES,
"NoClusters":1,
"numberHorizontal":6,
"numberVertical":9,
"panelOffset":400,
"panelSize":400,
"panelSpacing":500,
}

#Set Building Parameters
building_data={"room_width":4900,
               
"room_height":3100,
"glazing_percentage_w":0.92,
"glazing_percentage_h":0.97,
}



#Save parameters to be imported into grasshopper
with open('panel.json','w') as f:
    f.write(json.dumps(panel_data))

with open('building.json','w') as f:
    f.write(json.dumps(building_data))


waitfile=True
resultsdetected=0

print '\nStart radiation calculation with ladybug'

for HOY in range(hour_of_year, hour_of_year + 1):

#for HOY in range(0,8760):

    for x_angle in XANGLES:
        for y_angle in YANGLES:
            
            comb_data={"x_angle":x_angle,
                       "y_angle":y_angle,
                       "HOY":HOY}
                       
            #create json file with the set combination of x-angle,y-angle and HOY
            with open('comb.json','w') as f:
                f.write(json.dumps(comb_data))
                
                print HOY, x_angle, y_angle, resultsdetected              
                                           
                
                
            #Wait until the radiation_results were created    
            while not os.path.exists(paths['radiation_results']+'\\RadiationResults' + '_' + str(HOY) + '_' + str(x_angle) + '_' + str(y_angle)+ '.csv'):
                time.sleep(2)
            else:
                print 'next step'
                resultsdetected += 1

print 'radiation calculation finished!'


# add python_path to system path, so that all files are available: nötig??
#sys.path.insert(0, 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\Simulation_Environment\python\aux_files')


from prepareData import prepareMonthlyRadiatonData, readLayoutAndCombinations, CalcXYAnglesAndLocation, sum_monthly
#        
#from auxFunctions import changeMonthlyDataFunction

""" nötig?

# load sunTrackingData used for the LadyBug simulation:
with open(paths['geo'] + '\SunTrackingData.json', 'r') as fp:
        SunTrackingData = json.load(fp)
        fp.close()
        
        
lbSettings= {}
        
# find the number of hours analysed by ladybug:
lbSettings['numHoursLB'] = np.shape(SunTrackingData['HOY'])[0]
    
# find the number of combinations analysed by ladybug:
lbSettings['numCombLB'] = len(CalcXYAnglesAndLocation(readLayoutAndCombinations(paths['lb']))['allAngles'][0])        

"""


            
#check if pv results already exist, if not, create them, else load them
#with the radiation_results the Pv_results are calcualted

createPlots = 'True'
simulationOption = {'timePeriod' : None}

""" 
For evalation period, which is greater than only 1 hour

PV_electricity_results = {}
PV_detailed_ results = {}



for HOY in range(start,end)

    if createPlots:
            PV_electricity_results[HOY], PV_detailed_results[HOY], fig1, fig2 = \
            asf_electricity_production(
    ....
    {HOY : PV_electricity_results}    
    
"""


if not os.path.isfile(paths['PV'] + '\PV_electricity_results.npy'): 
    if not os.path.isdir(paths['PV']):
        os.makedirs(paths['PV'])
    from asf_electricity_production_mauro_2 import asf_electricity_production
    print '\ncalculating PV electricity production' 

    if createPlots:
        PV_electricity_results, PV_detailed_results, fig1, fig2 = \
        asf_electricity_production(
                           createPlots = createPlots, 
                           lb_radiation_path = paths['radiation_results'],
                           panelsize = 400, 
                           pvSizeOption = 0,
                           save_results_path = paths['PV'], 
                           lookup_table_path = paths['data'] + '\python\electrical_simulation', 
                           geo_path = paths['geo'],
                           flipOrientation= False, 
                           simulationOption = {'timePeriod' : None},
                           XANGLES = XANGLES, YANGLES= YANGLES, HOY = HOY)
                           
    else:
        PV_electricity_results, PV_detailed_results = \
        asf_electricity_production(
                           createPlots = createPlots, 
                           lb_radiation_path = paths['radiation_results'],
                           panelsize = 400, 
                           pvSizeOption = 0,
                           save_results_path = paths['PV'], 
                           lookup_table_path = paths['data'] + '\python\electrical_simulation', 
                           geo_path = paths['geo'],
                           flipOrientation= False, 
                           simulationOption = {'timePeriod' : None},
                           XANGLES = XANGLES, YANGLES= YANGLES, HOY = HOY)

else: 
    PV_electricity_results = np.load(paths['PV'] + '\PV_electricity_results.npy').item()
    PV_detailed_results = np.load(paths['PV'] + '\PV_detailed_results.npy').item()
    print 'PV_electricity_results loaded from folder'
    
print "\npreparing data\n"  


PV_sum = PV_electricity_results['Pmpp_sum']
Rad_sum = PV_electricity_results['Ins_sum']

PV_results_HOY= {}
RadiationBuilding_HOY = {}
 
i = 0
   
for ii in PV_sum:
    
    PV_results_HOY[i]=ii
    i += 1
    
print PV_results_HOY

j = 0

for jj in Rad_sum:
    
    RadiationBuilding_HOY[j] = jj - PV_results_HOY[j]
    j += 1

print RadiationBuilding_HOY




"""

not needed

# create dictionary to save monthly data:
monthlyData = {}

# prepare monthly PV and Radiation data and write it to the monthlyData dictionary:

monthlyData['efficiencies'] = {}
monthlyData['PV'], monthlyData['R'], monthlyData['efficiencies']['PV'],  monthlyData['R_avg'],\
monthlyData['R_theo'], monthlyData['PV_avg'], monthlyData['PV_eff'] \
                                        = prepareMonthlyRadiatonData(PV_electricity_results, simulationOption)
                                        
"""
                                        
## create dicitionary to save hourly data:
#hourlyData = {}
#
#hourlyData['efficiencies'] = {}
#hourlyData['PV'] = 
#hourlyData['R'] = 
#hourlyData['efficiencies']['PV'] = 
#hourlyData['R_avg'] = 
#hourlyData['R_theo'] = 
#hourlyData['PV_avg'] = 
#hourlyData['PV_eff'] = 
                                        
                                        
                                        
                                        
                                        
""" radiation energy, which enters the building (not absorbed by the PV panels) has to be transfered to
the building simulation

- dependend on the amount of angle combinations, H,C,L values are going to be calcualted (maybe only for relevant hour)
- H,C,L values will be returned and the PV energy production is going to be subtracted
- the lowest overall energy demand will be determined and angle combination for specific HOY returned

                                         
                                        
                                        
# add python_path to system path, so that all files are available:
sys.path.insert(0, 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\RC_BuildingSimulator-master\simulator')                                        
                                        
# calcualte Building Simulation (RC Model) and save H,C,L and uncomfortable hours
                                        
from main_RC_model import main_RC_model                                        
                                        
                                        
Data_T_in, Data_Heating, Data_Cooling, Data_Lighting = main_RC_model()

# create dicitionary to save relevant hourly data:
# max PV power production value has to be used

hourlyData = {}

#if Actuation:
#    hourlyData['Actuation'] = XY
#else:
#    hourlyData['Actuation'] = 0



hourlyData['PV'] = 0
hourlyData['H'] = Data_Heating[hour_of_year]
hourlyData['C'] = Data_Cooling[hour_of_year]
hourlyData['L'] = Data_Lighting[hour_of_year]
hourlyData['E_HCL'] = hourlyData['H'] + hourlyData['C'] + hourlyData['L']

#Add PV production to the energy demand of H,C,L, total energy demand at hour_of_year

hourlyData['E_tot'] = hourlyData['E_HCL'] - hourlyData['PV'] + hourlyData['Actuation']

"""          

