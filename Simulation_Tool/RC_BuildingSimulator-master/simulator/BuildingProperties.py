

"""
===========================
RC Model of a single zone building
===========================
File history and credits:
Prageeth Jayathissa
Mario Frei
Jeremias Schmidli
Amr Elesawy 
"""

class Building(object):
	'''Sets the parameters of the building. Default arguments are:
	Building(Fenst_A=13.5 , Room_Depth=7 , Room_Width=4.9 ,Room_Height=3.1 ,glass_solar_transmitance=0.687 ,
	glass_light_transmitance=0.744 ,LightLoad=0.0117 , LightingControl = 300,Cm=2.07, R_env=42, Infl=0.5, vent_Pp=0.016) '''

	def __init__(self, 
		Fenst_A=13.5 ,
		Room_Depth=7 ,
		Room_Width=4.9 ,
		Room_Height=3.1 ,
		glass_solar_transmitance=0.687 ,
		glass_light_transmitance=0.744 ,
		LightLoad=0.0117 ,
		LightingControl = 300,
		Cm=2.07,
		R_env=42,
		Infl=0.5,
		vent_Pp=0.016,
		):

		#Building Dimensions
		self.Fenst_A=Fenst_A #[m2] Window Area
		self.Room_Depth=Room_Depth #[m] Room Depth
		self.Room_Width=Room_Width #[m] Room Width
		self.Room_Height=Room_Height #[m] Room Height

		#Fenstration and Lighting Properties
		self.glass_solar_transmitance=glass_solar_transmitance #Dbl LoE (e=0.2) Clr 3mm/13mm Air
		self.glass_light_transmitance=glass_light_transmitance #Dbl LoE (e=0.2) Clr 3mm/13mm Air
		self.LightLoad=LightLoad #[kW/m2] lighting load
		self.LightingControl = LightingControl #[lux] Lighting setpoint

		#Calculated Propoerties
		self.Floor_A=Room_Depth*Room_Width #[m2] Floor Area
		self.Room_Vol=Room_Width*Room_Depth*Room_Height #[m3] Room Volume

		#Single Capacitance Model Parameters
		self.Cm=Cm #[kWh/K] Room Capacitance. Default based of Madsen2011
		self.R_env=R_env #[K/kW] Wall resistance to outside air. Default based off glass having a Uvalue of 1.978W/m2K, 12m2 facade glass

		#Infiltration 
		self.Infl=Infl # [ACH/hr] Air Changes per hour
		InflHeatTransfer=Infl*self.Room_Vol*1.2*1/3600 #[kW/K]
		self.R_infl=1.0/InflHeatTransfer # [K/kW]Resistance due to infiltration

		#Initialise ventilation set point
		self.vent_Pp=vent_Pp #[m3/s/person] ventilation rate requirements per person


	def setVentilation(self, people):
		self.vent=self.vent_Pp*people*self.Floor_A #[m3/s]
		heatTransfer=self.vent*1.2*1 #[kW/K] energy loss due to ventilation
		self.R_vent=1/heatTransfer #[K/kW] Resistance due to ventlation

		#Combine resistors in parallel 
		self.R_i=1.0/((1.0/self.R_env) + (1.0/self.R_infl) + (1.0/self.R_vent))



# HPZ=Building()

# print HPZ.Floor_A






