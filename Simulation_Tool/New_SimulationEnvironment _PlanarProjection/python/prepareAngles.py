# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 14:55:11 2016

@author: Assistenz
"""
import numpy as np
import pandas as pd

def prepareAngles(evaluationType, Building_Simulation_df, daysPerMonth, ANGLES):
    
    from calculateHOY import calcHOY

    #save keys of best comb
    BestKey_HOD= {}
    key_med = {}
    key_avg = {}
    key_avg_round = {}
    key_dict = {}
    
    #iterate through all months, days and hours
    for month in range(1,13):
        BestKey_HOD[month]= {}
        key_med[month] = {}
        key_avg[month] = {}
        key_avg_round[month] = {}
        key_dict[month] = {}    
        
        for hour in range(0,24):
            BestKey_HOD[month][hour] = np.array([])
            key_med[month][hour] = {}
            key_avg[month][hour] = {}
            key_avg_round[month][hour] = {}
            key_dict[month][hour] = {}        
            
            for day in range(1,daysPerMonth[month-1]+1):
                #sort keys for every month and hour
                HOY = calcHOY(month, day, hour)    
                BestKey_HOD[month][hour]= np.append(BestKey_HOD[month][hour], Building_Simulation_df[evaluationType][HOY])
                key_dict[month][hour][day] = Building_Simulation_df[evaluationType][HOY]
                
            
            #calculate median key for every month and hour
            key_avg[month][hour] = np.average(BestKey_HOD[month][hour])
            key_avg_round[month][hour] = np.round(key_avg[month][hour], decimals = 0)
            key_med[month][hour] = np.median(BestKey_HOD[month][hour])
    
    key_array = np.array([], dtype = int)
    comb_array = np.array([])
    
    #create an array with the searched keys        
    for month in range(1,13):
        for hour in range(0,24):
            key_array = np.append(key_array, key_med[month][hour])
    
    #create an comb_array with the combination belonging to the given key
    key_array = np.int_(key_array)
    comb_array= [ANGLES[ii] for ii in key_array]
    
    x_angle_array = np.array([], dtype = int)
    y_angle_array = np.array([], dtype = int)
    
    #divide the combination angles into x- and y-angle
    for jj in range(0,len(comb_array)):
            
            x_angle_array = np.append(x_angle_array, comb_array[jj][0])
            y_angle_array = np.append(y_angle_array, comb_array[jj][1])
    
    #create DataFrame with the evaluated keys        
    Best_Key_df = pd.DataFrame(BestKey_HOD)
            
    return Best_Key_df, x_angle_array, y_angle_array  