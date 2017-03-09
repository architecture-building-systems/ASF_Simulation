# -*- coding: utf-8 -*-
"""
Created on Wed Nov 02 08:30:45 2016

@author: Mauro
"""
import sys, os
import time
import json
import csv
import numpy as np

#def CalculateRadiationData(SimulationPeriode, XANGLES, YANGLES, paths):


    
print '\nStart radiation calculation with ladybug'
print 'Time: ' + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())


#
#result = np.array([])
#GridSize = [400,200,100,50,25]
#XANGLES = [0,45,90]
#YANGLES = [-45,0,45]
#
#
#pat = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\radiation_wall_ZH13_GridSizeWindow'
#
#for size in GridSize:
#    for monthi in range(6, 6+1): #month:
#         for day in range(6, 6 + 1):
#             
#            for hour in range(5, 20 + 1):
#    
#                #BuilRadData[hour]= {}
#                comb = -1             
#                for x_angle in XANGLES:
#                    for y_angle in YANGLES:
#                        comb += 1
#                                        
#                                             
#                    
#                    
#                        tic = time.time()
#                        
#                        #BuilRadData[hour][comb][size] = {}
#                        
#                        comb_data={"x_angle":x_angle,
#                                   "y_angle":y_angle,
#                                   "Hour":hour,
#                                   "Day": day,
#                                   "Month":monthi,
#                                   'Size' : size
#                                   }
#                        
#                        #create json file with the set combination of x-angle,y-angle and HOY
#                        with open('comb.json','w') as f:
#                            f.write(json.dumps(comb_data))
#                            
#                        
#                        
#                                                                                        
#                        #read total radition on wall and save it in BuildingRadiationData              
#                        while not os.path.exists(os.path.join(pat, 'RadiationWall' + '_' + str(hour) + '_' + str(day) + '_'+ str(size) + '_' + str(x_angle) + '_' + str(y_angle) + '.csv')):
#                            time.sleep(0.5)
#                        else:
#                           
#                            print size, hour, day, monthi, x_angle, y_angle
#                            toc = time.time() - tic
#                            print 'time passed (sec): ' + str(toc)
#                                
#                               
#                    
#                            

#
paths = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\radiation_wall_ZH13_GridSizeWindow'
day = 6
result = []
GridSize = [400,200,100,50,25]#,12.5]

ii = 0
for hour in range(5,20 + 1):

    comb = -1             
    for x_angle in [0,45,90]:
        for y_angle in [-45,0,45]:

            comb += 1

            for size in GridSize:                            

                with open(os.path.join(paths, 'RadiationWall' + '_' + str(hour) + '_' + str(day) + '_' + str(size) + '_' + str(x_angle) + '_' + str(y_angle) + '.csv'), 'r') as csvfile: 
                   reader = csv.reader(csvfile)
                   for idx,line in enumerate(reader):
                       if idx == 1:
                           value = float(line[0])
                           break

                
                result.append([hour, comb, size, value])
                ii += 1
                
import pandas as pd 
df = pd.DataFrame(result)
df.to_csv("C:\Users\Assistenz\Desktop\Mauro\GridSizeAnalysis\GridSizeWindow.csv")