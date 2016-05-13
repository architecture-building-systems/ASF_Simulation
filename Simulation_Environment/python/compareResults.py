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
OrientationStudy = True
EnergySavingsPotential = False
combinationStudy = True
ClusterStudy = True

roomSize = 30.0

# assign results folders to compare:
resultsFolder1 = 'Kloten_2clust_5x_1y'

resultsFolder2 = 'Kloten_25comb'




# set folders with orientation results 
OrientationFolders = {}

OrientationFolders['W'] = 'Kloten_25comb_W'
OrientationFolders['SW'] = 'Kloten_25comb_SW'
OrientationFolders['S'] = 'Kloten_25comb_largeContext'
OrientationFolders['SE'] = 'Kloten_25comb_SE_flipped'
OrientationFolders['E'] = 'Kloten_25comb_E_flipped'

OrientationFoldersNoShade = {}

OrientationFoldersNoShade['W'] = 'Kloten_noShade_W'
OrientationFoldersNoShade['SW'] = 'Kloten_noShade_SW'
OrientationFoldersNoShade['S'] = 'Kloten_noShade_basecase'
OrientationFoldersNoShade['SE'] = 'Kloten_noShade_SE'
OrientationFoldersNoShade['E'] = 'Kloten_noShade_E'

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

efficiencyFoldersNoShade = {}

efficiencyFoldersNoShade['CCOP1'] = 'Kloten_noShade_CCOP1'
efficiencyFoldersNoShade['CCOP2'] = 'Kloten_noShade_CCOP2'
efficiencyFoldersNoShade['CCOP3'] = 'Kloten_noShade_basecase'
efficiencyFoldersNoShade['CCOP4'] = 'Kloten_noShade_CCOP4'
efficiencyFoldersNoShade['CCOP5'] = 'Kloten_noShade_CCOP5'
efficiencyFoldersNoShade['CCOP6'] = 'Kloten_noShade_CCOP6'
efficiencyFoldersNoShade['CCOP7'] = 'Kloten_noShade_CCOP7'
efficiencyFoldersNoShade['CCOP8'] = 'Kloten_noShade_CCOP8'
efficiencyFoldersNoShade['CCOP9'] = 'Kloten_noShade_CCOP9'
efficiencyFoldersNoShade['CCOP10'] = 'Kloten_noShade_CCOP10'

efficiencyFoldersNoShade['HCOP1'] = 'Kloten_noShade_HCOP1'
efficiencyFoldersNoShade['HCOP2'] = 'Kloten_noShade_HCOP2'
efficiencyFoldersNoShade['HCOP3'] = 'Kloten_noShade_HCOP3'
efficiencyFoldersNoShade['HCOP4'] = 'Kloten_noShade_basecase'
efficiencyFoldersNoShade['HCOP5'] = 'Kloten_noShade_HCOP5'
efficiencyFoldersNoShade['HCOP6'] = 'Kloten_noShade_HCOP6'
efficiencyFoldersNoShade['HCOP7'] = 'Kloten_noShade_HCOP7'
efficiencyFoldersNoShade['HCOP8'] = 'Kloten_noShade_HCOP8'
efficiencyFoldersNoShade['HCOP9'] = 'Kloten_noShade_HCOP9'
efficiencyFoldersNoShade['HCOP10'] = 'Kloten_noShade_HCOP10'

efficiencyFoldersNoShade['L3'] = 'Kloten_noShade_L3'
efficiencyFoldersNoShade['L6'] = 'Kloten_noShade_L6'
efficiencyFoldersNoShade['L9'] = 'Kloten_noShade_L9'
efficiencyFoldersNoShade['L11.74'] = 'Kloten_noShade_basecase'
efficiencyFoldersNoShade['L15'] = 'Kloten_noShade_L15'

efficiencyFoldersNoShade['PV08'] = 'Kloten_noShade_basecase'
efficiencyFoldersNoShade['PV09'] = 'Kloten_noShade_basecase'
efficiencyFoldersNoShade['PV10'] = 'Kloten_noShade_basecase'
efficiencyFoldersNoShade['PV11'] = 'Kloten_noShade_basecase'
efficiencyFoldersNoShade['PV12'] = 'Kloten_noShade_basecase'
efficiencyFoldersNoShade['PV13'] = 'Kloten_noShade_basecase'
efficiencyFoldersNoShade['PV15'] = 'Kloten_noShade_basecase'
efficiencyFoldersNoShade['PV20'] = 'Kloten_noShade_basecase'
efficiencyFoldersNoShade['PV25'] = 'Kloten_noShade_basecase'

