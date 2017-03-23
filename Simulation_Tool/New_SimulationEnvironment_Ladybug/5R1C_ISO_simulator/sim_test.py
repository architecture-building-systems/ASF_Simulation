import unittest
import numpy as np
from buildingPhysics import Building #Importing Building Class
from supplySystem import *
from emissionSystem import *

class TestBuildingSim(unittest.TestCase):



    def test_NoHVACNoLight(self):
        theta_e=10
        theta_m_prev=22
        #Internal heat gains, in Watts
        phi_int=10

        #Solar heat gains after transmitting through the winow, in Watts
        phi_sol=2000

        #Illuminance after transmitting through the window 
        ill=44000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        #Set Building Parameters
        Office=Building(Fenst_A=13.5 ,
        Room_Depth=7 ,
        Room_Width=4.9 ,
        Room_Height=3.1 ,
        glass_solar_transmittance=0.687 ,
        glass_light_transmittance=0.744 ,
        lighting_load=11.7 ,
        lighting_control = 300,
        Lighting_Utilisation_Factor=0.45,
        Lighting_Maintenance_Factor=0.9,
        U_em = 0.2 , 
        U_w = 1.1,
        ACH_vent=1.5,
        ACH_infl=0.5,
        ventilation_efficiency=0,
        c_m_A_f = 165000,
        theta_int_h_set = 20,
        theta_int_c_set = 26,
        phi_c_max_A_f=-12,
        phi_h_max_A_f=12,
        heatingSupplySystem=DirectHeater,
        coolingSupplySystem=DirectCooler,
        heatingEmissionSystem=AirConditioning,
        coolingEmissionSystem=AirConditioning,
        )

        Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)
        Office.solve_building_lighting(ill, occupancy)


        self.assertEqual(round(Office.theta_m,2), 22.33)
        self.assertEqual(Office.phi_hc_nd_ac,0)
        self.assertEqual(round(Office.heatingSysElectricity,2),0)
        self.assertEqual(round(Office.coolingSysElectricity,2),0)
        self.assertEqual(Office.lighting_demand,0)


    def test_CoolingRequired(self):
        theta_e=25
        theta_m_prev=24
        #Internal heat gains, in Watts
        phi_int=10

        #Solar heat gains after transmitting through the winow, in Watts
        phi_sol=4000

        #Illuminance after transmitting through the window 
        ill=44000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        #Set Building Parameters
        Office=Building(Fenst_A=13.5 ,
        Room_Depth=7 ,
        Room_Width=4.9 ,
        Room_Height=3.1 ,
        glass_solar_transmittance=0.687 ,
        glass_light_transmittance=0.744 ,
        lighting_load=11.7 ,
        lighting_control = 300,
        Lighting_Utilisation_Factor=0.45,
        Lighting_Maintenance_Factor=0.9,
        U_em = 0.2 , 
        U_w = 1.1,
        ACH_vent=1.5,
        ACH_infl=0.5,
        ventilation_efficiency=0,
        c_m_A_f = 165000,
        theta_int_h_set = 20,
        theta_int_c_set = 26,
        phi_c_max_A_f=-12,
        phi_h_max_A_f=12,
        heatingSupplySystem=DirectHeater,
        coolingSupplySystem=DirectCooler,
        heatingEmissionSystem=AirConditioning,
        coolingEmissionSystem=AirConditioning,
        )

        Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)
        Office.solve_building_lighting(ill, occupancy)

        self.assertEqual(round(Office.phi_hc_nd_ac,2), -264.75)
        self.assertEqual(round(Office.coolingSysElectricity,2),264.75)
        self.assertEqual(round(Office.heatingSysElectricity,2),0)
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
        ill=44000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        #Set Building Parameters
        Office=Building(Fenst_A=13.5 ,
        Room_Depth=7 ,
        Room_Width=4.9 ,
        Room_Height=3.1 ,
        glass_solar_transmittance=0.687 ,
        glass_light_transmittance=0.744 ,
        lighting_load=11.7 ,
        lighting_control = 300,
        Lighting_Utilisation_Factor=0.45,
        Lighting_Maintenance_Factor=0.9,
        U_em = 0.2 , 
        U_w = 1.1,
        ACH_vent=1.5,
        ACH_infl=0.5,
        ventilation_efficiency=0,
        c_m_A_f = 165000,
        theta_int_h_set = 20,
        theta_int_c_set = 26,
        phi_c_max_A_f=-12,
        phi_h_max_A_f=12,
        heatingSupplySystem=DirectHeater,
        coolingSupplySystem=DirectCooler,
        heatingEmissionSystem=AirConditioning,
        coolingEmissionSystem=AirConditioning,
        )

        Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)
        Office.solve_building_lighting(ill, occupancy)

        self.assertEqual(round(Office.theta_m,2), 20.46)
        self.assertTrue(Office.has_heating_demand)
        self.assertEqual(round(Office.phi_hc_nd_ac,2), 328.09)
        self.assertEqual(round(Office.heatingSysElectricity,2),328.09)
        self.assertEqual(round(Office.coolingSysElectricity,2),0)
        self.assertEqual(Office.lighting_demand,0)

    def test_MaxCoolingRequired(self):
        theta_e=30
        theta_m_prev=25
        #Internal heat gains, in Watts
        phi_int=10

        #Solar heat gains after transmitting through the winow, in Watts
        phi_sol=5000

        #Illuminance after transmitting through the window 
        ill=44000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        #Set Building Parameters
        Office=Building(Fenst_A=13.5 ,
        Room_Depth=7 ,
        Room_Width=4.9 ,
        Room_Height=3.1 ,
        glass_solar_transmittance=0.687 ,
        glass_light_transmittance=0.744 ,
        lighting_load=11.7 ,
        lighting_control = 300,
        Lighting_Utilisation_Factor=0.45,
        Lighting_Maintenance_Factor=0.9,
        U_em = 0.2 , 
        U_w = 1.1,
        ACH_vent=1.5,
        ACH_infl=0.5,
        ventilation_efficiency=0,
        c_m_A_f = 165000,
        theta_int_h_set = 20,
        theta_int_c_set = 26,
        phi_c_max_A_f=-12,
        phi_h_max_A_f=12,
        heatingSupplySystem=DirectHeater,
        coolingSupplySystem=DirectCooler,
        heatingEmissionSystem=AirConditioning,
        coolingEmissionSystem=AirConditioning,
        )

        Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)
        Office.solve_building_lighting(ill, occupancy)

        self.assertEqual(round(Office.theta_m,2), 26.49)
        self.assertTrue(Office.has_cooling_demand)
        self.assertEqual(round(Office.phi_hc_nd_ac,2), -411.6)
        self.assertEqual(round(Office.coolingSysElectricity,2),411.6)
        self.assertEqual(round(Office.heatingSysElectricity,2),0)
        self.assertEqual(Office.lighting_demand,0)

    def test_MaxHeatingRequired(self):


        theta_e=5
        theta_m_prev=19
        #Internal heat gains, in Watts
        phi_int=10

        #Solar heat gains after transmitting through the winow, in Watts
        phi_sol=2000

        #Illuminance after transmitting through the window 
        ill=44000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        #Set Building Parameters
        Office=Building(Fenst_A=13.5 ,
        Room_Depth=7 ,
        Room_Width=4.9 ,
        Room_Height=3.1 ,
        glass_solar_transmittance=0.687 ,
        glass_light_transmittance=0.744 ,
        lighting_load=11.7 ,
        lighting_control = 300,
        Lighting_Utilisation_Factor=0.45,
        Lighting_Maintenance_Factor=0.9,
        U_em = 0.2 , 
        U_w = 1.1,
        ACH_vent=1.5,
        ACH_infl=0.5,
        ventilation_efficiency=0,
        c_m_A_f = 165000,
        theta_int_h_set = 20,
        theta_int_c_set = 26,
        phi_c_max_A_f=-12,
        phi_h_max_A_f=12,
        heatingSupplySystem=DirectHeater,
        coolingSupplySystem=DirectCooler,
        heatingEmissionSystem=AirConditioning,
        coolingEmissionSystem=AirConditioning,
        )

        Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)
        Office.solve_building_lighting(ill, occupancy)

        self.assertEqual(round(Office.theta_m,2), 19.39)
        self.assertTrue(Office.has_heating_demand)
        self.assertEqual(round(Office.phi_hc_nd_ac,2), 411.6)
        self.assertEqual(round(Office.heatingSysElectricity,2),411.6)
        self.assertEqual(round(Office.coolingSysElectricity,2),0)
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
        glass_solar_transmittance=0.687 ,
        glass_light_transmittance=0.744 ,
        lighting_load=11.7 ,
        lighting_control = 300,
        Lighting_Utilisation_Factor=0.45,
        Lighting_Maintenance_Factor=0.9,
        U_em = 0.2 , 
        U_w = 1.1,
        ACH_vent=1.5,
        ACH_infl=0.5,
        ventilation_efficiency=0,
        c_m_A_f = 165000,
        theta_int_h_set = 20.0,
        theta_int_c_set = 26.0,
        phi_c_max_A_f=-12.0,
        phi_h_max_A_f=12.0,
        heatingSupplySystem=DirectHeater,
        coolingSupplySystem=DirectCooler,
        heatingEmissionSystem=AirConditioning,
        coolingEmissionSystem=AirConditioning,
        )

        Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)
        Office.solve_building_lighting(ill, occupancy)

        self.assertEqual(round(Office.theta_m,2), 22.33)
        self.assertEqual(Office.phi_hc_nd_ac,0)
        self.assertEqual(round(Office.heatingSysElectricity,2),0)
        self.assertEqual(round(Office.coolingSysElectricity,2),0)
        self.assertEqual(round(Office.lighting_demand,2),401.31)

    
