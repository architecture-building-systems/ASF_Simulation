# -*- coding: utf-8 -*-
"""
Created on March 20 2017

@author: Prageeth Jayathissa
Status, temporary for refactoring
"""
import unittest
import os
import sys
import pandas as pd
import time


from j_paths import PATHS

paths = PATHS()
sys.path.insert(0, paths['5R1C_ISO_simulator'])
sys.path.insert(0, paths['main'])

from SimulationClass import ASF_Simulation
from build_dictionaries import BuildArchetypeDict

class TestMainSimulation(unittest.TestCase):
    def test_Standard(self):
        """
        Runs the ASF Simulation Analysis for multiple archetypes 

        TODO: Archetypes can only be chosen in the BuildArchetypeDict function. This should be moved here as an input parameter

        :Output: all_results: A dataframe of building energy requirements for each archetype evaluated
        """

        paths = PATHS()


        SimulationData = {
            'optimizationTypes' : ['E_total'], #, 'Cooling', 'Heating', 'SolarEnergy', 'Lighting', 'E_HCL'
            'DataFolderName' : 'ZH13_49comb', #'ZH13_49comb',
            'FileName': 'ZH13_49comb',
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
            "XANGLES": [0, 15, 30, 45, 60, 75, 90],
            "YANGLES" : [-45, -30,-15,0, 15, 30, 45],
            "NoClusters":1,
            "numberHorizontal":6,
            "numberVertical":9,
            "panelOffset":400,
            "panelSize":400,
            "panelSpacing":500, 
            "panelGridSize" : 25}

        ##----Static Facade---##

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

        # SimulationData = {
        #     'optimizationTypes' : ['E_total'], #, 'Cooling', 'Heating', 'SolarEnergy', 'Lighting', 'E_HCL'
        #     'DataFolderName' : 'ZH13_NoASF', #'ZH13_49comb_static_45_0',
        #     'FileName': 'ZH13_NoASF',
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
        #     "XANGLES": [0],
        #     "YANGLES" : [0],
        #     "NoClusters":1,
        #     "numberHorizontal":0,
        #     "numberVertical":0,
        #     "panelOffset":400,
        #     "panelSize":400,
        #     "panelSpacing":500, 
        #     "panelGridSize" : 25}

        BP_dict, SO_dict = BuildArchetypeDict(BuildingData)

        all_results=pd.DataFrame({'Name': []})
        all_results.set_index(['Name'], inplace=True)

        # loop through building properties and simulation options dictionaries:
        for ii,key in enumerate(BP_dict.keys()): #range(0, len(runlist)):
            print 'simulation %i/%i:' % (ii+1, len(BP_dict)) 

            # Run ASF simulation
            ASF_archetype = ASF_Simulation(SimulationData=SimulationData, BuildingData=BuildingData,
                                 BuildingProperties=BP_dict[key], SimulationOptions=SO_dict[key], PanelData=PanelData)
            ASF_archetype.SolveASF()

            # Add building name to dataframe and append subsequent iterations:
            current_result = ASF_archetype.yearlyData.T
            current_result['Name'] = key
            current_result.set_index(['Name'], inplace=True)
            temp_list = [all_results, current_result] #TODO: Change this to one line
            all_results = pd.concat(temp_list) 

        print '--simulations complete--'

        # write results to csv:
        timestr = time.strftime("%d%m%Y_%H%M")
        name = 'Archetypes_' + SimulationData.get('DataFolderName') + '_' + timestr + '.csv'
        all_results.to_csv(os.path.join(paths['CEA_folder'], name))

        print all_results

        self.assertEqual(round(all_results.loc["MULTI_RES2","E"],2),4063.44)
        self.assertEqual(round(all_results.loc["MULTI_RES1","E"],2),3899.25)

if __name__ == '__main__':
    unittest.main()