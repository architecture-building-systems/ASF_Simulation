# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:14:42 2016

main file for simulation environment

@author: Prageeth Jayathissa
@credits: Jerimias Schmidli

24.10.2016

monthly Simulation - main_new_mauro_5.gh
new RC-Model advanced

"""

import os, sys
import numpy as np
import json
import time
import warnings
import csv
import matplotlib.pyplot as plt
import csv
import pandas as pd


# get current time
now = time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
print "simulation start: " + now



# specify the location used for the analysis ‐ this name must be the same as a
# folder in the directory .../ASF_Simulation/Simulation_Environment/data/geographica
# new locations can be added with the grasshopper main script for any .epw weather
geoLocation = 'Zuerich_Kloten_2005'

NoClusters = 1



#Option to integrate the actuation energy consumption, 'yes' = energy consumption is included
#Actuation = True # False

#set builiding parameters, will be used, when calling the RC_model function
#location = (epw_name)
#building_stystem = capacitive heating/ cooling
#occupancy_profil = type of building utilisation (Office)


## Hier könnte man HOY definieren für die Berechnung:  simulationOption = {'timePeriod' : HOY}          
#simulationOption = {'timePeriod' : '1h'}
simulationOption = {'timePeriod' : None}

#PV production plots
createPlots = False


# create dictionary to write all paths:
paths = {}

# find path of current folder (simulation_environment)
paths['main'] = os.path.abspath(os.path.dirname(sys.argv[0]))

# define paths of subfolders:
paths['data'] = paths['main'] + '\\data'
paths['python'] = paths['main'] + '\\python'
paths['radiation_results'] = paths['main'] + '\\radiation_results'
paths['radiation_wall'] = paths['main'] + '\\radiation_wall'
paths['PV'] = paths['main'] + '\\PV_results'


# define path of weather file:
paths['weather'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\WeatherData\Zuerich-Kloten_2005.epw' #paths['epw_name']

# add python_path to system path, so that all files are available:
sys.path.insert(0, paths['python'] + '\\aux_files')
sys.path.insert(0, paths['python'])

from epwreader import epw_reader
#read epw file of needed destination
weatherData = epw_reader(paths['weather'])


#radiation subfolder is created, there the radiation_results are saved
if not os.path.isdir(paths['radiation_results']):
        os.makedirs(paths['radiation_results'])

if not os.path.isdir(paths['radiation_wall']):
        os.makedirs(paths['radiation_wall'])


# define path of geographical location:
paths['geo'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\data\geographical_location\Zuerich-Kloten' 
#paths['geo'] = os.path.join(( paths['data'] + "\geographical_location"), geoLocation)


# create sun data based on grasshopper file, this is only possible with the ladybug component SunPath
#execfile(paths['python'] + "\\aux_files\\SunAngles_Tracking_and_temperature.py")

# calculate and save lookup table if it does not yet exist:
if not os.path.isfile(paths['data'] + '\python\electrical_simulation\curr_model_submod_lookup.npy'): 
    if not os.path.isdir(paths['data'] + '\python\electrical_simulation'):
        os.makedirs(paths['data'] + '\python\electrical_simulation')
    execfile(paths['python'] + '\\aux_files\\create_lookup_table.py')
else:
    print 'lookup table not created as it already exists'


# load sunTrackingData used for the LadyBug simulation:
with open(paths['geo'] + '\SunTrackingData.json', 'r') as fp:
    SunTrackingData = json.load(fp)
    fp.close()


#Set Solar Panel Properties
XANGLES=[0]
YANGLES= [-45,0,45]

#XANGLES=[22.5,67.5]
#YANGLES= [-22.5,22.5]


#Make a list of all angle combinations
ANGLES= [(x, y) for x in XANGLES for y in YANGLES]

#create a dicitionary with all angle combinations
combinationAngles = {}

for i in range(0,len(ANGLES)):
    combinationAngles[i] = ANGLES[i]

NumberCombinations = len(XANGLES)*len(YANGLES) #*NoClusters   



#Set panel data
panel_data={"XANGLES": XANGLES ,
"YANGLES" : YANGLES,
"NoClusters":NoClusters,
"numberHorizontal":6,
"numberVertical":9,
"panelOffset":400,
"panelSize":400,
"panelSpacing":500,
}

#Set Building Parameters
building_data={"room_width":4900,     
"room_height":3100,
"room_depth":7000,
"glazing_percentage_w":0.92,
"glazing_percentage_h":0.97,
}


#Save parameters to be imported into grasshopper
with open('panel.json','w') as f:
    f.write(json.dumps(panel_data))

with open('building.json','w') as f:
    f.write(json.dumps(building_data))


resultsdetected=0

print '\nStart radiation calculation with ladybug'


# create dicitionary to save optimal angles:
opt_angles = {}
BuildingRadiationData_HOD = {}

daysPerMonth = np.array([31,28,31,30,31,30,31,31,30,31,30,31])

#hour_in_month is dependent on the location, this dict is for ZH
#load hour_in_month = SunTrackingData['HoursInMonth']
hour_in_month = {1:[8, 9, 10, 11, 12, 13, 14, 15],
                 2:[7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
                 3:[6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                 4:[5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
                 5:[4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
                 6:[4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
                 7:[4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
                 8:[5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
                 9:[6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
                 10:[6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
                 11:[7, 8, 9, 10, 11, 12, 13, 14, 15],
                 12:[8, 9, 10, 11, 12, 13, 14, 15]}


#maxcomb = NumberCombinations**panel_data['NoClusters']
#
#from NoClusters_mauro import NoClusters_mauro
#
#ASFangles = NoClusters_mauro(XANGLES = XANGLES, YANGLES = YANGLES, NoClusters = panel_data['NoClusters'], paths = paths['radiation_results'] )
#
#for index in range(maxcomb):
#       
#    print "Index", index
#    print ASFangles[index]
#
#months
start = 1
end = 2


for monthi in range(1,13): #month:
    
    BuildingRadiationData_HOD[monthi] = {}
    
    for HOD in hour_in_month[monthi]:
    #check if there is any radiation to analyse
        print 'HOD:', HOD, 'Month:', monthi
    
        BuildingRadiationData = np.array([])
        
        for x_angle in XANGLES:
            for y_angle in YANGLES:
                
                comb_data={"x_angle":x_angle,
                           "y_angle":y_angle,
                           "HOD":HOD,
                           "Month":monthi
                           }
                           
                #create json file with the set combination of x-angle,y-angle and HOY
                with open('comb.json','w') as f:
                    f.write(json.dumps(comb_data))
                    print HOD, monthi, x_angle, y_angle, resultsdetected              
                
#                #write ASFangles for Clusters
#                with open('outputASFangles.json','w') as f:
#                    f.write(json.dumps(ASFangles[index]))
#                    print "index:", index
#                      
                    
                #Wait until the radiation_results were created    
                while not os.path.exists(paths['radiation_results']+'\\RadiationResults' +'_'+  str(HOD) + '_' + str(monthi)  + '_' + str(x_angle) + '_' + str(y_angle)+ '.csv'):
                    time.sleep(1)
                
                #paths['radiation_results']+'\\RadiationResults' +'_Index_'+ str(index) + '_NoCluster_' + str(NoClusters) + '_'  + str(HOD) + '_' + str(monthi)  + '_' + str(x_angle) + '_' + str(y_angle)+ '.csv'                
                
                else:
                    print 'next step'
                    resultsdetected += 1
                                            
                    #read total radition on wall and save it in BuildingRadiationData              
                    while not os.path.exists(paths['radiation_wall'] + '\RadiationWall' + '_' + str(HOD) +'_'+ str(monthi) + '_'+ str(x_angle) + '_' + str(y_angle) + '.csv'):
                        time.sleep(1)
                    else:
                        with open(paths['radiation_wall'] + '\RadiationWall' + '_' + str(HOD) +'_'+ str(monthi) + '_'+ str(x_angle) + '_' + str(y_angle) + '.csv', 'r') as csvfile:
                            reader = csv.reader(csvfile)
                            for idx,line in enumerate(reader):
                                if idx == 1:
                                    BuildingRadiationData = np.append(BuildingRadiationData, [float(line[0])])
                                    break
                        
                                           
        
        for jj in range(0,daysPerMonth[monthi-1]):
            #Radiation data is calculated for all days per month, so the data is divided through the amount of days per month
            BuildingRadiationData_HOD[monthi][HOD+24*jj]= BuildingRadiationData * 1/daysPerMonth[monthi-1]

"""        
print 'radiation calculation finished!'

