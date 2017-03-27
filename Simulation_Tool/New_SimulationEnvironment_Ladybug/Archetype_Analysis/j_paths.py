import os, sys

def PATHS():
	paths = {}
	paths['main'] = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
	paths['Simulation_Tool'] =  os.path.dirname(os.path.dirname(paths['main']))
	paths['WeatherData'] = os.path.join(paths['Simulation_Tool'], 'CEA_Archetypes_CH')  
	paths['Weatherfile'] = os.path.join(paths['WeatherData'], 'Zuerich_Kloten_2013') 
	paths['CEA_folder'] = os.path.join(paths['main'], 'CEA_Archetypes_CH') 
	paths['Archetypes'] = os.path.join(paths['CEA_folder'], 'Archetypes') 
	paths['Archetypes_properties'] = os.path.join(paths['Archetypes'],'Archetypes_properties.xlsx')
	paths['Archetypes_schedules'] = os.path.join(paths['Archetypes'],'Archetypes_schedules.xlsx')
	paths['5R1C_ISO_simulator'] = os.path.join(paths['main'], '5R1C_ISO_simulator') 	
	paths['data'] = os.path.join(paths['5R1C_ISO_simulator'], 'data') 
	return paths