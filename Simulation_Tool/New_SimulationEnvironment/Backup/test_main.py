# -*- coding: utf-8 -*-
"""
Created on Wed Nov 02 09:22:20 2016

@author: Assistenz
"""

import sys

sys.path.insert(0, r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment')

from main_new_mauro import main


hourlyData, monthlyData, yearlyData = main()

if round(yearlyData['Zuerich_Kloten_2005']['C'],0) == 836.0 and round(monthlyData['E'][7] == 51.2,1):
    print 'Test passed'
else:
    print 'Test failed'