# set folders with combination results 
combinationFolders = {}

combinationFolders['22.5degx'] = 'Kloten_1x_1y_22.5deg'
combinationFolders['2x'] = 'Kloten_2x_1y'
combinationFolders['3x'] = 'Kloten_3x_1y'
combinationFolders['9'] = 'Kloten_3x_3y'
combinationFolders['5x'] = 'Kloten_5x_1y'
combinationFolders['5y22.5'] = 'Kloten_1x_5y_22.5deg'
combinationFolders['5y45'] = 'Kloten_1x_5y_45deg'
combinationFolders['19x'] = 'Kloten_19x_1y_1Infilt'
combinationFolders['25'] = 'Kloten_25comb_1Infilt'
combinationFolders['19x'] = 'Kloten_19x_1y_1Infilt'
combinationFolders['19y'] = 'Kloten_1x_19y_1Infilt'
combinationFolders['91'] = 'Kloten_7x_13y_1Infilt'
combinationFolders['49'] = 'Kloten_49comb'

# set infiltration folders:

infiltrationFolders = {}

infiltrationFolders['0.5'] = 'Kloten_25comb_0.5Infilt'
infiltrationFolders['0.75'] = 'Kloten_25comb_0.75Infilt'
infiltrationFolders['1'] = 'Kloten_25comb_1Infilt'
infiltrationFolders['1.25'] = 'Kloten_25comb_1.25Infilt'
infiltrationFolders['1.5'] = 'Kloten_25comb_1.5Infilt'

infiltrationFoldersNoShade = {}

infiltrationFoldersNoShade['0.5'] = 'Kloten_noShade_0.5Infilt'
infiltrationFoldersNoShade['0.75'] = 'Kloten_noShade_0.75Infilt'
infiltrationFoldersNoShade['1'] = 'Kloten_noShade_1Infilt'
infiltrationFoldersNoShade['1.25'] = 'Kloten_noShade_1.25Infilt'
infiltrationFoldersNoShade['1.5'] = 'Kloten_noShade_1.5Infilt'


#set folders with cluster analysis
clusterFolders ={}

clusterFolders['1clust'] = 'Kloten_4months_10panels_25comb'
clusterFolders['2clust'] = 'Kloten_2clust_25comb_4months'


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
        
    noShadeResults = {}
    for key, item in efficiencyFoldersNoShade.iteritems():
        noShadeResults[key] =  np.load(paths['results'] + '\\' + item + '\\all_results.npy').item()['TradeoffResults']
        
        
        
    ############ Heating Plots ####################

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
    
    ax1 = plt.subplot(2,7,1)
    
    rects1 = ax1.bar(ind, E/roomSize, width, color='red', alpha = 0.3) 

    # add some text for labels, title and axes ticks
    ax1.set_ylabel('Energy Savings per room area compared to facade at 45 deg [kWh/m2]')
    ax1.set_title('Sensitivity on Heating COP')
    
    ax1.set_xticks(ind+0.25)
    ax1.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']  )
    ax1.set_xlabel('Heating COP [-]')
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend()
    
    
    
    
    
    # number of bars
    N = 10
    
    # empty list for results
    E = []

    # fill result lists
    for i in ['HCOP1', 'HCOP2', 'HCOP3', 'HCOP4', 'HCOP5', 'HCOP6', 'HCOP7', 'HCOP8', 'HCOP9', 'HCOP10']:

        E.append(-results[i]['energy_opttot']['E_tot'] + noShadeResults[i]['energy_opttot']['E_tot'])
        
    # convert to numpy array
    E = np.array(E)
    
    
    ind = np.arange(N)-0.25  # the x locations for the groups
    width = 0.5       # the width of the bars
        
    ax2 = plt.subplot(2,7,8)
    
    rects1 = ax2.bar(ind, E/roomSize, width, color='red', alpha = 0.3) 

    # add some text for labels, title and axes ticks
    ax2.set_ylabel('Energy Savings per room area compared to no facade [kWh/m2]')
    ax2.set_title('Sensitivity on Heating COP')
    
    ax2.set_xticks(ind+0.25)
    ax2.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']  )
    ax2.set_xlabel('Heating COP [-]')
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend()
    
    
    
    
    
    
    
    ############ Cooling Plots ####################

    
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
    
    ax = plt.subplot(2,7,2, sharey=ax1)
    
    rects1 = ax.bar(ind, E/roomSize, width, color='blue', alpha = 0.3) 

    # add some text for labels, title and axes ticks
    ax.set_title('Sensitivity on Cooling COP')
    
    ax.set_xticks(ind+0.25)
    ax.set_xticklabels( ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] )
    ax.set_xlabel('Cooling COP [-]')
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend()



    # number of bars
    N = 10
    
    # empty list for results
    E = []

    # fill result lists
    for i in ['CCOP1', 'CCOP2', 'CCOP3', 'CCOP4', 'CCOP5', 'CCOP6', 'CCOP7', 'CCOP8', 'CCOP9', 'CCOP10']:

        E.append(-results[i]['energy_opttot']['E_tot'] + noShadeResults[i]['energy_opttot']['E_tot'])
        
    # convert to numpy array
    E = np.array(E)
    
    
    ind = np.arange(N)-0.25  # the x locations for the groups
    width = 0.5       # the width of the bars
    
    ax = plt.subplot(2,7,9, sharey=ax2)
    
    rects1 = ax.bar(ind, E/roomSize, width, color='blue', alpha = 0.3) 

    # add some text for labels, title and axes ticks
    ax.set_title('Sensitivity on Cooling COP')
    
    ax.set_xticks(ind+0.25)
    ax.set_xticklabels( ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] )
    ax.set_xlabel('Cooling COP [-]')
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend()
    
    
    
    
    
    
    ############ Lighting Plots ####################

    
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
    
    ax = plt.subplot(2,7,3, sharey=ax1)
    
    rects1 = ax.bar(ind, E/roomSize, width, color='green', alpha = 0.3) 

    # add some text for labels, title and axes ticks
    ax.set_title('Sensitivity on Lighting Load')
    
    ax.set_xticks(ind+0.25)
    ax.set_xticklabels(['3', '6', '9', '11.74', '15'] )
    ax.set_xlabel('Lighting Load [W/m2]')
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend()
    
    
    # number of bars
    N = 5
    
    # empty list for results
    E = []

    # fill result lists
