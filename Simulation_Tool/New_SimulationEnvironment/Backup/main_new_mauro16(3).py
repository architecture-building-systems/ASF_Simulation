# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:14:42 2016

main file for simulation environment

@author: Mauro Luzzatto 
@credits: Prageeth Jayathissa, Jerimias Schmidli

28.10.2016

new RC-Model, modified

"""

import os, sys
import numpy as np
import json
import time
import warnings
import csv
import matplotlib.pyplot as plt
import pandas as pd

#def main ():

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
paths['data'] =os.path.join(paths['main'], 'data')
paths['python'] = os.path.join(paths['main'], 'python')
paths['aux_files'] = os.path.join(paths['python'], 'aux_files')
paths['radiation_results'] = os.path.join(paths['main'],'radiation_results')
paths['radiation_wall'] = os.path.join(paths['main'],  'radiation_wall')
paths['PV'] = os.path.join(paths['main'], 'PV_results')

paths['weather_folder']= os.path.join(os.path.dirname(paths['main']), 'WeatherData')


# define path of weather file:
paths['weather_folder']= os.path.join(os.path.dirname(paths['main']), 'WeatherData')
paths['weather'] = os.path.join(paths['weather_folder'], geoLocation + '.epw')

# add python_path to system path, so that all files are available:
sys.path.insert(0, paths['aux_files'])
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
paths['geo_location'] = os.path.join(paths['data'], 'geographical_location')
paths['geo'] = os.path.join(paths['geo_location'], geoLocation)


# create sun data based on grasshopper file, this is only possible with the ladybug component SunPath
#execfile( os.path.join(paths['aux_files'], 'SunAngles_Tracking_and_temperature.py'))

# calculate and save lookup table if it does not yet exist:
paths['data_python'] = os.path.join(paths['data'], 'python')
paths['electrical_simulation'] = os.path.join(paths['data_python'], 'electrical_simulation') 

if not os.path.isfile(os.path.join(paths['electrical_simulation'], 'curr_model_submod_lookup.npy')): 
    if not os.path.isdir(paths['electrical_simulation']):
        os.makedirs(paths['electrical_simulation'])
    execfile(os.path.join(paths['aux_files'], 'create_lookup_table.py'))
else:
    print 'lookup table not created as it already exists'


# load sunTrackingData used for the LadyBug simulation:
with open(os.path.join(paths['geo'], 'SunTrackingData.json'), 'r') as fp:
    SunTrackingData = json.load(fp)
    fp.close()


#Set Solar Panel Properties
#XANGLES=[0, 15, 30, 45, 60, 75, 90]
#YANGLES= [-45, -30, -15, 0, 15, 30, 45]

XANGLES=[0, 15, 30, 45, 60, 75, 90]
YANGLES= [-45,-30,-15,0, 15, 30, 45]


#Make a list of all angle combinations
ANGLES= [(x, y) for x in XANGLES for y in YANGLES]

ANGLES.append((-15.,-60.))

#create a dicitionary with all angle combinations
combinationAngles = {}

for i in range(0,len(ANGLES)):
    combinationAngles[i] = ANGLES[i]

NumberCombinations = len(XANGLES)*len(YANGLES) #*NoClusters   


#ANGLES.append((-100.,-100.))

print ANGLES
ANGLES = ANGLES

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
print '\nTime: ' + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())


# create dicitionary to save optimal angles:
BuildingRadiationData_HOD = {}

daysPerMonth = np.array([31,28,31,30,31,30,31,31,30,31,30,31])

#hour_in_month is dependent on the location, this dict is for ZH
hours = SunTrackingData['HoursInMonth']
hour_in_month={}
#adjust shape of hour_in_month dictionary
for item in range(0,len(hours)):
    hour_in_month[item+1]= hours[item]


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
end = 13

tic = time.time()


for monthi in range(1,13): #month:
      
    BuildingRadiationData_HOD[monthi] = {}
    
    for HOD in hour_in_month[monthi]:
        
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
                    toc = time.time() - tic
                    print 'time passed (min): ' + str(toc/60.)
                
#                #write ASFangles for Clusters
#                with open('outputASFangles.json','w') as f:
#                    f.write(json.dumps(ASFangles[index]))
#                    print "index:", index
#                      
                    
                #Wait until the radiation_results were created    
                while not os.path.exists(os.path.join(paths['radiation_results'],'RadiationResults' +'_'+  str(int(HOD)) + '_' + str(monthi)  + '_' + str(x_angle) + '_' + str(y_angle)+ '.csv')):
                    time.sleep(1)
                
                #paths['radiation_results']+'\\RadiationResults' +'_Index_'+ str(index) + '_NoCluster_' + str(NoClusters) + '_'  + str(HOD) + '_' + str(monthi)  + '_' + str(x_angle) + '_' + str(y_angle)+ '.csv'                
                
                else:
                    print 'next step'
                    resultsdetected += 1
                                                                                    
                    #read total radition on wall and save it in BuildingRadiationData              
                    while not os.path.exists(os.path.join(paths['radiation_wall'], 'RadiationWall' + '_' + str(int(HOD)) +'_'+ str(monthi) + '_'+ str(x_angle) + '_' + str(y_angle) + '.csv')):
                        time.sleep(1)
                    else:
                        with open(os.path.join(paths['radiation_wall'], 'RadiationWall' + '_' + str(int(HOD)) +'_'+ str(monthi) + '_'+ str(x_angle) + '_' + str(y_angle) + '.csv'), 'r') as csvfile:
                            reader = csv.reader(csvfile)
                            for idx,line in enumerate(reader):
                                if idx == 1:
                                    BuildingRadiationData = np.append(BuildingRadiationData, [float(line[0])])
                                    break
                        
                                           
        
        for jj in range(0,daysPerMonth[monthi-1]):
            #Radiation data is calculated for all days per month, so the data is divided through the amount of days per month
            BuildingRadiationData_HOD[monthi][HOD+24*jj]= BuildingRadiationData * 1/daysPerMonth[monthi-1]
     
print "\nEnd of radiaiton calculation: " + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())

PV_electricity_results = {}
PV_detailed_results = {}

#with the radiation_results the Pv_results are calcualted
if not os.path.isfile(os.path.join(paths['PV'], 'PV_electricity_results.npy')): 
    if not os.path.isdir(paths['PV']):
        os.makedirs(paths['PV'])
    from asf_electricity_production_mauro import asf_electricity_production
    print '\ncalculating PV electricity production'     
    
    
    if createPlots:
        PV_electricity_results, PV_detailed_results, fig1, fig2 = \
        asf_electricity_production(
                           createPlots = createPlots, 
                           lb_radiation_path = paths['radiation_results'],
                           panelsize = 400, 
                           pvSizeOption = 0,
                           save_results_path = paths['PV'], 
                           lookup_table_path = paths['electrical_simulation'], 
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
                           lookup_table_path = paths['electrical_simulation'], 
                           geo_path = paths['geo'],
                           flipOrientation= False, 
                           simulationOption = {'timePeriod' :None},
                           XANGLES = XANGLES, YANGLES= YANGLES, hour_in_month = hour_in_month,
                           start = start, end = end)

else: 
    PV_electricity_results = np.load(os.path.join(paths['PV'], 'PV_electricity_results.npy')).item()
    PV_detailed_results = np.load(os.path.join(paths['PV'], 'PV_detailed_results.npy')).item()
    print 'PV_electricity_results loaded from folder'
    
print "\npreparing data\n"



PV={}


from hourRadiation import hourRadiation, hourRadiation_calculated, sumHours

hourRadiation = hourRadiation(hour_in_month, daysPerMonth)
hourRadiation_calculated = hourRadiation_calculated(hour_in_month,daysPerMonth)
sumHours = sumHours(daysPerMonth)

        
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
            BuildingRadiationData_HOY[passedHours + DAY] = BuildingRadiationData_HOD[monthi][DAY] #kW


for hour_of_year in range(0,8760):
    PV[hour_of_year]= {}
    PV[hour_of_year]['PV']= []    

count = 0
DAY = 0

for monthi in range(1,13):
    if monthi == 1:
        passedHours = 0
    else:
        passedHours = sumHours[monthi-2]
        
    for HOD in hour_in_month[monthi]:
            for jj in range(0,daysPerMonth[monthi-1]):
                DAY = HOD + jj*24    
                PV[passedHours + DAY]['PV'] = PV_electricity_results['Pmpp_sum'][count:count+NumberCombinations] #Watts
            count +=NumberCombinations
 
#Temperature in what range the heating can become warmer or colder, if there ar no people in the building
setBackTemp = 10.

  #set building properties 
BuildingProperties={
        "Fenst_A": 13.5,
        "Room_Dept":7,
        "Room_Width": 4.9,
        "Room_Height":3.1 ,
        "glass_solar_transmitance" : 0.687 ,
        "glass_light_transmitance" : 0.744 ,
        "lighting_load" : 11.74 ,
        "lighting_control" : 300,
        "Lighting_Utilisation_Factor" : 0.45,
        "Lighting_MaintenanceFactor" : 0.9,
        "U_em" : 0.2, 
        "U_w" : 1.2,
        "ACH_vent" : 1.5,
        "ACH_infl" : 0.5,
        "ventilation_efficiency" : 0.6,
        "c_m_A_f" : 165 * 10**3, #capcitance of the building dependent on building type: medium = 165'000, heavy = 260'000, light = 110'000, very heavy = 370'000
        "theta_int_h_set" : 20,
        "theta_int_c_set" : 26,
        "phi_c_max_A_f": -np.inf, #-np.inf,
        "phi_h_max_A_f": np.inf #np.inf
        }


    
from energy_minimization import energy_minimization


#set optimization type

optimizationType = 'E_total'
#optimizationType = 'Heating'
#optimizationType = 'Cooling'
#optimizationType = 'SolarrEnergy'


hourlyData, results_building_simulation = energy_minimization(optimization_type = optimizationType, 
                                                              paths = paths,
                                                              building_data = building_data, 
                                                              weatherData = weatherData, 
                                                              hourRadiation = hourRadiation, 
                                                              BuildingRadiationData_HOY = BuildingRadiationData_HOY, 
                                                              PV = PV, 
                                                              NumberCombinations = NumberCombinations, 
                                                              combinationAngles = combinationAngles,
                                                              BuildingProperties = BuildingProperties,
                                                              setBackTemp = setBackTemp
                                                              )



#store results of the best angle combinations in DataFrame   
Building_Simulation_df= pd.DataFrame(results_building_simulation).T

#store all results in a DataFrame
hourlyData_df = pd.DataFrame(hourlyData)
hourlyData_reform = {(outerKey, innerKey): values for outerKey, innerDict in hourlyData.iteritems() for innerKey, values in innerDict.iteritems()}


from prepareAngles import prepareAngles

evaluationType = 'BestCombKey'

Best_Key_df, x_angle_array_best, y_angle_array_best = prepareAngles(evaluationType = evaluationType,
                                                                    Building_Simulation_df = Building_Simulation_df, 
                                                                    daysPerMonth = daysPerMonth,
                                                                    ANGLES = ANGLES)

#evaluationType = 'HeatComb'
#
#Heat_Key_df, x_angle_array_heat, y_angle_array_heat = prepareAngles(evaluationType = evaluationType,
#                                                          Building_Simulation_df = Building_Simulation_df, 
#                                                          daysPerMonth = daysPerMonth,
#                                                          ANGLES = ANGLES)


 


"""
fig = plt.figure()   
with pd.plot_params.use('x_compat', True):
     T_out.plot(color='y')
     Building_Simulation_df['T_in'].plot(color='r')
