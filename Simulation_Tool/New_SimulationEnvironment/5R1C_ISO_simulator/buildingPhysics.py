"""
=========================================
Physics Required to calculate sensible space heating and space cooling loads
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
The equations presented here is this code are derived from ISO 13790 Annex C 

Methods are listed in order of apperance in the Annex



VARIABLE DEFINITION

theta_m_t: Medium temperature of the enxt time step 
theta_m_prev: Medium temperature from the previous time step
c_m: Thermal Capacitance of the medium 
h_tr_3: combined heat conductance, see function for definition
h_tr_em: Heat conductance from the outside through opaque elements TODO: Check this
phi_m_tot: see formula for the calculation, eq C.5 in standard

phi_m: Combination of internal and solar gains directly to the medium 
theta_e: External air temperature
phi_st: combination of internal and solar gains directly to the internal surface
h_tr_w: Heat transfer from the outside through windows, doors
h_tr_1: combined heat conductance, see function for definition
phi_ia: combination of internal and solar gains to the air 
phi_hc_nd: Heating and Cooling of the supply air
h_ve_adj: Ventilation heat transmission coefficient 
h_tr_2: combined heat conductance, see function for definition 

h_tr_is: Some heat transfer coefficient between the air and the inside surface TODO: Check this

H_tr_ms: Heat transfer coefficient between the internal surface temperature and the medium

theta_m: Some wierd average between the previous and current timestep of the medium TODO: Check this

"""



