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
Save = True

#calculation
calculation = False


# get current time
now = time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())

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


#set parmeters for evaluation
hour = [8, 12, 16]
Day = 6.0
monthi = 7.0
y_angle = 0

gridSize = [800.0 , 400.0, 200.0, 100.0, 50.] #mm2


if calculation == True:
    
    
    print "simulation start: " + now
    
    #Set Building Parameters
    building_data={"room_width":4900,     
    "room_height":3100,
    "room_depth":7000,
    "glazing_percentage_w":0.92,
    "glazing_percentage_h":0.97,
    }
    
    with open('building.json','w') as f:
        f.write(json.dumps(building_data))
    
    #paths['illuminance'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\IlluminanceResults\gridSizeAnalysis'
    paths['illuminance'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\IlluminanceResults'
    
    
    
    
    
    tic = time.time()
    
    resultsdetected=0
            
    print '\nStart illuminance calculation with ladybug'
    for HOD in hour:
        
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
            
                                     
                           
            for size in gridSize:
                
                
                print 'size', size
                toc = time.time() - tic
                print 'time passed (min): ' + str(toc/60.)
                
                illuminance = size
                    
                with open('illuminance.json','w') as f:
                    f.write(json.dumps(illuminance)) 
                            
                #Wait until the radiation_results were created
                #while not os.path.exists(paths['illuminance']+'\\Illuminance_gridSize_' + str(size) + '_hour_' + str(HOD) + '_xangle_'+ str(x_angle) + '_yangle_' + str(y_angle)+ '_.csv'):            
                while not os.path.exists(paths['illuminance']+'\\Illuminance_gridSize_' + str(size) +'_month_'+  str(monthi) + '_day_' + str(Day)  + '_hour_' + str(HOD) + '_xangle_'+ str(x_angle) + '_yangle_' + str(y_angle)+ '_.csv'):
                    time.sleep(3)
                       
                else:
                    print 'next step'
                    resultsdetected += 1
                                            
            
             
    print '\nGrid Size Analysis finished!\n'        



paths['illuminance'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\IlluminanceResults\gridSizeAnalysisNew'


illuminance_avg = {}
illuminance_data = {}

for x_angle in [0,90]:
    
    illuminance_avg[x_angle] = {}
    illuminance_data[x_angle] = {}   
    
    for HOD in hour:   
    
        illuminance_avg[x_angle][HOD] = {}
        illuminance_data[x_angle][HOD] = {}    
    
    
        for size in gridSize:
            
            IlluminanceData = np.array([])
            
            with open(paths['illuminance']+'\\Illuminance_gridSize_' + str(size) +'_month_'+  str(monthi) + '_day_' + str(Day)  + '_hour_' + str(HOD) + '_xangle_'+ str(x_angle) + '_yangle_' + str(y_angle)+ '_.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                for idx,line in enumerate(reader):
                    if idx >= 6:
                        IlluminanceData = np.append(IlluminanceData, [float(line[0])])
            illuminance_data[x_angle][HOD][size] = IlluminanceData                        
            illuminance_avg[x_angle][HOD][size] = np.average(IlluminanceData)
    



ill_angle = {}
ill_norm = {}
for x_angle in [0,90]:
    
    ill_norm[x_angle] = {}
    for HOD in hour:            

        ill_norm[x_angle][HOD] = {}
            
        for ii in gridSize:
            ill_norm[x_angle][HOD][ii] = (abs(1- illuminance_avg[x_angle][HOD][ii]/illuminance_avg[x_angle][HOD][50])) 
        


reform1 = {(outerKey, innerKey): values for outerKey, innerDict in ill_norm.iteritems() for innerKey, values in innerDict.iteritems()}

#ill_avg_df = pd.DataFrame(illuminance_avg)

ill_norm_df = pd.DataFrame(reform1).T   
   
reform2 = {(outerKey, innerKey): values for outerKey, innerDict in illuminance_avg.iteritems() for innerKey, values in innerDict.iteritems()}

ill_avg_df = pd.DataFrame(reform2).T


#gridConvergenceRad2 = [[],[],[],[],[]]
#
#for i in range(len(gridConvergence)):
#    gridConvergenceRad2[i%9].append(gridConvergence[(i,3)])
#    
#for i in range(9):
#    gridConvergenceRad2[i]=np.array(gridConvergenceRad2[i])



gridConvergenceBox = []

 

for i in range(len(gridSize)):
    gridConvergenceBox.append([])
    for x_angle in [0,90]:
        for HOD in hour:  
            gridConvergenceBox[i].append(illuminance_avg[x_angle][HOD][gridSize[i]]/illuminance_avg[x_angle][HOD][gridSize[4]])




if Plot == True:
    
    paths['illuminance'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\IlluminanceResults'
  
    #plot avg values
    fig0 = plt.figure(figsize=(4, 4))   
    #plt.subplot(1,2,1)
    
    with pd.plot_params.use('x_compat', True):
         ill_avg_df.plot(color=['y','r', 'b', 'k','c'], grid = True, logx = False)
         #.plot(color='r', xticks = gridSize, grid = True, logx = False)
    plt.title('Average Hourly Illuminance')
    plt.legend(loc=4, fontsize = 8)
    #plt.xlabel('grid size [mm]', fontsize=12)
    plt.ylabel('average illuminance [lux]', fontsize=12)    
#    
    #plot normalized values
    fig1 = plt.figure(figsize=(4, 4))   
    
    #plt.subplot(1,2,2)
    
    with pd.plot_params.use('x_compat', True):
         ill_norm_df.plot(color=['y','r', 'b', 'k','c'], yticks = None,  logx = False,  grid =True)
         #ill_norm_df[90].plot(color='r', yticks = None, xticks = gridSize, logx = False,  grid =True, legend = x_angle)
    plt.title('Normalised Hourly Illuminance')     
    plt.legend(loc='best', fontsize = 8) 
    plt.xlabel('grid size [mm]', fontsize=12)
    plt.ylabel('average deviation [-]', fontsize=12)
    
    
    
    fig2 = plt.figure(figsize=(6, 6))

    plt.suptitle("Grid Convergence for the Illuminance Calculation", size=16)

    plt.style.use('ggplot')
    
    #plt.subplot(2,1,2)
    #plt.subplot(1,2,2)   
    
    data = gridConvergenceBox
    
    
    
    xindex = [1,2,3,4,5] #[800, 400, 200 , 100 , 50]
    
    box = plt.boxplot(data, notch= False, patch_artist=True)
    
    plt.xticks(xindex,('800','400', '200','100','50'),size = 14)
    
    plt.yticks(size=14)
    #plt.yticks([0.9,0.95,1,1.05,1.1],size=14)
    plt.ylabel('normalized radiation [-]', fontsize = 14)
    plt.xlabel('grid size [mm]', fontsize = 14)
    #colors = ['cyan', 'lightblue', 'lightgreen', 'tan', 'pink', 'red']
    colors = ['cyan']*5
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
    
    #plt.tight_layout()
    plt.subplots_adjust(hspace=0.22, wspace=0.54, right=0.98, left=0.08, bottom=0.11)
    plt.grid()
    plt.show()

    
Save = False      
   
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
    fig2.savefig(paths['png'] + '\\figure2' + '.png')

    print '\nResults are saved!'
    
print "Program Finished"      













    
