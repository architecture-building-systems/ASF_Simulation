# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 12:40:50 2016

@author: Assistenz
"""

import os, sys
import numpy as np
import time
import pandas as pd


def energy_minimization(optimization_type, paths,building_data, weatherData, hourRadiation, BuildingRadiationData_HOY, PV, NumberCombinations, combinationAngles, BuildingProperties, setBackTemp):
    
    print '\nStart RC-Model calculation'
    print '\nTime: ' + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
    print "\noptimization", optimization_type
    
    #create dicitionary to save relevant hourly data:
    hourlyData = {}
    Data_HC_HOY = {}
    Data_Heating_HOY = {}
    Data_Cooling_HOY = {}
    Data_Lighting_HOY = {}
    Data_T_in_HOY = {}
    results_building_simulation = {}
    E_tot = {}
    E_HCL = {}
    
    
    
    #Temperature value, to start the simulation with
    T_in = 20
    
    
    
    tic = time.time()
    
    paths['5R1C_ISO_simulator'] = os.path.join(paths['main'], '5R1C_ISO_simulator')
    paths['5R1C_ISO_simulator_data'] = os.path.join(paths['5R1C_ISO_simulator'], 'data')    
    paths['Occupancy'] = os.path.join(paths['5R1C_ISO_simulator_data'],'Occupancy_COM.csv') 
    
    
    # add python_path to system path, so that all files are available:
    sys.path.insert(0, paths['5R1C_ISO_simulator'])
    
    
    #set parameters
    human_heat_emission=0.12 #[kWh] heat emitted by a human body per hour. Source: HVAC Engineers Handbook, F. Porges
    roomFloorArea = building_data['room_width']/1000.0 * building_data['room_depth']/1000.0 #[m^2] floor area
    roomVolume = building_data['room_width']/1000.0 * building_data['room_depth']/1000.0 * building_data['room_height']/1000.0 #[m^3] room area
    
    
    from buildingPhysics import Building #Importing Building Class
    from read_occupancy import read_occupancy, Equate_Ill, BuildingData
        
    #people/m2/h, W    
    occupancy, Q_human = read_occupancy(myfilename = paths['Occupancy'], human_heat_emission = human_heat_emission, floor_area = roomFloorArea)
    
    #Equation coefficients for linear polynomial
    Ill_Eq = Equate_Ill(weatherData = weatherData)
    
    #outside Temperatur
    T_out = weatherData['drybulb_C']
    
    #Values form the HoNR building
    
    #additional internal gains
    Q_equipment = 4 * roomFloorArea #4 W/m2 * FloorArea
    #Q_equipment = 0
    
    R_extWall = 3.61 #(m2*K)/W
    R_window = 0.585 #(m2*K)/W
    
    FreshAir = 0.016 #m3/(s*person)
    People = 0.1 #1/m2
    
    U_exWall, U_window, Ach_vent = BuildingData(R_extWall, R_window, FreshAir, People, roomFloorArea, roomVolume)
    
    #initilize uncomftrable hours
    uncomf_hours = 0
    uncomf_hours_HOY = []
    
    for hour_of_year in range(0,8760):
        
        #initilize all dictionaries for the needed data
        E_tot[hour_of_year] = {}
        E_HCL [hour_of_year] = {}
        Data_HC_HOY[hour_of_year] = {}
        Data_Heating_HOY[hour_of_year] = {}
        Data_Cooling_HOY[hour_of_year] = {}    
        Data_Lighting_HOY[hour_of_year] =  {}   
        Data_T_in_HOY[hour_of_year] = {}
        
        results_building_simulation[hour_of_year] = {}
        hourlyData[hour_of_year]= {}
        hourlyData[hour_of_year]['HC'] = []
        hourlyData[hour_of_year]['H'] = [] 
        hourlyData[hour_of_year]['C'] = [] 
        hourlyData[hour_of_year]['L'] = []       
        hourlyData[hour_of_year]['E_tot'] = []
        hourlyData[hour_of_year]['E_HCL'] = []
        hourlyData[hour_of_year]['T_out'] = []
        hourlyData[hour_of_year]['T_in'] = []
        hourlyData[hour_of_year]['AngleComb'] = []
        hourlyData[hour_of_year]['PV'] = PV[hour_of_year]['PV']
    
            
        results_building_simulation[hour_of_year]['E_tot'] = np.nan
        results_building_simulation[hour_of_year]['E_HCL'] = np.nan
        results_building_simulation[hour_of_year]['H']  = np.nan
        results_building_simulation[hour_of_year]['C']  = np.nan
        results_building_simulation[hour_of_year]['L']  = np.nan
        results_building_simulation[hour_of_year]['PV']  = np.nan
        results_building_simulation[hour_of_year]['OptAngles'] = np.nan
        results_building_simulation[hour_of_year]['BestCombKey'] = np.nan
        results_building_simulation[hour_of_year]['T_in'] = np.nan
        results_building_simulation[hour_of_year]['T_out'] = np.nan
        results_building_simulation[hour_of_year]['RadiationWindow'] = np.nan
    
                     
    for hour_of_year in range(0,8760):
          
        
        #class Building   
        Office=Building (                
                        lighting_load= BuildingProperties['lighting_load'],
                        lighting_control = BuildingProperties["lighting_control"],
                        Lighting_Utilisation_Factor = BuildingProperties["Lighting_Utilisation_Factor"],
                        Lighting_MaintenanceFactor = BuildingProperties["Lighting_MaintenanceFactor"], 
                        c_m_A_f = BuildingProperties["c_m_A_f"],
                        ACH_vent = BuildingProperties["ACH_vent"],
                        ACH_infl = BuildingProperties["ACH_infl"],
                        ventilation_efficiency = BuildingProperties["ventilation_efficiency"],                   
                        phi_c_max_A_f= -np.inf,
                        phi_h_max_A_f= np.inf,
                        U_em= BuildingProperties["U_em"], 
                        U_w = BuildingProperties["U_w"],
                        glass_solar_transmitance=BuildingProperties['glass_solar_transmitance'],
                        glass_light_transmitance = BuildingProperties["glass_light_transmitance"],
                        theta_int_h_set = BuildingProperties['theta_int_h_set'],
                        theta_int_c_set = BuildingProperties['theta_int_c_set']
                        )
                        
                               
        if occupancy['People'][hour_of_year] == 0:
             Office.theta_int_h_set = BuildingProperties['theta_int_h_set'] - setBackTemp
             Office.theta_int_c_set = BuildingProperties['theta_int_c_set'] + setBackTemp
        else:
             Office.theta_int_h_set = 20
             Office.theta_int_c_set = 26                   
        
        
        #check all angle combinations and determine, which combination results in the smallest energy demand (min(E_tot))
        for comb in range(0, NumberCombinations):
            
            
            #print "Rad", BuildingRadiationData_HOY[hour_of_year][comb]
                    
            Q_internal = (Q_human[hour_of_year] + Q_equipment)
                    
            Office.solve_building_energy(phi_int = Q_internal, #internal heat gains, humans and equipment [W]
                                         phi_sol = BuildingRadiationData_HOY[hour_of_year][comb], #W
                                         theta_e = T_out[hour_of_year], 
                                         theta_m_prev = T_in)
        
                    
            
            #Calculate Illuminance in the room. 
            fenstIll=BuildingRadiationData_HOY[hour_of_year][comb]*Ill_Eq[0] #Lumens.  Note that the constant has been ignored because it should be 0
            #Illuminance after transmitting through the window         
            TransIll=fenstIll*Office.glass_light_transmitance
            
           
            Office.solve_building_lighting(ill = TransIll, 
                                           occupancy = occupancy['People'][hour_of_year])
    
            
            
            #save all combination results for one HOY
            
            Data_Lighting_HOY[hour_of_year][comb] = Office.lighting_demand # Watts
            Data_HC_HOY[hour_of_year][comb] = Office.phi_hc_nd_ac #achtung heating und cooling 
            Data_T_in_HOY[hour_of_year][comb] = Office.theta_m
            
            if Office.phi_hc_nd_ac > 0:
                Data_Heating_HOY[hour_of_year][comb] = Office.phi_hc_nd_ac
                Data_Cooling_HOY[hour_of_year][comb] = 0
            elif Office.phi_hc_nd_ac < 0:
                Data_Heating_HOY[hour_of_year][comb] = 0
                Data_Cooling_HOY[hour_of_year][comb] = -Office.phi_hc_nd_ac
            else:
                Data_Heating_HOY[hour_of_year][comb] = 0
                Data_Cooling_HOY[hour_of_year][comb] = 0
                
            
            #determine best combination for the evaluated HOY
            #integrate the needed actuation energy to calculate the real total energy demand 
            E_tot[hour_of_year][comb]=  Data_Heating_HOY[hour_of_year][comb] + Data_Cooling_HOY[hour_of_year][comb] + Data_Lighting_HOY[hour_of_year][comb] - hourlyData[hour_of_year]['PV'][comb]
            E_HCL[hour_of_year][comb] = Data_Heating_HOY[hour_of_year][comb] + Data_Cooling_HOY[hour_of_year][comb] + Data_Lighting_HOY[hour_of_year][comb]
            
        hourlyData[hour_of_year]['HC'] = Data_HC_HOY[hour_of_year]
        hourlyData[hour_of_year]['H'] = Data_Heating_HOY[hour_of_year]
        hourlyData[hour_of_year]['C'] = Data_Cooling_HOY[hour_of_year]    
        hourlyData[hour_of_year]['L'] = Data_Lighting_HOY[hour_of_year]       
        hourlyData[hour_of_year]['E_tot'] = E_tot[hour_of_year]
        hourlyData[hour_of_year]['E_HCL'] = E_HCL[hour_of_year]
        hourlyData[hour_of_year]['T_out'] =T_out[hour_of_year]
        hourlyData[hour_of_year]['T_in'] = Data_T_in_HOY[hour_of_year]
        hourlyData[hour_of_year]['AngleComb'] = combinationAngles
        hourlyData[hour_of_year]['RadiationWindow'] = BuildingRadiationData_HOY[hour_of_year] #W
        
        """
        set the key to NumberCombinations if there is no adjustment of the ASF, set legend to balck for this value
        
        """        
        
        if optimization_type == 'E_total':
      
            #Best comb for overall energy demand
            if hour_of_year == 0:
            #initial condition        
                BestComb = 0
                BestCombKey = NumberCombinations # = np.nan
            
            if hourlyData[hour_of_year]['PV'][0] != 0:
                #get key with min value from the E_tot dictionary
                BestComb = min(E_tot[hour_of_year], key=lambda comb: E_tot[hour_of_year][comb])
                BestCombKey = BestComb       
               
            elif hourlyData[hour_of_year]['PV'][0] == 0 and hour_of_year != 0:
                #Check if there is no PV-value (nor radiation), then don't move the modules
                BestComb = BestComb        
                BestCombKey = NumberCombinations
       
        elif optimization_type == 'Heating':    
        
            #best comb for heating
            if hour_of_year == 0:
            #initial condition        
                BestComb = 0
                BestCombKey = NumberCombinations # = np.nan
                
            elif hourlyData[hour_of_year]['PV'][0] != 0:
                #get key with min value from the E_tot dictionary
                
                BestComb = min(Data_Heating_HOY[hour_of_year], key=lambda comb: Data_Heating_HOY[hour_of_year][comb])
                                
                if Data_Heating_HOY[hour_of_year][0] == 0:
                    
                    BestComb = 0
                    BestCombKey =NumberCombinations + 1
                else:
                    BestCombKey = BestComb
        
            elif hourlyData[hour_of_year]['PV'][0] == 0 and hour_of_year != 0:
                #Check if there is no PV-value (nor radiation), then don't move the modules
                BestComb = BestComb # take same comb value from the hour before       
                BestCombKey = NumberCombinations
        
        elif optimization_type == 'Cooling':
            #best comb for heating
            if hour_of_year == 0:
            #initil condition        
                BestComb = 0
                BestCombKey = NumberCombinations # = np.nan
                
            elif hourlyData[hour_of_year]['PV'][0] != 0:
                #get key with min value from the E_tot dictionary
                BestComb = min(Data_Cooling_HOY[hour_of_year], key=lambda comb: Data_Cooling_HOY[hour_of_year][comb])
                                
                if Data_Cooling_HOY[hour_of_year][0] == 0:
                    BestComb = 0                    
                    BestCombKey = NumberCombinations + 1 # = -100.
                else:
                    BestCombKey = BestComb
        
            elif hourlyData[hour_of_year]['PV'][0] == 0 and hour_of_year != 0:
                #Check if there is no PV-value (nor radiation), then don't move the modules
                BestComb = BestComb        
                BestCombKey = NumberCombinations
                
        elif optimization_type == 'Lighting':
            #best comb for heating
            if hour_of_year == 0:
            #initil condition        
                BestComb = 0
                BestCombKey = NumberCombinations
                
            if hourlyData[hour_of_year]['PV'][0] != 0:
                #get key with min value from the E_tot dictionary
                BestComb =BuildingRadiationData_HOY[hour_of_year].argmax(axis=0)
                BestCombKey = BestComb
              
        
            elif hourlyData[hour_of_year]['PV'][0] == 0 and hour_of_year != 0:
                #Check if there is no PV-value (nor radiation), then don't move the modules
                BestComb = BestComb       
                BestCombKey = NumberCombinations
                
                
        elif optimization_type == 'SolarEnergy':
            #best comb for heating
            if hour_of_year == 0:
            #initil condition        
                BestComb = 0
                BestCombKey = NumberCombinations
                
            if hourlyData[hour_of_year]['PV'][0] != 0:
                #get key with min value from the dictionary
                BestComb = hourlyData[hour_of_year]['PV'].argmax(axis=0)
                BestCombKey = BestComb                
                        
            elif hourlyData[hour_of_year]['PV'][0] == 0 and hour_of_year != 0:
                #Check if there is no PV-value (nor radiation), then don't move the modules
                BestComb = BestComb        
                BestCombKey = NumberCombinations
                
        elif optimization_type == 'E_HCL':
            #best comb for heating
            if hour_of_year == 0:
            #initil condition        
                BestComb = 0
                BestCombKey = NumberCombinations
                
            if hourlyData[hour_of_year]['PV'][0] != 0:
                #get key with min value from the dictionary
                BestComb = min(E_HCL[hour_of_year], key=lambda comb: E_HCL[hour_of_year][comb])
                                
                if E_HCL[hour_of_year][0] == 0:
                    BestCombKey = NumberCombinations+1
                else:
                    BestCombKey = BestComb
        
            elif hourlyData[hour_of_year]['PV'][0] == 0 and hour_of_year != 0:
                #Check if there is no PV-value (nor radiation), then don't move the modules
                BestComb = BestComb        
                BestCombKey = NumberCombinations
        
            
        
        T_in = Data_T_in_HOY[hour_of_year][BestComb] #most efficient solution has to be used again
        
    
        #count uncomfortable hours
        if (T_in > 26.0 or T_in < 20.0): #and occupancy['People'][hour_of_year] != 0:#T_in > BuildingProperties['theta_int_c_set'] or T_in < BuildingProperties['theta_int_h_set']:
            uncomf_hours += 1
            uncomf_hours_HOY.append(hour_of_year)
            
        
        #save optimal results in a dictionary and convert to a DataFrame   
        results_building_simulation[hour_of_year]['E_tot'] = hourlyData[hour_of_year]['E_tot'][BestComb]
        results_building_simulation[hour_of_year]['E_HCL'] =hourlyData[hour_of_year]['E_HCL'][BestComb]
        results_building_simulation[hour_of_year]['HC']  = hourlyData[hour_of_year]['HC'][BestComb]
        results_building_simulation[hour_of_year]['H']  = hourlyData[hour_of_year]['H'][BestComb]
        results_building_simulation[hour_of_year]['C']  = hourlyData[hour_of_year]['C'][BestComb]
        results_building_simulation[hour_of_year]['L']  = hourlyData[hour_of_year]['L'][BestComb]
        results_building_simulation[hour_of_year]['PV']  = hourlyData[hour_of_year]['PV'][BestComb]
        results_building_simulation[hour_of_year]['OptAngles'] = combinationAngles[BestComb]   
        results_building_simulation[hour_of_year]['BestCombKey'] = [BestCombKey]
        results_building_simulation[hour_of_year]['T_in'] = Data_T_in_HOY[hour_of_year][BestComb]
        results_building_simulation[hour_of_year]['T_out'] = hourlyData[hour_of_year]['T_out']
        results_building_simulation[hour_of_year]['RadiationWindow'] = BuildingRadiationData_HOY[hour_of_year][BestComb] #W
        
        #show which HOY is calculated
        if hour_of_year % 1000 == 0 and hour_of_year != 0:
            print 'HOY:', hour_of_year
            toc = time.time() - tic
            print 'time passed (min): ' + str(toc/60.)
            
    
    #store results of the best angle combinations in DataFrame   
    Building_Simulation_df= pd.DataFrame(results_building_simulation).T    
    hourlyData_df = pd.DataFrame(hourlyData)
     
    print "\nEnd of RC-Model calculation: " + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
    print "uncomfortable Hours: ", uncomf_hours
    
    
    return  hourlyData_df,Building_Simulation_df