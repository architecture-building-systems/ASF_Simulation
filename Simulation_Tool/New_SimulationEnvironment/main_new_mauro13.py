# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:14:42 2016

main file for simulation environment

@author: Prageeth Jayathissa
@credits: Jerimias Schmidli

5.10.2016

monthly Simulation - main_new_mauro_5.gh
RC 4

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
geoLocation = 'Zuerich‐Kloten'

# Time: Which our of the year should be evaluated?
#hour_of_year = 4000 # 0? to 8760 hour

#For evalation period, which is greater than only 1 hour
 
start = 13
end =  15








#5341 -> 11.august, 11 uhr bis 12 uhr

#Option for integration of the actuation energy consumption, 'yes' = energy consumption is included
#Actuation = True # False

#set builiding parameters, will be used, when calling the RC_model function
#location = (epw_name)
#building_stystem = capacitive heating/ cooling
#occupancy_profil = type of building utilisation (Office)


## Hier könnte man HOY definieren für die Berechnung:  simulationOption = {'timePeriod' : HOY}          
#simulationOption = {'timePeriod' : '1h'}
simulationOption = {'timePeriod' : None}

#PV production plots
createPlots = True


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

# define path of geographical location:
paths['geo'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\data\geographical_location\Zuerich-Kloten' 

# define path of weather file:
paths['weather'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\WeatherData\Zurich-Kloten_2013.epw'


from epwreader import epw_reader
#read epw file of needed destination
weatherData = epw_reader(paths['weather'])



#radiation subfolder is created, there the radiation_results are saved

if not os.path.isdir(paths['radiation_results']):
        os.makedirs(paths['radiation_results'])

if not os.path.isdir(paths['radiation_wall']):
        os.makedirs(paths['radiation_wall'])

# add python_path to system path, so that all files are available:
sys.path.insert(0, paths['python'] + '\\aux_files')


# create sun data based on grasshopper file
#execfile(paths['python'] + "\\aux_files\\SunAngles_Tracking_and_temperature.py")

# calculate and save lookup table if it does not yet exist:
if not os.path.isfile(paths['data'] + '\python\electrical_simulation\curr_model_submod_lookup.npy'): 
    if not os.path.isdir(paths['data'] + '\python\electrical_simulation'):
        os.makedirs(paths['data'] + '\python\electrical_simulation')
    execfile(paths['python'] + '\\aux_files\\create_lookup_table.py')
else:
    print 'lookup table not created as it already exists'




#Set Solar Panel Properties
XANGLES=[0,15,30,45,60,75,90]
YANGLES= [-45,-30,-15,0,15,30,45]

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
"NoClusters":1,
"numberHorizontal":6,
"numberVertical":9,
"panelOffset":400,
"panelSize":400,
"panelSpacing":500,
}

#Set Building Parameters
building_data={"room_width":4900,     
"room_height":3100,
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


PV_electricity_results = {}
PV_detailed_results = {}


# create dicitionary to save optimal angles:
opt_angles = {}
BuildingRadiationData_HOD = {}



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


for monthi in range(1,13): #month:
    
    BuildingRadiationData_HOD[monthi] = {}
    
    for HOD in hour_in_month[monthi]: #hourMonth:
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
                                                              
                    
                #Wait until the radiation_results were created    
                while not os.path.exists(paths['radiation_results']+'\\RadiationResults' + '_' + str(HOD) +'_'+ str(monthi) + '_' + str(x_angle) + '_' + str(y_angle)+ '.csv'):
                    time.sleep(1)
                   
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
                        
                                           
        print 'radiation calculation finished!'
        BuildingRadiationData_HOD[monthi][HOD]= BuildingRadiationData
     
#with the radiation_results the Pv_results are calcualted
if not os.path.isfile(paths['PV'] + '\PV_electricity_results.npy'): 
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
                           XANGLES = XANGLES, YANGLES= YANGLES, hour_in_month = hour_in_month)
                           
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
                           simulationOption = {'timePeriod' : None},
                           XANGLES = XANGLES, YANGLES= YANGLES, hour_in_month = hour_in_month)

else: 
    PV_electricity_results = np.load(paths['PV'] + '\PV_electricity_results.npy').item()
    PV_detailed_results = np.load(paths['PV'] + '\PV_detailed_results.npy').item()
    print 'PV_electricity_results loaded from folder'
    
print "\npreparing data\n"

        

