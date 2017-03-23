# -*- coding: utf-8 -*-
"""
Created on Wed Nov 09 11:53:33 2016

@author: Prageeth Technology
Status, temporary for refactoring
"""
import unittest
import os
import pandas as pd
import time

from j_paths import PATHS
from SimulationClass import ASF_Simulation
from j_build_dictionaries import BuildArchetypeDict

class TestMainSimulation(unittest.TestCase):
    def test_Standard(self):

        paths = PATHS()

        SimulationData = {
            'optimizationTypes': ['E_total'],
            'DataName': 'ZH13_49comb',
            'geoLocation': 'Zuerich_Kloten_2013',
            'EPWfile': 'Zuerich_Kloten_2013.epw',
            'Save': False,
            'ShowFig': False}

        # Set Building Parameters in [mm]
        BuildingData = {
            "room_width": 4900,
            "room_height": 3100,
            "room_depth": 7000,
            "glazing_percentage_w": 0.92,
            "glazing_percentage_h": 0.97}

        BP_dict, SO_dict = BuildArchetypeDict(BuildingData)

        all_results=pd.DataFrame({'Name': []})
        all_results.set_index(['Name'], inplace=True)

        # loop through building properties and simulation options dictionaries:
        for ii,key in enumerate(BP_dict.keys()): #range(0, len(runlist)):
            print 'simulation %i/%i:' % (ii+1, len(BP_dict)) 

            # Run ASF simulation
            ASF_archetype = ASF_Simulation(SimulationData=SimulationData, BuildingData=BuildingData,
                                 BuildingProperties=BP_dict[key], SimulationOptions=SO_dict[key])
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
        name = 'Archetypes_' + SimulationData.get('DataName') + '_' + timestr + '.csv'
        all_results.to_csv(os.path.join(paths['CEA_folder'], name))

        print all_results

        self.assertEqual(all_results.loc["MULTI_RES2","E"],4063.4510553479877)
        self.assertEqual(all_results.loc["MULTI_RES1","E"],3899.2592356541536)

if __name__ == '__main__':
    unittest.main()