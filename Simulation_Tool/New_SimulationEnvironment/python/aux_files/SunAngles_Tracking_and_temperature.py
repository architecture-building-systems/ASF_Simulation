# -*- coding: utf-8 -*-
"""
Created on Tue Mar 08 10:46:36 2016

Script to calculate sun-tracking-angles and temperatures for evaluation of 
average days for every month. corresponding data is generated in grasshopper. 

@author: Jeremias
"""

import numpy as np
import json

from average_monthly import average_monthly, daysPassedMonth
from calculateHOY import calcHOY

# set path equal to the one defined in main.py script:
location_path = paths['geo']

#import temperature:
Temperature=np.genfromtxt(os.path.join(location_path,'Temperature.csv'),delimiter=',', skip_header = 2)

#average temperature for every month:
Temperature = Temperature[np.newaxis, :]
daysPassedMonth, daysPerMonth = daysPassedMonth()
Temp_month = average_monthly(Temperature, daysPassedMonth, daysPerMonth)

#import sun angle data:
SunAngles=np.genfromtxt(os.path.join(location_path,'SunPosition.csv'),delimiter=',', skip_header = 1)

#create np.array with asf angles
asfSunTracking = np.empty(np.shape(SunAngles))
asfSunTracking[:] = np.NAN
asfSunTracking[0,:]=SunAngles[0]
asfSunTracking[1,:]=SunAngles[1]

counter = 0

#adjust for different angle convention:
AzimuthSouth = -(SunAngles[2]-180)

#include limit on azimuth angles:
for i in range(len(AzimuthSouth)):
    
    if AzimuthSouth[i]>45:
        asfSunTracking[2,i] = 45
    elif AzimuthSouth[i]< -45:
        asfSunTracking[2,i] = -45
    else:
        asfSunTracking[2,i] = AzimuthSouth[i]

# Find Hours that correspond to the middle of the month:
MiddleOfMonth=np.ones((12,1))
for i in range(1,13):
    MiddleOfMonth[i-1]=calcHOY(i,int(np.round(daysPerMonth[i-1]/2.0)),1)
    print 'use day ' + str(int(np.round(daysPerMonth[i-1]/2.0))) + ' for month ' + str(i)
    

# Create array with all hours of middle day for each month
allHours = np.ones(288)
HoursToEvaluateInMonth = []
for i in range(12):
    allHours[24*i:24*i+24] = range(int(MiddleOfMonth[i]),int(MiddleOfMonth[i]+24))
    HoursToEvaluateInMonth.append([])
    
# Assign Angles and corresponding hour for middle day of the month when sun is risen:
HoursToEvaluate = []
XanglesTracking = []
YanglesTracking = []
for i in allHours:
    if i in asfSunTracking[0,:]:
        HoursToEvaluate.append(i)
        ind = np.where(asfSunTracking[0,:]==i)[0][0]
        YanglesTracking.append(asfSunTracking[2,ind])
        XanglesTracking.append(asfSunTracking[1,ind])

# Create List with sub-lists for each month that holds evaluated hours of day
monthi = 0
for hour in HoursToEvaluate:
    if hour>MiddleOfMonth[monthi][0]+24:
        monthi += 1
    HoursToEvaluateInMonth[monthi].append(hour-MiddleOfMonth[monthi][0])
    
    if hour<MiddleOfMonth[monthi][0]:
        monthi += 1
    
# create lists with hours of day and month corresponding to each angle in list: 
HoursInMonthTracking = []
MonthTracking = []
monthi=1
for i in HoursToEvaluateInMonth:
    HoursInMonthTracking += i
    for j in i:
        MonthTracking.append(monthi)
    monthi+=1
    
# find average temperature corresponding to hours evaluated
TempTracking = []
for idx, month in enumerate(MonthTracking):
    TempTracking.append(Temp_month[0,(month-1)*24+HoursInMonthTracking[idx]-1])

# save everything to dictionary
SunTrackingData = {'HOY': HoursToEvaluate, 'Xangles': XanglesTracking, 'Yangles': YanglesTracking, 'HoursInMonth' : HoursToEvaluateInMonth, 'MonthTracking': MonthTracking, 'HoursInMonthTracking': HoursInMonthTracking, 'TempTracking' : TempTracking}

# save dictionary with json:
with open(os.path.join(location_path ,'SunTrackingData.json'), 'w') as fp:
    json.dump(SunTrackingData, fp)
    fp.close()

#save temperature to seperate json:
with open(os.path.join(location_path ,'TempTracking.json'), 'w') as fp:
    json.dump(TempTracking, fp)
    fp.close()

# clear all variables from memory except for SunTrackingData
del location_path, Temperature, daysPassedMonth, daysPerMonth, Temp_month, SunAngles, asfSunTracking, counter, AzimuthSouth, MiddleOfMonth, allHours, HoursToEvaluateInMonth, HoursToEvaluate, XanglesTracking, YanglesTracking, HoursInMonthTracking, MonthTracking, monthi, TempTracking, i, j, idx, ind, month, hour 