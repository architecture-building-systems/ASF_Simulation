# -*- coding: utf-8 -*-
"""
Created on Tue Nov 08 11:42:45 2016

@author: Mauro
"""

import os, sys
import numpy as np
import json
import time
import warnings
import csv
import matplotlib.pyplot as plt
import pandas as pd

def initializeSimulation(SimulationData):
           
    #check if E_total is selcted
    count = 0
    for ii in SimulationData['optimizationTypes']:  
        if ii == 'E_total':
            pass
        elif ii != 'E_total':
            count +=1
    if count == len(SimulationData['optimizationTypes']):       
        print '\nE_total is needed as default!'
        print 'Change the optimizationTypes.\n'
        sys.exit()
    else:
        pass
    
    
    #Set panel data
    FolderName={
    "DataNamePV": SimulationData['DataName'],
    "DataNameWin": SimulationData['DataName']  
    }
    
    #Save parameters to be imported into grasshopper
    with open('FolderName.json','w') as f:
        f.write(json.dumps(FolderName))    
            
    
    return FolderName

def initializeASF(panel_data):
  
    #Save parameters to be imported into grasshopper
    with open('panel.json','w') as f:
        f.write(json.dumps(panel_data))
        

def setBuildingParameters(building_data):
    
    #Save parameters to be imported into grasshopper
    with open('building.json','w') as f:
        f.write(json.dumps(building_data))
    
    roomFloorArea = building_data['room_width']/1000.0 * building_data['room_depth']/1000.0 #[m^2] floor area
    
    return roomFloorArea
    
    
def initializeBuildingSimulation(building_data, BuildingProperties):
    #set building properties for the RC-Model analysis 
    BuildingProperties.update({
            "Fenst_A": building_data['room_width']/1000.0*building_data['room_height']/1000.0*building_data['glazing_percentage_h']*building_data['glazing_percentage_w'],
            "Room_Depth": building_data['room_depth']/1000.0,
            "Room_Width": building_data['room_width']/1000.0,
            "Room_Height":building_data['room_height']/1000.0})                
        
    return BuildingProperties
    
    
def setPaths(geoLocation, Occupancy, FolderName):
    
    # create dictionary to write all paths:
    paths = {}
    
    # find path of current folder (simulation_environment)
    paths['main'] = os.path.abspath(os.path.dirname(sys.argv[0]))
    
    # define paths of subfolders:
    paths['data'] =os.path.join(paths['main'], 'data')
    paths['python'] = os.path.join(paths['main'], 'python')
    paths['aux_files'] = os.path.join(paths['python'], 'aux_files')
    
    paths['radiation_results'] = os.path.join(paths['main'],'radiation_results_' + FolderName['DataNamePV'])
    paths['radiation_wall'] = os.path.join(paths['main'],  'radiation_wall_' + FolderName['DataNamePV'])
    paths['PV'] = os.path.join(paths['main'], 'PV_results')

    paths['save_results_path'] = paths['PV']
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
    
    #define paths of the RC-Model    
    paths['5R1C_ISO_simulator'] = os.path.join(paths['main'], '5R1C_ISO_simulator')
    paths['5R1C_ISO_simulator_data'] = os.path.join(paths['5R1C_ISO_simulator'], 'data')    
    paths['Occupancy'] = os.path.join(paths['5R1C_ISO_simulator_data'], Occupancy) 
    
    from SunAnglesTrackingAndTemperatureFunction import SunAnglesTackingAndTemperature
    # create sun data based on grasshopper file, this is only possible with the ladybug component SunPath
    SunTrackingData = SunAnglesTackingAndTemperature(paths = paths,
                                                     weatherData = weatherData)  
    
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
    
    return paths, weatherData, SunTrackingData
    
    
def CalculateVariables(SunTrackingData, building_data, XANGLES, YANGLES):
    #Calculate variables
    
    #hour_in_month is dependent on the location, this dict is for ZH
    hours = SunTrackingData['HoursInMonth']
    hour_in_month={}
    
    #adjust shape of hour_in_month dictionary
    for item in range(0,len(hours)):
        hour_in_month[item+1]= hours[item]
    
    
    daysPerMonth = np.array([31,28,31,30,31,30,31,31,30,31,30,31])
    
    from hourRadiation import hourRadiation, hourRadiation_calculated, sumHours
    
    
    hourRadiation = hourRadiation(hour_in_month, daysPerMonth)
    hourRadiation_calculated = hourRadiation_calculated(hour_in_month,daysPerMonth)
    sumHours = sumHours(daysPerMonth)

    
    #Make a list of all angle combinations
    ANGLES= [(x, y) for x in XANGLES for y in YANGLES]
    
    #append to more ANGLES combination option for the angle carpetplot
    ANGLES.append((np.nan,np.nan)) # no sun
    #ANGLES.append((-100.,-100.)) # no movement
    
    #create a dicitionary with all angle combinations
    combinationAngles = {}
    
    for i in range(0,len(ANGLES)):
        combinationAngles[i] = ANGLES[i]
    
    
    NumberCombinations = len(XANGLES)*len(YANGLES) #*NoClusters
    
    return ANGLES, hour_in_month, NumberCombinations, combinationAngles, daysPerMonth, hourRadiation, hourRadiation_calculated, sumHours
    

    