#    for i in ['L5', 'L10', 'L15', 'L20']:

    for i in ['L3', 'L6', 'L9', 'L11.74', 'L15']:

        E.append(-results[i]['energy_opttot']['E_tot'] + noShadeResults[i]['energy_opttot']['E_tot'])
        
    # convert to numpy array
    E = np.array(E)
    
    
    ind = np.arange(N)-0.25  # the x locations for the groups
    width = 0.5       # the width of the bars
    
    ax = plt.subplot(2,7,10, sharey=ax2)
    
    rects1 = ax.bar(ind, E/roomSize, width, color='green', alpha = 0.3) 

    # add some text for labels, title and axes ticks
    ax.set_title('Sensitivity on Lighting Load')
    
    ax.set_xticks(ind+0.25)
    ax.set_xticklabels(['3', '6', '9', '11.74', '15'] )
    ax.set_xlabel('Lighting Load [W/m2]')
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend()
    
    
    
    
    
    ############ PV Plots ####################
    
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
    
    ax = plt.subplot(2,7,4, sharey=ax1)
    
    rects1 = ax.bar(ind, E/roomSize, width, color='cyan', alpha = 0.3) 

    # add some text for labels, title and axes ticks
    ax.set_title('Sensitivity on Average PV Efficiency')
    
    ax.set_xticks(ind+0.25)
    ax.set_xticklabels( ['8', '9', '10', '11', '12', '13', '15', '20', '25'] )
    ax.set_xlabel('PV Efficiency [%]')
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend()




    # number of bars
    N = 9
    
    # empty list for results
    E = []

    # fill result lists
    for i in ['PV08', 'PV09', 'PV10', 'PV11', 'PV12', 'PV13', 'PV15', 'PV20', 'PV25']:

        E.append(-results[i]['energy_opttot']['E_tot'] + noShadeResults[i]['energy_opttot']['E_tot'])
        
    # convert to numpy array
    E = np.array(E)
    
    
    ind = np.arange(N)-0.25  # the x locations for the groups
    width = 0.5       # the width of the bars
    
    ax = plt.subplot(2,7,11, sharey=ax2)
    
    rects1 = ax.bar(ind, E/roomSize, width, color='cyan', alpha = 0.3) 

    # add some text for labels, title and axes ticks
    ax.set_title('Sensitivity on Average PV Efficiency')
    
    ax.set_xticks(ind+0.25)
    ax.set_xticklabels( ['8', '9', '10', '11', '12', '13', '15', '20', '25'] )
    ax.set_xlabel('PV Efficiency [%]')
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend()    
    
    
    
    
    
    ########################### Orientation Plots ###############################
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
    
    ax = plt.subplot(2,7,5, sharey=ax1)
    
    rects1 = ax.bar(ind, E/roomSize, width, color='black', alpha = 0.3) 

    # add some text for labels, title and axes ticks

    ax.set_title('Sensitivity on Building Orientation')
    
    ax.set_xticks(ind+0.25)
    ax.set_xticklabels( ['W', 'SW', 'S', 'SE', 'E'] , rotation='vertical' )
    ax.set_xlabel('Building Orientation')
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend() 
    
    
    
    
    for key, item in OrientationFoldersNoShade.iteritems():
        print key, item
        noShadeResults[key] = np.load(paths['results'] + '\\' + item + '\\all_results.npy').item()['TradeoffResults']
        
     # number of bars
    N = 5
    
    # empty list for results
    E = []

    # fill result lists
    for i in  ['W', 'SW', 'S', 'SE', 'E']:

        E.append(-results[i]['energy_opttot']['E_tot'] + noShadeResults[i]['energy_opttot']['E_tot'])
        
    # convert to numpy array
    E = np.array(E)
    
    
    ind = np.arange(N)-0.25  # the x locations for the groups
    width = 0.5       # the width of the bars
    
    ax = plt.subplot(2,7,12, sharey=ax2)
    
    rects1 = ax.bar(ind, E/roomSize, width, color='black', alpha = 0.3) 

    # add some text for labels, title and axes ticks

    ax.set_title('Sensitivity on Building Orientation')
    
    ax.set_xticks(ind+0.25)
    ax.set_xticklabels( ['W', 'SW', 'S', 'SE', 'E'] , rotation='vertical' )
    ax.set_xlabel('Building Orientation')
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend() 
    
    
    
    
    ################ Combinations Plots #########################
    
    for key, item in combinationFolders.iteritems():
        print key, item
        results[key] = np.load(paths['results'] + '\\' + item + '\\all_results.npy').item()['TradeoffResults']
        
     # number of bars
