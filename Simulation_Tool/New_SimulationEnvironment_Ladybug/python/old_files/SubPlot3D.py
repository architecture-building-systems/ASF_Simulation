# -*- coding: utf-8 -*-
"""
Created on Fri Dec 02 15:59:45 2016

@author: Assistenz
"""

import matplotlib.pyplot as plt

def SubPlotFunction(figures, start, end):
    
    fig = plt.figure(figsize=(16, 16))

    count = 1
    print figures
    
       
    plt.subplot(4,4,1)   
    figures[start]
    plt.subplot(4,4,2)   
    figures[start+1]
        
    return fig
    