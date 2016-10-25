# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 16:58:45 2016

@author: Assistenz
"""
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:14:42 2016

main file for simulation environment

@author: Mauro Luzzatto 
@credits: Prageeth Jayathissa, Jerimias Schmidli

25.10.2016

Illuminance

"""

import os, sys
import numpy as np
import json
import time
import warnings
import csv
import matplotlib.pyplot as plt
import csv
import pandas as pd

# get current time
now = time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
print "simulation start: " + now

geoLocation = 'Zuerich_Kloten_2013'

# create dictionary to write all paths:
paths = {}

# find path of current folder (simulation_environment)
paths['main'] = os.path.abspath(os.path.dirname(sys.argv[0]))

# define paths of subfolders:
paths['data'] = paths['main'] + '\\data'
paths['python'] = paths['main'] + '\\python'



# define path of weather file:
paths['weather'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\WeatherData\Zuerich-Kloten_2005.epw' #paths['epw_name']

# add python_path to system path, so that all files are available:
sys.path.insert(0, paths['python'] + '\\aux_files')
sys.path.insert(0, paths['python'])

from epwreader import epw_reader
#read epw file of needed destination
weatherData = epw_reader(paths['weather'])


# define path of geographical location:
paths['geo'] = os.path.join(( paths['data'] + "\geographical_location"), geoLocation)


# create sun data based on grasshopper file, this is only possible with the ladybug component SunPath
#execfile(paths['python'] + "\\aux_files\\SunAngles_Tracking_and_temperature.py")

# calculate and save lookup table if it does not yet exist:
if not os.path.isfile(paths['data'] + '\python\electrical_simulation\curr_model_submod_lookup.npy'): 
    if not os.path.isdir(paths['data'] + '\python\electrical_simulation'):
        os.makedirs(paths['data'] + '\python\electrical_simulation')
    execfile(paths['python'] + '\\aux_files\\create_lookup_table.py')
else:
    print 'lookup table not created as it already exists'


# load sunTrackingData used for the LadyBug simulation:
with open(paths['geo'] + '\SunTrackingData.json', 'r') as fp:
    SunTrackingData = json.load(fp)
    fp.close()


#Set Solar Panel Properties
XANGLES=[0,15,30,45,60,75, 90]
YANGLES= [-45,-30,-15, 0, 15,30, 45]

#XANGLES=[22.5,67.5]
#YANGLES= [-22.5,22.5]


#Make a list of all angle combinations
ANGLES= [(x, y) for x in XANGLES for y in YANGLES]

#create a dicitionary with all angle combinations
combinationAngles = {}

for i in range(0,len(ANGLES)):
    combinationAngles[i] = ANGLES[i]

NumberCombinations = len(XANGLES)*len(YANGLES) #*NoClusters   



#Set panel data
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
"room_depth":7000,
"glazing_percentage_w":0.92,
"glazing_percentage_h":0.97,
}


gridSize = [400.0,200.0,100.0,50.0,25.0,12.5] #mm2

#Save parameters to be imported into grasshopper
with open('panel.json','w') as f:
    f.write(json.dumps(panel_data))

with open('building.json','w') as f:
    f.write(json.dumps(building_data))



resultsdetected=0

print '\nStart illuminance calculation with ladybug'

comb_data={"x_angle":0,
           "y_angle":0,
           "HOD":12,
           "Month":1
            }
                       
#create json file with the set combination of x-angle,y-angle and HOY
with open('comb.json','w') as f:
    f.write(json.dumps(comb_data))
    

paths['illuminance'] = paths['main'] + '\\IlluminanceResults'
HOD = 12.0
Day = 15.0
monthi = 1.0
x_angle = 0
y_angle = 0



           
for size in gridSize:
#check if there is any radiation to analysis
    with open('illuminance.json','w') as f:
        f.write(json.dumps(size)) 
                
    #Wait until the radiation_results were created    
    while not os.path.exists(paths['illuminance']+'\\Illuminance_gridSize_' + str(size) +'_month_'+  str(monthi) + '_day_' + str(Day)  + '_hour_' + str(HOD) + '_xangle_'+ str(x_angle) + '_yangle_' + str(y_angle)+ '_.csv'):
        time.sleep(1)
           
    else:
        print 'next step'
        resultsdetected += 1
                                
        
        
print 'illuminance calculation finished!'

IlluminanceData = np.array([])

with open(paths['illuminance']+'\\Illuminance_gridSize_' + str(size) +'_month_'+  str(monthi) + '_day_' + str(Day)  + '_hour_' + str(HOD) + '_xangle_'+ str(x_angle) + '_yangle_' + str(y_angle)+ '_.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for idx,line in enumerate(reader):
        if idx == 1:
            IlluminanceData = np.append(IlluminanceData, [float(line[0])])
            break
                    
                                       
    
