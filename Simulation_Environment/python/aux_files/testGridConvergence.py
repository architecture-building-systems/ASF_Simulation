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
gridConvergenceSmall = np.genfromtxt(path + 'gridConvergence_12.47_deleteDoubleEntries.csv',delimiter=',')

startHour = int(min(gridConvergence[:,0]))
endHour = int(max(gridConvergence[:,0]))
numberOfComb = int(max(gridConvergence[:,1]+1))
numberOfHours = endHour + 1 - startHour
numberOfTestSizes = 5

x_angles = [0,45,90]
y_angles = [-45,0,45]

anglecombinations = []

for i in range(9):
    anglecombinations.append(str(x_angles[i/3]) + '/' + str(y_angles[i%3]))


## create custum colormap:
#cdict1 = {'red':   ((0.0, 0.0, 0.0),
#                   (0.5, 0.0, 0.1),
#                   (1.0, 1.0, 1.0)),
#
#         'green': ((0.0, 0.0, 0.0),
#                   (1.0, 0.0, 0.0)),
#
#         'blue':  ((0.0, 0.0, 1.0),
#                   (0.5, 0.1, 0.0),
#                   (1.0, 0.0, 0.0))
#        }
#
#blue_red1 = LinearSegmentedColormap('BlueRed1', cdict1)

gridConvergenceRad = []

for i in range(numberOfHours):
    gridConvergenceRad.append([])
    
    for j in range(numberOfComb):
        gridConvergenceRad[i].append([])
        
        for k in range(numberOfTestSizes):
            gridConvergenceRad[i][j].append(gridConvergence[i*numberOfComb*numberOfTestSizes+j*numberOfTestSizes +k][3])
        gridConvergenceRad[i][j].append(gridConvergenceSmall[i*numberOfComb+j][3])

gridConvergenceRad2 = [[],[],[],[],[]]

for i in range(len(gridConvergence)):
    gridConvergenceRad2[i%5].append(gridConvergence[(i,3)])
    
for i in range(5):
    gridConvergenceRad2[i]=np.array(gridConvergenceRad2[i])
gridConvergenceRad2.append(gridConvergenceSmall[:,3])

gridConvergenceBox = []

for i in range(6):
    gridConvergenceBox.append([])
    gridConvergenceBox[i]=gridConvergenceRad2[i]/gridConvergenceRad2[5]
        
fig = plt.figure(figsize=(16, 12))
plt.suptitle("Grid Convergence", size=16)

plt.subplot(4,2,3)
cmap = mpl.cm.cubehelix
cmap = mpl.cm.jet
#cmap = mpl.cm.RdYlGn
#cmap = blue_red1
xindex = [1,2,3,4,5,6] #[400,199,99.5,49.8,24.9]
for i in range(numberOfHours):
    for j in range(numberOfComb):
        if j==0:
            plt.plot(xindex,np.array(gridConvergenceRad[i][j])/gridConvergenceRad[i][j][5], color=cmap(i/float(numberOfHours)), label=str(5+i) +':00 - ' + str(5+i+1) +':00', marker = 'D')
        else:
            plt.plot(xindex,np.array(gridConvergenceRad[i][j])/gridConvergenceRad[i][j][5], color=cmap(i/float(numberOfHours)), marker = 'D')
plt.xticks(xindex,('400', '200', '100', '50', '25', '12.5'))
plt.ylabel('normalized radiation [-]',fontsize=14)#, verticalalignment = 'top', horizontalalignment = 'left')
ax = plt.gca()
ax.yaxis.set_label_coords(-0.1, 0.5)
plt.grid()
plt.tick_params(axis=u'both',labelsize=14)

plt.subplot(4,2,1)
for i in range(numberOfHours):
    for j in range(numberOfComb):
        if j==0:
            plt.plot(xindex,np.array(gridConvergenceRad[i][j]), color=cmap(i/float(numberOfHours)), label=str(5+i) +':00 - ' + str(5+i+1) +':00', marker = 'D')
        else:
            plt.plot(xindex,np.array(gridConvergenceRad[i][j]), color=cmap(i/float(numberOfHours)), marker = 'D')
plt.xticks(xindex,('400', '200', '100', '50', '25', '12.5'))
plt.ylabel('total radiation [kWh/h]',fontsize=14)#, verticalalignment = 'bottom', horizontalalignment = 'left')
ax = plt.gca()
ax.yaxis.set_label_coords(-0.1, 0.5)
plt.tick_params(axis=u'both',labelsize=14)
fig.subplots_adjust(right=0.8)
plt.grid()
plt.legend(loc=2, bbox_to_anchor=(1.02, 1), title = 'Hour', fontsize = 14)
ax.get_legend().get_title().set_fontsize(14)
    

