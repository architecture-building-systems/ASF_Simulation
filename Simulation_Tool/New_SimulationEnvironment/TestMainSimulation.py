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

#sys.path.insert(0, os.path.abspath(os.path.dirname(sys.argv[0])))        
#from mainSimulation import MainCalculateASF



class TestMainSimulation(unittest.TestCase):
	
		     
        

	def test_Standard(self):
		#Set simulation data
		print 'running standard test'
		SimulationData= {
		'optimizationTypes' : ['E_total'],
		'DataFolderName' : 'ZH05_49comb',
		'FileName': 'ZH05_49comb',
		'geoLocation' : 'Zuerich_Kloten_2005',
		'EPWfile' : 'Zuerich_Kloten_2005.epw',
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
		"heatingSystem" : DirectHeater, #DirectHeater, #ResistiveHeater #HeatPumpHeater
		"coolingSystem" : DirectCooler, #DirectCooler, #HeatPumpCooler
		"heatingEfficiency" : 1,
		"coolingEfficiency" :1,
           "COP_H": 1,
           "COP_C":1}
		
		#Set simulation Properties
		SimulationOptions= {
		'setBackTempH' : 4.,
		'setBackTempC': 4,
		'Occupancy' : 'Occupancy_COM.csv',
		'ActuationEnergy' : False}
		
		
		ASFtest=ASF_Simulation(SimulationData = SimulationData, PanelData = PanelData, BuildingData = BuildingData, BuildingProperties = BuildingProperties, SimulationOptions = SimulationOptions)
		ASFtest.SolveASF()
		
		self.assertEqual(round(ASFtest.yearlyData['E_total']['E'],2), 1182.16)
		self.assertEqual(round(ASFtest.yearlyData['E_total']['PV'],2), -709.2)
		#self.assertEqual(round(monthlyData['H'][0],2),3.56)
		self.assertEqual(ASFtest.ResultsBuildingSimulation['E_total']['BestCombKey'][38],39)
		
		
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
		'setBackTempC': 4,
		'Occupancy' : 'Occupancy_COM.csv',
		'ActuationEnergy' : False}
		
		
		ASFtest=ASF_Simulation(SimulationData = SimulationData, PanelData = PanelData, BuildingData = BuildingData, BuildingProperties = BuildingProperties, SimulationOptions = SimulationOptions)
		ASFtest.SolveASF()
		
																					 
		self.assertEqual(round(ASFtest.yearlyData['E_total_elec']['E_elec'],2), 1419.46)
		self.assertEqual(round(ASFtest.yearlyData['E_total_elec']['PV'],2), -723.99)
		self.assertEqual(ASFtest.ResultsBuildingSimulation['E_total_elec']['BestCombKey'][38],46)
  
	def test_COPHeating(self):
		#Set simulation data
		print 'running COP H test'
		SimulationData= {
		'optimizationTypes' : ['E_total'],
		'DataFolderName' : 'ZH13_49comb',
		'FileName': 'ZH13_49comb',
		'geoLocation' : 'Zuerich_Kloten_2013',
		'EPWfile' : 'Zuerich_Kloten_2013.epw',
		'Save' : False,
		'ShowFig': False}
		
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
           "COP_H": 4,
           "COP_C":1}		

		

		
		ASFtest2=ASF_Simulation(SimulationData = SimulationData,BuildingProperties = BuildingProperties)
		ASFtest2.SolveASF()
		
																					 
		self.assertEqual(round(ASFtest2.yearlyData['E_total']['E'],2), 1049.13)
		self.assertEqual(round(ASFtest2.yearlyData['E_total']['H'],2), 315.13)
		
  
	def test_COPCooling(self):
          
		#Set simulation data
		print 'running COP C test'
		SimulationData= {
		'optimizationTypes' : ['E_total'],
		'DataFolderName' : 'ZH13_49comb',
		'FileName': 'ZH13_49comb',
		'geoLocation' : 'Zuerich_Kloten_2013',
		'EPWfile' : 'Zuerich_Kloten_2013.epw',
		'Save' : False,
		'ShowFig': False}
		
				
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
           "COP_C":3}
		
		
		
		
		ASF_COP_C=ASF_Simulation(SimulationData = SimulationData,BuildingProperties = BuildingProperties)
		ASF_COP_C.SolveASF()
		
																					 
		self.assertEqual(round(ASF_COP_C.yearlyData['E_total']['E'],2), 681.32)
		self.assertEqual(round(ASF_COP_C.yearlyData['E_total']['C'],2), 376.69)
		
	def test_NoASF(self):
          
		#Set simulation data
		print 'test NoASF'
		SimulationData= {
		'optimizationTypes' : ['E_total'],
  		'DataFolderName' : 'ZH13_NoASF',
		'FileName': 'ZH13_NoASF',
		'geoLocation' : 'Zuerich_Kloten_2013',
		'EPWfile' : 'Zuerich_Kloten_2013.epw',
		'Save' : False,
		'ShowFig': False}
		
				
		PanelData={
            "XANGLES": [0],
            "YANGLES" : [0],
            "NoClusters":1,
            "numberHorizontal":0,
            "numberVertical":0,
            "panelOffset":400,
            "panelSize":400,
            "panelSpacing":500}
            
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
		

		NoASF=ASF_Simulation(SimulationData = SimulationData,PanelData = PanelData, BuildingProperties= BuildingProperties)
		NoASF.SolveASF()
		
																					 
		self.assertEqual(round(NoASF.yearlyData['E_total']['E'],2), 5147.59)
		self.assertEqual(round(NoASF.yearlyData['E_total']['PV'],2), 0.00)
		self.assertEqual(NoASF.ResultsBuildingSimulation['E_total']['BestCombKey'][38],1)
		self.assertEqual(NoASF.ResultsBuildingSimulation['E_total']['BestCombKey'][4000],1)
  
	def test_1comb(self):
          
		#Set simulation data
		print 'test 1 combination'
		SimulationData= {
		'optimizationTypes' : ['E_total'],
  		'DataFolderName' : 'ZH13_49comb',
		'FileName': 'ZH13_1comb_0_0',
		'geoLocation' : 'Zuerich_Kloten_2013',
		'EPWfile' : 'Zuerich_Kloten_2013.epw',
		'Save' : False,
		'ShowFig': False}
		
				
		PanelData={
            "XANGLES": [0],
            "YANGLES" : [0],
            "NoClusters":1,
            "numberHorizontal":6,
            "numberVertical":9,
            "panelOffset":400,
            "panelSize":400,
            "panelSpacing":500}
            
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
		
		
		
		
		OneASF=ASF_Simulation(SimulationData = SimulationData,PanelData = PanelData, BuildingProperties=BuildingProperties)
		OneASF.SolveASF()
		
																					 
		self.assertEqual(round(OneASF.yearlyData['E_total']['E'],2), 2601.4)
		self.assertEqual(round(OneASF.yearlyData['E_total']['PV'],2),-658.0)
		self.assertEqual(OneASF.ResultsBuildingSimulation['E_total']['BestCombKey'][38],0)
  
	def test_AcuationEnergy(self):
          
		print 'running AcuationEnergy test'
		SimulationData= {
		'optimizationTypes' : ['E_total'],
		'DataFolderName' : 'ZH13_49comb',
		'FileName': 'ZH13_49comb',
		'geoLocation' : 'Zuerich_Kloten_2013',
		'EPWfile' : 'Zuerich_Kloten_2013.epw',
		'Save' : False,
		'ShowFig': False}
		
				

		#Set simulation Properties
		SimulationOptions= {
		'setBackTempH' : 4.,
		'setBackTempC': 4,
		'Occupancy' : 'Occupancy_COM.csv',
		'ActuationEnergy' : True}
		
		
		
		
		AcuationEnergyASF=ASF_Simulation(SimulationData = SimulationData, SimulationOptions = SimulationOptions)
		AcuationEnergyASF.SolveASF()
		
																					 
		self.assertEqual(round(AcuationEnergyASF.yearlyData['E_total']['E'],2),492)
		self.assertEqual(round(AcuationEnergyASF.yearlyData['E_total']['AE'],2),2.74)
		self.assertEqual(AcuationEnergyASF.ResultsBuildingSimulation['E_total']['BestCombKey'][38],0)
		
  
  

if __name__ == '__main__':
	unittest.main()