PV_electricity_results = {}
PV_detailed_results = {}

#with the radiation_results the Pv_results are calcualted
#if not os.path.isfile(paths['PV'] + '\PV_electricity_results.npy'): 
if not os.path.isdir(paths['PV']):
    os.makedirs(paths['PV'])
from asf_electricity_production_mauro_3 import asf_electricity_production
print '\ncalculating PV electricity production'     


if createPlots:
    PV_electricity_results, PV_detailed_results, fig1, fig2 = \
    asf_electricity_production(
                       createPlots = createPlots, 
                       lb_radiation_path = paths['radiation_results'],
                       panelsize = 400, 
                       pvSizeOption = 0,
                       save_results_path = paths['PV'], 
                       lookup_table_path = paths['data'] + '\python\electrical_simulation', 
                       geo_path = paths['geo'],
                       flipOrientation= False, 
                       simulationOption = {'timePeriod' : None},
                       XANGLES = XANGLES, YANGLES= YANGLES, hour_in_month = hour_in_month, 
                       start = start, end = end)
                       
else:
    PV_electricity_results, PV_detailed_results = \
    asf_electricity_production(
                       createPlots = createPlots, 
                       lb_radiation_path = paths['radiation_results'],
                       panelsize = 400, 
                       pvSizeOption = 0,
                       save_results_path = paths['PV'], 
                       lookup_table_path = paths['data'] + '\python\electrical_simulation', 
                       geo_path = paths['geo'],
                       flipOrientation= False, 
                       simulationOption = {'timePeriod' :None},
                       XANGLES = XANGLES, YANGLES= YANGLES, hour_in_month = hour_in_month,
                       start = start, end = end)

