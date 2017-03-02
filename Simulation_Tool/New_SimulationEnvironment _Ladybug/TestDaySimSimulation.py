# -*- coding: utf-8 -*-
"""
Created on Wed Nov 09 11:53:33 2016

@author: Mauro
"""
import unittest
import sys,os
import numpy as np
from buildingSystem import *  
from SimulationClassDaySim import ASF_Simulation



class TestMainSimulation(unittest.TestCase):
	

    def test_Standard(self):
        print 'Standard Test DaySim: year withouth reflectance'
        
        SimulationData = {
        'optimizationTypes' : ['E_total', 'Cooling'],
        'DataFolderName' : 'DaySimZH13YearMat0', 
        'FileName': 'DaySimZH13YearMat0', 
        'ProjectName': 'Mat0',
        'SubFolder': '2ASF',
        'Save' : False,
        'ShowFig': True,
        'start' : 0,
        'end': 8760} 
        
        PanelData = {
        "XANGLES": [0,15,30,45,60,75,90],
        "YANGLES" : [-45,-30,-15,0,15,30,45]}
        
        Material = {
        'ASF' : 0,
        'Window': 0}
        
        BuildingProperties = {"glass_solar_transmitance" : 0.691,
        "glass_light_transmitance" : 0.744,
        "lighting_load" : 11.74,
        "lighting_control" : 300,
        "Lighting_Utilisation_Factor" :  0.6,
        "Lighting_MaintenanceFactor" : 0.9,
        "U_em" : 0.2,
        "U_w" : 1.1,
        "ACH_vent" : 1.5,
        "ACH_infl" :0.5,
        "ventilation_efficiency" : 0.6 ,
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
        
        SimulationOptions= {
        'setBackTempH' : 4.,
        'setBackTempC' : 4., 
        'Occupancy' : 'Occupancy_COM.csv',
        'ActuationEnergy' : False,
        'human_heat_emission' : 0.12,
        'Temp_start' : 20}
        
        ASFtest = ASF_Simulation(SimulationData = SimulationData, 
                             PanelData = PanelData, 
                             Material = Material, 
                             BuildingProperties = BuildingProperties,
                             SimulationOptions = SimulationOptions)
        ASFtest.SolveASF()
        
        self.assertEqual(round(ASFtest.yearlyData['E_total']['E'],2), 604.85)
        self.assertEqual(round(ASFtest.yearlyData['E_total']['PV'],2), -815.75)
        self.assertEqual(round(ASFtest.yearlyData['E_total']['AE'],2), 0)
        self.assertEqual(ASFtest.ResultsBuildingSimulation['E_total']['BestCombKey'][180],10)
        self.assertEqual(round(ASFtest.yearlyData['Cooling']['E'],2), 834.84)
        self.assertEqual(round(ASFtest.yearlyData['Cooling']['PV'],2), -736.92)
        self.assertEqual(round(ASFtest.yearlyData['Cooling']['AE'],2), 0)

if __name__ == '__main__':
	unittest.main()