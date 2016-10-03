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


# create dictionary to write all paths:
paths = {}

radiation_results = {}


# find path of current folder (simulation_environment)
paths['main'] = os.path.abspath(os.path.dirname(sys.argv[0]))

# define paths of subfolders:
paths['radiation_results'] = paths['main'] + '\\radiation_results'

#radiation subfolder is created, were radiation_results are saved
os.makedirs(paths['radiation_results'])



#Set Solar Panel Properties
XANGLES=[0,22.5,45,67.5,90]
YANGLES= [-45,-22.5,0,22.5,45]

#XANGLES=[45,67.5]
#YANGLES= [0,22.5,45]

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

#HOY= Hour of the year

for HOY in range(408,409):

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

print 'calculation finished!'
            
            


#with open('radiation_resultsRadiationResults.csv', 'r') as csv_radiation:
#                        radiation_results = csv.reader(csv_radiation)
#                        for row in radiation_results:
#                            print row
                
