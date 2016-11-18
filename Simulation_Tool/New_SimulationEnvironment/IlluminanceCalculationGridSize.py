"""
Created on Thu Mar 24 11:14:42 2016

main file for simulation environment

@author: Mauro Luzzatto 


25.10.2016

Illuminance calculation, grid size analysis

"""

import os, sys
import numpy as np
import json
import time
import csv
import matplotlib.pyplot as plt
import csv
import pandas as pd



#create Plots
Plot = True
#save Results
Save = False


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

paths['illuminance'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\IlluminanceResults\gridSizeAnalysis'

#set parmeters for evaluation
HOD = 12.0
Day = 6.0
monthi = 7.0
y_angle = 0



tic = time.time()

resultsdetected=0
        
print '\nStart illuminance calculation with ladybug'

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
    
                
    print HOD, monthi, x_angle
            
    comb_data={"x_angle": x_angle,
               "y_angle":y_angle,
               "HOD":HOD,
               "Month":monthi,
               "Day": Day
                }
                
     #create json file with the set combination of x-angle,y-angle and HOY
    with open('comb.json','w') as f:
        f.write(json.dumps(comb_data))
    
                             
    ab = [0,1,2,3]
    aa = [0.5, 0.25, 0]
    ad = [0,1024, 2048]
    ar = [8,64,128]
    aS = [0,256,512]
    
    gridSize = [400.0]#, 200.0, 100.0, 50., 25.] #mm2
   
#    
                   
    for size in gridSize:
        for abi in ab:
            for aai in aa:
                for adi in ad:
                    for ari in ar:
                        for aSi in aS:
        
                            print 'size', size
                            toc = time.time() - tic
                            print 'time passed (min): ' + str(toc/60.)
                            
                            illuminance = {
                            'Size': size,
                            'ab': abi,
                            'aa':aai,
                            'ar':ari,
                            'ad':adi,
                            'as':aSi        
                            }
                                
                            with open('illuminance.json','w') as f:
                                f.write(json.dumps(illuminance)) 
                                        
                            #Wait until the radiation_results were created
                            while not os.path.exists(paths['illuminance']+'\\Illuminance_gridSize_' + str(size) +'_para_'+  str(abi) +'_' +str(aai)+ '_' +str(ari)+ '_' +str(adi) + '_' +str(aSi)  + '_hour_' + str(HOD) + '_xangle_'+ str(x_angle) + '_yangle_' + str(y_angle)+ '_.csv'):            
                            #while not os.path.exists(paths['illuminance']+'\\Illuminance_gridSize_' + str(size) +'_month_'+  str(monthi) + '_day_' + str(Day)  + '_hour_' + str(HOD) + '_xangle_'+ str(x_angle) + '_yangle_' + str(y_angle)+ '_.csv'):
                                time.sleep(3)
                                   
                            else:
                                print 'next step'
                                resultsdetected += 1
                                    
    
         
print '\nGrid Size Analysis finished!\n'        

"""

illuminance_avg = {}
illuminance_data = {}

for x_angle in [0,90]:
 #for monthi in [1,4,8,12]:
        #for HOD in [12]   
    
    
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
    



ill_angle = {}

for x_angle in [0,90]:            

    ill_norm = {}
        
    for ii in gridSize:
        ill_norm[ii] = abs(1- illuminance_avg[x_angle][ii]/illuminance_avg[x_angle][12.5]) 
    
    ill_angle[x_angle]= ill_norm

ill_norm_df = pd.DataFrame(ill_angle)
ill_avg_df = pd.DataFrame(illuminance_avg)   



if Plot == True:   
    #plot avg values
    fig0 = plt.figure(figsize=(8, 4))   
    with pd.plot_params.use('x_compat', True):
         ill_avg_df[0].plot(color='y', xticks = gridSize, grid = True, logx = False)
         ill_avg_df[90].plot(color='r', xticks = gridSize, grid = True, logx = False)
    plt.title('Average Hourly Illuminance')
    plt.legend(loc='best')
    plt.xlabel('grid size [mm]', fontsize=12)
    plt.ylabel('average illuminance [lux]', fontsize=12)    
    
    #plot normalized values
    fig1 = plt.figure(figsize=(8, 4))   
    with pd.plot_params.use('x_compat', True):
         ill_norm_df[0].plot(color='y', yticks = None, xticks = gridSize, logx = False,  grid =True, legend = x_angle)
         ill_norm_df[90].plot(color='r', yticks = None, xticks = gridSize, logx = False,  grid =True, legend = x_angle)
    plt.title('Normalised Hourly Illuminance')     
    plt.legend(loc='best') 
    plt.xlabel('grid size [mm]', fontsize=12)
    plt.ylabel('average deviation [-]', fontsize=12)
    
    
    
   
if Plot == True and Save == True:   

    paths['result']= os.path.join(paths['illuminance'], 'Results_' + str(now))
    
    os.makedirs(paths['result'])    
    
    ill_avg_df.to_csv(paths['result'] + '\\illuminance_gridSizeAnalysis_averageValues.csv')
    ill_norm_df.to_csv(paths['result'] + '\\illuminance_gridSizeAnalysis_normalisedValues.csv')                                   
    
    
    #create folder to save figures as png:
    paths['png'] =paths['result'] + '\\png'
    
    os.makedirs(paths['png'])
    fig0.savefig(paths['png'] + '\\figure0' + '.png')
    fig1.savefig(paths['png'] + '\\figure1' + '.png')

    print '\nResults are saved!'
    
print "Program Finished"      



"""










    
