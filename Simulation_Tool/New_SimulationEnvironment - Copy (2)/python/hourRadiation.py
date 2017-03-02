# -*- coding: utf-8 -*-
"""
Created on Thu Oct 06 17:05:27 2016

@author:
 Assistenz
"""



import numpy as np

daysPerMonth = np.array([31,28,31,30,31,30,31,31,30,31,30,31])
hoursPerMonth = daysPerMonth*24
hoursPerMonth = [744,  672,  744, 720, 744, 720, 744, 744, 720, 744, 720, 744]
sumHours = [  744,  1416,  2160,  2880,  3624,  4344,  5088,  5832,  6552,  7296,  8016,  8760]


def sumHours(daysPerMonth):
    hoursPerMonth = daysPerMonth*24
    sumHours = np.zeros(12)
    for ii in range(0,len(hoursPerMonth)):
        if ii == 0:    
            sumHours[ii] = hoursPerMonth[ii]
        else:
            sumHours[ii]= sumHours[ii-1]+hoursPerMonth[ii]    
    return sumHours




def hourRadiation(hour_in_month,daysPerMonth):
    
    hourRadiation = []
    for monthi in range(1,13):
        
        for HOD in hour_in_month[monthi]:
            if monthi==1:
                for jj in range(0,daysPerMonth[monthi-1]):
                    hourRadiation.append(HOD+24*jj)
            else:
                for ii in range(0,daysPerMonth[monthi-1]):
                    
                    day = 0
                    for i in range(0,monthi-1):
                        day += daysPerMonth[i]*24
                    day += HOD + 24*ii
                    hourRadiation.append(day)
            

    hourRadiation.sort()

    return hourRadiation

def hourRadiation_calculated(hour_in_month,daysPerMonth):
        
    hourRadiation_calculated = []

    for monthi in range(1,13):
        for HOD in hour_in_month[monthi]:
            if monthi==1:
                hourRadiation_calculated.append(HOD)
            else:
                day = 0
                for i in range(0,monthi-1):  
                    day += daysPerMonth[i]*24
                day += HOD
                hourRadiation_calculated.append(day)
    
        
    return hourRadiation_calculated

