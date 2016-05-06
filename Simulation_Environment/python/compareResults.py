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

# set folders with orientation results 
OrientationFolders = {}

OrientationFolders['W'] = 'Kloten_25comb_SW'
OrientationFolders['SW'] = 'Kloten_25comb_SW'
OrientationFolders['S'] = 'Kloten_25comb_largeContext'
OrientationFolders['SE'] = 'Kloten_25comb_SE_flipped'
OrientationFolders['E'] = 'Kloten_25comb_SE_flipped'

# set folders with efficiency results
efficiencyFolders = {}

efficiencyFolders['CCOP1'] = 'Kloten_25comb_CCOP1'
efficiencyFolders['CCOP2'] = 'Kloten_25comb_CCOP2'
efficiencyFolders['CCOP3'] = 'Kloten_25comb_basecase'
efficiencyFolders['CCOP4'] = 'Kloten_25comb_CCOP4'
efficiencyFolders['CCOP5'] = 'Kloten_25comb_CCOP5'
efficiencyFolders['CCOP6'] = 'Kloten_25comb_CCOP6'
efficiencyFolders['CCOP7'] = 'Kloten_25comb_CCOP7'
efficiencyFolders['CCOP8'] = 'Kloten_25comb_CCOP8'
efficiencyFolders['CCOP9'] = 'Kloten_25comb_CCOP9'
efficiencyFolders['CCOP10'] = 'Kloten_25comb_CCOP10'

efficiencyFolders['HCOP1'] = 'Kloten_25comb_HCOP1'
efficiencyFolders['HCOP2'] = 'Kloten_25comb_HCOP2'
efficiencyFolders['HCOP3'] = 'Kloten_25comb_HCOP3'
efficiencyFolders['HCOP4'] = 'Kloten_25comb_basecase'
efficiencyFolders['HCOP5'] = 'Kloten_25comb_HCOP5'
efficiencyFolders['HCOP6'] = 'Kloten_25comb_HCOP6'
efficiencyFolders['HCOP7'] = 'Kloten_25comb_HCOP7'
efficiencyFolders['HCOP8'] = 'Kloten_25comb_HCOP8'
efficiencyFolders['HCOP9'] = 'Kloten_25comb_HCOP9'
efficiencyFolders['HCOP10'] = 'Kloten_25comb_HCOP10'

efficiencyFolders['L3'] = 'Kloten_25comb_L3'
efficiencyFolders['L5'] = 'Kloten_25comb_L5'
efficiencyFolders['L6'] = 'Kloten_25comb_L6'
efficiencyFolders['L9'] = 'Kloten_25comb_L9'
efficiencyFolders['L10'] = 'Kloten_25comb_L10'
efficiencyFolders['L11.74'] = 'Kloten_25comb_basecase'
efficiencyFolders['L15'] = 'Kloten_25comb_L15'
efficiencyFolders['L20'] = 'Kloten_25comb_L20'

efficiencyFolders['PV08'] = 'Kloten_25comb_PV0.8'
efficiencyFolders['PV09'] = 'Kloten_25comb_PV0.9'
efficiencyFolders['PV10'] = 'Kloten_25comb_basecase'
efficiencyFolders['PV11'] = 'Kloten_25comb_PV1.1'
efficiencyFolders['PV12'] = 'Kloten_25comb_PV1.2'
efficiencyFolders['PV13'] = 'Kloten_25comb_PV1.3'
efficiencyFolders['PV15'] = 'Kloten_25comb_PV1.5'
efficiencyFolders['PV20'] = 'Kloten_25comb_PV2'
efficiencyFolders['PV25'] = 'Kloten_25comb_PV2.5'

# set folders with combination results 
combinationFolders = {}

combinationFolders['25'] = 'Kloten_25comb_1Infilt'
combinationFolders['19x'] = 'Kloten_19x_1y_1Infilt'
combinationFolders['19y'] = 'Kloten_1x_19y_1Infilt'
combinationFolders['91'] = 'Kloten_7x_13y_1Infilt'
combinationFolders['49'] = 'Kloten_49comb_1Infilt'


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
    
if EnergySavingsPotential:
    

    results = {}
    for key, item in efficiencyFolders.iteritems():
        print key, item
        results[key] = np.load(paths['results'] + '\\' + item + '\\all_results.npy').item()['TradeoffResults']
        
        

    # number of bars
    N = 10
    
    # empty list for results
    E = []

    # fill result lists
    for i in ['HCOP1', 'HCOP2', 'HCOP3', 'HCOP4', 'HCOP5', 'HCOP6', 'HCOP7', 'HCOP8', 'HCOP9', 'HCOP10']:

        E.append(-results[i]['energy_opttot']['E_tot'] + results[i]['energy_45']['E_tot'])
        
    # convert to numpy array
    E = np.array(E)
    
    
    ind = np.arange(N)-0.25  # the x locations for the groups
    width = 0.5       # the width of the bars
    
    fig = plt.figure()
    
    ax = plt.subplot(1,6,1)
    
    rects1 = ax.bar(ind, E, width, color='red', alpha = 0.3) 

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Energy Savings [kWh]')
    ax.set_title('Sensitivity on Heating COP')
    
    ax.set_xticks(ind+0.25)
    ax.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']  )
    ax.set_xlabel('Heating COP [-]')
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend()
    
    
    
    
    plt.subplot(1,6,2)
    # number of bars
    N = 10
    
    # empty list for results
    E = []

    # fill result lists
    for i in ['CCOP1', 'CCOP2', 'CCOP3', 'CCOP4', 'CCOP5', 'CCOP6', 'CCOP7', 'CCOP8', 'CCOP9', 'CCOP10']:

        E.append(-results[i]['energy_opttot']['E_tot'] + results[i]['energy_45']['E_tot'])
        
    # convert to numpy array
    E = np.array(E)
    
    
    ind = np.arange(N)-0.25  # the x locations for the groups
    width = 0.5       # the width of the bars
    
    ax = plt.subplot(1,6,2, sharey=ax)
    
    rects1 = ax.bar(ind, E, width, color='blue', alpha = 0.3) 

    # add some text for labels, title and axes ticks
    ax.set_title('Sensitivity on Cooling COP')
    
    ax.set_xticks(ind+0.25)
    ax.set_xticklabels( ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] )
    ax.set_xlabel('Cooling COP [-]')
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend()



    
    
    plt.subplot(1,6,3)
    # number of bars
    N = 5
    
    # empty list for results
    E = []

    # fill result lists
