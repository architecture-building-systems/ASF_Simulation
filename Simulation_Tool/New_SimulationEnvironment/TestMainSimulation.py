# -*- coding: utf-8 -*-
"""
Created on Wed Nov 09 11:53:33 2016

@author: Mauro
"""
import unittest
import sys,os
import numpy as np
from buildingSystem import *  

sys.path.insert(0, os.path.abspath(os.path.dirname(sys.argv[0])))        
from mainSimulation import MainCalculateASF



class TestMainSimulation(unittest.TestCase):
	
		

	def test_Standard(self):
		#Set simulation data
		print 'running standard test'
		SimulationData= {
		'optimizationTypes' : ['E_total'],
		'DataName' : 'ZH05_49comb',
		'geoLocation' : 'Zuerich_Kloten_2005',
		'EPWfile' : 'Zuerich_Kloten_2005.epw',
		'Save' : True,
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
		"heatingSystem" : DirectHeater, #DirectHeater, #ResistiveHeater #HeatPumpHeater
		"coolingSystem" : DirectCooler, #DirectCooler, #HeatPumpCooler
		"heatingEfficiency" : 1,
		"coolingEfficiency" :1}
		
		#Set simulation Properties
		SimulationOptions= {
		'setBackTemp' : 4.,
		'Occupancy' : 'Occupancy_COM.csv',
		'ActuationEnergy' : False}
		
		
		ResultsBuildingSimulation, monthlyData, yearlyData = MainCalculateASF(SimulationData = SimulationData, 
																			  PanelData = PanelData, 
																			  BuildingData = BuildingData, 
																			  BuildingProperties = BuildingProperties, 
																			  SimulationOptions = SimulationOptions)
		
		self.assertEqual(round(yearlyData['E_total']['E'],2), 1189.82)
		self.assertEqual(round(yearlyData['E_total']['PV'],2), -707.01)
		#self.assertEqual(round(monthlyData['H'][0],2),3.56)
		self.assertEqual(ResultsBuildingSimulation['E_total']['BestCombKey'][38],[5])
		
		
	def atest_ELEC2013(self):
		#Set simulation data
		print 'running elec test'
		SimulationData= {
		'optimizationTypes' : ['E_total_elec'],
		'DataName' : 'ZH13_49comb',
		'geoLocation' : 'Zuerich_Kloten_2013',
		'EPWfile' : 'Zuerich_Kloten_2013.epw',
		'Save' : False,
		'ShowFig': True}
		
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
		"heatingSystem" : DirectHeater, #DirectHeater, #ResistiveHeater #HeatPumpHeater
		"coolingSystem" : DirectCooler, #DirectCooler, #HeatPumpCooler
		"heatingEfficiency" : 1,
		"coolingEfficiency" :1}
		
		#Set simulation Properties
		SimulationOptions= {
		'setBackTemp' : 4.,
		'Occupancy' : 'Occupancy_COM.csv',
		'ActuationEnergy' : False}
		
		
		ResultsBuildingSimulation, monthlyData, yearlyData = MainCalculateASF(SimulationData = SimulationData, 
																			  PanelData = PanelData, 
																			  BuildingData = BuildingData, 
																			  BuildingProperties = BuildingProperties, 
																			  SimulationOptions = SimulationOptions)
		
		self.assertEqual(round(yearlyData['E_total_elec']['E_elec'],2), 1408.88)
		self.assertEqual(round(yearlyData['E_total_elec']['PV'],2), -727.06)
		self.assertEqual(ResultsBuildingSimulation['E_total_elec']['BestCombKey'][38],[45])
	


if __name__ == '__main__':
	unittest.main()