#else: 
#    PV_electricity_results = np.load(paths['PV'] + '\PV_electricity_results.npy').item()
#    PV_detailed_results = np.load(paths['PV'] + '\PV_detailed_results.npy').item()
#    print 'PV_electricity_results loaded from folder'
    
print "\npreparing data\n"
"""

#Temperature value, to start the simulation with
T_in = 20


#create dicitionary to save relevant hourly data:
hourlyData = {}
Data_HC_HOY = {}

Data_Lighting_HOY = {}
Data_T_in_HOY = {}
results_building_simulation = {}
E_tot = {}
PV={}


ii= 0

from hourRadiation import hourRadiation, hourRadiation_calculated, sumHours

hourRadiation = hourRadiation(hour_in_month, daysPerMonth)
hourRadiation_calculated = hourRadiation_calculated(hour_in_month,daysPerMonth)
sumHours = sumHours(daysPerMonth)


#if not os.path.isfile(paths['main'] + '\\Results' + '\\Building_Simulation.npy'): 
        
#add the radiation data to the specific HOY
BuildingRadiationData_HOY= {}
passedHours = 0

for monthi in range(1,13):
    if monthi == 1:
        passedHours = 0
    else:
        passedHours = sumHours[monthi-2]     
    
    for HOD in hour_in_month[monthi]:
        for ii in range(0,daysPerMonth[monthi-1]):             
            DAY = ii*24 + HOD   
            BuildingRadiationData_HOY[passedHours + DAY] = BuildingRadiationData_HOD[monthi][DAY]


for hour_of_year in range(0,8760):
    PV[hour_of_year]= {}
    PV[hour_of_year]['PV']= []    

count = 0
DAY = 0
#for jj in range(1,len(PV_electricity_results['Pmpp_sum'])):
"""
for monthi in range(1,13):
    if monthi == 1:
        passedHours = 0
    else:
        passedHours = sumHours[monthi-2]
        
    for HOD in hour_in_month[monthi]:
            for jj in range(0,daysPerMonth[monthi-1]):
                DAY = HOD + jj*24    
                PV[passedHours + DAY]['PV'] = 0.001 * PV_electricity_results['Pmpp_sum'][count:count+NumberCombinations]
            count +=NumberCombinations
