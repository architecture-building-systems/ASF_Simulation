# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:14:42 2016

main file for simulation environment

@author: Prageeth Jayathissa
@credits: Jerimias Schmidli

29.09.2016
"""

import os, sys
import numpy as np
import json
import time
import warnings
import csv
import matplotlib.pyplot as plt
import csv

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
 
start = 11
end =  13

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

# define path of geographical location:
paths['geo'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\data\geographical_location\Zuerich-Kloten' 


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
XANGLES=[0]
YANGLES= [-22.5,22.5]

#XANGLES=[22.5,67.5]
#YANGLES= [-22.5,22.5]


#Make a list of all angle combinations
ANGLES= [(x, y) for x in XANGLES for y in YANGLES]

#create a dicitionary with all angle combinations
combinationAngles = {}

for i in range(0,len(ANGLES)):
    combinationAngles[i] = ANGLES[i]

   

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
Results = {}

# create dicitionary to save optimal angles:
opt_angles = {}
HOY_night = {}


BuildingRadiationData_HOY = {}


for HOY in range(start,end):
    HOY_night[HOY] = False
    BuildingRadiationData = []
    
    for x_angle in XANGLES:
        
        if HOY_night[HOY] == True:
            break #HOY with no radiation are not further evaluated
                  
        for y_angle in YANGLES:
            
            comb_data={"x_angle":x_angle,
                       "y_angle":y_angle,
                       "HOY":HOY}
                       
            #create json file with the set combination of x-angle,y-angle and HOY
            with open('comb.json','w') as f:
                f.write(json.dumps(comb_data))
                print HOY, x_angle, y_angle, resultsdetected              
                                                          
                
            #Wait until the radiation_results were created    
            while not os.path.exists(paths['radiation_results']+'\\RadiationResults' + '_' + str(HOY) + '_' + str(x_angle) + '_' + str(y_angle)+ '.csv'):
                time.sleep(1)
   
                  
                
                
                
            else:
                if os.path.getsize(paths['radiation_results']+'\\RadiationResults' + '_' + str(HOY) + '_' + str(x_angle) + '_' + str(y_angle)+ '.csv') == 25879L:
                    print 'No Radiaiton: HOY =', HOY, '\nEvaluate next hour of the year!\n'
                    HOY_night[HOY] = True
                    break  #HOY with no radiation are not further evaluated
                
                else:
                    print 'next step'
                    resultsdetected += 1
                                            
                    #read total radition on wall and save it in BuildingRadiationData              
                    while not os.path.exists(paths['radiation_wall'] + '\RadiationWall' + '_' + str(HOY) + '_' + str(x_angle) + '_' + str(y_angle) + '.csv'):
                        time.sleep(1)
                    else:
                        
                        with open(paths['radiation_wall'] + '\RadiationWall' + '_' + str(HOY) + '_' + str(x_angle) + '_' + str(y_angle) + '.csv', 'r') as csvfile:
                            reader = csv.reader(csvfile)
                            for idx,line in enumerate(reader):
                                if idx == 1:
                                    BuildingRadiationData.append(float(line[0]))
                                    break
                    
                                       
    print 'radiation calculation finished!'
    BuildingRadiationData_HOY[HOY]= BuildingRadiationData
    
    
    from prepareData import prepareMonthlyRadiatonData, readLayoutAndCombinations, CalcXYAnglesAndLocation, sum_monthly


#with the radiation_results the Pv_results are calcualted
    if HOY_night[HOY]==True:
        pass # all HOY with no radiation are not used for electricity calculation
    else:
        if not os.path.isdir(paths['PV']):
            os.makedirs(paths['PV'])
        from asf_electricity_production_mauro_2 import asf_electricity_production
        print '\ncalculating PV electricity production' 
    
        if createPlots:
            PV_electricity_results[HOY], PV_detailed_results[HOY], fig1, fig2 = \
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
                               XANGLES = XANGLES, YANGLES= YANGLES, HOY = HOY)
                               
        else:
            PV_electricity_results[HOY], PV_detailed_results[HOY] = \
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
                               XANGLES = XANGLES, YANGLES= YANGLES, HOY = HOY)
        
        
        print "\npreparing data\n"  





#one could delete this loop, and change variable names to HOY
for hour_of_year in range(start,end):
    if HOY_night[hour_of_year] != True:  
        # do evaluation if HOY is not in the night 
        #from the dicitionary PV_electricity_results access from the key 4000, the values from Pmpp_sum
        PV_sum = PV_electricity_results[hour_of_year]['Pmpp_sum']
        
        
        PV_results_HOY= {}
         
        i = 0
           
        for ii in PV_sum:
            
            PV_results_HOY[i]=ii
            i += 1
            
        print 'PV results:', PV_electricity_results[hour_of_year]['Pmpp_sum']    
        
#        
                        
                                                
        #                                        
        #""" radiation energy, which enters the building (not absorbed by the PV panels) has to be transfered to
        #the building simulation
        #
        #- dependend on the amount of angle combinations, H,C,L values are going to be calcualted (maybe only for relevant hour)
        #- H,C,L values will be returned and the PV energy production is going to be subtracted
        #- the lowest overall energy demand will be determined and angle combination for specific HOY returned
        #
        # """                                        
        
        # add python_path to system path, so that all files are available:
        sys.path.insert(0, 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RC_BuildingSimulator-master\simulator')
                                        
        # calcualte Building Simulation (RC Model) and save H,C,L and uncomfortable hours
                                                
        from main_RC_model2 import main_RC_model
        
        paths['epw_name'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RC_BuildingSimulator-master\simulator\data' + '\\Zurich-Kloten_2013.epw'
        paths['Radiation_Buidling'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RC_BuildingSimulator-master\simulator\data' + '\\adiation_Building_Zh.csv'
        paths['Occupancy'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RC_BuildingSimulator-master\simulator\data' + '\\Occupancy_COM.csv'                                        
                                                
        
        NumberCombinations = len(XANGLES)*len(YANGLES) #*NoClusters
                                    
        Data_T_in, Data_Heating, Data_Cooling, Data_Lighting, Q_fenstRad = main_RC_model(start, end, NumberCombinations, BuildingRadiationData_HOY,paths['epw_name'],paths['Radiation_Buidling'],paths['Occupancy'])
        
        
        #if actiuation energy schould be included, option == 'True'
    #    if Actuation:
    #        if opt_angles[hour_of_year] == opt_angles[hour_of_year]:
    #           #if there is no acuation between the hour time step, acutaion energy = 0           
    #           hourlyData['Actuation'] = 0
    #       else:
    #           hourlyData['Actuation'] = XY
    
        #create dicitionary to save relevant hourly data:
        hourlyData = {}
        
        #get key with max value from the pv results dictionary, save the max value into hourlyData['PV']
        hourlyData['PV'] = PV_results_HOY[max(PV_results_HOY, key=lambda i: PV_results_HOY[i])]
        
        
        
        if hourlyData['PV'] != 0 or bool(opt_angles) == False :
            opt_angles[hour_of_year] = combinationAngles[max(PV_results_HOY, key=lambda i: PV_results_HOY[i])]
              
        else:      
            #do not move the PV panels, optimal angle HOY== angle HOY-1        
            opt_angles[hour_of_year] = opt_angles[hour_of_year-1]
            
                   
            
        
        hourlyData['H'] = Data_Heating[hour_of_year]
        hourlyData['C'] = Data_Cooling[hour_of_year]
        hourlyData['L'] = Data_Lighting[hour_of_year]
        hourlyData['E_HCL'] = hourlyData['H'] + hourlyData['C'] + hourlyData['L']
        
        #Add PV production to the energy demand of H,C,L, total energy demand at hour_of_year
        
        hourlyData['E_tot'] = hourlyData['E_HCL'] - hourlyData['PV']/1000 #+ hourlyData['Actuation']
        
        print '\nThe Evaluated hour of the year:', hour_of_year
        
        print 'Hourly PV production is:', hourlyData['PV'], 'Wh'
        print 'Hourly Heating load is:',hourlyData['H'],  'kWh' 
        print 'Hourly Cooling load is:',hourlyData['C'], 'kWh'
        print 'Hourly Lighting load is:',hourlyData['L'], 'kWh' 
        print 'Hourly total load is:',hourlyData['E_HCL'], 'kWh' 
        
        #Add PV production to the energy demand of H,C,L, total energy demand at hour_of_year
        
        print 'Hourly total energy demand is:', hourlyData['E_tot'], 'kWh'
        print '\nOptimal angle combination(X-angle,Y-angle):', opt_angles[hour_of_year],'\n'
        
        Results[hour_of_year] = hourlyData
        Results[hour_of_year]['OptAngles'] = opt_angles[hour_of_year]
    else:
        Results[hour_of_year] = 'night'
        
# create folder where results will be saved:
if not os.path.isdir(paths['main'] + '\\Results'):
    os.makedirs(paths['main'] + '\\Results')    
# save all results
np.save(paths['main'] + '\\Results' + '\\Results' + '_' + str(now) + '.npy', Results)
        
print "simulation end: " + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())



    
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



    
   

#        
#  
    
    

