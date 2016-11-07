# -*- coding: utf-8 -*-
"""

@author: Mauro Luzzatto 

Methode 1: Illuminance calculation with LadyBug

"""

import os, sys
import numpy as np
import json
import time
import csv
import matplotlib.pyplot as plt
import pandas as pd


def IlluminanceCalculationAnalysis():

    #geoLocation = 'Zuerich_Kloten_2013'
    
    
    # set if calculation is need, False = No
    Calculation = False#True#False
    
    
    # create dictionary to write all paths:
    paths = {}
    
    # find path of current folder (simulation_environment)
    paths['main'] = os.path.abspath(os.path.dirname(sys.argv[0]))
    
    # define paths of subfolders:
    paths['data'] = paths['main'] + '\\data'
    paths['python'] = paths['main'] + '\\python'
    
    
    
    # define path of weather file:
    paths['weather'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\WeatherData\Zuerich_Kloten_2013.epw' #paths['epw_name']
    
    # add python_path to system path, so that all files are available:
    sys.path.insert(0, paths['python'] + '\\aux_files')
    sys.path.insert(0, paths['python'])
      
    
    
    #Set Building Parameters
    building_data={"room_width":4900,     
    "room_height":3100,
    "room_depth":7000,
    "glazing_percentage_w":0.92,
    "glazing_percentage_h":0.97,
    }
    
    with open('building.json','w') as f:
        f.write(json.dumps(building_data))
    
    #paths['illuminance'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\IlluminanceResultsAnalysis'
    paths['illuminance'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\IlluminanceResults'
    
    if Calculation == True:
        
        # get current time
        now = time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
        print "simulation start: " + now
        #set parmeters for evaluation
        HOD = 12.0
        Day = 15.0
        monthi = 1.0
        x_angle = 0
        y_angle = 0
        
        
        
        combination = 0
        
        tic = time.time()
        
        resultsdetected=0
                
        print '\nStart illuminance calculation with ladybug'
        
        for x_angle in [0,90]:
        
            #Set panel data
            panel_data={"XANGLES": x_angle ,
            "YANGLES" : y_angle,
            "NoClusters":1,
            "numberHorizontal":6,
            "numberVertical":9,
            "panelOffset":400,
            "panelSize":400,
            "panelSpacing":500,
            }
            
            #Save parameters to be imported into grasshopper
            with open('panel.json','w') as f:
                f.write(json.dumps(panel_data))
            
            for monthi in range(1,13):
                for HOD in [8,10,12,14,16,18]:
                    
                    print "Combination number", combination
                    print HOD, monthi, x_angle
                    combination += 1
                    
                    
                    comb_data={"x_angle": x_angle,
                               "y_angle":y_angle,
                               "HOD":HOD,
                               "Month":monthi,
                               "Day": Day
                                }
                                
                     #create json file with the set combination of x-angle,y-angle and HOY
                    with open('comb.json','w') as f:
                        f.write(json.dumps(comb_data))
                    
                                             
                    
                    
                    #gridSize = [400.0, 200.0, 100.0, 50., 25., 12.5] #mm2
                    gridSize = [50.0]
                    #gridSize = [400.0]
                                       
                    for size in gridSize:
                        
                        print 'size', size
                        toc = time.time() - tic
                        print 'time passed (min): ' + str(toc/60.)
                            
                        with open('illuminance.json','w') as f:
                            f.write(json.dumps(size)) 
                                    
                        #Wait until the radiation_results were created    
                        while not os.path.exists(paths['illuminance']+'\\Illuminance_gridSize_' + str(size) +'_month_'+  str(monthi) + '_day_' + str(Day)  + '_hour_' + str(HOD) + '_xangle_'+ str(x_angle) + '_yangle_' + str(y_angle)+ '_.csv'):
                            time.sleep(3)
                               
                        else:
                            print 'next step'
                            resultsdetected += 1
                                                
            
                 
        print 'illuminance calculation finished!'
    else:
        pass        
    #set path, were the results are stored and shall be loaded
    paths['illuminance'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\IlluminanceResults\IlluminanceAnalysis_50mm'
        
    
    illuminance_avg = {}
    illuminance_data = {}
        
    y_angle = 0
    Day = 15.0
    size= 50.0
    
    for x_angle in [0,90]:
        illuminance_avg[x_angle] = {}
        illuminance_data[x_angle] = {}
    
        for monthi in range(1,13):
             illuminance_avg[x_angle][monthi] = {}
             illuminance_data[x_angle][monthi] = {}
             
             for HOD in [8,10,12,14,16,18]:  
                illuminance_avg[x_angle][monthi][HOD] = {}
                illuminance_data[x_angle][monthi][HOD] = {}    
                
                IlluminanceData = np.array([])
                
                with open(paths['illuminance']+'\\Illuminance_gridSize_' + str(size) +'_month_'+  str(monthi) + '_day_' + str(Day)  + '_hour_' + str(HOD) + '_xangle_'+ str(x_angle) + '_yangle_' + str(y_angle)+ '_.csv', 'r') as csvfile:
                    reader = csv.reader(csvfile)
                    for idx,line in enumerate(reader):
                        if idx >= 6:
                            IlluminanceData = np.append(IlluminanceData, [float(line[0])])
                illuminance_data[x_angle][monthi][HOD] = IlluminanceData                        
                illuminance_avg[x_angle][monthi][HOD]= np.average(IlluminanceData)
                
        
    illuLB = {}
    for x_angle in [0,90]:
            z = []
            for monthi in range(1,13):
                for HOD in [8,10,12,14,16,18]:  
                    z.append(illuminance_avg[x_angle][monthi][HOD])
            
            z = np.array(z)
            
            illuLB[x_angle]= np.reshape(z,(12,6))    
        
    return illuLB, illuminance_avg

illuLB, illuminance_avg = IlluminanceCalculationAnalysis()
print "test"












    
