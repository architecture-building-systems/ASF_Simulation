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
from j_build_dictionaries import ArchT_build_df


class TestMainSimulation(unittest.TestCase):
	
		     
        

	def test_Standard(self):
		BuildingData={
		"room_width": 4900,     
		"room_height":3100,
		"room_depth":7000,
		"glazing_percentage_w": 0.92,
		"glazing_percentage_h": 0.97}

		b_dataOut = ArchT_build_df(BuildingData)
		

		self.assertEqual(b_dataOut.size,5148)
		self.assertEqual(b_dataOut.Qs_Wm2[1],1.00485)
		self.assertEqual(b_dataOut.U_wall[5],0.11)

if __name__ == '__main__':
	unittest.main()