def runRadiationCalculation(SimulationPeriode, paths, XANGLES, YANGLES, hour_in_month, FolderName, panel_data, NumberCombinations, createPlots, start, end):
     # Start the simulation
    
    now = time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
#    print "simulation start: " + now    
    
    from RadiationCalculation_hourly import CalculateRadiationData
    
    
    
    #Calculate the Radiation on the solar panels and window with ladybug
    HourlyRadiation = CalculateRadiationData(SimulationPeriode = SimulationPeriode,
                                            XANGLES = XANGLES, 
                                            YANGLES = YANGLES, 
                                            paths = paths, 
                                            DataNamePV = FolderName['DataNamePV'],
                                            DataNameWin = FolderName['DataNameWin'])
    
    
#    
    
    #if there are no panels vertical and horizontal
    if panel_data['numberHorizontal'] == 0 and panel_data['numberVertical'] == 0:
        PV_electricity_results = {}
        
        PV_electricity_results['Pmpp_sum'] = np.array(NumberCombinations * len(hour_in_month) * [0])
        print "PV_electricity_results is zero"
        
    
    #with the radiation_results the Pv_results are calcualted, make sure you know where the results are saved, otherwise they will just be loaded
    if not os.path.isfile(os.path.join(paths['PV'], 'HourlyPV_electricity_results_' + FolderName['DataNamePV'] + '.npy')): 
        if not os.path.isdir(paths['PV']):
            os.makedirs(paths['PV'])
            
        from asf_electricity_production_mauro_hourly import asf_electricity_production
        print '\nCalculating PV electricity production'     
        
        
        if createPlots:
            PV_electricity_results, PV_detailed_results, fig1, fig2 = \
            asf_electricity_production(
                               createPlots = createPlots, 
                               lb_radiation_path = paths['radiation_results'],
                               panelsize = panel_data['panelSize'], 
                               pvSizeOption = 0,
                               save_results_path = paths['PV'], 
                               lookup_table_path = paths['electrical_simulation'], 
                               geo_path = paths['geo'],
                               flipOrientation= False, 
                               XANGLES = XANGLES, YANGLES= YANGLES, 
                               hour_in_month = hour_in_month, 
                               paths = paths, DataNamePV = FolderName['DataNamePV'],
                               SimulationPeriode = SimulationPeriode, start = start, end = end)
                               
        else:
            PV_electricity_results, PV_detailed_results = \
            asf_electricity_production(
                               createPlots = createPlots, 
                               lb_radiation_path = paths['radiation_results'],
                               panelsize = panel_data['panelSize'], 
                               pvSizeOption = 0,
                               save_results_path = paths['PV'], 
                               lookup_table_path = paths['electrical_simulation'], 
                               geo_path = paths['geo'],
                               flipOrientation= False, 
                               XANGLES = XANGLES, YANGLES= YANGLES, 
                               hour_in_month = hour_in_month,
                               paths = paths, DataNamePV = FolderName['DataNamePV'],
                               SimulationPeriode = SimulationPeriode, start = start, end = end)
    
    else: 
        PV_electricity_results = np.load(os.path.join(paths['PV'], 'HourlyPV_electricity_results_' + FolderName['DataNamePV'] + '.npy')).item()
        PV_detailed_results = np.load(os.path.join(paths['PV'], 'HourlyPV_detailed_results_' + FolderName['DataNamePV'] + '.npy')).item()
        print '\nLadyBug data loaded from Folder:'
        print 'radiation_results_' + FolderName['DataNamePV']  
        
      
    
    
    return PV_electricity_results, PV_detailed_results, HourlyRadiation, now,  
   
   
 
def PrepareRadiationData(HourlyRadiation, PV_electricity_results, NumberCombinations, SimulationPeriode, start, end):
    
    
    print '\n'          
    #add the radiation data to the specific HOY
    PV={}
    BuildingRadiationHOY= {}
    passedHours = 0
    count = 0
    
    for monthi in range(SimulationPeriode['FromMonth'], SimulationPeriode['ToMonth'] + 1):
       for day in range(SimulationPeriode['FromDay'], SimulationPeriode['ToDay'] + 1):
            for hour in range(SimulationPeriode['FromHour'], SimulationPeriode['ToHour'] + 1):        
                
                HOY = start + passedHours
                BuildingRadiationHOY[HOY] = HourlyRadiation[monthi][day][hour] #W
                
                print 'HOY: ' + str(HOY) + ' of ' + str(end)

                PV[HOY] = PV_electricity_results['Pmpp_sum'][count:count+NumberCombinations] #Watts
                count +=NumberCombinations               
               
                passedHours += 1
                         
    
    return PV, BuildingRadiationHOY


    
