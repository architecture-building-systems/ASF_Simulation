"""
=========================================
Physics Required to calculate sensible space heating and space cooling loads, and space lighting loads
EN-13970
=========================================
"""

import numpy as np


__author__ = "Prageeth Jayathissa"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Gabriel Happle"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Prageeth Jayathissa"
__email__ = "jayathissa@arch.ethz.ch"
__status__ = "Production"



"""
The equations presented here is this code are derived from ISO 13790 Annex C, Methods are listed in order of apperance in the Annex 

Daylighting is based on methods in The Environmental Science Handbook, S V Szokolay

HOW TO USE
from buildingPhysics import Building #Importing Building Class
Office=Building() #Set an instance of the class
Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev) #Solve for Heating
Office.solve_building_lighting(ill, occupancy) #Solve for Lighting


VARIABLE DEFINITION

	phi_int: Internal Heat Gains [W]
	phi_sol: Solar Heat Gains [W]
	theta_e: Outdoor air temperature [C]
	theta_m_prev: Air temperature from the previous time step 
	ill: Illuminance in contact with the total outdoor window surface [lumens]
	occupancy: Occupancy [people/m2]

	theta_m_t: Medium temperature of the enxt time step [C]
	theta_m_prev: Medium temperature from the previous time step [C]
	theta_m: Some wierd average between the previous and current timestep of the medium  [C] #TODO: Check this 

	c_m: Thermal Capacitance of the medium [J/K]
	h_tr_is: Heat transfer coefficient between the air and the inside surface [W/K]
	h_tr_w: Heat transfer from the outside through windows, doors [W/K]
	H_tr_ms: Heat transfer coefficient between the internal surface temperature and the medium [W/K]
	h_tr_em: Heat conductance from the outside through opaque elements [W/K]
	h_ve_adj: Ventilation heat transmission coefficient [W/K]

	phi_m_tot: see formula for the calculation, eq C.5 in standard [W]
	phi_m: Combination of internal and solar gains directly to the medium [W]
	phi_st: combination of internal and solar gains directly to the internal surface [W]
	phi_ia: combination of internal and solar gains to the air [W]
	phi_hc_nd: Heating and Cooling of the supply air [W]

	h_tr_1: combined heat conductance, see function for definition [W/K]
	h_tr_2: combined heat conductance, see function for definition [W/K]
	h_tr_3: combined heat conductance, see function for definition [W/K]


	
INPUT PARAMETER DEFINITION 

	Fenst_A: Area of the Glazed Surface  [m2]
	Room_Depth=7.0 Depth of the modeled room [m]
	Room_Width=4.9 Width of the modeled room [m]
	Room_Height=3.1 Height of the modeled room [m]
	glass_solar_transmitance: Fraction of Radiation transmitting through the window []
	glass_light_transmitance: Fraction of visible light (luminance) transmitting through the window []
	lighting_load: Lighting Load [W/m2] 
	lighting_control: Lux threshold at which the lights turn on [Lx]
	U_em: U value of opaque surfaces  [W/m2K]
	U_w: U value of glazed surfaces [W/m2K]
	ACH_vent: Air changes per hour through ventilation [Air Changes Per Hour]
	ACH_infl: Air changes per hour through infiltration [Air Changes Per Hour]
	ventilation_efficiency: The efficiency of the heat recovery system for ventilation. Set to 0 if there is no heat recovery []
	c_m_A_f: Thermal capacitance of the room per floor area [J/m2K]
	theta_int_h_set : Thermal heating set point [C]
	theta_int_c_set: Thermal cooling set point [C]
	phi_c_max_A_f: Maximum cooling load. Set to -np.inf for unresctricted cooling [C]
	phi_h_max_A_f: Maximum heating load. Set to no.inf for unrestricted heating [C]

"""