"""       


print '\nStart RC-Model calculation'
print '\nTime: ' + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())

# add python_path to system path, so that all files are available:
sys.path.insert(0, r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\5R1C_ISO_simulator')
                                
#    # calcualte Building Simulation (RC Model) and save H,C,L for every our of the year                              
#    from main_RC_model3 import main_RC_model

   
paths['Radiation_Building'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RC_BuildingSimulator-master\simulator\data' + '\\adiation_Building_Zh.csv'
paths['Occupancy'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RC_BuildingSimulator-master\simulator\data' + '\\Occupancy_COM.csv' 

#set parameters
human_heat_emission=0.12 #[kWh] heat emitted by a human body per hour. Source: HVAC Engineers Handbook, F. Porges
floor_area=30 #[m^2] floor area

from read_occupancy import read_occupancy, Equate_Ill
    
#people/m2/h, W    
occupancy, Q_human = read_occupancy(myfilename = paths['Occupancy'], human_heat_emission = human_heat_emission, floor_area = floor_area)
#Equation coefficients for linear polynomial
Ill_Eq = Equate_Ill(weatherData = weatherData)
   
    
from buildingPhysics import Building #Importing Building Class


for hour_of_year in range(0,8760):#range(0,8760):
    
    print "HOY", hour_of_year
    Data = {}
    E_tot[hour_of_year] = {}
    Data_HC_HOY[hour_of_year] = {}
    Data_Lighting_HOY[hour_of_year] =  {}   
    Data_T_in_HOY[hour_of_year] = {}
    
    results_building_simulation[hour_of_year] = {}
    hourlyData[hour_of_year]= {}
    hourlyData[hour_of_year]['H'] = []
    hourlyData[hour_of_year]['C'] = []
    hourlyData[hour_of_year]['L'] = []       
    hourlyData[hour_of_year]['E_tot'] = []
    hourlyData[hour_of_year]['T_out'] = []
    hourlyData[hour_of_year]['T_in'] = []
    hourlyData[hour_of_year]['AngleComb'] = []
    hourlyData[hour_of_year]['HC'] = []

    if hour_of_year not in hourRadiation:
        BuildingRadiationData_HOY[hour_of_year] = [0]* NumberCombinations
        hourlyData[hour_of_year]['PV'] = [0]* NumberCombinations
    else:
        hourlyData[hour_of_year]['PV'] = PV[hour_of_year]['PV']
                 

    """
    use of the new RC-Model
    """
    
    
 
   
    #theta_m_prev: Medium temperature from the previous time step
    #theta_e: External air temperature
    
#    theta_e=10
#    theta_m_prev=22
    
#    #Internal heat gains, in Watts
#    phi_int=10
    
#    #Solar heat gains after transmitting through the winow, in Watts
#    phi_sol=2000
    
    #BuildingRadiationData_HOY[hour_of_year][comb] in kWh/h, multiply with 1000 to get Watts
     
    #Set Building Parameters
    Office=Building(phi_c_max_A_f=-np.inf,
                    phi_h_max_A_f=np.inf)
    
    #check all angle combinations and determine, which combination results in the smallest energy demand (min(E_tot))
    for comb in range(0, NumberCombinations):
        
        print "Q_human", Q_human[hour_of_year]
        print "Rad", BuildingRadiationData_HOY[hour_of_year][comb]*1000
        print "Temp", weatherData['drybulb_C'][hour_of_year]
        
        
        Office.solve_building_energy(phi_int = Q_human[hour_of_year], 
                                     phi_sol = BuildingRadiationData_HOY[hour_of_year][comb]*1000,
                                     theta_e = weatherData['drybulb_C'][hour_of_year], 
                                     theta_m_prev = T_in)
    
            
        #Calculate Illuminance in the room. 
        fenstIll=BuildingRadiationData_HOY[hour_of_year][comb]*1000*Ill_Eq[0] #Lumens.  Note that the constant has been ignored because it should be 0
        #Illuminance after transmitting through the window         
        TransIll=fenstIll*Office.glass_light_transmitance
        
       
        Office.solve_building_lighting(ill = TransIll, 
                                       occupancy = occupancy['People'][hour_of_year])

        print "Office.lightning_demand", Office.lighting_demand
        print "Office.phi_hc_nd_ac", Office.phi_hc_nd_ac
        print "T_in", Office.theta_m

        Data_Lighting_HOY[hour_of_year][comb] = Office.lighting_demand
        Data_HC_HOY[hour_of_year][comb] = Office.phi_hc_nd_ac #achtung heating und cooling 
        Data_T_in_HOY[hour_of_year][comb] = Office.theta_m
        
    T_in = Office.theta_m #most efficient solution has to be used again
    hourlyData[hour_of_year]['T_out'] = weatherData['drybulb_C'][hour_of_year]
    hourlyData[hour_of_year]['HC'] = Data_HC_HOY[hour_of_year]    




data_df = pd.DataFrame(Data_HC_HOY).T
   
fig = plt.figure()   
with pd.plot_params.use('x_compat', True):
     data_df[0].plot(color='y')
    
plt.legend(loc='best')
plt.xlabel('Hour of the year', fontsize=18)
plt.ylabel('HC [kW/m2]', fontsize=16)    
    



"""

                                      
    
    #check all angle combinations and determine, which combination results in the smallest energy demand (min(E_tot))
    for comb in range(0, NumberCombinations):
        
        #set occupancy profil of the building
        Data_T_in, T_out, Data_Heating, Data_Cooling, Data_Lighting = main_RC_model(hour_of_year, T_in, BuildingRadiationData_HOY[hour_of_year][comb],paths['weather'],paths['Radiation_Building'],paths['Occupancy'])
        
        #save all combination results for one HOY
        Data_Heating_HOY[hour_of_year][comb]= Data_Heating
        Data_Cooling_HOY[hour_of_year][comb] = Data_Cooling
        Data_Lighting_HOY[hour_of_year][comb] = Data_Lighting       
        Data_T_in_HOY[hour_of_year][comb] = Data_T_in[0]
 
        #determine best combination for the evaluated HOY
        #integrate the needed actuation energy to calculate the real total energy demand 
        E_tot[hour_of_year][comb]=  Data_Heating_HOY[hour_of_year][comb] + Data_Cooling_HOY[hour_of_year][comb] + Data_Lighting_HOY[hour_of_year][comb] - hourlyData[hour_of_year]['PV'][comb]      
      
    hourlyData[hour_of_year]['H'] = Data_Heating_HOY[hour_of_year]
    hourlyData[hour_of_year]['C'] = Data_Cooling_HOY[hour_of_year]
    hourlyData[hour_of_year]['L'] = Data_Lighting_HOY[hour_of_year]       
    hourlyData[hour_of_year]['E_tot'] = E_tot[hour_of_year]
    hourlyData[hour_of_year]['T_out'] =T_out
    hourlyData[hour_of_year]['T_in'] = Data_T_in_HOY[hour_of_year]
    hourlyData[hour_of_year]['AngleComb'] = combinationAngles
    hourlyData[hour_of_year]['RadiationWindow'] = BuildingRadiationData_HOY[hour_of_year]
    
    if hour_of_year == 0:
    #initil condition        
        BestComb = 0
    
    if hourlyData[hour_of_year]['PV'][0] != 0:
        #get key with min value from the E_tot dictionary
        BestComb = min(E_tot[hour_of_year], key=lambda comb: E_tot[hour_of_year][comb])
    elif hourlyData[hour_of_year]['PV'][0] == 0 and hour_of_year != 0:
        #Check if there is no PV-value (nor radiation), then don't move the modules
        BestComb = BestComb
  
  
    #save optimal results in a dictionary and convert to a DataFrame   
    results_building_simulation[hour_of_year]['E_tot'] = hourlyData[hour_of_year]['E_tot'][BestComb]
    results_building_simulation[hour_of_year]['H']  = hourlyData[hour_of_year]['H'][BestComb]
    results_building_simulation[hour_of_year]['C']  = hourlyData[hour_of_year]['C'][BestComb]
    results_building_simulation[hour_of_year]['L']  = hourlyData[hour_of_year]['L'][BestComb]
    results_building_simulation[hour_of_year]['PV']  = hourlyData[hour_of_year]['PV'][BestComb]
    results_building_simulation[hour_of_year]['OptAngles'] = combinationAngles[BestComb]   
    results_building_simulation[hour_of_year]['T_in'] = Data_T_in_HOY[hour_of_year][BestComb]
    results_building_simulation[hour_of_year]['T_out'] = hourlyData[hour_of_year]['T_out']
    results_building_simulation[hour_of_year]['RadiationWindow'] = BuildingRadiationData_HOY[hour_of_year][BestComb]
    
    
    T_in = Data_T_in_HOY[hour_of_year][comb]
    
    #show which HOY is calculated
    if hour_of_year % 1000 == 0:
        print 'HOY:', hour_of_year    
    

