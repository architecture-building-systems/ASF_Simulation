# -*- coding: utf-8 -*-
"""
Created on Thu Jan 05 14:31:30 2017

@author: Assistenz
"""
import numpy as np
import pandas as pd
import time
import os



def ShapeData(project_folder, project_name, path_save, start, end, x_angle, y_angle):
    
    PanelNum = 50
    PanelLen = 400 #mm
    GridSize = 25 #mm
    GridPoints = (PanelLen/GridSize)**2
    
    print 'Save Data of DaySim Radiation Calculation: ', project_name      
    print 'Time: ' + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
    print 'From hour: ' + str(start)  
    print 'Until hour: ' + str(end-1)    

    tic = time.time()
    
    location1 = os.path.join(os.path.join(os.path.join('output', 'ASF1_' + str(x_angle) + '_' + str(y_angle)), 'res'), 'ASF1_' + str(x_angle) + '_' + str(y_angle) + '.ill')
    location2 = os.path.join(os.path.join(os.path.join('output', 'ASF2_' + str(x_angle) + '_' + str(y_angle)), 'res'), 'ASF2_' + str(x_angle) + '_' + str(y_angle) + '.ill')
    location3 = os.path.join(os.path.join(os.path.join('output', 'ASF3_' + str(x_angle) + '_' + str(y_angle)), 'res'), 'ASF3_' + str(x_angle) + '_' + str(y_angle) + '.ill')
    location4 = os.path.join(os.path.join(os.path.join('output', 'ASF4_' + str(x_angle) + '_' + str(y_angle)), 'res'), 'ASF4_' + str(x_angle) + '_' + str(y_angle) + '.ill')
    
    path1 = os.path.join(os.path.join(project_folder, project_name), location1)
    path2 = os.path.join(os.path.join(project_folder, project_name), location2)
    path3 = os.path.join(os.path.join(project_folder, project_name), location3)
    path4 = os.path.join(os.path.join(project_folder, project_name), location4)
    
    skip_start = start
    skip_end = 8760-end
        
    d1 = np.genfromtxt(path1, skip_footer= skip_end, skip_header= skip_start) #, usecols = (3)
    d2 = np.genfromtxt(path2, skip_footer= skip_end, skip_header= skip_start)
    d3 = np.genfromtxt(path3, skip_footer= skip_end, skip_header= skip_start)
    d4 = np.genfromtxt(path4, skip_footer= skip_end, skip_header= skip_start)
    
    #the first thre values stand for the time, therefore skip them
    ASF = np.concatenate((d1[:,3:]/1000., d2[:,3:]/1000., d3[:,3:]/1000.,d4[:,3:]/1000.), axis=1)
    

    ASF_HOY = {}
    TimePeriod = end-start
    
    for hour in range(TimePeriod):
        hourHOY = 0
        hourHOY = hour + start
        ASF_HOY[hourHOY]= np.reshape(ASF[hour],(PanelNum, GridPoints))
        #ASF_HOY[hour]= np.reshape(ASF[hour],(PanelNum, GridPoints))
    
    path5 = os.path.join(os.path.join(project_folder, project_name), r'output\Window\res\Window.csv')
    
    d5 = np.genfromtxt(path5, skip_footer= skip_end, skip_header= skip_start)
    
    Window = d5 * (0.2**2) # * area of sensorpoint in Wh
    
    np.save(os.path.join(path_save,project_name) + '_' + str(start) + '_' + str(end-1) + '.npy',ASF_HOY)
    np.save(os.path.join(path_save, 'Window_'+str(x_angle) + '_' + str(y_angle)) + '_' + str(start) + '_' + str(end-1)+ '.npy',Window)
    
    toc = time.time() - tic
    print 'time passed (min): ' + str(round(toc/60.,2))
    print '\nData Sucessfully Saved'

