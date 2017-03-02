"""
=========================================
Building System Parameters for Heating and Cooling

=========================================
"""

import numpy as np


__author__ = "Prageeth Jayathissa"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = [""]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Prageeth Jayathissa"
__email__ = "jayathissa@arch.ethz.ch"
__status__ = "Production"



"""
Model of different building systems. New Building Systems can be introduced by adding new classes
"""

class Director:
	
	"""
	The director sets what building system is being used, and runs that set building system
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


class Builder:

	""" The base class in which systems are built from 
	"""

	def __init__(self, Load, theta_e, theta_m_prev, efficiency):
		self.Load=Load #Energy Demand of the building at that time step
		self.theta_e=theta_e #Outdoor Air Temperature
		self.theta_m_prev=theta_m_prev #Room Temperature at that timestep
		self.efficiency=efficiency #Efficiency of the system

	def calcLoads(self): pass
	def calcCoolingLoads(self): pass


class DirectHeater(Builder):
	#The direct heater outputs the raw energy demand. No modifications are made

	def calcLoads(self):
		heater = System()
		heater.electricity = self.Load
		return heater


class DirectCooler(Builder):
	#The direct cooler outputs the raw energy demand. No modificactons are made

	def calcLoads(self):
		heater = System()
		heater.electricity = self.Load
		return heater

class ResistiveHeater(Builder):
	#The resistive heater converts electricty to heat with a set efficiency

	def calcLoads(self):
		heater = System()
		heater.electricity = self.Load * self.efficiency
		return heater


class HeatPumpHeater(Builder):
	#The heat pump calculates a COP with an efficiency and outputs the electricty input requirement

	def calcLoads(self):
		heater= System()
		heater.COP=self.efficiency*((self.theta_m_prev+273.0)/(self.theta_m_prev-self.theta_e))
		heater.electricity=self.Load/heater.COP
		return heater

class HeatPumpCooler(Builder):
	#The heat pump calculates a COP with an efficiency and outputs the electricty input requirement
	
	def calcLoads(self):
		cooler=System()
		cooler.COP=self.efficiency*((self.theta_m_prev+273.0)/(self.theta_e-self.theta_m_prev))
		cooler.electricity=self.Load/cooler.COP
		return cooler


class System:
	#The System class which is used to output the final results
	electricity = None
	COP=None




if __name__ == "__main__":
	print "Resistive Office Heater"
	director = Director()
	director.setBuilder(HeatPumpHeater(Load=100, theta_e=10,theta_m_prev=20,efficiency=0.8))
	system = director.calcSystem()


	print system.electricity
	print system.COP


