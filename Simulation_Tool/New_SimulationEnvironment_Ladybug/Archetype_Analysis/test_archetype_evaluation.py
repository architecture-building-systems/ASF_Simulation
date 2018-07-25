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

        BuildingData = {
            "room_width": 3000, 
            "room_height":3600, 
            "room_depth":4000, 
            "glazing_percentage_w": 0.92,
            "glazing_percentage_h": 0.97, 
            "WindowGridSize": 200, 
            "BuildingOrientation" : 0}

        #ASF

        # SimulationData = {
        #     'optimizationTypes' : ['E_total'], #, 'Cooling', 'Heating', 'SolarEnergy', 'Lighting', 'E_HCL'
        #     'DataFolderName' : 'HS_49comb_HiLo', #'ZH13_49comb_HiLo', #'ZH13_49comb',Cairo_49comb_HiLo
        #     'FileName': 'HS_49comb_HiLo', #'ZH_49comb_HiLo',
        #     'geoLocation' : 'FIN_Helsinki.029740_IWEC',#'Zuerich_Kloten_2013',EGY_Cairo.623660_IWEC, FIN_Helsinki.029740_IWEC
        #     'EPWfile': 'FIN_Helsinki.029740_IWEC.epw',#'Zuerich_Kloten_2013.epw',EGY_Cairo.623660_IWEC.epw, FIN_Helsinki.029740_IWEC.epw
        #     'Save' : False,
        #     'ShowFig': False,
        #     'timePeriod': None,
        #     'total_pv_combinations': 49}


        # PanelData = {
        #     "XANGLES": [0, 15, 30, 45, 60, 75, 90],
        #     "YANGLES" : [-45, -30,-15,0, 15, 30, 45],
        #     "NoClusters":1,
        #     "numberHorizontal":5,
        #     "numberVertical":6,
        #     "panelOffset":400,
        #     "panelSize":425,
        #     "panelSpacing":510, 
        #     "panelGridSize" : 25}

        ##----Static Facade---##

        # SimulationData = {
        #     'optimizationTypes' : ['E_total'], #, 'Cooling', 'Heating', 'SolarEnergy', 'Lighting', 'E_HCL'
        #     'DataFolderName' : 'HS_49comb_HiLo_static', #'ZH13_49comb_HiLo', #'ZH13_49comb',Cairo_49comb_HiLo
        #     'FileName': 'HS_49comb_HiLo_static', #'ZH_49comb_HiLo',
        #     'geoLocation' : 'FIN_Helsinki.029740_IWEC',#'Zuerich_Kloten_2013',EGY_Cairo.623660_IWEC, FIN_Helsinki.029740_IWEC
        #     'EPWfile': 'FIN_Helsinki.029740_IWEC.epw',#'Zuerich_Kloten_2013.epw',EGY_Cairo.623660_IWEC.epw, FIN_Helsinki.029740_IWEC.epw
        #     'Save' : False,
        #     'ShowFig': False,
        #     'timePeriod': None,
        #     'total_pv_combinations': 1}

        # PanelData = {
        #     "XANGLES": [45],
        #     "YANGLES" : [0],
        #     "NoClusters":1,
        #     "numberHorizontal":5,
        #     "numberVertical":6,
        #     "panelOffset":400,
        #     "panelSize":425,
        #     "panelSpacing":510, 
        #     "panelGridSize" : 25}
                    


        ###----No ASF Simulatin -----

        SimulationData = {
            'optimizationTypes' : ['E_total'], #, 'Cooling', 'Heating', 'SolarEnergy', 'Lighting', 'E_HCL'
            'DataFolderName' : 'HS_49comb_HiLo_noASF', #'ZH13_49comb_HiLo', #'ZH13_49comb',Cairo_49comb_HiLo
            'FileName': 'HS_49comb_HiLo_noASF', #'ZH13_49comb_HiLo', #'ZH13_49comb',Cairo_49comb_HiLo
            'geoLocation' : 'FIN_Helsinki.029740_IWEC',#'Zuerich_Kloten_2013',EGY_Cairo.623660_IWEC, FIN_Helsinki.029740_IWEC
            'EPWfile': 'FIN_Helsinki.029740_IWEC.epw',#'Zuerich_Kloten_2013.epw',EGY_Cairo.623660_IWEC.epw, FIN_Helsinki.029740_IWEC.epw
            'Save' : False,
            'ShowFig': False,
            'timePeriod': None,
            'total_pv_combinations': 1}

        PanelData = {
            "XANGLES": [0],
            "YANGLES" : [0],
            "NoClusters":1,
            "numberHorizontal":0,
            "numberVertical":0,
            "panelOffset":400,
            "panelSize":425,
            "panelSpacing":510, 
            "panelGridSize" : 25}
                    


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
            print ASF_archetype.yearlyData
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


if __name__ == '__main__':
    unittest.main()