# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 11:26:40 2016

Calculate hour of the year based on date input

@author: Jeremias
"""
import numpy as np

# define days per month:
daysPerMonth = np.array([31,28,31,30,31,30,31,31,30,31,30,31])

month = 3
day = 11
hour = 1

def calcHOY(month, day, hour, daysPerMonth):
    HOY = 0
    for i in range(month-1):
        HOY += daysPerMonth[i]*24
    HOY +=(day-1)*24+hour
    return HOY
    
HOY = calcHOY(month, day, hour, daysPerMonth)
    
MiddleOfMonth=np.ones((12,1))

for i in range(1,13):
    MiddleOfMonth[i-1]=calcHOY(i,int(np.round(daysPerMonth[i-1]/2.0)),1,daysPerMonth)
    print 'use day ' + str(int(np.round(daysPerMonth[i-1]/2.0))) + ' for month ' + str(i)