class Building(object):
	'''Sets the parameters of the building. '''

	def __init__(self, 
		Fenst_A=13.5 ,
		Room_Depth=7 ,
		Room_Width=4.9 ,
		Room_Height=3.1 ,
		glass_solar_transmitance=0.687 ,
		glass_light_transmitance=0.744 ,
		lighting_load=0.0117 ,
		lighting_control = 300,
		h_tr_em = 47 , 
		h_tr_w = 13,
		h_ve_adj = 45,
		c_m = 2.07*3.6*10**6,
		h_tr_ms = 45,
		h_tr_is = 15,
		theta_int_h_set = 20,
		theta_int_c_set = 26,

		):
		# type: (object, object, object, object, object, object, object, object, object, object, object, object, object, object, object, object) -> object

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

		#Calculated Propoerties
		self.A_f=Room_Depth*Room_Width #[m2] Floor Area
		self.A_m=self.A_f* 2.5 #[m2] Effective Mass Area assuming a medium weight building #12.3.1.2
		self.Room_Vol=Room_Width*Room_Depth*Room_Height #[m3] Room Volume
		self.A_t=self.A_f*2 + Room_Width*Room_Height*2 + Room_Depth*Room_Height*2 #TODO: Not sure what A_t is, check it out

		#Single Capacitance Model Parameters
		self.c_m=c_m #[kWh/K] Room Capacitance. Default based of Madsen2011, consider changing to ISO standard 12.3.1.2
		self.h_tr_em = h_tr_em #Conductance of opaque surfaces to exterior [W/K]
		self.h_tr_w = 	h_tr_w  #Conductance to exterior through glazed surfaces [W/K]
		self.h_ve_adj =	h_ve_adj  #Conductance through ventilation [W/M]
		self.c_m = c_m 			#Thermal Capacitance in J/K
		self.h_tr_ms = 	h_tr_ms #Opaque transimitance #TODO: Check what this really means
		self.h_tr_is = 	h_tr_is # Conductance from the conditioned air to interior building surface

		#Thermal set points
		self.theta_int_h_set = theta_int_h_set
		self.theta_int_c_set = theta_int_c_set

		#Thermal Properties
		self.has_heating_demand=False #Boolean for if heating is required
		self.has_cooling_demand=False #Boolean for if cooling is required
		self.phi_hc_nd=0 			#the heating/cooilng load
		self.phi_c_max = 100 #max cooling load
		self.phi_h_max = 100 #max heating load


	def calc_heatflow(self,phi_int, phi_sol):
		#C.1 - C.3 in [C.3 ISO 13790]


		self.phi_ia=0.5*phi_int

		self.phi_m=(self.A_m/self.A_t)*(0.5*phi_int+phi_sol)

		self.phi_st=(1-(self.A_m/self.A_t)-(self.h_tr_w/(9.1*self.A_t)))*(0.5*phi_int+phi_sol)

		'''manually checked, OK'''

	def calc_theta_m_t(self, theta_m_prev):

		# (C.4) in [C.3 ISO 13790]

		self.theta_m_t = ((theta_m_prev*((self.c_m/3600.0)-0.5*(self.h_tr_3+self.h_tr_em))) + self.phi_m_tot) / ((self.c_m/3600.0)+0.5*(self.h_tr_3+self.h_tr_em))




	def calc_phi_m_tot(self, theta_e, phi_hc_nd):

		# (C.5) in [C.3 ISO 13790]
		# h_ve = h_ve_adj and theta_sup = theta_e [9.3.2 ISO 13790]

		self.phi_m_tot = self.phi_m + self.h_tr_em*theta_e + \
		self.h_tr_3*(self.phi_st + self.h_tr_w*theta_e+self.h_tr_1*(((self.phi_ia+phi_hc_nd)/self.h_ve_adj)+theta_e))/self.h_tr_2

		print 'phi_m_tot =', self.phi_m_tot

	'''Functions to Caluculate the derived heat transfer simplifications'''

	def calc_h_tr_1(self):

		# (C.6) in [C.3 ISO 13790]

		self.h_tr_1 = 1.0/(1.0/self.h_ve_adj + 1.0/self.h_tr_is)

		print 'h_tr_1=', self.h_tr_1

	def calc_h_tr_2(self):

		# (C.7) in [C.3 ISO 13790]

		self.h_tr_2 = self.h_tr_1 + self.h_tr_w

		print 'h_tr_2 =',self.h_tr_2

	def calc_h_tr_3(self):

		# (C.8) in [C.3 ISO 13790]

		self.h_tr_3 = 1.0/(1.0/self.h_tr_2 + 1.0/self.h_tr_ms)
		
		print 'h_tr_3=', self.h_tr_3

	'''Functions to Calculate the temperatures at the nodes'''

	def calc_theta_m(self,theta_m_prev):
		#PJ doesn't understand this

		# (C.9) in [C.3 ISO 13790]
		self.theta_m = (self.theta_m_t+theta_m_prev)/2.0



	def calc_theta_s(self, theta_e, phi_hc_nd):

		# (C.10) in [C.3 ISO 13790]
		# h_ve = h_ve_adj and theta_sup = theta_e [9.3.2 ISO 13790]
		self.theta_s = (self.h_tr_ms*self.theta_m+self.phi_st+self.h_tr_w*theta_e+self.h_tr_1*(theta_e+(self.phi_ia+phi_hc_nd)/self.h_ve_adj)) / \
				  (self.h_tr_ms+self.h_tr_w+self.h_tr_1)



	def calc_theta_air(self, theta_e, phi_hc_nd):
		# (C.11) in [C.3 ISO 13790]
		# h_ve = h_ve_adj and theta_sup = theta_e [9.3.2 ISO 13790]

		self.theta_air = (self.h_tr_is * self.theta_s + self.h_ve_adj * theta_e + self.phi_ia + phi_hc_nd) / (self.h_tr_is + self.h_ve_adj)


	def calc_theta_op(self):

		# (C.12) in [C.3 ISO 13790]
		self.theta_op = 0.3 * self.theta_air + 0.7 * self.theta_s

	'''Derivate using the Crank-Nicolson method'''

	def calc_temperatures_crank_nicholson(self, phi_hc_nd, phi_int, phi_sol, theta_e, theta_m_prev):

		# calculates air temperature and operative temperature for a given heating/cooling load
		# section C.3 in [C.3 ISO 13790]


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

		phi_hc_nd=0
		self.calc_temperatures_crank_nicholson(phi_hc_nd, phi_int, phi_sol, theta_e, theta_m_prev)

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

		self.phi_hc_nd_un = phi_hc_nd_10*(theta_air_set - theta_air_0)/(theta_air_10 - theta_air_0)


	def calc_phi_hc_ac(self, phi_int, phi_sol, theta_e, theta_m_prev):

		# Crank-Nicholson calculation procedure if heating/cooling system is active
		# Step 1 - Step 4 in Section C.4.2 in [C.3 ISO 13790]

		# Step 1:
		phi_hc_nd_0 = 0
		theta_air_0=self.calc_temperatures_crank_nicholson(phi_hc_nd_0, phi_int, phi_sol, theta_e, theta_m_prev)[1] #This is more stable
		#theta_air_0 = self.theta_air #This should return the same value

		# Step 2:


		if self.has_heating_demand:
			theta_air_set = self.theta_int_h_set
		elif self.has_cooling_demand:
			theta_air_set=self.theta_int_c_set
		else:
			print "error heating function has been called event though no heating is required"

		phi_hc_nd_10 = 10 * self.A_f

		theta_air_10=self.calc_temperatures_crank_nicholson(phi_hc_nd_10, phi_int, phi_sol, theta_e, theta_m_prev)[1]
		#theta_air_10 = self.theta_air

		self.phi_hc_nd_un = self.calc_phi_hc_nd_un(phi_hc_nd_10,theta_air_set, theta_air_0, theta_air_10)

		# Step 3:


		if self.phi_c_max <= self.phi_hc_nd_un <= self.phi_h_max:

			self.phi_hc_nd_ac = phi_hc_nd_un
			self.theta_air_ac = theta_air_set

		# Step 4:
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


		#TODO: Define theta_m_prev and theta_e
		
		# building thermal properties at previous time step
		# +++++++++++++++++++++++++++++++++++++++++++++++++
		#theta_m_prev = None

		# environmental properties
		# ++++++++++++++++++++++++
		#theta_e = None

		# air flows
		# +++++++++
		m_ve_mech = None
		m_ve_window = None
		m_ve_leakage = None

		# air supply temperatures (HEX)
		# +++++++++++++++++++++++++++++
		temp_ve_mech = None

	   

		self.calc_h_tr_1()
		self.calc_h_tr_2()
		self.calc_h_tr_3()

		# check demand
		# ++++++++++++
		self.has_demand(phi_int, phi_sol,theta_e, theta_m_prev)

		if not self.has_heating_demand and not self.has_cooling_demand:

			# no heating or cooling demand
			# calculate temperatures of building R-C-model and exit
			# --> rc_model_function_1(...)
			self.phi_hc_nd = 0
			calc_temperatures_crank_nicholson( phi_hc_nd, phi_int, phi_sol, theta_e, theta_m_prev)

		   

		else:

			# has heating demand
			
			self.calc_phi_hc_ac(phi_int, phi_sol, theta_e, theta_m_prev)

			


		return


	def solve_building_lighting(self, ill, occupancy):

		Lux=ill/self.A_f #[Lx]

		if Lux < self.lighting_control and occupancy>0:
			self.lighting_demand=self.lighting_load*self.A_f #Lighting demand for the hour
		else:
			self.lighting_demand=0










