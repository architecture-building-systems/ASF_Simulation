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
  
   
    
    #x = range(start, end+1)
      
    x= TotalHOY
   
    
    fig = plt.figure(figsize=(8, 4))
    
    plt.style.use('ggplot')
    
    ax1 = fig.add_subplot(111)
    
    ax1.set_title(title, fontsize = 18)
    
    ax1.plot(x, E, 'k-')
    ax1.plot(x, PV, 'y-')
    ax1.plot(x, L, 'm-')
    ax1.plot(x, H, 'r-')
    ax1.plot(x, C, 'b-')
    ax1.set_xlabel('Hour of Year')
    ax1.set_yticks([-800,-400,0,400,800])
    #ax1.set_xticks(range(6,24,3))
    # Make the y-axis label and tick labels match the line color.
    ax1.set_ylabel('Net Energy Demand [Wh]', fontsize = 16)
    
    plt.legend(['E','PV','L','H', 'C'], loc = 3)
    
    
    ax2 = ax1.twinx()
    
    
    
    ax2.plot(x, x_angle, 'c--')
    ax2.plot(x, y_angle, 'k--')
    #ax2.set_ylabel('[deg]', fontsize = 16)
    ax2.set_yticks([-90,-45,0,45,90])
    
    plt.legend(['Altitude Angle','Azimuth Angle'], loc = 4)
    
    plt.legend(loc=2, fontsize = 6)    

    return fig