# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 10:36:51 2016

@author: Mauro
"""

import os, sys
import numpy as np
import json
import time
import warnings
import csv
import matplotlib.pyplot as plt
import pandas as pd


import matplotlib as mpl
label_size = 14
mpl.rcParams['xtick.labelsize'] = label_size 
mpl.rcParams['ytick.labelsize'] = label_size 


def PlotHour(E, PV, L, H, C, x_angle, y_angle, start, end, title, TotalHOY):
    
    plt.style.use('seaborn-white')
    #plt.style.use('ggplot')
       

    x= TotalHOY
   
    z_max = round(max(E),-2)
    z_min = round(min(PV),-2)
    
    print 'z_max', z_max
    print 'z_min', z_min
    
    diff = z_max-z_min
    
    fig = plt.figure(figsize=(8, 4))
    
    ax1 = fig.add_subplot(111)
    
    ax1.set_title(title, fontsize = 18)
    
    lineW = 1
    
    ax1.plot(x, E, 'k-', linewidth = lineW)
    ax1.plot(x, PV, 'y-', linewidth = lineW)
    ax1.plot(x, L, 'm-', linewidth = lineW)
    ax1.plot(x, H, 'r-', linewidth = lineW)
    ax1.plot(x, C, 'b-', linewidth = lineW)
    ax1.set_xlabel('Hour of Day', fontsize = 16)
    #ax1.set_yticks([z_min,z_min + diff/4, z_min + 2* diff/4, z_max - diff/4, z_max])
    
    ax1.set_yticks([-800,-400,0,400,800,1200])
    #ax1.set_xticks(range(6,24,3))
    # Make the y-axis label and tick labels match the line color.
    ax1.set_ylabel('Net Energy Demand [Wh]', fontsize = 16)
    
    plt.legend(['E','PV','L','H', 'C'], loc = 3)
    plt.grid(True)
    
    ax2 = ax1.twinx()
 
    ax2.plot(x, x_angle, 'c--', linewidth = lineW)
    ax2.plot(x, y_angle, 'k--', linewidth = lineW)
    ax2.set_ylabel('[deg]', fontsize = 16)
    ax2.set_yticks([-90,-45,0,45,90])

    plt.legend(['Altitude Angle','Azimuth Angle'], loc = 4)
    
    plt.legend(loc=2, fontsize = 6)    

    
    gridlines = ax1.get_xgridlines() + ax1.get_ygridlines()
    for line in gridlines:
        line.set_linestyle('-.')
    
    
    
    ticklines = ax1.get_xticklines() + ax1.get_yticklines()


    for line in ticklines:
        line.set_linewidth(6)
    
    plt.tight_layout()
    
    plt.show()
    
    return fig