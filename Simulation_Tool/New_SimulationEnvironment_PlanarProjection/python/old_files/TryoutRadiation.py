# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 20:32:10 2016

some python script to tryout some things concerning radiation, not longer needed
probably not worth it to be looked at again!

@author: Assistenz
"""


import math, sys, copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab

from sortAngles import CalcXYAnglesAndLocation, unique
from calculate_angles_function import create_ASF_angles  
from PostProcessThermal_functions import scatterResults, pcolorDays, AngleHistogram, pcolorEnergyDays

#angles9=[[]]
#
#for i in range(9):
#    angles9[0].append(allAngles[0][i])
    

figcounter+=1
fig = plt.figure(num = figcounter, figsize=(16, 12))
pcolorDays(R_tot, 'xy', x_angle_location, y_angle_location, allAngles[0], 'max')
plt.title("Radiation on panels")

fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(allAngles[0])))
cbar.ax.set_yticklabels(allAngles[0])
plt.show()

figcounter+=1
fig = plt.figure(num = figcounter, figsize=(16, 12))
pcolorEnergyDays(R_tot)

axis_ind =[]
ind=np.argmax(X,axis=0)
#    if rotation_axis == 'x':
#        for i in range(len(ind)):
#            axis_ind.append(x_angle_location[ind[i]])
#    elif rotation_axis == 'y':
#        for i in range(len(ind)):
#            axis_ind.append(y_angle_location[ind[i]])
#    else:
#        print 'axis not available'
dx, dy = 1, 1

# generate 2 2d grids for the x & y bounds
y, x = np.mgrid[slice(1, 24 + dy, dy),
                slice(1, 365 + dx, dx)]
z=[]
for i in range(24):
    z.append([])
    for j in range(365):
        z[i].append(X[ind[24*j + i]][24*j + i])
z = np.asarray(z)

z_min, z_max = 0, np.max(z)
#print z_min, z_max

#plt.pcolor(x, y, z, cmap='jet', vmin=z_min, vmax=z_max)
plt.pcolor(x, y, z, cmap='afmhot', vmin=z_min, vmax=z_max)
#plt.pcolor(x, y, z, cmap='nipy_spectral', vmin=z_min, vmax=z_max)

#plt.title('pcolor')
plt.xlabel("Day of the Year")
plt.ylabel("Hour of the Day")
# set the limits of the plot to the limits of the data
plt.axis([x.min(), x.max(), y.min(), y.max()])

