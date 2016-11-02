# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 16:58:45 2016

@author: Assistenz
"""
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:14:42 2016

main file for simulation environment

@author: Mauro Luzzatto 
@credits: Prageeth Jayathissa, Jerimias Schmidli

25.10.2016

Illuminance

"""

import os, sys
import numpy as np
import json
import time
import warnings
import csv
import matplotlib.pyplot as plt
import csv
import pandas as pd
import math

# get current time
now = time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
print "simulation start: " + now

geoLocation = 'Zuerich_Kloten_2013'

# create dictionary to write all paths:
paths = {}

# find path of current folder (simulation_environment)
paths['main'] = os.path.abspath(os.path.dirname(sys.argv[0]))

# define paths of subfolders:
paths['data'] = paths['main'] + '\\data'
paths['python'] = paths['main'] + '\\python'



# define path of weather file:
paths['weather'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\WeatherData\Zuerich_Kloten_2013.epw' #paths['epw_name']

# add python_path to system path, so that all files are available:
sys.path.insert(0, paths['python'] + '\\aux_files')
sys.path.insert(0, paths['python'])

from epwreader import epw_reader
#read epw file of needed destination
weatherData = epw_reader(paths['weather'])


# define path of geographical location:
paths['geo'] = os.path.join(( paths['data'] + "\geographical_location"), geoLocation)

paths['radiation_wall'] = os.path.join(paths['main'], 'radiation_wall')




#Set Building Parameters
building_data={"room_width":4900,     
"room_height":3100,
"room_depth":7000,
"glazing_percentage_w":0.92,
"glazing_percentage_h":0.97,
}

with open('building.json','w') as f:
    f.write(json.dumps(building_data))

paths['illuminance'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\IlluminanceResults'

#set parmeters for evaluation



HOD = 12.0
Day = 15.0
monthi = 1.0
x_angle = 0
y_angle = 0

#gridSize = [50.]

combination = 0

tic = time.time()

for x_angle in [0,90]:

    #Set panel data
    panel_data={"XANGLES": x_angle ,
    "YANGLES" : y_angle,
    "NoClusters":1,
    "numberHorizontal":6,
    "numberVertical":9,
    "panelOffset":400,
    "panelSize":400,
    "panelSpacing":500,
    }
    
    #Save parameters to be imported into grasshopper
    with open('panel.json','w') as f:
        f.write(json.dumps(panel_data))
    
#    for monthi in [1,3,6,9,12]:
#        for HOD in [8,10,12,16,18,20]:
            
        print "Combination number", combination
        print HOD, monthi, x_angle
        combination += 1
        
        
        comb_data={"x_angle": x_angle,
                   "y_angle":y_angle,
                   "HOD":HOD,
                   "Month":monthi,
                   "Day": Day
                    }
                    
         #create json file with the set combination of x-angle,y-angle and HOY
        with open('comb.json','w') as f:
            f.write(json.dumps(comb_data))
        
                                 
        resultsdetected=0
        
        print '\nStart illuminance calculation with ladybug'
        
        gridSize = [400.0, 200.0, 100.0, 50., 25., 12.5] #mm2
        #gridSize = [50.0]
                           
        for size in gridSize:
            
            print 'size', size
            toc = time.time() - tic
            print 'time passed (min): ' + str(toc/60.)
                
            with open('illuminance.json','w') as f:
                f.write(json.dumps(size)) 
                        
            #Wait until the radiation_results were created    
            while not os.path.exists(paths['illuminance']+'\\Illuminance_gridSize_' + str(size) +'_month_'+  str(monthi) + '_day_' + str(Day)  + '_hour_' + str(HOD) + '_xangle_'+ str(x_angle) + '_yangle_' + str(y_angle)+ '_.csv'):
                time.sleep(3)
                   
            else:
                print 'next step'
                resultsdetected += 1
    
#                #read total radition on wall and save it in BuildingRadiationData              
#                while not os.path.exists(os.path.join(paths['radiation_wall'], 'RadiationWall' + '_' + str(int(HOD)) +'_'+ str(monthi) + '_'+ str(x_angle) + '_' + str(y_angle) + '.csv')):
#                    time.sleep(1)
#                else:
#                    pass

                                    
    
         
print 'illuminance calculation finished!'        

illuminance_avg = {}
illuminance_data = {}

for x_angle in [0,90]:#[0,90]:
 #for monthi in [1,3,6,9,12]:
        #for HOD in [8,12,18]   
    
    
    illuminance_avg[x_angle] = {}
    illuminance_data[x_angle] = {}
    for size in gridSize:
        
        IlluminanceData = np.array([])
        
        with open(paths['illuminance']+'\\Illuminance_gridSize_' + str(size) +'_month_'+  str(monthi) + '_day_' + str(Day)  + '_hour_' + str(HOD) + '_xangle_'+ str(x_angle) + '_yangle_' + str(y_angle)+ '_.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for idx,line in enumerate(reader):
                if idx >= 6:
                    IlluminanceData = np.append(IlluminanceData, [float(line[0])])
        illuminance_data[x_angle][size] = IlluminanceData                        
        illuminance_avg[x_angle][size]= np.average(IlluminanceData)
    




for x_angle in [0,90]:#[0,90]:              

    
    
    ill_norm = {}
    ill_angle = {}
    
    for ii in gridSize:
        ill_norm[ii] = abs(1- illuminance_avg[x_angle][ii]/illuminance_avg[x_angle][12.5]) 
    
    ill_angle[x_angle]= ill_norm

ill_norm_df = pd.DataFrame(ill_angle)
   
print "end"   

"""    
    #ill_norm_df.plot(logx=True)
    ##plot normalized avg values
    
    fig0 = plt.figure()   
    with pd.plot_params.use('x_compat', True):
         ill_norm_df.plot(color='y', yticks = None, xticks = gridSize, logx = False,  grid =True, legend = x_angle)
     
    plt.xlabel('grid size [mm]', fontsize=12)
    plt.ylabel('average deviation [-]', fontsize=12)
    

    #plot avg values
    fig1 = plt.figure()   
    with pd.plot_params.use('x_compat', True):
         ill_avg_df.plot(color='b', xticks = gridSize, grid = True)   
    plt.legend(loc='best')
    plt.xlabel('grid size [mm]', fontsize=18)
    plt.ylabel('average illuminance [lux]', fontsize=16)
    
    
    
    # Axis scale must be set prior to declaring the Formatter
    # If it is not the Formatter will use the default log labels for ticks.
    plt.figure()
    plt.set_xscale('log')
    
    
    
    
    # Create some artificial data.
    result1 = ill_norm
    xvalue = gridSize
    
    
    # Plot
    plt.scatter(result1, xvalue, s=40, c='b', marker='s', faceted=False)
    
    
    plt.set_xlim(1e-1, 1e4)
    plt.set_ylim(1e-1, 1e4)
    plt.grid(True)
    
    plt.xlabel(r"Result", fontsize = 12)
    plt.ylabel(r"Prediction", fontsize = 12)






    paths['result']= os.path.join(paths['illuminance'], 'Results_' + geoLocation + '_xangle_'+ str(x_angle) + '_yangle_' + str(y_angle))
    
    if not os.path.isdir(paths['result']):
        os.makedirs(paths['result'])    
    
    ill_avg_df.to_csv(paths['result'] + '\\illuminance_avg_results_month_'+  str(monthi) + '_day_' + str(Day)  + '_hour_' + str(HOD) + '_xangle_'+ str(x_angle) + '_yangle_' + str(y_angle) +'.csv')
    ill_norm_df.to_csv(paths['result'] + '\\illuminance_norm_results_month_'+  str(monthi) + '_day_' + str(Day)  + '_hour_' + str(HOD) + '_xangle_'+ str(x_angle) + '_yangle_' + str(y_angle) +'.csv')                                   


    #create folder to save figures as png:
    paths['png'] =paths['result'] + '\\png'
    
    os.makedirs(paths['png'])
    fig0.savefig(paths['png'] + '\\figure0' + '.png')
    fig1.savefig(paths['png'] + '\\figure1' + '.png')

    
    fig = plt.figure()
    ax = plt.gca()
    ax.plot(data['o_value'] ,data['time_diff_day'], 'o', c='blue', alpha=0.05, markeredgecolor='none')
    ax.set_yscale('log')
    ax.set_xscale('log')
    
    
    data = DataFrame(pd.read_csv(file_name))

    y = np.log(data['o_value'], dtype='float64')
    x = np.log(data['time_diff_day'], dtype='float64')
    
    fig = plt.figure()
    plt.scatter(x, y, c='blue', alpha=0.05, edgecolors='none')
    fig.suptitle('test title', fontsize=20)
    plt.xlabel('time_diff_day', fontsize=18)
    plt.ylabel('o_value', fontsize=16)
    plt.xticks(gridSize)
    
    plt.grid(True)
    pylab.show()

    """
#BuildingRadiationData = np.array([])
#
#with open(os.path.join(paths['radiation_wall'], 'RadiationWall' + '_' + str(int(HOD)) +'_'+ str(monthi) + '_'+ str(x_angle) + '_' + str(y_angle) + '.csv'), 'r') as csvfile:
#   reader = csv.reader(csvfile)
#   for idx,line in enumerate(reader):
#       if idx == 1:
#           BuildingRadiationData = np.append(BuildingRadiationData, [float(line[0])])
#           break












    
