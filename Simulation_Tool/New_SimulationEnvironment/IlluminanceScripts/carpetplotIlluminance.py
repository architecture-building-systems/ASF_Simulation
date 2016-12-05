# -*- coding: utf-8 -*-
"""
Created on Thu Nov 03 15:29:54 2016

@author: Assistenz
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.cm as cm


def carpetPlotIlluminance(z, z_min, z_max, title):
    
    y = range(8,19)
    x = range(0,13)

                   
    #cmap = LinearSegmentedColormap.from_list('mycmap', [(0, 'white'),(0.33, 'yellow'),(0.66, 'olive'),(1,'green')])

    #cmap = plt.cm.autumn
    #cmap = plt.cm.afmhot_r
    cmap = plt.cm.afmhot
    
    #cmap = LinearSegmentedColormap.from_list('mycmap', [(0, 'grey'), (1,'yellow')])
    
    cmap = cm.get_cmap('afmhot', 20)    # 11 discrete colors



    
    
    yy, xx = np.meshgrid(y,x)
    
    plt.style.use('ggplot')       
    # create the carpet plot:
    plt.pcolormesh(xx, yy, z, cmap=cmap, vmin=z_min, vmax=z_max)
    
    # set the limits of the plot to the limits of the data
    plt.tick_params(axis=u'both',labelsize=14)
    plt.title(title)
            
           
