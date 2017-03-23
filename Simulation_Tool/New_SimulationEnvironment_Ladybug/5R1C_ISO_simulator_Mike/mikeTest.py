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
    coolingEmissionSystem=AirConditioning,
    phi_c_max_A_f=-100.0,
    phi_h_max_A_f=100.0)

A_floor = Office.Room_Width*Office.Room_Depth
A_person = 21.0                #Area per office worker
maxPeople = A_floor/A_person   #Max occupancy in number of people
maxIntGain = 23.3*A_floor      #Max internal gains from appliances and lighting
maxPeopGain = 100*maxPeople    #Max internal gains from metabolic heat from workers (100 W/cap assumed)


#%%

ElectricityOut = []
HeatingDemand = []      #Energy required by the zone
HeatingInput = []       #Energy required by the supply system to provide HeatingDemand
CoolingDemand = []      #Energy surplus of the zone
CoolingInput = []       #Energy required by the supply system to get rid of CoolingDemand
IndoorAir = []
outTemp = []


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
    HeatingDemand.append(Office.heatingDemand)
    HeatingInput.append(Office.heatingEnergy)
    CoolingDemand.append(Office.coolingDemand)
    CoolingInput.append(Office.coolingEnergy)
    ElectricityOut.append(Office.electricityOut)
    IndoorAir.append(Office.theta_air)
    outTemp.append(theta_e)
    
    
    
#%%

#t = range(4300,4400)


mp.figure(figsize=(15,5))
mp.plot(HeatingDemand, color = (0.8,0.2,0.1))
mp.plot(CoolingDemand, color = (0.1, 0.4, 0.8))
mp.xlabel('Time (h)')
mp.ylabel('Power (W)')
mp.title('Zone Power Demand Over One Year (2013)')
mp.grid(False)
mp.savefig("Heating.png", dpi=300)
mp.show()


#Energy sum of various systems


#deg = u'\u2103'
#
#mp.figure(figsize=(15,5))
#mp.plot(outTemp, color = '0.4')
#mp.xlabel('Time (h)')
#mp.ylabel('Outdoor Temperature ('+deg+')')
#mp.title('Outdoor Temperature Over One Year (2013)')
#mp.grid(False)
#mp.savefig("Temperature.png", dpi=300)
#mp.show()



#mp.figure(figsize=(15,6))
#mp.plot(CoolingDemand, color = (0.1, 0.4, 0.8))
#mp.xlabel('Time (h)')
#mp.ylabel('Cooling Power (W)')
#mp.title('Cooling Power Over One Year (2013)')
#mp.grid(False)
#mp.savefig("Cooling.png", dpi=300)
#mp.show()
#


















