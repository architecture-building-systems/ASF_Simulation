# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 10:32:28 2017

@author: Jeri
credits: Mauro

"""

import sys, os

def readLayoutAndCombinations(path):
    """
    reads and executes LayoutAndCombinations.txt file \n
    input: path to results folder \n
    output: dictionary with LayoutAndCombinations
    """
    
    # import parameters used for simulation:
    with open(os.path.join(path,'LayoutAndCombinations.txt'), 'rb') as f:
        parameters = f.readlines()
        f.close()
    
    # execute all lines of the file:
    for i in range(len(parameters)):
        exec parameters[i]
    
    # save parameters to dictionary
    LayoutAndCombinations = {'Xangles':XANGLES, 'Yangles':YANGLES, 'NoClusters':NoClusters, 'panelSize':panelSize, 'panelSpacing':panelSpacing, 'ASFarray':ASFarray, 'desiredGridPointSize':desiredGridPointSize}
   
    return LayoutAndCombinations