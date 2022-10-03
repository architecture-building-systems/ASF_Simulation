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

def CalculateRadiationData(XANGLES, YANGLES, paths, daysPerMonth, hour_in_month, FolderName):
                   
    if not os.path.isfile(os.path.join(paths['PV'], 'BuildingRadiationData_' + FolderName['FileName'] + '.npy')) or not os.path.isfile(os.path.join(paths['PV'], 'BuildingRadiationData_' + FolderName['FileName'] + '.npy')):    
        if not os.path.isdir(paths['PV']):
            os.makedirs(paths['PV'])

        # create dicitionary to save optimal angles:
        BuildingRadiationData_HOD = {}
        
        resultsdetected=0
        
        print '\nStart radiation calculation with ladybug'
        print '\nTime: ' + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())

        tic = time.time()
        
    
        for monthi in range(1,13): #month:
              
            BuildingRadiationData_HOD[monthi] = {}
            
            for HOD in hour_in_month[monthi]:
                
                BuildingRadiationData = np.array([])
                
                for x_angle in XANGLES:
                    for y_angle in YANGLES:
                        
                        comb_data={"x_angle":x_angle,
                                   "y_angle":y_angle,
                                   "HOD":HOD,
                                   "Month":monthi
                                   }
                                   
                        #create json file with the set combination of x-angle,y-angle and HOY
                        with open('comb.json','w') as f:
                            f.write(json.dumps(comb_data))
                            
                        print HOD, monthi, x_angle, y_angle, resultsdetected
                        toc = time.time() - tic
                        print 'time passed (min): ' + str(toc/60.)
                        
   
                        #Wait until the radiation_results were created    
                        while not os.path.exists(os.path.join(paths['radiation_results'],'RadiationResults' +'_'+  str(int(HOD)) + '_' + str(monthi)  + '_' + str(x_angle) + '_' + str(y_angle)+ '.csv')):
                            time.sleep(1)
                            
                                                
                        else:
                            print 'next step'
                            resultsdetected += 1
                                                                                            
                            #read total radition on wall and save it in BuildingRadiationData              
                            while not os.path.exists(os.path.join(paths['radiation_wall'], 'RadiationWall' + '_' + str(int(HOD)) +'_'+ str(monthi) + '_'+ str(x_angle) + '_' + str(y_angle) + '.csv')):
                                time.sleep(1)
                            else:
                                with open(os.path.join(paths['radiation_wall'], 'RadiationWall' + '_' + str(int(HOD)) +'_'+ str(monthi) + '_'+ str(x_angle) + '_' + str(y_angle) + '.csv'), 'r') as csvfile:
                                    reader = csv.reader(csvfile)
                                    for idx,line in enumerate(reader):
                                        if idx == 1:
                                            BuildingRadiationData = np.append(BuildingRadiationData, [float(line[0])])
                                            break
                                
                                                   
                
                for jj in range(0,daysPerMonth[monthi-1]):
                    #Radiation data is calculated for all days per month, so the data is divided through the amount of days per month
                    BuildingRadiationData_HOD[monthi][HOD+24*jj]= BuildingRadiationData * 1/daysPerMonth[monthi-1] *1000. #W/h
                
                #print len(BuildingRadiationData_HOD[monthi][HOD+24*jj])
        
        np.save(os.path.join(paths['save_results_path'],'BuildingRadiationData_' + FolderName['FileName'] + '.npy'),BuildingRadiationData_HOD)
        print "\nEnd of radiation calculation: " + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())

    else:
        BuildingRadiationData_HOD = np.load(os.path.join(paths['PV'], 'BuildingRadiationData_' + FolderName['FileName'] + '.npy'), allow_pickle=True).item()
        print '\nLadyBug data loaded from Folder:'
        print 'radiation_wall_'+ FolderName['DataFolderName']
        print 'File: ', FolderName['FileName']
     
    
    
    return BuildingRadiationData_HOD