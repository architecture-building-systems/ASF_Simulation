# -*- coding: utf-8 -*-
"""
Created on Tue Jan 05 14:16:24 2016

Function to read RadiationResults.csv

@author: Jeremias Schmidli
"""

import csv

def import_radiation(path, filename):

    with open(path + filename, 'rb') as f:
        reader = csv.reader(f)
        Radiation_string = list(reader)
    total_radiation = float(Radiation_string[1][0])
    panel_size = float(Radiation_string[3][0])
    for i in range(0,5):
        del Radiation_string[0]
        
    Radiation=[]
    for j in range(0,len(Radiation_string)):
        Radiation.append([])
        
        for k in Radiation_string[j]:
            Radiation[j].append(float(k))
    f.close()
    return (Radiation, total_radiation, panel_size)
        
