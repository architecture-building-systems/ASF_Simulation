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



def scatterResults(X, Xcolour,offset,x_angles,x_angle_location,y_angles,y_angle_location):
    """
    function to show frequencies of x and y angle combinations
    """
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
    
    
def pcolorDays(DIVA_results, arg):
    """
    function that shows optimal angle combinations for every hour of the year for one axis
    """
    
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
#    plt.pcolor(x, y, z, cmap='cubehelix', vmin=z_min, vmax=z_max)
    plt.pcolor(x, y, z, cmap='PRGn', vmin=z_min, vmax=z_max)
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
#    cmap = plt.cm.cubehelix
    #cmap = plt.cm.PRGn
#    cmap = plt.cm.RdBu$
    cmap = plt.cm.CMRmap
    cmap = plt.cm.gnuplot
    cmap = plt.cm.afmhot
    
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
    
#    # create custom color dictionary:
#    cdict1 = {'red':   ((0.0, 0.0, 0.0),
#                       (z_middle, 0.0, 0.1),
#                       (1.0, 1.0, 1.0)),
#    
#             'green': ((0.0, 0.0, 0.0),
#                       (z_middle, 0.0, 0.0),
#                       (1.0, 0.0, 0.0)),
#    
#             'blue': ((0.0, 0.0, 1.0),
#                       (z_middle, 0.1, 0.0),
#                       (1.0, 0.0, 0.0))
#            }    # create custom color dictionary:
    cdict1 = {'red':   ((0.0, 0.0, 0.0),
                       (z_middle, 0.0, 0.1),
                       (1.0, 1.0, 1.0)),
    
             'white': ((0.0, 0.0, 0.0),
                       (z_middle, 0.0, 0.0),
                       (1.0, 0.0, 0.0)),
    
             'blue': ((0.0, 0.0, 1.0),
                       (z_middle, 0.1, 0.0),
                       (1.0, 0.0, 0.0))
            }
            
    cmap = LinearSegmentedColormap.from_list('mycmap', [(0, 'navy'),
                                                    (z_middle, 'white'),
                                                    (1, 'firebrick')]
                                        )
    
    # create colormap:
    blue_red1 = LinearSegmentedColormap('mycmap', cdict1)   
   
   # plot data:
#    plt.pcolor(x, y, z, cmap=blue_red1, vmin=z_min, vmax=z_max)   
    plt.pcolor(x, y, z, cmap=cmap, vmin=z_min, vmax=z_max)   
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
    """
    function that generates a carpet plot of the sun tracking angles
    """
    
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
    cmap = plt.cm.RdBu
    cmap.set_bad('grey',1.)

    
    #plt.pcolor(x, y, z, cmap='jet', vmin=z_min, vmax=z_max)
    plt.pcolormesh(x, y, masked_array, cmap=cmap, vmin=z_min, vmax=z_max)

    # set the limits of the plot to the limits of the data
    plt.axis([x.min(), x.max(), 3, 22])
    plt.colorbar()
    plt.tick_params(axis=u'both',labelsize=14)


def plotDataForIndices(monthlyData, indices, usedEfficiencies, arg):
    """
    function that plots the energy specified by arg for different optimization
    strategies and fixed at 45 deg
    """
    
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
    plt.plot(multiplier*monthlyData[energyType][indices['PVC'], dummyRange], label = 'optimized for PV and C', color='b', alpha = 0.5)
    if not indices['45']==None:
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
    plt.plot(multiplier*monthlyData[energyType][indices['PVC'], dummyRange]-multiplier*monthlyData[energyType][indices[energyType], dummyRange], label = 'optimized for PV and C', color='b', alpha = 0.5)
    if not indices['45']==None:
        plt.plot(multiplier*monthlyData[energyType][indices['45'],:]-multiplier*monthlyData[energyType][indices[energyType], dummyRange], label = 'fixed at 45 deg', color='y')
    plt.ylabel('Energy Difference [kWh]')
    plt.legend()

    ax2.xaxis.set_major_locator(majorLocator)
    ax2.xaxis.set_major_formatter(majorFormatter)
    ax2.xaxis.set_minor_locator(minorLocator)
