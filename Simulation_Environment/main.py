# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:14:42 2016

main file for simulation environment

@author: Jeremias
"""

import os, sys


######### -----USER INTERACTION------ #############

# set mode of this main script ('initialize', 'post-processing')
mainMode = 'initialize'

# specify the location used for the analysis - this name must be the same as a
# folder in the directory .../ASF_Simulation/Simulation_Environment/data/geographical_location
# new locations can be added with the grasshopper main script for any .epw weather data
geoLocation = 'Zuerich-Kloten' # 'Zuerich-Kloten', 'MADRID_ESP'

# set folder name of DIVA simulation data (in data\grasshopper\DIVA):
diva_folder = 'Simulation_Kloten_25comb'

# set the number of combinations used for the analysis
numCombDIVA = 25


# set folder name of LadyBug simulation data (in data\grasshopper\LadyBug). 
# This folder has the same name as the generated folder for the electrical 
# results in data\python\electrical:
radiation_folder = 'Radiation_electrical_monthly_25comb'

# set the number of combinations and hours used for the LadyBug analysis:
numCombLB = 25
numHoursLB = 2

# set option to change the size of the PV area for the electrical simulation, 
# this is done in steps of 2 times the radiation gridsize, so 0 corresponds a 
# PV-size of 400mm, 1 corresponds to PV-size of 350mm, 2 corresponds to 300mm 
# etc.:
pvSizeOption = 0


# specify if  plots should be created:
createPLots = True



######### -----END OF USER INTERACTION------ #############







# find path of current folder (simulation_environment)
main_path = os.path.abspath(os.path.dirname(sys.argv[0]))

# define paths of subfolders:
data_path = main_path + '\data'
python_path = main_path + '\python'
gh_path = main_path + '\grasshopper'

# add python path to system path, so that all files are available:
sys.path.insert(0, python_path)

# define paths of data_folders:
diva_path = os.path.join(( data_path + "\grasshopper\DIVA"), diva_folder)
lb_path = os.path.join(( data_path + "\grasshopper\LadyBug"), radiation_folder)
electrical_path = os.path.join(( data_path + "\python\electrical"), radiation_folder)

if mainMode == 'initialize':
    # define path of geographical location:
    geo_path = os.path.join(( data_path + "\geographical_location"), geoLocation)
    # create sun data based on grasshopper file
    execfile(python_path + "\SunAngles_Tracking_and_temperature.py")


#execfile(python_path + "\PostProcessRadiation.py")