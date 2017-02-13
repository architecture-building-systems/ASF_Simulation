# -*- coding: utf-8 -*-
"""
Created on Mon Feb 06 11:34:20 2017

@author: Assistenz

PV electricity caluclation simplified
"""
import pandas as pd
import sys,os

import matplotlib
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

paths = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RadiationModel'
PowerLoss = pd.read_csv(os.path.join(paths, 'powerloss.csv'))
longitude = pd.read_csv(os.path.join(paths, 'longitude.csv'))
latitude = pd.read_csv(os.path.join(paths, 'latitude.csv'))

PowerLoss.columns = [range(50)]

PowerLoss2 = np.matrix(PowerLoss)
logitude2 = np.matrix(longitude)
latidude2 = np.matrix(latitude)

Long = np.array(range(0,100,2))/100.
Lat = np.array(range(0,100,2))/100.

Long = Long.tolist()
Lat = Lat.tolist()

delta = 2
x = np.arange(0, 100, delta)
y = np.arange(0, 100, delta)
X, Y = np.meshgrid(x, y)
Z = PowerLoss


fig = plt.figure()
CS = plt.contour(X, Y, Z, 8)
plt.clabel(CS, inline=1, fontsize=10)
plt.title('Power Loss [%]')
plt.xlabel('Logitudinal Shading [%]')
plt.ylabel('Lateral Shading [%]')
plt.xticks([20,40,60,80,100])
plt.yticks([20,40,60,80,100])


fig.savefig(os.path.join(paths, 'PowerLoss.pdf'))
            
