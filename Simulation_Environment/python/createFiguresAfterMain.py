# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 09:10:58 2016

Script to try out plotting functions, only works if data is loaded to workspace.
run main.py first or load data from results.

@author: Jeremias
"""

from plotDataFunctions import create3Dplot, plotTotEfixedY, plotTotEfixedX, plotAngleSavings

#create3Dplot(monthlyData, 'E_tot', 'value')
#create3Dplot(monthlyData, 'E_tot', 'normalized')
#create3Dplot(monthlyData, 'E_tot', 'difference')
#create3Dplot(monthlyData, 'PV', 'difference')
#create3Dplot(monthlyData, 'H', 'difference')
#create3Dplot(monthlyData, 'C', 'difference')
#create3Dplot(monthlyData, 'L', 'difference')
#create3Dplot(monthlyData, 'C', 'value')
#create3Dplot(monthlyData, 'E_tot', 'diffMin')
#create3Dplot(monthlyData, 'PV', 'diffMin')
#create3Dplot(monthlyData, 'H', 'diffMin')
#create3Dplot(monthlyData, 'C', 'diffMin')
#create3Dplot(monthlyData, 'L', 'diffMin')
#create3Dplot(monthlyData, 'C', 'value')
#create3Dplot(monthlyData, 'E_tot', 'diffMinCarpet')
#create3Dplot(monthlyData, 'PV', 'diffMinCarpet')
#create3Dplot(monthlyData, 'H', 'diffMinCarpet')
#create3Dplot(monthlyData, 'C', 'diffMinCarpet')
#create3Dplot(monthlyData, 'L', 'diffMinCarpet')
#
##
#
plotTotEfixedX(monthlyData)
#
#
#
#plotMaxMinDiff(monthlyData)


# load data:
resultsFolder1 = 'Kloten_19x_1y'

resultsFolder2 = 'Kloten_1x_19y'

# paths dict:
paths = {}

paths['main'] = os.path.dirname(os.path.dirname(sys.argv[0]))
paths['results'] = paths['main'] + '\\results'
paths['aux_functions'] = paths['main'] + '\\python\\aux_files'

# add python_path to system path, so that all files are available:
sys.path.insert(0, paths['aux_functions'])

from createFigures import compareResultsFigure

# load results
results1 = np.load(paths['results'] + '\\' + resultsFolder1 + '\\all_results.npy').item()
results2 = np.load(paths['results'] + '\\' + resultsFolder2 + '\\all_results.npy').item()

plotAngleSavings(results1['monthlyData'], xy = 'x')


plotAngleSavings(results2['monthlyData'], xy = 'y')

plotAngleSavings(monthlyData, xy = 'y')