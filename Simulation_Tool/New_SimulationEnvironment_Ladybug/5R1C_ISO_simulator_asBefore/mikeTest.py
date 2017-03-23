"""
=========================================
Main file to calculate the building loads
EN-13970
=========================================
"""

import pandas as pd
import numpy as np
from buildingPhysics import Building #Importing Building Class
from epwreader import epw_reader #Weather file reader
from sunPositionReader import SunPosition_reader
import matplotlib.pyplot as mp

from supplySystem import *
from emissionSystem import *

__author__ = "Prageeth Jayathissa"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Gabriel Happle"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Prageeth Jayathissa"
__email__ = "jayathissa@arch.ethz.ch"
__status__ = "Production"




#Example Inputs
#theta_e=10
#theta_m_prev=22
#phi_int=10 #Internal heat gains, in Watts
#phi_sol=2000 #Solar heat gains after transmitting through the winow [Watts]
#ill=44000 #Illuminance before transmitting through the window [Lumens]
#occupancy = 0.1 #Occupancy for the timestep [people/square_meter]


#Initialise an instance of the building. Empty brackets take on the default parameters. See buildingPhysics.py to see the default values
Office=Building(
    heatingSupplySystem=OilBoilerMed,
    coolingSupplySystem=HeatPumpAir,
    heatingEmissionSystem=NewRadiators,
    coolingEmissionSystem=AirConditioning,)

A_floor = Office.Room_Width*Office.Room_Depth
A_person = 21.0                #Area per office worker
maxPeople = A_floor/A_person   #Max occupancy in number of people
maxIntGain = 23.3*A_floor      #Max internal gains from appliances and lighting
maxPeopGain = 100*maxPeople    #Max internal gains from metabolic heat from workers (100 W/cap assumed)

HeatingDemand = []
CoolingDemand = []
ElectricityOut = []
IndoorAir = []

offOcc = pd.read_csv('schedules_el_OFFICE.csv')
sunPos = pd.read_csv('SunPosition.csv', skiprows=1)
weather = epw_reader('Zurich-Kloten_2013.epw')

theta_m_prev = 20


for hour in range(8760):
    phi_int = offOcc.loc[hour,'People']*(maxIntGain+maxPeopGain)
    occupancy = offOcc.loc[hour,'People']/A_person
    theta_e = weather['drybulb_C'][hour]
    try:
        strH = str(hour)
        altitude = sunPos.loc[0, strH]   #Elevation angle from horizontal in degrees
        azimuth = sunPos.loc[1, strH]    #Azimuth angle east of north in degrees
        if altitude<90.0 and azimuth>90 and azimuth<270:    #Sun hits the window front (south)
            phi_sol = weather['dirnorrad_Whm2'][hour]*np.cos(altitude*np.pi/180.0)*np.sin((azimuth-90)*np.pi/180.0) + 0.5*weather['difhorrad_Whm2'][hour]
            ill = weather['dirnorillum_lux'][hour]*np.cos(altitude*np.pi/180.0)*np.sin((azimuth-90)*np.pi/180.0) + 0.5*weather['difhorillum_lux'][hour]
        else:
            phi_sol = 0.5*weather['difhorrad_Whm2'][hour]
            ill = 0.5*weather['difhorillum_lux'][hour]
    except KeyError:
            phi_sol = 0.5*weather['difhorrad_Whm2'][hour]
            ill = 0.5*weather['difhorillum_lux'][hour]
    Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)
    theta_m_prev = Office.theta_m_t
    HeatingDemand.append(Office.heatingEnergy)
    CoolingDemand.append(Office.coolingEnergy)
    ElectricityOut.append(Office.electricityOut)
    IndoorAir.append(Office.theta_air)
        
        
#print HeatingDemand

t = range(4300,4600)

mp.plot(t, HeatingDemand[4300:4600])

#epw_reader('Zurich-Kloten_2013.epw')['hour'][34]
#
##offOcc = pd.read_csv('schedules_el_OFFICE.csv')
#
##offOcc.loc[8759,'People']  #share of max amount of people present at t = 8759+1
#
#           
##21 #m2 per person
#
#sunPos = pd.read_csv('SunPosition.csv', skiprows=1)
##
##print test.iat[1,1]
#
#print test
#
#test.loc[0,'9.0']  #Altitude at t=9
#test.loc[1,'9.0']  #Azimuth at t=9
#
#str(i)
#
#try:
#    x = int(raw_input("Please enter a number: "))
#    break
#except ValueError:
#    print "Oops!  That was no valid number.  Try again..."
#
#KeyError
#
#
#HOY on line 2, Altitude (degrees from horizontal) on line 3, Azimuth (degrees east of north) on line 4
#




#Test for epw reader
#print epw_reader('Zurich-Kloten_2013.epw')['hour'][34]


#Solve for building energy
#Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)

#Solve for building lighting
#Office.solve_building_lighting(ill, occupancy)


#print Office.theta_m #Printing Room Temperature of the medium
#print Office.lighting_demand #Print Lighting Demand
#print Office.phi_hc_nd_ac #Print heating/cooling loads
#
##Example of how to change the set point temperature after running a simulation
#Office.theta_int_h_set = 20.0
#
##Solve again for the new set point temperature
#Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)
#
#print Office.theta_m #Print the new internal temperature
#
#print Office.has_heating_demand #Print a boolean of whether there is a heating demand
