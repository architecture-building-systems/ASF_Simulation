from buildingSystem import *

if __name__ == "__main__":

	Heating=HeatPumpHeater

	Cooling=HeatPumpCooler

	print "Resistive Office Heater"
	director = Director()

	director.setBuilder(Heating(Load=100, theta_e=10,theta_m_prev=20,efficiency=0.5))
	system = director.calcSystem()

	director.setBuilder(Cooling(Load=100, theta_e=35,theta_m_prev=20,efficiency=0.5))
 
	system = director.calcSystem()


	print system.electricity
	print system.COP