#    ax2.xaxis.set_minor_formatter(minorFormatter)
    plt.grid(True, which='both')
    
    return fig
    
def plotResultsComparison(monthlyData1, monthlyData2, indices, arg):
    """
    function that plots the energy according to arg for two different monthlyData sources
    """
    
    energyType = arg[0]    
    
    dummyRange = np.asarray(range(len(indices['E_tot1'])))
    
    fig = plt.figure(figsize=(16, 8))
    
#    plt.suptitle('Heating Demand (COP=' + str(usedEfficiencies['H_COP']) + ')')
    if energyType == 'PV':
        multiplier = -1
    else:
        multiplier = 1
    
    ax1 = plt.subplot(2,1,1)
    
    plt.plot(multiplier*monthlyData1[energyType][indices['E_tot1'], dummyRange], label = 'Results1', color='b')
    plt.plot(multiplier*monthlyData2[energyType][indices['E_tot2'], dummyRange], label = 'Results2', color='g')
    
    plt.ylabel('Energy [kWh]')
    plt.legend()
    
    majorLocator = MultipleLocator(24)
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(24)
    minorFormatter = FormatStrFormatter('%d')

    ax1.xaxis.set_major_locator(majorLocator)
    ax1.xaxis.set_major_formatter(majorFormatter)
    ax1.xaxis.set_minor_locator(minorLocator)
#    ax1.xaxis.set_minor_formatter(minorFormatter)
    plt.grid(True, which='both')
    
    ax2 = plt.subplot(2,1,2, sharex=ax1)
    
    plt.plot(multiplier*monthlyData1[energyType][indices['E_tot1'], dummyRange]-multiplier*monthlyData2[energyType][indices['E_tot2'], dummyRange], label = '1-2', color='b')

    plt.ylabel('Energy Difference [kWh]')
    plt.legend()

    ax2.xaxis.set_major_locator(majorLocator)
    ax2.xaxis.set_major_formatter(majorFormatter)
    ax2.xaxis.set_minor_locator(minorLocator)
#    ax2.xaxis.set_minor_formatter(minorFormatter)
    plt.grid(True, which='both')
    
    return fig

def plotEnergiesOpt(monthlyData, optIdx):
    """
    function that plots the energies of the monthlyData for the optimum index 
    given by optIdx
    """
    
    
    dummyRange = np.asarray(range(len(optIdx)))
    
    fig = plt.figure(figsize=(16, 8))
    
    plt.suptitle('Energy Comparison')
    ax1 = plt.subplot(1,1,1)
    plt.plot(monthlyData['H'][optIdx, dummyRange], label = 'H', color='r')
    plt.plot(monthlyData['C'][optIdx, dummyRange], label = 'C', color='b')
    plt.plot(monthlyData['L'][optIdx, dummyRange], label = 'L', color='g')
    plt.plot(monthlyData['PV'][optIdx, dummyRange], label = 'PV', color='c')
    plt.plot(monthlyData['E_HCL'][optIdx, dummyRange], label = 'HCL', color='m')
    plt.plot(monthlyData['E_tot'][optIdx, dummyRange], label = 'E_tot', color='k')
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
#    
#    ax2 = plt.subplot(2,1,2, sharex=ax1)
#    plt.plot(multiplier*monthlyData[energyType][indices['H'], dummyRange]-multiplier*monthlyData[energyType][indices[energyType], dummyRange], label = 'optimized for H', color='r')
#    plt.plot(multiplier*monthlyData[energyType][indices['C'], dummyRange]-multiplier*monthlyData[energyType][indices[energyType], dummyRange], label = 'optimized for C', color='b')
#    plt.plot(multiplier*monthlyData[energyType][indices['L'], dummyRange]-multiplier*monthlyData[energyType][indices[energyType], dummyRange], label = 'optimized for L', color='g')
#    plt.plot(multiplier*monthlyData[energyType][indices['PV'], dummyRange]-multiplier*monthlyData[energyType][indices[energyType], dummyRange], label = 'optimized for PV', color='c')
#    plt.plot(multiplier*monthlyData[energyType][indices['E_HCL'], dummyRange]-multiplier*monthlyData[energyType][indices[energyType], dummyRange], label = 'optimized for HCL', color='m')
#    plt.plot(multiplier*monthlyData[energyType][indices['E_tot'], dummyRange]-multiplier*monthlyData[energyType][indices[energyType], dummyRange], label = 'optimized for E_tot', color='k')
#    plt.plot(multiplier*monthlyData[energyType][indices['45'],:]-multiplier*monthlyData[energyType][indices[energyType], dummyRange], label = 'fixed at 45 deg', color='y')
#    plt.ylabel('Energy Difference [kWh]')
#    plt.legend()
#
#    ax2.xaxis.set_major_locator(majorLocator)
#    ax2.xaxis.set_major_formatter(majorFormatter)
#    ax2.xaxis.set_minor_locator(minorLocator)
##    ax2.xaxis.set_minor_formatter(minorFormatter)
#    plt.grid(True, which='both')
#    
    return fig
    
