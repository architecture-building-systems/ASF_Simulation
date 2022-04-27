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
                BestKey_HOD[month][hour]= np.append(BestKey_HOD[month][hour], Building_Simulation_df['BestCombKey'][HOY])
                key_dict[month][hour][day] = Building_Simulation_df['BestCombKey'][HOY]
                
            
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
    BestKey_df = pd.DataFrame(key_med)
            
    return BestKey_df, x_angle_array, y_angle_array
    
    
    
def prepareResults (Building_Simulation_df):
    
    from prepareData_mauro import sum_monthly
        
    #Calculate the summed monthly values and store it in dicitionary (24 hour per every month)
    monthlyData = {}
    yearlyData = {}
    monthlyData['Total'] = []    
    # summed data for each hour of a month in kWh:
    monthlyData['L'] = sum_monthly(X = np.array(Building_Simulation_df['L']) *0.001)
    monthlyData['E'] = sum_monthly(X = np.array(Building_Simulation_df['E_tot']) *0.001)
    monthlyData['E_HCL'] = sum_monthly(X = np.array(Building_Simulation_df['E_HCL']) *0.001)
    monthlyData['C'] = sum_monthly(X = np.array(Building_Simulation_df['C']) *0.001)
    monthlyData['H'] = sum_monthly(X = np.array(Building_Simulation_df['H']) *0.001)
    monthlyData['PV'] = -1* sum_monthly(X = np.array(Building_Simulation_df['PV']) *0.001)
    #monthlyData['Total'] = sum_monthly.sum(axis=0)
    for i in range(len(monthlyData['E'])):
        monthlyData['Total'].append(monthlyData['L'][i]+monthlyData['C'][i]+monthlyData['H'][i]+monthlyData['PV'][i])
    
    #in kWh/year
    yearlyData['E'] = monthlyData['E'].sum() 
    yearlyData['E_HCL'] = monthlyData['E_HCL'].sum() 
    yearlyData['PV'] = monthlyData['PV'].sum() 
    yearlyData['H'] = monthlyData['H'].sum() 
    yearlyData['C'] = monthlyData['C'].sum() 
    yearlyData['L'] =monthlyData['L'].sum() 

    monthlyData['AE'] = sum_monthly(X = np.array(Building_Simulation_df['AE']) *0.001)
    yearlyData['AE'] = monthlyData['AE'].sum()
    
    return  monthlyData, yearlyData


def prepareResultsELEC (Building_Simulation_df):
    
    from prepareData_mauro import sum_monthly
   
    #Calculate the summed monthly values and store it in dicitionary (24 hour per every month)
    monthlyData = {}
    yearlyData = {}
    
    
    #in kWh/DaysPerMonth
    monthlyData['L'] = sum_monthly(X = np.array(Building_Simulation_df['L'] *0.001))
    monthlyData['PV'] = -1 * sum_monthly(X = np.array(Building_Simulation_df['PV'] *0.001))
    monthlyData['H_elec'] = sum_monthly(X = np.array(Building_Simulation_df['H_elec'] *0.001))
    monthlyData['C_elec'] = sum_monthly(X = np.array(Building_Simulation_df['C_elec'] *0.001))
    monthlyData['E_elec'] = sum_monthly(X = np.array(Building_Simulation_df['E_tot_elec'] *0.001))
    monthlyData['E_HCL_elec'] = sum_monthly(X = np.array(Building_Simulation_df['E_HCL_elec'] *0.001))
    
    #in kWh/year
    yearlyData['PV'] =  monthlyData['PV'].sum() 
    yearlyData['L'] = monthlyData['L'].sum()
    yearlyData['E_elec'] =  monthlyData['E_elec'].sum()
    yearlyData['E_HCL_elec'] =  monthlyData['E_HCL_elec'].sum()
    yearlyData['C_elec'] =  monthlyData['C_elec'].sum() 
    yearlyData['H_elec'] =  monthlyData['H_elec'].sum() 
    

    return  monthlyData, yearlyData
    
    
    