#store all results in a DataFrame
hourlyData_df = pd.DataFrame(hourlyData)

#store results of the best angle combinations in DataFrame   
Building_Simulation_df= pd.DataFrame(results_building_simulation).T   


           
# create folder where results will be saved:
if not os.path.isdir(paths['main'] + '\\Results'+ '\\Results_' + now):
    os.makedirs(paths['main'] + '\\Results'+ '\\Results_' + now)    

# save all results
Building_Simulation_df.to_csv(paths['main'] + '\\Results'+ '\\Results_' + now + '\\Building_Simulation.csv')
hourlyData_df.to_csv(paths['main'] + '\\Results'+ '\\Results_' + now + '\\hourlyData.csv')




#else: 
#    results_building_simulation = np.load(paths['main'] + '\\Results' + '\\Building_Simulation_12_10_2016.npy').item()
#    Building_Simulation_df= pd.DataFrame(results_building_simulation).T
#    print 'Building_Simulation_results loaded from folder'
     #read csv file and load as dataFrame   
#    test_df = pd.read_csv(r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\test.csv')   
#
#
#
#fig = plt.figure() 
#fig.suptitle('Yearly Energy Demand', fontsize=20)
#        
#with pd.plot_params.use('x_compat', True):
#    Building_Simulation_df['T_in'].plot(color='r')
#    Building_Simulation_df['T_out'].plot(color='g') 
##    Building_Simulation_df['H'].plot(color='b') 
##    Building_Simulation_df['C'].plot(color='k') 
###    Building_Simulation_df['L'].plot(color='y') 
#
#plt.legend(loc='best')
#plt.xlabel('Hour of the year', fontsize=18)
#plt.ylabel('Temperatur [°C]', fontsize=16)
#
#
##fig1 = plt.figure() 
#with pd.plot_params.use('x_compat', True):
#    Building_Simulation_df['PV'].plot(color='g')
#    
#plt.legend(loc='best')
#plt.xlabel('Hour of the year', fontsize=18)
#plt.ylabel('Energy consumption [kWh/h]', fontsize=16)    
#
#
#fig2 = plt.figure()   
#with pd.plot_params.use('x_compat', True):
#    Building_Simulation_df['C'].plot(color='k')
#    
#plt.legend(loc='best')
#plt.xlabel('Hour of the year', fontsize=18)
#plt.ylabel('Energy consumption [kWh/h]', fontsize=16)
#
#
#
#fig3 = plt.figure()   
#with pd.plot_params.use('x_compat', True):
#    Building_Simulation_df['H'].plot(color='y')
#    
#plt.legend(loc='best')
#plt.xlabel('Hour of the year', fontsize=18)
#plt.ylabel('Energy consumption [kWh/h]', fontsize=16)




