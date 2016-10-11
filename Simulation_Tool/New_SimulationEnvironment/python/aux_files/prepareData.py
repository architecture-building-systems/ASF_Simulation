# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 16:47:05 2016

functions to import and prepare data for post processing

@author: Jeremias
"""

import numpy as np 
import json
from calculate_angles_function import create_ASF_angles  
from auxFunctions import unique, calcDaysPassedMonth, calculate_sum_for_index


def prepareMonthlyRadiatonData(PV_electricity_results, simulationOption):
    """
    input: dictionary with PV_electricity_results, simulationOption dictionary\n
    output: monthly radiation data for post-processing
    """

    # read power for all combinations and hours:
    PV_monthly_list = PV_electricity_results['Pmpp_sum']
    
    # new empty array for pv data:
    PV_monthly_array = np.empty((len(PV_monthly_list)))*np.nan
    
    # multiply the average pv generation by the number of days per month and convert to kWh:
    for i in range(len(PV_monthly_list)):
        PV_monthly_array[i] = PV_monthly_list[i]/1000.*PV_electricity_results['days_per_month'][PV_electricity_results['month'][i/PV_electricity_results['numComb']]-1] #kWh
    
    # resize data, so that it matches the number of combinations and the number of hours:
    PV_monthly_array.resize(PV_electricity_results['numHours'],PV_electricity_results['numComb'])
    
    # transpose array to match thermal and lighting results:
    PV_monthly_array = PV_monthly_array.transpose()
    
    
    if simulationOption['timePeriod'] == '4months' and PV_electricity_results['numHours']<140:
        months = 4
        hour_in_month = []
        month = []
        for i in range(len(PV_electricity_results['month'])):
            if PV_electricity_results['month'][i]==3:
                month.append(1)
                hour_in_month.append(PV_electricity_results['hour_in_month'][i])
            elif PV_electricity_results['month'][i]==6:
                month.append(2)
                hour_in_month.append(PV_electricity_results['hour_in_month'][i])
            elif PV_electricity_results['month'][i]==9:
                month.append(3)
                hour_in_month.append(PV_electricity_results['hour_in_month'][i])
            elif PV_electricity_results['month'][i]==12: 
                month.append(4)
                hour_in_month.append(PV_electricity_results['hour_in_month'][i])
    else:
        months = 12
        month = PV_electricity_results['month']
        hour_in_month = PV_electricity_results['hour_in_month']
        
    TotalHoursPerDay = 24
    TotalHours = (months*TotalHoursPerDay)
    
    # create zero array that includes 24 hours for every month:
    PV_monthly = np.zeros((PV_electricity_results['numComb'],TotalHours))
    
    # fill in the evaluated hours with the data from PV_monthly_array:
    PV_monthly[:,((np.array(month)-1)*24+np.array(hour_in_month)).astype(int)]=PV_monthly_array
    
    
    #  read radiation for all combinations and hours:
    R_monthly_list = PV_electricity_results['Ins_sum']
    
    # new empty array for radiation data:
    R_monthly_array = np.empty((len(R_monthly_list)))*np.nan
    
     # multiply the average radiation by the number of days per month and convert to kWh:
    for i in range(len(R_monthly_list)):
        R_monthly_array[i] = R_monthly_list[i]/1000.*PV_electricity_results['days_per_month'][month[i/PV_electricity_results['numComb']]-1] #kWh

    # resize data, so that it matches the number of combinations and the number of hours:
    R_monthly_array.resize(PV_electricity_results['numHours'],PV_electricity_results['numComb'])
    
    # transpose array to match thermal and lighting results:
    R_monthly_array = R_monthly_array.transpose()            
        
    # create zero array that includes 24 hours for every month:
    R_monthly = np.zeros((PV_electricity_results['numComb'],TotalHours))
    
    # fill in the evaluated hours with the data from R_monthly_array:
    R_monthly[:,((np.array(month)-1)*24+np.array(hour_in_month)).astype(int)]=R_monthly_array
    
    
    
    #  read power for all combinations and hours:
    PV_avg_list = PV_electricity_results['Pmpp_avg']
    
    # new empty array for pv data:
    PV_avg_array = np.empty((len(PV_avg_list)))*np.nan
    
    PV_avg_array = PV_avg_list #W/m2

    # resize data, so that it matches the number of combinations and the number of hours:
    PV_avg_array.resize(PV_electricity_results['numHours'],PV_electricity_results['numComb'])
    
    # transpose array to match thermal and lighting results:
    PV_avg_array = PV_avg_array.transpose()            
        
    # create zero array that includes 24 hours for every month:
    PV_avg = np.zeros((PV_electricity_results['numComb'],TotalHours))
    
    # fill in the evaluated hours with the data from PV_avg_array:
    PV_avg[:,((np.array(month)-1)*24+np.array(hour_in_month)).astype(int)]=PV_avg_array
    
    
    #  read insolation for all combinations and hours:
    Ins_avg_list = PV_electricity_results['Ins_avg']
    
    # new empty array for insolation data:
    Ins_avg_array = np.empty((len(Ins_avg_list)))*np.nan
    
     # multiply the average insolation by the number of days per month and convert to kWh:
    for i in range(len(Ins_avg_list)):
        Ins_avg_array[i] = Ins_avg_list[i] #W/m2

    # resize data, so that it matches the number of combinations and the number of hours:
    Ins_avg_array.resize(PV_electricity_results['numHours'],PV_electricity_results['numComb'])
    
    # transpose array to match thermal and lighting results:
    Ins_avg_array = Ins_avg_array.transpose()            
        
    # create zero array that includes 24 hours for every month:
    Ins_avg = np.zeros((PV_electricity_results['numComb'],TotalHours))
    
    # fill in the evaluated hours with the data from Ins_avg_array:
    Ins_avg[:,((np.array(month)-1)*24+np.array(hour_in_month)).astype(int)]=Ins_avg_array
    
    
    #  read insolation for all combinations and hours:
    Ins_theoretical_list = PV_electricity_results['theoreticalMaxRad']
    
    # new empty array for insolation data:
    Ins_theoretical_array = np.empty((len(Ins_theoretical_list)))*np.nan
    
     # multiply the average insolation by the number of days per month and convert to kWh:
    for i in range(len(Ins_theoretical_list)):
        Ins_theoretical_array[i] = Ins_theoretical_list[i] #W/m2

    # resize data, so that it matches the number of combinations and the number of hours:
    Ins_theoretical_array.resize(PV_electricity_results['numHours'],PV_electricity_results['numComb'])
    
    # transpose array to match thermal and lighting results:
    Ins_theoretical_array = Ins_theoretical_array.transpose()            
        
    # create zero array that includes 24 hours for every month:
    Ins_theoretical = np.zeros((PV_electricity_results['numComb'],TotalHours))
    
    # fill in the evaluated hours with the data from Ins_theoretical_array:
    Ins_theoretical[:,((np.array(month)-1)*24+np.array(hour_in_month)).astype(int)]=Ins_theoretical_array
    
    
    #  read efficiencies for all combinations and hours:
    eff_list = PV_electricity_results['eff_ap']
    
    # new empty array for efficiencies data:
    eff_array = np.empty((len(eff_list)))*np.nan
    
     # multiply the average efficiencies by the number of days per month and convert to kWh:
    for i in range(len(eff_list)):
        eff_array[i] = eff_list[i] #W/m2

    # resize data, so that it matches the number of combinations and the number of hours:
    eff_array.resize(PV_electricity_results['numHours'],PV_electricity_results['numComb'])
    
    # transpose array to match thermal and lighting results:
    eff_array = eff_array.transpose()            
        
    # create zero array that includes 24 hours for every month:
    eff = np.zeros((PV_electricity_results['numComb'],TotalHours))
    
    # fill in the evaluated hours with the data from eff_array:
    eff[:,((np.array(month)-1)*24+np.array(hour_in_month)).astype(int)]=eff_array
    
    # calculate average efficiency at optimum angle combination
    PV_eff_opt = calculate_sum_for_index(PV_monthly, np.argmax(PV_monthly,axis=0))/calculate_sum_for_index(R_monthly, np.argmax(PV_monthly,axis=0))
    
    # select only the four months if requested:
    if simulationOption['timePeriod'] == '4months' and PV_electricity_results['numHours']>96:
        indices4m = np.hstack((range(48,72),range(120,144),range(192,216),range(264,288)))
        PV_monthly = PV_monthly[:,indices4m]
        R_monthly = R_monthly[:,indices4m]
#        PV_eff_opt = PV_eff_opt[:,indices4m]
        Ins_avg = Ins_avg[:,indices4m]
        Ins_theoretical = Ins_theoretical[:,indices4m]
        PV_avg = PV_avg[:,indices4m]
        eff = eff[:,indices4m]
        
    return PV_monthly, R_monthly, PV_eff_opt, Ins_avg, Ins_theoretical, PV_avg, eff
    
def importDIVAresults(path):
    """
    reads heating, cooling and lighting csv files form path as well as json 
    file with the corresponding efficiencies for the simulation \n
    input: path to DIVA results folder \n
    output: dictionary with results
    """
    

    # Import data from csv
    C=np.genfromtxt(path + '\cooling.csv',delimiter=',')
    H=np.genfromtxt(path + '\heating.csv',delimiter=',')
    L=np.genfromtxt(path + '\lighting.csv',delimiter=',')
    
    for i in range(1,100):
        try:
            C = np.concatenate((C, np.genfromtxt(path + '\cooling' + str(i) + '.csv',delimiter=',')), axis=0)
            H = np.concatenate((H, np.genfromtxt(path + '\heating' + str(i) + '.csv',delimiter=',')), axis=0)
            L = np.concatenate((L, np.genfromtxt(path + '\lighting' + str(i) + '.csv',delimiter=',')), axis=0)
        except:
            pass
    
    with open(path + '\efficiencies.json', 'r') as fp:
        efficiencies = json.load(fp)
        fp.close()
        
    if np.shape(C)[0]==8760:
        C = np.expand_dims(C, axis=0)
        H = np.expand_dims(H, axis=0)
        L = np.expand_dims(L, axis=0)
    # Calculate the total Energy Consumption
    E=C+H+L
    
    # write data to dictionary:
    DIVA_results = {'H':H, 'C':C, 'L':L, 'E':E, 'efficiencies':efficiencies, 'efficienciesChanged':False}
    
    return DIVA_results
    
def readLayoutAndCombinations(path):
    """
    reads and executes LayoutAndCombinations.txt file \n
    input: path to results folder \n
    output: dictionary with LayoutAndCombinations
    """
    
    # import parameters used for simulation:
    with open(path + '\LayoutAndCombinations.txt', 'rb') as f:
        parameters = f.readlines()
        f.close()
    
    # execute all lines of the file:
    for i in range(len(parameters)):
        exec parameters[i]
    
    # save parameters to dictionary
    LayoutAndCombinations = {'Xangles':XANGLES, 'Yangles':YANGLES, 'NoClusters':NoClusters, 'panelSize':panelSize, 'panelSpacing':panelSpacing, 'ASFarray':ASFarray, 'desiredGridPointSize':desiredGridPointSize}
   
    return LayoutAndCombinations
   
   
def CalcXYAnglesAndLocation(LayoutAndCombinations):
    """
    calculates the x and y angles and their corresponding combination
    input: dict of LayoutAndCombinations
    output: dict with angles and combinations
    """        
    ASFarray, XANGLES, YANGLES, NoClusters = LayoutAndCombinations['ASFarray'], LayoutAndCombinations['Xangles'], LayoutAndCombinations['Yangles'], LayoutAndCombinations['NoClusters']
    allAngles = create_ASF_angles(ASFarray, XANGLES, YANGLES, NoClusters)
    
    #make NoClusters an integer:
    NoClusters = int(NoClusters)        
    
    # create list with all angles:
    new_list = []
    
    for i in range(len(allAngles[0])):
        new_list.append([])
        for j in range(NoClusters):
            new_list[i].append(allAngles[j][i])
    
    # calculate x-angles
    x_angles=[]
    for i in range(len(new_list)):
        x_angles.append([])
        for j in range(NoClusters):
            x_angles[i].append(new_list[i][j][0])
        x_angles[i] = tuple(x_angles[i])
    x_angles_full = x_angles
    x_angles = unique(x_angles)
    
    # find x angle location
    x_angle_location=[]
    for i in range(len(x_angles_full)):
        x_angle_location.append(0)
        x_angle_location[i]=x_angles.index(x_angles_full[i])
            
    # calculate y-angles:
    y_angles=[]
    for i in range(len(new_list)):
        y_angles.append([])
        for j in range(NoClusters):
            y_angles[i].append(new_list[i][j][1])
        y_angles[i] = tuple(y_angles[i])
    y_angles_full = y_angles
    y_angles = unique(y_angles)
    
    # find y angle location
    y_angle_location=[]
    for i in range(len(y_angles_full)):
        y_angle_location.append(0)
        y_angle_location[i]=y_angles.index(y_angles_full[i])
        
    SimulationAngles = {'allAngles':allAngles, 'x_angles':x_angles, 'x_angles_full':x_angles_full, 'x_angle_location':x_angle_location, 'y_angles':y_angles, 'y_angles_full':y_angles_full, 'y_angle_location':y_angle_location}
    return SimulationAngles
    


    

def sum_monthly(X, options=None):
    """
    function that adds data for every month
    input: numpy array with yearly data, options to only look at certain months
    output: numpy array with summed up monthly data
    """    
    # get days per month and added up days per month:
    daysPassedMonth, daysPerMonth = calcDaysPassedMonth()
    

    NumberCombinations = np.shape(X)[0]
    X_sum=np.zeros((NumberCombinations, 24*12))
    for combination in range(NumberCombinations):
        #dayi=0
        monthi=0
        #testmonth=[]
        for day in range(365):
            for hour in range(24):
                X_sum[combination][monthi*24+hour]+=X[combination][day*24+hour]
                if day == daysPassedMonth[monthi]:
                    monthi+=1
                    
    
    if options['timePeriod'] == '4months':
        indices = np.hstack((range(48,72),range(120,144),range(192,216),range(264,288)))
        X_sum = X_sum[:,indices]

    return X_sum
#            testmonth.append(monthi)
        
    
    
def average_monthly(X):
    """
    function that averages data for every month
    input: numpy array with yearly data
    output: numpy array with averaged up monthly data
    """    
    # get days per month and added up days per month:
    daysPassedMonth, daysPerMonth = calcDaysPassedMonth()
    
    NumberCombinations = np.shape(X)[0]
    X_average=np.zeros((NumberCombinations, 24*12))
    for combination in range(NumberCombinations):
        #dayi=0
        monthi=0
        #testmonth=[]
        for day in range(365):
            for hour in range(24):
                X_average[combination][monthi*24+hour]+=X[combination][day*24+hour]/daysPerMonth[monthi]
                if day == daysPassedMonth[monthi]:
                    monthi+=1
    return X_average
  
def changeDIVAresults(DIVA_results, efficiencyChanges):
    """
    function to change DIVA data according to efficiencyChanges
    """
    
    if DIVA_results['efficienciesChanged']:
        print 'efficiencies were already changed, they will not be changed again'
        
    elif not DIVA_results['efficienciesChanged']:
        print 'changing DIVA efficiencies'
        DIVA_results['H'] = DIVA_results['H']*DIVA_results['efficiencies']['H_COP']/efficiencyChanges['H_COP']
        DIVA_results['C'] = DIVA_results['C']*DIVA_results['efficiencies']['C_COP']/efficiencyChanges['C_COP']
        DIVA_results['L'] = DIVA_results['L']*efficiencyChanges['L_Load']/DIVA_results['efficiencies']['L_Load']
        DIVA_results['E'] = DIVA_results['H'] + DIVA_results['C'] + DIVA_results['L']
        DIVA_results['efficienciesChanged'] = True
        DIVA_results['efficiencyChanges'] = efficiencyChanges
        
        return DIVA_results

    else:
        print 'warning: efficienciesChanged not defined in DIVA_results'
        
    
# test functions:
#asdf = sum_monthly(DIVA_results['C'])
#asdf = CalcXYAnglesAndLocation(DIVA_results['LayoutAndCombinations'])
#asdf = readLayoutAndCombinations(diva_path)
# DIVA_results = importDIVAresults(diva_path)
#pv, r  = prepareMonthlyRadiatonData(PV_electricity_results)