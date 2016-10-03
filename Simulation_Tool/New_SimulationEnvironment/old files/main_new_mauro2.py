# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:14:42 2016

main file for simulation environment

@author: Prageeth Jayathissa
@credits: Jerimias Schmidli
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


## Hier könnte man HOY definieren für die Berechnung:  simulationOption = {'timePeriod' : HOY}          
#simulationOption = {'timePeriod' : '1h'}


# create dictionary to write all paths:
paths = {}


# find path of current folder (simulation_environment)
paths['main'] = os.path.abspath(os.path.dirname(sys.argv[0]))

# define paths of subfolders:
paths['radiation_results'] = paths['main'] + '\\radiation_results'
paths['PV'] = paths['main'] + '\\PV_results'



#radiation subfolder is created, were radiation_results are saved
os.makedirs(paths['radiation_results'])



#Set Solar Panel Properties
#XANGLES=[0,22.5,45,67.5,90]
#YANGLES= [-45,-22.5,0,22.5,45]

XANGLES=[45,67.5]
YANGLES= [0,22.5]

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

print 'Start radiation calculation with ladybug'

#HOY= Hour of the year

for HOY in range(4000,4001):

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


# add python_path to system path, so that all files are available:
sys.path.insert(0, 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\Simulation_Environment\python\aux_files')


from prepareData import prepareMonthlyRadiatonData, importDIVAresults, \
        readLayoutAndCombinations, CalcXYAnglesAndLocation, sum_monthly, changeDIVAresults
        
from auxFunctions import changeMonthlyDataFunction




            
#check if pv results already exist, if not, create them, else load them
#with the radiation_results the Pv_results are calcualted


createPlots = 'True'


if not os.path.isfile(paths['PV'] + '\PV_electricity_results.npy'): 
    if not os.path.isdir(paths['PV']):
        os.makedirs(paths['PV'])
    from asf_electricity_production_mauro_2 import asf_electricity_production
    print 'calculating PV electricity production' 

    if createPlots:
        PV_electricity_results, PV_detailed_results, fig1, fig2 = \
        asf_electricity_production(True, 
                           paths['radiation_results'],
                           400, 0,
                           paths['PV'], 
                           lookup_table_path ='C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\Simulation_Environment\data\python\electrical_simulation', 
                           geo_path = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\Simulation_Environment\data\geographical_location\Zuerich-Kloten',
                           flipOrientation= False, 
                           simulationOption = {'timePeriod' : None},
                           XANGLES = XANGLES, YANGLES= YANGLES, HOY = HOY)
    else:
         pass
    
#        
#    else:
#        PV_electricity_results, PV_detailed_results= \
#        asf_electricity_production(createPlots=createPlots, 
#                                   lb_radiation_path=paths['lb'], 
#                                   panelsize=lbSettings['panelsize'], 
#                                   pvSizeOption=pvSizeOption, 
#                                   save_results_path = paths['PV'],
#                                   lookup_table_path = paths['data'] + '\python\electrical_simulation',
#                                   geo_path=paths['geo'],
#                                   flipOrientation = pvFlipOrientation,
#                                   simulationOption = simulationOption)
else: 
    PV_electricity_results = np.load(paths['PV'] + '\PV_electricity_results.npy').item()
    PV_detailed_results = np.load(paths['PV'] + '\PV_detailed_results.npy').item()
    print 'PV_electricity_results loaded from folder'
    
print "preparing data"            

