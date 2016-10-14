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
    # define what data should be plotted:
    
    
    #in kWh/m2, so divide through 8m2
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