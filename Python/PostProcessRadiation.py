# -*- coding: utf-8 -*-
"""
Created on Tue Jan 05 17:25:56 2016

Post process the radiation evaluation results 

options 'year' and 'week' of import option not working automaticaly - to be done if needed


@author: Jeremias Schmidli
"""

import numpy as np
import math
import matplotlib.pyplot as plt

#define if data should be imported, set False if desired radiation data is already in workspace:
importDataFlag = True
importDataOption = 'monthly' #'year', 'week', 'monthly'

if importDataFlag:
    if importDataOption == 'year':
        from ImportRadiationResults import import_radiation, import_radiation_year, import_radiation_monthly, add_hours_without_sun, create_npArray_with_total_Radiation
        
        # define path and filename:
        path = "C:/Users/Assistenz/Documents/MT_Jeremias/Simulation_Data/RadiationEvaluation/Radiation_yearly_25_angles/"
        filename = 'RadiationResults'
        start_combination = 9
        end_combination = 24
        panelSize = 400.0
        numberOfPanels = 50
        R_2=[]
        
        R = create_npArray_with_total_Radiation(Radiation,panelSize,numberOfPanels,'year')
        
        for i in range(start_combination, end_combination+1):
                
            iterateFile = filename + str(i) + '.csv'
            print 'importing file ' + iterateFile
            RadiationData, missingIteration, IterationNumbers, header =  import_radiation_year(path, iterateFile)
            iterateRad = add_hours_without_sun(RadiationData, sunRisen)
            R_i = create_npArray_with_total_Radiation(iterateRad,panelSize,numberOfPanels,'year')
            if i==start_combination:
                R_2 = R_i
            else:
                R_2 = np.append(R_2,R_i, axis=0)
            
            R_tot = np.append(R,R_2,axis=0)
        
        #calculate PV energy production with average efficiency:
        efficiency = 0.1
        PV = R_tot*efficiency
        
        E_withPV = C+H+L-PV
        # load simulation data:
        #Radiation, total_radiation, panel_size = import_radiation(path, filename) 
    elif importDataOption == 'week':
        from ImportRadiationResults import import_radiation, import_radiation_week, add_hours_without_sun, create_npArray_with_total_Radiation
        
        # define path and filename:
        path = "C:/Users/Assistenz/Documents/MT_Jeremias/Simulation_Data/RadiationEvaluation/Results_25_comb_1_week_july/"
        filename = 'RadiationResults'
        hoursFile = 'CHE_Geneva.067000_IWEC_HoursThatSunIsRisen_July_20_to_July_26.csv'
        start_combination = 0
        end_combination = 24
        panelSize = 400.0
        R_week=[]
        
        #R = create_npArray_with_total_Radiation(Radiation,panelSize,numberOfPanels)
        
        for i in range(start_combination, end_combination+1):
                
            iterateFile = filename + str(i) + '.csv'
            print 'importing file ' + iterateFile
            RadiationDataWeek, missingIteration, IterationNumbers, header =  import_radiation_week(path, iterateFile)
#            hoursEvaluated = np.genfromtxt(path + 'CHE_Geneva.067000_IWEC_HoursThatSunIsRisen_July_20_to_July_26.csv',delimiter=',')            
#            hoursEvaluated = hoursEvaluated.astype(int)        
#            allHours = [0]*8760
#            for i in hoursEvaluated:
#                allHours[i-1]=1
                
            iterateRad = add_hours_without_sun(RadiationDataWeek, allHours)
            R_i = create_npArray_with_total_Radiation(iterateRad,panelSize,numberOfPanels)
            if i==start_combination:
                R_week = R_i
            else:
                R_week = np.append(R_week,R_i, axis=0)
            
            #R_tot = np.append(R,R_2,axis=0)
        
        #calculate PV energy production with average efficiency:
        efficiency = 0.1
        PV = R_tot*efficiency
        
        E_withPV = C+H+L-PV
        # load simulation data:
        #Radiation, total_radiation, panel_size = import_radiation(path, filename) 
        
    elif importDataOption == 'monthly':
        from ImportRadiationResults import import_radiation, import_radiation_monthly, add_hours_without_sun, create_npArray_with_total_Radiation
        
        # define path and filename:
        path = 'C:/Users/Assistenz/Documents/MT_Jeremias/Simulation_Data/RadiationEvaluation/Radiation_monthly_25_angles/'
        filename = 'RadiationResults'
        #hoursFile = 'CHE_Geneva.067000_IWEC_HoursThatSunIsRisen_July_20_to_July_26.csv'
        startHour=4
        endHour=22
        start_combination = 0
        end_combination = 24
        panelSize = 400.0
        numberOfPanels = 50
        months = 12
        TotalHoursPerDay = 24
        R_monthly=[]
        
        #R = create_npArray_with_total_Radiation(Radiation,panelSize,numberOfPanels)
        
        for i in range(start_combination, end_combination+1):
                
            iterateFile = filename + str(i) + '.csv'
            print 'importing file ' + iterateFile
            RadiationDataMonthly, missingIteration, IterationNumbers, header =  import_radiation_monthly(path, iterateFile)
   
            allHours = [0]*(months*TotalHoursPerDay)
            for month in range(months):
                for hour in range(TotalHoursPerDay):
                    if hour>=startHour and hour<endHour:
                        allHours[month*TotalHoursPerDay +hour] = 1
                
            iterateRad = add_hours_without_sun(RadiationDataMonthly, allHours)
            R_i = create_npArray_with_total_Radiation(iterateRad,panelSize,numberOfPanels,'monthly')
            if i==start_combination:
                R_monthly = R_i
            else:
                R_monthly = np.append(R_monthly,R_i, axis=0)
            
            #R_tot = np.append(R,R_2,axis=0)
        
        #calculate PV energy production with average efficiency:
        efficiency = 0.08*0.9
        PV_month = R_monthly*efficiency
        
        #this is not a very nice solution but unfortunately month and monthly ar not consistently differentiated:
        R_month = R_monthly
        
#        E_month_withPV = C_month+H_month+L_month-PV_month
        # load simulation data:
        #Radiation, total_radiation, panel_size = import_radiation(path, filename)
    
    else:
        raise ValueError('unable to read importDataOption!')
        
#this analysis was developed for yearly option, which is currently not under further developement:
if importDataOption == 'year':
    
    averageRadiation = []
    for i in Radiation:
        averageRadiation.append(np.sum(i)/len(i))
    
    #plot average radiation for each panel:
    #plt.rc('text', usetex=False)
    #plt.rc('font', family='serif')
    plt.plot(range(0,len(averageRadiation)),averageRadiation, 'bo')
    plt.title('Average Radiation on Panels', size = 20)
    plt.xticks(range(0,len(averageRadiation)),range(1,len(averageRadiation)+1))
    plt.xlabel(r'panel number',size=16)
    plt.ylabel(r'average radiation on panel $\left[\frac{kWh}{m^2 year}\right]$', size=16)
    plt.grid(b=True, which='both')
    
    #calculate total radiation:
    totRadCal=sum(averageRadiation)*(panel_size/1000)**2

    #compare ladybug total radiation with own calculation:
    print 'total radiation calculated by ladybug:', total_radiation, 'kWh/year'
    print 'total radiation calculated based on evaluation of all results: ',  totRadCal, 'kWh/year'