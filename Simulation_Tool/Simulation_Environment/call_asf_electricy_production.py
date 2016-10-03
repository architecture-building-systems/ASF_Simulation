# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 09:01:20 2016

@author: Assistenz
"""





#def asf_electricity_production(
#    createPlots=False, 
#    lb_radiation_path=None, 
#    panelsize = 400, 
#    pvSizeOption=0, 
#    save_results_path = None,
#    lookup_table_path = None, 
#    geo_path = None, 
#    flipOrientation = False, 
#    simulationOption = None):


#Set Solar Panel Properties




from asf_electricity_production_mauro_2 import asf_electricity_production

simulationOption = {'timePeriod' : None}
XANGLES=[45,67.5]
YANGLES= [0,45]
HOY = 4000

PV_electricity_results, PV_detailed_results, fig1, fig2 = asf_electricity_production(True, 
                           'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\\radiation_results',
                           400, 0,
                           save_results_path = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment', 
                           lookup_table_path ='C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\Simulation_Environment\data\python\electrical_simulation', 
                           geo_path = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\Simulation_Environment\data\geographical_location\Zuerich-Kloten',
                           flipOrientation= False, simulationOption = {'timePeriod' : None})
                           

                           
                           