# -*- coding: utf-8 -*-
"""
Created on Mon May 23 15:57:13 2016

make plot to visualize optimization

@author: Assistenz
"""
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt


data = monthlyData['E_tot'][:,130]

dataMatrix = data.reshape(7,7)

fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')
x,y = np.shape(dataMatrix)
X,Y = np.meshgrid(range(x),range(y))
X = X*15-45
Y = Y*15
#plt.pcolor(X,Y,-monthlyData[typeE][:,plotRange].transpose()+np.array(np.max(monthlyData[typeE], axis=0))[plotRange, None], cmap = 'jet')
#plt.pcolor(X,Y,dataMatrix, cmap = 'jet')
#ax.plot_surface(X,Y,-monthlyData[typeE][:,plotRange].transpose()+np.array(np.max(monthlyData[typeE], axis=0))[plotRange, None], cmap = cm.jet,rstride=1, cstride=1)
ax.plot_surface(X,Y,dataMatrix, cmap = cm.jet,rstride=1, cstride=1)

plt.title('Energy Dependency on Angle Combination' )
plt.axis([X.min(), X.max(), Y.min(), Y.max()])
#fig.subplots_adjust(right=0.8)
#cbar_ax = fig.add_axes([0.85, 0.1, 0.05, 0.78])
#cbar = plt.colorbar(cax=cbar_ax)
plt.xlabel('Azimuth [deg]')
plt.ylabel('Altitude [deg]')
ax.set_zlabel('Energy [kWh]')