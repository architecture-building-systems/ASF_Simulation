# -*- coding: utf-8 -*-
"""
Created on Wed Feb 08 14:35:43 2017

@author: Assistenz
"""

import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import math

plotShow = True
if plotShow == True: 
    fig = plt.figure(figsize=(6, 4))
    
    plt.style.use('seaborn-white')
    
    #Azimuth
    x = np.array([23,23,26,10,10,14,14,0])
    y = np.array([16.,16.09,18.04,7.94,7.99,10.72,10.78,0])
    
    # Our model is y = a * x, so things are quite simple, in this case...
    # x needs to be a column vector instead of a 1D vector for this, however.
    x = x[:,np.newaxis]
    a, _, _, _ = np.linalg.lstsq(x, y)
    
    plt.plot(x, y, 'ro', label='Azimuth')
    plt.plot(x, a*x, 'k-', label='Trendline Azimuth: ' + str(round(a[0],2)))
    
    
    
    #Altitude
    
    x2 = np.array([0,15,22.5,30,37.5])
    y2 = np.array([0,10.03,14.38,19.74,25.98])
    
    # Our model is y = a * x, so things are quite simple, in this case...
    # x needs to be a column vector instead of a 1D vector for this, however.
    x2 = x2[:,np.newaxis]
    a2, _, _, _ = np.linalg.lstsq(x2, y2)
    
    plt.plot(x2, y2, 'yo', label='Altitude')
    plt.plot(x2, a2*x2, 'b-', label='Trendline Altitude: ' + str(round(a2[0],2)))
    
    plt.title('Actuation Energy Demand', fontsize=12)
    plt.xlabel('Angle Range [deg]', fontsize=12)
    plt.ylabel('Energy Demand [mWh/deg]', fontsize=12)
    plt.xticks(range(0,50,10))
    plt.yticks(range(0,40,10))
    
    plt.tight_layout()
    plt.show()
    
    plt.legend(loc=2, numpoints=1, ncol=1, fontsize=12)
    
    print 'Slope', a
    print 'Slope', a2
    






def ActuationDemand (oldX, newX, oldY, newY, PanelNum):

    ZeroPosX = 45
    ZeroPosY = 0
    MaxX = 90
    MinX = 0
    MaxY = 45
    MinY = -45
    
    Slope = 0.67175309 # Altitude
    SlopeY = 0.71685727 # Azimuth
    
    if math.isnan(oldX) and math.isnan(oldY):
        oldX = ZeroPosX
        oldY = ZeroPosY
        
    
    if math.isnan(newX) and math.isnan(newY):
        newX = ZeroPosX
        newY = ZeroPosY
    
#    print 'x'        
#    print 'Neu', newX
#    print 'old', oldX
#    print 'energy', Energy, 'mWh'
#    print 'dif', Energy/Slope
    

    if oldX == ZeroPosX:
        Energy = Slope * abs(newX-oldX) 
    elif newX == ZeroPosX:
        Energy = 0 
    else:   
        if oldX in range(MinX,ZeroPosX):
            Var1 = 'A'
            
        elif oldX in range(ZeroPosX+1,MaxX+1):
            Var1 = 'B'
        
        if newX in range(MinX,ZeroPosX):
            Var2 = 'C'
            
        elif newX in range(ZeroPosX+1,MaxX+1):
            Var2 = 'D'       
                
        if Var1 == 'A' and Var2 == 'C':
            if newX > oldX:
                Energy = Slope * (newX-oldX)
            else:
                Energy = 0
                
        elif Var1 == 'A' and Var2 == 'D':
            Energy = Slope * (newX - ZeroPosX)
        
        elif Var1 == 'B' and Var2 == 'C':
            Energy = Slope * (ZeroPosX -newX) # mWh
            
        elif Var1 == 'B' and Var2 == 'D':
            if newX > oldX:
                Energy = Slope * (newX-oldX)
            else:
                Energy = 0
#    print 'x'        
#    print 'Neu', newX
#    print 'old', oldX
#    print 'energy', Energy, 'mWh'
#    print 'dif', Energy/Slope
    
    
    if oldY == ZeroPosY:
        EnergyY = SlopeY * abs(newY-oldY) 
        
    elif newY == ZeroPosY:
        EnergyY = 0 

    else:   
        if oldY in range(MinY, ZeroPosY):
            Var3 = 'A'
            
        elif oldY in range(ZeroPosY + 1, MaxY + 1):
            Var3 = 'B'
        
        if newY in range(MinY, ZeroPosY):
            Var4 = 'C'
            
        elif newY in range(ZeroPosY + 1, MaxY + 1):
            Var4 = 'D'       
                
        if Var3 == 'A' and Var4 == 'C':
            if abs(newY) > abs(oldY):
                EnergyY = SlopeY * (abs(newY)-abs(oldY))
            else:
                Energy = 0
        elif Var3 == 'A' and Var4 == 'D':
            EnergyY = SlopeY * (newY - ZeroPosY)
        
        elif Var3 == 'B' and Var4 == 'C':
            EnergyY = SlopeY * (ZeroPosY - abs(newY)) # mWh
            
        elif Var3 == 'B' and Var4 == 'D':
            if newY > oldY:
                EnergyY = SlopeY * (newX-oldX)
            else:
                EnergyY = 0
    
    
#    print 'y'        
#    print 'Neu', newY
#    print 'old', oldY
#    print 'energy', EnergyY, 'mWh'
#    print 'dif', EnergyY/SlopeY
    
    #print 'total', (Energy + EnergyY)/1000. * PanelNum, 'Wh/50 Panels'
    
    return round((Energy + EnergyY)/1000. * PanelNum,2)
    
#TnewX = 17
#TnewY = 43
#
#ToldX = np.nan
#ToldY = np.nan
#
#TotalEnergy =  ActuationDemand (oldX = ToldX, newX = TnewX, oldY = ToldY, newY = TnewY, PanelNum = 50)