#    N = 5
    N = 12
    
    # empty list for results
    E = []

    # fill result lists
    for i in  ['22.5degx','2x','3x','9','5x','5y22.5','5y45','19x', '19y', '25', '49', '91']:# ['19x', '19y', '25', '49', '91']:

        E.append(-results[i]['energy_opttot']['E_tot'] + results['25']['energy_45']['E_tot'])
        
    # convert to numpy array
    E = np.array(E)
    
    
    ind = np.arange(N)-0.25  # the x locations for the groups
    width = 0.5       # the width of the bars
    
    ax = plt.subplot(2,7,6, sharey=ax1)
    
    rects1 = ax.bar(ind, E/roomSize, width, color='orange', alpha = 0.3) 

    # add some text for labels, title and axes ticks

    ax.set_title('Sensitivity on Simulation Combination')
    
    ax.set_xticks(ind+0.25)
#    ax.set_xticklabels( ['19/0', '0/19', '5/5', '7/7', '13/7'], rotation='vertical' )
    ax.set_xticklabels(  ['22.5degx','2x','3x','9','5x','5y22.5','5y45','19x', '19y', '25', '49', '91'], rotation='vertical' )

    ax.set_xlabel('azimuth/altitude')
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    
    
    
    plt.legend()
    
     # number of bars
#    N = 5
    N = 12
    
    # empty list for results
    E = []

    # fill result lists
    for i in   ['22.5degx','2x','3x','9','5x','5y22.5','5y45','19x', '19y', '25', '49', '91']:#['19x', '19y', '25', '49', '91']:

        E.append(-results[i]['energy_opttot']['E_tot'] + noShadeResults['CCOP3']['energy_opttot']['E_tot'])
        
    # convert to numpy array
    E = np.array(E)
    
    
    ind = np.arange(N)-0.25  # the x locations for the groups
    width = 0.5       # the width of the bars
    
    ax = plt.subplot(2,7,13, sharey=ax2)
    
    rects1 = ax.bar(ind, E/roomSize, width, color='orange', alpha = 0.3) 

    # add some text for labels, title and axes ticks

    ax.set_title('Sensitivity on Simulation Combination')
    
    ax.set_xticks(ind+0.25)
