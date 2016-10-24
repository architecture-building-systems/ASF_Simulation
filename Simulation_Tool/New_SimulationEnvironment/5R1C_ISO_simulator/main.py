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





theta_e=10
theta_m_prev=22

#Internal heat gains, in Watts
phi_int=10

#Solar heat gains after transmitting through the winow, in Watts
phi_sol=2000

#Illuminance after transmitting through the window 
ill=14000 #Lumens

#Occupancy for the timestep [people/hour/square_meter]
occupancy = 0.1

#Set Building Parameters
Office=Building()

Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)
Office.solve_building_lighting(ill, occupancy)


print Office.theta_m

print Office.lighting_demand


# print 'phi_ia=', Office.phi_ia
# print 'phi_m=', Office.phi_m
# print 'phi_st=',Office.phi_st

print Office.phi_hc_nd_ac

#print Office.has_heating_demand

# print Office.phi_m_tot