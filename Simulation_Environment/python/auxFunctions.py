# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 18:32:12 2016

auxiliary functions that may be used in different contexts

@author: Jeremias
"""

import numpy as np

# define function to make items unique in a list (represent every angle combination)
def unique(items):
    found = set([])
    keep = []

    for item in items:
        if item not in found:
            found.add(item)
            keep.append(item)

    return keep
    
# function that sums up the days of the previous month:
def calcDaysPassedMonth():
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
    Xsum = []
    
    if not np.shape(Xind)==():
        for i in range(len(Xind)):
            Xsum.append(X[Xind[i]][i])
            sumX = np.sum(Xsum)
    else:
        sumX = np.sum(X[Xind])
        
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