#Temperature value, to start the simulation with
T_in = 20

#create dicitionary to save relevant hourly data:
hourlyData = {}
Data_Heating_HOY = {}
Data_Cooling_HOY = {}
Data_Lighting_HOY = {}
Data_T_in_HOY = {}

results_building_simulation = {}
E_tot = {}

for monthi in range(1,13):
    E_tot[monthi] = {}
    Data_Heating_HOY[monthi] = {}
    Data_Cooling_HOY[monthi] = {}
    Data_Lighting_HOY[monthi] =  {}   
    Data_T_in_HOY[monthi] = {}
    results_building_simulation[monthi] = {}
    hourlyData[monthi]={}
    
    for HOD in hour_in_month[monthi]:
        print 'HOD:', HOD, 'Month:', monthi

        E_tot[monthi][HOD] = {}
        Data_Heating_HOY[monthi][HOD] = {}
        Data_Cooling_HOY[monthi][HOD] = {}
        Data_Lighting_HOY[monthi][HOD] =  {}   
        Data_T_in_HOY[monthi][HOD] = {}
        results_building_simulation[monthi][HOD] = {}
        hourlyData[monthi][HOD]={}
            
        # add python_path to system path, so that all files are available:
        sys.path.insert(0, 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RC_BuildingSimulator-master\simulator')
                                        
        # calcualte Building Simulation (RC Model) and save H,C,L and uncomfortable hours
                                                
        from main_RC_model4 import main_RC_model
        
        paths['epw_name'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RC_BuildingSimulator-master\simulator\data' + '\\Zurich-Kloten_2013.epw'
        paths['Radiation_Building'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RC_BuildingSimulator-master\simulator\data' + '\\adiation_Building_Zh.csv'
        paths['Occupancy'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RC_BuildingSimulator-master\simulator\data' + '\\Occupancy_COM.csv'                                        
                                                
        
        ii= 0
        hourlyData[monthi][HOD]['PV'] = 0.001 * PV_electricity_results['Pmpp_sum'][ii]
        ii += 1
        
        daysPerMonth = np.array([31,28,31,30,31,30,31,31,30,31,30,31])
        
        hour_of_year = 0
        
        if monthi==1:
            hour_of_year = HOD
        else:
            for i in range(0,monthi-1):  
                hour_of_year += daysPerMonth[i]*24
            hour_of_year += HOD
        
        
            
        for comb in range(0, NumberCombinations):
            
            #set occupancy profil of the building
            Data_T_in, T_out, Data_Heating, Data_Cooling, Data_Lighting = main_RC_model(monthi, hour_of_year, T_in, BuildingRadiationData_HOD[monthi][HOD][comb],paths['epw_name'],paths['Radiation_Building'],paths['Occupancy'])
            
            #save all combination results for one HOY
            Data_Heating_HOY[monthi][HOD][comb] = Data_Heating
            Data_Cooling_HOY[monthi][HOD][comb] = Data_Cooling
            Data_Lighting_HOY[monthi][HOD][comb] =  Data_Lighting       
            Data_T_in_HOY[monthi][HOD][comb] = Data_T_in[0]
     
            #determine best combination for the evaluated HOY
            E_tot[monthi][HOD][comb]=  Data_Heating_HOY[monthi][HOD][comb] + Data_Cooling_HOY[monthi][HOD][comb] + Data_Lighting_HOY[monthi][HOD][comb] - hourlyData[monthi][HOD]['PV'][comb]
            """
            Achtung PV hat combinationen noch nicht intergriert, zu ordnung muss different gemacht werden
            """
            
        hourlyData[monthi][HOD]['H'] = Data_Heating_HOY[monthi][HOD]
        hourlyData[monthi][HOD]['C'] = Data_Cooling_HOY[monthi][HOD]
        hourlyData[monthi][HOD]['L'] = Data_Lighting_HOY[monthi][HOD]           
        hourlyData[monthi][HOD]['E_tot'] = E_tot[monthi][HOD]
        hourlyData[monthi][HOD]['T_out'] = T_out    
            
        #get key with min value from the E_tot dictionary
        BestComb = min(E_tot[monthi][HOD], key=lambda comb: E_tot[monthi][HOD][comb])
       
      
        results_building_simulation[monthi][HOD]['E_tot'] = hourlyData[monthi][HOD]['E_tot'][BestComb]
        results_building_simulation[monthi][HOD]['H']  = hourlyData[monthi][HOD]['H'][BestComb]
        results_building_simulation[monthi][HOD]['C']  = hourlyData[monthi][HOD]['C'][BestComb]
        results_building_simulation[monthi][HOD]['L']  = hourlyData[monthi][HOD]['L'][BestComb]
        results_building_simulation[monthi][HOD]['PV']  = hourlyData[monthi][HOD]['PV']#[BestComb]
        results_building_simulation[monthi][HOD]['OptAngles'] = combinationAngles[BestComb]   
        results_building_simulation[monthi][HOD]['T_in'] = Data_T_in_HOY[monthi][HOD][BestComb]
        results_building_simulation[monthi][HOD]['T_out'] = hourlyData[monthi][HOD]['T_out']
        
        Building_Simulation_df = pd.DataFrame(results_building_simulation)
        Building_Simulation_df = Building_Simulation_df.T
        
        
        T_in = Data_T_in_HOY[monthi][HOD][comb]
        
df = pd.Panel.from_dict(results_building_simulation).to_frame()

#data for chossen month can be displayed
Building_df= pd.DataFrame(results_building_simulation[1]).T

fig = plt.figure() 

    
with pd.plot_params.use('x_compat', True):
    Building_df['E_tot'].plot(color='r')
    Building_df['PV'].plot(color='g') 
    Building_df['H'].plot(color='b') 
    Building_df['C'].plot(color='k') 
    Building_df['L'].plot(color='y') 
    

plt.legend(loc='best')
     
# create folder where results will be saved:
if not os.path.isdir(paths['main'] + '\\Results'):
    os.makedirs(paths['main'] + '\\Results')    
# save all results
np.save(paths['main'] + '\\Results' + '\\Building_Simulation' + '_' + str(now) + '.npy', results_building_simulation)

# create folder to save figures as png:
os.makedirs(paths['main'] + '\\Results' + '\\' + now + '\\png' )
fig.savefig(paths['main'] + '\\Results' + '\\' + now + '\\png\\' + 'figure' + '.png')



#        
print "\nsimulation end: " + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())


"""
"""
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
ts = ts.cumsum()
plt.figure()
ts.plot()
plt.savefig("foo.png", bbox_inches='tight')





    if hourlyData['PV'] == 0:
         opt_angles[hour_of_year] = combinationAngles[BestComb]
              
    else:      
         #do not move the PV panels, optimal angle HOY== angle HOY-1        
         opt_angles[hour_of_year] = opt_angles[hour_of_year-1]
       
    
        print '\nThe Evaluated hour of the year:', hour_of_year
        print 'Angle combination: ', combinationAngles[ii]
        print 'Hourly PV production is:', hourlyData['PV'][ii], 'kWh'
        print 'Hourly Heating load is:',hourlyData['H'][ii],  'kWh' 
        print 'Hourly Cooling load is:',hourlyData['C'][ii], 'kWh'
        print 'Hourly Lighting load is:',hourlyData['L'][ii], 'kWh' 
        print 'Hourly total Energy demand:',hourlyData['E_tot'][ii], 'kWh' 
#                
#        #Add PV production to the energy demand of H,C,L, total energy demand at hour_of_year
     
    
    print '\nFor HOY', hour_of_year, 'the hourly total energy demand is:', hourlyData['E_tot'][BestComb], 'kWh'
    print 'With optimal angle combination(X-angle,Y-angle):', combinationAngles[BestComb]
#        
"""



    
#plt.figure(1)
#plt.plot(range(0, int(len(PV_sum))),PV_sum[0:int(len(PV_sum))])
#plt.ylabel('Energy production')
#plt.xlabel('Angle combination')
#plt.title('HOY: ' + str(hour_of_year))

#plt.figure(2)
#plt.plot(range(4000,4001), Results[4000]['E_tot'], Results[4001]['E_tot'])

#plt.show()

#E_tot = []  
#
#for hour_of_year in range (start,end):
#    E_tot[1] = Results[hour_of_year]['E_tot']


    #if actiuation energy schould be included, option == 'True'
#    if Actuation:
#        if opt_angles[hour_of_year] == opt_angles[hour_of_year]:
#           #if there is no acuation between the hour time step, acutaion energy = 0           
#           hourlyData['Actuation'] = 0
#       else:
#           hourlyData['Actuation'] = XY

"""
"""