# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 10:49:26 2017

@author: Mauro
"""

import shutil
import sys, os
import json
import numpy as np
import csv
import time

"""
open SensorPoints.GH file
"""

x_angle = 76
y_angle = 4

MaterialDict = {'ASF': 0.2,
                'Window': 0.654}

source = r'C:\Users\Assistenz\Desktop\Mauro\radiation_visualization\ASF_0_0_AM\input'


def CreateFolder(x_angle, y_angle, MaterialDict, source):
    
    project_name = 'ASF_' + str(x_angle) + '_' + str(y_angle)
        
    print '\ncreate Folder: ', project_name

    paths = {}
    paths['folder'] = r'C:\Users\Assistenz\Desktop\Mauro\radiation_visualization'
    paths['project'] = os.path.join(paths['folder'], project_name)
    paths['input'] = os.path.join(paths['project'], 'input')
    paths['output'] = os.path.join(paths['project'], 'output')
    paths['py2radiance_data'] = os.path.join(paths['input'],'py2radiance_data')
    paths['source'] = source
    paths['Simulation_Environment'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment' 
    
    comb_data={}
    with open(os.path.join(paths['Simulation_Environment'],'comb.json'),'w') as f:
        f.write(json.dumps(comb_data))
        
    empty = []
    with open(os.path.join(paths['Simulation_Environment'],'project_folder.json'),'w') as f:
        f.write(json.dumps(empty))
    
    if not os.path.isdir(paths['project']):
        os.makedirs(paths['project'])
        os.makedirs(paths['input'])
        os.makedirs(paths['output'])
        os.makedirs(paths['py2radiance_data'])
    
    
        src= os.path.join(paths['source'],'Room.stl')
        shutil.copy(src, paths['input'])
        
        src= os.path.join(paths['source'], 'Window.stl')
        shutil.copy(src, paths['input'])
        
        src= os.path.join(paths['source'],'Context.stl')
        shutil.copy(src, paths['input'])
        
        src= os.path.join(paths['source'], 'base.rad')
        shutil.copy(src, paths['input'])
        
        
        src= os.path.join(os.path.join(paths['source'], 'py2radiance_data'), 'command.txt')
        shutil.copy(src, paths['py2radiance_data'])
        
        src= os.path.join(os.path.join(paths['source'], 'py2radiance_data'), 'geometry.rad')
        shutil.copy(src, paths['py2radiance_data'])
        
        
        with open(os.path.join(paths['input'],'background_geometries.csv'), 'wb') as csvfile:
            fieldnames = ['name', 'mat_name', 'mat_value']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
            writer.writeheader()
            writer.writerow({'name': project_name , 'mat_name': '0_6', 'mat_value': MaterialDict['ASF']})
            writer.writerow({'name': 'Window', 'mat_name': '0_7', 'mat_value': MaterialDict['Window']})
            writer.writerow({'name': 'Room', 'mat_name': '0_8', 'mat_value': 0.2})
            writer.writerow({'name': 'Context', 'mat_name': '0_8', 'mat_value': 0.2})
       
        comb_data={"x_angle":x_angle,
                   "y_angle":y_angle,
                   "Hour": 12,
                   "Day":  1,
                   "Month": 1
                   }

        
        print 'Folder: ', paths['input']
        
        with open(os.path.join(paths['Simulation_Environment'],'comb.json'),'w') as f:
            f.write(json.dumps(comb_data))
            
        with open(os.path.join(paths['Simulation_Environment'],'project_folder.json'),'w') as f:
            f.write(json.dumps(paths['input']))
       
       
        while not os.path.exists(os.path.join(paths['input'],'ASF4_' + str(x_angle) + '_' + str(y_angle)+ '.csv')):
            time.sleep(1)                                
        else:
            pass

        
        while not os.path.exists(os.path.join(paths['input'],'ASF_' + str(x_angle) + '_' + str(y_angle)+ '.stl')):
            time.sleep(1)
        else:
            pass
        
        
        with open(os.path.join(paths['Simulation_Environment'],'project_folder.json'),'w') as f:
            f.write(json.dumps(empty))

        comb_data={}
        
        with open(os.path.join(paths['Simulation_Environment'],'comb.json'),'w') as f:
            f.write(json.dumps(comb_data))
    
        print 'Folder Sucessfully Created!' 
        

    else:
        'Folder Already Exists!'
    
    
CreateFolder(x_angle, y_angle, MaterialDict, source)
        