
"""
Created on Fri Oct 14 15:35:22 2016

@author: Mauro
"""

import os, sys
import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np


# create dictionary to write all paths:
paths = {}

# find path of current folder (simulation_environment)
paths['main'] = os.path.abspath(os.path.dirname(sys.argv[0]))


# define path of weather file:
paths['ZH2013'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\WeatherData\Zuerich_Kloten_2013.epw'
#paths['ZH2005'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\WeatherData\Zuerich_Kloten_2005.epw'
#paths['GE'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\WeatherData\CHE_Geneva.067000_IWEC.epw'
#paths['FR'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\WeatherData\DEU_Frankfurt.am.Main.106370_IWEC.epw'


from epwreader import epw_reader
#read epw file of needed destination
weatherDataZH13 = epw_reader(paths['ZH2013'])
#weatherDataZH05 = epw_reader(paths['ZH2005'])
#weatherDataGE = epw_reader(paths['GE'])
#weatherDataFR = epw_reader(paths['FR'])

#DataNameWin = 'ZH13_49comb_cloudy_4_7'
#paths['PV'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\PV_results'
#
#
#BuilRadData = np.load(os.path.join(paths['PV'], 'HourlyBuildingRadiationData_' + DataNameWin + '.npy')).item()
#print '\nLadyBug data loaded from Folder:'
#print 'radiation_wall_'+ DataNameWin   

#Rad = [0.,0.]
#
#for ii in range(1,25):
#
#  Rad.append(BuilRadData[7][4][ii][3])
#  
#  
#
#Dir = weatherDataZH13['dirnorrad_Whm2'][4417:4441].T
#
#x,y = [],[]
#
#RAD = Rad[0:24]
#
#
#
#y = RAD
#x = Dir
#
#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.plot(x,y,'o')
#
#plt.legend(loc='best')
#plt.xlabel('direct normal radiation [Wh/m2]', fontsize=12)
#plt.ylabel('Building Radiation [Wh]', fontsize=12)
#
#plt.show()


fig = plt.figure(figsize=(12, 4))
#plt.title("Linear Correlations for differen Locations", fontsize=16)

#Achtung evt. um eine stunde verschoben

#1
time = range(4512,4536)

ax1 = fig.add_subplot(131) 
#ax1.title('Cloudy Day', fontsize=12)
ax1.title.set_text('08.07.2013')      

with pd.plot_params.use('x_compat', True):
    weatherDataZH13['dirnorrad_Whm2'][time].plot(color='r')    
    weatherDataZH13['difhorrad_Whm2'][time].plot(color='b')
    weatherDataZH13['glohorrad_Whm2'][time].plot(color='g')
    
plt.legend(loc=1, fontsize = 10)
#plt.legend(loc='best')
plt.xlabel('Hour of Day', fontsize=12)
plt.ylabel('Radiation [Wh/m2]', fontsize=12)











plt.style.use('ggplot')


fig = plt.figure(figsize=(12, 4))
#plt.title("Linear Correlations for differen Locations", fontsize=16)

#Achtung evt. um eine stunde verschoben

#1
a= {'direct': range(0,24) ,'diffuse': range(0,24) , 'global': range(0,24) }

a['direct'][1:25] = weatherDataZH13['dirnorrad_Whm2'][4416:4440]
a['diffuse'][1:25] = weatherDataZH13['difhorrad_Whm2'][4416:4440]
a['global'][1:25] = weatherDataZH13['glohorrad_Whm2'][4416:4440]

a = pd.DataFrame(a)

ax1 = fig.add_subplot(131) 
#ax1.title('Cloudy Day', fontsize=12)
ax1.title.set_text('Cloudy Day: 04.07.2013')      

with pd.plot_params.use('x_compat', True):
    a['global'].plot(color='r')    
    a['direct'].plot(color='b')
    a['diffuse'].plot(color='g')
    
plt.legend(loc=1, fontsize = 10)
#plt.legend(loc='best')
plt.xlabel('Hour of Day', fontsize=12)
plt.ylabel('Radiation [Wh/m2]', fontsize=12)



#2
a= {'direct': range(24) ,'diffuse': range(24) , 'global': range(24) }

a['direct'][1:25] = weatherDataZH13['dirnorrad_Whm2'][4464:4490]
a['diffuse'][1:25] = weatherDataZH13['difhorrad_Whm2'][4464:4490]
a['global'][1:25] = weatherDataZH13['glohorrad_Whm2'][4464:4490]

a = pd.DataFrame(a)

ax2 = fig.add_subplot(132) 
ax2.title.set_text('Sunny Day: 06.07.2013')

with pd.plot_params.use('x_compat', True):
    a['global'].plot(color='r')    
    a['direct'].plot(color='b')
    a['diffuse'].plot(color='g')
    

plt.legend(loc=1, fontsize = 10)
#plt.legend(loc='best')
plt.xlabel('Hour of Day', fontsize=12)
#plt.ylabel('Radiation [Wh/m2]', fontsize=12)



#3
a= {'direct': range(24) ,'diffuse': range(24) , 'global': range(24) }

a['direct'][1:25] = weatherDataZH13['dirnorrad_Whm2'][4561:4585]
a['diffuse'][1:25] = weatherDataZH13['difhorrad_Whm2'][4561:4585]
a['global'][1:25] = weatherDataZH13['glohorrad_Whm2'][4561:4585]

a = pd.DataFrame(a)

ax3 = fig.add_subplot(133) 
ax3.title.set_text('Half Cloudy Day: 10.07.2016')

with pd.plot_params.use('x_compat', True):
    a['global'].plot(color='r')    
    a['direct'].plot(color='b')
    a['diffuse'].plot(color='g')
    

plt.legend(loc=1, fontsize = 10)
#plt.legend(loc='best')
plt.xlabel('Hour of Day', fontsize=12)
#plt.ylabel('Radiation [Wh/m2]', fontsize=12)

plt.tight_layout()


save = False

if save == True:
    fig.savefig(r'C:\Users\Assistenz\Desktop\Mauro\Images\figure1.pdf')

##############################################################################
"""
#old


fig = plt.figure(figsize=(12, 4))


ax1 = fig.add_subplot(131) 
#ax1.title('Cloudy Day', fontsize=12)
ax1.title.set_text('Cloudy Day: 04.07.2013')      

with pd.plot_params.use('x_compat', True):
    weatherDataZH13['glohorrad_Whm2'][4415:4440].plot(color='r')    
    weatherDataZH13['dirnorrad_Whm2'][4415:4440].plot(color='b')
    weatherDataZH13['difhorrad_Whm2'][4415:4440].plot(color='g')
    

plt.legend(loc=2, fontsize = 7)
#plt.legend(loc='best')
plt.xlabel('Hour of the year', fontsize=12)
plt.ylabel('Radiation [Wh/m2]', fontsize=12)




ax2 = fig.add_subplot(132) 
ax2.title.set_text('Day without Clouds: 06.07.2013')
        
with pd.plot_params.use('x_compat', True):
    weatherDataZH13['glohorrad_Whm2'][4460:4485].plot(color='r')
    weatherDataZH13['dirnorrad_Whm2'][4460:4485].plot(color='b')
    weatherDataZH13['difhorrad_Whm2'][4460:4485].plot(color='g')
    

plt.legend(loc=2, fontsize = 7)
#plt.legend(loc='best')
plt.xlabel('Hour of the year', fontsize=12)
#plt.ylabel('Wh per m2', fontsize=12)


ax3 = fig.add_subplot(133) 
ax3.title.set_text('Half Cloudy Day: 10.07.2016')
        
with pd.plot_params.use('x_compat', True):
    weatherDataZH13['glohorrad_Whm2'][4555:4580].plot(color='r')
    weatherDataZH13['dirnorrad_Whm2'][4555:4580].plot(color='b')
    weatherDataZH13['difhorrad_Whm2'][4555:4580].plot(color='g')
    

plt.legend(loc=2, fontsize = 7)
plt.xlabel('Hour of the year', fontsize=12)
#plt.ylabel('Wh per m2', fontsize=12)


"""


#
#
#
#x,y = [],[]
#
#x.append(weatherDataZH13['dirnorrad_Whm2'])
#y.append(weatherDataZH13['difhorrad_Whm2'])
#
#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.plot(y,x,'o-')
#
#plt.legend(loc='best')
#plt.xlabel('direct normal radiation', fontsize=18)
#plt.ylabel('diffuse horizontal radiation', fontsize=16)
#
#plt.show()

