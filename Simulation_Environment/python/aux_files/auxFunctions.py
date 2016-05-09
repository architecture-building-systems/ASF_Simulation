# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 18:32:12 2016

auxiliary functions that may be used in different contexts

@author: Jeremias
"""

import numpy as np


def unique(items):
    """
    function to make items unique in a list (represent every angle combination)
    """
    found = set([])
    keep = []

    for item in items:
        if item not in found:
            found.add(item)
            keep.append(item)

    return keep
    

def calcDaysPassedMonth():
    """
    function that sums up the days of the previous month
    """
    daysPerMonth = np.array([31,28,31,30,31,30,31,31,30,31,30,31])
    #hoursPerMonth = daysPerMonth*24
    daysPassedMonth = []
    for i in range(12):
        if i == 0:
            daysPassedMonth.append(daysPerMonth[i])
        else:
            daysPassedMonth.append(daysPerMonth[i]+daysPassedMonth[i-1])
            
    return daysPassedMonth, daysPerMonth
    
    
def calculate_sum_for_index(X,Xind):
    """
    function that calculates the sum of a two dimensional array X for a specific
    index or index-list
    """
    Xsum = []
    
    if not np.shape(Xind)==():
        for i in range(len(Xind)):
            Xsum.append(X[Xind[i]][i])
            sumX = np.sum(Xsum)
    else:
        if not Xind==None:
            sumX = np.sum(X[Xind])
        else:
            sumX = np.nan
    return sumX
    
def create_evalList(dataType, month, startHour, endHour):
    """
    example: \n
    create_evalList('monthly', 6, 12, 13) \n
    outputs a list which corresponds to the monthly data of june for hours between 11:00 and 13:00. 
    Note that month, startHour and endHour correspond to a counter value that starts with 1.
    """
    if dataType == 'monthly':
        evalList=[]
        for i in range(endHour-(startHour-1)):
            evalList.append((month-1)*24 + startHour - 1 + i)
    else:
        raise ValueError("dataType: "+str(dataType)+" not (yet) implemented")
        
    return evalList
    
def changeMonthlyDataFunction(monthlyData, DataRows):
    """
    function to only select certain rows from monthlyData
    """
    newMonthlyData = {}
    for i in ['C','E_HCL','E_tot', 'H', 'L', 'R', 'PV', 'PV_avg', 'PV_eff', 'R_avg', 'R_theo']:

        newMonthlyData[i] = monthlyData[i][DataRows]
        
    for i in ['changedEfficiency','efficiencies']:
        
        newMonthlyData[i] = monthlyData[i]
    
    newMonthlyData['angles'] = {}
    
    for i in ['x_angle_location', 'x_angles_full', 'y_angle_location', 'y_angles_full']:
        
        newMonthlyData['angles'][i] = []
        
        for ii in DataRows:
            newMonthlyData['angles'][i].append(monthlyData['angles'][i][ii])
        
#     # find x angle location
#    x_angle_location=[]
#    for i in range(len(x_angles_full)):
#        x_angle_location.append(0)
#        x_angle_location[i]=x_angles.index(x_angles_full[i])
        
    
            
    newMonthlyData['angles']['allAngles']=[[]]
    for i in DataRows:
        newMonthlyData['angles']['allAngles'][0].append(monthlyData['angles']['allAngles'][0][i])
        
    newMonthlyData['angles']['x_angles'] = unique(newMonthlyData['angles']['x_angles_full'])
    newMonthlyData['angles']['y_angles'] = unique(newMonthlyData['angles']['y_angles_full'])
    
    for i in range(len(DataRows)):
        newMonthlyData['angles']['x_angle_location'][i]=newMonthlyData['angles']['x_angles'].index(newMonthlyData['angles']['x_angles_full'][i])
        newMonthlyData['angles']['y_angle_location'][i]=newMonthlyData['angles']['y_angles'].index(newMonthlyData['angles']['y_angles_full'][i])
    
        
    
        
        
    return newMonthlyData