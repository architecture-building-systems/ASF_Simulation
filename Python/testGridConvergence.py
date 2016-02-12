# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 16:33:12 2016

@author: Jeremias
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np


path = "C:/Users/Assistenz/Documents/MT_Jeremias/Simulation_Data/RadiationEvaluation/gridConvergenceEvaluation/"
    
#Import data from csv
gridConvergence=np.genfromtxt(path + 'gridConvergence_deleteDoubleEntries.csv',delimiter=',')

startHour = int(min(gridConvergence[:,0]))
endHour = int(max(gridConvergence[:,0]))
numberOfComb = int(max(gridConvergence[:,1]+1))
numberOfHours = endHour + 1 - startHour
numberOfTestSizes = 5

gridConvergenceRad = []

for i in range(numberOfHours):
    gridConvergenceRad.append([])
    
    for j in range(numberOfComb):
        gridConvergenceRad[i].append([])
        
        for k in range(numberOfTestSizes):
            gridConvergenceRad[i][j].append(gridConvergence[i*numberOfComb*numberOfTestSizes+j*numberOfTestSizes +k][3])
            
fig = plt.figure()
cmap = mpl.cm.cubehelix
cmap = mpl.cm.jet
for i in range(numberOfHours):
    for j in range(numberOfComb):
        if j==0:
            plt.plot([1,2,3,4,5],np.array(gridConvergenceRad[i][j])/gridConvergenceRad[i][j][4], color=cmap(i/float(numberOfHours)), label='hour'+str(5+i))
        else:
            plt.plot([1,2,3,4,5],np.array(gridConvergenceRad[i][j])/gridConvergenceRad[i][j][4], color=cmap(i/float(numberOfHours)))
fig.subplots_adjust(right=0.8)
plt.legend(loc=2, bbox_to_anchor=(1., 1))    
    #plt.legend(['hour'+str(5+i)])

#cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,numberOfHours))


## Generate data...
#nx, nsteps = 100, 20
#x = np.linspace(0, 1, nx)
#data = np.random.random((nx, nsteps)) - 0.5
#data = data.cumsum(axis=0)
#data = data.cumsum(axis=1)
#
## Plot
#cmap = mpl.cm.autumn
#for i, y in enumerate(data.T):
#    plt.plot(x, y, color=cmap(i / float(nsteps)))
#
#plt.show()