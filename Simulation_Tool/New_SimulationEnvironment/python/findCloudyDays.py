# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 15:35:22 2016

@author: Mauro
"""

import os, sys
import matplotlib.pyplot as plt
import pandas as pd
import math

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



fig = plt.figure() 
fig.suptitle('Diffuse and Direct Radiation 4250:4400', fontsize=16)
        
with pd.plot_params.use('x_compat', True):
    weatherDataZH13['dirnorrad_Whm2'][4250:4400].plot(color='r')
    weatherDataZH13['difhorrad_Whm2'][4250:4400].plot(color='g')
    weatherDataZH13['glohorrad_Whm2'][4250:4400].plot(color='b')

plt.legend(loc='best')
plt.xlabel('Hour of the year', fontsize=16)
plt.ylabel('Wh per m2', fontsize=16)




fig = plt.figure() 
fig.suptitle('Diffuse and Direct Radiation 4400:4500', fontsize=16)
        
with pd.plot_params.use('x_compat', True):
    weatherDataZH13['dirnorrad_Whm2'][4400:4500].plot(color='r')
    weatherDataZH13['difhorrad_Whm2'][4400:4500].plot(color='g')
    weatherDataZH13['glohorrad_Whm2'][4400:4500].plot(color='b')


plt.legend(loc='best')
plt.xlabel('Hour of the year', fontsize=16)
plt.ylabel('Wh per m2', fontsize=16)


fig = plt.figure() 
fig.suptitle('Diffuse and Direct Radiation 4500:4600', fontsize=16)
        
with pd.plot_params.use('x_compat', True):
    weatherDataZH13['dirnorrad_Whm2'][4500:4600].plot(color='r')
    weatherDataZH13['difhorrad_Whm2'][4500:4600].plot(color='g')
    weatherDataZH13['glohorrad_Whm2'][4500:4600].plot(color='b')

#plt.legend(loc='best')
plt.xlabel('Hour of the year', fontsize=16)
plt.ylabel('Wh per m2', fontsize=16)





x = []

x.append(weatherDataZH13['dirnorrad_Whm2'][4200:4500])
y = [range(4300,4401)]

fig = plt.figure()
fig.suptitle('Direct Normal Radiation', fontsize=20)
ax = fig.add_subplot(111)
ax.plot(y,x,'o-')

plt.legend(loc='best')
plt.xlabel('Hour of the year', fontsize=18)
plt.ylabel('Wh per m2', fontsize=16)

plt.show()




        





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

