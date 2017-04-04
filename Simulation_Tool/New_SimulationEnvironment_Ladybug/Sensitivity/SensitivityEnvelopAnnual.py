"""
Created on March 20 2017

@author: Prageeth Jayathissa
"""
import unittest
import os
import sys
import pandas as pd
import time
import numpy as np


from j_paths import PATHS

paths = PATHS()
sys.path.insert(0, paths['5R1C_ISO_simulator'])
sys.path.insert(0, paths['main'])

from SimulationClass import ASF_Simulation
from supplySystem import *
from emissionSystem import *


class TestMainSimulation(unittest.TestCase):
    def test_Standard(self):
        """
        Runs the ASF Simulation Analysis for multiple archetypes 

        TODO: Archetypes can only be chosen in the BuildArchetypeDict function. This should be moved here as an input parameter

        :Output: all_results: A dataframe of building energy requirements for each archetype evaluated
        """

        paths = PATHS()


        # SimulationData = {
        #     'optimizationTypes' : ['E_total'], #, 'Cooling', 'Heating', 'SolarEnergy', 'Lighting', 'E_HCL'
        #     'DataFolderName' : 'ZH13_49comb', #'ZH13_49comb',
        #     'FileName': 'ZH13_49comb',
        #     'geoLocation' : 'Zuerich_Kloten_2013',
        #     'EPWfile': 'Zuerich_Kloten_2013.epw',
        #     'Save' : False,
        #     'ShowFig': False}

        # # Set Building Parameters in [mm]
        # BuildingData = {
        #     "room_width": 4900,
        #     "room_height": 3100,
        #     "room_depth": 7000,
        #     "glazing_percentage_w": 1.0, #0.92
        #     "glazing_percentage_h": 1.0} #0.97

        # PanelData = {
        #     "XANGLES": [0, 15, 30, 45, 60, 75, 90],
        #     "YANGLES" : [-45, -30,-15,0, 15, 30, 45],
        #     "NoClusters":1,
        #     "numberHorizontal":6,
        #     "numberVertical":9,
        #     "panelOffset":400,
        #     "panelSize":400,
        #     "panelSpacing":500, 
        #     "panelGridSize" : 25}

        ##-----Static Simulatioh----
        # SimulationData = {
        #     'optimizationTypes' : ['E_total'], #, 'Cooling', 'Heating', 'SolarEnergy', 'Lighting', 'E_HCL'
        #     'DataFolderName' : 'ZH13_49comb_static_45_0', #'ZH13_49comb_static_45_0',
        #     'FileName': 'ZH13_49comb_static_45_0',
        #     'geoLocation' : 'Zuerich_Kloten_2013',
        #     'EPWfile': 'Zuerich_Kloten_2013.epw',
        #     'Save' : False,
        #     'ShowFig': False}

        # # Set Building Parameters in [mm]
        # BuildingData = {
        #     "room_width": 4900,
        #     "room_height": 3100,
        #     "room_depth": 7000,
        #     "glazing_percentage_w": 0.92,
        #     "glazing_percentage_h": 0.97}

        # PanelData = {
        #     "XANGLES": [45],
        #     "YANGLES" : [0],
        #     "NoClusters":1,
        #     "numberHorizontal":6,
        #     "numberVertical":9,
        #     "panelOffset":400,
        #     "panelSize":400,
        #     "panelSpacing":500, 
        #     "panelGridSize" : 25}

        ###----No ASF Simulatin -----

        SimulationData = {
            'optimizationTypes' : ['E_total'], #, 'Cooling', 'Heating', 'SolarEnergy', 'Lighting', 'E_HCL'
            'DataFolderName' : 'ZH13_NoASF', #'ZH13_49comb_static_45_0',
            'FileName': 'ZH13_NoASF',
            'geoLocation' : 'Zuerich_Kloten_2013',
            'EPWfile': 'Zuerich_Kloten_2013.epw',
            'Save' : False,
            'ShowFig': False}

        # Set Building Parameters in [mm]
        BuildingData = {
            "room_width": 4900,
            "room_height": 3100,
            "room_depth": 7000,
            "glazing_percentage_w": 0.92,
            "glazing_percentage_h": 0.97}

        PanelData = {
            "XANGLES": [0],
            "YANGLES" : [0],
            "NoClusters":1,
            "numberHorizontal":0,
            "numberVertical":0,
            "panelOffset":400,
            "panelSize":400,
            "panelSpacing":500, 
            "panelGridSize" : 25}

        #Set building properties for RC-Model simulator

        
        #Set simulation Properties
        SimulationOptions= {
            'setBackTempH' : 4.,
            'setBackTempC' : 4., 
            'Occupancy' : 'Occupancy_COM.csv',
            'ActuationEnergy' : False, 
            "Temp_start" : 20, 
            'human_heat_emission' : 0.12,}

        #U_Range=np.arange(0.2,4.1,0.2)
        U_Range=np.arange(0.2,2.1,0.2)


        all_results=pd.DataFrame({'Infiltration': []})
        all_results.set_index(['Infiltration'], inplace=True)

        # loop through building properties and simulation options dictionaries:
        for ii,sens in enumerate(U_Range): #range(0, len(runlist)):


            BuildingProperties={
                "glass_solar_transmittance" : 0.687 ,
                "glass_light_transmittance" : 0.744 ,
                "lighting_load" : 11.74 ,
                "lighting_control" : 300,
                "Lighting_Utilisation_Factor" :  0.45,
                "Lighting_Maintenance_Factor" : 0.9,
                "U_em" : 0.2, 
                "U_w" : 1.2,
                "ACH_vent" : 1.5,
                "ACH_infl" :sens,
                "ventilation_efficiency" : 0.6 ,
                "c_m_A_f" : 165 * 10**3,
                "theta_int_h_set" : 20,
                "theta_int_c_set" : 26,
                "phi_c_max_A_f": -np.inf,
                "phi_h_max_A_f": np.inf,
                "heatingSupplySystem" : DirectHeater,
                "coolingSupplySystem" : COP3Cooler,
                "heatingEmissionSystem" : AirConditioning,
                "coolingEmissionSystem" : AirConditioning,
                }
            # Run ASF simulation
            ASF_archetype = ASF_Simulation(SimulationData=SimulationData, BuildingData=BuildingData,
                                 BuildingProperties=BuildingProperties, SimulationOptions=SimulationOptions, PanelData=PanelData)
            ASF_archetype.SolveASF()

            # Add building U_envelope to dataframe and append subsequent iterations:
            current_result = ASF_archetype.yearlyData.T
            current_result['Infiltration'] = sens
            current_result.set_index(['Infiltration'], inplace=True)
            temp_list = [all_results, current_result] #TODO: Change this to one line
            all_results = pd.concat(temp_list) 

        print '--simulations complete--'

        # write results to csv:
        timestr = time.strftime("%d%m%Y_%H%M")
        name = 'Sensitivity_' + SimulationData.get('DataFolderName') + '_' + timestr + '.csv'
        all_results.to_csv(name)

        print all_results

if __name__ == '__main__':
    unittest.main()