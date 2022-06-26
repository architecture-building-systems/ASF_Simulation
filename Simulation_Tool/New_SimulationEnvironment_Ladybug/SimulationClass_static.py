# -*- coding: utf-8 -*-
"""
Created on Tue Nov 08 11:42:45 2016

@author: PJ
@credits: Mauro


"""

import os, sys
import numpy as np
import json
import time
import warnings
import csv
import matplotlib.pyplot as plt
import pandas as pd
sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), '5R1C_ISO_simulator'))    
    
from buildingPhysics import Building #Importing Building Class
from supplySystem import *  
from emissionSystem import *


class ASF_Simulation(object):
    #initilize ASF_simulation class

    #@Michael: This initialisation will need to be modified to fit your code
    def __init__(self,
            SimulationData,
            BlindData = 
            {"PERCENT_HEIGHT" : [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],"TILT_ANGLE": [0, 45, 90],"slat_height" : 100,"slat_thickness" : 2,"BlindOffset": 150, "BlindGridSize":50},
            PanelData = 
            {"moduleHeight": 1600, "moduleWidth":700, "PV_Height":1600,"PanelGridSize": 25},
            BuildingData = 
            {"room_width": 4900, "room_height":3100, "room_depth":7000, "WWR": 55, "FrameThickness":100, "WindowGridSize": 200, "BuildingOrientation" : 0},
            BuildingProperties = 
            {"glass_solar_transmittance" : 0.691,"glass_light_transmittance" : 0.744,"lighting_load" : 11.74,"lighting_control" : 300,"Lighting_Utilisation_Factor" :  0.6,\
            "Lighting_Maintenance_Factor" : 0.9,"U_em" : 0.2,"U_w" : 1.1,"ACH_vent" : 1.5,"ACH_infl" :0.5,"ventilation_efficiency" : 0.6 ,"c_m_A_f" : 165 * 10**3,"theta_int_h_set" : 22,\
            "theta_int_c_set" : 26,"phi_c_max_A_f": -np.inf,"phi_h_max_A_f":np.inf,"heatingSupplySystem" : DirectHeater,"coolingSupplySystem" : DirectCooler, "heatingEmissionSystem" : AirConditioning,"coolingEmissionSystem" : AirConditioning,},
            SimulationOptions= 
            {'setBackTempH' : 4.,'setBackTempC' : 4., 'Occupancy' : 'Occupancy_COM.csv','ActuationEnergy' : False, "Temp_start" : 20, 'human_heat_emission' : 0.12,},
            CO2ComputationOptions=
            {'CO2_content_produced_electricity': 40}):
                    
                            
        #define varibales of object
        self.SimulationData=SimulationData
        self.PanelData=PanelData
        self.BlindData=BlindData
        self.BuildingData=BuildingData
        self.BuildingProperties=BuildingProperties
        self.SimulationOptions=SimulationOptions

        self.BuildingData["window_percentage_h"] = (self.BuildingData["WWR"]/100.0)**0.5
        self.BuildingData["window_percentage_w"] = (self.BuildingData["WWR"]/100.0)**0.5
        
        self.XANGLES=self.BlindData['PERCENT_HEIGHT']
        self.YANGLES = self.BlindData['TILT_ANGLE']	
        self.createPlots=False
        self.geoLocation = SimulationData['geoLocation']
        self.now = time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
        self.optimization_Types = self.SimulationData['optimizationTypes']

        self.CO2ComputationOptions = CO2ComputationOptions

        total_blind_combinations = 0 
        for ii in self.XANGLES:
            for jj in self.YANGLES: 
                total_blind_combinations+=1
        print "total_blind_combinations", total_blind_combinations
        self.SimulationData['total_blind_combinations']= total_blind_combinations

        #Set folder name and chosen epw-file
        self.FolderName={
        "DataFolderName": SimulationData['DataFolderName'],
        "EPW" : SimulationData['EPWfile']  
        }
        
        #Save parameters to be imported into grasshopper
        with open('FolderName.json','w') as f:
            f.write(json.dumps(self.FolderName))    
                
        

    def initializeASF(self):
    
        #Save parameters to be imported into grasshopper
        with open('static_panel.json','w') as f:
            f.write(json.dumps(self.PanelData))

        with open('blinds.json','w') as f:
            f.write(json.dumps(self.BlindData))
            

    def setBuildingParameters(self):
        
        #Save parameters to be imported into grasshopper
        with open('building.json','w') as f:
            f.write(json.dumps(self.BuildingData))
        
        #calculate room floor area
        self.roomFloorArea = self.BuildingData['room_width']/1000.0 * self.BuildingData['room_depth']/1000.0 #[m^2] floor area
        
        
        
    def initializeBuildingSimulation(self):
        #set building properties for the RC-Model analysis 
        self.BuildingProperties.update({
                "Fenst_A": self.BuildingData['room_width']/1000.0*self.BuildingData['room_height']/1000.0*self.BuildingData['window_percentage_h']*self.BuildingData['window_percentage_w'],
                #"Fenst_A": self.BuildingData['room_width']/1000.0*self.BuildingData['room_height']/1000.0*self.BuildingData['glazing_percentage_h']*self.BuildingData['glazing_percentage_w'],
                "Room_Depth": self.BuildingData['room_depth']/1000.0,
                "Room_Width": self.BuildingData['room_width']/1000.0,
                "Room_Height":self.BuildingData['room_height']/1000.0})                
        
        
    def setPaths(self): 
    
        #set the occupancy file, which will be used for the evaluation
        Occupancy = self.SimulationOptions['Occupancy']

        # create dictionary to write all paths:
        self.paths = {}
        
        # find path of current folder (simulation_environment)
        self.paths['main'] = os.path.abspath(os.path.dirname(__file__))
        
        # define self.paths of subfolders:
        self.paths['data'] =os.path.join(self.paths['main'], 'data')
        self.paths['python'] = os.path.join(self.paths['main'], 'python')
        self.paths['RadiationData'] = os.path.join(self.paths['main'], 'RadiationData')
        #path of the ladybug radiation results for the ASF and window
        self.paths['radiation_results'] = os.path.join(self.paths['RadiationData'],'radiation_results_' + self.FolderName['DataFolderName'])
        self.paths['radiation_wall'] = os.path.join(self.paths['RadiationData'],  'radiation_wall_' + self.FolderName['DataFolderName'])
        #folder where radiaton results are going to be stored
        self.paths['PV'] = os.path.join(self.paths['main'], 'PV_results')
        self.paths['save_results_path'] = self.paths['PV']

        self.paths['weather_folder']= os.path.join(os.path.dirname(self.paths['main']), 'WeatherData')
        
        
        # define path of weather file:
        self.paths['weather_folder']= os.path.join(os.path.dirname(self.paths['main']), 'WeatherData')
        print self.geoLocation
        self.paths['weather'] = os.path.join(self.paths['weather_folder'], self.geoLocation + '.epw')

        #define path for CO2 electrcitiy calculations
        self.paths['CO2_electricity'] = os.path.join(self.paths['main'],'CO2_electricity')
        
        # add python_path to system path, so that all files are available:
        sys.path.insert(0, self.paths['python'])
        
        from epwreader import epw_reader
        from SunAnglesTrackingAndTemperatureFunction import SunAnglesTackingAndTemperature # used?
        from create_lookup_table import lookUpTableFunction

        #read epw file of needed destination
        self.weatherData = epw_reader(self.paths['weather'])
        self.radiation = self.weatherData[['year', 'month', 'day', 'hour','dirnorrad_Whm2', 'difhorrad_Whm2','glohorrad_Whm2','totskycvr_tenths']]

        if not os.path.isdir(self.paths['PV']):
            os.makedirs(self.paths['PV']) 

        if not os.path.isdir(self.paths['RadiationData']):
            os.makedirs(self.paths['RadiationData'])

        #radiation subfolder is created, there the radiation_results are saved
        if not os.path.isdir(self.paths['radiation_results']):
            os.makedirs(self.paths['radiation_results'])
        
        if not os.path.isdir(self.paths['radiation_wall']):
            os.makedirs(self.paths['radiation_wall'])
        
        # define path of geographical location:
        self.paths['geo_location'] = os.path.join(self.paths['data'], 'geographical_location')
        self.paths['geo'] = os.path.join(self.paths['geo_location'], self.geoLocation)
        
        #define self.paths of the RC-Model    
        self.paths['5R1C_ISO_simulator'] = os.path.join(self.paths['main'], '5R1C_ISO_simulator')
        self.paths['5R1C_ISO_simulator_data'] = os.path.join(self.paths['5R1C_ISO_simulator'], 'data')    
        self.paths['Occupancy'] = os.path.join(self.paths['5R1C_ISO_simulator_data'], Occupancy) 
        
        
        # create sun data based on grasshopper file, this is only possible with the ladybug component SunPath
        self.SunTrackingData = SunAnglesTackingAndTemperature(paths = self.paths,
                                                                weatherData = self.weatherData)    

        # calculate and save lookup table if it does not yet exist:
        self.paths['data_python'] = os.path.join(self.paths['data'], 'python')
        self.paths['electrical_simulation'] = os.path.join(self.paths['data_python'], 'electrical_simulation') 
    
        #check if look up table is already created
        if not os.path.isfile(os.path.join(self.paths['electrical_simulation'], 'curr_model_submod_lookup.npy')): 
            if not os.path.isdir(self.paths['electrical_simulation']):
                os.makedirs(self.paths['electrical_simulation'])
            lookUpTableFunction(self.paths)
        else:
            print 'lookup table not created as it already exists'
        
        
        # load self.sunTrackingData used for the LadyBug simulation:
        with open(os.path.join(self.paths['geo'], 'SunTrackingData.json'), 'r') as fp:
            self.SunTrackingData = json.load(fp)
            fp.close()
        
        
        
    def CalculateVariables(self):
        #Calculate variables
        from hourRadiation import hourRadiation, hourRadiation_calculated, sumHours

        #hour_in_month is dependent on the location, this dict is for ZH
        hours = self.SunTrackingData['HoursInMonth']
        self.hour_in_month={}
        
        #adjust shape of self.hour_in_month dictionary
        for item in range(0,len(hours)):
            self.hour_in_month[item+1]= hours[item]
        
        
        self.daysPerMonth = np.array([31,28,31,30,31,30,31,31,30,31,30,31])
        
        #hours for which the radiaiton is available
        self.hourRadiation = hourRadiation(self.hour_in_month, self.daysPerMonth)
        #hours for which the radiaiton is calculated
        self.hourRadiation_calculated = hourRadiation_calculated(self.hour_in_month,self.daysPerMonth)
            #summe of the hours of year in monthly steps
        self.sumHours = sumHours(self.daysPerMonth)
        
        #Make a list of all angle combinations
        self.ANGLES= [(x, y) for x in self.XANGLES for y in self.YANGLES]
        
        #append ANGLES combination option, for the case, the ASF is not moving and there is no sunlight
        self.ANGLES.append((0.1111,0.1111)) # no sun
    
        #create a dicitionary with all angle combinations
        self.combinationAngles = {}
        
        for i in range(0,len(self.ANGLES)):
            self.combinationAngles[i] = self.ANGLES[i]
        
        
        self.NumberCombinations = len(self.XANGLES)*len(self.YANGLES) #*NoClusters
        self.total_pv_combinations = self.SimulationData['total_pv_combinations']
        self.total_blind_combinations = self.SimulationData['total_blind_combinations']
        
        

        
    def runRadiationCalculation(self):

        from RadiationCalculation_static import CalculateRadiationData
        from static_electricity_production_2 import asf_electricity_production

        #Calculate the Radiation on the solar panels and window with ladybug
        self.BuildingRadiationData_HOD = CalculateRadiationData(XANGLES = self.XANGLES, 
                                                                YANGLES = self.YANGLES, 
                                                                paths = self.paths,
                                                                daysPerMonth = self.daysPerMonth, 
                                                                hour_in_month = self.hour_in_month,
                                                                FolderName = self.SimulationData)
        
        """#print self.PanelData['numberHorizontal']
        #if there are no panels vertical and horizontal
        if self.PanelData['numberHorizontal'] == 0 and self.PanelData['numberVertical'] == 0:
            print 'hellow'
            self.PV_electricity_results = {}
            
            self.PV_electricity_results['Pmpp_sum'] = np.array(self.NumberCombinations * len(self.hour_in_month) * [0])
            print "PV_electricity_results is zero"
            
        
        #with the radiation_results the Pv_results are calcualted, make sure you know where the results are saved, otherwise they will just be loaded
        else:"""
        if not os.path.isfile(os.path.join(self.paths['PV'], 'PV_electricity_results_' + self.SimulationData['FileName'] + '.npy')): 
            if not os.path.isdir(self.paths['PV']):
                os.makedirs(self.paths['PV'])
            print '\nCalculating PV electricity production'     
            
            
            if self.createPlots:
                self.PV_electricity_results, self.PV_detailed_results, fig1, fig2 = \
                    asf_electricity_production(
                                    createPlots = self.createPlots, 
                                    lb_radiation_path = self.paths['radiation_results'],
                                    panelsize = self.PanelData['moduleWidth'], 
                                    pvSizeOption = 0,
                                    save_results_path = self.paths['PV'], 
                                    lookup_table_path = self.paths['electrical_simulation'], 
                                    geo_path = self.paths['geo'],
                                    flipOrientation= False, 
                                    SimulationData = self.SimulationData,
                                    XANGLES = self.XANGLES, YANGLES= self.YANGLES, 
                                    hour_in_month = self.hour_in_month, 
                                    paths = self.paths, DataNamePV = self.SimulationData['FileName'])
                                    
            else:
                #option the show plots of PV-production calculation
                self.PV_electricity_results, self.PV_detailed_results = \
                    asf_electricity_production(
                                    createPlots = self.createPlots, 
                                    lb_radiation_path = self.paths['radiation_results'],
                                    panelsize = self.PanelData['moduleWidth'], 
                                    pvSizeOption = 0,
                                    save_results_path = self.paths['PV'], 
                                    lookup_table_path = self.paths['electrical_simulation'], 
                                    geo_path = self.paths['geo'],
                                    flipOrientation= False, 
                                    SimulationData = self.SimulationData,
                                    XANGLES = self.XANGLES, 
                                    YANGLES= self.YANGLES, 
                                    hour_in_month = self.hour_in_month,
                                    paths = self.paths, 
                                    DataNamePV = self.SimulationData['FileName'])
        
        else: 
            #if PV-results are available, they will be loaded from folder
            self.PV_electricity_results = np.load(os.path.join(self.paths['PV'], 'PV_electricity_results_' + self.SimulationData['FileName'] + '.npy'), allow_pickle=True).item()
            self.PV_detailed_results = np.load(os.path.join(self.paths['PV'], 'PV_detailed_results_' + self.SimulationData['FileName'] + '.npy'), allow_pickle=True).item()
            print '\nLadyBug data loaded from Folder:'
            print 'radiation_results_' + self.FolderName['DataFolderName']  
            print 'File: ', self.SimulationData['FileName']

    
    
    def PrepareRadiationData(self):
        #arrange radiaiton data into the correct form, so it can be used for the RC-model calculation
        
        from hourRadiation import hourRadiation, hourRadiation_calculated, sumHours
        
        hourRadiation = hourRadiation(self.hour_in_month, self.daysPerMonth)
        hourRadiation_calculated = hourRadiation_calculated(self.hour_in_month,self.daysPerMonth)
        sumHours = sumHours(self.daysPerMonth)
                    
        #add the radiation data to the specific HOY
        self.PV={}
        self.BuildingRadiationData_HOY= {}
        passedHours = 0
        
        for monthi in range(1,13):
            if monthi == 1:
                passedHours = 0
            else:
                passedHours = sumHours[monthi-2]     
            
            for HOD in self.hour_in_month[monthi]:
                for ii in range(0,self.daysPerMonth[monthi-1]):             
                    DAY = ii*24 + int(HOD)
                    
                    self.BuildingRadiationData_HOY[passedHours + DAY] = self.BuildingRadiationData_HOD[monthi][DAY] #W
            
            
        count = 0
        DAY = 0
        passedHours = 0
        #check if no panels are selected, if so, than PV-Production is zero
        """if self.PanelData['numberHorizontal'] == 0 and self.PanelData['numberVertical'] == 0:
            
                for hour_of_year in range(0,8760):
                    self.PV[int(hour_of_year)] = [0]
        else:		"""
        for monthi in range(1,13):
            for HOD in self.hour_in_month[monthi]:
                for jj in range(0,self.daysPerMonth[monthi-1]):
                    DAY = passedHours + jj*24 + HOD     
                    self.PV[DAY] = self.PV_electricity_results['Pmpp_sum'][count:count+self.total_pv_combinations] #Watts
                count +=self.total_pv_combinations
            passedHours += self.daysPerMonth[monthi-1]*24

        
        #add the window radiation data to the specific HOY		TODO: Check number combinations here	
        for hour_of_year in range(0,8760):
            if hour_of_year not in hourRadiation:
                self.BuildingRadiationData_HOY[int(hour_of_year)] = np.asarray([0]* self.total_blind_combinations, dtype = np.float64)
                self.PV[int(hour_of_year)] = np.asarray([0]* self.total_pv_combinations, dtype = np.float64)


        
        
        
    def runBuildingSimulation(self):
        #method which calls the RC-Model and runs the building energy simulation
        
        # add python_path to system path, so that all files are available:
        sys.path.insert(0, self.paths['5R1C_ISO_simulator'])
            
        if self.BuildingProperties["blinds_control"]==True:	
            from energy_minimization_static_blinds import RC_Model
        else: 
            from energy_minimization_static import RC_Model

        from prepareDataMain import prepareAngles, prepareResults, prepareResultsELEC
        from read_occupancy import read_occupancy
                
        #create dicitionaries to save the results
        self.hourlyData = {}
        self.monthlyData = {}
        self.yearlyData = {}
        self.ResultsBuildingSimulation = {} #total energy building simulation results
        self.BuildingSimulationELEC = {} #Building simulation results, if heating/cooling system is chosen
        self.x_angles = {} #optimized x-angles
        self.y_angles = {} #optimized y-angles
        self.BestKey_df = {} #optimized keys of the ANGLES dictionary
                
                        
        #people/m2/h, W    
        occupancy, Q_human = read_occupancy(myfilename = self.paths['Occupancy'], human_heat_emission = self.SimulationOptions['human_heat_emission'] , floor_area = self.roomFloorArea)    
                
                        
        #run the RC-Model for the needed optimization Type and save RC-Model results in dictionaries for every optimization type analysed
        for optimizationType in self.optimization_Types:
            self.hourlyData[optimizationType], self.ResultsBuildingSimulation[optimizationType], \
                self.BuildingSimulationELEC[optimizationType] = RC_Model (
                                                                    optimization_type = optimizationType, 
                                                                    paths = self.paths,
                                                                    building_data = self.BuildingData, 
                                                                    weatherData = self.weatherData,  
                                                                    BuildingRadiationData_HOY = self.BuildingRadiationData_HOY, 
                                                                    PV = self.PV, 
                                                                    NumberCombinations = self.NumberCombinations, 
                                                                    combinationAngles = self.combinationAngles,
                                                                    BuildingProperties = self.BuildingProperties,
                                                                    SimulationOptions = self.SimulationOptions,
                                                                    occupancy = occupancy,
                                                                    Q_human = Q_human, 
                                                                    ANGLES=self.ANGLES
                                                                    )
        
            #prepareAngles creates two arrays with x- and y-angles for the respective optimization type and a dataFrame with all the keys stored  
            self.BestKey_df[optimizationType], self.x_angles[optimizationType], self.y_angles[optimizationType] = prepareAngles(
                                                                                Building_Simulation_df = self.ResultsBuildingSimulation[optimizationType], 
                                                                                daysPerMonth = self.daysPerMonth,
                                                                                ANGLES = self.ANGLES)   
        
            
            #calculate the monthlyData dependet on which opimization is chosen
            if optimizationType == ('E_total' or 'Heating' or 'Cooling' or 'E_HCL' or 'SolarEnergy' or 'Lighting'):
                # prepare Building simulation Data into final form, monthly Data [kWh/DaysPerMonth], self.yearlyData [kWh/year]
                self.monthlyData[optimizationType], self.yearlyData[optimizationType] = prepareResults(Building_Simulation_df = self.ResultsBuildingSimulation[optimizationType])
            
            elif optimizationType == ('E_total_elec' or 'Heating_elec' or 'Cooling_elec'  or 'E_HCL_elec' ):                                                           
                self.monthlyData[optimizationType], self.yearlyData[optimizationType] = prepareResultsELEC(Building_Simulation_df = self.BuildingSimulationELEC[optimizationType])
            
    def computeElecFlow(self):

        from hourlySelfConsumption import computeSelfConsumption, monthlyAndYearlyFLows, impacts_energy_flows
        
        self.Energy_Flow_df = {}
        self.monthlyFlowElec = {}
        self.yearlyFlowElec = {}
        self.totalMonthlyData = {}
        self.monthlyImpactFlow = {}
        self.av_monthly_impact_el = {}
        
        for optimizationType in self.optimization_Types:
            self.Energy_Flow_df[optimizationType] = computeSelfConsumption(SimulationData_dict = self.ResultsBuildingSimulation[optimizationType])
            self.monthlyFlowElec[optimizationType], self.totalMonthlyData[optimizationType], self.yearlyFlowElec[optimizationType] = monthlyAndYearlyFLows(Energy_Flow_df = self.Energy_Flow_df[optimizationType])  #W , floor_area = self.roomFloorArea
            self.monthlyImpactFlow[optimizationType], self.av_monthly_impact_el[optimizationType], self.yearlyImpactFlow = impacts_energy_flows(paths = self.paths, monthlyData = self.monthlyFlowElec[optimizationType])


    def createAllPlots(self):
        #create energy- and angle- carpet plots
        
        from createCarpetPlot_static import createCarpetPlot, createCarpetPlotXAngles, createCarpetPlotYAngles
        from hourlySelfConsumption import plotFlowElec, plotCO2, plotAver_CO2
        self.fig = {}    
        
        # carpet plot for total energy values
        if ('E_total') in self.optimization_Types:    
            #create the carpet plots detailing the net energy consumption, set only monthlyData['E_total']
            print '\nFigure: total energy demand'    
            
            fig0 = createCarpetPlot (monthlyData = self.monthlyData['E_total'], roomFloorArea = self.roomFloorArea,  H = 'H', C = 'C', E = 'E', E_HCL = 'E_HCL')
            
            self.fig.update({'fig0': fig0})
        # carpet plots for electricity demand
        if ('E_total_elec') in self.optimization_Types:
            
            print 'Figure: total electrical energy demand'
            
            figA = createCarpetPlot (monthlyData = self.monthlyData['E_total_elec'], roomFloorArea = self.roomFloorArea,  H = 'H_elec', C = 'C_elec', E = 'E_elec', E_HCL = 'E_HCL_elec')
            self.fig.update({'figA' : figA})
        
        # angle-carpet plots
        if ('E_total' and 'Heating' and 'Cooling' and 'E_HCL') in self.optimization_Types: 
            if ('SolarEnergy' and 'Lighting') in self.optimization_Types:
                #create the angles carpet plots for the opimised simulation option, this option needs all simulation types
                fig1 = createCarpetPlotXAngles(self.x_angles, self.hour_in_month, H = 'Heating', C = 'Cooling', E = 'E_total', E_HCL = 'E_HCL')
                fig2 = createCarpetPlotYAngles(self.y_angles, self.hour_in_month, H = 'Heating', C = 'Cooling', E = 'E_total', E_HCL = 'E_HCL')

                self.fig.update({'fig1' : fig1, 'fig2' : fig2})

        if ('E_total_elec' and 'Heating_elec' and 'Cooling_elec'  and 'E_HCL_elec' ) in self.optimization_Types:
            if ('SolarEnergy' and 'Lighting') in self.optimization_Types:

                #create the angles carpet plots for the opimised simulation option, this option needs all simulation types
                figB = createCarpetPlotXAngles(self.x_angles, self.hour_in_month, H = 'Heating_elec', C = 'Cooling_elec', E = 'E_total_elec', E_HCL = 'E_HCL_elec')
                figC = createCarpetPlotYAngles(self.y_angles, self.hour_in_month, H = 'Heating_elec', C = 'Cooling_elec', E = 'E_total_elec', E_HCL = 'E_HCL_elec')
                
                self.fig.update({'figB' : figB, 'figC' : figC})
        
        if ('E_total') in self.optimization_Types:
            fig_elec = plotFlowElec(self.Energy_Flow_df['E_total'], self.monthlyFlowElec['E_total'], self.yearlyFlowElec['E_total'], self.totalMonthlyData['E_total'], self.roomFloorArea)
            self.fig.update({'fig_elec' : fig_elec})

            #fig_CO2 = plotCO2(self.monthlyImpactFlow['E_total'])
            #self.fig.update({'fig_CO2' : fig_CO2})

            fig_avCO2 = plotAver_CO2(self.av_monthly_impact_el['E_total'])
            self.fig.update({'fig_avCO2' : fig_avCO2})
    
    def SaveResults(self):
        #method which saves the data and plots    
        #self.monthlyData = pd.DataFrame(self.monthlyData)
        self.yearlyData = pd.DataFrame(self.yearlyData)
        self.totalMonthlyData = pd.DataFrame(self.totalMonthlyData['E_total']).T
        self.monthlyImpactFlow = pd.DataFrame(self.monthlyImpactFlow['E_total']).T
        self.yearlyFlowElec = pd.DataFrame(self.yearlyFlowElec['E_total'], index=[0]).T
        #self.monthlyFlowElec = pd.DataFrame(self.monthlyFlowElec)

        #BestKeyDF = pd.DataFrame(self.BestKey_df)    
        if self.SimulationData['Save']: 
            # create folder where results will be saved:
            self.paths['result_folder'] = os.path.join(self.paths['main'], 'Results')
            if self.BuildingProperties["blinds_control"]==True: 
                #self.paths['result']= os.path.join(self.paths['result_folder'], 'Results_' + self.SimulationData['FileName'] + '_date_' + self.now + '_threshold' + '_' + self.SimulationData['ResultName'])
                self.paths['result']= os.path.join(self.paths['result_folder'], 'Results_' + self.SimulationData['FileName'] + '_threshold' + '_' + self.SimulationData['ResultName'])
            else: 
                #self.paths['result']= os.path.join(self.paths['result_folder'], 'Results_' + self.SimulationData['FileName'] + '_date_' + self.now+ '_' + self.SimulationData['ResultName'])	
                self.paths['result']= os.path.join(self.paths['result_folder'], 'Results_' + self.SimulationData['FileName'] + '_' + self.SimulationData['ResultName'])	
            if not os.path.isdir(self.paths['result']):
                os.makedirs(self.paths['result'])    
                    
            #create folder to save figures as svg and png:
            self.paths['pdf'] = os.path.join(self.paths['result'], 'Figures')
            if not os.path.isdir(self.paths['pdf']):
                os.makedirs(self.paths['pdf'])

            if ('E_total') in self.optimization_Types:
                self.fig['fig0'].savefig(os.path.join(self.paths['pdf'], 'figure0' + '.pdf'))
                self.fig['fig0'].savefig(os.path.join(self.paths['pdf'], 'figure0' + '.png'))
                
                self.fig['fig_elec'].savefig(os.path.join(self.paths['pdf'], 'figure_elec' + '.pdf'))
                self.fig['fig_elec'].savefig(os.path.join(self.paths['pdf'], 'figure_elec' + '.png'))
                #self.fig['fig_elec'].get_figure().savefig(os.path.join(self.paths['pdf'], 'figure_elec' + '.pdf'))
                #self.fig['fig_elec'].get_figure().savefig(os.path.join(self.paths['pdf'], 'figure_elec' + '.png'))

                #self.fig['fig_CO2'].savefig(os.path.join(self.paths['pdf'], 'figure_CO2' + '.pdf'))
                #self.fig['fig_CO2'].savefig(os.path.join(self.paths['pdf'], 'figure_CO2' + '.png'))

                self.fig['fig_avCO2'].savefig(os.path.join(self.paths['pdf'], 'figure_AvCO2' + '.pdf'))
                self.fig['fig_avCO2'].savefig(os.path.join(self.paths['pdf'], 'figure_AvCO2' + '.png'))

            # self.fig['fig0'].savefig(os.path.join(self.paths['pdf'], 'figure0' + '.pdf'))
            # self.fig['fig0'].savefig(os.path.join(self.paths['pdf'], 'figure0' + '.png'))
            
                if ('E_total_elec') in self.optimization_Types:
                    self.fig['figA'].savefig(os.path.join(self.paths['pdf'], 'figureA' + '.pdf'))
                    self.fig['figA'].savefig(os.path.join(self.paths['pdf'], 'figureA' + '.png'))
                else:
                    pass

                if ('E_total' and 'Heating' and 'Cooling' and 'E_HCL') in self.optimization_Types: 
                    if ('SolarEnergy' and 'Lighting') in self.optimization_Types:                          
                        #save figures
                        self.fig['fig1'].savefig(os.path.join(self.paths['pdf'], 'figure1' + '.pdf'))
                        self.fig['fig2'].savefig(os.path.join(self.paths['pdf'], 'figure2' + '.pdf'))
                        self.fig['fig1'].savefig(os.path.join(self.paths['pdf'], 'figure1' + '.png'))
                        self.fig['fig2'].savefig(os.path.join(self.paths['pdf'], 'figure2' + '.png'))
                else:
                    pass
                
                if ('E_total_elec' and 'Heating_elec' and 'Cooling_elec'  and 'E_HCL_elec' ) in self.optimization_Types:
                    if ('SolarEnergy' and 'Lighting') in self.optimization_Types:           
                        #save figures
                        self.fig['figB'].savefig(os.path.join(self.paths['pdf'], 'figureB' + '.pdf'))
                        self.fig['figC'].savefig(os.path.join(self.paths['pdf'], 'figureC' + '.pdf'))
                        self.fig['figB'].savefig(os.path.join(self.paths['pdf'], 'figureB' + '.png'))
                        self.fig['figC'].savefig(os.path.join(self.paths['pdf'], 'figureC' + '.png'))
                    else:
                        pass
                
                for ii in self.optimization_Types:
                    if ii == ('E_total' or 'Heating' or 'Cooling' or 'E_HCL' or 'SolarEnergy' or 'Lighting'):
                        # save results 
                        self.ResultsBuildingSimulation[ii].to_csv(os.path.join(self.paths['result'], 'BuildingSimulation_'+ ii + '.csv'))
                    elif ii == ('E_total_elec' or 'Heating_elec' or 'Cooling_elec'  or 'E_HCL_elec' ):
                        self.BuildingSimulationELEC[ii].to_csv(os.path.join(self.paths['result'], 'BuildingSimulationELEC_'+ ii + '.csv'))
                x_angles_df = pd.DataFrame(self.x_angles)
                y_angles_df = pd.DataFrame(self.y_angles)           
                
                self.paths['LCA'] = os.path.join(self.paths['result'], 'ResultsForLCA') 
                if not os.path.isdir(self.paths['LCA']):
                    os.makedirs(self.paths['LCA'])

                np.save(os.path.join(self.paths['result'], 'monthlyData.npy'), self.monthlyData)
                #self.monthlyData.to_csv(os.path.join(self.paths['result'], 'monthlyData.csv'))
                self.yearlyData.to_csv(os.path.join(self.paths['result'], 'yearlyData.csv'))
                self.totalMonthlyData.to_csv(os.path.join(self.paths['LCA'], 'totalMonthlyEnergyFlow.csv'))
                self.yearlyFlowElec.to_csv(os.path.join(self.paths['LCA'], 'YearlyEnergyFlow.csv'))
                #self.monthlyFlowElec.to_csv(os.path.join(self.paths['result'], 'MonthlyElecFlow.csv'))
                self.monthlyImpactFlow.to_csv(os.path.join(self.paths['LCA'], 'totalMonthlyImpactFlow.csv'))
                x_angles_df.to_csv(os.path.join(self.paths['result'], 'X-Angles.csv'))
                y_angles_df.to_csv(os.path.join(self.paths['result'], 'Y-Angles.csv'))
                
                
                #self.totalMonthlyData = pd.DataFrame.from_dict(self.totalMonthlyData['E_total'])
                #self.yearlyFlowElec = pd.DataFrame.from_dict(self.yearlyFlowElec['E_total']).T
                #self.monthlyImpactFlow = pd.DataFrame.from_dict(self.monthlyImpactFlow['E_total']).T
                
                with open(os.path.join(self.paths['result'], 'MonthlyElecFlow.json'), 'w') as f:
                    f.write(json.dumps(self.monthlyFlowElec))
                
                class NumpyEncoder(json.JSONEncoder):
                    def default(self, obj):
                        if isinstance(obj, np.ndarray):
                            return obj.tolist()
                        return json.JSONEncoder.default(self, obj)

                with open(os.path.join(self.paths['result'], 'monthlyData.json'), 'w') as f:
                    f.write(json.dumps(self.monthlyData, cls=NumpyEncoder))

                #convert heating/cooling system variables into strings			
                self.BuildingProperties["heatingSupplySystem"] = str(self.BuildingProperties["heatingSupplySystem"])
                self.BuildingProperties["coolingSupplySystem"] = str(self.BuildingProperties["coolingSupplySystem"])
                self.BuildingProperties["heatingEmissionSystem"] = str(self.BuildingProperties["heatingEmissionSystem"])
                self.BuildingProperties["coolingEmissionSystem"] = str(self.BuildingProperties["coolingEmissionSystem"])
                self.BuildingProperties["T_start"] = self.SimulationOptions['Temp_start'] 
                self.BuildingProperties["SetBack_H"] = self.SimulationOptions['setBackTempH']
                self.BuildingProperties["SetBack_C"] = self.SimulationOptions['setBackTempC']

                #save building properties in json files
                with open(os.path.join(self.paths['result'], 'BuildingProperties.json'), 'w') as f:
                    f.write(json.dumps(self.BuildingProperties))

                print '\nResults are saved!'    

        print "\nSimulation end: " + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
    
    def SolveASF(self):
        #main method which calls all sub-methods

            self.initializeASF()
            print 'setting parameters'
            self.setBuildingParameters()
            print 'initialising'		
            self.initializeBuildingSimulation()
            self.setPaths()				
            print 'calc variavbles'
            self.CalculateVariables()
            print 'run radiation calc'
            self.runRadiationCalculation()	
            print 'prepare rad data'	  		 
            self.PrepareRadiationData()	
            print 'running simulation'												   
            self.runBuildingSimulation()
            print 'electricity flow'												   
            self.computeElecFlow()
            
            if self.SimulationData['ShowFig'] or self.SimulationData['Save']:   
                self.createAllPlots()
            else:
                self.fig = None 
         
            self.SaveResults()