hourly_data_reform = {(outerKey, innerKey): values for outerKey, innerDict in hourlyData.iteritems() for innerKey, values in innerDict.iteritems()}



from carpetPlot import carpetPlot
from prepareData_mauro import prepareMonthlyRadiatonData, average_monthly, sum_monthly
        
#From the radiation results calculate the monthly Radiation data, PV_monthly = kWh for each hour of a month      
PV_monthly, R_monthly, PV_eff_opt, Ins_avg, Ins_theoretical, PV_Function_Average, eff=  prepareMonthlyRadiatonData(PV_electricity_results, simulationOption)


H =Building_Simulation_df['H']
C =Building_Simulation_df['C']
L =Building_Simulation_df['L']
E =Building_Simulation_df['E_tot'] 
PV =Building_Simulation_df['PV']

# new empty array for Heating data:
H_monthly_array = np.empty(len(H))*np.nan
C_monthly_array = np.empty(len(C))*np.nan
L_monthly_array = np.empty(len(L))*np.nan
E_monthly_array = np.empty(len(E))*np.nan
PV_monthly_array = np.empty(len(PV))*np.nan

#
## multiply the average pv generation by the number of days per month and convert to kWh:
for i in range(len(H)):
    H_monthly_array[i] = H[i]
    C_monthly_array[i] = C[i]
    L_monthly_array[i] = L[i]
    E_monthly_array[i] = E[i]
    PV_monthly_array[i] = PV[i]

