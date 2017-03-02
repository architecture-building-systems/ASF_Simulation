# -*- coding: utf-8 -*-
"""
Created on Wed Nov 09 11:53:33 2016

@author: Mauro
"""
import unittest
import sys,os
import numpy as np
from buildingSystem import *  
from SimulationClassPlanarProjection import ASF_Simulation




class TestMainSimulation(unittest.TestCase):
	
    def test_SummerStandard(self):
        print 'Standard Planar Projection Test: Sunny Summer Day'       

        SimulationPeriod = {
        'FromMonth': 7,
        'ToMonth': 7,
        'FromDay': 6,
        'ToDay': 6, 
        'FromHour': 5,
        'ToHour': 20}
        
        PlanarProjectionSettings = {
        'ShadingCase' : ['1','2','3'],
        'reflectance' : 0,
        'DistWindow' : 300, #Distance from the Glazed Surface
        'shadingPV' : True }
        
        #Set simulation data 
        SimulationData= {
        'optimizationTypes' : ['E_total'], 
        'FileName' : 'ZH13_49comb_SummerSunnyDay_PP',
        'geoLocation' : 'Zuerich_Kloten_2013', 
        'Save' : False, 
        'ShowFig': True, 
        'timePeriod': None} # asf_electricity_function  
        
         
        PanelData = {
        "XANGLES": [0, 15, 30, 45, 60, 75, 90],
        "YANGLES" : [-45, -30,-15,0, 15, 30, 45],
        "NoClusters":1,
        "numberHorizontal":6,
        "numberVertical":9,
        "panelSize":400.,
        "panelSpacing":500.}
        
        
        BuildingData={
        "room_width": 4900,     
        "room_height":3100,
        "room_depth":7000,
        "glazing_percentage_w": 0.92,
        "glazing_percentage_h": 0.97,
        "BuildingOrientation" : 0} 
        
        
        BuildingProperties={
        "glass_solar_transmitance" : 0.691 ,
        "glass_light_transmitance" : 0.744 ,
        "lighting_load" : 11.74 ,
        "lighting_control" : 300,
        "Lighting_Utilisation_Factor" :  0.45, # 0.75
        "Lighting_MaintenanceFactor" : 0.9,
        "U_em" : 0.2, 
        "U_w" : 1.1,
        "ACH_vent" : 1.5,
        "ACH_infl" : 0.5,
        "ventilation_efficiency" : 0.6,
        "c_m_A_f" : 165 * 10**3,
        "theta_int_h_set" : 22,
        "theta_int_c_set" : 26,
        "phi_c_max_A_f": -np.inf,
        "phi_h_max_A_f":np.inf,
        "heatingSystem" : DirectHeater, 
        "coolingSystem" : DirectCooler, 
        "heatingEfficiency" : 1,
        "coolingEfficiency" :1,
        'COP_H': 3,
        'COP_C':3}
        #
        #Set simulation Properties
        SimulationOptions= {
        'setBackTempH' : 4.,
        'setBackTempC' : 4.,
        'Occupancy' : 'Occupancy_COM.csv',
        'ActuationEnergy' : False,
        'Temp_start' : 22,
        'human_heat_emission' : 0.12} #[kWh] heat emitted by a human body per hour. Source: HVAC Engineers Handbook, F. Porges
           

    
        ASFtest = ASF_Simulation(SimulationPeriod = SimulationPeriod,
                                 PlanarProjectionSettings = PlanarProjectionSettings,
                                 SimulationData = SimulationData, 
                                 PanelData = PanelData,
                                 BuildingData = BuildingData,
                                 BuildingProperties = BuildingProperties, 
                                 SimulationOptions = SimulationOptions)
		
        ASFtest.SolveASF()
        		
        self.assertEqual(round(ASFtest.TotalHourlyData['E_total']['E'],2), -3.71)
        self.assertEqual(round(ASFtest.TotalHourlyData['E_total']['PV'],2), -5.74)
        self.assertEqual(ASFtest.ResultsBuildingSimulation['E_total']['BestCombKey'][4476],39)
        
		
    	

  

if __name__ == '__main__':
	unittest.main()