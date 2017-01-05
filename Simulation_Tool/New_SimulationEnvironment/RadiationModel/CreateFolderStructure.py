# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 10:49:26 2017

@author: Assistenz
"""

import shutil
import sys, os
import json
import numpy as np

import csv
import time




XANGLES = [76]
YANGLES = [-45,-30]

MaterialValueASF = 0.2
MaterialValueWindow = 0.654

source = r'C:\Users\Assistenz\Desktop\Mauro\radiation_visualization\ASF_0_0\input'


for x_angle in XANGLES:
    for y_angle in YANGLES:
        
        print '\ncreate Folder ASF_' + str(x_angle) + '_' + str(y_angle)

        paths = {}
        paths['folder'] = r'C:\Users\Assistenz\Desktop\Mauro\radiation_visualization'
        paths['project'] = os.path.join(paths['folder'], 'ASF_' + str(x_angle) + '_' + str(y_angle))
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
                writer.writerow({'name': 'ASF_' + str(x_angle) + '_' + str(y_angle) , 'mat_name': '0_6', 'mat_value': MaterialValueASF})
                writer.writerow({'name': 'Window', 'mat_name': '0_7', 'mat_value': MaterialValueWindow})
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
            
            
            
            time.sleep(180)
            
            with open(os.path.join(paths['Simulation_Environment'],'project_folder.json'),'w') as f:
                f.write(json.dumps(empty))
        
            print 'Folder created!' 
            
    
        else:
            'Folder already exists!'
        
        