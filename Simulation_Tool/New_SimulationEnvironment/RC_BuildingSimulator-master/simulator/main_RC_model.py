

"""
===========================
RC Model of a single zone building
===========================
File history and credits:
Prageeth Jayathissa
Mario Frei
Jeremias Schmidli
Amr Elesawy 


possible input parameters:
- location (epw_name)
- building stystem: capacitive heating/ cooling
- occupancy profil: type of building utilisation (Office)




"""
    
def main_RC_model (epw_name, myfilename1, myfilename2):
    
    import sys
    import numpy as np
    import math
    import input_data_mauro as f
    import matplotlib.pyplot as plt
    import PID_controller
    from BuildingProperties import Building #Importing Building Class
    
    sys.path.insert(0, 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\RC_BuildingSimulator-master\simulator\data')                                        
                      

    
    #Import Data
    T_out,glbRad, glbIll= f.read_EWP(epw_name) #C, W, lx
    
    #heat gain from the sun
    Q_fenstRad=f.read_transmittedR(myfilename1) #kWh/h
    
    #occupancy profil of the building
    occupancy, Q_human=f.read_occupancy(myfilename2) #people/m2/h, kWh/h
    Ill_Eq= f.Equate_Ill(epw_name) #Equation coefficients for linear polynomial
    
    
    #Set Office Building Parameters. See BuildingProperties.py
    Office=Building(Cm=2.07, R_env=42, Infl=0.5, vent_Pp=0.016)
    
    
    #Calculate Illuminance in the room. 
    fenstIll=Q_fenstRad*1000*Ill_Eq[0] #Lumens.  Note that the constant has been ignored because it should be 0
    TransIll=fenstIll*Office.glass_light_transmitance
    Lux=TransIll/Office.Floor_A
    
    #Other Set Points
    tintH_set=20.0
    tintC_set=26.0 #Because data in occupancy is a bit wierd and will causes control issues FIX THIS
    
    
    #Calculate external heat gains
    Q_fenstRad=Q_fenstRad*Office.glass_solar_transmitance #Solar Gains from ladybug analysis
    
    
    Q=Q_fenstRad.add(Q_human, axis=0) #only solar gains and human gains for now
    
    
    
    #Initialise Conditions
    Q_heat=0
    Q_cool=0
    Total_Heating=0
    Total_Cooling=0
    Total_Lighting=0
    T_in=20 #Starting internal temperature
    Data_T_in=[] 
    Data_Heating=np.empty([8760])
    Data_Cooling=np.empty([8760])
    Data_Lighting=np.empty([8760])
    Data_uncomfortHours=np.zeros([8760])
    uncomfortHours=0
    
    #PID setup
    heatingControl=PID_controller.PID(P=1.0, I=0.08, D=0.0, Derivator=0, Integrator=0, Integrator_max=5, Integrator_min=-5)
    coolingControl=PID_controller.PID(P=2.0, I=1.0, D=0.0, Derivator=0, Integrator=0, Integrator_max=5, Integrator_min=-5)
    heatingControl.setPoint(tintH_set)
    coolingControl.setPoint(tintC_set)
    
    #Differential Equation Parameters
    dt=0.25 #hours
    
    for ii in range(0, int(8760)): #evaluate needed range
    	#Initialise hourly energy requirements
    	Heat_hr=0
    	Cool_hr=0
    	Lighting_hr=0
    	Office.setVentilation(occupancy['People'][ii])
    
    
    	for jj in range(0,int(1/dt)):
    
    			
    
    		dT_in=((Q.iat[ii,0]+Q_heat+Q_cool)/(Office.Cm) + (1/(Office.Cm*Office.R_i))*(float(T_out[ii])-T_in))*dt
    		T_in=T_in+dT_in
    		if T_in<tintH_set and occupancy['People'].iat[ii]>=0: 
    			#Note that occupancy control is currently disabled. This is done through the >=. If you want occupancy
    			#control then set it to >
    			 		
    
    			Q_heat= heatingControl.update(T_in)+1.5 #1.5 is a V_o correction factor to maintain 20C
    		else:
    			Q_heat=0
    		Heat_hr+=Q_heat #Determine total heat in kW for this time step. This will be averaged later
    
    
    
    		if  T_in>tintC_set and occupancy['People'].iat[ii]>=0:
    			#Note that occupancy control is currently disabled. This is done through the >=. If you want occupancy
    			#control then set it to >
    					
    			Q_cool = coolingControl.update(T_in)
    		else:
    			Q_cool=0
    		Cool_hr+=Q_cool #Determine total cooling power in KW. This will be averaged later
    
    	#Average the kW by the timestep to determine the kWh for the timestep
    	Heat_hr=Heat_hr*dt
    	Cool_hr=Cool_hr*dt
    
    	#Sum up all the timesteps
    	Total_Heating+=Heat_hr
    	Total_Cooling+=Cool_hr
    
    
    	#Check for Hours outside the setpoint +/- 1
    	if T_in>tintC_set+1 or T_in<tintH_set-1:
    		if occupancy['People'].iat[ii]>0:
    			uncomfortHours+=1 #Number of uncomfortable hours
    			Data_uncomfortHours[ii]=1 #array to show which hours were uncomfortable
    
    
    
    	#Lighting calc. Double check this as I wrote it rushed. Try find allternative for .iat
    	if Lux.get_value(ii,0)< Office.LightingControl and occupancy['People'].iat[ii]>0:
    		Lighting_hr=Office.LightLoad*Office.Floor_A
    		Total_Lighting+=Lighting_hr
    
    
    
    	Data_T_in.append(T_in)
    	Data_Heating[ii]=Heat_hr
    	Data_Cooling[ii]=abs(Cool_hr)
    	Data_Lighting[ii]=Lighting_hr
    
#    print 'Total Heating Load is:', Total_Heating, 'kWh'
#    print 'Total Cooling Load is:', Total_Cooling*-1, 'kWh'
#    print 'Total Lighting Load is:', Total_Lighting, 'kWh'
#    print 'Total Uncomfortable Hours are', uncomfortHours,' hours'
    #Heating is good
    #Cooling is about 1000kWh lower than Diva, but the same as design builder
    #Lighting is 150kWh lower than design builder and DIVA
    #		heating 	Cooling 	Lighting
    #Diva 	1224		4337		427
    #Db 	1386		2990		497
    
    pltrange=8760
    
    plt.figure(1)
    plt.plot(range(0, int(pltrange)),Data_T_in[0:pltrange], range(0, int(pltrange)),T_out[0:pltrange])
     
    plt.figure(2)
    plt.plot(range(0, int(pltrange)),Data_Heating[0:pltrange])
    
    plt.figure(3)
    plt.plot(range(0, int(pltrange)),Data_Lighting[0:pltrange])
    
    plt.figure(4)
    plt.plot(range(0, int(pltrange)),Data_Cooling[0:pltrange])
    
    plt.show()
    
    return Data_T_in, Data_Heating, Data_Cooling, Data_Lighting, Q_fenstRad