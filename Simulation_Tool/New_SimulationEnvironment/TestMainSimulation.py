# -*- coding: utf-8 -*-
"""
Created on Wed Nov 09 11:53:33 2016

@author: Mauro
"""
import unittest
import sys,os

sys.path.insert(0, os.path.abspath(os.path.dirname(sys.argv[0])))        
from mainSimulation import MainCalculateASF


class TestMainSimulation(unittest.TestCase):
    
    

    def test_Standard(self):
        
#        sys.path.insert(0, os.path.abspath(os.path.dirname(sys.argv[0])))        
#        from main import __main__
        
        geoLocation = 'Zuerich_Kloten_2005'
        optimization_Types = ['E_total']
        DataName = 'ZH05_49comb'
    
        ResultsBuildingSimulation, monthlyData, yearlyData = MainCalculateASF(geoLocation = geoLocation, 
                                                                               optimization_Types = optimization_Types, 
                                                                               DataName = DataName)
              
        self.assertEqual(round(yearlyData['E_total']['E'],2), 1185.72)
        self.assertEqual(round(yearlyData['E_total']['PV'],2), 708.40)
        #self.assertEqual(round(monthlyData['H'][0],2),3.56)
        self.assertEqual(ResultsBuildingSimulation['BestCombKey'][38],[5])



if __name__ == '__main__':
	unittest.main()