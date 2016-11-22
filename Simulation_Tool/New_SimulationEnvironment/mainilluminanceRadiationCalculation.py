# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:14:42 2016

main file for simulation environment

@author: Mauro Luzzatto 
@credits: Prageeth Jayathissa, Jerimias Schmidli

28.10.2016

new RC-Model, modified

"""

import os, sys
import numpy as np
import json
import time
import warnings
import csv
import matplotlib.pyplot as plt
import pandas as pd

#def main ():

# get current time
now = time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
print "simulation start: " + now


geoLocation = 'Zuerich_Kloten_2013'




# create dictionary to write all paths:
paths = {}

# find path of current folder (simulation_environment)
paths['main'] = os.path.abspath(os.path.dirname(sys.argv[0]))

# define paths of subfolders:
paths['data'] =os.path.join(paths['main'], 'data')
paths['python'] = os.path.join(paths['main'], 'python')


paths['radiation_wall'] = os.path.join(paths['main'],  'radiation_wall')
paths['PV'] = os.path.join(paths['main'], 'PV_results')

paths['weather_folder']= os.path.join(os.path.dirname(paths['main']), 'WeatherData')


# define path of weather file:
paths['weather_folder']= os.path.join(os.path.dirname(paths['main']), 'WeatherData')
paths['weather'] = os.path.join(paths['weather_folder'], geoLocation + '.epw')

# add python_path to system path, so that all files are available:

sys.path.insert(0, paths['python'])

from epwreader import epw_reader
#read epw file of needed destination
weatherData = epw_reader(paths['weather'])


#radiation subfolder is created, there the radiation_results are saved


if not os.path.isdir(paths['radiation_wall']):
        os.makedirs(paths['radiation_wall'])





#Set Solar Panel Properties
XANGLES=[0,90]
YANGLES= [0]



#Set panel data
panel_data={"XANGLES": XANGLES ,
"YANGLES" : YANGLES,
"NoClusters":1,
"numberHorizontal":6,#6,
"numberVertical":9,#9,
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



#Save parameters to be imported into grasshopper
with open('panel.json','w') as f:
    f.write(json.dumps(panel_data))

with open('building.json','w') as f:
    f.write(json.dumps(building_data))


timeRange = range(8,19)

resultsdetected=0

print '\nStart radiation calculation with ladybug'
print '\nTime: ' + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())


# create dicitionary to save optimal angles:
BuildingRadiationData_HOD = {}


tic = time.time()


for monthi in range(1,13):
      
    BuildingRadiationData_HOD[monthi] = {}
    
    for HOD in timeRange:#hour_in_month[monthi]:
        
        BuildingRadiationData = np.array([])
        
        for x_angle in XANGLES:
            for y_angle in YANGLES:
                
                comb_data={"x_angle":x_angle,
                           "y_angle":y_angle,
                           "HOD":HOD,
                           "Month":monthi
                           }
                           
                #create json file with the set combination of x-angle,y-angle and HOY
                with open('comb.json','w') as f:
                    f.write(json.dumps(comb_data))
                    print HOD, monthi, x_angle, y_angle, resultsdetected
                    toc = time.time() - tic
                    print 'time passed (min): ' + str(toc/60.)

                  
                                                                                    
                #read total radition on wall and save it in BuildingRadiationData              
                while not os.path.exists(os.path.join(paths['radiation_wall'], 'RadiationWall' + '_' + str(int(HOD)) +'_'+ str(monthi) + '_'+ str(x_angle) + '_' + str(y_angle) + '.csv')):
                    time.sleep(1)
                else:
                    print 'next step'
                    resultsdetected += 1
                        
                    
     
print "\nEnd of radiaiton calculation: " + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