def create3Dplot(monthlyData, typeE, option, startMonth=1, endMonth=12, fig=None, ax=None ):
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    
    plotRange = range(24*(startMonth-1),24*endMonth)
#    plotRange = range(288)

    if option=='value':
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        x,y = np.shape(monthlyData[typeE][:,plotRange])
        X,Y = np.meshgrid(range(x),range(y))
        ax.plot_surface(X,Y,monthlyData[typeE][:,plotRange].transpose(), cmap = cm.cubehelix,rstride=1, cstride=1)
        plt.title('energy value' + typeE)
#    
    if option=='normalized':
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        x,y = np.shape(monthlyData[typeE][:,plotRange])
        X,Y = np.meshgrid(range(x),range(y))
        ax.plot_surface(X,Y,monthlyData[typeE][:,plotRange].transpose()/np.array(np.mean(monthlyData[typeE], axis=0))[plotRange, None], cmap = cm.cubehelix,rstride=1, cstride=1)
        plt.title('normalized energy by mean' + typeE)
        
    if option=='difference':
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        x,y = np.shape(monthlyData[typeE][:,plotRange])
        X,Y = np.meshgrid(range(x),range(y))
        ax.plot_surface(X,Y,monthlyData[typeE][:,plotRange].transpose()-np.array(np.mean(monthlyData[typeE], axis=0))[plotRange, None], cmap = cm.cubehelix,rstride=1, cstride=1)
        plt.title('energy difference to mean' + typeE)
    
    if option=='diffMin':
#        ax = fig.add_subplot(111, projection='3d')
        x,y = np.shape(monthlyData[typeE][:,plotRange])
        X,Y = np.meshgrid(range(x),range(y))
        ax.plot_surface(X,Y,-monthlyData[typeE][:,plotRange].transpose()+np.array(np.max(monthlyData[typeE], axis=0))[plotRange, None], cmap = cm.jet,rstride=1, cstride=1)
#        plt.title('energy difference to maximum' + typeE)
        plt.xlabel('combination')
        plt.ylabel('hour')
        ax.set_zlabel('Energy [kWh')

    if option=='diffMinCarpet':
        fig = plt.figure()
        ax = fig.add_subplot(111)
        x,y = np.shape(monthlyData[typeE][:,plotRange])
        X,Y = np.meshgrid(range(x),range(y))
        plt.pcolor(X,Y,-monthlyData[typeE][:,plotRange].transpose()+np.array(np.max(monthlyData[typeE], axis=0))[plotRange, None], cmap = 'jet')
        plt.title('energy difference to maximum' + typeE)
        plt.axis([X.min(), X.max(), Y.min(), Y.max()])
        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.85, 0.1, 0.05, 0.78])
        cbar = plt.colorbar(cax=cbar_ax)
        
    if option=='diffMinAltitude':
#        ax = fig.add_subplot(111, projection='3d')
        x,y = np.shape(monthlyData[typeE][:,plotRange])
        X,Y = np.meshgrid(range(x),range(y))
        ax.plot_surface(X*5,Y,-monthlyData[typeE][:,plotRange].transpose()+np.array(np.max(monthlyData[typeE], axis=0))[plotRange, None], cmap = cm.jet,rstride=1, cstride=1)
#        plt.title('energy difference to maximum' + typeE)
        plt.xlabel('Altitude [deg]')
        plt.ylabel('Hour')
        ax.set_zlabel('Energy [kWh]')
        
