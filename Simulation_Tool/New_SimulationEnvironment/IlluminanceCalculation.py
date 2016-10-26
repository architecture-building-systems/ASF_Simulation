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
paths['weather'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\WeatherData\Zuerich-Kloten_2005.epw' #paths['epw_name']

# add python_path to system path, so that all files are available:
sys.path.insert(0, paths['python'] + '\\aux_files')
sys.path.insert(0, paths['python'])

from epwreader import epw_reader
#read epw file of needed destination
weatherData = epw_reader(paths['weather'])


# define path of geographical location:
paths['geo'] = os.path.join(( paths['data'] + "\geographical_location"), geoLocation)






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

#gridSize = []




#for y_angle in [0,45]:
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

#for monthi in [1,3,6,9,12]:
#for HOD in [8,12,18]

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

gridSize = [800.0,400.0,200.0,100.0,50.0,25.0] #mm2
#gridSize = [7000.0, 6000.0, 5000.0] #mm2

illuminance_avg = {}
illuminance_data = {}

           
for size in gridSize:
    
    print 'size', size
        
    with open('illuminance.json','w') as f:
        f.write(json.dumps(size)) 
                
    #Wait until the radiation_results were created    
    while not os.path.exists(paths['illuminance']+'\\Illuminance_gridSize_' + str(size) +'_month_'+  str(monthi) + '_day_' + str(Day)  + '_hour_' + str(HOD) + '_xangle_'+ str(x_angle) + '_yangle_' + str(y_angle)+ '_.csv'):
        time.sleep(1)
           
    else:
        print 'next step'
        resultsdetected += 1

    print 'illuminance calculation finished!'
                                
    IlluminanceData = np.array([])
    
    with open(paths['illuminance']+'\\Illuminance_gridSize_' + str(size) +'_month_'+  str(monthi) + '_day_' + str(Day)  + '_hour_' + str(HOD) + '_xangle_'+ str(x_angle) + '_yangle_' + str(y_angle)+ '_.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for idx,line in enumerate(reader):
            if idx >= 6:
                IlluminanceData = np.append(IlluminanceData, [float(line[0])])
    illuminance_data[size] = IlluminanceData                        
    illuminance_avg[size]= np.average(IlluminanceData)
            
print 'illuminance calculation finished!'        
print "end"
                    

"""
#create DataFrame and store it as .csv
illuminance_avg_df = pd.DataFrame(illuminance_avg)
illuminance_avg_df.to_csv(paths['illuminance'] + '\\illuminance_avg_results_month_'+  str(monthi) + '_day_' + str(Day)  + '_hour_' + str(HOD) + '_xangle_'+ str(x_angle) + '_yangle_' + str(y_angle) +'.csv')
                                       
#plot avg values
fig0 = plt.figure()   
with pd.plot_params.use('x_compat', True):
     illuminance_avg_df.plot(color='y')   
plt.legend(loc='best')
plt.xlabel('grid size [mm]', fontsize=18)
plt.ylabel('average illuminance [lux]', fontsize=16)

#nomralize the illuminance value for the smallest value
#illuminance_avg_df[1].div(100,axis='columns')

#illuminance_avg_df[2] = illuminance_avg_df[1].div(100)

#plot normalized avg values

#plot avg values
fig1 = plt.figure()   
with pd.plot_params.use('x_compat', True):
     illuminance_avg_df.plot(color='y')   
plt.legend(loc='best')
plt.xlabel('grid size [mm]', fontsize=18)
plt.ylabel('average deviation [-]', fontsize=16)


#create folder to save figures as png:
paths['png'] =paths['illuminance'] + '\\png'

os.makedirs(paths['png'])
fig0.savefig(paths['png'] + '\\figure0' + '.png')
fig1.savefig(paths['png'] + '\\figure1' + '.png')


#Equation relating illuminance to irradiation.

  
glbRad = weatherData['glohorrad_Whm2']
glbIll = weatherData['glohorillum_lux']
#Measured data for plotting
X=glbRad
Y=glbIll

#Aquire best fit vector of coefficients. 1st order
eq = np.polyfit(X,Y,1)

#Vector for plotting the best fit
x=np.arange(0,1000)

"""















    
