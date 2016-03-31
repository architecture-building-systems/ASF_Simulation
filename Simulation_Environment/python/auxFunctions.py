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