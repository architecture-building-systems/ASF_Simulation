# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 10:49:26 2017

@author: Mauro
"""


import sys, os
import json
import numpy as np
import csv
import time

"""
Create Folder structure for the DAYSIM radiation calculation

-open SensorPoints.GH file

"""


def CreateFolder(x_angle, y_angle, MaterialDict, project_name, PanelDat, BuildingData, paths, ProjectFolder):
    
    print '\ncreate Folder: ', project_name

    ProjectFolder_path = os.path.join(paths['DaySimFolder'], ProjectFolder)
    Project = os.path.join(ProjectFolder_path, project_name)
    Input = os.path.join(Project, 'input')
    Output = os.path.join(Project, 'output')
    
    paths.update({'project': Project ,
                    'input': Input,
                    'output': Output})
    
    
    
    comb_data={}
    with open(os.path.join(paths['Simulation_Environment'],'comb.json'),'w') as f:
        f.write(json.dumps(comb_data))
        
    empty = []
    with open(os.path.join(paths['Simulation_Environment'],'project_folder.json'),'w') as f:
        f.write(json.dumps(empty))
    
    if not os.path.isdir(ProjectFolder_path):
        os.makedirs(ProjectFolder_path)

    if not os.path.isdir(paths['project']):
        os.makedirs(paths['project'])
        os.makedirs(paths['input'])
        os.makedirs(paths['output'])
        
    
    
        
        
        with open(os.path.join(paths['input'],'background_geometries.csv'), 'wb') as csvfile:
            fieldnames = ['name', 'mat_name', 'mat_value']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
            writer.writeheader()
            writer.writerow({'name': project_name , 'mat_name': '0_name', 'mat_value': MaterialDict['ASF']})
            writer.writerow({'name': 'Window', 'mat_name': '0_name', 'mat_value': MaterialDict['Window']})
            writer.writerow({'name': 'Room', 'mat_name': '0_name', 'mat_value': MaterialDict['Room']})
            writer.writerow({'name': 'Context', 'mat_name': '0_name', 'mat_value': MaterialDict['Context']})
    
        PanelData.update({
        "XANGLES": x_angle,
        "YANGLES" : y_angle})
        
       
        comb_data={
        "x_angle":x_angle,
        "y_angle":y_angle
        }
        
        #Save parameters to be imported into grasshopper
        with open('panel.json','w') as f:
            f.write(json.dumps(PanelData))
            
        with open('building.json','w') as f:
            f.write(json.dumps(BuildingData))
        
        
        with open(os.path.join(paths['Simulation_Environment'],'comb.json'),'w') as f:
            f.write(json.dumps(comb_data))
        
        with open(os.path.join(paths['Simulation_Environment'],'project_folder.json'),'w') as f:
            f.write(json.dumps(paths['input']))
        
       
        while not os.path.exists(os.path.join(paths['input'],'ASF4_' +str(x_angle) + '_' + str(y_angle) + '.csv')):
            time.sleep(1)
        else:
            with open(os.path.join(paths['Simulation_Environment'],'project_folder.json'),'w') as f:
                f.write(json.dumps(empty))
            comb_data={}    
            with open(os.path.join(paths['Simulation_Environment'],'comb.json'),'w') as f:
                f.write(json.dumps(comb_data))               

        time.sleep(50)     
        print 'Folder Sucessfully Created!' 
        

    else:
        'Folder Already Exists!'


def STLFiles(x_angle, y_angle, PanelData, BuildingData, paths):
       
    print '\ncreate STL files'

    
    
    paths.update({'STL' : os.path.join(paths['DaySimFolder'], 'STL')})
    
    
     
    if not os.path.isdir(paths['STL']):
        os.makedirs(paths['STL'])
        
    PanelData.update({
    "XANGLES": x_angle,
    "YANGLES" : y_angle})
      
    
   
    comb_data={
    "x_angle":x_angle,
    "y_angle":y_angle
    }
    
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

    print 'STL Files Sucessfully Created!' 
    


    
    
    
#XANGLES = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90]
#YANGLES = [-45,-40,-35,-30,-25,-20,-15,-10,-5,0,5,10,15,20,25,30,35,40,45]

XANGLES = [45]
YANGLES = [0]

# set material reflectance valcue of ASF and Window (from 0 to 1)
MaterialDict = {
'ASF': 0.2,
'Window': 0.2,
'Context' : 0.2,
'Room': 0.2}


PanelData = {
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


ProjectFolder = 'MatTest2'
SubFolder = 'ASF'

paths = {}
paths['Simulation_Environment'] =  os.path.abspath(os.path.dirname(sys.argv[0]))
paths['DaySimFolder'] = os.path.join(os.path.dirname(paths['Simulation_Environment']), 'DaySimFolder')

for x_angle in XANGLES:
    for y_angle in YANGLES:
        
        #1 set a project name        
        project_name = SubFolder + '_' + str(x_angle) + '_' + str(y_angle)
        
        #2 create Folder structure for all ASF combiantions
        #CreateFolder(x_angle, y_angle, MaterialDict, project_name, PanelData, BuildingData, paths, ProjectFolder)
        
        #3 create STL files and folder
        STLFiles(x_angle, y_angle, PanelData, BuildingData, paths)
        
        
        