class Building(object):
	'''Sets the parameters of the building. '''

	def __init__(self, 
		Fenst_A=13.5 ,
		Room_Depth=7.0 ,
		Room_Width=4.9 ,
		Room_Height=3.1 ,
		glass_solar_transmitance=0.687 ,
		glass_light_transmitance=0.744 ,
		lighting_load=11.7 ,
		lighting_control = 300,
		Lighting_Utilisation_Factor=0.45,
		Lighting_MaintenanceFactor=0.9,
		U_em = 0.2 , 
		U_w = 1.1,
		ACH_vent=1.5,
		ACH_infl=0.5,
		ventilation_efficiency=.6,
		c_m_A_f = 165000,
		theta_int_h_set = 20.0,
		theta_int_c_set = 26.0,
		phi_c_max_A_f=-20.0,
		phi_h_max_A_f=20.0,

		):
		

		#Building Dimensions
		self.Fenst_A=Fenst_A #[m2] Window Area
		self.Room_Depth=Room_Depth #[m] Room Depth
		self.Room_Width=Room_Width #[m] Room Width
		self.Room_Height=Room_Height #[m] Room Height

		#Fenstration and Lighting Properties
		self.glass_solar_transmitance=glass_solar_transmitance #Dbl LoE (e=0.2) Clr 3mm/13mm Air
		self.glass_light_transmitance=glass_light_transmitance #Dbl LoE (e=0.2) Clr 3mm/13mm Air
		self.lighting_load=lighting_load #[kW/m2] lighting load
		self.lighting_control = lighting_control #[lux] Lighting setpoint
		self.Lighting_Utilisation_Factor=Lighting_Utilisation_Factor #How the light entering the window is transmitted to the working plane
		self.Lighting_MaintenanceFactor= Lighting_MaintenanceFactor #How dirty the window is. Section 2.2.3.1 Environmental Science Handbook

		#Calculated Propoerties
		self.A_f=Room_Depth*Room_Width #[m2] Floor Area
		self.A_m=self.A_f* 2.5 #[m2] Effective Mass Area assuming a medium weight building #12.3.1.2
		self.Room_Vol=Room_Width*Room_Depth*Room_Height #[m3] Room Volume
		self.A_tot=self.A_f*2 + Room_Width*Room_Height*2 + Room_Depth*Room_Height*2
		self.A_t=self.A_tot #TODO: Not sure what A_t is, check it out

		#Single Capacitance  5 conductance Model Parameters
		self.c_m=c_m_A_f*self.A_f #[kWh/K] Room Capacitance. Default based on ISO standard 12.3.1.2 for medium heavy buildings
		self.h_tr_em = U_em*(Room_Height*Room_Width-Fenst_A) #Conductance of opaque surfaces to exterior [W/K]
		self.h_tr_w = 	U_w*Fenst_A  #Conductance to exterior through glazed surfaces [W/K], based on U-wert of 1W/m2K
		
		#Determine the ventilation conductance
		ACH_tot=ACH_infl+ACH_vent #Total Air Changes Per Hour
		b_ek=(1-(ACH_vent/(ACH_tot))*ventilation_efficiency) #temperature adjustement factor taking ventilation and inflimtration [ISO: E -27]
		self.h_ve_adj =	1200*b_ek*self.Room_Vol*(ACH_tot/3600)  #Conductance through ventilation [W/M]
		self.h_tr_ms = 	9.1 * self.A_m #Transmitance from the internal air to the thermal mass of the building
		self.h_tr_is = 	self.A_tot * 3.45 # Conductance from the conditioned air to interior building surface

		#Thermal set points
		self.theta_int_h_set = theta_int_h_set
		self.theta_int_c_set = theta_int_c_set

		#Thermal Properties
		self.has_heating_demand=False #Boolean for if heating is required
		self.has_cooling_demand=False #Boolean for if cooling is required
		self.phi_c_max = phi_c_max_A_f*self.A_f #max cooling load
		self.phi_h_max = phi_h_max_A_f*self.A_f #max heating load


	def calc_heatflow(self,phi_int, phi_sol):
		#C.1 - C.3 in [C.3 ISO 13790]

		#Calculates the heat flows to various points of the building based on the breakdown in section C.2, formulas C.1-C.3

		self.phi_ia=0.5*phi_int

		self.phi_m=(self.A_m/self.A_t)*(0.5*phi_int+phi_sol)

		self.phi_st=(1-(self.A_m/self.A_t)-(self.h_tr_w/(9.1*self.A_t)))*(0.5*phi_int+phi_sol)


	def calc_theta_m_t(self, theta_m_prev):

		# (C.4) in [C.3 ISO 13790]

		#Primary Equation, calculates the temperature of the next time step

		self.theta_m_t = ((theta_m_prev*((self.c_m/3600.0)-0.5*(self.h_tr_3+self.h_tr_em))) + self.phi_m_tot) / ((self.c_m/3600.0)+0.5*(self.h_tr_3+self.h_tr_em))




	def calc_phi_m_tot(self, theta_e, phi_hc_nd):

		# (C.5) in [C.3 ISO 13790]
		# h_ve = h_ve_adj and theta_sup = theta_e [9.3.2 ISO 13790]

		#Calculates a global heat transfer. This is a definition used to simplify equation calc_theta_m_t so it's not so long

		theta_sup=theta_e #Supply air comes straight from the outside air

		self.phi_m_tot = self.phi_m + self.h_tr_em*theta_e + \
		self.h_tr_3*(self.phi_st + self.h_tr_w*theta_e+self.h_tr_1*(((self.phi_ia+phi_hc_nd)/self.h_ve_adj)+theta_sup))/self.h_tr_2

		#print 'phi_m_tot =', self.phi_m_tot



	def calc_h_tr_1(self):

		# (C.6) in [C.3 ISO 13790]

		#Definition to simplify calc_phi_m_tot

		self.h_tr_1 = 1.0/(1.0/self.h_ve_adj + 1.0/self.h_tr_is)

		#print 'h_tr_1=', self.h_tr_1

	def calc_h_tr_2(self):

		# (C.7) in [C.3 ISO 13790]

		#Definition to simplify calc_phi_m_tot
		self.h_tr_2 = self.h_tr_1 + self.h_tr_w

		#print 'h_tr_2 =',self.h_tr_2

	def calc_h_tr_3(self):
		# (C.8) in [C.3 ISO 13790]

		#Definition to simplify calc_phi_m_tot
		self.h_tr_3 = 1.0/(1.0/self.h_tr_2 + 1.0/self.h_tr_ms)
		
		#print 'h_tr_3=', self.h_tr_3

	'''Functions to Calculate the temperatures at the nodes'''

	def calc_theta_m(self,theta_m_prev):
		#PJ doesn't understand this but it's in the ISO standard

		# (C.9) in [C.3 ISO 13790]
		self.theta_m = (self.theta_m_t+theta_m_prev)/2.0



	def calc_theta_s(self, theta_e, phi_hc_nd):

		# (C.10) in [C.3 ISO 13790]
		# h_ve = h_ve_adj and theta_sup = theta_e [9.3.2 ISO 13790]

		#Calculate the temperature of the inside room surfaces
		theta_sup=theta_e

		self.theta_s = (self.h_tr_ms*self.theta_m+self.phi_st+self.h_tr_w*theta_e+self.h_tr_1*(theta_sup+(self.phi_ia+phi_hc_nd)/self.h_ve_adj)) / \
				  (self.h_tr_ms+self.h_tr_w+self.h_tr_1)



	def calc_theta_air(self, theta_e, phi_hc_nd):
		# (C.11) in [C.3 ISO 13790]
		# h_ve = h_ve_adj and theta_sup = theta_e [9.3.2 ISO 13790]

		theta_sup=theta_e

		#Calculate the temperature of the inside air
		self.theta_air = (self.h_tr_is * self.theta_s + self.h_ve_adj * theta_sup + self.phi_ia + phi_hc_nd) / (self.h_tr_is + self.h_ve_adj)


	def calc_theta_op(self):

		# (C.12) in [C.3 ISO 13790]

		#The opperative temperature is a weighted average of the air and mean radiant temperatures. It is not used in any further calculation at this stage
		self.theta_op = 0.3 * self.theta_air + 0.7 * self.theta_s

	'''Derivate using the Crank-Nicolson method'''

	def calc_temperatures_crank_nicholson(self, phi_hc_nd, phi_int, phi_sol, theta_e, theta_m_prev):
		# section C.3 in [C.3 ISO 13790]

		# calculates air temperature and operative temperature for a given heating/cooling load
		#It effectively runs all the functions above

		


		self.calc_heatflow(phi_int, phi_sol)

		self.calc_phi_m_tot(theta_e, phi_hc_nd)

		self.calc_theta_m_t(theta_m_prev)

		self.calc_theta_m(theta_m_prev)

		self.calc_theta_s(theta_e, phi_hc_nd)

		self.calc_theta_air(theta_e, phi_hc_nd)

		self.calc_theta_op()

		return self.theta_m_t, self.theta_air, self.theta_op

	def has_demand(self,phi_int, phi_sol,theta_e, theta_m_prev):

		# step 1 in section C.4.2 in [C.3 ISO 13790]

		#Determines if the building has a heating or cooling demand

		phi_hc_nd=0
		#Determine the temperatures at various nodes
		self.calc_temperatures_crank_nicholson(phi_hc_nd, phi_int, phi_sol, theta_e, theta_m_prev)

		#If the air temperature is less or greater than the set temperature, there is a heating/cooling load
		if self.theta_air < self.theta_int_h_set:
			self.has_heating_demand=True
			self.has_cooling_demand=False
		elif self.theta_air > self.theta_int_c_set:
			self.has_cooling_demand=True
			self.has_heating_demand=False
		else:
			self.has_heating_demand=False
			self.has_cooling_demand=False


	def calc_phi_hc_nd_un(self, phi_hc_nd_10, theta_air_set, theta_air_0, theta_air_10):

		# calculates unrestricted heating power
		# (C.13) in [C.3 ISO 13790]

		'''Based on the Thales Intercept Theorem. 
		Where we set a heating case that is 10x the floor area and determine the temperature as a result 
		Assuming that the relation is linear, one can draw a right angle triangle. 
		From this we can determine the heating level required to achieve the set point temperature
		This assumes a perfect HVAC control system
		'''
		self.phi_hc_nd_un = phi_hc_nd_10*(theta_air_set - theta_air_0)/(theta_air_10 - theta_air_0)


	def calc_phi_hc_ac(self, phi_int, phi_sol, theta_e, theta_m_prev):

		# Crank-Nicholson calculation procedure if heating/cooling system is active
		# Step 1 - Step 4 in Section C.4.2 in [C.3 ISO 13790]

		# Step 1: Check if heating or cooling is needed
		#Set heating/cooling to 0
		phi_hc_nd_0 = 0
		#Calculate the air temperature with no heating/cooling
		theta_air_0=self.calc_temperatures_crank_nicholson(phi_hc_nd_0, phi_int, phi_sol, theta_e, theta_m_prev)[1] #This is more stable
		#theta_air_0 = self.theta_air #This should return the same value


		# Step 2: Calculate the unrestricted heating/cooling required

		#determine if we need heating or cooling based based on the condition that no heating or cooling is required
		if self.has_heating_demand:
			theta_air_set = self.theta_int_h_set
		elif self.has_cooling_demand:
			theta_air_set=self.theta_int_c_set
		else:
			print "error heating function has been called event though no heating is required"

		#Set a heating case where the heating load is 10x the floor area
		phi_hc_nd_10 = 10 * self.A_f

		#Calculate the air temperature obtained by having this 10x setpoint
		theta_air_10=self.calc_temperatures_crank_nicholson(phi_hc_nd_10, phi_int, phi_sol, theta_e, theta_m_prev)[1]
		#theta_air_10 = self.theta_air

		#Determine the unrestricted heating/cooling off the building
		self.calc_phi_hc_nd_un(phi_hc_nd_10,theta_air_set, theta_air_0, theta_air_10)

		# Step 3: Check if available heating or cooling power is sufficient
		#print 'hello', self.phi_hc_nd_un
		if self.phi_c_max <= self.phi_hc_nd_un <= self.phi_h_max:


			self.phi_hc_nd_ac = self.phi_hc_nd_un
			self.theta_air_ac = theta_air_set #not sure what this is used for at this stage TODO

		# Step 4: if not sufficient then set the heating/cooling setting to the maximum
		elif self.phi_hc_nd_un > self.phi_h_max: # necessary heating power exceeds maximum available power

			self.phi_hc_nd_ac = self.phi_h_max

		elif self.phi_hc_nd_un < self.phi_c_max: # necessary cooling power exceeds maximum available power

			self.phi_hc_nd_ac = self.phi_c_max

		else: # unknown situation

			self.phi_hc_nd_ac = 0
			print('ERROR: unknown radiative heating/cooling system status')


		# calculate system temperatures for Step 3/Step 4
		temp_ac = self.calc_temperatures_crank_nicholson(self.phi_hc_nd_ac, phi_int, phi_sol, theta_e, theta_m_prev)

		# theta_m_t_ac = temp_ac[0]
		# theta_air_ac = temp_ac[1]  # should be the same as theta_air_set in the first case
		# theta_op_ac = temp_ac[2]

		# # exit calculation
		# return theta_m_t_ac, theta_air_ac, theta_op_ac, phi_hc_nd_ac



	def solve_building_energy(self,phi_int, phi_sol,theta_e, theta_m_prev):


		#Calculate the heat transfer definitions for formula simplification
		self.calc_h_tr_1()
		self.calc_h_tr_2()
		self.calc_h_tr_3()

		# check demand
		self.has_demand(phi_int, phi_sol,theta_e, theta_m_prev)

		if not self.has_heating_demand and not self.has_cooling_demand:

			# no heating or cooling demand
			# calculate temperatures of building R-C-model and exit
			# --> rc_model_function_1(...)
			self.phi_hc_nd_ac=0
			self.calc_temperatures_crank_nicholson( self.phi_hc_nd_ac, phi_int, phi_sol, theta_e, theta_m_prev)

		   

		else:

			# has heating/cooling demand
			
			self.calc_phi_hc_ac(phi_int, phi_sol, theta_e, theta_m_prev)

			


		return

	####################################################Lighting Calculations###################################################
	def solve_building_lighting(self, ill, occupancy):

		#Cite: Environmental Science Handbook, SV Szokolay, Section 2.2.1.3
		Lux=(ill*self.Lighting_Utilisation_Factor*self.Lighting_MaintenanceFactor*self.glass_light_transmitance)/self.A_f #[Lx]

		if Lux < self.lighting_control and occupancy>0:
			self.lighting_demand=self.lighting_load*self.A_f #Lighting demand for the hour
		else:
			self.lighting_demand=0