plt.subplot(4,2,5)
cmap = mpl.cm.cubehelix
cmap = mpl.cm.gist_earth
#cmap = mpl.cm.RdYlGn
#cmap = blue_red1
xindex = [1,2,3,4,5,6] #[400,199,99.5,49.8,24.9]
for i in range(numberOfHours):
    for j in range(numberOfComb):
        if i==0:
            plt.plot(xindex,np.array(gridConvergenceRad[i][j])/gridConvergenceRad[i][j][5], color=cmap(j/float(numberOfComb)), label=anglecombinations[j], marker = 'D')
        else:
            plt.plot(xindex,np.array(gridConvergenceRad[i][j])/gridConvergenceRad[i][j][5], color=cmap(j/float(numberOfComb)), marker = 'D')

plt.xticks(xindex,('400', '200', '100', '50', '25', '12.5'))
plt.ylabel('normalized radiation [-]',fontsize=14)#, verticalalignment = 'top', horizontalalignment = 'left')
plt.legend(loc=2, bbox_to_anchor=(1.02, 1),title = 'Alt/Azim [deg]', fontsize = 14)    
ax = plt.gca()
ax.get_legend().get_title().set_fontsize(14)
ax.yaxis.set_label_coords(-0.1, 0.5)
plt.grid()
plt.tick_params(axis=u'both',labelsize=14)

plt.subplot(4,2,7)
cmap = mpl.cm.cubehelix
cmap = mpl.cm.jet
#cmap = mpl.cm.RdYlGn
#cmap = blue_red1
xindex = [1,2,3,4,5,6] #[400,199,99.5,49.8,24.9]
counter = 0
sumDiff = np.array([0.0]*6)
for i in range(numberOfHours):
    for j in range(numberOfComb):
        sumDiff += np.abs(np.array(gridConvergenceRad[i][j])-gridConvergenceRad[i][j][5])/gridConvergenceRad[i][j][5]
        counter +=1        
        if i==0:
            pass
            #plt.plot(xindex,np.array(gridConvergenceRad[i][j])/gridConvergenceRad[i][j][5], color=cmap(j/float(numberOfComb)), label='combination '+str(j), marker = 'D')
            #plt.plot(xindex,np.abs(np.array(gridConvergenceRad[i][j])-gridConvergenceRad[i][j][5])/gridConvergenceRad[i][j][5], color=cmap(j/float(numberOfComb)), label='combination '+str(j), marker = 'D')
        else:
            pass
            #plt.plot(xindex,np.array(gridConvergenceRad[i][j])/gridConvergenceRad[i][j][5], color=cmap(j/float(numberOfComb)), marker = 'D')
            #plt.plot(xindex,np.abs(np.array(gridConvergenceRad[i][j])-gridConvergenceRad[i][j][5])/gridConvergenceRad[i][j][5], color=cmap(j/float(numberOfComb)), marker = 'D')
plt.plot(xindex, sumDiff/counter, linewidth = 4)
plt.xlabel('grid size [mm]',fontsize=14)
plt.xticks(xindex,('400', '200', '100', '50', '25', '12.5'))
plt.ylabel('average deviation [-]',fontsize=14)#, verticalalignment = 'top', horizontalalignment = 'left')
plt.legend(loc=2, bbox_to_anchor=(1.02, 1),fontsize = 14)    
ax = plt.gca()
ax.yaxis.set_label_coords(-0.1, 0.5)
plt.grid()
plt.tick_params(axis=u'both',labelsize=14)



plt.subplot(1,2,2)

#data = [np.random.normal(0, std, 1000) for std in range(1, 6)]
data = gridConvergenceBox
box = plt.boxplot(data, notch=True, patch_artist=True)
plt.xticks(xindex,('400', '200', '100', '50', '25', '12.5'),size = 14)
plt.yticks(size=14)
plt.ylabel('normalized radiation [-]', fontsize = 14)
plt.xlabel('grid size [mm]', fontsize = 14)
#colors = ['cyan', 'lightblue', 'lightgreen', 'tan', 'pink', 'red']
colors = ['lightblue']*6
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)
#plt.tight_layout()
plt.subplots_adjust(hspace=0.22, wspace=0.54, right=0.98, left=0.08, bottom=0.11)
plt.grid()
plt.show()
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