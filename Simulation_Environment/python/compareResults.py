# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 11:16:09 2016

Compare Results script

@author: Jeremias
"""

import numpy as np
import sys, os

# assign results folders to compare:
resultsFolder1 = 'Kloten_2clust_5x_1y'

resultsFolder2 = 'Kloten_25comb'

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

# plot data 
figures = compareResultsFigure(results1['monthlyData'], results2['monthlyData'])