def plotMaxMinDiff(monthlyData):
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    indices = ['H','C','L','PV','E_tot']
    
    for i in indices:
        ax.plot(np.array(np.max(monthlyData[i], axis=0)-np.array(np.min(monthlyData[i], axis=0))), label = i, alpha = 0.5)
    plt.legend()
    
    plt.title('maximum difference by combination')

#plotMaxMinDiff(monthlyData)

#create3Dplot(monthlyData, 'E_tot', 'value')
#create3Dplot(monthlyData, 'E_tot', 'normalized')
#create3Dplot(monthlyData, 'E_tot', 'difference')#create3Dplot(monthlyData, 'E_tot', 'diffMin')
#create3Dplot(monthlyData, 'PV', 'diffMin')
#create3Dplot(monthlyData, 'H', 'diffMin')
#create3Dplot(monthlyData, 'C', 'diffMin')
#create3Dplot(monthlyData, 'L', 'diffMin')
#create3Dplot(monthlyData, 'C', 'value')
#create3Dplot(monthlyData, 'E_tot', 'diffMinCarpet')
#create3Dplot(monthlyData, 'PV', 'diffMinCarpet')
#create3Dplot(monthlyData, 'H', 'diffMinCarpet')
#create3Dplot(monthlyData, 'C', 'diffMinCarpet')
#create3Dplot(monthlyData, 'L', 'diffMinCarpet')
#

#create3Dplot(monthlyData, 'PV', 'difference')
#create3Dplot(monthlyData, 'H', 'difference')
#create3Dplot(monthlyData, 'C', 'difference')
#create3Dplot(monthlyData, 'L', 'difference')
#create3Dplot(monthlyData, 'C', 'value')



def plotTotEfixedY(monthlyData):
    """
    function to plot monthlyData for x-angle tracking
    """
    
    #assign x-angles (must be equally distributed between 0 and 90 deg)
    Xangles = np.array(range(len(monthlyData['angles']['x_angles'])))*90./(len(monthlyData['angles']['x_angles'])-1)
    
    fig = plt.figure()
    ax1=plt.subplot(2,1,1)
    plt.plot(Xangles, np.sum(monthlyData['H'], axis=1)/np.mean( np.sum(monthlyData['H'], axis=1)), label='H', color='r')
    plt.plot(Xangles, np.sum(monthlyData['C'], axis=1)/np.mean( np.sum(monthlyData['C'], axis=1)), label='C', color='b')
    plt.plot(Xangles, np.sum(monthlyData['L'], axis=1)/np.mean( np.sum(monthlyData['L'], axis=1)), label='L', color='g')
    plt.plot(Xangles, np.sum(monthlyData['PV'], axis=1)/np.mean( np.sum(monthlyData['PV'], axis=1)), label='PV', color='c')
    plt.plot(Xangles, np.sum(monthlyData['E_HCL'], axis=1)/np.mean( np.sum(monthlyData['E_HCL'], axis=1)), label='E_HCL', color='m')
    plt.plot(Xangles, np.sum(monthlyData['E_tot'], axis=1)/np.mean( np.sum(monthlyData['E_tot'], axis=1)), label='E_tot', color='k')
    plt.legend()
    
    plt.subplot(2,1,2, sharex=ax1)
    plt.plot(Xangles, np.sum(monthlyData['H'], axis=1), label='H', color='r')
    plt.plot(Xangles, np.sum(monthlyData['C'], axis=1), label='C', color='b')
    plt.plot(Xangles, np.sum(monthlyData['L'], axis=1), label='L', color='g')
    plt.plot(Xangles, np.sum(monthlyData['PV'], axis=1), label='PV', color='c')
    plt.plot(Xangles, np.sum(monthlyData['E_HCL'], axis=1), label='E_HCL', color='m')
    plt.plot(Xangles, np.sum(monthlyData['E_tot'], axis=1), label='E_tot', color='k')
    plt.legend()
    
    return fig
    
    
#tryout:

#plotTotEfixedY(monthlyData)



