# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 17:14:42 2016

@author: Mauro
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

def carpetPlot(X, z_min, z_max, title):
    
        
    fig = plt.figure(figsize=(8, 4))
   
    z= np.reshape(X,(12,24)).T
    

    dx, dy = 1, 1
    
    # generate 2 2d grids for the x & y bounds:
    y, x = np.mgrid[slice(0, 24 + dy, dy),
                    slice(0, 12 + dx, dx)]
    
    
    # define the location of the middle number (where 0 is):
    z_middle = float(abs(z_min)) / (z_max-z_min) 
                
    cmap = LinearSegmentedColormap.from_list('mycmap', [(0, 'navy'),
                                                    (z_middle, 'white'),
                                                    (1, 'firebrick')])
    
    # define what happens to bad data (i.e. data outside the mask):
    cmap.set_bad('grey',1.)
    
    # create the carpet plot:
    plt.pcolormesh(x, y, z, cmap=cmap, vmin=z_min, vmax=z_max)
    
    # set the limits of the plot to the limits of the data
    plt.axis([x.min(), x.max(), 3, 22])
    plt.tick_params(axis=u'both',labelsize=14)
    plt.title(title)
    plt.xlabel("Month of the Year",size=14)
    plt.ylabel("Hour of the Day",size=14)
    
    
    #legend
    cbar = plt.colorbar()
    cbar.set_label('kWh')
        
    return fig
    
def carpetPlotAngles(X, z_min, z_max, title):
    
        
    fig = plt.figure(figsize=(4, 4))
   
    z= np.reshape(X,(12,24)).T
    

    dx, dy = 1, 1
    
    # generate 2 2d grids for the x & y bounds:
    y, x = np.mgrid[slice(0, 24 + dy, dy),
                    slice(0, 12 + dx, dx)]
    
        
    cmap = plt.cm.CMRmap
    cmap = plt.cm.gnuplot
    cmap = plt.cm.afmhot
    
        
    # define what happens to bad data (i.e. data outside the mask):
    cmap.set_bad('grey',1.)
    
    # create the carpet plot:
    plt.pcolormesh(x, y, z, cmap=cmap, vmin=z_min, vmax=z_max)
    
    # set the limits of the plot to the limits of the data
    plt.axis([x.min(), x.max(), 3, 22])
    plt.tick_params(axis=u'both',labelsize=14)
    plt.title(title)
    plt.xlabel("Month of the Year",size=14)
    plt.ylabel("Hour of the Day",size=14)
    
    
    #legend
    cbar = plt.colorbar()
    cbar.set_label('[deg]')
        
    return fig
    
def carpetPlotMask(X, z_min, z_max, title, hour_in_month):
    
        
    fig = plt.figure(figsize=(4, 4))
   
    z= np.reshape(X,(12,24)).T
    

    dx, dy = 1, 1
    
    # generate 2 2d grids for the x & y bounds:
    y, x = np.mgrid[slice(0, 24 + dy, dy),
                    slice(0, 12 + dx, dx)]
    
        
    
    
    # create array for carpet plots (False can be ignored)
    z3 = np.empty((24,12))*False
    
    # set values to True which correspond to hours with sun
    # and the hours with no sun to (False)
    for i in range(24):
       for j in range(1,13):
           if i in hour_in_month[j]:
               #sun                
               z3[i,j-1] = True
           else:
               #no sun
               z3[i,j-1] = False
               
    # set values to nan wihich are zero:
    z3[z3 == 0] = np.nan
    
    # create sun mask where True corresponds to no sun, all values with no sun will later be grey
    sunMask=np.isnan(z3)

    # create masked array from sunMask:
    masked_array = np.ma.array(z, mask=sunMask)
    
    # define colormap:
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
    plt.title(title)
    plt.xlabel("Month of the Year",size=14)
    plt.ylabel("Hour of the Day",size=14)
    
    
    #legend
    cbar = plt.colorbar()
    cbar.set_label('[deg]')
        
    return fig    