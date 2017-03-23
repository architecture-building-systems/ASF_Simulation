##5R1C Building Simulation Model

* `buildingPhysics.py`: Is the RC model class
* `buildingSystem.py`: Is a builder pattern class to define the building system (Work in Progress)
* `example.py` : Is an example showing the implentation of the RC model for one timestep
* `test.py` : Is the unittest file for the software. Run this before each commit and after each pull


The equations presented here is this code are derived from ISO 13790 Annex C, Methods are listed in order of apperance in the Annex 

###HOW TO USE
```python
from buildingPhysics import Building #Importing Building Class
Office=Building() #Set an instance of the class
Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev) #Solve for Heating
Office.solve_building_lighting(ill, occupancy) #Solve for Lighting
```


###VARIABLE DEFINITION

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


	
###INPUT PARAMETER DEFINITION 

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

###CLASS ATTRIBUTES	

	self.theta_m : Room medium temperature
	self.theta_air : Room air temperature
	self.theta_s : Room internal surface temperature
	self.phi_hc_ac: Room heating/cooling load. Negative if cooling, positive if heating
	self.phi_hc_nd_ac: Unrestricuted heating/coolign load. Negative if cooling, positive if heating
	self.heatingElectricity: Electricty consumption through heating. Dependent on the building system (in progress)
	self.coolingElectricity: Electricty consumption through cooling. Dependent on the building system (in progress)
	self.lighting_demand: Lighting demand of the building
	self.has_heating_demand : Boolean if heating is required
	self.has_cooling_demand : Boolean if cooling is required


	self.heatingSystem
	self.coolingSystem
	self.heatiningEfficiency
	self.coolingEfficiency

There are other attributes that are not very important, and can be found within buildingPhysics.py. Post an issue if you have any questions



