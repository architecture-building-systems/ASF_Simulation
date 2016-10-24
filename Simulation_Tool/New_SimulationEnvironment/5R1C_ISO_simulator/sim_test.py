import unittest
import numpy as np
from buildingPhysics import Building #Importing Building Class

class TestBuildingSim(unittest.TestCase):



	def test_NoHVACNoLight(self):
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
		Office=Building(Fenst_A=13.5 ,
		Room_Depth=7 ,
		Room_Width=4.9 ,
		Room_Height=3.1 ,
		glass_solar_transmitance=0.687 ,
		glass_light_transmitance=0.744 ,
		lighting_load=0.0117 ,
		lighting_control = 300,
		U_em = 0.2 , 
		U_w = 1.1,
		ACH=2,
		c_m_A_f = 165000,
		theta_int_h_set = 20,
		theta_int_c_set = 26,
		phi_c_max_A_f=-12,
		phi_h_max_A_f=12,
		)

		Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)
		Office.solve_building_lighting(ill, occupancy)

		self.assertEqual(round(Office.theta_m,2), 22.33)
		self.assertEqual(Office.phi_hc_nd_ac,0)
		self.assertEqual(Office.lighting_demand,0)

	def test_CoolingRequired(self):
		theta_e=25
		theta_m_prev=24
		#Internal heat gains, in Watts
		phi_int=10

		#Solar heat gains after transmitting through the winow, in Watts
		phi_sol=4000

		#Illuminance after transmitting through the window 
		ill=14000 #Lumens

		#Occupancy for the timestep [people/hour/square_meter]
		occupancy = 0.1

		#Set Building Parameters
		Office=Building(Fenst_A=13.5 ,
		Room_Depth=7 ,
		Room_Width=4.9 ,
		Room_Height=3.1 ,
		glass_solar_transmitance=0.687 ,
		glass_light_transmitance=0.744 ,
		lighting_load=0.0117 ,
		lighting_control = 300,
		U_em = 0.2 , 
		U_w = 1.1,
		ACH=2,
		c_m_A_f = 165000,
		theta_int_h_set = 20,
		theta_int_c_set = 26,
		phi_c_max_A_f=-12,
		phi_h_max_A_f=12,
		)

		Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)
		Office.solve_building_lighting(ill, occupancy)

		self.assertEqual(round(Office.phi_hc_nd_ac,2), -264.75)
		self.assertEqual(round(Office.theta_m,2), 25.15)
		self.assertTrue(Office.has_cooling_demand)
		
		self.assertEqual(Office.lighting_demand,0)

	def test_HeatingRequired(self):


		theta_e=10
		theta_m_prev=20
		#Internal heat gains, in Watts
		phi_int=10

		#Solar heat gains after transmitting through the winow, in Watts
		phi_sol=2000

		#Illuminance after transmitting through the window 
		ill=14000 #Lumens

		#Occupancy for the timestep [people/hour/square_meter]
		occupancy = 0.1

		#Set Building Parameters
		Office=Building(Fenst_A=13.5 ,
		Room_Depth=7 ,
		Room_Width=4.9 ,
		Room_Height=3.1 ,
		glass_solar_transmitance=0.687 ,
		glass_light_transmitance=0.744 ,
		lighting_load=0.0117 ,
		lighting_control = 300,
		U_em = 0.2 , 
		U_w = 1.1,
		ACH=2,
		c_m_A_f = 165000,
		theta_int_h_set = 20,
		theta_int_c_set = 26,
		phi_c_max_A_f=-12,
		phi_h_max_A_f=12,
		)

		Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)
		Office.solve_building_lighting(ill, occupancy)

		self.assertEqual(round(Office.theta_m,2), 20.46)
		self.assertTrue(Office.has_heating_demand)
		self.assertEqual(round(Office.phi_hc_nd_ac,2), 328.09)
		self.assertEqual(Office.lighting_demand,0)

	def test_MaxCoolingRequired(self):
		theta_e=30
		theta_m_prev=25
		#Internal heat gains, in Watts
		phi_int=10

		#Solar heat gains after transmitting through the winow, in Watts
		phi_sol=5000

		#Illuminance after transmitting through the window 
		ill=14000 #Lumens

		#Occupancy for the timestep [people/hour/square_meter]
		occupancy = 0.1

		#Set Building Parameters
		Office=Building(Fenst_A=13.5 ,
		Room_Depth=7 ,
		Room_Width=4.9 ,
		Room_Height=3.1 ,
		glass_solar_transmitance=0.687 ,
		glass_light_transmitance=0.744 ,
		lighting_load=0.0117 ,
		lighting_control = 300,
		U_em = 0.2 , 
		U_w = 1.1,
		ACH=2,
		c_m_A_f = 165000,
		theta_int_h_set = 20,
		theta_int_c_set = 26,
		phi_c_max_A_f=-12,
		phi_h_max_A_f=12,
		)

		Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)
		Office.solve_building_lighting(ill, occupancy)

		self.assertEqual(round(Office.theta_m,2), 26.49)
		self.assertTrue(Office.has_cooling_demand)
		self.assertEqual(round(Office.phi_hc_nd_ac,2), -411.6)
		self.assertEqual(Office.lighting_demand,0)

	def test_MaxHeatingRequired(self):


		theta_e=5
		theta_m_prev=19
		#Internal heat gains, in Watts
		phi_int=10

		#Solar heat gains after transmitting through the winow, in Watts
		phi_sol=2000

		#Illuminance after transmitting through the window 
		ill=14000 #Lumens

		#Occupancy for the timestep [people/hour/square_meter]
		occupancy = 0.1

		#Set Building Parameters
		Office=Building(Fenst_A=13.5 ,
		Room_Depth=7 ,
		Room_Width=4.9 ,
		Room_Height=3.1 ,
		glass_solar_transmitance=0.687 ,
		glass_light_transmitance=0.744 ,
		lighting_load=0.0117 ,
		lighting_control = 300,
		U_em = 0.2 , 
		U_w = 1.1,
		ACH=2,
		c_m_A_f = 165000,
		theta_int_h_set = 20,
		theta_int_c_set = 26,
		phi_c_max_A_f=-12,
		phi_h_max_A_f=12,
		)

		Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)
		Office.solve_building_lighting(ill, occupancy)

		self.assertEqual(round(Office.theta_m,2), 19.39)
		self.assertTrue(Office.has_heating_demand)
		self.assertEqual(round(Office.phi_hc_nd_ac,2), 411.6)
		self.assertEqual(Office.lighting_demand,0)

	def test_lightingrequired(self):

		theta_e=10
		theta_m_prev=22
		#Internal heat gains, in Watts
		phi_int=10

		#Solar heat gains after transmitting through the winow, in Watts
		phi_sol=2000

		#Illuminance after transmitting through the window 
		ill=4000 #Lumens

		#Occupancy for the timestep [people/hour/square_meter]
		occupancy = 0.1

		#Set Building Parameters
		Office=Building(Fenst_A=13.5 ,
		Room_Depth=7 ,
		Room_Width=4.9 ,
		Room_Height=3.1 ,
		glass_solar_transmitance=0.687 ,
		glass_light_transmitance=0.744 ,
		lighting_load=0.0117 ,
		lighting_control = 300,
		U_em = 0.2 , 
		U_w = 1.1,
		ACH=2,
		c_m_A_f = 165000,
		theta_int_h_set = 20,
		theta_int_c_set = 26,
		phi_c_max_A_f=-12,
		phi_h_max_A_f=12,
		)

		Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)
		Office.solve_building_lighting(ill, occupancy)

		self.assertEqual(round(Office.theta_m,2), 22.33)
		self.assertEqual(Office.phi_hc_nd_ac,0)
		self.assertEqual(round(Office.lighting_demand,2),0.40)



if __name__ == '__main__':
	unittest.main()



