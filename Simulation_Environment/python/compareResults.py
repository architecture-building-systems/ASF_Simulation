# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 11:16:09 2016

Compare Results script

@author: Jeremias
"""

import numpy as np
import sys, os
import matplotlib.pyplot as plt

CompareResults = False
OrientationStudy = False
EnergySavingsPotential = True

# assign results folders to compare:
resultsFolder1 = 'Kloten_2clust_5x_1y'

resultsFolder2 = 'Kloten_25comb'


#OrientationFolders = {'W','SW','S','SE','E'}
OrientationFolders = {}

OrientationFolders['W'] = 'Kloten_25comb_SW'
OrientationFolders['SW'] = 'Kloten_25comb_SW'
OrientationFolders['S'] = 'Kloten_25comb_largeContext'
OrientationFolders['SE'] = 'Kloten_25comb_SE_flipped'
OrientationFolders['E'] = 'Kloten_25comb_SE_flipped'




# paths dict:
paths = {}

paths['main'] = os.path.dirname(os.path.dirname(sys.argv[0]))
paths['results'] = paths['main'] + '\\results'
paths['aux_functions'] = paths['main'] + '\\python\\aux_files'

# add python_path to system path, so that all files are available:
sys.path.insert(0, paths['aux_functions'])

from createFigures import compareResultsFigure

if CompareResults:
    # load results
    results1 = np.load(paths['results'] + '\\' + resultsFolder1 + '\\all_results.npy').item()
    results2 = np.load(paths['results'] + '\\' + resultsFolder2 + '\\all_results.npy').item()
    
    # plot data 
    figures = compareResultsFigure(results1['monthlyData'], results2['monthlyData'])
    
if OrientationStudy:
    
    
    #results1 = np.load(paths['results'] + '\\' + resultsFolder1 + '\\all_results.npy').item()
    #results2 = np.load(paths['results'] + '\\' + resultsFolder2 + '\\all_results.npy').item()
    
    results = {}
    for key, item in OrientationFolders.iteritems():
        print key, item
        results[key] = np.load(paths['results'] + '\\' + item + '\\all_results.npy').item()['TradeoffResults']['energy_opttot']
        
    # number of bars
    N = 5
    
    # empty list for results
    H = []
    C = []
    L = []
    PV = []
    E = []

    # fill result lists
    for i in ['W', 'SW', 'S', 'SE', 'E']:
        
        H.append(results[i]['H'])
        C.append(results[i]['C'])
        L.append(results[i]['L'])
        PV.append(results[i]['PV'])
        E.append(results[i]['E_tot'])
        
    # convert them to numpy arrays
    H = np.array(H)
    C = np.array(C)
    L = np.array(L)
    PV = np.array(PV)
    E = np.array(E)
    
    
    ind = np.arange(N) + .15 # the x locations for the groups
    width = 0.35       # the width of the bars
    
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, H, width, color='r', alpha = 0.3, label = 'heating') 
    rects2 = ax.bar(ind, C, width, color='b', alpha = 0.3, label = 'cooling', bottom = H) 
    rects3 = ax.bar(ind, L, width, color='g', alpha = 0.3, label = 'lighting', bottom = H+C)
    rects4 = ax.bar(ind, PV, width, color='cyan', alpha = 0.3, label = 'PV') 
    
    #TotE = (140, 90, 78, 65, 50)
    
    
    xtra_space = 0.0
    rects2 = ax.bar(ind + width + xtra_space , E, width, color='black', alpha = 0.3, label = 'total') 
    
    
    
    # add some text for labels, title and axes ticks
    ax.set_ylabel('Energy [kWh]')
    ax.set_title('Energy Dependency on Building Orientation')
    
    ax.set_xticks(ind+width+xtra_space)
    ax.set_xticklabels( ('W', 'SW', 'S', 'SE', 'E') )
    ax.set_xlabel('Building Orientation')
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend()
    
    plt.show()