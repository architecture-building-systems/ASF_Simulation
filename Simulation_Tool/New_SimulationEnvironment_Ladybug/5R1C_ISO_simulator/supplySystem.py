"""
=========================================
Supply System Parameters for Heating and Cooling

=========================================
"""

import numpy as np
#from emissionSystem import *


__author__ = "Prageeth Jayathissa, Michael Fehr"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = [""]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Prageeth Jayathissa"
__email__ = "jayathissa@arch.ethz.ch"
__status__ = "Production"



"""
Model of different Supply systems. New Supply Systems can be introduced by adding new classes
"""

class SupplyDirector:
    
    """
    The director sets what Supply system is being used, and runs that set Supply system
    """

    __builder = None
    

    #Sets what building system is used
    def setBuilder(self, builder):
        self.__builder = builder

    # Calcs the energy load of that system. This is the main() fu
    def calcSystem(self):

        # Director asks the builder to produce the system body. self.__builder is an instance of the class
        
        body = self.__builder.calcLoads()

        return body 


class SupplyBuilder:

    """ The base class in which Supply systems are built from 
    """

    def __init__(self, Load, theta_e, theta_m, supplyTemperature):
        self.Load=Load #Energy Demand of the building at that time step
        self.theta_e=theta_e #Outdoor Air Temperature
        self.theta_m=theta_m #Room Temperature at that timestep
        self.supplyTemperature = supplyTemperature # Temperature required by the emission system
        


    def calcLoads(self): pass
#    def calcCoolingLoads(self): pass


class OilBoilerOld(SupplyBuilder):
    #Old oil boiler with fuel efficiency of 63 percent (medium of range in report of semester project M. Fehr)
    #No condensation, pilot light

    def calcLoads(self):
        heater = SupplyOut()
        heater.energyIn = self.Load/0.63
        heater.electricityOut = 0
        return heater


class OilBoilerMed(SupplyBuilder):
    #Classic oil boiler with fuel efficiency of 82 percent (medium of range in report of semester project M. Fehr)
    #No condensation, but better nozzles etc.
    
    def calcLoads(self):
        heater = SupplyOut()
        heater.energyIn = self.Load/0.82
        heater.electricityOut = 0
        return heater


class OilBoilerNew(SupplyBuilder):
    #New oil boiler with fuel efficiency of 98 percent (value from report of semester project M. Fehr)
    #Condensation boiler, latest generation

    def calcLoads(self):
        heater = SupplyOut()
        heater.energyIn = self.Load/0.98
        heater.electricityOut = 0
        return heater


class HeatPumpAir(SupplyBuilder):
    #Air-Water heat pump. epsilon_carnot = 0.4. Outside Temperature as reservoir temperature.

    def calcLoads(self):
        if self.Load > 0:                                   #Heating
            heater = SupplyOut()
            heater.energyIn = self.Load/(0.4*(self.supplyTemperature+273)/(self.supplyTemperature-self.theta_e))
            heater.electricityOut = 0
        else:                                               #Cooling
            heater = SupplyOut()
            heater.energyIn = self.Load/(0.4*(self.supplyTemperature+273)/(self.theta_e-self.SupplyTemperature))
            heater.electricityOut = 0
        return heater


class HeatPumpWater(SupplyBuilder):
    #Water-Water heat pump. epsilon_carnot = 0.5. Reservoir temperatures 7 degC (winter) and 12 degC (summer).

    def calcLoads(self):
        heater = SupplyOut()
        if self.Load > 0:                                   #Heating
            heater.energyIn = self.Load/(0.5*(self.supplyTemperature+273)/(self.supplyTemperature-7))
        else:                                               #Cooling 
            if self.supplyTemperature > 12:                 #Only by pumping 
                heater.energyIn = self.Load*0.1
            else:                                           #Heat Pump active
                heater.energyIn = self.Load/(0.5*(self.supplyTemperature+273)/(12-self.supplyTemperature))
        heater.electricityOut = 0
        return heater


class HeatPumpGround(SupplyBuilder):
    #Ground-Water heat pump. epsilon_carnot = 0.45. Reservoir temperatures 7 degC (winter) and 12 degC (summer). (Same as HeatPumpWater except for lower e_Carnot)

    def calcLoads(self):
        heater = SupplyOut()
        if self.Load > 0:                                   #Heating
            heater.energyIn = self.Load/(0.45*(self.supplyTemperature+273)/(self.supplyTemperature-7))
        else:                                               #Cooling 
            if self.supplyTemperature > 12:                 #Only by pumping 
                heater.energyIn = self.Load*0.1
            else:                                           #Heat Pump active
                heater.energyIn = self.Load/(0.45*(self.supplyTemperature+273)/(12-self.supplyTemperature))
        heater.electricityOut = 0
        return heater


class ElectricHeating(SupplyBuilder):
    #Straight forward electric heating. 100 percent conversion to heat.
    
    def calcLoads(self):
        heater=SupplyOut()
        heater.energyIn = self.Load
        heater.electricityOut = 0
        return heater
    


class CHP(SupplyBuilder):
    #Combined heat and power unit with 60 percent thermal and 33 percent electrical fuel conversion.
    
    def calcLoads(self):
        heater=SupplyOut()
        heater.energyIn = self.Load/0.6
        heater.electricityOut = heater.energyIn*0.33
        return heater

class DirectHeater(SupplyBuilder):
    #Created by PJ to check accuracy against previous simulation
    
    def calcLoads(self):
        heater=SupplyOut()
        heater.energyIn = self.Load
        heater.electricityOut = 0
        return heater

class DirectCooler(SupplyBuilder):
    #Created by PJ to check accuracy against previous simulation
    
    def calcLoads(self):
        heater=SupplyOut()
        heater.energyIn = self.Load
        heater.electricityOut = 0
        return heater

class COP3Heater(SupplyBuilder):
    #Created by PJ to check accuracy against previous simulation
    
    def calcLoads(self):
        heater=SupplyOut()
        heater.energyIn = self.Load/3.0
        heater.electricityOut = 0
        return heater

class COP3Cooler(SupplyBuilder):
    #Created by PJ to check accuracy against previous simulation
    
    def calcLoads(self):
        heater=SupplyOut()
        heater.energyIn = self.Load/3.0
        heater.electricityOut = 0
        return heater


class SupplyOut:
    #The System class which is used to output the final results
    energyIn = None
    electricityOut = None




#if __name__ == "__main__":
#    print "Resistive Office Heater"
#    director = Director()
#    director.setBuilder(HeatPumpHeater(Load=100, theta_e=10,theta_m_prev=20,efficiency=0.8))
#    system = director.calcSystem()
#
#
#    print system.electricity
#    print system.COP


