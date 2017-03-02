# -*- coding: utf-8 -*-
"""
Created on Wed Feb 08 14:35:43 2017

@author: Assistenz
"""

import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import math

plotShow = False
if plotShow == True: 
    fig = plt.figure(figsize=(8, 4))
    
    plt.style.use('seaborn-white')
    
    #Azimuth
    x = np.array([23,23,26,10,10,14,14,0])
    y = np.array([16.,16.09,18.04,7.94,7.99,10.72,10.78,0])
    
    # Our model is y = a * x, so things are quite simple, in this case...
    # x needs to be a column vector instead of a 1D vector for this, however.
    x = x[:,np.newaxis]
    a, _, _, _ = np.linalg.lstsq(x, y)
    
    plt.plot(x, y, 'ro', label='Azimuth')
    plt.plot(x, a*x, 'k-', label='y = ' + str(round(a[0],2)) +'x, R**2 = 0.9873')
    
    
    
    #Altitude
    
    x2 = np.array([0,15,22.5,30,37.5])
    y2 = np.array([0,10.03,14.38,19.74,25.98])
    
    # Our model is y = a * x, so things are quite simple, in this case...
    # x needs to be a column vector instead of a 1D vector for this, however.
    x2 = x2[:,np.newaxis]
    a2, _, _, _ = np.linalg.lstsq(x2, y2)
    
    plt.plot(x2, y2, 'yo', label='Altitude')
    plt.plot(x2, a2*x2, 'b-', label='y = ' + str(round(a2[0],2)) + 'x , R**2 = 0.9965')
    
    #plt.title('Actuation Energy Demand', fontsize=12)
    plt.xlabel('Angle [deg]', fontsize=12)
    plt.ylabel('Energy Demand [mWh/deg]', fontsize=12)
    plt.xticks(range(0,50,10))
    plt.yticks(range(0,40,10))
    
    plt.tight_layout()
    plt.show()
    
    plt.legend(loc=2, numpoints=1, ncol=1, fontsize=12)
    
    path = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\PlotMidTerm'
    fig.savefig(path + '\\ActuationEnergyDemand.png')
    
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
        oldX = 0
        oldY = -45
        
    
    if math.isnan(newX) and math.isnan(newY):
        newX = 0
        newY = -45
    
#    print 'x'        
#    print 'Neu', newX
#    print 'old', oldX
#    print 'energy', Energy, 'mWh'
#    print 'dif', Energy/Slope
    

    if oldX == ZeroPosX:
        Energy = Slope * abs(newX-oldX) 
        
    elif newX == ZeroPosX or newX == oldX:
        Energy = 0

    else:   
        if oldX in range(MinX,ZeroPosX) and newX in range(MinX,ZeroPosX):
            if newX > oldX:
                Energy = Slope * (newX-oldX)
            else:
                Energy = 0
        elif oldX in range(MinX,ZeroPosX) and newX in range(ZeroPosX+1,MaxX+1):
            Energy = Slope * (newX - ZeroPosX)
        
        elif oldX in range(ZeroPosX+1,MaxX+1) and newX in range(MinX,ZeroPosX):
            Energy = Slope * (ZeroPosX -newX) # mWh
            
        elif oldX in range(ZeroPosX+1,MaxX+1) and newX in range(ZeroPosX+1,MaxX+1):
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
        
    elif newY == ZeroPosY or oldY == newY:
        EnergyY = 0 

    else:    
        if oldY in range(MinY, ZeroPosY) and newY in range(MinY, ZeroPosY):
           if abs(newY) > abs(oldY):
                EnergyY = SlopeY * (abs(newY)-abs(oldY))
           else:
                EnergyY = 0
                
        elif oldY in range(MinY, ZeroPosY) and newY in range(ZeroPosY + 1, MaxY + 1):   
            EnergyY = SlopeY * (abs(newY) - ZeroPosY)
        
        elif oldY in range(ZeroPosY + 1, MaxY + 1) and newY in range(MinY, ZeroPosY):
            EnergyY = SlopeY * (abs(newY)- ZeroPosY) # mWh
        
        elif oldY in range(ZeroPosY + 1, MaxY + 1) and newY in range(ZeroPosY + 1, MaxY + 1):
            if newY > oldY:
                EnergyY = SlopeY * (newY-oldY)
            else:
                EnergyY = 0
    
    
#    print 'y'        
#    print 'Neu', newY
#    print 'old', oldY
    #print 'energyY', EnergyY, 'mWh'
#    print 'dif', EnergyY/SlopeY
    
#    print 'total', (Energy + EnergyY)/1000. * PanelNum, 'Wh/50 Panels'
    
    return round((Energy + EnergyY)/1000. * PanelNum,2)

   
TnewX = np.nan
TnewY = np.nan

ToldX = np.nan
ToldY = np.nan


#TotalEnergy =  ActuationDemand (oldX = ToldX, newX = TnewX, oldY = ToldY, newY = TnewY, PanelNum = 50)




