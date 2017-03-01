# -*- coding: utf-8 -*-
"""
Created on Tue Mar 08 10:46:36 2016

@author: Assistenz
"""

import numpy as np
import matplotlib.pyplot as plt
import json

path = "C:/Users/Assistenz/Documents/MT_Jeremias/Simulation_Data/RadiationEvaluation/"

SunAngles=np.genfromtxt(path + 'SunPosition.csv',delimiter=',', skiprows = 1)


asfSunTracking = np.empty((3,4400))
asfSunTracking[:] = np.NAN

asfSunTracking[0,:]=SunAngles[0]
asfSunTracking[1,:]=SunAngles[1]

counter = 0
AzimuthSouth = -(SunAngles[2]-180)

for i in range(len(AzimuthSouth)):
    
    if AzimuthSouth[i]>45:
        asfSunTracking[2,i] = 45
    elif AzimuthSouth[i]< -45:
        asfSunTracking[2,i] = -45
    else:
        asfSunTracking[2,i] = AzimuthSouth[i]
#
#AzimuthSunRad = AzimuthSouth*np.pi/180
#AltitudeSunRad = np.pi/2-SunAngles[1]*np.pi/180
##AzimuthASFRad = asfSunTracking[2,:]*np.pi/180
#AzimuthASFRad = np.empty((4400))
#AzimuthASFRad[:] = np.NAN
#AltitudeASFRad = AltitudeSunRad
#
##c1 = np.sin(AltitudeSunRad[i])*np.cos(AzimuthSunRad[i])*np.cos(AzimuthASFRad[i]) + np.sin(AltitudeSunRad[i])*np.sin(AzimuthSunRad[i])*np.sin(AzimuthASFRad[i])
##c2 = np.cos(AltitudeSunRad[i])
##
##AltitudeASFRad = 2*np.arctan((np.sqrt(c1**2 +c2**2)-c2)/c1)
#
#for i in range(len(AzimuthSunRad)):
#    
#    if AzimuthSunRad[i]>np.pi/4:
#        AzimuthASFRad[i] = np.pi/4
#        c1 = np.sin(AltitudeSunRad[i])*np.cos(AzimuthSunRad[i])*np.cos(AzimuthASFRad[i]) + np.sin(AltitudeSunRad[i])*np.sin(AzimuthSunRad[i])*np.sin(AzimuthASFRad[i])
#        c2 = np.cos(AltitudeSunRad[i])
#        AltitudeASFRad[i] = 2*np.arctan((np.sqrt(c1**2 +c2**2)-c2)/c1)
#        
#    elif AzimuthSunRad[i]< -np.pi/4:
#        AzimuthASFRad[i] = -np.pi/4
#        c1 = np.sin(AltitudeSunRad[i])*np.cos(AzimuthSunRad[i])*np.cos(AzimuthASFRad[i]) + np.sin(AltitudeSunRad[i])*np.sin(AzimuthSunRad[i])*np.sin(AzimuthASFRad[i])
#        c2 = np.cos(AltitudeSunRad[i])
#        AltitudeASFRad[i] = 2*np.arctan((np.sqrt(c1**2 +c2**2)-c2)/c1)
#        
#    else:
#        AzimuthASFRad[i] = AzimuthSunRad[i]
#        
        
execfile("calculateHOY.py")

allHours = np.ones(288)
HoursToEvaluateInMonth = []
for i in range(12):
    allHours[24*i:24*i+24] = range(int(MiddleOfMonth[i]),int(MiddleOfMonth[i]+24))
    HoursToEvaluateInMonth.append([])
    
HoursToEvaluate = []
XanglesTracking = []
YanglesTracking = []
#HoursToEvaluateInMonth = []
for i in allHours:
    
    if i in asfSunTracking[0,:]:
        HoursToEvaluate.append(i)
        ind = np.where(asfSunTracking[0,:]==i)[0][0]
        YanglesTracking.append(asfSunTracking[2,ind])
        XanglesTracking.append(asfSunTracking[1,ind])

monthi = 0
for hour in HoursToEvaluate:
    if hour>MiddleOfMonth[monthi][0]+24:
        monthi += 1
    HoursToEvaluateInMonth[monthi].append(hour-MiddleOfMonth[monthi][0])
    
    if hour<MiddleOfMonth[monthi][0]:
        monthi += 1
    
SunTrackingData = {'HOY': HoursToEvaluate, 'Xangles': XanglesTracking, 'Yangles': YanglesTracking, 'HoursInMonth' : HoursToEvaluateInMonth}

with open('SunTrackingData.json', 'w') as fp:
    json.dump(SunTrackingData, fp)
    fp.close()
#plt.figure()
#plt.plot(range(len(AzimuthASFRad)),AzimuthASFRad)