#
## average data for every hour of a month:
#L_avg = average_monthly(L_monthly_array)
#E_avg = average_monthly(E_monthly_array)
#C_avg = average_monthly(C_monthly_array)
#H_avg = average_monthly(H_monthly_array)
#PV_avg = -1* average_monthly(PV_monthly_array)


# summed data for each hour of a month:
L_sum = sum_monthly(L_monthly_array)
E_sum = sum_monthly(E_monthly_array)
C_sum = sum_monthly(C_monthly_array)
H_sum = sum_monthly(H_monthly_array)
PV_sum = -1* sum_monthly(PV_monthly_array)

#PV_function = PV_average[5]/1000



#Calculate the summed monthly values and store it in dicitionary (24 hour per every month)
monthlyData = {}

monthlyData['H'] = H_sum
monthlyData['C'] = C_sum
monthlyData['L'] = L_sum
monthlyData['E'] = E_sum
monthlyData['PV'] = PV_sum



roomFloorArea = building_data['room_width']/1000.0*building_data['room_depth']/1000.0



fig0 = carpetPlot(X = PV_sum, z_min = -12, z_max= 70, title = 'PV supply')

fig1 = carpetPlot(X = E_sum, z_min = -12, z_max= 70, title = 'Net Demand including PV')

fig2 = carpetPlot(X = C_sum, z_min = -12, z_max= 70, title = 'Cooling Demand')

fig3 = carpetPlot(X = L_sum, z_min = -12, z_max= 70, title = 'Lightning Demand')

fig4 = carpetPlot(X = H_sum, z_min = -12, z_max= 70, title = 'Heating Demand')



#fig0 = carpetPlot(X = PV_avg, z_min = -5, z_max= 0, title = 'PV supply')
#
#fig1 = carpetPlot(X = E_avg, z_min = -2, z_max= 5, title = 'Net Demand including PV')
#
#fig2 = carpetPlot(X = C_avg, z_min = 0, z_max= 5, title = 'Cooling Demand')
#
#fig3 = carpetPlot(X = L_avg, z_min = 0, z_max= 5, title = 'Lightning Demand')
#
#fig4 = carpetPlot(X = H_avg, z_min = 0, z_max= 5, title = 'Heating Demand')


#create folder to save figures as png:
os.makedirs(paths['main'] + '\\Results'+'\\Results_' + now + '\\png' )
fig0.savefig(paths['main'] + '\\Results'+ '\\Results_' + now + '\\png\\' + 'figure0' + '.png')
fig1.savefig(paths['main'] + '\\Results'+ '\\Results_' + now + '\\png\\' + 'figure1' + '.png')
fig2.savefig(paths['main'] + '\\Results'+ '\\Results_' + now + '\\png\\' + 'figure2' + '.png')
fig3.savefig(paths['main'] + '\\Results'+ '\\Results_' + now + '\\png\\' + 'figure3' + '.png')
fig4.savefig(paths['main'] + '\\Results'+ '\\Results_' + now + '\\png\\' + 'figure4' + '.png')

yearlyData = {}
yearlyData['E'] = Building_Simulation_df['E_tot'].sum()
yearlyData['PV'] = Building_Simulation_df['PV'].sum()
yearlyData['H'] = Building_Simulation_df['H'].sum()
yearlyData['C'] = Building_Simulation_df['C'].sum()
yearlyData['L'] = Building_Simulation_df['L'].sum()


yearlyData_df = pd.DataFrame(yearlyData)
monthlyData_df = pd.DataFrame(monthlyData)

yearlyData_df.to_csv(paths['main'] + '\\Results'+ '\\Results_' + now + '\\yearlyData.csv')
monthlyData_df.to_csv(paths['main'] + '\\Results'+ '\\Results_' + now + '\\monthlyData.csv')


print "\nsimulation end: " + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
"""