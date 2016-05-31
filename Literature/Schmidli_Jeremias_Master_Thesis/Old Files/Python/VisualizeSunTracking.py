# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 13:00:21 2016

visualize sun tracking angles

@author: Jeremias

"""

def VisualizeSunTrackingAngles(SunTrackingData, rotation_axis):
    
#    if len(arg)==0:
#        max_min = 'min'
#    else:
#        max_min = arg[0]
#        
#    axis_ind =[]
#    
#    if max_min == 'min':
#        ind=np.argmin(X,axis=0)
#    elif max_min == 'max':
#        ind=np.argmax(X,axis=0)
#    else:
#        print "somehow max min is not working"


#    z_min=0
#    if rotation_axis == 'x':
#        for i in range(len(ind)):
#            axis_ind.append(x_angle_location[ind[i]])
#            z_max=max(x_angle_location)
#    elif rotation_axis == 'y':
#        for i in range(len(ind)):
#            axis_ind.append(y_angle_location[ind[i]])
#            z_max=max(y_angle_location)
#    elif rotation_axis == 'xy':
#        axis_ind = ind
#        z_max=len(allAngles[0])-1
#    else:
#        print 'axis not available'
    dx, dy = 1, 1
    
    # generate 2 2d grids for the x & y bounds
    y, x = np.mgrid[slice(0, 24 + dy, dy),
                    slice(0, 12 + dx, dx)]
#    z=[]
#    for i in range(24):
#        z.append([])
#        for j in range(12):
#            z[i].append(axis_ind[24*j + i])
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
        
    #z_mask = np.ones((24, 12), dtype=bool)
    z_mask = np.isnan(z)
    masked_array = np.ma.array(z, mask=z_mask)
    cmap = plt.cm.cubehelix
    cmap.set_bad('grey',1.)
    
   # z_min, z_max = 0, len()
    #print z_min, z_max
    
    #plt.pcolor(x, y, z, cmap='jet', vmin=z_min, vmax=z_max)
    plt.pcolormesh(x, y, masked_array, cmap=cmap, vmin=z_min, vmax=z_max)

    #plt.pcolor(x, y, z, cmap='CMRmap', vmin=z_min, vmax=z_max)

    #plt.pcolor(x, y, z, cmap='nipy_spectral', vmin=z_min, vmax=z_max)

    #plt.title('pcolor')
#    plt.xlabel("Day of the Year")
#    plt.ylabel("Hour of the Day")
    # set the limits of the plot to the limits of the data
    plt.axis([x.min(), x.max(), 3, 22])
    plt.colorbar()
    plt.tick_params(axis=u'both',labelsize=14)
    
#    cbar_ax = plt.add_axes([0.85, 0.15, 0.05, 0.7])
#    cbar = plt.colorbar(cax=cbar_ax)
#    cbar.ax.set_yticklabels(allAngles[0])
    
fig = plt.figure()
plt.subplot(2,1,1)
VisualizeSunTrackingAngles(SunTrackingData, 'x')
#cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#cbar = plt.colorbar(cax=cbar_ax)
plt.subplot(2,1,2)
VisualizeSunTrackingAngles(SunTrackingData, 'y')
#cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#cbar = plt.colorbar(cax=cbar_ax)
