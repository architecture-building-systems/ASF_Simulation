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
#from matplotlib import rcParams
#rcParams.update({'figure.autolayout': False})

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

#%%


fossilsSum = []
electricitySum = []
electricityCoolSum = []
eOut = []

supSystems = [OilBoilerOld, OilBoilerMed, OilBoilerNew, HeatPumpAir, HeatPumpWater, HeatPumpGround, ElectricHeating, CHP]
emSystems = [OldRadiators, NewRadiators, ChilledBeams, AirConditioning, FloorHeating, TABS]
heatPumps = [HeatPumpAir, HeatPumpWater, HeatPumpGround]
    
sysMapHeat = []
sysMapCool = []

for supSys in heatPumps:

    heatingLine = []
    coolingLine = []
    
    for emSys in emSystems:
    
        #Initialise an instance of the building. Empty brackets take on the default parameters. See buildingPhysics.py to see the default values
        Office=Building(
            heatingSupplySystem=supSys,
            coolingSupplySystem=supSys,
            heatingEmissionSystem=emSys,
            coolingEmissionSystem=emSys,
            phi_c_max_A_f=-100.0,
            phi_h_max_A_f=100.0)
        
        A_floor = Office.Room_Width*Office.Room_Depth
        A_person = 21.0                #Area per office worker
        maxPeople = A_floor/A_person   #Max occupancy in number of people
        maxIntGain = 23.3*A_floor      #Max internal gains from appliances and lighting
        maxPeopGain = 100*maxPeople    #Max internal gains from metabolic heat from workers (100 W/cap assumed)        
        
        offOcc = pd.read_csv('schedules_el_OFFICE.csv')
        sunPos = pd.read_csv('SunPosition.csv', skiprows=1)
        weather = epw_reader('Zurich-Kloten_2013.epw')
        
        ElectricityOut = []
        HeatingDemand = []              #Energy required by the zone
        HeatingElectricity = []         #Electricity required by the supply system to provide HeatingDemand
        HeatingFossils = []             #Fossil Fuels required by the supply system to provide HeatingDemand
        CoolingDemand = []              #Energy surplus of the zone
        CoolingElectricity = []         #Electricity required by the supply system to get rid of CoolingDemand
        IndoorAir = []
        outTemp = []
        
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
            HeatingElectricity.append(Office.heatingSysElectricity)
            HeatingFossils.append(Office.heatingSysFossils)
            CoolingDemand.append(Office.coolingDemand)
            CoolingElectricity.append(Office.coolingSysElectricity)
#            ElectricityOut.append(Office.electricityOut)
#            IndoorAir.append(Office.theta_air)
#            outTemp.append(theta_e)
        
#        fossilsSum.append(np.sum(HeatingFossils))
#        electricitySum.append(np.sum(HeatingElectricity))
#        eOut.append(np.sum(ElectricityOut))
#        electricityCoolSum.append(np.sum(CoolingElectricity))
        
        heatingLine.append(np.sum(HeatingElectricity) + np.sum(HeatingFossils))
        coolingLine.append(np.sum(CoolingElectricity))
        
    sysMapHeat.append(heatingLine)
    sysMapCool.append(coolingLine)


#mp.figure(figsize=(7,7))    
#mp.imshow(sysMapHeat, cmap='plasma', interpolation='nearest')
#mp.show()


#%%

heatPumps = [HeatPumpAir, HeatPumpWater, HeatPumpGround]


n = len(heatPumps)
ind = range(n)

for hp in ind:

    eOutNegkWh = []
    fossilsSumkWh = []
    electricitySumkWh = []
    names =[]
    heatingkWh = []
    coolingkWh = []
    
    nem = len(emSystems)
    indem = range(nem)
    
    for i in indem:
    #    eOutNegkWh.append(-eOut[i]/1000)
    #    fossilsSumkWh.append(fossilsSum[i]/1000)
    #    electricitySumkWh.append(electricitySum[i]/1000)
        names.append(emSystems[i].name)
        heatingkWh.append(sysMapHeat[hp][i]/1000)
        coolingkWh.append(sysMapCool[hp][i]/1000)
    
    mp.figure(figsize=(4,7))
     
    p1 = mp.bar(indem, coolingkWh, color = (0.3, 0.8, 1), edgecolor = 'k', width = 0.6)
#    p2 = mp.bar(indem, coolingkWh, color = (1, 0.9, 0.1), edgecolor = 'k', width = 0.6)
#    p3 = mp.bar(indem, eOutNegkWh, color = (0.5,0.9,0), edgecolor = 'k', width = 0.6)
    
    mp.ylabel('kWh/a')
    mp.title(heatPumps[hp].name)
    mp.xticks(indem, names, rotation='vertical')
    mp.yticks(np.arange(0, 11, 5))
#    mp.legend((p1[0], p2[0]), ('Fossils Consumption', 'Electricity Consumption'))
    mp.ylim([-2,15])
    mp.margins(0.05)
    mp.axhline(0, color='k', linewidth=0.5)
    mp.tight_layout()
    
    mp.savefig(heatPumps[hp].name + '.png', dpi=300)
    
    mp.show()


#%%


#n = len(emSystems)
#ind = range(n)
#
#eOutNegkWh = []
#fossilsSumkWh = []
#electricitySumkWh = []
#electricityCoolSumkWh = []
#names =[]
#
#for i in ind:
#    eOutNegkWh.append(-eOut[i]/1000)
#    fossilsSumkWh.append(fossilsSum[i]/1000)
#    electricitySumkWh.append(electricitySum[i]/1000)
#    names.append(emSystems[i].name)
#    electricityCoolSumkWh.append(-electricityCoolSum[i]/1000)
#
#mp.figure(figsize=(5,7))
# 
#p1 = mp.bar(ind, electricitySumkWh, color = (1, 0.8, 0.3), edgecolor = 'k', width = 0.6)
#p2 = mp.bar(ind, electricityCoolSumkWh, color =(0.3, 0.8, 1), edgecolor = 'k', width = 0.6)
#
#mp.ylabel('kWh/a')
#mp.title('Impact of the Emission System on Energy Consumption')
#mp.xticks(ind, names, rotation='vertical')
#mp.yticks(np.arange(0, 4001, 1000))
#mp.legend((p1[0], p2[0]), ('Heating', 'Cooling'))
#mp.ylim([-500,5000])
#mp.margins(0.1)
#mp.axhline(0, color='k', linewidth=0.5)
#mp.tight_layout()
#
#mp.savefig('YearlyEmSys.png', dpi=300)
#
#mp.show()




#%%



#mp.figure(figsize=(7,5))
#mp.plot(HeatingDemand, color = (0.8,0.2,0.1))
#mp.plot(CoolingDemand, color = (0.1, 0.4, 0.8))
#mp.xlabel('Time (h)')
#mp.ylabel('Power (W)')
#mp.title('Heating Supply System Power Demand ' + supSys.name)
#mp.grid(False)
#mp.savefig(str(supSys)+'.png', dpi=300)
#mp.show()


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