def runBuildingSimulation(geoLocation, paths, optimization_Types, building_data, weatherData, hourRadiation, BuildingRadiationData_HOY, PV, \
                            NumberCombinations, combinationAngles, BuildingProperties, setBackTemp, daysPerMonth, ANGLES,\
                            start, end):
    
    # add python_path to system path, so that all files are available:
    sys.path.insert(0, paths['5R1C_ISO_simulator'])     
    
    from energy_minimization_hourly import RC_Model
    from prepareDataMain_hourly import prepareAngles
    from read_occupancy import read_occupancy
    
    #create dicitionaries to save the results
    hourlyData = {}
    ResultsBuildingSimulation = {}
    
    x_angles = {} #optimized x-angles
    y_angles = {} #optimized y-angles
    BestKey = {} #optimized keys of the ANGLES dictionary
    
    #set parameters
    human_heat_emission=0.12 #[kWh] heat emitted by a human body per hour. Source: HVAC Engineers Handbook, F. Porges
    roomFloorArea = building_data['room_width']/1000.0 * building_data['room_depth']/1000.0 #[m^2] floor area
     
    #people/m2/h, W    
    occupancy, Q_human = read_occupancy(myfilename = paths['Occupancy'], human_heat_emission = human_heat_emission, floor_area = roomFloorArea)      
            
    #run the RC-Model for the needed optimization Type and save RC-Model results in dictionaries for every optimization type analysed
    for optimizationType in optimization_Types:
            
        hourlyData[optimizationType], ResultsBuildingSimulation[optimizationType] = RC_Model (
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
                                                                      setBackTemp = setBackTemp,
                                                                      occupancy = occupancy,
                                                                      Q_human = Q_human, 
                                                                      start = start, end = end                                                                      
                                                                      )
        
        
        #prepareAngles creates two arrays with x- and y-angles for the respective optimization type and a dataFrame with all the keys stored  
        BestKey[optimizationType], x_angles[optimizationType], y_angles[optimizationType] = prepareAngles(
                                                                            Building_Simulation_df = ResultsBuildingSimulation[optimizationType], 
                                                                            ANGLES = ANGLES,
                                                                            start = start, end = end)   
    
#        # prepare Building simulation Data into final form, monthly Data [kWh/DaysPerMonth], yearlyData [kWh/year]
#        monthlyData[optimizationType], yearlyData[optimizationType] = prepareResults(Building_Simulation_df = ResultsBuildingSimulation[optimizationType])
#        
    return hourlyData, ResultsBuildingSimulation, BestKey, x_angles, y_angles
    
    
    
#
#def createAllPlots(monthlyData, roomFloorArea, x_angles, y_angles, hour_in_month, optimization_Types):
#    
#    from createCarpetPlot import createCarpetPlot, createCarpetPlotXAngles, createCarpetPlotYAngles
#    
#    #create the carpet plots detailing the net energy consumption, set only monthlyData['E_total']
#    fig0 = createCarpetPlot (monthlyData = monthlyData['E_total'], roomFloorArea = roomFloorArea)
#    
#    fig = {'fig0' : fig0}
#    
#    if optimization_Types == ['E_total','Heating','Cooling', 'SolarEnergy', 'E_HCL', 'Lighting']:    
#        #create the angles carpet plots for the opimised simulation option, this option needs all simulation types
#        fig1 = createCarpetPlotXAngles(x_angles, hour_in_month)
#        fig2 = createCarpetPlotYAngles(y_angles, hour_in_month)
#        
#        fig = {'fig0' : fig0, 'fig1' : fig1, 'fig2' : fig2}
#    
#    
#    return fig




