# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 11:26:40 2016

Calculate hour of the year based on date input

@author: Jeremias
"""

# import days per month
path = "C:/Users/Assistenz/ASF_Simulation/Python/"
filename = "days_per_month.csv"
daysPerMonth=np.genfromtxt(path + filename, delimiter=',')
daysPerMonth=np.asarray(daysPerMonth, dtype='int32')

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
    