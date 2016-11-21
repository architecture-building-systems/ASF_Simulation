"""
=========================================
main file for simulation environment
=========================================
"""


"""
@author: Mauro Luzzatto 
@credits: Prageeth Jayathissa, Jerimias Schmidli

02.11.2016
"""


"""
Description of the code 


HOW TO USE:
- Open the main_new_mauro.GH file in Grasshopper
- Set the location in the Grasshopper file to same Location as defined in geoLoaction in this script
- Set both red framed boolean toggles to true 
- Set all needed values for evaluation at the beginning of the main.py script

if LadyBug once has calculated all the radiation data, they will be stored in the folder with the corresponding DataName. 
Also the Data of the PV producation and radiation hitting the window will be saved and can be loaded again, with the same DataName.


VARIABLE DEFINITION

   geoLocation: set the location which should be evaluated, make sure the correspoding .epw file is saved in the WeatherData folder
   Save: decide weather you want to save (True) or not save (False) the results
   optimization_Types: Decide for which energy demand type, you want to do the optimisation for
   DataName: choose the name for the stored data
   XANGLES = set the X-Angles of the ASF = [0, 15, 30, 45, 60, 75, 90] , 0 = closed, 90 = open
   YANGLES = set the Y-Angles of the ASF = [-45, -30,-15,0, 15, 30, 45] 
   NoClusters = option for using different multiple clusters
   ActuationEnergy = choose weather you want to include the the needed actuation energy for the ASF adjustment
   room_width =     
   room_height =
   room_depth = 
   glazing_percentage_w = perecentage of glazing of the total room width
   glazing_percentage_h =  perecentage of glazing of the total room height


	
INPUT PARAMETER DEFINITION 

	Fenst_A: Area of the Glazed Surface  [m2]
	Room_Depth=7.0 Depth of the modeled room [m]
	Room_Width=4.9 Width of the modeled room [m]
	Room_Height=3.1 Height of the modeled room [m]
	glass_solar_transmitance: Fraction of Radiation transmitting through the window []
	glass_light_transmitance: Fraction of visible light (luminance) transmitting through the window []
	lighting_load: Lighting Load [W/m2] 
	lighting_control: Lux threshold at which the lights turn on [Lx]
	U_em: U value of opaque surfaces  [W/m2K]
	U_w: U value of glazed surfaces [W/m2K]
	ACH_vent: Air changes per hour through ventilation [Air Changes Per Hour]
	ACH_infl: Air changes per hour through infiltration [Air Changes Per Hour]
	ventilation_efficiency: The efficiency of the heat recovery system for ventilation. Set to 0 if there is no heat recovery []
	c_m_A_f: Thermal capacitance of the room per floor area [J/m2K] #capcitance of the building dependent on building type: medium = 165'000, heavy = 260'000, light = 110'000, very heavy = 370'000
	theta_int_h_set : Thermal heating set point [C]
	theta_int_c_set: Thermal cooling set point [C]
	phi_c_max_A_f: Maximum cooling load. Set to -np.inf for unresctricted cooling [C]
	phi_h_max_A_f: Maximum heating load. Set to no.inf for unrestricted heating [C]

"""



import os, sys
import numpy as np
import pandas as pd
from buildingSystem import *  


# 'ZH13_49comb'
# 'Zuerich_Kloten_2013.epw'

