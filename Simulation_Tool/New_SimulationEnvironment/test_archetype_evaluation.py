# -*- coding: utf-8 -*-
"""
Created on Wed Nov 09 11:53:33 2016

@author: Prageeth Technology
Status, temporary for refactoring
"""
import unittest
import sys
import os
import numpy as np
import j_build_dictionaries
import pandas as pd
import time

from j_paths import PATHS
from buildingSystem import *
from SimulationClass import ASF_Simulation as ASF
from j_build_dictionaries import ArchT_build_df, sort_dicts


class TestMainSimulation(unittest.TestCase):
    def test_Standard(self):


        paths = PATHS()

        # Constants
        # ---------
        ###Zurich South##########################################
        SimulationData_ZW = {
            'optimizationTypes': ['E_total'],
            'DataName': 'ZH13_49comb',
            'geoLocation': 'Zuerich_Kloten_2013',
            'EPWfile': 'Zuerich_Kloten_2013.epw',
            'Save': False,
            'ShowFig': False}

        PanelData = {
            "XANGLES": [0, 15, 30, 45, 60, 75, 90],
            "YANGLES": [-45, -30, -15, 0, 15, 30, 45],
            "NoClusters": 1,
            "numberHorizontal": 6,
            "numberVertical": 9,
            "panelOffset": 400,
            "panelSize": 400,
            "panelSpacing": 500}

        # Set Building Parameters in [mm]
        BuildingData = {
            "room_width": 4900,
            "room_height": 3100,
            "room_depth": 7000,
            "glazing_percentage_w": 0.92,
            "glazing_percentage_h": 0.97}

        BP_dict, SO_dict = ArchT_build_df(BuildingData)

        all_results=pd.DataFrame({'Name': []})
        all_results.set_index(['Name'], inplace=True)

        # loop through building properties and simulation options dictionaries:
        for ii,key in enumerate(BP_dict.keys()): #range(0, len(runlist)):
            print 'simulation %i/%i:' % (ii+1, len(BP_dict)) 

            # Run ASF simulation
            ASF_archetype = ASF(SimulationData=SimulationData_ZW, PanelData=PanelData, BuildingData=BuildingData,
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
        name = 'Archetypes_' + SimulationData_ZW.get('DataName') + '_' + timestr + '.csv'
        all_results.to_csv(os.path.join(paths['CEA_folder'], name))


        print all_results

        self.assertEqual(all_results.loc["MULTI_RES2","E"],4063.4510553479877)
        self.assertEqual(all_results.loc["MULTI_RES1","E"],3899.2592356541536)


if __name__ == '__main__':
    unittest.main()