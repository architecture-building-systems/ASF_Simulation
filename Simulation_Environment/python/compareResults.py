# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 11:16:09 2016

Compare Results script

@author: Jeremias
"""

import numpy as np
import sys, os
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter


CompareResults = False
OrientationStudy = True
LocationStudy = True
BuildingParameterStudy = False
EnergySavingsPotential = False
combinationStudy = False
ClusterStudy = False

roomSize = 34.3

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


# set folders with Location results 
LocationFolders = {}

LocationFolders['Helsinki'] = 'Helsinki_25comb'
LocationFolders['Zurich'] = 'Kloten_25comb_largeContext'
LocationFolders['Madrid'] = 'Madrid_25comb'
LocationFolders['Cairo'] = 'Cairo_25comb'


LocationFoldersNoShade = {}

LocationFoldersNoShade['Helsinki'] = 'Helsinki_noShade'
LocationFoldersNoShade['Zurich'] = 'Kloten_noShade_basecase'
LocationFoldersNoShade['Madrid'] = 'Madrid_noShade'
LocationFoldersNoShade['Cairo'] = 'Cairo_noShade'

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
#combinationFolders['91'] = 'Kloten_7x_13y_1Infilt'
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

clusterFolders['2clust_base'] = 'Kloten_4months_10panels_25comb'
clusterFolders['2clust'] = 'Kloten_2clust_25comb_4months'
clusterFolders['3clust_base'] = 'Kloten_4months_8panels_5x_1y'
clusterFolders['3clust'] = 'Kloten_4months_8panels_3clust_5x_1y'


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
    
    fig = plt.figure(figsize=(16,12))
    ax = plt.subplot(3,1,1)
    rects1 = ax.bar(ind, H/roomSize, width, color='r', alpha = 0.3, label = 'heating') 
    rects2 = ax.bar(ind, C/roomSize, width, color='b', alpha = 0.3, label = 'cooling', bottom = H/roomSize) 
    rects3 = ax.bar(ind, L/roomSize, width, color='g', alpha = 0.3, label = 'lighting', bottom = H/roomSize+C/roomSize)
    rects4 = ax.bar(ind, PV/roomSize, width, color='cyan', alpha = 0.3, label = 'PV') 
    
    #TotE = (140, 90, 78, 65, 50)
    
    
    xtra_space = 0.0
    rects2 = ax.bar(ind + width + xtra_space , E/roomSize, width, color='black', alpha = 0.3, label = 'total') 
    
    
    
    # add some text for labels, title and axes ticks
    ax.set_ylabel(r'Energy Demand$\mathregular{\left[\frac{kWh}{m^2year}\right]}$', fontsize = 14)
    ax.set_title('(a) Energy Demand Dependency on Building Orientation')
    
    ax.set_xticks(ind+width+xtra_space)
    ax.set_xticklabels( ('W', 'SW', 'S', 'SE', 'E'), fontsize = 14 )
    ax.tick_params(labelsize=14)
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    for key, item in OrientationFolders.iteritems():
        print key, item
        results[key] = np.load(paths['results'] + '\\' + item + '\\all_results.npy').item()['TradeoffResults']
        
     # number of bars
    N = 5
    
    # empty list for results
    H = []
    C = []
    L = []
    PV = []
    E = []


    # fill result lists
    for i in  ['W', 'SW', 'S', 'SE', 'E']:

        H.append(-results[i]['energy_opttot']['H'] + results[i]['energy_45']['H'])
        C.append(-results[i]['energy_opttot']['C'] + results[i]['energy_45']['C'])
        L.append(-results[i]['energy_opttot']['L'] + results[i]['energy_45']['L'])
        PV.append(-results[i]['energy_opttot']['PV'] + results[i]['energy_45']['PV'])
        E.append(-results[i]['energy_opttot']['E_tot'] + results[i]['energy_45']['E_tot'])
        
        
        
    # convert them to numpy arrays
    H = np.array(H)
    C = np.array(C)
    L = np.array(L)
    PV = np.array(PV)
    E = np.array(E)

    
    
    ind = np.arange(N)+0.15  # the x locations for the groups
    width = 0.35       # the width of the bars
    
    ax = plt.subplot(3,1,2)
    
    rects1 = ax.bar(ind, H/roomSize, width, color='r', alpha = 0.3, label = 'heating') 
    rects2 = ax.bar(ind, C/roomSize, width, color='b', alpha = 0.3, label = 'cooling', bottom=H/roomSize) 
    rects3 = ax.bar(ind, L/roomSize, width, color='g', alpha = 0.3, label = 'lighting', bottom = H/roomSize + C/roomSize)
    rects4 = ax.bar(ind, PV/roomSize, width, color='cyan', alpha = 0.3, label = 'PV', bottom = H/roomSize + C/roomSize + L/roomSize) 
    
    #TotE = (140, 90, 78, 65, 50)
    
    
    xtra_space = 0.0
    rects2 = ax.bar(ind + width + xtra_space , E/roomSize, width, color='black', alpha = 0.3, label = 'total') 

    # add some text for labels, title and axes ticks

    ax.set_title('(b) Energy Difference in Comparison to Fixed Facade at 45 deg Altitude')
    ax.set_ylabel(r'Energy Savings $\mathregular{\left[\frac{kWh}{m^2year}\right]}$', fontsize = 14)
    ax.set_xticks(ind+width+xtra_space)
    ax.tick_params(labelsize=14)
    ax.set_xticklabels( ['W', 'SW', 'S', 'SE', 'E'] , rotation='horizontal' , fontsize = 14)
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
        
    
    
    noShadeResults = {}
    
    for key, item in OrientationFoldersNoShade.iteritems():
        print key, item
        noShadeResults[key] = np.load(paths['results'] + '\\' + item + '\\all_results.npy').item()['TradeoffResults']
        
     # number of bars
    N = 5
    
    # empty list for results
    H = []
    C = []
    L = []
    PV = []
    E = []


    # fill result lists
    for i in  ['W', 'SW', 'S', 'SE', 'E']:

        H.append(-results[i]['energy_opttot']['H'] + noShadeResults[i]['energy_opttot']['H'])
        C.append(-results[i]['energy_opttot']['C'] + noShadeResults[i]['energy_opttot']['C'])
        L.append(-results[i]['energy_opttot']['L'] + noShadeResults[i]['energy_opttot']['L'])
        PV.append(-results[i]['energy_opttot']['PV'] + noShadeResults[i]['energy_opttot']['PV'])
        E.append(-results[i]['energy_opttot']['E_tot'] + noShadeResults[i]['energy_opttot']['E_tot'])
        
        
        
    # convert them to numpy arrays
    H = np.array(H)
    C = np.array(C)
    L = np.array(L)
    PV = np.array(PV)
    E = np.array(E)

    
    
    ind = np.arange(N)+0.15  # the x locations for the groups
    width = 0.35       # the width of the bars
    
    ax = plt.subplot(3,1,3)
    
    rects1 = ax.bar(ind, H/roomSize, width, color='r', alpha = 0.3, label = 'heating') 
    rects2 = ax.bar(ind, C/roomSize, width, color='b', alpha = 0.3, label = 'cooling') 
    rects3 = ax.bar(ind, L/roomSize, width, color='g', alpha = 0.3, label = 'lighting', bottom = H/roomSize)
    rects4 = ax.bar(ind, PV/roomSize, width, color='cyan', alpha = 0.3, label = 'PV', bottom = C/roomSize) 
    
    #TotE = (140, 90, 78, 65, 50)
    
    
    xtra_space = 0.0
    rects2 = ax.bar(ind + width + xtra_space , E/roomSize, width, color='black', alpha = 0.3, label = 'total') 

    # add some text for labels, title and axes ticks

    ax.set_title('(c) Energy Difference in Comparison to No Shading System')
    ax.set_ylabel(r'Energy Savings $\mathregular{\left[\frac{kWh}{m^2year}\right]}$', fontsize = 14)
#    ax.set_ylabel(r'Energy   $\mathregular{(\frac{1}{s})}$', fontsize = 14)
    ax.set_xticks(ind+width+xtra_space)
    ax.set_xticklabels( ['W', 'SW', 'S', 'SE', 'E'] , rotation='horizontal' , fontsize = 14)
    ax.tick_params(labelsize=14)
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend() 
    
    
    plt.legend()
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -.35),
          ncol=5, fancybox=True, shadow=False)
    
    plt.show()
    
if LocationStudy:
    
    
    #results1 = np.load(paths['results'] + '\\' + resultsFolder1 + '\\all_results.npy').item()
    #results2 = np.load(paths['results'] + '\\' + resultsFolder2 + '\\all_results.npy').item()
    
    results = {}
    for key, item in LocationFolders.iteritems():
        print key, item
        results[key] = np.load(paths['results'] + '\\' + item + '\\all_results.npy').item()['TradeoffResults']['energy_opttot']
        
    # number of bars
    N = 4
    
    # empty list for results
    H = []
    C = []
    L = []
    PV = []
    E = []

    # fill result lists
    for i in ['Helsinki',  'Zurich', 'Madrid', 'Cairo' ]:
        
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
    
    fig = plt.figure(figsize=(16,12))
    ax = plt.subplot(3,1,1)
    rects1 = ax.bar(ind, H/roomSize, width, color='r', alpha = 0.3, label = 'heating') 
    rects2 = ax.bar(ind, C/roomSize, width, color='b', alpha = 0.3, label = 'cooling', bottom = H/roomSize) 
    rects3 = ax.bar(ind, L/roomSize, width, color='g', alpha = 0.3, label = 'lighting', bottom = H/roomSize+C/roomSize)
    rects4 = ax.bar(ind, PV/roomSize, width, color='cyan', alpha = 0.3, label = 'PV') 
    
    #TotE = (140, 90, 78, 65, 50)
    
    
    xtra_space = 0.0
    rects2 = ax.bar(ind + width + xtra_space , E/roomSize, width, color='black', alpha = 0.3, label = 'total') 
    
    
    
    # add some text for labels, title and axes ticks
    ax.set_ylabel(r'(a) Energy Demand$\mathregular{\left[\frac{kWh}{m^2year}\right]}$', fontsize = 14)
    ax.set_title('Energy Demand Dependency on Building Location')
    
    ax.set_xticks(ind+width+xtra_space)
    ax.set_xticklabels( ('Helsinki',  'Zurich', 'Madrid', 'Cairo' ), fontsize = 14 )
    ax.tick_params(labelsize=14)
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    for key, item in LocationFolders.iteritems():
        print key, item
        results[key] = np.load(paths['results'] + '\\' + item + '\\all_results.npy').item()['TradeoffResults']
        
     # number of bars
    N = 4
    
    # empty list for results
    H = []
    C = []
    L = []
    PV = []
    E = []


    # fill result lists
    for i in  ['Helsinki',  'Zurich', 'Madrid', 'Cairo' ]:

        H.append(-results[i]['energy_opttot']['H'] + results[i]['energy_45']['H'])
        C.append(-results[i]['energy_opttot']['C'] + results[i]['energy_45']['C'])
        L.append(-results[i]['energy_opttot']['L'] + results[i]['energy_45']['L'])
        PV.append(-results[i]['energy_opttot']['PV'] + results[i]['energy_45']['PV'])
        E.append(-results[i]['energy_opttot']['E_tot'] + results[i]['energy_45']['E_tot'])
        
        
        
    # convert them to numpy arrays
    H = np.array(H)
    C = np.array(C)
    L = np.array(L)
    PV = np.array(PV)
    E = np.array(E)

    
    
    ind = np.arange(N)+0.15  # the x locations for the groups
    width = 0.35       # the width of the bars
    
    ax = plt.subplot(3,1,2)
    
    #assign bottom array:
    bottom1 = np.array([H[0],H[1],0,0])/roomSize
    
    rects1 = ax.bar(ind, H/roomSize, width, color='r', alpha = 0.3, label = 'heating') 
    rects2 = ax.bar(ind, C/roomSize, width, color='b', alpha = 0.3, label = 'cooling', bottom=bottom1 ) 
    rects3 = ax.bar(ind, L/roomSize, width, color='g', alpha = 0.3, label = 'lighting', bottom = bottom1 + C/roomSize)
    rects4 = ax.bar(ind, PV/roomSize, width, color='cyan', alpha = 0.3, label = 'PV', bottom = bottom1 + C/roomSize + L/roomSize) 
    
    #TotE = (140, 90, 78, 65, 50)
    
    
    xtra_space = 0.0
    rects2 = ax.bar(ind + width + xtra_space , E/roomSize, width, color='black', alpha = 0.3, label = 'total') 

    # add some text for labels, title and axes ticks

    ax.set_title('(b) Energy Difference in Comparison to Fixed Facade at 45 deg Altitude')
    ax.set_ylabel(r'Energy Savings $\mathregular{\left[\frac{kWh}{m^2year}\right]}$', fontsize = 14)
    ax.set_xticks(ind+width+xtra_space)
    ax.tick_params(labelsize=14)
    ax.set_xticklabels( ['Helsinki',  'Zurich', 'Madrid', 'Cairo' ] , rotation='horizontal' , fontsize = 14)
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
        
    
    
    noShadeResults = {}
    
    for key, item in LocationFoldersNoShade.iteritems():
        print key, item
        noShadeResults[key] = np.load(paths['results'] + '\\' + item + '\\all_results.npy').item()['TradeoffResults']
        
     # number of bars
    N = 4
    
    # empty list for results
    H = []
    C = []
    L = []
    PV = []
    E = []


    # fill result lists
    for i in  ['Helsinki',  'Zurich', 'Madrid', 'Cairo' ]:

        H.append(-results[i]['energy_opttot']['H'] + noShadeResults[i]['energy_opttot']['H'])
        C.append(-results[i]['energy_opttot']['C'] + noShadeResults[i]['energy_opttot']['C'])
        L.append(-results[i]['energy_opttot']['L'] + noShadeResults[i]['energy_opttot']['L'])
        PV.append(-results[i]['energy_opttot']['PV'] + noShadeResults[i]['energy_opttot']['PV'])
        E.append(-results[i]['energy_opttot']['E_tot'] + noShadeResults[i]['energy_opttot']['E_tot'])
        
        
        
    # convert them to numpy arrays
    H = np.array(H)
    C = np.array(C)
    L = np.array(L)
    PV = np.array(PV)
    E = np.array(E)

    
    
    ind = np.arange(N)+0.15  # the x locations for the groups
    width = 0.35       # the width of the bars
    
    ax = plt.subplot(3,1,3)
    
    rects1 = ax.bar(ind, H/roomSize, width, color='r', alpha = 0.3, label = 'heating') 
    rects2 = ax.bar(ind, C/roomSize, width, color='b', alpha = 0.3, label = 'cooling') 
    rects3 = ax.bar(ind, L/roomSize, width, color='g', alpha = 0.3, label = 'lighting', bottom = H/roomSize)
    rects4 = ax.bar(ind, PV/roomSize, width, color='cyan', alpha = 0.3, label = 'PV', bottom = C/roomSize) 
    
    #TotE = (140, 90, 78, 65, 50)
    
    
    xtra_space = 0.0
    rects2 = ax.bar(ind + width + xtra_space , E/roomSize, width, color='black', alpha = 0.3, label = 'total') 

    # add some text for labels, title and axes ticks

    ax.set_title('(c) Energy Difference in Comparison to No Shading System')
    ax.set_ylabel(r'Energy Savings $\mathregular{\left[\frac{kWh}{m^2year}\right]}$', fontsize = 14)
#    ax.set_ylabel(r'Energy   $\mathregular{(\frac{1}{s})}$', fontsize = 14)
    ax.set_xticks(ind+width+xtra_space)
    ax.set_xticklabels( ['Helsinki',  'Zurich', 'Madrid', 'Cairo' ] , rotation='horizontal' , fontsize = 14)
    ax.tick_params(labelsize=14)
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend() 
    
    
    plt.legend()
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -.35),
          ncol=5, fancybox=True, shadow=False)
    
    plt.show()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
if BuildingParameterStudy:
    

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
    baselineN = 3
    barcolors = []   
    for i in range(N):
        if i == baselineN:
            barcolors.append('black')
        else:
            barcolors.append('grey')
 
    # empty list for results
    E = []

    # fill result lists
    for i in ['HCOP1', 'HCOP2', 'HCOP3', 'HCOP4', 'HCOP5', 'HCOP6', 'HCOP7', 'HCOP8', 'HCOP9', 'HCOP10']:

        E.append(-results[i]['energy_opttot']['E_tot'] + results[i]['energy_45']['E_tot'])
        
    # convert to numpy array
    E = np.array(E)
    
    
    ind = np.arange(N)-0.25  # the x locations for the groups
    width = 0.5       # the width of the bars
    
    fig = plt.figure(figsize=(16, 8))
    
    ax1 = plt.subplot(2,4,1)
    
    rects1 = ax1.bar(ind, E/roomSize, width, color=barcolors, alpha = 0.7) 

    # add some text for labels, title and axes ticks
    ax1.set_ylabel('Energy Savings per Room Area \nCompared to Facade at 45 deg \n' + r'$\mathregular{\left[\frac{kWh}{m^2year}\right]}$', fontsize = 14)
    ax1.set_title('Sensitivity on Heating COP')
    
    ax1.set_xticks(ind+0.25)
    ax1.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']  )
    ax1.set_ylim(bottom=0)
#    ax1.set_xlabel('Heating COP [-]')
    ax1.tick_params(labelsize=14)
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend()
    
    
    
    
    
    # number of bars
    N = 10
    baselineN = 3
    barcolors = []   
    for i in range(N):
        if i == baselineN:
            barcolors.append('black')
        else:
            barcolors.append('grey')
 
    
    # empty list for results
    E = []

    # fill result lists
    for i in ['HCOP1', 'HCOP2', 'HCOP3', 'HCOP4', 'HCOP5', 'HCOP6', 'HCOP7', 'HCOP8', 'HCOP9', 'HCOP10']:

        E.append(-results[i]['energy_opttot']['E_tot'] + noShadeResults[i]['energy_opttot']['E_tot'])
        
    # convert to numpy array
    E = np.array(E)
    
    
    ind = np.arange(N)-0.25  # the x locations for the groups
    width = 0.5       # the width of the bars
        
    ax2 = plt.subplot(2,4,5)
    
    rects1 = ax2.bar(ind, E/roomSize, width, color=barcolors, alpha = 0.7) 

    # add some text for labels, title and axes ticks
    ax2.set_ylabel('Energy Savings per Room Area \nCompared to No Shading System \n' + r'$\mathregular{\left[\frac{kWh}{m^2year}\right]}$', fontsize = 14 )
#    ax2.set_title('Sensitivity on Heating COP')
    
    ax2.set_xticks(ind+0.25)
    ax2.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']  )
    ax2.set_xlabel('Heating COP [-]', fontsize=14)
    ax2.tick_params(labelsize=14)
    ax2.set_ylim(bottom=0)
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend()
    
    
    
    
    
    
    
    ############ Cooling Plots ####################

    
    # number of bars
    N = 10
    baselineN = 2
    barcolors = []   
    for i in range(N):
        if i == baselineN:
            barcolors.append('black')
        else:
            barcolors.append('grey')
 
    
    # empty list for results
    E = []

    # fill result lists
    for i in ['CCOP1', 'CCOP2', 'CCOP3', 'CCOP4', 'CCOP5', 'CCOP6', 'CCOP7', 'CCOP8', 'CCOP9', 'CCOP10']:

        E.append(-results[i]['energy_opttot']['E_tot'] + results[i]['energy_45']['E_tot'])
        
    # convert to numpy array
    E = np.array(E)
    
    
    ind = np.arange(N)-0.25  # the x locations for the groups
    width = 0.5       # the width of the bars
    
    ax = plt.subplot(2,4,2, sharey=ax1)
    
    rects1 = ax.bar(ind, E/roomSize, width, color=barcolors, alpha = 0.7) 

    # add some text for labels, title and axes ticks
    ax.set_title('Sensitivity on Cooling COP')
    
    ax.set_xticks(ind+0.25)
    ax.set_xticklabels( ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] )
#    ax.set_xlabel('Cooling COP [-]')
    ax.tick_params(labelsize=14)
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend()



    # number of bars
    N = 10
    baselineN = 2
    barcolors = []   
    for i in range(N):
        if i == baselineN:
            barcolors.append('black')
        else:
            barcolors.append('grey')
 
    
    # empty list for results
    E = []

    # fill result lists
    for i in ['CCOP1', 'CCOP2', 'CCOP3', 'CCOP4', 'CCOP5', 'CCOP6', 'CCOP7', 'CCOP8', 'CCOP9', 'CCOP10']:

        E.append(-results[i]['energy_opttot']['E_tot'] + noShadeResults[i]['energy_opttot']['E_tot'])
        
    # convert to numpy array
    E = np.array(E)
    
    
    ind = np.arange(N)-0.25  # the x locations for the groups
    width = 0.5       # the width of the bars
    
    ax = plt.subplot(2,4,6, sharey=ax2)
    
    rects1 = ax.bar(ind, E/roomSize, width, color=barcolors, alpha = 0.7) 

    # add some text for labels, title and axes ticks
#    ax.set_title('Sensitivity on Cooling COP')
    
    ax.set_xticks(ind+0.25)
    ax.set_xticklabels( ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] )
    ax.set_xlabel('Cooling COP [-]', fontsize=14)
    ax.tick_params(labelsize=14)
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend()
    
    
    
    
    
    
    ############ Lighting Plots ####################

    
    # number of bars
    N = 5
    baselineN = 3
    barcolors = []   
    for i in range(N):
        if i == baselineN:
            barcolors.append('black')
        else:
            barcolors.append('grey')
 
    
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
    
    ax = plt.subplot(2,4,3, sharey=ax1)
    
    rects1 = ax.bar(ind, E/roomSize, width, color=barcolors, alpha = 0.7) 

    # add some text for labels, title and axes ticks
    ax.set_title('Sensitivity on Lighting Load')
    
    ax.set_xticks(ind+0.25)
    ax.set_xticklabels(['3', '6', '9', '11.74', '15'] )
#    ax.set_xlabel('Lighting Load [W/m2]')
    ax.tick_params(labelsize=14)
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend()
    
    
    # number of bars
    N = 5
    baselineN = 3
    barcolors = []   
    for i in range(N):
        if i == baselineN:
            barcolors.append('black')
        else:
            barcolors.append('grey')
 
    
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
    
    ax = plt.subplot(2,4,7, sharey=ax2)
    
    rects1 = ax.bar(ind, E/roomSize, width, color=barcolors, alpha = 0.7) 

    # add some text for labels, title and axes ticks
#    ax.set_title('Sensitivity on Lighting Load')
    
    ax.set_xticks(ind+0.25)
    ax.set_xticklabels(['3', '6', '9', '11.74', '15'] )
    ax.set_xlabel('Lighting Load [W/m2]', fontsize=14)
    ax.tick_params(labelsize=14)
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
    baselineN = 2
    barcolors = []   
    for i in range(N):
        if i == baselineN:
            barcolors.append('black')
        else:
            barcolors.append('grey')
 
    
    # empty list for results
    E = []

    # fill result lists

    for i in ['0.5', '0.75', '1', '1.25', '1.5']:

        E.append(-resultsInfilt[i]['energy_opttot']['E_tot'] + resultsInfilt[i]['energy_45']['E_tot'])
        
    # convert to numpy array
    E = np.array(E)
    
    
    ind = np.arange(N)-0.25  # the x locations for the groups
    width = 0.5       # the width of the bars
    
    ax = plt.subplot(2,4,4, sharey=ax1)
    
    rects1 = ax.bar(ind, E/roomSize, width, color=barcolors, alpha = 0.7) 

    # add some text for labels, title and axes ticks
    ax.set_title('Sensitivity on Infiltration Rate')
    
    ax.set_xticks(ind+0.25)
    ax.set_xticklabels( ['0.5', '0.75', '1', '1.25', '1.5'] )
    ax.tick_params(labelsize=14)
    ax.set_ylim(bottom=0)
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    plt.legend()
    
    
    # number of bars
    N = 5
    baselineN = 2
    barcolors = []   
    for i in range(N):
        if i == baselineN:
            barcolors.append('black')
        else:
            barcolors.append('grey')
 
    
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
    
    ax = plt.subplot(2,4,8, sharey=ax2)
    
    rects1 = ax.bar(ind, E/roomSize, width, color=barcolors, alpha = 0.7) 

    # add some text for labels, title and axes ticks
#    ax.set_title('Sensitivity on Infiltration Rate')
    
    ax.set_xticks(ind+0.25)
    ax.set_xticklabels( ['0.5', '0.75', '1', '1.25', '1.5'] )
    ax.set_xlabel('Infiltration Rate [1/h]', fontsize=14)
    ax.tick_params(labelsize=14)
    ax.set_ylim(bottom=0)
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
    
    noShadeResult = np.load(paths['results'] + '\\' + 'Kloten_noShade_basecase' + '\\all_results.npy').item()['TradeoffResults']
    # number of bars
#    N = 11
#    
#    # empty list for results
#    H = []
#    C = []
#    L = []
#    PV = []
#    E = []
#
#    # fill result lists
#    for i in ['22.5degx','2x','3x','9','5x','5y22.5','5y45','19x', '19y', '25', '49']:
#        
#        H.append(combinationResults[i]['H'])
#        C.append(combinationResults[i]['C'])
#        L.append(combinationResults[i]['L'])
#        PV.append(combinationResults[i]['PV'])
#        E.append(combinationResults[i]['E_tot'])
#        
#    # convert them to numpy arrays
#    H = np.array(H)
#    C = np.array(C)
#    L = np.array(L)
#    PV = np.array(PV)
#    E = np.array(E)
#    
#    
#    ind = np.arange(N) + .15 # the x locations for the groups
#    width = 0.35       # the width of the bars
#    
#    fig = plt.figure(figsize=(16,12))
#    ax = plt.subplot(3,1,1)
#    rects1 = ax.bar(ind, H, width, color='r', alpha = 0.3, label = 'heating') 
#    rects2 = ax.bar(ind, C, width, color='b', alpha = 0.3, label = 'cooling', bottom = H) 
#    rects3 = ax.bar(ind, L, width, color='g', alpha = 0.3, label = 'lighting', bottom = H+C)
#    rects4 = ax.bar(ind, PV, width, color='cyan', alpha = 0.3, label = 'PV') 
#    
#    #TotE = (140, 90, 78, 65, 50)
#    
#    
#    xtra_space = 0.0
#    rects2 = ax.bar(ind + width + xtra_space , E, width, color='black', alpha = 0.3, label = 'total') 
#    
#    
#    
#    # add some text for labels, title and axes ticks
#    ax.set_ylabel('Energy [kWh]')
#    ax.set_title('Energy Dependency on Building Orientation')
#    
#    ax.set_xticks(ind+width+xtra_space)
#    ax.set_xticklabels( ['22.5degx','2x','3x','9','5x','5y22.5','5y45','19x', '19y', '25', '49'] )
#    ax.set_xlabel('Building Orientation')
#    plt.axhline(y=0, linewidth=1, color = 'k')
#    plt.grid( axis = u'y')
#    
#    plt.legend()
#    
#    plt.show()
    
    results = {}
     
    for key, item in combinationFolders.iteritems():
        print key, item
        results[key] = np.load(paths['results'] + '\\' + item + '\\all_results.npy').item()['TradeoffResults']
        
     # number of bars
#    N = 5
    N = 11
    
    labels = ['$\mathregular{2}$ Altitude Angles \nAzimuth  = $\mathregular{0^\circ}$\n',
              'Altitude =$\mathregular{22.5^\circ}$ \nAzimuth  = $\mathregular{0^\circ}$\n',
              '$\mathregular{3}$ Altitude Angles \nAzimuth  = $\mathregular{0^\circ}$\n',
              '$\mathregular{3}$ Altitude Angles \n$\mathregular{3}$ Azimuth Angles \n',
              'Altitude =$\mathregular{45^\circ}$ \n$\mathregular{3}$ Azimuth Angles \n',
              '$\mathregular{5}$ Altitude Angles \nAzimuth  = $\mathregular{0^\circ}$\n',
              'Altitude =$\mathregular{22.5^\circ}$ \n$\mathregular{5}$ Azimuth Angles \n',
              '$\mathregular{19}$ Altitude Angles \nAzimuth  = $\mathregular{0^\circ}$\n',
              '$\mathregular{5}$ Altitude Angles \n$\mathregular{5}$ Azimuth Angles \n',
              'Altitude =$\mathregular{20^\circ}$ \n$\mathregular{19}$ Azimuth Angles \n',
              '$\mathregular{7}$ Altitude Angles \n$\mathregular{7}$ Azimuth Angles \n']
              #'3x','9','5y45','5x','5y22.5','19x', '25', '19y', '49']    
    
    barColors=[]
#    cmap = mpl.cm.cubehelix
    cmap = mpl.cm.ocean_r
#    cmap = mpl.cm.brg
#    cmap = mpl.cm.afmhot
    for i in range(N):
        
        barColors.append(cmap((i+1)/float(N)))
    
    
    # empty list for results
    E = []

    # fill result lists
    for i in  ['2x','22.5degx','3x','9','5y45','5x','5y22.5','19x', '25', '19y', '49']:# ['19x', '19y', '25', '49', '91']:

        E.append(-results[i]['energy_opttot']['E_tot'] + results['25']['energy_45']['E_tot'])
        
    # convert to numpy array
    E = np.array(E)
    
    
    ind = np.arange(N)-0.25  # the x locations for the groups
    width = 0.7       # the width of the bars
    
    fig = plt.figure(figsize=(16,11))

    ax = plt.subplot(2,1,1)
    
#    rects1 = ax.bar(ind, E/roomSize, width, color='orange', alpha = 0.3) 
#     rects1 = ax.bar(ind, E/roomSize, width, color=barColors, label=labels, alpha = 0.7) 

    for i in range(N):
        rects1 = ax.bar(1+i, E[i]/roomSize, width, color=barColors[i], label=labels[i], alpha = 0.7, align='center') 

    # add some text for labels, title and axes ticks

    ax.set_title('Sensitivity on Simulation Combination')
    
    ax.set_ylabel('Energy Savings per room area \ncompared to facade at 45 deg \n' + r'$\mathregular{\left[\frac{kWh}{m^2year}\right]}$', fontsize = 14)

    
    ax.set_xticks(ind+1.25)
    ax.tick_params(labelsize=14)

#    ax.set_xticklabels( ['19/0', '0/19', '5/5', '7/7', '13/7'], rotation='vertical' )
#    ax.set_xticklabels(  ['2x','22.5degx','3x','9','5y45','5x','5y22.5','19x', '25', '19y', '49'], rotation='vertical' )

#    ax.set_xlabel('azimuth/altitude')
#    ax.set_xlabel('Combination')
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    
    # Put a legend to the right of the current axis
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1.05))
    
    
#    plt.legend()
    
     # number of bars
#    N = 5
    N = 11
    
    # empty list for results
    E = []

    # fill result lists
    for i in   ['2x','22.5degx','3x','9','5y45','5x','5y22.5','19x', '25', '19y', '49']:#['19x', '19y', '25', '49', '91']:

        E.append(-results[i]['energy_opttot']['E_tot'] + noShadeResult['energy_opttot']['E_tot'])
        
    # convert to numpy array
    E = np.array(E)
    
    
    ind = np.arange(N)-0.25  # the x locations for the groups
    width = 0.5       # the width of the bars
    
    ax = plt.subplot(2,1,2)
    
#    rects1 = ax.bar(ind, E/roomSize, width, color=barColors, alpha = 0.7) 
    
    for i in range(N):
        rects1 = ax.bar(1+i, E[i]/roomSize, width, color=barColors[i], label=labels[i], alpha = 0.7, align='center') 

    # add some text for labels, title and axes ticks

#    ax.set_title('Sensitivity on Simulation Combination')
    ax.set_xticks(ind+1.25)
#    ax.set_xticks(ind+0.25)
#    ax.set_xticklabels( ['19/0', '0/19', '5/5', '7/7', '13/7'], rotation='vertical' )
#    ax.set_xticklabels(  ['2x','22.5degx','3x','9','5y45','5x','5y22.5','19x', '25', '19y', '49'], rotation='vertical' )
#    ax.set_xlabel('azimuth/altitude')
    ax.set_ylabel('Energy Savings per room area \ncompared to no facade \n' + r'$\mathregular{\left[\frac{kWh}{m^2year}\right]}$', fontsize = 14)
    ax.set_xlabel('Combination', fontsize=14)
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    ax.tick_params(labelsize=14)

    
    
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    
    # Put a legend to the right of the current axis
#    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
#    plt.legend()
        
    
if ClusterStudy:
    
    clusterResults = {}
    
    # load results
    for key, item in clusterFolders.iteritems():
        print key, item
        clusterResults[key] = np.load(paths['results'] + '\\' + item + '\\all_results.npy').item()#['TradeoffResults']['energy_opttot']
    
#    
#    results1 = np.load(paths['results'] + '\\' + clusterFolders['1clust'] + '\\all_results.npy').item()
#    results2 = np.load(paths['results'] + '\\' + clusterFolders['2clust'] + '\\all_results.npy').item()
#    
     #plot data 
#    figures= {}
#    figures['2clust'] = compareResultsFigure(clusterResults['2clust_base']['monthlyData'], clusterResults['2clust']['monthlyData'], evaluate='E_tot')
#    plt.xticks(range(0,288,24),('Mar', 'Jun', 'Sep', 'Dec'))    
#    figures['3clust'] = compareResultsFigure(clusterResults['3clust_base']['monthlyData'], clusterResults['3clust']['monthlyData'], evaluate='E_tot')
#    plt.xticks(range(0,288,24),('Mar', 'Jun', 'Sep', 'Dec'))
    
#        
#    majorLocator = MultipleLocator(24)
#    majorFormatter = FormatStrFormatter('%d')
#    minorLocator = MultipleLocator(12)
#    minorFormatter = FormatStrFormatter('%d')
    
    ##    ax1.xaxis.set_minor_formatter(minorFormatter)
    #plt.grid(True, which='both')
    #
    #ax = plt.subplot(3,1,1)
    #plt.plot(monthlyData_comb['R_avg'][PV_max_ind, range(len(R_max_ind))], label='optimized for PV')
    #plt.plot(monthlyData_tracking['R_avg'].transpose(), label = 'sun tracking')
    #plt.plot(monthlyData_comb['R_theo'][R_max_ind, range(len(R_max_ind))], label = 'without shading')
    #plt.ylabel('Radiation [W/m2]', fontsize = 14)
    #plt.title ('Average Radiation on Panels')
    #plt.legend()
    #plt.grid()
    #ax.tick_params(labelsize=14)
    
#    ax = figures['2clust']['E_tot'].add_subplot(2,1,1)
#    ax.xaxis.set_major_locator(majorLocator)
#    ax.xaxis.set_major_formatter(majorFormatter)
#    ax.xaxis.set_minor_locator(minorLocator)
#    plt.xticks(range(0,288,24),('Mar', 'Jun', 'Sep', 'Dec'))
#    
#    ax = figures['2clust']['E_tot'].add_subplot(2,1,2)
#    ax.xaxis.set_major_locator(majorLocator)
#    ax.xaxis.set_major_formatter(majorFormatter)
#    ax.xaxis.set_minor_locator(minorLocator)
#    plt.xticks(range(0,288,24),('Mar', 'Jun', 'Sep', 'Dec'))
#    
#    ax = figures['3clust']['E_tot'].add_subplot(2,1,1)
#    ax.xaxis.set_major_locator(majorLocator)
#    ax.xaxis.set_major_formatter(majorFormatter)
#    ax.xaxis.set_minor_locator(minorLocator)
#    plt.xticks(range(0,288,24),('Mar', 'Jun', 'Sep', 'Dec'))
#    
#    ax = figures['3clust']['E_tot'].add_subplot(2,1,2)
#    ax.xaxis.set_major_locator(majorLocator)
#    ax.xaxis.set_major_formatter(majorFormatter)
#    ax.xaxis.set_minor_locator(minorLocator)
#    plt.xticks(range(0,288,24),('Mar', 'Jun', 'Sep', 'Dec'))
    
    
           ############ data 1    
    
    # assign data:
    H1 = clusterResults['2clust_base']['monthlyData']['H']
    C1 = clusterResults['2clust_base']['monthlyData']['C']
    L1 = clusterResults['2clust_base']['monthlyData']['L']
    PV1 = clusterResults['2clust_base']['monthlyData']['PV']

     # assign what efficiencies were used for evaluation:  
    if clusterResults['2clust_base']['monthlyData']['changedEfficiency'] == True:
        usedEfficiencies1 = clusterResults['2clust_base']['monthlyData']['efficiencyChanges']
    else:
        usedEfficiencies1 = clusterResults['2clust_base']['monthlyData']['efficiencies']
    
    # sum individual data
    E_HCL1 = H1+C1+L1
    E_tot11 = E_HCL1+PV1
    
    # select only june:
    E_tot1 = E_tot11[:,range(24,48)]
    
    # find indices
    E_totind1 = np.argmin(E_tot1,axis=0)
    
    
    
    ################## data 2
    
     # assign data:
    H2 = clusterResults['2clust']['monthlyData']['H']
    C2 = clusterResults['2clust']['monthlyData']['C']
    L2 = clusterResults['2clust']['monthlyData']['L']
    PV2 = clusterResults['2clust']['monthlyData']['PV']

     # assign what efficiencies were used for evaluation:  
#    if clusterResults['2clust']['monthlyData']['changedEfficiency'] == True:
#        usedEfficiencies2 = clusterResults['2clust']['monthlyData']['efficiencyChanges']
#    else:
#        usedEfficiencies2 = clusterResults['2clust']['monthlyData']['efficiencies']
        
    # sum individual data
    E_HCL2 = H2+C2+L2
    E_tot22 = E_HCL2+PV2
    
    # select only june:
    E_tot2 = E_tot22[:,range(24,48)]
        
    
    # find indices
    E_totind2 = np.argmin(E_tot2,axis=0)

    indices = {'E_tot1':E_totind1, 'E_tot2':E_totind2 }    
    
    
    ################ data 3
    
     # assign data:
    H3 = clusterResults['3clust_base']['monthlyData']['H']
    C3 = clusterResults['3clust_base']['monthlyData']['C']
    L3 = clusterResults['3clust_base']['monthlyData']['L']
    PV3 = clusterResults['3clust_base']['monthlyData']['PV']

     # assign what efficiencies were used for evaluation:  
    if clusterResults['3clust_base']['monthlyData']['changedEfficiency'] == True:
        usedEfficiencies3 = clusterResults['2clust_base']['monthlyData']['efficiencyChanges']
    else:
        usedEfficiencies3 = clusterResults['2clust_base']['monthlyData']['efficiencies']
    
    # sum individual data
    E_HCL3 = H3+C3+L3
    E_tot33 = E_HCL3+PV3
    
    # select only june:
    E_tot3 = E_tot33[:,range(24,48)]
    
    # find indices
    E_totind3 = np.argmin(E_tot3,axis=0)
    
    
    indices['E_tot3']=E_totind3

    ################## data 4
    
     # assign data:
    H4 = clusterResults['3clust']['monthlyData']['H']
    C4 = clusterResults['3clust']['monthlyData']['C']
    L4 = clusterResults['3clust']['monthlyData']['L']
    PV4 = clusterResults['3clust']['monthlyData']['PV']

     # assign what efficiencies were used for evaluation:  
#    if clusterResults['2clust']['monthlyData']['changedEfficiency'] == True:
#        usedEfficiencies2 = clusterResults['2clust']['monthlyData']['efficiencyChanges']
#    else:
#        usedEfficiencies2 = clusterResults['2clust']['monthlyData']['efficiencies']
        
    # sum individual data
    E_HCL4 = H4+C4+L4
    E_tot44 = E_HCL4+PV4
    
    # select only june:
    E_tot4 = E_tot44[:,range(24,48)]
        
    
    # find indices
    E_totind4 = np.argmin(E_tot4,axis=0)

    indices['E_tot4']=E_totind4
#    if usedEfficiencies1 == usedEfficiencies2:
#        usedEfficiencies = usedEfficiencies1
    

#    plotResultsComparison(clusterResults['2clust_base']['monthlyData'], clusterResults['2clust']['monthlyData'], indices, [evaluate])
        #figures[evaluate].suptitle(evaluate)

    
    
        
    energyType = 'E_tot'
    
    dummyRange = np.asarray(range(24,48))
    
    fig = plt.figure(figsize=(16, 8))
    
#    plt.suptitle('Heating Demand (COP=' + str(usedEfficiencies['H_COP']) + ')')
    if energyType == 'PV':
        multiplier = -1
    else:
        multiplier = 1
    
    ax1 = plt.subplot(3,2,1)
    
    plt.plot(multiplier*clusterResults['2clust_base']['monthlyData'][energyType][indices['E_tot1'], dummyRange]/(roomSize*30*0.001), label = '1 Cluster', color='b')
    plt.plot(multiplier*clusterResults['2clust']['monthlyData'][energyType][indices['E_tot2'], dummyRange]/(roomSize*30*0.001), label = '2 Clusters', color='g')
    
    plt.ylabel('Average Power Use \n' +r' $\mathregular{\left[\frac{W}{m^2}\right]}$', fontsize=14)
    plt.title('2 Cluster Comparison', fontsize=14)
    plt.legend(loc=4)
    plt.tick_params(labelsize=14)
    
    majorLocator = MultipleLocator(6)
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(2)
    minorFormatter = FormatStrFormatter('%d')
#
#    ax1.xaxis.set_major_locator(majorLocator)
#    ax1.xaxis.set_major_formatter(majorFormatter)
#    ax1.xaxis.set_minor_locator(minorLocator)
#    ax1.xaxis.set_minor_formatter(minorFormatter)
    plt.grid(True, which='both')
    
    ax2 = plt.subplot(3,2,3, sharex=ax1)
    
    plt.plot(multiplier*clusterResults['2clust_base']['monthlyData'][energyType][indices['E_tot1'], dummyRange]-multiplier*clusterResults['2clust']['monthlyData'][energyType][indices['E_tot2'], dummyRange], label = '1-2', color='b')

    plt.ylabel('Power Difference \n' +r'$\mathregular{\left[\frac{W}{m^2}\right]}$', fontsize=14)
    plt.xlabel('Hour of the Day', fontsize=14)
    #plt.legend()

    ax2.xaxis.set_major_locator(majorLocator)
    ax2.xaxis.set_major_formatter(majorFormatter)
    ax2.xaxis.set_minor_locator(minorLocator)
    ax2.tick_params(labelsize=14)
#    ax2.xaxis.set_minor_formatter(minorFormatter)
    plt.grid(True, which='both')
    
    
    ax3 = plt.subplot(3,2,2,  sharey=ax1)
    
    plt.plot(multiplier*clusterResults['3clust_base']['monthlyData'][energyType][indices['E_tot3'], dummyRange]/(roomSize*30*0.001), label = '1 Cluster', color='b')
    plt.plot(multiplier*clusterResults['3clust']['monthlyData'][energyType][indices['E_tot4'], dummyRange]/(roomSize*30*0.001), label = '3 Clusters', color='g')
    
#    plt.ylabel('Average Power Use \n' +r' $\mathregular{\left[\frac{W}{m^2}\right]}$', fontsize=14)
    plt.title('3 Cluster Comparison', fontsize=14)
    plt.legend(loc=4)
    plt.tick_params(labelsize=14)
    
    majorLocator = MultipleLocator(6)
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(2)
    minorFormatter = FormatStrFormatter('%d')
#
#    ax1.xaxis.set_major_locator(majorLocator)
#    ax1.xaxis.set_major_formatter(majorFormatter)
#    ax1.xaxis.set_minor_locator(minorLocator)
#    ax1.xaxis.set_minor_formatter(minorFormatter)
    plt.grid(True, which='both')
    
    ax4 = plt.subplot(3,2,4, sharex=ax3, sharey=ax2)
    
    plt.plot(multiplier*clusterResults['3clust_base']['monthlyData'][energyType][indices['E_tot3'], dummyRange]-multiplier*clusterResults['3clust']['monthlyData'][energyType][indices['E_tot4'], dummyRange], label = '1-2', color='b')

#    plt.ylabel('Power Difference \n' +r'$\mathregular{\left[\frac{W}{m^2}\right]}$', fontsize=14)
    plt.xlabel('Hour of the Day', fontsize=14)
    #plt.legend()

    ax4.xaxis.set_major_locator(majorLocator)
    ax4.xaxis.set_major_formatter(majorFormatter)
    ax4.xaxis.set_minor_locator(minorLocator)
    ax4.tick_params(labelsize=14)
#    ax2.xaxis.set_minor_formatter(minorFormatter)
    plt.grid(True, which='both')
    
    
    
    ######### bar plots
    
    # number of bars
    N = 5
    
    # empty list for results
    H = []
    C = []
    L = []
    PV = []
    E = []

    # fill result lists
    for i in ['2clust_base','2clust','3clust_base','3clust']:
        
        H.append(clusterResults[i]['TradeoffResults']['energy_opttot']['H'])
        C.append(clusterResults[i]['TradeoffResults']['energy_opttot']['C'])
        L.append(clusterResults[i]['TradeoffResults']['energy_opttot']['L'])
        PV.append(clusterResults[i]['TradeoffResults']['energy_opttot']['PV'])
        E.append(clusterResults[i]['TradeoffResults']['energy_opttot']['E_tot'])
        
    # convert them to numpy arrays
    H = np.array(H)/4./roomSize*1000
    C = np.array(C)/4./roomSize*1000
    L = np.array(L)/4./roomSize*1000
    PV = np.array(PV)/4./roomSize*1000
    E = np.array(E)/4./roomSize*1000
    
        
    EnergySavings2clust = []
    EnergySavings3clust = []

    for i in [H,C,L,PV,E]:
        EnergySavings2clust.append(i[0]-i[1])
        EnergySavings3clust.append(i[2]-i[3])
        
    clusterColors = ['r','b','g','cyan','black']
        
        
    ind = np.arange(N) #+ .15 # the x locations for the groups
    width = 0.7       # the width of the bars
    
    ax = plt.subplot(3,2,5)
        

    rects1 = ax.bar(ind, EnergySavings2clust, width, color=clusterColors, alpha = 0.3 ) 
    
    
    # add some text for labels, title and axes ticks
    ax.set_ylabel('Energy Savings\n'+r'$\mathregular{\left[\frac{Wh}{m^2month}\right]}$', fontsize=14)
#    ax.set_title('Energy Dependency on Building Orientation')
    
#    ax.set_xticks(ind+width+xtra_space)
#    ax.set_xticklabels( ['1 Cluster','2 Clusters'] , fontsize=14)    
    ax.set_xticks(ind + width/2.)
    ax.set_xticklabels( ['H','C','L','PV','E'] , fontsize=14)
    ax.tick_params(labelsize=14)
#    ax.set_yticklabels([-10,'',0,'',15,'',20,'',30],fontsize=14)
#    ax.set_xlabel('Building Orientation')
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    ax = plt.subplot(3,2,6, sharey=ax)
        
        
    rects1 = ax.bar(ind, EnergySavings3clust, width, color=clusterColors, alpha = 0.3 ) 
    
    
    # add some text for labels, title and axes ticks
#    ax.set_ylabel('Energy Savings\n'+r'$\mathregular{\left[\frac{Wh}{m^2month}\right]}$', fontsize=14)
#    ax.set_title('Energy Dependency on Building Orientation')
    
#    ax.set_xticks(ind+width+xtra_space)
#    ax.set_xticklabels( ['1 Cluster','2 Clusters'] , fontsize=14)    
    ax.set_xticks(ind + width/2.)
    ax.set_xticklabels( ['H','C','L','PV','E'] , fontsize=14)
    ax.tick_params(labelsize=14)
#    ax.set_yticklabels([-10,'',0,'',15,'',20,'',30],fontsize=14)
#    ax.set_xlabel('Building Orientation')
    plt.axhline(y=0, linewidth=1, color = 'k')
    plt.grid( axis = u'y')
    
    #ax.legend(loc='lower center', bbox_to_anchor=(0.5, -.35),
     #     ncol=5, fancybox=True, shadow=False)
    plt.show()
    
    
   
        
