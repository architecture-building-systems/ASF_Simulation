# -*- coding: utf-8 -*-
"""
Created on Wed Nov 09 11:53:33 2016

@author: Mauro
"""
import unittest
import sys,os
import numpy as np
from buildingSystem import *  
from SimulationClass import ASF_Simulation


class TestMainSimulation2(unittest.TestCase):


	def test_ELEC2013(self):
		#Set simulation data
		print 'running elec test'
		SimulationData= {
		'optimizationTypes' : ['E_total_elec'],
		'DataFolderName' : 'ZH13_49comb',
		'FileName': 'ZH13_49comb',
		'geoLocation' : 'Zuerich_Kloten_2013',
		'EPWfile' : 'Zuerich_Kloten_2013.epw',
		'Save' : False,
		'ShowFig': False}
		
		#Set panel data
		PanelData={
		"XANGLES": [0, 15, 30, 45, 60, 75, 90],
		"YANGLES" : [-45, -30,-15,0, 15, 30, 45],
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
		"phi_h_max_A_f": np.inf,
		"heatingSystem" : DirectHeater, 
		"coolingSystem" : DirectCooler, 
		"heatingEfficiency" : 1,
		"coolingEfficiency" :1,
		"COP_H": 1,
		"COP_C":1}
		
		#Set simulation Properties
		SimulationOptions= {
            'setBackTempH' : 4.,
            'setBackTempC' : 4., 
            'Occupancy' : 'Occupancy_COM.csv',
            'ActuationEnergy' : False, 
            "Temp_start" : 20, 
            'human_heat_emission' : 0.12,}
                     
		
		
		ASFtest=ASF_Simulation(SimulationData = SimulationData, PanelData = PanelData, BuildingData = BuildingData, BuildingProperties = BuildingProperties, SimulationOptions = SimulationOptions)
		ASFtest.SolveASF()
		
																					 
		self.assertEqual(round(ASFtest.yearlyData['E_total_elec']['E_elec'],2), 1419.46)
		self.assertEqual(round(ASFtest.yearlyData['E_total_elec']['PV'],2), -723.99)
		self.assertEqual(ASFtest.ResultsBuildingSimulation['E_total_elec']['BestCombKey'][38],46)



if __name__ == '__main__':
	unittest.main()

	