def SaveResults(now, Save, geoLocation, paths, optimization_Types,  ResultsBuildingSimulation, BuildingProperties, x_angles, y_angles, SimulationData):
    
    angles = {}
    
    angles['X_Angles']= x_angles['E_total']
    angles['Y_Angles'] = y_angles['E_total']
    angles['Temperature']= ResultsBuildingSimulation['E_total']['T_in']
    
    angles_df = pd.DataFrame(angles)
    
    anglesHOY = angles_df
    
    
    ResultsBuildingSimulation['E_total']['PV'] = ResultsBuildingSimulation['E_total']['PV']*-1    
    
    plt.style.use('ggplot')
    fig = plt.figure(figsize=(6, 3))
    
    
    ax1 = fig.add_subplot(111) 
    #ax1.title('Cloudy Day', fontsize=12)
    ax1.title.set_text(SimulationData['DataName'])      
    
  
    with pd.plot_params.use('x_compat', True):
        ResultsBuildingSimulation['E_total']['E_tot'].plot(color='r', label = 'E')    
        ResultsBuildingSimulation['E_total']['C'].plot(color='b', label = 'C')
        lns1 = ResultsBuildingSimulation['E_total']['H'].plot(color='g', label = 'H')
        lns2 = ResultsBuildingSimulation['E_total']['PV'].plot(color='y', label = 'PV')
        lns3 = ResultsBuildingSimulation['E_total']['L'].plot(color='m', label = 'L')    
        
   
#    lns = lns1+lns2+lns3
#    labs = [l.get_label() for l in lns]
#
#    lgd=ax1.legend(lns, labs, loc=4,bbox_to_anchor=(0.9,-4.5), ncol=3)       
        
    plt.legend(loc='best', fontsize = 6)
    #plt.legend(loc='center right', bbox_to_anchor=(1.3, 0.5))

    plt.ylabel('Net Energy [kWh]', fontsize=12)
    plt.yticks([-400,0,400,800,1200])
    plt.xlabel('Hour of Day', fontsize=12)   
    
    with pd.plot_params.use('x_compat', True):        
        angles_df['X_Angles'].plot(color='c',style='--', secondary_y=True) 
        angles_df['Y_Angles'].plot(color='k', style='--',secondary_y=True) 
        
    #ax1.set_yticklabels([20,100])
    #ax.set_xticklabels([])    
    
    plt.legend(loc=4, fontsize = 10)
    #plt.legend(loc='best')
    
    plt.ylabel('Angles [deg]', fontsize=12)    
    plt.yticks([-90,-45,0,45,90])
    
    plt.tight_layout()
    
#    fig = plt.figure(figsize=(4, 4))
#    plt.style.use('ggplot')
    
        
#    ax2 = fig.add_subplot(111) 
#    #ax2.title('Cloudy Day', fontsize=12)
#    ax2.title.set_text('title')  
#    
#    with pd.plot_params.use('x_compat', True):         
#        angles_df['X_ANGLES1'].plot(color='c', secondary_y=True) 
#        angles_df['Y_ANGLES1'].plot(color='k', secondary_y=True) 
#        
#    plt.legend(loc=1, fontsize = 10)
#    #plt.legend(loc='best')
#    plt.xlabel('Energy', fontsize=12)
#    plt.ylabel('Radiation [Wh/m2]', fontsize=12)    
        

    
    
#    df = pd.DataFrame(ResultsBuildingSimulation['E_total'], columns= ['E_tot','C'])
##    angles_df['X_ANGLES1'].plot(color='m', secondary_y=True) 
###        angles_df['Y_ANGLES1'].plot(color='k', secondary_y=True)    
#    
#    df.plot(style='k--', label='Series')    
#    angles_df.plot(color='m', secondary_y= ['X_ANGLES1', 'Y_ANGLES1'], label='Series')       
    
    angles_df = angles_df.T
    angles_df.columns = range(5,20)
    

     
    
    if Save == True: 
        
        # create folder where results will be saved:
        paths['result_folder'] = os.path.join(paths['main'], 'Results') 
        paths['result']= os.path.join(paths['result_folder'], 'Results_' + geoLocation + '_date_' + now + '_name_' + SimulationData['DataName'])
        
        if not os.path.isdir(paths['result']):
            os.makedirs(paths['result'])    
        
       
        for ii in optimization_Types:
            # save results 
            ResultsBuildingSimulation[ii] = ResultsBuildingSimulation[ii].T
            ResultsBuildingSimulation[ii].to_csv(os.path.join(paths['result'], 'Building_Simulation_'+ ii + '.csv'))
        
        #change name of the columns
        
       
        angles_df.to_csv(os.path.join(paths['result'], 'Angles.csv'))
        
        fig.savefig(os.path.join(paths['result'],'BuildingSimulation.pdf'), format='pdf')       
        
        BuildingProperties["heatingSystem"] = str(BuildingProperties["heatingSystem"])
        BuildingProperties["coolingSystem"] = str(BuildingProperties["coolingSystem"])
        
             
        #save building properties
        with open(os.path.join(paths['result'], 'BuildingProperties.json'), 'w') as f:
            f.write(json.dumps(BuildingProperties))
        
    
        print '\nResults are saved!'    
    
    print "\nSimulation end: " + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
    
    return ResultsBuildingSimulation, angles_df,anglesHOY

        
