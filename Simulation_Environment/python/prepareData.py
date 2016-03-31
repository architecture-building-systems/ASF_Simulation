# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 16:47:05 2016

functions to import and prepare data for post processing

@author: Jeremias
"""

import numpy as np 
from calculate_angles_function import create_ASF_angles  
from auxFunctions import unique, calcDaysPassedMonth


def prepareMonthlyRadiatonData(PV_electricity_results):
    """
    input: dictionary with PV_electricity_results \n
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
    
    months = 12
    TotalHoursPerDay = 24
    TotalHours = (months*TotalHoursPerDay)
    
    # create zero array that includes 24 hours for every month:
    PV_monthly = np.zeros((PV_electricity_results['numComb'],TotalHours))
    
    # fill in the evaluated hours with the data from PV_monthly_array:
    PV_monthly[:,((np.array(PV_electricity_results['month'])-1)*24+np.array(PV_electricity_results['hour_in_month'])).astype(int)]=PV_monthly_array
    

    #  read radiation for all combinations and hours:
    R_monthly_list = PV_electricity_results['Ins_sum']
    
    # new empty array for radiation data:
    R_monthly_array = np.empty((len(R_monthly_list)))*np.nan
    
     # multiply the average radiation by the number of days per month and convert to kWh:
    for i in range(len(R_monthly_list)):
        R_monthly_array[i] = R_monthly_list[i]/1000.*PV_electricity_results['days_per_month'][PV_electricity_results['month'][i/PV_electricity_results['numComb']]-1] #kWh

    # resize data, so that it matches the number of combinations and the number of hours:
    R_monthly_array.resize(PV_electricity_results['numHours'],PV_electricity_results['numComb'])
    
    # transpose array to match thermal and lighting results:
    R_monthly_array = R_monthly_array.transpose()            
    
    months = 12
    TotalHoursPerDay = 24
    TotalHours = (months*TotalHoursPerDay)
    
    # create zero array that includes 24 hours for every month:
    R_monthly = np.zeros((PV_electricity_results['numComb'],TotalHours))
    
    # fill in the evaluated hours with the data from R_monthly_array:
    R_monthly[:,((np.array(PV_electricity_results['month'])-1)*24+np.array(PV_electricity_results['hour_in_month'])).astype(int)]=R_monthly_array
    
    return PV_monthly, R_monthly
    
def importDIVAresults(path):
    """
    reads heating, cooling and lighting csv files form path \n
    input: path to DIVA results folder \n
    output: dictionary with results
    """
    

    # Import data from csv
    C=np.genfromtxt(path + '\cooling.csv',delimiter=',')
    H=np.genfromtxt(path + '\heating.csv',delimiter=',')
    L=np.genfromtxt(path + '\lighting.csv',delimiter=',')
    
    # Calculate the total Energy Consumption
    E=C+H+L
    
    # write data to dictionary:
    DIVA_results = {'H':H, 'C':C, 'L':L,'E':E}
    
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
    LayoutAndCombinations = {'Xangles':XANGLES, 'Yangles':YANGLES, 'NoClusters':NoClusters, 'panelSize':panelSize, 'panelSpacing':panelSpacing, 'ASFarray':ASFarray}
   
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
    

def sum_monthly(X):
    """
    function that adds data for every month
    input: numpy array with yearly data
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
  

# test functions:
#asdf = sum_monthly(DIVA_results['C'])
#asdf = CalcXYAnglesAndLocation(DIVA_results['LayoutAndCombinations'])
#asdf = readLayoutAndCombinations(diva_path)
# DIVA_results = importDIVAresults(diva_path)
#pv, r  = prepareMonthlyRadiatonData(PV_electricity_results)