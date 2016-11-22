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

def CalculateRadiationData(SimulationPeriode, XANGLES, YANGLES, paths, DataNamePV, DataNameWin, GridSize):

                   
#    if not os.path.isfile(os.path.join(paths['PV'], 'HourlyPV_electricity_results_' + DataNamePV + '.npy')) or not os.path.isfile(os.path.join(paths['PV'], 'HourlyBuildingRadiationData_' + DataNameWin + '.npy')):    
#        if not os.path.isdir(paths['PV']):
#            os.makedirs(paths['PV'])
    
    # create dicitionary to save optimal angles:
    BuilRadData = {}
    
    comb = 0        
    
    print '\nStart radiation calculation with ladybug'
    print 'Time: ' + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())

    tic = time.time()
    
    
    #GridSize = [12.5]
    
    for monthi in range(SimulationPeriode['FromMonth'], SimulationPeriode['ToMonth']+1): #month:
         for day in range(SimulationPeriode['FromDay'], SimulationPeriode['ToDay'] + 1):
             
            for hour in range(SimulationPeriode['FromHour'], SimulationPeriode['ToHour'] + 1):

                #BuilRadData[hour]= {}
                             
                for x_angle in XANGLES:
                    for y_angle in YANGLES:

                        #BuilRadData[hour][comb] = {}                            
                        comb +=1                            
                        
                        for size in GridSize:
                            
                            #BuilRadData[hour][comb][size] = {}
                            
                            comb_data={"x_angle":x_angle,
                                       "y_angle":y_angle,
                                       "Hour":hour,
                                       "Day": day,
                                       "Month":monthi,
                                       'Size' : size
                                       }
                            
                            #create json file with the set combination of x-angle,y-angle and HOY
                            with open('comb.json','w') as f:
                                f.write(json.dumps(comb_data))
                                
                            print size, hour, day, monthi, x_angle, y_angle
                            toc = time.time() - tic
                            print 'time passed (min): ' + str(toc/60.)
                            
                                                                                            
                            #read total radition on wall and save it in BuildingRadiationData              
                            while not os.path.exists(os.path.join(paths['radiation_wall'], 'RadiationWall' + '_' + str(hour) + '_' + str(day) + '_'+ str(size) + '_' + str(x_angle) + '_' + str(y_angle) + '.csv')):
                                time.sleep(0.5)
                            else:
                                pass
#                                    with open(os.path.join(paths['radiation_wall'], 'RadiationWall' + '_' + str(hour) + '_' + str(day) + '_' + str(size) + '_' + str(x_angle) + '_' + str(y_angle) + '.csv'), 'r') as csvfile:
#                                        reader = csv.reader(csvfile)
#                                        for idx,line in enumerate(reader):
#                                            if idx == 1:
#                                                BuilRadData[hour][comb][size] = float(line[0]) *1000.
#                                                break
#    
#                    
#                        
#    
#        np.save(os.path.join(paths['save_results_path'],'HourlyBuildingRadiationData_' + DataNameWin + '.npy'), BuilRadData)
#        print "\nEnd of radiation calculation: " + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())

#    else:
#        BuilRadData = np.load(os.path.join(paths['PV'], 'HourlyBuildingRadiationData_' + DataNameWin + '.npy')).item()
#        print '\nLadyBug data loaded from Folder:'
#        print 'radiation_wall_'+ DataNameWin   
    
    return BuilRadData