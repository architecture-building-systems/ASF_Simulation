# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 12:40:50 2016

@author: Mauro

@Modified: Prageeth Jayathissa

Note: _elec subscript refers to the primary energy requirement. In the case of a Gas Burner, this is the gas energy required 
"""

import os, sys
import numpy as np
import time
import pandas as pd


def RC_Model (optimization_type, paths ,building_data, weatherData, BuildingRadiationData_HOY, PV, NumberCombinations, combinationAngles, BuildingProperties, SimulationOptions, occupancy, Q_human):

    # add python_path to system path, so that all files are available:
    sys.path.insert(0, paths['5R1C_ISO_simulator'])    
    
    from buildingPhysics import Building #Importing Building Class
    from read_occupancy import Equate_Ill, BuildingData
    from optimzeTemperatureFunction import optimzeTemp, checkEqual
    from ActuationEnergyCalc import ActuationDemand
    
    import progressbar
    
    #Temperature value, to start the simulation with
    T_in = SimulationOptions['Temp_start']
    setBackTempH = SimulationOptions['setBackTempH']
    setBackTempC = SimulationOptions['setBackTempC']
    
    Tmax = BuildingProperties['theta_int_c_set'] 
    Tmin = BuildingProperties['theta_int_h_set']
    
    #calcualte floor area and room volume
    roomFloorArea = building_data['room_width']/1000.0 * building_data['room_depth']/1000.0 #[m^2] floor area
    roomVolume = building_data['room_width']/1000.0 * building_data['room_depth']/1000.0 * building_data['room_height']/1000.0 #[m^3] room area
    
    #Equation coefficients for linear polynomial
    Ill_Eq = Equate_Ill(weatherData = weatherData)
    
    #outside Temperatur
    T_out = weatherData['drybulb_C']
    
    
    #additional internal gains
    Q_equipment = 4 * roomFloorArea #4 W/m2 * FloorArea
        
    R_extWall = 3.61 #(m2*K)/W
    R_window = 0.585 #(m2*K)/W
    
    FreshAir = 0.016 #m3/(s*person)
    People = 0.1 #1/m2
    
    U_exWall, U_window, Ach_vent = BuildingData(R_extWall, R_window, FreshAir, People, roomFloorArea, roomVolume)
    
    #initilize uncomftrable hours
    uncomf_hours = 0
    uncomf_hours_HOY = []
    
    #create dicitionary to save relevant hourly data:
    hourlyData = {}
    Data_HC_HOY = {}
    Data_Heating_HOY = {}
    Data_Cooling_HOY = {}
    Data_Lighting_HOY = {}
    Data_T_in_HOY = {}
    Data_T_air_HOY = {}
    results_building_simulation = {}
    BuildingSimulationELEC = {}
    E_tot = {}
    E_HCL = {}
    Actuation = {}
    
    Data_H_elec = {}
    Data_C_elec = {}
    E_tot_elec = {}
    E_HCL_elec = {}
    
    
    print '\nStart RC-Model calculation'
    print '\nTime: ' + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
    print "\noptimization", optimization_type
    
    #class Building   
    Office=Building (
                    Fenst_A = BuildingProperties['Fenst_A'],
                    Room_Depth = BuildingProperties['Room_Depth'],
                    Room_Width = BuildingProperties['Room_Width'],
            	   Room_Height = BuildingProperties['Room_Height'],              
                    lighting_load= BuildingProperties['lighting_load'],
                    lighting_control = BuildingProperties["lighting_control"],
                    Lighting_Utilisation_Factor = BuildingProperties["Lighting_Utilisation_Factor"],
                    Lighting_Maintenance_Factor = BuildingProperties["Lighting_Maintenance_Factor"], 
                    c_m_A_f = BuildingProperties["c_m_A_f"],
                    ACH_vent = BuildingProperties["ACH_vent"],
                    ACH_infl = BuildingProperties["ACH_infl"],
                    ventilation_efficiency = BuildingProperties["ventilation_efficiency"],                   
                    U_em= BuildingProperties["U_em"], 
                    U_w = BuildingProperties["U_w"],
                    glass_solar_transmittance=BuildingProperties['glass_solar_transmittance'],
                    glass_light_transmittance = BuildingProperties["glass_light_transmittance"],
                    theta_int_h_set = BuildingProperties['theta_int_h_set'],
                    theta_int_c_set = BuildingProperties['theta_int_c_set'],
                    phi_c_max_A_f=BuildingProperties['phi_c_max_A_f'],
                    phi_h_max_A_f=BuildingProperties['phi_h_max_A_f'],
                    heatingSupplySystem=BuildingProperties["heatingSupplySystem"],
                    coolingSupplySystem=BuildingProperties["coolingSupplySystem"],
                    heatingEmissionSystem=BuildingProperties["heatingEmissionSystem"],
                    coolingEmissionSystem=BuildingProperties["coolingEmissionSystem"],
                    )         
    
    for hour_of_year in range(0,8760):
        
        #initilize all dictionaries for the needed data
        E_tot[hour_of_year] = {}
        E_HCL [hour_of_year] = {}
        Data_HC_HOY[hour_of_year] = {}
        Data_Heating_HOY[hour_of_year] = {}
        Data_Cooling_HOY[hour_of_year] = {}    
        Data_Lighting_HOY[hour_of_year] =  {}   
        Data_T_in_HOY[hour_of_year] = {}
        Data_T_air_HOY[hour_of_year] = {}
        Actuation[hour_of_year] = {}
        Data_H_elec[hour_of_year] = {}
        Data_C_elec[hour_of_year] = {}
        E_tot_elec[hour_of_year] = {}
        E_HCL_elec[hour_of_year] = {}         
        
        
        results_building_simulation[hour_of_year] = {}
        BuildingSimulationELEC[hour_of_year] = {}        
        
        hourlyData[hour_of_year]= {}
        hourlyData[hour_of_year]['PV'] = PV[hour_of_year]
        
    
    tic = time.time()
    #run for every hour of year the RC-Model    
    for hour_of_year in range(0,8760):
          
        
        if occupancy['People'][hour_of_year] == 0:
             Office.theta_int_h_set = BuildingProperties['theta_int_h_set'] - setBackTempH
             Office.theta_int_c_set = BuildingProperties['theta_int_c_set'] + setBackTempC
        else:
             Office.theta_int_h_set = BuildingProperties['theta_int_h_set']
             Office.theta_int_c_set = BuildingProperties['theta_int_c_set']                   
        
        
        #check all angle combinations and determine, which combination results in the smallest energy demand (min(E_tot))
        for comb in range(0, NumberCombinations):

            # HACK: skip if hour was not calculated
            if len(BuildingRadiationData_HOY[hour_of_year]) == 1 and comb > 0:
                continue
            # elif len(BuildingRadiationData_HOY[hour_of_year])
                    
            Q_internal = (Q_human[hour_of_year] + Q_equipment)
            Office.solve_building_energy(phi_int = Q_internal, #internal heat gains, humans and equipment [W]
                                         phi_sol = BuildingRadiationData_HOY[hour_of_year][comb] * BuildingProperties['glass_solar_transmittance'], #W
                                         theta_e = T_out[hour_of_year], 
                                         theta_m_prev = T_in)
        
            
            #Calculate Illuminance in the room. 
            fenstIll=BuildingRadiationData_HOY[hour_of_year][comb]*Ill_Eq[0] #Lumens.  Note that the constant has been ignored because it should be 0
            #Illuminance after transmitting through the window         
            TransIll=fenstIll*Office.glass_light_transmittance
            
            #Determine if people are sleeping
            if  hour_of_year%24 < 5 or hour_of_year%24 > 20:
                probLighting = 0
            else:
                probLighting = 1
           
            Office.solve_building_lighting(ill = TransIll, 
                                           occupancy = occupancy['People'][hour_of_year], probLighting = probLighting)
    
            
            
            #save all combination results for one HOY
            Data_Lighting_HOY[hour_of_year][comb] = Office.lighting_demand # Watts
            Data_HC_HOY[hour_of_year][comb] = Office.phi_hc_nd_ac #achtung heating und cooling 
            Data_T_in_HOY[hour_of_year][comb] = Office.theta_m
            Data_T_air_HOY[hour_of_year][comb] = Office.theta_air
            Data_H_elec[hour_of_year][comb] = Office.heatingEnergy
            Data_C_elec[hour_of_year][comb] = Office.coolingEnergy
            
            if Office.phi_hc_nd_ac > 0:
                Data_Heating_HOY[hour_of_year][comb] = Office.heatingEnergy 
                Data_Cooling_HOY[hour_of_year][comb] = 0
            elif Office.phi_hc_nd_ac < 0:
                Data_Heating_HOY[hour_of_year][comb] = 0
                Data_Cooling_HOY[hour_of_year][comb] = Office.coolingEnergy 
            else:
                Data_Heating_HOY[hour_of_year][comb] = 0
                Data_Cooling_HOY[hour_of_year][comb] = 0
                
            if SimulationOptions['ActuationEnergy'] == True:
                
                if hour_of_year >= 1:        
                    OldAngles = results_building_simulation[hour_of_year-1]['OptAngles']
                    NewAngles = combinationAngles[comb]
                    Actuation[hour_of_year][comb] = ActuationDemand (oldX = OldAngles[0], newX = NewAngles[0], oldY = OldAngles[1], newY = NewAngles[1], PanelNum = 50)
                else: 
                    Actuation[hour_of_year][comb] = 0
                    
            else: 
                Actuation[hour_of_year][comb] = 0

            #determine best combination for the evaluated HOY
            #integrate the needed actuation energy to calculate the real total energy demand 
            E_tot[hour_of_year][comb]=  Data_Heating_HOY[hour_of_year][comb] + Data_Cooling_HOY[hour_of_year][comb] + \
                 Data_Lighting_HOY[hour_of_year][comb] + Actuation[hour_of_year][comb] - hourlyData[hour_of_year]['PV'][comb]
            E_HCL[hour_of_year][comb] = Data_Heating_HOY[hour_of_year][comb] + Data_Cooling_HOY[hour_of_year][comb] + Data_Lighting_HOY[hour_of_year][comb]
            
            # calculated with electrical heating and cooling            
            E_tot_elec[hour_of_year][comb] =  Data_H_elec[hour_of_year][comb] + Data_C_elec[hour_of_year][comb] + Data_Lighting_HOY[hour_of_year][comb] + Actuation[hour_of_year][comb] - hourlyData[hour_of_year]['PV'][comb]
            E_HCL_elec[hour_of_year][comb] =  Data_H_elec[hour_of_year][comb] + Data_C_elec[hour_of_year][comb] + Data_Lighting_HOY[hour_of_year][comb]        

 
            
        hourlyData[hour_of_year]['HC'] = Data_HC_HOY[hour_of_year]
        hourlyData[hour_of_year]['H'] = Data_Heating_HOY[hour_of_year]
        hourlyData[hour_of_year]['H_elec'] = Data_H_elec[hour_of_year]
        hourlyData[hour_of_year]['C'] = Data_Cooling_HOY[hour_of_year]    
        hourlyData[hour_of_year]['C_elec'] =Data_C_elec[hour_of_year]
        hourlyData[hour_of_year]['L'] = Data_Lighting_HOY[hour_of_year]       
        hourlyData[hour_of_year]['E_tot'] = E_tot[hour_of_year]
        hourlyData[hour_of_year]['E_tot_elec'] = E_tot_elec[hour_of_year]
        hourlyData[hour_of_year]['E_HCL'] = E_HCL[hour_of_year]
        hourlyData[hour_of_year]['E_HCL_elec'] = E_HCL_elec[hour_of_year]
        hourlyData[hour_of_year]['T_out'] =T_out[hour_of_year]
        hourlyData[hour_of_year]['T_in'] = Data_T_in_HOY[hour_of_year]
        hourlyData[hour_of_year]['T_air'] = Data_T_air_HOY[hour_of_year]
        hourlyData[hour_of_year]['AngleComb'] = combinationAngles
        hourlyData[hour_of_year]['RadiationWindow'] = BuildingRadiationData_HOY[hour_of_year] #W
        hourlyData[hour_of_year]['AE'] = Actuation[hour_of_year]
               
        if optimization_type == 'E_total':
            #Best comb for overall energy demand
                        
            if max(hourlyData[hour_of_year]['PV']) != 0:
                #get key with min value from the E_tot dictionary
                BestComb = min(E_tot[hour_of_year], key=lambda comb: E_tot[hour_of_year][comb])

                if hour_of_year == 2932:
                    print hourlyData[hour_of_year]['RadiationWindow']
                
                equal = checkEqual(Data = E_tot[hour_of_year])
                
                if equal == True:
                    BestComb = optimzeTemp(DataTemp = Data_T_in_HOY[hour_of_year],Tmax = Tmax, Tmin = Tmin)
                else:
                    pass
                
                BestCombKey = BestComb       
               
            elif max(hourlyData[hour_of_year]['PV']) == 0:
                #Check if there is no PV-value (no radiation)
                equal = checkEqual(Data = Data_T_in_HOY[hour_of_year])                
                
                if equal == False:
                    #if temperatures are not the same, take temp which is closest to average temperature
                    BestComb = optimzeTemp(DataTemp = Data_T_in_HOY[hour_of_year], Tmax = Tmax, Tmin = Tmin)           
                    BestCombKey = BestComb
                    
                elif equal == True: #PV = 0, Temp are equal
                    BestComb = 0 #chose random Temp
                    BestCombKey = NumberCombinations # make colormap grey
        
        elif optimization_type == 'E_total_elec':
            #Best comb for overall energy demand
                        
            if max(hourlyData[hour_of_year]['PV']) != 0:
                #get key with min value from the E_tot dictionary
                BestComb = min(E_tot_elec[hour_of_year], key=lambda comb: E_tot_elec[hour_of_year][comb])
                
                equal = checkEqual(Data = E_tot[hour_of_year])
                
                if equal == True:
                    BestComb = optimzeTemp(DataTemp = Data_T_in_HOY[hour_of_year],Tmax = Tmax, Tmin = Tmin)
                
                BestCombKey = BestComb      
               
            elif max(hourlyData[hour_of_year]['PV']) == 0:
                #Check if there is no PV-value (no radiation)
                equal = checkEqual(Data = Data_T_in_HOY[hour_of_year])                
                
                if equal == False:
                    #if temperatures are not the same, take temp which is closest to average temperature
                    BestComb = optimzeTemp(DataTemp = Data_T_in_HOY[hour_of_year], Tmax = Tmax, Tmin = Tmin)           
                    BestCombKey = BestComb
                    
                elif equal == True: #PV = 0, Temp are equal
                    BestComb = 0 #chose random Temp
                    BestCombKey = NumberCombinations # make colormap grey    
 
        
        elif optimization_type == 'Lighting':
            
            if max(BuildingRadiationData_HOY[hour_of_year]) != 0:
                #get key with max building radiaiton value
                BestComb =BuildingRadiationData_HOY[hour_of_year].argmax(axis=0)
                BestCombKey = BestComb
              
        
            elif max(BuildingRadiationData_HOY[hour_of_year]) == 0:
                #Check if there is no PV-value (no radiation)
                equal = checkEqual(Data = Data_T_in_HOY[hour_of_year])                
                
                if equal == False:
                    #not needed
                    #if temperatures are not the same, take temp which is closest to average temperature
                    BestComb = optimzeTemp(DataTemp = Data_T_in_HOY[hour_of_year], Tmax = Tmax, Tmin = Tmin)           
                    BestCombKey = BestComb
                    
                    
                elif equal == True: #PV = 0, Temp are equal
                    BestComb = 0 #chose random Temp
                    BestCombKey = NumberCombinations # make colormap grey    
                
                
        elif optimization_type == 'SolarEnergy':
           
            if max(hourlyData[hour_of_year]['PV']) != 0:
                #get key with max PV production
                BestComb = hourlyData[hour_of_year]['PV'].argmax(axis=0)
                BestCombKey = BestComb               
                        
            elif max(hourlyData[hour_of_year]['PV']) == 0:
                #Check if there is no PV-value (no radiation)
                equal = checkEqual(Data = Data_T_in_HOY[hour_of_year])                
                
                if equal == False:
                    # PV production is very small and not big enough for the threshold, thefore it will result in zero PV, but in slightly different Temperatures
                    #if temperatures are not the same, take temp which is closest to average temperature
                    BestComb = optimzeTemp(DataTemp = Data_T_in_HOY[hour_of_year], Tmax = Tmax, Tmin = Tmin)           
                    BestCombKey = BestComb
                    
                    
                elif equal == True: #PV = 0, Temp are equal
                    BestComb = 0 #chose random Temp
                    BestCombKey = NumberCombinations # make colormap grey       
       
       
        elif optimization_type == 'Heating':    
        
            if max(hourlyData[hour_of_year]['PV']) != 0:
                #get key with min value from the E_tot dictionary
                BestComb = min(Data_Heating_HOY[hour_of_year], key=lambda comb: Data_Heating_HOY[hour_of_year][comb])
                 
                equal = checkEqual(Data = Data_Heating_HOY[hour_of_year])
                
                if equal == True:
                #for zero heating, chose key for max inside temperature
                    BestComb = max(Data_T_in_HOY[hour_of_year], key=lambda comb:Data_T_in_HOY[hour_of_year][comb])        
                
                BestCombKey = BestComb
        
            elif max(hourlyData[hour_of_year]['PV']) == 0:
                #Check if there is no PV-value (no radiation)
                equal = checkEqual(Data = Data_T_in_HOY[hour_of_year])                
                
                if equal == False:
                    #if temperatures are not the same, take heighest temp value
                    BestComb = max(Data_T_in_HOY[hour_of_year], key=lambda comb:Data_T_in_HOY[hour_of_year][comb])        
                    BestCombKey = BestComb
                    
                elif equal == True: #PV = 0, Temp are equal
                    BestComb = 0 #chose random Temp
                    BestCombKey = NumberCombinations # make colormap grey
        
        elif optimization_type == 'Heating_elec':    
        
            if max(hourlyData[hour_of_year]['PV']) != 0:
                #get key with min value from the E_tot dictionary
                BestComb = min(Data_H_elec[hour_of_year], key=lambda comb: Data_H_elec[hour_of_year][comb])
                 
                equal = checkEqual(Data = Data_H_elec[hour_of_year])
                
                if equal == True:
                #for zero heating, chose key for max inside temperature
                    BestComb = max(Data_T_in_HOY[hour_of_year], key=lambda comb:Data_T_in_HOY[hour_of_year][comb])        
                
                BestCombKey = BestComb
        
            elif max(hourlyData[hour_of_year]['PV']) == 0:
                #Check if there is no PV-value (no radiation)
                equal = checkEqual(Data = Data_T_in_HOY[hour_of_year])                
                
                if equal == False:
                    #if temperatures are not the same, take heighest temp value
                    BestComb = max(Data_T_in_HOY[hour_of_year], key=lambda comb:Data_T_in_HOY[hour_of_year][comb])        
                    BestCombKey = BestComb
                    
                elif equal == True: #PV = 0, Temp are equal
                    BestComb = 0 #chose random Temp
                    BestCombKey = NumberCombinations # make colormap grey
 
        
        elif optimization_type == 'Cooling':
            
            if max(hourlyData[hour_of_year]['PV']) != 0:
                #get key with min value from the E_tot dictionary
                BestComb = min(Data_Cooling_HOY[hour_of_year], key=lambda comb: Data_Cooling_HOY[hour_of_year][comb])
                
                equal = checkEqual(Data = Data_Cooling_HOY[hour_of_year])
                
                if equal == True:
                    BestComb = min(Data_T_in_HOY[hour_of_year], key=lambda comb:Data_T_in_HOY[hour_of_year][comb])
                
                BestCombKey = BestComb
        
            elif max(hourlyData[hour_of_year]['PV']) == 0:
                #Check if there is no PV-value (nor radiation), then don't move the modules
                equal = checkEqual(Data = Data_T_in_HOY[hour_of_year])                
                
                if equal == False:
                    #if temperatures are not the same, take smallest temp value
                    BestComb = min(Data_T_in_HOY[hour_of_year], key=lambda comb:Data_T_in_HOY[hour_of_year][comb])        
                    BestCombKey = BestComb
                    
                elif equal == True: #PV = 0, Temp are equal
                    BestComb = 0 #chose random Temp
                    BestCombKey = NumberCombinations # make colormap grey
                    
        elif optimization_type == 'Cooling_elec':
            
            if max(hourlyData[hour_of_year]['PV']) != 0:
                #get key with min value from the E_tot dictionary
                BestComb = min(Data_C_elec[hour_of_year], key=lambda comb: Data_C_elec[hour_of_year][comb])
                
                equal = checkEqual(Data = Data_C_elec[hour_of_year])
                
                if equal == True:
                    BestComb = min(Data_T_in_HOY[hour_of_year], key=lambda comb:Data_T_in_HOY[hour_of_year][comb])
                
                BestCombKey = BestComb
        
            elif max(hourlyData[hour_of_year]['PV']) == 0:
                #Check if there is no PV-value (nor radiation), then don't move the modules
                equal = checkEqual(Data = Data_T_in_HOY[hour_of_year])                
                
                if equal == False:
                    #if temperatures are not the same, take smallest temp value
                    BestComb = min(Data_T_in_HOY[hour_of_year], key=lambda comb:Data_T_in_HOY[hour_of_year][comb])        
                    BestCombKey = BestComb
                    
                elif equal == True: #PV = 0, Temp are equal
                    BestComb = 0 #chose random Temp
                    BestCombKey = NumberCombinations # make colormap grey
                
                        
        elif optimization_type == 'E_HCL':
                            
            if max(hourlyData[hour_of_year]['PV']) != 0:
                #get key with min value from the dictionary
                BestComb = min(E_HCL[hour_of_year], key=lambda comb: E_HCL[hour_of_year][comb])
                
                equal = checkEqual(Data = E_HCL[hour_of_year])
                
                if equal == True:
                    BestComb = optimzeTemp(DataTemp = Data_T_in_HOY[hour_of_year],Tmax = Tmax, Tmin = Tmin)
                
                BestCombKey = BestComb 
            
            elif max(hourlyData[hour_of_year]['PV']) == 0:
                
                #Check if there is no PV-value (nor radiation), then don't move the modules
                equal = checkEqual(Data = Data_T_in_HOY[hour_of_year])                
                
                if equal == False:
                    BestComb = optimzeTemp(DataTemp = Data_T_in_HOY[hour_of_year], Tmax = Tmax, Tmin = Tmin)        
                    BestCombKey = BestComb
                    
                elif equal == True: #PV = 0, Temp are equal
                    BestComb = 0 #chose random Temp
                    BestCombKey = NumberCombinations # make colormap grey
                                 
      
        
        elif optimization_type == 'E_HCL_elec':
                            
            if max(hourlyData[hour_of_year]['PV']) != 0:
                #get key with min value from the dictionary
                BestComb = min(E_HCL_elec[hour_of_year], key=lambda comb: E_HCL_elec[hour_of_year][comb])
                
                equal = checkEqual(Data = E_HCL_elec[hour_of_year])
                
                if equal == True:
                    BestComb =optimzeTemp(DataTemp = Data_T_in_HOY[hour_of_year],Tmax = Tmax, Tmin = Tmin)
                
                BestCombKey = BestComb 
            
            elif max(hourlyData[hour_of_year]['PV']) == 0:
                
                #Check if there is no PV-value (nor radiation), then don't move the modules
                equal = checkEqual(Data = Data_T_in_HOY[hour_of_year])                
                
                if equal == False:
                    BestComb = optimzeTemp(DataTemp = Data_T_in_HOY[hour_of_year], Tmax = Tmax, Tmin = Tmin)        
                    BestCombKey = BestComb
                    
                elif equal == True: #PV = 0, Temp are equal
                    BestComb = 0 #chose random Temp
                    BestCombKey = NumberCombinations # make colormap grey
      

        T_in = Data_T_in_HOY[hour_of_year][BestComb] #most efficient solution has to be used again
        T_air = Data_T_air_HOY[hour_of_year][BestComb]
        
    
        #count uncomfortable hours
        # with 10 Precent range
        UncomfHour = None
        if occupancy['People'][hour_of_year] != 0: 
            if T_air  > Tmax * 1.1 or T_air  < Tmin * 0.9:
                uncomf_hours += 1
                uncomf_hours_HOY.append(hour_of_year)
                UncomfHour = True
            else:
                UncomfHour = False

        #BestComb=24
        
        #save optimal results in a dictionary and convert to a DataFrame   
        results_building_simulation[hour_of_year]['UncomfHour'] = UncomfHour
        results_building_simulation[hour_of_year]['E_tot'] = hourlyData[hour_of_year]['E_tot'][BestComb]
        results_building_simulation[hour_of_year]['E_HCL'] =hourlyData[hour_of_year]['E_HCL'][BestComb]
        results_building_simulation[hour_of_year]['HC']  = hourlyData[hour_of_year]['HC'][BestComb]
        results_building_simulation[hour_of_year]['H']  = hourlyData[hour_of_year]['H'][BestComb]
        results_building_simulation[hour_of_year]['C']  = hourlyData[hour_of_year]['C'][BestComb]
        results_building_simulation[hour_of_year]['L']  = hourlyData[hour_of_year]['L'][BestComb]
        results_building_simulation[hour_of_year]['PV']  = hourlyData[hour_of_year]['PV'][BestComb]
        results_building_simulation[hour_of_year]['AE'] = hourlyData[hour_of_year]['AE'][BestComb]        
        results_building_simulation[hour_of_year]['BestCombKey'] = BestCombKey
        results_building_simulation[hour_of_year]['T_in'] = Data_T_in_HOY[hour_of_year][BestComb]
        results_building_simulation[hour_of_year]['T_out'] = hourlyData[hour_of_year]['T_out']
        results_building_simulation[hour_of_year]['RadiationWindow'] = BuildingRadiationData_HOY[hour_of_year][BestComb] #W
        
        BuildingSimulationELEC[hour_of_year]['E_tot_elec'] = hourlyData[hour_of_year]['E_tot_elec'][BestComb]
        BuildingSimulationELEC[hour_of_year]['E_HCL_elec'] =hourlyData[hour_of_year]['E_HCL_elec'][BestComb]
        BuildingSimulationELEC[hour_of_year]['H_elec']  = hourlyData[hour_of_year]['H_elec'][BestComb]
        BuildingSimulationELEC[hour_of_year]['C_elec']  = hourlyData[hour_of_year]['C_elec'][BestComb]
        BuildingSimulationELEC[hour_of_year]['L']  = hourlyData[hour_of_year]['L'][BestComb]
        BuildingSimulationELEC[hour_of_year]['PV']  = hourlyData[hour_of_year]['PV'][BestComb]
        BuildingSimulationELEC[hour_of_year]['BestCombKey'] = BestCombKey
        BuildingSimulationELEC[hour_of_year]['T_in'] = Data_T_in_HOY[hour_of_year][BestComb]
        BuildingSimulationELEC[hour_of_year]['T_out'] = hourlyData[hour_of_year]['T_out']
        BuildingSimulationELEC[hour_of_year]['RadiationWindow'] = BuildingRadiationData_HOY[hour_of_year][BestComb] #W
        BuildingSimulationELEC[hour_of_year]['AE'] = hourlyData[hour_of_year]['AE'][BestComb]
        

        
        if BestCombKey == NumberCombinations:
            results_building_simulation[hour_of_year]['OptAngles'] = (np.nan,np.nan)
            BuildingSimulationELEC[hour_of_year]['OptAngles'] = (np.nan, np.nan)
        else:
            results_building_simulation[hour_of_year]['OptAngles'] = combinationAngles[BestComb]
            BuildingSimulationELEC[hour_of_year]['OptAngles'] = combinationAngles[BestComb]

            
            
        #show which HOY is calculated
        # if hour_of_year % 1000 == 0 and hour_of_year != 0:
        #     # print 'HOY:', hour_of_year
        #     toc = time.time() - tic
        #     # print 'time passed (sec): ' + str(round(toc,2))
        toc = time.time() - tic
        progressbar.printProgressBar(hour_of_year, 8760, suffix="Time passed (min): %2.1f" % (toc/60.0))
            
            
    
    #store results of the best angle combinations in DataFrame   
    BuildingSimulation_df= pd.DataFrame(results_building_simulation).T 
    BuildingSimulationELEC_df = pd.DataFrame(BuildingSimulationELEC).T
    hourlyData_df = pd.DataFrame(hourlyData)
     
    print "\nEnd of RC-Model calculation: " + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
    print "uncomfortable Hours: ", uncomf_hours
    
    
    return  hourlyData_df, BuildingSimulation_df, BuildingSimulationELEC_df
    
    