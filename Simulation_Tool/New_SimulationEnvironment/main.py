# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:14:42 2016

main file for simulation environment

@author: Mauro Luzzatto 
@credits: Prageeth Jayathissa, Jerimias Schmidli

02.11.2016

Make sure: 
- main_new_mauro.GH file is open in Grasshopper
- both red framed boolean toggles are set to true 
- the needed epw-file is chosen, the same as set at geoLocation

"""

import os, sys
import numpy as np
import pandas as pd


# add python_path to system path, so that all files are available:
sys.path.insert(0, os.path.abspath(os.path.dirname(sys.argv[0])))
sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'python'))



def main():
    
    from simulationFunctions import initializeSimulation, initializeASF, setBuildingParameters, initializeBuildingSimulation 
    from simulationFunctions import setPaths, CalculateVariables, runRadiationCalculation, runBuildingSimulation, createAllPlots, SaveResults 
    from prepareDataMain import PrepareRadiationData
    
        
    geoLocation, Save, optimization_Types = initializeSimulation(
                               geoLocation = 'Zuerich_Kloten_2005', 
                               Save = False, 
                               optimization_Types = ['E_total','Heating','Cooling', 'SolarEnergy', 'E_HCL', 'Lighting'])
       
        
    panel_data = initializeASF(XANGLES = [0, 15, 30, 45, 60, 75, 90], 
                               YANGLES= [-45,-30,-15,0, 15, 30, 45], 
                               NoClusters = 1, #not working yet
                               ActuationEnergy = False) #not working yet
    
    
    
    building_data, roomFloorArea = setBuildingParameters(
                            room_width = 4900,     
                            room_height = 3100,
                            room_depth = 7000,
                            glazing_percentage_w = 0.92,
                            glazing_percentage_h = 0.97) 
    
    BuildingProperties, setBackTemp, Occupancy = initializeBuildingSimulation(
                            building_data = building_data,    
                            glass_solar_transmitance = 0.687 ,
                            glass_light_transmitance = 0.744 ,
                            lighting_load = 11.74 ,
                            lighting_control = 300,
                            Lighting_Utilisation_Factor = 0.45,
                            Lighting_MaintenanceFactor = 0.9,
                            U_em = 0.2, 
                            U_w = 1.2,
                            ACH_vent = 1.5,
                            ACH_infl = 0.5,
                            ventilation_efficiency = 0.6,
                            c_m_A_f = 165 * 10**3, #capcitance of the building dependent on building type: medium = 165'000, heavy = 260'000, light = 110'000, very heavy = 370'000
                            theta_int_h_set = 20,
                            theta_int_c_set = 26,
                            phi_c_max_A_f = -np.inf, 
                            phi_h_max_A_f = np.inf,
                            setBackTemp = 4.,
                            Occupancy = 'Occupancy_COM.csv')
    
    ###########################################################################    
    
    paths, weatherData, SunTrackingData = setPaths(
                                geoLocation = geoLocation, 
                                Occupancy = Occupancy)
    
    
    ANGLES, hour_in_month, NumberCombinations, combinationAngles, daysPerMonth, \
    hourRadiation, hourRadiation_calculated, sumHours = CalculateVariables(
                                SunTrackingData = SunTrackingData, 
                                building_data = building_data, 
                                XANGLES = panel_data['XANGLES'], 
                                YANGLES = panel_data['YANGLES'])
    
    PV_electricity_results, PV_detailed_results, \
    BuildingRadiationData_HOD, now = runRadiationCalculation(
                                paths = paths, 
                                XANGLES = panel_data['XANGLES'], 
                                YANGLES = panel_data['YANGLES'], 
                                daysPerMonth = daysPerMonth, 
                                hour_in_month = hour_in_month, 
                                DataName = None, 
                                panel_data = panel_data, 
                                NumberCombinations = NumberCombinations, 
                                createPlots = False, 
                                simulationOption = {'timePeriod' : None})
     
     
    #rearrange the Radiation Data on PV and Window into HOY form
    PV, BuildingRadiationData_HOY = PrepareRadiationData(
                            hour_in_month = hour_in_month, 
                            daysPerMonth = daysPerMonth, 
                            BuildingRadiationData_HOD = BuildingRadiationData_HOD, 
                            PV_electricity_results = PV_electricity_results, 
                            NumberCombinations = NumberCombinations)
    
                 
    hourlyData, monthlyData, yearlyData, ResultsBuildingSimulation, \
    BestKey_df, x_angles, y_angles = runBuildingSimulation(
                            geoLocation = geoLocation, 
                            paths = paths, 
                            optimization_Types = optimization_Types, 
                            building_data =  building_data, 
                            weatherData = weatherData, 
                            hourRadiation = hourRadiation, 
                            BuildingRadiationData_HOY = BuildingRadiationData_HOY, 
                            PV = PV, 
                            NumberCombinations = NumberCombinations, 
                            combinationAngles = combinationAngles, 
                            BuildingProperties = BuildingProperties, 
                            setBackTemp = setBackTemp, 
                            daysPerMonth = daysPerMonth, 
                            ANGLES = ANGLES)
        
    fig0, fig1, fig2 = createAllPlots(
                                monthlyData = monthlyData, 
                                roomFloorArea = roomFloorArea, 
                                x_angles = x_angles, 
                                y_angles = y_angles, 
                                hour_in_month = hour_in_month, 
                                optimization_Types = optimization_Types)
       
      
        
    ResultsBuildingSimulation, monthlyData, yearlyData \
                            = SaveResults(
                            now = now, 
                            Save = Save, 
                            geoLocation = geoLocation, 
                            paths = paths, 
                            fig0 = fig0, 
                            fig1 = fig1, 
                            fig2 = fig2, 
                            optimization_Types = optimization_Types,  
                            monthlyData = monthlyData, 
                            yearlyData = yearlyData, 
                            ResultsBuildingSimulation = ResultsBuildingSimulation, 
                            BuildingProperties = BuildingProperties)
                            
    return ResultsBuildingSimulation, monthlyData, yearlyData

ResultsBuildingSimulation, monthlyData, yearlyData = main()