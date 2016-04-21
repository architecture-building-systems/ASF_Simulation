# -*- coding: utf-8 -*-
"""
Created on Tue Feb 02 14:55:48 2016

functions needed to average hourly DIVA data of a whole year for to monthly hours

@author: Jeremias
"""
import numpy as np


def daysPassedMonth():
    """
    function that returns a list with all the number of days per month and 
    a list with the cumulative number of days passed at the end of the month
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


def sum_monthly(X, daysPassedMonth):
    """
    function that adds data for every month so that each month is represented by 
    a cumulative day with hourly values, where each hour represents the sum of the 
    corresponding hours during that month
    """
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
    
def average_monthly(X, daysPassedMonth, daysPerMonth):
    """
    function that averages data for every month so that each month is represented by 
    an average day with hourly values, where each hour represents the average of the 
    corresponding hours during that month
    """
   
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