for ii in [0,1,2]: #[2]

    
    print "start"
    
    Data = {'Name' : ['ZH13_49comb_cloudy_4_7', 'ZH13_49comb_Notcloudy_6_7', 'ZH13_49comb_Halfcloudy_10_7'],
            'day' : [4,6,10]}
    
    
    
    #DefaultValues
    ###############################################################################
    SimulationPeriod = {
    'FromMonth': 7,
    'ToMonth':7,
    'FromDay': Data['day'][ii],
    'ToDay': Data['day'][ii],
    'FromHour': 5,
    'ToHour': 19}
    
    
    
    #Set simulation data
    SimulationData= {
    'optimizationTypes' : ['E_total'],# 'Heating','Cooling', 'SolarEnergy', 'E_HCL', 'Lighting'],
    'DataName' : Data['Name'][ii],
    'geoLocation' : 'Zuerich_Kloten_2013',
    'Save' : False}
    
    #Set panel data
    PanelData={
    "XANGLES": [0, 15, 30, 45, 60, 75, 90],
    "YANGLES" : [-45,-30,-15, 0, 15, 30, 45],
    "NoClusters":1,
    "numberHorizontal":6,
    "numberVertical":9,
    "panelOffset":400,
    "panelSize":400,
    "panelSpacing":500}
    
    #Set Building Parameters in [mm]
    BuildingData={
    "room_width": 4900,     
    "room_height":3100,
    "room_depth":7000,
    "glazing_percentage_w": 0.92,
    "glazing_percentage_h": 0.97}
    
    #Set building properties for RC-Model simulator
    BuildingProperties={
    "glass_solar_transmitance" : 0.687 ,
    "glass_light_transmitance" : 0.744 ,
    "lighting_load" : 11.74 ,
    "lighting_control" : 300,
    "Lighting_Utilisation_Factor" :  0.45,
    "Lighting_MaintenanceFactor" : 0.9,
    "U_em" : 0.2, 
    "U_w" : 1.2,
    "ACH_vent" : 1.5,
    "ACH_infl" :0.5,
    "ventilation_efficiency" : 0.6 ,
    "c_m_A_f" : 165 * 10**3,
    "theta_int_h_set" : 20,
    "theta_int_c_set" : 26,
    "phi_c_max_A_f": -np.inf,
    "phi_h_max_A_f":np.inf,
    "heatingSystem" : DirectHeater, #DirectHeater, #ResistiveHeater #HeatPumpHeater
    "coolingSystem" : DirectCooler, #DirectCooler, #HeatPumpCooler
    "heatingEfficiency" : 1,
    "coolingEfficiency" :1}
    
    #Set simulation Properties
    SimulationOptions= {
    'setBackTemp' : 0.,
    'Occupancy' : 'Occupancy_COM.csv',
    'ActuationEnergy' : False}
    
    ###############################################################################
    
    def MainCalculateASF(SimulationPeriod, SimulationData, PanelData, BuildingData, BuildingProperties, SimulationOptions):
        
        # add python_path to system path, so that all files are available:
        sys.path.insert(0, os.path.abspath(os.path.dirname(sys.argv[0])))
        sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'python'))
        
        from simulationFunctions_hourly import initializeSimulation, initializeASF, setBuildingParameters, initializeBuildingSimulation, setPaths, CalculateVariables  
        from simulationFunctions_hourly import PrepareRadiationData, runRadiationCalculation, runBuildingSimulation, SaveResults 
        from calculateHOY import calcHOY
        
      
        start =calcHOY(month = SimulationPeriod['FromMonth'], day = SimulationPeriod['FromDay'], hour = SimulationPeriod['FromHour'])
        end = calcHOY(month = SimulationPeriod['ToMonth'], day = SimulationPeriod['ToDay'], hour = SimulationPeriod['ToHour'])
        
        print "\nThe simulation starts at the hour of the year: " + str(start) + " and ends at: " + str(end) + "\n"
        
        
        FolderName = initializeSimulation(SimulationData = SimulationData)
                                                
                
        initializeASF(panel_data = PanelData)
       
        
        roomFloorArea = setBuildingParameters(
                                 building_data = BuildingData)
                                
        
        BuildingProperties = initializeBuildingSimulation(
                                 building_data = BuildingData,    
                                 BuildingProperties = BuildingProperties)
                        
        
        paths, weatherData, SunTrackingData = setPaths(
                                  geoLocation = SimulationData['geoLocation'], 
                                  Occupancy = SimulationOptions['Occupancy'],
                                  FolderName = FolderName)
        
        
        ANGLES, hour_in_month, NumberCombinations, combinationAngles, daysPerMonth, \
        hourRadiation, hourRadiation_calculated, sumHours = CalculateVariables(
                                SunTrackingData = SunTrackingData, 
                                building_data = BuildingData, 
                                XANGLES = PanelData['XANGLES'], 
                                YANGLES = PanelData['YANGLES'])
        
        PV_electricity_results, PV_detailed_results, HourlyRadiation, now = runRadiationCalculation(
                                SimulationPeriode = SimulationPeriod,
                                paths = paths, 
                                XANGLES = PanelData['XANGLES'], 
                                YANGLES = PanelData['YANGLES'], 
                                hour_in_month = hour_in_month, 
                                FolderName = FolderName,
                                panel_data = PanelData, 
                                NumberCombinations = NumberCombinations, 
                                createPlots = False, 
                                start = start, end = end)
                        
    
        #rearrange the Radiation Data on PV and Window into HOY form
        PV_Data, BuildingRadiationHOY = PrepareRadiationData(
                                HourlyRadiation = HourlyRadiation, 
                                PV_electricity_results = PV_electricity_results, 
                                NumberCombinations = NumberCombinations,
                                SimulationPeriode = SimulationPeriod,
                                start = start, end = end)
                                
        #return PV_Data, BuildingRadiationHOY, PV_electricity_results
                   
        hourlyData, ResultsBuildingSimulation, BestKey, x_angles, y_angles = runBuildingSimulation(
                                geoLocation = SimulationData['geoLocation'], 
                                paths = paths, 
                                optimization_Types = SimulationData['optimizationTypes'], 
                                building_data =  BuildingData, 
                                weatherData = weatherData, 
                                hourRadiation = hourRadiation, 
                                BuildingRadiationData_HOY = BuildingRadiationHOY, 
                                PV = PV_Data, 
                                NumberCombinations = NumberCombinations, 
                                combinationAngles = combinationAngles, 
                                BuildingProperties = BuildingProperties, 
                                setBackTemp = SimulationOptions['setBackTemp'], 
                                daysPerMonth = daysPerMonth, 
                                ANGLES = ANGLES,
                                start = start,
                                end = end)
        
        #print "calucation is finished"
                                   
            
        ResultsBuildingSimulation, angles_df, anglesHOY = SaveResults(
                                now = now, 
                                Save = SimulationData['Save'], 
                                geoLocation = SimulationData['geoLocation'], 
                                paths = paths, 
                                optimization_Types = SimulationData['optimizationTypes'],  
                                ResultsBuildingSimulation = ResultsBuildingSimulation, 
                                BuildingProperties = BuildingProperties,
                                x_angles = x_angles,
                                y_angles = y_angles,
                                SimulationData = SimulationData)
        print "calucation is finished"
                        
        return ResultsBuildingSimulation, angles_df, anglesHOY                       
    

    ResultsBuildingSimulation, angles_df, anglesHOY = MainCalculateASF(SimulationPeriod, SimulationData, PanelData, BuildingData, BuildingProperties, SimulationOptions)
    
    
    
