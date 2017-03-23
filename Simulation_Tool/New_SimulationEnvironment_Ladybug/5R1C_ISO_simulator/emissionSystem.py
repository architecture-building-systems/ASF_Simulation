"""
=========================================
Emission System Parameters for Heating and Cooling

=========================================
"""

import numpy as np


__author__ = "Prageeth Jayathissa, Michael Fehr"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = [""]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Prageeth Jayathissa"
__email__ = "jayathissa@arch.ethz.ch"
__status__ = "Production"



"""
Model of different Emission systems. New Emission Systems can be introduced by adding new classes
"""

class EmissionDirector:

    """
    The director sets what Emission system is being used, and runs that set Emission system
    """

#    __builder = None
    builder = None

    #Sets what Emission system is used
    def setBuilder(self, builder):
#        self.__builder = builder
        self.builder = builder
    # Calcs the energy load of that system. This is the main() fu
    def calcFlows(self):

        # Director asks the builder to produce the system body. self.__builder is an instance of the class

#        body = self.__builder.heatFlows()
        body = self.builder.heatFlows()

        return body





class EmissionBuilder:

    """ The base class in which systems are built from
    """

    def __init__(self, theta_e, phi_int, phi_sol, phi_hc_nd, A_m, A_t, h_tr_w, theta_int_h_set, theta_int_c_set):
      self.theta_e = theta_e   #Outdoor Air Temperature
      self.phi_int = phi_int
      self.phi_sol = phi_sol
      self.phi_hc_nd = phi_hc_nd
      self.A_m = A_m
      self.A_t = A_t
      self.h_tr_w = h_tr_w
      self.theta_int_h_set = theta_int_h_set
      self.theta_int_c_set = theta_int_c_set

    def heatFlows(self): pass

    name = None



class OldRadiators(EmissionBuilder):
    #Old building with radiators and high supply temperature

    def heatFlows(self):
        flows = EmissionOut()
        flows.phi_ia = 0.5*(self.phi_int+self.phi_hc_nd)
        flows.phi_st = (1-(self.A_m/self.A_t)-(self.h_tr_w/(9.1*self.A_t)))*(0.5*(self.phi_int+self.phi_hc_nd)+self.phi_sol)
        flows.phi_m = (self.A_m/self.A_t)*(0.5*(self.phi_int+self.phi_hc_nd)+self.phi_sol)
        flows.heatingSupplyTemperature = self.theta_int_h_set - 37.0/30 * (self.theta_e-self.theta_int_h_set)
        flows.coolingSupplyTemperature = self.theta_int_c_set - 37.0/30 * (self.theta_e-self.theta_int_c_set)
        return flows

    name = 'Old Radiators'

class NewRadiators(EmissionBuilder):
    #Newer building with radiators and medium supply temperature

    def heatFlows(self):
        flows = EmissionOut()
        flows.phi_ia = 0.5*(self.phi_int+self.phi_hc_nd)
        flows.phi_st = (1-(self.A_m/self.A_t)-(self.h_tr_w/(9.1*self.A_t)))*(0.5*(self.phi_int+self.phi_hc_nd)+self.phi_sol)
        flows.phi_m = (self.A_m/self.A_t)*(0.5*(self.phi_int+self.phi_hc_nd)+self.phi_sol)
        flows.heatingSupplyTemperature = self.theta_int_h_set - 24.0/30 * (self.theta_e-self.theta_int_h_set)
        flows.coolingSupplyTemperature = self.theta_int_c_set - 24.0/30 * (self.theta_e-self.theta_int_c_set)
        return flows
    
    name = 'New Radiators'

class ChilledBeams(EmissionBuilder):
    #Chilled beams: identical to newRadiators but used for cooling 

    def heatFlows(self):
        flows = EmissionOut()
        flows.phi_ia = 0.5*(self.phi_int+self.phi_hc_nd)
        flows.phi_st = (1-(self.A_m/self.A_t)-(self.h_tr_w/(9.1*self.A_t)))*(0.5*(self.phi_int+self.phi_hc_nd)+self.phi_sol)
        flows.phi_m = (self.A_m/self.A_t)*(0.5*(self.phi_int+self.phi_hc_nd)+self.phi_sol)
        flows.heatingSupplyTemperature = self.theta_int_h_set - 24.0/30 * (self.theta_e-self.theta_int_h_set)
        flows.coolingSupplyTemperature = self.theta_int_c_set - 24.0/30 * (self.theta_e-self.theta_int_c_set)
        return flows

    name = 'Chilled Beams'

class AirConditioning(EmissionBuilder):
    #All heat is given to the air via an AC-unit. HC input via the air node as in the ISO standard.
    #supplyTemperature as with new radiators (assumption)

    def heatFlows(self):
        flows = EmissionOut()
        flows.phi_ia = 0.5*self.phi_int+self.phi_hc_nd
        flows.phi_st = (1-(self.A_m/self.A_t)-(self.h_tr_w/(9.1*self.A_t)))*(0.5*self.phi_int+self.phi_sol)
        flows.phi_m = (self.A_m/self.A_t)*(0.5*self.phi_int+self.phi_sol)
        flows.heatingSupplyTemperature = self.theta_int_h_set-24.0/30* (self.theta_e-self.theta_int_h_set)
        flows.coolingSupplyTemperature = self.theta_int_c_set-24.0/30* (self.theta_e-self.theta_int_c_set)
        return flows

    name = 'Air Conditioning'

class FloorHeating(EmissionBuilder):
    #All HC energy goes into the surface node, supplyTemperature low

    def heatFlows(self):
        flows = EmissionOut()
        flows.phi_ia = 0.5*self.phi_int
        flows.phi_st = (1-(self.A_m/self.A_t)-(self.h_tr_w/(9.1*self.A_t)))*(0.5*self.phi_int+self.phi_sol)+self.phi_hc_nd
        flows.phi_m = (self.A_m/self.A_t)*(0.5*self.phi_int+self.phi_sol)
        flows.heatingSupplyTemperature = self.theta_int_h_set - 18.0/30 * (self.theta_e-self.theta_int_h_set)
        flows.coolingSupplyTemperature = self.theta_int_c_set - 18.0/30 * (self.theta_e-self.theta_int_c_set)
        return flows

    name = 'Floor Heating'

class TABS(EmissionBuilder):
    #Thermally activated Building systems. HC energy input into bulk node. Supply Temperature low.

    def heatFlows(self):
        flows = EmissionOut()
        flows.phi_ia = 0.5*self.phi_int
        flows.phi_st = (1-(self.A_m/self.A_t)-(self.h_tr_w/(9.1*self.A_t)))*(0.5*self.phi_int+self.phi_sol)
        flows.phi_m = (self.A_m/self.A_t)*(0.5*self.phi_int+self.phi_sol)+self.phi_hc_nd
        flows.heatingSupplyTemperature = self.theta_int_h_set - 18.0/30 * (self.theta_e-self.theta_int_h_set)
        flows.coolingSupplyTemperature = self.theta_int_c_set - 18.0/30 * (self.theta_e-self.theta_int_c_set)
        return flows

    name = 'TABS'

class EmissionOut:
    #The System class which is used to output the final results

    phi_ia= None

    phi_m= None

    phi_st= None

    heatingSupplyTemperature = None
    coolingSupplyTemperature = None



#if __name__ == "__main__":
#    print "Resistive Office Heater"
#    director = Director()
#    director.setBuilder(HeatPumpHeater(Load=100, theta_e=10,theta_m_prev=20,efficiency=0.8))
#    system = director.calcSystem()
#
#
#    print system.electricity
#    print system.COP