#     ###############################Tests with infiltration variation###############################

    def test_NoHVACNoLight_infl(self):
        theta_e=10
        theta_m_prev=22
        #Internal heat gains, in Watts
        phi_int=10

        #Solar heat gains after transmitting through the winow, in Watts
        phi_sol=2000

        #Illuminance after transmitting through the window 
        ill=44000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        #Set Building Parameters
        Office=Building(Fenst_A=13.5 ,
        Room_Depth=7 ,
        Room_Width=4.9 ,
        Room_Height=3.1 ,
        glass_solar_transmittance=0.687 ,
        glass_light_transmittance=0.744 ,
        lighting_load=11.7 ,
        lighting_control = 300,
        Lighting_Utilisation_Factor=0.45,
        Lighting_Maintenance_Factor=0.9,
        U_em = 0.2 , 
        U_w = 1.1,
        ACH_vent=1.5,
        ACH_infl=0.5,
        ventilation_efficiency=0.66,
        c_m_A_f = 165000,
        theta_int_h_set = 20,
        theta_int_c_set = 26,
        phi_c_max_A_f=-12,
        phi_h_max_A_f=12,
        heatingSupplySystem=DirectHeater,
        coolingSupplySystem=DirectCooler,
        heatingEmissionSystem=AirConditioning,
        coolingEmissionSystem=AirConditioning,
        )

        Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)
        Office.solve_building_lighting(ill, occupancy)

        self.assertEqual(round(Office.theta_m,2), 22.44)
        self.assertEqual(Office.phi_hc_nd_ac,0)
        self.assertEqual(round(Office.heatingSysElectricity,2),0)
        self.assertEqual(round(Office.coolingSysElectricity,2),0)
        self.assertEqual(Office.lighting_demand,0)

    def test_CoolingRequired_infl(self):
        theta_e=25
        theta_m_prev=24
        #Internal heat gains, in Watts
        phi_int=10

        #Solar heat gains after transmitting through the winow, in Watts
        phi_sol=4000

        #Illuminance after transmitting through the window 
        ill=44000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        #Set Building Parameters
        Office=Building(Fenst_A=13.5 ,
        Room_Depth=7 ,
        Room_Width=4.9 ,
        Room_Height=3.1 ,
        glass_solar_transmittance=0.687 ,
        glass_light_transmittance=0.744 ,
        lighting_load=11.7 ,
        lighting_control = 300,
        Lighting_Utilisation_Factor=0.45,
        Lighting_Maintenance_Factor=0.9,
        U_em = 0.2 , 
        U_w = 1.1,
        ACH_vent=1.5,
        ACH_infl=0.5,
        ventilation_efficiency=0.6,
        c_m_A_f = 165000,
        theta_int_h_set = 20,
        theta_int_c_set = 26,
        phi_c_max_A_f=-12,
        phi_h_max_A_f=12,
        heatingSupplySystem=DirectHeater,
        coolingSupplySystem=DirectCooler,
        heatingEmissionSystem=AirConditioning,
        coolingEmissionSystem=AirConditioning,
        )

        Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)
        Office.solve_building_lighting(ill, occupancy)

        self.assertEqual(round(Office.phi_hc_nd_ac,2), -296.65)
        self.assertEqual(round(Office.coolingSysElectricity,2),296.65)
        self.assertEqual(round(Office.heatingSysElectricity,2),0)
        self.assertEqual(round(Office.theta_m,2), 25.15)
        self.assertTrue(Office.has_cooling_demand)
        
        self.assertEqual(Office.lighting_demand,0)

    def test_HeatingRequired_infl(self):


        theta_e=10
        theta_m_prev=20
        #Internal heat gains, in Watts
        phi_int=10

        #Solar heat gains after transmitting through the winow, in Watts
        phi_sol=2000

        #Illuminance after transmitting through the window 
        ill=44000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        #Set Building Parameters
        Office=Building(Fenst_A=13.5 ,
        Room_Depth=7 ,
        Room_Width=4.9 ,
        Room_Height=3.1 ,
        glass_solar_transmittance=0.687 ,
        glass_light_transmittance=0.744 ,
        lighting_load=11.7 ,
        lighting_control = 300,
        Lighting_Utilisation_Factor=0.45,
        Lighting_Maintenance_Factor=0.9,
        U_em = 0.2 , 
        U_w = 1.1,
        ACH_vent=1.5,
        ACH_infl=0.5,
        ventilation_efficiency=0.6,
        c_m_A_f = 165000,
        theta_int_h_set = 20,
        theta_int_c_set = 26,
        phi_c_max_A_f=-12,
        phi_h_max_A_f=12,
        heatingSupplySystem=DirectHeater,
        coolingSupplySystem=DirectCooler,
        heatingEmissionSystem=AirConditioning,
        coolingEmissionSystem=AirConditioning,
        )

        Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)
        Office.solve_building_lighting(ill, occupancy)

        self.assertEqual(round(Office.theta_m,2), 20.46)
        self.assertTrue(Office.has_heating_demand)
        self.assertEqual(round(Office.phi_hc_nd_ac,2), 9.1)
        self.assertEqual(round(Office.heatingSysElectricity,2),9.1)
        self.assertEqual(round(Office.coolingSysElectricity,2),0)
        self.assertEqual(Office.lighting_demand,0)

    def test_MaxCoolingRequired_infl(self):
        theta_e=30
        theta_m_prev=25
        #Internal heat gains, in Watts
        phi_int=10

        #Solar heat gains after transmitting through the winow, in Watts
        phi_sol=5000

        #Illuminance after transmitting through the window 
        ill=44000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        #Set Building Parameters
        Office=Building(Fenst_A=13.5 ,
        Room_Depth=7 ,
        Room_Width=4.9 ,
        Room_Height=3.1 ,
        glass_solar_transmittance=0.687 ,
        glass_light_transmittance=0.744 ,
        lighting_load=11.7 ,
        lighting_control = 300,
        Lighting_Utilisation_Factor=0.45,
        Lighting_Maintenance_Factor=0.9,
        U_em = 0.2 , 
        U_w = 1.1,
        ACH_vent=1.5,
        ACH_infl=0.5,
        ventilation_efficiency=0.6,
        c_m_A_f = 165000,
        theta_int_h_set = 20,
        theta_int_c_set = 26,
        phi_c_max_A_f=-12,
        phi_h_max_A_f=12,
        heatingSupplySystem=DirectHeater,
        coolingSupplySystem=DirectCooler,
        heatingEmissionSystem=AirConditioning,
        coolingEmissionSystem=AirConditioning,
        )

        Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)
        Office.solve_building_lighting(ill, occupancy)

        self.assertEqual(round(Office.theta_m,2), 26.48)
        self.assertTrue(Office.has_cooling_demand)
        self.assertEqual(round(Office.phi_hc_nd_ac,2), -411.6)
        self.assertEqual(round(Office.coolingSysElectricity,2),411.6)
        self.assertEqual(round(Office.heatingSysElectricity,2),0)
        self.assertEqual(Office.lighting_demand,0)

    def test_MaxHeatingRequired_infl(self):


        theta_e=5
        theta_m_prev=19
        #Internal heat gains, in Watts
        phi_int=10

        #Solar heat gains after transmitting through the winow, in Watts
        phi_sol=2000

        #Illuminance after transmitting through the window 
        ill=44000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        #Set Building Parameters
        Office=Building(Fenst_A=13.5 ,
        Room_Depth=7 ,
        Room_Width=4.9 ,
        Room_Height=3.1 ,
        glass_solar_transmittance=0.687 ,
        glass_light_transmittance=0.744 ,
        lighting_load=11.7 ,
        lighting_control = 300,
        Lighting_Utilisation_Factor=0.45,
        Lighting_Maintenance_Factor=0.9,
        U_em = 0.2 , 
        U_w = 1.1,
        ACH_vent=1.5,
        ACH_infl=0.5,
        ventilation_efficiency=0.6,
        c_m_A_f = 165000,
        theta_int_h_set = 20,
        theta_int_c_set = 26,
        phi_c_max_A_f=-12,
        phi_h_max_A_f=12,
        heatingSupplySystem=DirectHeater,
        coolingSupplySystem=DirectCooler,
        heatingEmissionSystem=AirConditioning,
        coolingEmissionSystem=AirConditioning,
        )

        Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)
        Office.solve_building_lighting(ill, occupancy)

        self.assertEqual(round(Office.theta_m,2), 19.51)
        self.assertTrue(Office.has_heating_demand)
        self.assertEqual(round(Office.phi_hc_nd_ac,2), 411.6)
        self.assertEqual(round(Office.coolingSysElectricity,2),0)
        self.assertEqual(round(Office.heatingSysElectricity,2),411.6)
        self.assertEqual(Office.lighting_demand,0)

    def test_lightingrequired_infl(self):

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
        glass_solar_transmittance=0.687 ,
        glass_light_transmittance=0.744 ,
        lighting_load=11.7 ,
        lighting_control = 300,
        Lighting_Utilisation_Factor=0.45,
        Lighting_Maintenance_Factor=0.9,
        U_em = 0.2 , 
        U_w = 1.1,
        ACH_vent=1.5,
        ACH_infl=0.5,
        ventilation_efficiency=0.6,
        c_m_A_f = 165000,
        theta_int_h_set = 20.0,
        theta_int_c_set = 26.0,
        phi_c_max_A_f=-12.0,
        phi_h_max_A_f=12.0,
        heatingSupplySystem=DirectHeater,
        coolingSupplySystem=DirectCooler,
        heatingEmissionSystem=AirConditioning,
        coolingEmissionSystem=AirConditioning,
        )

        Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)
        Office.solve_building_lighting(ill, occupancy)

        self.assertEqual(round(Office.theta_m,2), 22.43)
        self.assertEqual(Office.phi_hc_nd_ac,0)
        self.assertEqual(round(Office.coolingSysElectricity,2),0)
        self.assertEqual(round(Office.heatingSysElectricity,2),0)
        self.assertEqual(round(Office.lighting_demand,2),401.31)

    def test_lightingrequired_probabiltyOff(self):

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

        probLighting=0.01

        #Set Building Parameters
        Office=Building(Fenst_A=13.5 ,
        Room_Depth=7 ,
        Room_Width=4.9 ,
        Room_Height=3.1 ,
        glass_solar_transmittance=0.687 ,
        glass_light_transmittance=0.744 ,
        lighting_load=11.7 ,
        lighting_control = 300,
        Lighting_Utilisation_Factor=0.45,
        Lighting_Maintenance_Factor=0.9,
        U_em = 0.2 , 
        U_w = 1.1,
        ACH_vent=1.5,
        ACH_infl=0.5,
        ventilation_efficiency=0.6,
        c_m_A_f = 165000,
        theta_int_h_set = 20.0,
        theta_int_c_set = 26.0,
        phi_c_max_A_f=-12.0,
        phi_h_max_A_f=12.0,
        heatingSupplySystem=DirectHeater,
        coolingSupplySystem=DirectCooler,
        heatingEmissionSystem=AirConditioning,
        coolingEmissionSystem=AirConditioning,
        )

        Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)
        Office.solve_building_lighting(ill, occupancy, probLighting)

        self.assertEqual(round(Office.theta_m,2), 22.43)
        self.assertEqual(Office.phi_hc_nd_ac,0)
        self.assertEqual(round(Office.coolingSysElectricity,2),0)
        self.assertEqual(round(Office.heatingSysElectricity,2),0)
        self.assertEqual(round(Office.lighting_demand,2),0)

    
# ############################ System Variations ########################



if __name__ == '__main__':
    unittest.main()


