# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 11:27:46 2015

@author: Assistenz
"""


import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab

# function to show frequencies of x and y angle combinations
def scatterResults(X, Xcolour,offset,x_angles,x_angle_location,y_angles,y_angle_location):
    #ind=np.argpartition(X, 4, axis=0)[:4]
    ind=np.argmin(X,axis=0)
    xind = []
    yind = []
    for i in range(len(ind)):
        xind.append(x_angle_location[ind[i]])
        yind.append(y_angle_location[ind[i]])
    plt.scatter(xind,yind, alpha=0.01, color=Xcolour)
    plt.xticks(np.array(range(0,len(x_angles))),x_angles)
    pylab.xlim(-1,len(x_angles)+1)
    plt.yticks(np.array(range(0,len(y_angles))),y_angles)
    pylab.ylim(-1,len(y_angles)+1)    
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)
    plt.xlabel("x-angles")
    plt.ylabel("y-angles")
    plt.grid(b=True, which='major')
    
    
# function that shows optimal angle combinations for every hour of the year for one axis
def pcolorDays(X, rotation_axis, x_angle_location, y_angle_location):
    axis_ind =[]
    ind=np.argmin(X,axis=0)
    if rotation_axis == 'x':
        for i in range(len(ind)):
            axis_ind.append(x_angle_location[ind[i]])
    elif rotation_axis == 'y':
        for i in range(len(ind)):
            axis_ind.append(y_angle_location[ind[i]])
    else:
        print 'axis not available'
    dx, dy = 1, 1
    
    # generate 2 2d grids for the x & y bounds
    y, x = np.mgrid[slice(1, 24 + dy, dy),
                    slice(1, 365 + dx, dx)]
    z=[]
    for i in range(24):
        z.append([])
        for j in range(365):
            z[i].append(axis_ind[24*j + i])
    z = np.asarray(z)
    
    z_min, z_max = 0, 27
    #print z_min, z_max
    
    #plt.pcolor(x, y, z, cmap='jet', vmin=z_min, vmax=z_max)
    plt.pcolor(x, y, z, cmap='cubehelix', vmin=z_min, vmax=z_max)
    #plt.pcolor(x, y, z, cmap='nipy_spectral', vmin=z_min, vmax=z_max)

    #plt.title('pcolor')
    plt.xlabel("Day of the Year")
    plt.ylabel("Hour of the Day")
    # set the limits of the plot to the limits of the data
    plt.axis([x.min(), x.max(), y.min(), y.max()])
    
# function that shows optimal angle combinations for every hour of the year for one axis
def pcolorEnergyDays(X):
    axis_ind =[]
    ind=np.argmin(X,axis=0)
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
    
    z_min, z_max = 0, 1
    #print z_min, z_max
    
    #plt.pcolor(x, y, z, cmap='jet', vmin=z_min, vmax=z_max)
    plt.pcolor(x, y, z, cmap='afmhot', vmin=z_min, vmax=z_max)
    #plt.pcolor(x, y, z, cmap='nipy_spectral', vmin=z_min, vmax=z_max)

    #plt.title('pcolor')
    plt.xlabel("Day of the Year")
    plt.ylabel("Hour of the Day")
    # set the limits of the plot to the limits of the data
    plt.axis([x.min(), x.max(), y.min(), y.max()])



# function that shows histograms of angle combinations for one axis
def AngleHistogram(X,rotation_axis,x_angles,x_angle_location,y_angles,y_angle_location):
    axis_ind =[]
    ind=np.argmin(X,axis=0)
    if rotation_axis == 'x':
        for i in range(len(ind)):
            axis_ind.append(x_angle_location[ind[i]])
        plt.hist(axis_ind, bins=np.array(range(0,len(x_angles)))-0.5)
        plt.xticks(np.array(range(0,len(x_angles))),x_angles)
        pylab.xlim(-1,len(x_angles)+1)
        plt.xlabel("x-angles")
        plt.ylabel("frequency")
    elif rotation_axis == 'y':
        for i in range(len(ind)):
            axis_ind.append(y_angle_location[ind[i]])
        plt.hist(axis_ind, bins=np.array(range(0,len(y_angles)))-0.5)
        plt.xticks(np.array(range(0,len(y_angles))),y_angles)
        pylab.xlim(-1,len(y_angles)+1)
        plt.xlabel("y-angles")
        plt.ylabel("frequency")
    else:
        print 'axis not available'
    #return axis_ind
    
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)



#fig = plt.figure()
#
#plt.suptitle("Angle Distribution around x-axis", size=16)
#p1 = plt.subplot(2,2,1)
#pcolorDays(H,'x')
#plt.title("Heating Demand")
#p1 = plt.subplot(2,2,2)
#pcolorDays(C,'x')
#plt.title("Cooling Demand")
#p1 = plt.subplot(2,2,3)
#pcolorDays(L,'x')
#plt.title("Lighting Demand")
#p1 = plt.subplot(2,2,4)
#pcolorDays(E,'x')
#plt.title("Total Energy Demand")
#
#fig.subplots_adjust(right=0.8)
#cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(x_angles)))
#cbar.ax.set_yticklabels(x_angles)
#plt.show()
#
#
#fig = plt.figure()
#plt.suptitle("Angle Distribution around y-axis", size=16)
#plt.subplot(2,2,1)
#pcolorDays(H,'y')
#plt.title("Heating Demand")
#plt.subplot(2,2,2)
#pcolorDays(C,'y')
#plt.title("Cooling Demand")
#plt.subplot(2,2,3)
#pcolorDays(L,'y')
#plt.title("Lighting Demand")
#plt.subplot(2,2,4)
#pcolorDays(E,'y')
#plt.title("Total Energy Demand")
#
#fig.subplots_adjust(right=0.8)
#cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(y_angles)))
#cbar.ax.set_yticklabels(y_angles)
#plt.show()
#
#
#
#fig = plt.figure()
#plt.suptitle("Angle Combination Distribution", size=16)
#plt.subplot(2,2,1)
#scatterResults(H,'r',0)
#plt.title("Heating Demand")
#plt.subplot(2,2,2)
#scatterResults(C,'b',1)
#plt.title("Cooling Demand")
#plt.subplot(2,2,3)
#scatterResults(L,'g',2)
#plt.title("Lighting Demand")
#plt.subplot(2,2,4)
#scatterResults(E,'c',3)
#plt.title("Angle Combination")
#plt.subplots_adjust(hspace=0.4)
##plt.locator_params(nbins=30)
##fig.ax.set_yticklabels(y_angles)
##fig.ax.set_xticklabels(x_angles)
#plt.show()
#
#
#fig = plt.figure()
#plt.suptitle("Histograms of Angle Distribution around x-axis", size=16)
#plt.subplot(2,2,1)
#AngleHistogram(H,'x')
#plt.title("Heating Demand")
#plt.subplot(2,2,2)
#AngleHistogram(C,'x')
#plt.title("Cooling Demand")
#plt.subplot(2,2,3)
#AngleHistogram(L,'x')
#plt.title("Lighting Demand")
#plt.subplot(2,2,4)
#AngleHistogram(E,'x')
#plt.title("Total Energy Demand")
#plt.tight_layout()
#
#fig = plt.figure()
#plt.suptitle("Histograms of Angle Distribution around y-axis", size=16)
#plt.subplot(2,2,1)
#AngleHistogram(H,'y')
#plt.title("Heating Demand")
#plt.subplot(2,2,2)
#AngleHistogram(C,'y')
#plt.title("Cooling Demand")
#plt.subplot(2,2,3)
#AngleHistogram(L,'y')
#plt.title("Lighting Demand")
#plt.subplot(2,2,4)
#AngleHistogram(E,'y')
#plt.title("Total Energy Demand")
#plt.tight_layout()

#print np.histogram(minInd, bins=len(minInd), range=None, normed=False, weights=None, density=None)#[source]
#numpy.histogram(a, bins=10, range=None, normed=False, weights=None, density=None)[source]

#plt.hist(minInd, bins=729)

