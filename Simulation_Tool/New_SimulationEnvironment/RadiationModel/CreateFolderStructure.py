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

#x_angle = 76
#y_angle = 4
#
#MaterialDict = {'ASF': 0.2,
#                'Window': 0.654}
#
#source = r'C:\Users\Assistenz\Desktop\Mauro\radiation_visualization\ASF_0_0_AM\input'


def CreateFolder(x_angle, y_angle, MaterialDict, source, project_name):
    
        
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
    
    
#        src= os.path.join(paths['source'],'Room.stl')
#        shutil.copy(src, paths['input'])
#        
#        src= os.path.join(paths['source'], 'Window.stl')
#        shutil.copy(src, paths['input'])
#        
#        src= os.path.join(paths['source'],'Context.stl')
#        shutil.copy(src, paths['input'])
        
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
    
        PanelData = {
        "XANGLES": x_angle,
        "YANGLES" : y_angle,
        "NoClusters":1,
        "numberHorizontal":6,
        "numberVertical":9,
        "panelOffset":400,
        "panelSize":400,
        "panelSpacing":500,
        "panelGridSize" : 25}
        
        BuildingData = {
        "room_width": 4900, 
        "room_height":3100, 
        "room_depth":7000, 
        "glazing_percentage_w": 0.92,
        "glazing_percentage_h": 0.97, 
        "WindowGridSize": 200,
        "BuildingOrientation" : 0} #building orientation of 0 corresponds to south facing, 90 is east facing, -90 is west facing

       
        comb_data={
        "x_angle":x_angle,
        "y_angle":y_angle,
        "Hour": 12,
        "Day":  1,
        "Month": 1}
        
        #Save parameters to be imported into grasshopper
        with open('panel.json','w') as f:
            f.write(json.dumps(PanelData))
            
        with open('building.json','w') as f:
            f.write(json.dumps(BuildingData))
        
        #print 'Folder: ', paths['input']
        
        
        with open(os.path.join(paths['Simulation_Environment'],'comb.json'),'w') as f:
            f.write(json.dumps(comb_data))
        
        with open(os.path.join(paths['Simulation_Environment'],'project_folder.json'),'w') as f:
            f.write(json.dumps(paths['input']))
        
            

       
        while not os.path.exists(os.path.join(paths['input'],'ASF4_' + str(x_angle) + '_' + str(y_angle)+ '.csv')):
            time.sleep(1)                                
        else:
            pass

        for ii in range(1,5):
            if os.path.exists(os.path.join(paths['input'], 'ASF' + str(ii) + '_' + str(x_angle) + '_' + str(y_angle + 5) + '.csv')):
                os.remove(os.path.join(paths['input'], 'ASF' + str(ii) + '_' + str(x_angle) + '_' + str(y_angle + 5) + '.csv'))
            
        
        comb_data={}
        
        with open(os.path.join(paths['Simulation_Environment'],'project_folder.json'),'w') as f:
            f.write(json.dumps(empty))
        
        
        with open(os.path.join(paths['Simulation_Environment'],'comb.json'),'w') as f:
            f.write(json.dumps(comb_data))
            
        
        time.sleep(2)   
        
    
        print 'Folder Sucessfully Created!' 
        

    else:
        'Folder Already Exists!'

def STLFolder(x_angle, y_angle):
    
        
    print '\ncreate Folder: ', project_name

    paths = {}
    paths['folder'] = r'C:\Users\Assistenz\Desktop\Mauro\radiation_visualization'
    paths['STL'] = os.path.join(paths['folder'], 'STL')
    paths['Simulation_Environment'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment' 
    
     
    if not os.path.isdir(paths['STL']):
        os.makedirs(paths['STL'])
      
    
    PanelData = {
    "XANGLES": x_angle,
    "YANGLES" : y_angle,
    "NoClusters":1,
    "numberHorizontal":6,
    "numberVertical":9,
    "panelOffset":400,
    "panelSize":400,
    "panelSpacing":500,
    "panelGridSize" : 25}
    
    BuildingData = {
    "room_width": 4900, 
    "room_height":3100, 
    "room_depth":7000, 
    "glazing_percentage_w": 0.92,
    "glazing_percentage_h": 0.97, 
    "WindowGridSize": 200,
    "BuildingOrientation" : 0} #building orientation of 0 corresponds to south facing, 90 is east facing, -90 is west facing

   
    comb_data={
    "x_angle":x_angle,
    "y_angle":y_angle,
    "Hour": 12,
    "Day":  1,
    "Month": 1}
    
    #Save parameters to be imported into grasshopper
    with open('panel.json','w') as f:
        f.write(json.dumps(PanelData))
        
    with open('building.json','w') as f:
        f.write(json.dumps(BuildingData))
    
    
    
    with open(os.path.join(paths['Simulation_Environment'],'comb.json'),'w') as f:
        f.write(json.dumps(comb_data))
        
    with open(os.path.join(paths['Simulation_Environment'],'project_folder.json'),'w') as f:
        f.write(json.dumps(paths['STL']))
   
   
    

    
    while not os.path.exists(os.path.join(paths['STL'],'ASF_' + str(x_angle) + '_' + str(y_angle)+ '.stl')):
        time.sleep(1)
    else:
        pass
    
    comb_data={}
       
    
    with open(os.path.join(paths['Simulation_Environment'],'comb.json'),'w') as f:
        f.write(json.dumps(comb_data))
        
      
    

    print 'Folder Sucessfully Created!' 
    


    
    
    
XANGLES = [0,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90]
YANGLES = [-45,-40,-35,-30,-25,-20,-15,-10,-5,0,5,10,15,20,25,30,35,40,45]#,0,45]

MaterialDict = {'ASF': 0.2,
                'Window': 0.2}

source = r'C:\Users\Assistenz\Desktop\Mauro\radiation_visualization\ASF_0_0_AM\input' 
path_project = r'C:\Users\Assistenz\Desktop\Mauro\radiation_visualization'   

for x_angle in XANGLES:
    for y_angle in YANGLES:
        
        project_name = '2ASF_' + str(x_angle) + '_' + str(y_angle)
        CreateFolder(x_angle, y_angle, MaterialDict, source, project_name)
        
        #STLFolder(x_angle, y_angle)
"""            

x_angle = 0
y_angle = -45       
path = r'C:\Users\Assistenz\Desktop\Mauro\radiation_visualization\2ASF_0_-45\input'    
destination  = r'C:\Users\Assistenz\Desktop\Mauro\radiation_visualization'
source = os.path.join(path, 'ASF1_' + str(x_angle) + '_' + str(y_angle) + '.csv')    

shutil.move(source, destination)


os.remove(pathTest)

"""