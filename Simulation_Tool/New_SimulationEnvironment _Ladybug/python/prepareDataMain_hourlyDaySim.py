# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 14:55:11 2016

@author: Mauro
"""
import numpy as np
import pandas as pd


def prepareAngles(Building_Simulation_df, ANGLES, start, end, TotalHOY):
    
    
    #save keys of best comb
    key_dict = {}
    key_array = np.array([], dtype = int)
    comb_array = np.array([])
    
    #iterate through all months, days and hours
    for HOY in TotalHOY:
        
        key_array = np.append(key_array, Building_Simulation_df['BestCombKey'][HOY])
        key_dict[HOY] = Building_Simulation_df['BestCombKey'][HOY]
        
    #create an comb_array with the combination belonging to the given key
    key_array = np.int_(key_array)
    comb_array= [ANGLES[ii] for ii in key_array]
    
    x_angle_array = np.array([], dtype = int)
    y_angle_array = np.array([], dtype = int)
    
    #divide the combination angles into x- and y-angle
    for jj in range(0,len(comb_array)):
        
        if comb_array[jj][0]== 0.1111:
            x_angle_array = np.append(x_angle_array, np.nan)
            y_angle_array = np.append(y_angle_array, np.nan)
        else:
            x_angle_array = np.append(x_angle_array, comb_array[jj][0])
            y_angle_array = np.append(y_angle_array, comb_array[jj][1])
            

    
    #create DataFrame with the evaluated keys        
    BestKey = key_dict
    
    
    
    #convert into kWh
    H = np.array(Building_Simulation_df['H'] *0.001)
    C = np.array(Building_Simulation_df['C'] *0.001)
    L = np.array(Building_Simulation_df['L'] *0.001)
    E = np.array(Building_Simulation_df['E_tot'] *0.001) 
    PV =np.array(Building_Simulation_df['PV'] *0.001) 
    E_HCL = np.array(Building_Simulation_df['E_HCL'] *0.001)
    AE = np.array(Building_Simulation_df['AE'] *0.001)
    H_elec = np.array(Building_Simulation_df['H_elec'] *0.001)
    C_elec = np.array(Building_Simulation_df['C_elec'] *0.001)
    E_elec = np.array(Building_Simulation_df['E_tot_elec'] *0.001)
    E_HCL_elec = np.array(Building_Simulation_df['E_HCL_elec'] *0.001)
    
    
    HourlyTotalData = {}
    
    
    #in kWh for all analysed hours
    HourlyTotalData['H'] = H.sum()
    HourlyTotalData['C'] = C.sum()
    HourlyTotalData['L'] = L.sum()
    HourlyTotalData['E'] = E.sum()
    HourlyTotalData['E_HCL'] = E_HCL.sum()
    HourlyTotalData['PV'] = PV.sum()
    HourlyTotalData['AE'] = AE.sum()
    HourlyTotalData['H_elec'] = H_elec.sum()
    HourlyTotalData['C_elec'] = C_elec.sum()
    HourlyTotalData['E_elec'] = E_elec.sum()
    HourlyTotalData['E_HCL_elec'] = E_HCL_elec.sum()
    


        
    return BestKey, x_angle_array, y_angle_array, HourlyTotalData
    
   
    