# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 14:55:11 2016

@author: Mauro
"""
import numpy as np
import pandas as pd


def prepareAngles(Building_Simulation_df, daysPerMonth, ANGLES):
    
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
                BestKey_HOD[month][hour]= np.append(BestKey_HOD[month][hour], Building_Simulation_df['BestCombKey'][HOY][0])
                key_dict[month][hour][day] = Building_Simulation_df['BestCombKey'][HOY][0]
                
            
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
    
def prepareResults (Building_Simulation_df):
    
    from prepareData_mauro import sum_monthly
    
    #convert into kWh
    H =Building_Simulation_df['H'] *0.001
    C =Building_Simulation_df['C'] *0.001
    L =Building_Simulation_df['L'] *0.001
    E =Building_Simulation_df['E_tot'] *0.001 
    PV =Building_Simulation_df['PV'] *0.001
    E_HCL = Building_Simulation_df['E_HCL'] *0.001
    
    # new empty array for Heating data:
    H_monthly_array = np.empty(len(H))*np.nan
    C_monthly_array = np.empty(len(C))*np.nan
    L_monthly_array = np.empty(len(L))*np.nan
    E_monthly_array = np.empty(len(E))*np.nan
    E_HCL_monthly_array = np.empty(len(E_HCL))*np.nan
    PV_monthly_array = np.empty(len(PV))*np.nan
    
    #
    ## multiply the average pv generation by the number of days per month in kWh:
    for i in range(len(H)):
        H_monthly_array[i] = H[i]
        C_monthly_array[i] = C[i]
        L_monthly_array[i] = L[i]
        E_monthly_array[i] = E[i]
        E_HCL_monthly_array[i] = E_HCL[i]
        PV_monthly_array[i] = PV[i]
    
      
    
    # summed data for each hour of a month in kWh:
    sum_L = sum_monthly(L_monthly_array)
    sum_E = sum_monthly(E_monthly_array)
    sum_E_HCL = sum_monthly(E_HCL_monthly_array)
    sum_C = sum_monthly(C_monthly_array)
    sum_H = sum_monthly(H_monthly_array)
    sum_PV = -1* sum_monthly(PV_monthly_array)
    
    
    #Calculate the summed monthly values and store it in dicitionary (24 hour per every month)
    monthlyData = {}
    yearlyData = {}
    
    
    #in kWh/DaysPerMonth
    monthlyData['H'] = sum_H
    monthlyData['C'] = sum_C
    monthlyData['L'] = sum_L
    monthlyData['E'] = sum_E
    monthlyData['E_HCL'] = sum_E_HCL
    monthlyData['PV'] = sum_PV
    
    #in kWh/year
    yearlyData['E'] = E.sum()
    yearlyData['E_HCL'] = E_HCL.sum()
    yearlyData['PV'] = PV.sum() 
    yearlyData['H'] = H.sum() 
    yearlyData['C'] = C.sum()
    yearlyData['L'] = L.sum()    

    return  monthlyData, yearlyData
    
    
    