plt.legend(loc='best')
plt.xlabel('Hour of the year', fontsize=18)
plt.ylabel('Temp', fontsize=16)
"""

from carpetPlot import carpetPlot, carpetPlotAngles, carpetPlotMask
from prepareData_mauro import prepareMonthlyRadiatonData, average_monthly, sum_monthly


#fig5 = carpetPlotAngles(X = x_angle_array, z_min = 0, z_max= 90, title = 'Altitude Angle (X-Angles)')
#fig6 = carpetPlotAngles(X = y_angle_array, z_min = -45, z_max= 45, title = 'Azimuth Angle (Y-Angles)')

fig7 = carpetPlotMask(X = x_angle_array_best, z_min = 0, z_max= 90, title = 'Altitude Angle (X-Angles)', hour_in_month = hour_in_month)
fig8 = carpetPlotMask(X = y_angle_array_best, z_min = -45, z_max= 45, title = 'Azimuth Angle (Y-Angles)', hour_in_month = hour_in_month)

##fig.suptitle('Yearly Energy Demand', fontsize=20)
#fig9 = carpetPlotMask(X = x_angle_array_heat, z_min = 0, z_max= 90, title = 'Altitude Angle (X-Angles)', hour_in_month = hour_in_month)
#fig10 = carpetPlotMask(X = y_angle_array_heat, z_min = -45, z_max= 45, title = 'Azimuth Angle (Y-Angles)', hour_in_month = hour_in_month)


       
        
#From the radiation results calculate the monthly Radiation data, PV_monthly = kWh for each hour of a month      
PV_monthly, R_monthly, PV_eff_opt, Ins_avg, Ins_theoretical, PV_Function_Average, eff=  prepareMonthlyRadiatonData(PV_electricity_results, simulationOption)



H =Building_Simulation_df['H'] *0.001
C =Building_Simulation_df['C'] *0.001
L =Building_Simulation_df['L'] *0.001
E =Building_Simulation_df['E_tot'] *0.001 
PV =Building_Simulation_df['PV'] *0.001
E_HCL = Building_Simulation_df['E_HCL'] *0.001

# new empty array for Heating data:
H_monthly_array = np.empty(len(H))*np.nan
C_monthly_array = np.empty(len(C))*np.nan
L_monthly_array = np.empty(len(L))*np.nan
E_monthly_array = np.empty(len(E))*np.nan
E_HCL_monthly_array = np.empty(len(E_HCL))*np.nan
PV_monthly_array = np.empty(len(PV))*np.nan

#
## multiply the average pv generation by the number of days per month and convert to kWh:
for i in range(len(H)):
    H_monthly_array[i] = H[i]
    C_monthly_array[i] = C[i]
    L_monthly_array[i] = L[i]
    E_monthly_array[i] = E[i]
    E_HCL_monthly_array[i] = E_HCL[i]
    PV_monthly_array[i] = PV[i]

  

# summed data for each hour of a month:
sum_L = sum_monthly(L_monthly_array)
sum_E = sum_monthly(E_monthly_array)
sum_E_HCL = sum_monthly(E_HCL_monthly_array)
sum_C = sum_monthly(C_monthly_array)
sum_H = sum_monthly(H_monthly_array)
sum_PV = -1* sum_monthly(PV_monthly_array)


#Calculate the summed monthly values and store it in dicitionary (24 hour per every month)
monthlyData = {}
yearlyData = {}

monthlyData['H'] = sum_H
monthlyData['C'] = sum_C
monthlyData['L'] = sum_L
monthlyData['E'] = sum_E
monthlyData['E_HCL'] = sum_E_HCL
monthlyData['PV'] = sum_PV


yearlyData[geoLocation]={}
yearlyData[geoLocation]['E'] = E.sum()
yearlyData[geoLocation]['E_HCL'] = E_HCL.sum()
yearlyData[geoLocation]['PV'] = PV.sum() 
yearlyData[geoLocation]['H'] = H.sum() 
yearlyData[geoLocation]['C'] = C.sum()
yearlyData[geoLocation]['L'] = L.sum()

#create DataFrame
monthlyData_df = pd.DataFrame(monthlyData)
yearlyData_df = pd.DataFrame(yearlyData)


from createCarpetPlot import createCarpetPlot

fig0 = createCarpetPlot (monthlyData = monthlyData)




# create folder where results will be saved:
paths['result_folder'] = os.path.join(paths['main'], 'Results') 
paths['result']= os.path.join(paths['result_folder'], 'Results_' + geoLocation + '_date_' + now)

if not os.path.isdir(paths['result']):
    os.makedirs(paths['result'])    

#create folder to save figures as png:
paths['png'] = os.path.join(paths['result'], 'png')

os.makedirs(paths['png'])
fig0.savefig(os.path.join(paths['png'], 'figure0' + '.png'))


# save all results, in kWh
Building_Simulation_df.to_csv(os.path.join(paths['result'], 'Building_Simulation.csv'))
hourlyData_df.to_csv(os.path.join(paths['result'], 'hourlyData.csv'))
monthlyData_df.to_csv(os.path.join(paths['result'], 'monthlyData.csv'))
yearlyData_df.to_csv(os.path.join(paths['result'], 'yearlyData.csv'))


#save building properties
with open(os.path.join(paths['result'], 'BuildingProperties.json'), 'w') as f:
    f.write(json.dumps(BuildingProperties))

print "\nsimulation end: " + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())

#main()