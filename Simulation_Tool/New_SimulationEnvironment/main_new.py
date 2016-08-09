# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:14:42 2016

main file for simulation environment

@author: Prageeth Jayathissa
@credits: Jerimias Schmidli
"""

import os, sys
import numpy as np
import json
import time
import warnings

#Set Solar Panel Properties
XANGLES=[0,22.5,45,67.5,90]
YANGLES= [-45,-22.5,0,22.5,45]


panel_data={"XANGLES": XANGLES ,
"YANGLES" : YANGLES,
"NoClusters":1,
"numberHorizontal":6,
"numberVertical":9,
"panelOffset":400,
"panelSize":400,
"panelSpacing":500,
}

#Set Building Parameters
building_data={"room_width":4900,
"room_height":3100,
"glazing_percentage_w":0.92,
"glazing_percentage_h":0.97,
}

#Save parameters to be imported into grasshopper
with open('panel.json','w') as f:
    f.write(json.dumps(panel_data))

with open('building.json','w') as f:
    f.write(json.dumps(building_data))


waitfile=True
resultsdetected=0
for HOY in range(10,11):

    for x_angle in XANGLES:
        for y_angle in YANGLES:
            
            comb_data={"x_angle":x_angle,
                       "y_angle":y_angle,
                       "HOY":HOY}
            
            with open('comb.json','w') as f:
                f.write(json.dumps(comb_data))
                time.sleep(5)
            
            while waitfile:
                if os.path.exists('radiation_resultsRadiationResults.csv'):
                    resultsdetected+=1
                    os.remove('radiation_resultsRadiationResults.csv')
                    waitfile=False
                    print 'next ste', x_angle, y_angle
            waitfile=True
                

