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
#XANGLES=[45]
#YANGLES= [0]

XANGLES=[0, 15, 30, 45, 60, 75, 90]
YANGLES= [-45,-30,-15,0, 15, 30, 45]


#Make a list of all angle combinations
ANGLES= [(x, y) for x in XANGLES for y in YANGLES]

ANGLES.append((np.nan,np.nan)) # no sun
ANGLES.append((-100.,-100.)) # no movement

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
"numberHorizontal":6,#6,
"numberVertical":9,#9,
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

roomFloorArea = building_data['room_width']/1000.0 * building_data['room_depth']/1000.0 #[m^2] floor area


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

#function CalculateRadiationData

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

if panel_data['numberHorizontal'] == 0 and panel_data['numberVertical'] == 0:
    PV_electricity_results['Pmpp_sum'] = np.array(NumberCombinations * 145 * [0])
    print "PV_electricity_results is zero"
    



#with the radiation_results the Pv_results are calcualted
if not os.path.isfile(os.path.join(paths['PV'], 'PV_electricity_results.npy')): 
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
                           lookup_table_path = paths['electrical_simulation'], 
                           geo_path = paths['geo'],
                           flipOrientation= False, 
                           simulationOption = {'timePeriod' : None},
                           XANGLES = XANGLES, YANGLES= YANGLES, hour_in_month = hour_in_month, 
                           start = start, end = end, paths = paths)
                           
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
                           start = start, end = end, paths = paths)

else: 
    PV_electricity_results = np.load(os.path.join(paths['PV'], 'PV_electricity_results.npy')).item()
    PV_detailed_results = np.load(os.path.join(paths['PV'], 'PV_detailed_results.npy')).item()
    print 'PV_electricity_results loaded from folder'
    
print "\npreparing data\n"


from hourRadiation import hourRadiation, hourRadiation_calculated, sumHours
from prepareDataMain import PrepareRadiationData

hourRadiation = hourRadiation(hour_in_month, daysPerMonth)
hourRadiation_calculated = hourRadiation_calculated(hour_in_month,daysPerMonth)
sumHours = sumHours(daysPerMonth)

#rearrange the Radiation Data into into HOY form
PV, BuildingRadiationData_HOY = PrepareRadiationData(hour_in_month, 
                                                     daysPerMonth, 
                                                     BuildingRadiationData_HOD, 
                                                     PV_electricity_results, 
                                                     NumberCombinations)
PV_data = PV
 
#Temperature in what range the heating can become warmer or colder, if there ar no people in the building
setBackTemp = 4. #4.

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


optHourlyData = {}
optResultsBuildingSimulation = {}
optResultsBuildingSimulation_df = {}

x_angle_array = {}
y_angle_array = {}
Best_Key_df = {}

#set optimization type

#optimizationType = 'E_total'
#optimizationType = 'Heating'
#optimizationType = 'Cooling'
#optimizationType = 'SolarEnergy'
#optimizationType = 'E_HCL'
#optimizationType = 'Lighting'

for optimizationType in ['E_total','Heating','Cooling', 'SolarEnergy', 'E_HCL', 'Lighting']:
        
    hourlyData, results_building_simulation, Building_Simulation_df = energy_minimization(
                                                                  optimization_type = optimizationType, 
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
    
    #save RC-Model results in dictionaries for every optimization type analysed
    optHourlyData[optimizationType] = hourlyData
    optResultsBuildingSimulation[optimizationType] = results_building_simulation
    optResultsBuildingSimulation_df[optimizationType] = Building_Simulation_df
    
    
    
    #store all results in a DataFrame
    hourlyData_df = pd.DataFrame(hourlyData)
    hourlyData_reform = {(outerKey, innerKey): values for outerKey, innerDict in hourlyData.iteritems() for innerKey, values in innerDict.iteritems()}
    
    
    from prepareDataMain import prepareAngles, prepareResults
    
    
    #set optimizationType
    
    
    Best_Key_df[optimizationType], x_angle_array[optimizationType], y_angle_array[optimizationType] = prepareAngles(
                                                                        Building_Simulation_df = optResultsBuildingSimulation_df[optimizationType], 
                                                                        daysPerMonth = daysPerMonth,
                                                                        ANGLES = ANGLES)
    
    
    
    from carpetPlot import carpetPlotMask
    from prepareData_mauro import prepareMonthlyRadiatonData
    
    from createCarpetPlot import createCarpetPlot, createCarpetPlotXAngles, createCarpetPlotYAngles    
    
    fig7 = carpetPlotMask(X =x_angle_array[optimizationType], z_min = 0, z_max= 90, title = 'Altitude Angle (X-Angles)', hour_in_month = hour_in_month)
    fig8 = carpetPlotMask(X =y_angle_array[optimizationType], z_min = -45, z_max= 45, title = 'Azimuth Angle (Y-Angles)', hour_in_month = hour_in_month)
#    
    ##fig.suptitle('Yearly Energy Demand', fontsize=20)
    #fig9 = carpetPlotMask(X = x_angle_array_heat, z_min = 0, z_max= 90, title = 'Altitude Angle (X-Angles)', hour_in_month = hour_in_month)
    #fig10 = carpetPlotMask(X = y_angle_array_heat, z_min = -45, z_max= 45, title = 'Azimuth Angle (Y-Angles)', hour_in_month = hour_in_month)



        
#From the radiation results calculate the monthly Radiation data, PV_monthly = kWh for each hour of a month      
#PV_monthly, R_monthly, PV_eff_opt, Ins_avg, Ins_theoretical, PV_Function_Average, eff=  prepareMonthlyRadiatonData(PV_electricity_results, simulationOption)

# prepare Building simulation Data into final form
# kWh/DaysPerMonth, kWh/year
monthlyData, yearlyData, monthlyData_df, yearlyData_df  = prepareResults (optResultsBuildingSimulation_df['E_total'], geoLocation)



fig1 = createCarpetPlotXAngles(x_angle_array, hour_in_month)
fig2 = createCarpetPlotYAngles(y_angle_array, hour_in_month)

#create the carpet plots detailing the net energy consumption
fig0 = createCarpetPlot (monthlyData = monthlyData, roomFloorArea = roomFloorArea)




# create folder where results will be saved:
paths['result_folder'] = os.path.join(paths['main'], 'Results') 
paths['result']= os.path.join(paths['result_folder'], 'Results_' + geoLocation + '_date_' + now)

if not os.path.isdir(paths['result']):
    os.makedirs(paths['result'])    

#create folder to save figures as svg and png:
paths['svg'] = os.path.join(paths['result'], 'svg')

os.makedirs(paths['svg'])
fig0.savefig(os.path.join(paths['svg'], 'figure0' + '.svg'))
fig0.savefig(os.path.join(paths['svg'], 'figure0' + '.png'))
fig1.savefig(os.path.join(paths['svg'], 'figure1' + '.png'))
fig2.savefig(os.path.join(paths['svg'], 'figure2' + '.png'))

fig0.savefig(os.path.join(paths['svg'], 'figure3' + '.pdf'))
fig1.savefig(os.path.join(paths['svg'], 'figure4' + '.pdf'))
fig2.savefig(os.path.join(paths['svg'], 'figure5' + '.pdf'))
#fig0.savefig("foo.pdf")
#fig1.savefig("foo.pdf")
#fig2.savefig("foo.pdf")

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