def plotTotEfixedX(monthlyData):
    """
    function to plot monthlyData for x-angle tracking
    """
    
    #assign x-angles (must be equally distributed between 0 and 90 deg)
    Xangles = (np.array(range(len(monthlyData['angles']['y_angles'])))-10)*90./(len(monthlyData['angles']['y_angles'])-1)
    
    fig = plt.figure()
    ax1=plt.subplot(2,1,1)
    plt.plot(Xangles, np.sum(monthlyData['H'], axis=1)/np.mean( np.sum(monthlyData['H'], axis=1)), label='H', color='r')
    plt.plot(Xangles, np.sum(monthlyData['C'], axis=1)/np.mean( np.sum(monthlyData['C'], axis=1)), label='C', color='b')
    plt.plot(Xangles, np.sum(monthlyData['L'], axis=1)/np.mean( np.sum(monthlyData['L'], axis=1)), label='L', color='g')
    plt.plot(Xangles, np.sum(monthlyData['PV'], axis=1)/np.mean( np.sum(monthlyData['PV'], axis=1)), label='PV', color='c')
    plt.plot(Xangles, np.sum(monthlyData['E_HCL'], axis=1)/np.mean( np.sum(monthlyData['E_HCL'], axis=1)), label='E_HCL', color='m')
    plt.plot(Xangles, np.sum(monthlyData['E_tot'], axis=1)/np.mean( np.sum(monthlyData['E_tot'], axis=1)), label='E_tot', color='k')
    plt.legend()
    
    plt.subplot(2,1,2, sharex=ax1)
    plt.plot(Xangles, np.sum(monthlyData['H'], axis=1), label='H', color='r')
    plt.plot(Xangles, np.sum(monthlyData['C'], axis=1), label='C', color='b')
    plt.plot(Xangles, np.sum(monthlyData['L'], axis=1), label='L', color='g')
    plt.plot(Xangles, np.sum(monthlyData['PV'], axis=1), label='PV', color='c')
    plt.plot(Xangles, np.sum(monthlyData['E_HCL'], axis=1), label='E_HCL', color='m')
    plt.plot(Xangles, np.sum(monthlyData['E_tot'], axis=1), label='E_tot', color='k')
    plt.legend()
    
    return fig
    

def AngleHistogram(X,rotation_axis,x_angles,x_angle_location,y_angles,y_angle_location,allAngles):
    """
    function that shows histograms of angle combinations for one axis
    """
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
    
    
def plotAngleSavings(monthlyData, xy = None):
    """
    Function that is showing the cumulative benefit of each angle, when it is at 
    the optimum position.
    """
    
    energies = ['H','C','L','PV','E_tot']
    
    fig = plt.figure()
    for energy in energies:
        minInd = np.argmin(monthlyData[energy], axis=0)
        minMax = np.max(monthlyData[energy], axis=0)-np.min(monthlyData[energy], axis=0)
    
        angleSavings = np.zeros([len(monthlyData['angles']['allAngles'][0]),1])
        angleFrequency = np.zeros([len(monthlyData['angles']['allAngles'][0]),1])
        
        for i in range(len(minInd)):
            angleSavings[minInd[i]] += minMax[i]
            angleFrequency[minInd[i]] += 1
            
        ax1=plt.subplot(2,1,1)
        if xy == None:
            ax1.plot(np.array(range(len(angleSavings))), angleSavings, label=energy)
            
        elif xy == 'x':
            ax1.plot(np.array(range(len(angleSavings)))*5, angleSavings, label=energy)
            
        elif xy=='y':
            ax1.plot(np.array(range(len(angleSavings)))*5-45, angleSavings, label=energy)
            
        ax2 = plt.subplot(2,1,2)
        if xy == None:
            ax2.plot(np.array(range(len(angleFrequency))), angleFrequency, label=energy)
            
        elif xy == 'x':
            ax2.plot(np.array(range(len(angleFrequency)))*5, angleFrequency, label=energy)
            
        elif xy=='y':
            ax2.plot(np.array(range(len(angleFrequency)))*5-45, angleFrequency, label=energy)
            
        
    ax1.legend()
    ax1.grid()
    ax1.set_ylabel('Energy Savings Potential [kWh]')
    ax2.legend()
    ax2.set_ylabel('Frequency [-]')
    ax2.set_xlabel('angle [deg]')    
    ax2.grid()
