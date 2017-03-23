"""
=========================================
Main file to calculate the building loads
EN-13970
=========================================
"""

import numpy as np
from buildingPhysics import Building #Importing Building Class

__author__ = "Prageeth Jayathissa"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Gabriel Happle"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Prageeth Jayathissa"
__email__ = "jayathissa@arch.ethz.ch"
__status__ = "Production"




#Example Inpiuts
theta_e=10
theta_m_prev=22
phi_int=10 #Internal heat gains, in Watts
phi_sol=2000 #Solar heat gains after transmitting through the winow [Watts]
ill=44000 #Illuminance after transmitting through the window [Lumens]
occupancy = 0.1 #Occupancy for the timestep [people/hour/square_meter]


#Initialise an instance of the building. Empty brackets take on the default parameters. See buildingPhysics.py to see the default values
Office=Building()

#Solve for building energy
Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)

#Solve for building lighting
Office.solve_building_lighting(ill, occupancy)


print Office.theta_m #Printing Room Temperature of the medium
print Office.lighting_demand #Print Lighting Demand
print Office.phi_hc_nd_ac #Print heating/cooling loads

#Example of how to change the set point temperature after running a simulation
Office.theta_int_h_set = 20.0

#Solve again for the new set point temperature
Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)

print Office.theta_m #Print the new internal temperature

print Office.has_heating_demand #Print a boolean of whether there is a heating demand
