# -*- coding: utf-8 -*-
"""
Created on Fri Jan 06 09:16:01 2017

@author: Mauro
Unused!
"""
import os, sys
import numpy as np
import time
import warnings
import csv
import matplotlib.pyplot as plt
import pandas as pd


    
x_angle = 76
y_angle = 3

weatherFile = 'Zuerich_Kloten_2013.epw'

start = 2
end = 19

path_save = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RadiationModel'
project_folder = r'C:\Users\Assistenz\Desktop\Mauro\radiation_visualization'


# add python_path to system path, so that all files are available:
sys.path.insert(0, project_folder)
sys.path.insert(0, path_save)

from daysim_exe import calc_radiation
from RadianceParameters import Library


project_name = 'ASF_' + str(x_angle)+ '_' + str(y_angle)

location1 = os.path.join(os.path.join(os.path.join('output', 'ASF1_' + str(x_angle) + '_' + str(y_angle)), 'res'), 'ASF1_' + str(x_angle) + '_' + str(y_angle) + '.ill')
location2 = os.path.join(os.path.join(os.path.join('output', 'ASF2_' + str(x_angle) + '_' + str(y_angle)), 'res'), 'ASF2_' + str(x_angle) + '_' + str(y_angle) + '.ill')
location3 = os.path.join(os.path.join(os.path.join('output', 'ASF3_' + str(x_angle) + '_' + str(y_angle)), 'res'), 'ASF3_' + str(x_angle) + '_' + str(y_angle) + '.ill')
location4 = os.path.join(os.path.join(os.path.join('output', 'ASF4_' + str(x_angle) + '_' + str(y_angle)), 'res'), 'ASF4_' + str(x_angle) + '_' + str(y_angle) + '.ill')

path1 = os.path.join(os.path.join(project_folder, project_name), location1)
path2 = os.path.join(os.path.join(project_folder, project_name), location2)
path3 = os.path.join(os.path.join(project_folder, project_name), location3)
path4 = os.path.join(os.path.join(project_folder, project_name), location4)


if not os.path.exists(path1) and not os.path.exists(path2) and not os.path.exists(path3) and not os.path.exists(path4):
    
    if __name__ == '__main__':           
        
        print '\nStart radiation calculation with daysim'
        print 'Time: ' + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
        
        tic = time.time()
        
        geometry_table_name = 'background_geometries'
        #sensor_geometries_name = 'sensor_geometries'
        #sen_list = 'sen_dir'
      
        sen_list = ['ASF1_' + str(x_angle)+ '_' + str(y_angle),
                    'ASF2_' + str(x_angle)+ '_' + str(y_angle),
                    'ASF3_' + str(x_angle)+ '_' + str(y_angle),
                    'ASF4_' + str(x_angle)+ '_' + str(y_angle), 
                    'Window', 'Room'] #csv-file (sensor points, independent of stl-geometry files)
        
        
        #1
        project_path = os.path.join(project_folder, project_name) 
        input_path = os.path.join(project_path, 'input')
        
        
        #2
        weatherFileFolder = r'C:\Users\Assistenz\Desktop\Mauro\radiation_visualization\WeatherData'
        weatherfile_path = os.path.join(weatherFileFolder, weatherFile)
        
        #3
        RadianceValues = 'Default'
        rad_params = Library (RadianceValues = RadianceValues)
        
     
        #option to chose    
        calc_radiation(input_path, project_path, geometry_table_name, weatherfile_path, sen_list=sen_list, rad_params = rad_params)
        #calc_radiation(input_path, project_path, geometry_table_name, weatherfile_path, sensor_geometries_name=sensor_geometries_name, rad_params = rad_params)

        print project_name + ' done'
        
        toc = time.time() - tic
        print 'time passed (min): ' + str(round(toc/60.,2))
    
   
    
else:
    "Radiation Calculation with Daysim already completed"                

"""



    ShapeData(path_project = project_folder, project_name = project_name, path_save = path_save, start = start, end= end, x_angle = x_angle, y_angle = y_angle)


    pass
#in asf_electricity_prodcution_daysim load

Test = np.load(os.path.join(path_save,project_name) + '_' + str(start) + '_' + str(end-1) + '.npy').item()
"""