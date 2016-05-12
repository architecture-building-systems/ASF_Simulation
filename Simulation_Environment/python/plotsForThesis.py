# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 09:10:58 2016

Plots for thesis

@author: Jeremias
"""

from plotDataFunctions import create3Dplot, plotTotEfixedY, plotTotEfixedX, plotAngleSavings, plotMaxMinDiff
#


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
#
#plotAngleSavings(results1['monthlyData'], xy = 'x')
#
#
#plotAngleSavings(results2['monthlyData'], xy = 'y')
#
#plotAngleSavings(monthlyData, xy = None)

fig = plt.figure(figsize=(16, 5))
ax = fig.add_subplot(131, projection='3d')
create3Dplot(results1['monthlyData'], 'E_tot', 'diffMinAltitude', startMonth = 3, endMonth = 3, fig=fig, ax=ax)
plt.title('March')
ax = fig.add_subplot(132, projection='3d')
create3Dplot(results1['monthlyData'], 'E_tot', 'diffMinAltitude', startMonth = 6, endMonth = 6, fig=fig, ax=ax)
plt.title('June')
ax = fig.add_subplot(133, projection='3d')
create3Dplot(results1['monthlyData'], 'E_tot', 'diffMinAltitude', startMonth = 9, endMonth = 9, fig=fig, ax=ax)
plt.title('September')
#ax = fig.add_subplot(224, projection='3d')
#create3Dplot(results1['monthlyData'], 'E_tot', 'diffMinAltitude', startMonth = 12, endMonth = 12, fig=fig, ax=ax)
#plt.title('December')
