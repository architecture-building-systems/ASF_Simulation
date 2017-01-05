# -*- coding: utf-8 -*-
"""
Created on Thu Jan 05 14:31:30 2017

@author: Assistenz
"""
import numpy as np
import pandas as pd
import time
import os

path = r'C:\Users\Assistenz\Desktop\Mauro\radiation_visualization'
project = 'ASF_0_0_AM'
TimePeriod = 24
PanelNum = 50
PanelLen = 400
GridSize = 25

GridPoints = PanelLen/GridSize**2
print GridPoints

#def ShapeData(path, project, TimePeriod, PanelNum, GridPoints):

print 'Time: ' + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
tic = time.time()

path1 = os.path.join(path,project) + '\output\ASF1\res\ASF1.ill'
path2 = os.path.join(path,project) + '\output\ASF2\res\ASF2.ill'
path3 = os.path.join(path,project) + '\output\ASF3\res\ASF3.ill'
path4 = os.path.join(path,project) + '\output\ASF4\res\ASF4.ill'

skip = 8760 - TimePeriod

d1 = np.genfromtxt(path1, skip_footer= skip) #, usecols = (3)
d2 = np.genfromtxt(path2, skip_footer= skip)
d3 = np.genfromtxt(path3, skip_footer= skip)
d4 = np.genfromtxt(path4, skip_footer= skip)

ASF = np.concatenate((d1[:,3:]/1000., d2[:,3:]/1000., d3[:,3:]/1000.,d4[:,3:]/1000.), axis=1)



HOURS = np.size(ASF,0)
HOY = {}



for hour in range(HOURS):
    HOY[hour]= np.reshape(ASF[hour],(PanelNum, GridPoints))
   
hallo = HOY

save= r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RadiationModel'
np.save(os.path.join(save,'Test.npy'),HOY)


toc = time.time() - tic
print 'time passed (min): ' + str(round(toc/60.,2))