#    for i in ['L5', 'L10', 'L15', 'L20']:

    for i in ['L3', 'L6', 'L9', 'L11.74', 'L15']:

        E.append(-results[i]['energy_opttot']['E_tot'] + results[i]['energy_45']['E_tot'])
        
    # convert to numpy array
    E = np.array(E)
    
    
    ind = np.arange(N)-0.25  # the x locations for the groups
    width = 0.5       # the width of the bars
    
    ax = plt.subplot(1,6,3, sharey=ax)
    
    rects1 = ax.bar(ind, E, width, color='green', alpha = 0.3) 

    # add some text for labels, title and axes ticks
    ax.set_title('Sensitivity on Lighting Load')
    
    ax.set_xticks(ind+0.25)
    ax.set_xticklabels(['3', '6', '9', '11.74', '15'] )
    ax.set_xlabel('Lighting Load [W/m2]')
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend()
    
    
    
    
    
    plt.subplot(1,6,4)
    # number of bars
    N = 9
    
    # empty list for results
    E = []

    # fill result lists
    for i in ['PV08', 'PV09', 'PV10', 'PV11', 'PV12', 'PV13', 'PV15', 'PV20', 'PV25']:

        E.append(-results[i]['energy_opttot']['E_tot'] + results[i]['energy_45']['E_tot'])
        
    # convert to numpy array
    E = np.array(E)
    
    
    ind = np.arange(N)-0.25  # the x locations for the groups
    width = 0.5       # the width of the bars
    
    ax = plt.subplot(1,6,4, sharey=ax)
    
    rects1 = ax.bar(ind, E, width, color='cyan', alpha = 0.3) 

    # add some text for labels, title and axes ticks
    ax.set_title('Sensitivity on Average PV Efficiency')
    
    ax.set_xticks(ind+0.25)
    ax.set_xticklabels( ['8', '9', '10', '11', '12', '13', '15', '20', '25'] )
    ax.set_xlabel('PV Efficiency [%]')
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend()
    
    
    for key, item in OrientationFolders.iteritems():
        print key, item
        results[key] = np.load(paths['results'] + '\\' + item + '\\all_results.npy').item()['TradeoffResults']
        
     # number of bars
    N = 5
    
    # empty list for results
    E = []

    # fill result lists
    for i in  ['W', 'SW', 'S', 'SE', 'E']:

        E.append(-results[i]['energy_opttot']['E_tot'] + results[i]['energy_45']['E_tot'])
        
    # convert to numpy array
    E = np.array(E)
    
    
    ind = np.arange(N)-0.25  # the x locations for the groups
    width = 0.5       # the width of the bars
    
    ax = plt.subplot(1,6,5, sharey=ax)
    
    rects1 = ax.bar(ind, E, width, color='black', alpha = 0.3) 

    # add some text for labels, title and axes ticks

    ax.set_title('Sensitivity on Building Orientation')
    
    ax.set_xticks(ind+0.25)
    ax.set_xticklabels( ['W', 'SW', 'S', 'SE', 'E'] , rotation='vertical' )
    ax.set_xlabel('Building Orientation')
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend() 
    
    
    for key, item in combinationFolders.iteritems():
        print key, item
        results[key] = np.load(paths['results'] + '\\' + item + '\\all_results.npy').item()['TradeoffResults']
        
     # number of bars
    N = 5
    
    # empty list for results
    E = []

    # fill result lists
    for i in  ['19x', '19y', '25', '49', '91']:

        E.append(-results[i]['energy_opttot']['E_tot'] + results['25']['energy_45']['E_tot'])
        
    # convert to numpy array
    E = np.array(E)
    
    
    ind = np.arange(N)-0.25  # the x locations for the groups
    width = 0.5       # the width of the bars
    
    ax = plt.subplot(1,6,6, sharey=ax)
    
    rects1 = ax.bar(ind, E, width, color='orange', alpha = 0.3) 

    # add some text for labels, title and axes ticks

    ax.set_title('Sensitivity on Building Orientation')
    
    ax.set_xticks(ind+0.25)
    ax.set_xticklabels( ['19 azim', '19 alt', '5 azim / 5 alt', '7 azim / 7 alt', '13 azim / 13 alt'], rotation='vertical' )
    ax.set_xlabel('Building Orientation')
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend()
        
    
    plt.show()