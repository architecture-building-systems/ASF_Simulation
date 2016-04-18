# -*- coding: utf-8 -*-
"""
Plot Data Functions

@author: Assistenz
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import MultipleLocator, FormatStrFormatter


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
def pcolorDays(DIVA_results, arg):
    
    # use maximum or minimum value:
    max_min = arg[0]
    
    # define what data should be plotted:
    X = DIVA_results[arg[1]]
    
    # define rotation axis:
    rotation_axis = arg[2]
    
    # assign angles and angle_locations:    
    x_angle_location = DIVA_results['angles']['x_angle_location']
    y_angle_location = DIVA_results['angles']['y_angle_location']
    allAngles = DIVA_results['angles']['allAngles']
    
    if len(arg)==0:
        max_min = 'min'
    else:
        max_min = arg[0]
        
    axis_ind =[]
    
    if max_min == 'min':
        ind=np.argmin(X,axis=0)
    elif max_min == 'max':
        ind=np.argmax(X,axis=0)


    z_min=0
    if rotation_axis == 'x':
        for i in range(len(ind)):
            axis_ind.append(x_angle_location[ind[i]])
            z_max=max(x_angle_location)
    elif rotation_axis == 'y':
        for i in range(len(ind)):
            axis_ind.append(y_angle_location[ind[i]])
            z_max=max(y_angle_location)
    elif rotation_axis == 'xy':
        axis_ind = ind
        z_max=len(allAngles[0])-1
    else:
        print 'axis not available'
    dx, dy = 1, 1
    
    # generate 2 2d grids for the x & y bounds
    y, x = np.mgrid[slice(0, 24 + dy, dy),
                    slice(0, 365 + dx, dx)]
    z=[]
    for i in range(24):
        z.append([])
        for j in range(365):
            z[i].append(axis_ind[24*j + i])
    z = np.asarray(z)
    
   # z_min, z_max = 0, len()
    #print z_min, z_max
    
    #plt.pcolor(x, y, z, cmap='jet', vmin=z_min, vmax=z_max)
    plt.pcolor(x, y, z, cmap='cubehelix', vmin=z_min, vmax=z_max)
    #plt.pcolor(x, y, z, cmap='nipy_spectral', vmin=z_min, vmax=z_max)

    #plt.title('pcolor')
#    plt.xlabel("Day of the Year")
#    plt.ylabel("Hour of the Day")
    # set the limits of the plot to the limits of the data
    plt.axis([x.min(), x.max(), y.min(), y.max()])
    
    
def pcolorMonths(monthlyData, arg):
    """
    create carpet plot from monthly data \n
    inputs: monthlyData dictionary, arg (['min'/'max', 'X', 'rotation_axis', 'DIVA'/'LB']) \n
    output: carpetplot
    """
    # use maximum or minimum value:
    max_min = arg[0]
    
    # define what data should be plotted:
    X = monthlyData[arg[1]]
    
    # define rotation axis:
    rotation_axis = arg[2]
    
    # define mask:
    if arg[3]=='DIVA':
        sunMask = monthlyData['DIVAmask']
    elif arg[3]=='LB':
        sunMask = monthlyData['LBmask']
    else:
        raise ValueError('mask does not exist')
        
    # assign angles and angle_locations:    
    x_angle_location = monthlyData['angles']['x_angle_location']
    y_angle_location = monthlyData['angles']['y_angle_location']
    allAngles = monthlyData['angles']['allAngles']
    
    # find index of max/min from data according to the given option:
    if max_min == 'min':
        ind=np.argmin(X,axis=0)
    elif max_min == 'max':
        ind=np.argmax(X,axis=0)
    else:
        print "somehow max min is not working"

     # define axis index list:      
    axis_ind =[]
    
    # assign indices according to option:
    z_min=0
    if rotation_axis == 'x':
        for i in range(len(ind)):
            axis_ind.append(x_angle_location[ind[i]])
        z_max=max(x_angle_location)
    elif rotation_axis == 'y':
        for i in range(len(ind)):
            axis_ind.append(y_angle_location[ind[i]])
        z_max=max(y_angle_location)
    elif rotation_axis == 'xy':
        axis_ind = ind
        z_max=len(allAngles[0])-1
    else:
        print 'axis not available'
    dx, dy = 1, 1
    
    # generate 2 2d grids for the x & y bounds:
    y, x = np.mgrid[slice(0, 24 + dy, dy),
                    slice(0, 12 + dx, dx)]
                    
    # create array with data that will be plotted:
    z=[]
    for i in range(24):
        z.append([])
        for j in range(12):
            z[i].append(axis_ind[24*j + i])
    z = np.asarray(z)
    
    # create masked array from sunMask:
    masked_array = np.ma.array(z, mask=sunMask)
    
    # define colormap:
    cmap = plt.cm.cubehelix
    
    # define what happens to bad data (i.e. data outside the mask):
    cmap.set_bad('grey',1.)
    
    # create the carpet plot:
    plt.pcolormesh(x, y, masked_array, cmap=cmap, vmin=z_min, vmax=z_max)

    # set the limits of the plot to the limits of the data
    plt.axis([x.min(), x.max(), 3, 22])
    plt.tick_params(axis=u'both',labelsize=14)
    
def pcolorEnergyMonths(monthlyData, arg):
    """
    create carpet plot for the energy from monthly data \n
    inputs: monthlyData dictionary, arg (['min'/'max', 'X']) \n
    output: carpetplot
    """
    # use maximum or minimum value:
    max_min = arg[0]
            
    # define what data should be plotted:
    X = monthlyData[arg[1]]

    # define maximum and minimum values of data, used for plotting:
    z_min = arg[4]
    z_max = arg[5]    
    
    # find indices:
    if max_min == 'min':
        ind=np.argmin(X,axis=0)
    elif max_min == 'max':
        ind=np.argmax(X,axis=0)
    else:
        raise ValueError("maxMin must be either 'max' or 'min'")
 
    # generate 2 2d grids for the x & y bounds
    dx, dy = 1, 1
    y, x = np.mgrid[slice(0, 24 + dy, dy),
                    slice(0, 12 + dx, dx)]
                    
    # assign values used for colormap:
    z=[]
    for i in range(24):
        z.append([])
        for j in range(12):
            z[i].append(X[ind[24*j + i]][24*j + i])
    z = np.asarray(z)
    
    # create custum colormap:
    
    # define the location of the middle number (where 0 is):
    z_middle = float(abs(z_min)) / (z_max-z_min) 
    
    # create custom color dictionary:
    cdict1 = {'red':   ((0.0, 0.0, 0.0),
                       (z_middle, 0.0, 0.1),
                       (1.0, 1.0, 1.0)),
    
             'green': ((0.0, 0.0, 0.0),
                       (z_middle, 0.0, 0.0),
                       (1.0, 0.0, 0.0)),
    
             'blue': ((0.0, 0.0, 1.0),
                       (z_middle, 0.1, 0.0),
                       (1.0, 0.0, 0.0))
            }
    
    # create colormap:
    blue_red1 = LinearSegmentedColormap('BlueRed1', cdict1)   
   
   # plot data:
    plt.pcolor(x, y, z, cmap=blue_red1, vmin=z_min, vmax=z_max)   
    plt.axis([x.min(), x.max(), y.min(), y.max()])
    plt.tick_params(axis=u'both',labelsize=14)

def pcolorEnergyDays(DIVA_results, arg):
    """
    create carpet plot for the energy from monthly data \n
    inputs: DIVA_results dictionary, arg (['min'/'max', 'X']) \n
    output: carpetplot
    """
    # use maximum or minimum value:
    max_min = arg[0]
            
    # define what data should be plotted:
    X = DIVA_results[arg[1]]

    # define maximum and minimum values of data, used for plotting:
    z_min = arg[4]
    z_max = arg[5]    
    
    # find indices:
    if max_min == 'min':
        ind=np.argmin(X,axis=0)
    elif max_min == 'max':
        ind=np.argmax(X,axis=0)
    else:
        raise ValueError("maxMin must be either 'max' or 'min'")
 
    # generate 2 2d grids for the x & y bounds
    dx, dy = 1, 1
    y, x = np.mgrid[slice(0, 24 + dy, dy),
                    slice(0, 365 + dx, dx)]
                    
    # assign values used for colormap:
    z=[]
    for i in range(24):
        z.append([])
        for j in range(365):
            z[i].append(X[ind[24*j + i]][24*j + i])
    z = np.asarray(z)
    
    # create custum colormap:
    
    # define the location of the middle number (where 0 is):
    z_middle = float(abs(z_min)) / (z_max-z_min) 
    
    # create custom color dictionary:
    cdict1 = {'red':   ((0.0, 0.0, 0.0),
                       (z_middle, 0.0, 0.1),
                       (1.0, 1.0, 1.0)),
    
             'green': ((0.0, 0.0, 0.0),
                       (z_middle, 0.0, 0.0),
                       (1.0, 0.0, 0.0)),
    
             'blue': ((0.0, 0.0, 1.0),
                       (z_middle, 0.1, 0.0),
                       (1.0, 0.0, 0.0))
            }
    
    # create colormap:
    blue_red1 = LinearSegmentedColormap('BlueRed1', cdict1)   
   
   # plot data:
    plt.pcolor(x, y, z, cmap='afmhot', vmin=z_min, vmax=z_max)   
    plt.axis([x.min(), x.max(), y.min(), y.max()])
    plt.tick_params(axis=u'both',labelsize=14)
    

def VisualizeSunTrackingAngles(SunTrackingData, rotation_axis):
    
    dx, dy = 1, 1
    
    # generate 2 2d grids for the x & y bounds
    y, x = np.mgrid[slice(0, 24 + dy, dy),
                    slice(0, 12 + dx, dx)]

    z = np.empty((24,12))*np.nan
    
    if rotation_axis == 'x':
        for i in range(len(SunTrackingData['HOY'])):
            z[SunTrackingData['HoursInMonthTracking'][i],SunTrackingData['MonthTracking'][i]-1]= SunTrackingData['Xangles'][i]
            z_min = 0
            z_max = 90
    elif rotation_axis == 'y':
        for i in range(len(SunTrackingData['HOY'])):
            z[SunTrackingData['HoursInMonthTracking'][i],SunTrackingData['MonthTracking'][i]-1]= SunTrackingData['Yangles'][i]   
            z_min = -45
            z_max = 45
    else:
        print 'axis not available'
        
    z_mask = np.isnan(z)
    masked_array = np.ma.array(z, mask=z_mask)
    cmap = plt.cm.cubehelix
    cmap.set_bad('grey',1.)

    
    #plt.pcolor(x, y, z, cmap='jet', vmin=z_min, vmax=z_max)
    plt.pcolormesh(x, y, masked_array, cmap=cmap, vmin=z_min, vmax=z_max)

    # set the limits of the plot to the limits of the data
    plt.axis([x.min(), x.max(), 3, 22])
    plt.colorbar()
    plt.tick_params(axis=u'both',labelsize=14)

def plotDataForIndices(monthlyData, indices, usedEfficiencies, arg):
    
    energyType = arg[0]    
    
    dummyRange = np.asarray(range(len(indices[energyType])))
    
    fig = plt.figure(figsize=(16, 8))
    
#    plt.suptitle('Heating Demand (COP=' + str(usedEfficiencies['H_COP']) + ')')
    if energyType == 'PV':
        multiplier = -1
    else:
        multiplier = 1
    
    ax1 = plt.subplot(2,1,1)
    plt.plot(multiplier*monthlyData[energyType][indices['H'], dummyRange], label = 'optimized for H', color='r')
    plt.plot(multiplier*monthlyData[energyType][indices['C'], dummyRange], label = 'optimized for C', color='b')
    plt.plot(multiplier*monthlyData[energyType][indices['L'], dummyRange], label = 'optimized for L', color='g')
    plt.plot(multiplier*monthlyData[energyType][indices['PV'], dummyRange], label = 'optimized for PV', color='c')
    plt.plot(multiplier*monthlyData[energyType][indices['E_HCL'], dummyRange], label = 'optimized for HCL', color='m')
    plt.plot(multiplier*monthlyData[energyType][indices['E_tot'], dummyRange], label = 'optimized for E_tot', color='k')
    plt.plot(multiplier*monthlyData[energyType][indices['45'], :], label = 'fixed at 45 deg', color='y')
    plt.ylabel('Energy [kWh]')
    plt.legend()
    
    majorLocator = MultipleLocator(24)
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(4)
    minorFormatter = FormatStrFormatter('%d')

    ax1.xaxis.set_major_locator(majorLocator)
    ax1.xaxis.set_major_formatter(majorFormatter)
    ax1.xaxis.set_minor_locator(minorLocator)
#    ax1.xaxis.set_minor_formatter(minorFormatter)
    plt.grid(True, which='both')
    
    ax2 = plt.subplot(2,1,2, sharex=ax1)
    plt.plot(multiplier*monthlyData[energyType][indices['H'], dummyRange]-multiplier*monthlyData[energyType][indices[energyType], dummyRange], label = 'optimized for H', color='r')
    plt.plot(multiplier*monthlyData[energyType][indices['C'], dummyRange]-multiplier*monthlyData[energyType][indices[energyType], dummyRange], label = 'optimized for C', color='b')
    plt.plot(multiplier*monthlyData[energyType][indices['L'], dummyRange]-multiplier*monthlyData[energyType][indices[energyType], dummyRange], label = 'optimized for L', color='g')
    plt.plot(multiplier*monthlyData[energyType][indices['PV'], dummyRange]-multiplier*monthlyData[energyType][indices[energyType], dummyRange], label = 'optimized for PV', color='c')
    plt.plot(multiplier*monthlyData[energyType][indices['E_HCL'], dummyRange]-multiplier*monthlyData[energyType][indices[energyType], dummyRange], label = 'optimized for HCL', color='m')
    plt.plot(multiplier*monthlyData[energyType][indices['E_tot'], dummyRange]-multiplier*monthlyData[energyType][indices[energyType], dummyRange], label = 'optimized for E_tot', color='k')
    plt.plot(multiplier*monthlyData[energyType][indices['45'],:]-multiplier*monthlyData[energyType][indices[energyType], dummyRange], label = 'fixed at 45 deg', color='y')
    plt.ylabel('Energy Difference [kWh]')
    plt.legend()

    ax2.xaxis.set_major_locator(majorLocator)
    ax2.xaxis.set_major_formatter(majorFormatter)
    ax2.xaxis.set_minor_locator(minorLocator)
#    ax2.xaxis.set_minor_formatter(minorFormatter)
    plt.grid(True, which='both')
    
    return fig

# function that shows histograms of angle combinations for one axis
def AngleHistogram(X,rotation_axis,x_angles,x_angle_location,y_angles,y_angle_location,allAngles):
    axis_ind =[]
    ind=np.argmin(X,axis=0)
    if rotation_axis == 'x':
        for i in range(len(ind)):
            axis_ind.append(x_angle_location[ind[i]])
        plt.hist(axis_ind, bins=np.array(range(-1,len(x_angles)))+0.5)
        plt.xticks(np.array(range(0,len(x_angles))),x_angles)
        pylab.xlim(-1,len(x_angles))
        plt.xlabel("x-angles")
        plt.ylabel("frequency")
    elif rotation_axis == 'y':
        for i in range(len(ind)):
            axis_ind.append(y_angle_location[ind[i]])
        plt.hist(axis_ind, bins=np.array(range(-1,len(y_angles)))+0.5)
        plt.xticks(np.array(range(0,len(y_angles))),y_angles)
        pylab.xlim(-1,len(y_angles))
        plt.xlabel("y-angles")
        plt.ylabel("frequency")
    elif rotation_axis == 'xy':
        axis_ind=ind
        plt.hist(axis_ind, bins=np.array(range(-1,len(allAngles[0])))+0.5)
        plt.xticks(np.array(range(0,len(allAngles[0]))),allAngles[0])
        pylab.xlim(-1,len(allAngles[0]))
        plt.xlabel("angles")
        plt.ylabel("frequency")
    else:
        print 'axis not available'
    #return axis_ind
    
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)