#    ax.set_xticklabels( ['19/0', '0/19', '5/5', '7/7', '13/7'], rotation='vertical' )
    ax.set_xticklabels(  ['22.5degx','2x','3x','9','5x','5y22.5','5y45','19x', '19y', '25', '49', '91'], rotation='vertical' )
    ax.set_xlabel('azimuth/altitude')
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend()
        
        
        
        
        
    ####################### Infiltration Plots ##########################


    resultsInfilt = {}
    for key, item in infiltrationFolders.iteritems():
        resultsInfilt[key] = np.load(paths['results'] + '\\' + item + '\\all_results.npy').item()['TradeoffResults']
        
    noShadeResultsInfilt = {}
    for key, item in infiltrationFoldersNoShade.iteritems():
        noShadeResultsInfilt[key] =  np.load(paths['results'] + '\\' + item + '\\all_results.npy').item()['TradeoffResults']    
    
    # number of bars
    N = 5
    
    # empty list for results
    E = []

    # fill result lists

    for i in ['0.5', '0.75', '1', '1.25', '1.5']:

        E.append(-resultsInfilt[i]['energy_opttot']['E_tot'] + resultsInfilt[i]['energy_45']['E_tot'])
        
    # convert to numpy array
    E = np.array(E)
    
    
    ind = np.arange(N)-0.25  # the x locations for the groups
    width = 0.5       # the width of the bars
    
    ax = plt.subplot(2,7,7, sharey=ax1)
    
    rects1 = ax.bar(ind, E/roomSize, width, color='indigo', alpha = 0.3) 

    # add some text for labels, title and axes ticks
    ax.set_title('Sensitivity on Infiltration Rate')
    
    ax.set_xticks(ind+0.25)
    ax.set_xticklabels( ['0.5', '0.75', '1', '1.25', '1.5'] )
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend()
    
    
    # number of bars
    N = 5
    
    # empty list for results
    E = []

    # fill result lists
#    for i in ['L5', 'L10', 'L15', 'L20']:

    for i in  ['0.5', '0.75', '1', '1.25', '1.5']:

        E.append(-resultsInfilt[i]['energy_opttot']['E_tot'] + noShadeResultsInfilt[i]['energy_opttot']['E_tot'])
        
    # convert to numpy array
    E = np.array(E)
    
    
    ind = np.arange(N)-0.25  # the x locations for the groups
    width = 0.5       # the width of the bars
    
    ax = plt.subplot(2,7,14, sharey=ax2)
    
    rects1 = ax.bar(ind, E/roomSize, width, color='indigo', alpha = 0.3) 

    # add some text for labels, title and axes ticks
    ax.set_title('Sensitivity on Infiltration Rate')
    
    ax.set_xticks(ind+0.25)
    ax.set_xticklabels( ['0.5', '0.75', '1', '1.25', '1.5'] )
    ax.set_xlabel('Infiltration Rate [1/h]')
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend()
    
    plt.show()
    
    if combinationStudy:
        
        
            #results1 = np.load(paths['results'] + '\\' + resultsFolder1 + '\\all_results.npy').item()
            #results2 = np.load(paths['results'] + '\\' + resultsFolder2 + '\\all_results.npy').item()
    
        combinationResults = {}
        for key, item in combinationFolders.iteritems():
            print key, item
            combinationResults[key] = np.load(paths['results'] + '\\' + item + '\\all_results.npy').item()['TradeoffResults']['energy_opttot']
        
        # number of bars
        N = 12
        
        # empty list for results
        H = []
        C = []
        L = []
        PV = []
        E = []
    
        # fill result lists
        for i in ['22.5degx','2x','3x','9','5x','5y22.5','5y45','19x', '19y', '25', '49', '91']:
            
            H.append(combinationResults[i]['H'])
            C.append(combinationResults[i]['C'])
            L.append(combinationResults[i]['L'])
            PV.append(combinationResults[i]['PV'])
            E.append(combinationResults[i]['E_tot'])
            
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
        ax.set_xticklabels( ['22.5degx','2x','3x','9','5x','5y22.5','5y45','19x', '19y', '25', '49', '91'] )
        ax.set_xlabel('Building Orientation')
        plt.axhline(y=0, linewidth=1, color = 'k')
        plt.grid( axis = u'y')
        
        plt.legend()
        
        plt.show()
        

if ClusterStudy:

    # load results
    results1 = np.load(paths['results'] + '\\' + clusterFolders['1clust'] + '\\all_results.npy').item()
    results2 = np.load(paths['results'] + '\\' + clusterFolders['2clust'] + '\\all_results.npy').item()
    
    # plot data 
    figures = compareResultsFigure(results1['monthlyData'], results2['monthlyData'])