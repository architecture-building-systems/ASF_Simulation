# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 14:55:11 2016

@author: Mauro
"""
import numpy as np
import pandas as pd


def prepareAngles(Building_Simulation_df, ANGLES, start, end):
    
    
    #save keys of best comb
    key_dict = {}
    key_array = np.array([], dtype = int)
    comb_array = np.array([])
    
    #iterate through all months, days and hours
    for HOY in range(start, end+1):
        
        key_array = np.append(key_array, Building_Simulation_df['BestCombKey'][HOY][0])
        key_dict[HOY] = Building_Simulation_df['BestCombKey'][HOY][0]
        
    #create an comb_array with the combination belonging to the given key
    key_array = np.int_(key_array)
    comb_array= [ANGLES[ii] for ii in key_array]
    
    x_angle_array = np.array([], dtype = int)
    y_angle_array = np.array([], dtype = int)
    
    #divide the combination angles into x- and y-angle
    for jj in range(0,len(comb_array)):
            
            x_angle_array = np.append(x_angle_array, comb_array[jj][0])
            y_angle_array = np.append(y_angle_array, comb_array[jj][1])
            
    x_angle = {}
    y_angle = {}        
            
    for  jj in range(0,len(comb_array)):
        
        x_angle[start + jj] = x_angle_array[jj]
        y_angle[start + jj] = y_angle_array[jj]
    
    #create DataFrame with the evaluated keys        
    BestKey = key_dict
            
    return BestKey, x_angle, y_angle
    
   
   
    
def prepareResults (Building_Simulation_df):
    
    from prepareData_mauro import sum_monthly
    
    
    #convert into kWh
    H_monthly_array = np.array(Building_Simulation_df['H'] *0.001)
    C_monthly_array = np.array(Building_Simulation_df['C'] *0.001)
    L_monthly_array = np.array(Building_Simulation_df['L'] *0.001)
    E_monthly_array = np.array(Building_Simulation_df['E_tot'] *0.001) 
    PV_monthly_array =np.array(Building_Simulation_df['PV'] *0.001)
    E_HCL_monthly_array = np.array(Building_Simulation_df['E_HCL'] *0.001)
    
    H_elec_monthly_array = np.array(Building_Simulation_df['H_elec'] *0.001)
    C_elec_monthly_array = np.array(Building_Simulation_df['C_elec'] *0.001)
    E_elec_monthly_array = np.array(Building_Simulation_df['E_tot_elec'] *0.001)
    E_HCL_elec_monthly_array = np.array(Building_Simulation_df['E_HCL_elec'] *0.001)
    
        
    # summed data for each hour of a month in kWh:
    sum_L = sum_monthly(X = L_monthly_array)
    sum_E = sum_monthly(X = E_monthly_array)
    sum_E_HCL = sum_monthly(X = E_HCL_monthly_array)
    sum_C = sum_monthly(X = C_monthly_array)
    sum_H = sum_monthly(X = H_monthly_array)
    sum_PV = -1* sum_monthly(X = PV_monthly_array)
    
    sum_E_HCL_elec = sum_monthly(X = E_HCL_elec_monthly_array)
    sum_C_elec = sum_monthly(X = C_elec_monthly_array)
    sum_H_elec = sum_monthly(X = H_elec_monthly_array)
    sum_E_elec = sum_monthly(X = E_elec_monthly_array)
    
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

    monthlyData['H_elec'] = sum_H_elec
    monthlyData['C_elec'] = sum_C_elec
    monthlyData['E_elec'] = sum_E_elec
    monthlyData['E_HCL_elec'] = sum_E_HCL_elec
    
    #in kWh/year
    yearlyData['E'] = sum_E.sum()
    yearlyData['E_HCL'] = sum_E_HCL.sum()
    yearlyData['PV'] = sum_PV.sum() 
    yearlyData['H'] = sum_H.sum() 
    yearlyData['C'] = sum_C.sum()
    yearlyData['L'] = sum_L.sum()
    
    yearlyData['E_elec'] = sum_E_elec.sum()
    yearlyData['E_HCL_elec'] = sum_E_HCL_elec.sum()
    yearlyData['C_elec'] = sum_C_elec.sum() 
    yearlyData['H_elec'] = sum_H_elec.sum() 
    

    return  monthlyData, yearlyData
    
    
    