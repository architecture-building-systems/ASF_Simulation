# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 14:25:32 2016

SunTracking evaluation

@author: Jeremias
"""

import os, sys
import numpy as np
import json


radiation_comb = 'Radiation_Kloten_49comb'
radiation_tracking = 'Radiation_Kloten_tracking'

geoLocation = 'Zuerich-Kloten' # 'MADRID_ESP', 'SINGAPORE_SGP'

pvSizeOption = 0

# create dictionary to write all paths:
paths = {}

# find path of current folder (simulation_environment)
paths['main'] = os.path.dirname(os.path.dirname(sys.argv[0]))

# define paths of subfolders:
paths['data'] = paths['main'] + '\\data'
paths['python'] = paths['main'] + '\\python'
paths['gh'] = paths['main'] + '\\grasshopper'
paths['results'] = paths['main'] + '\\results'

# add python_path to system path, so that all files are available:
sys.path.insert(0, paths['python'] + '\\aux_files')

# define paths of data_folders:
paths['lb_comb'] = os.path.join(( paths['data'] + "\grasshopper\LadyBug"), radiation_comb)
paths['electrical_comb'] = os.path.join(( paths['data'] + "\python\electrical_simulation"), radiation_comb)
paths['lb_tracking'] = os.path.join(( paths['data'] + "\grasshopper\LadyBug"), radiation_tracking)
paths['electrical_tracking'] = os.path.join(( paths['data'] + "\python\electrical_simulation"), radiation_tracking)
paths['geo'] = os.path.join(( paths['data'] + "\geographical_location"), geoLocation)


#load functions used for evaluation:
from prepareData import prepareMonthlyRadiatonData, readLayoutAndCombinations, CalcXYAnglesAndLocation
from plotDataFunctions import VisualizeSunTrackingAngles, pcolorMonths
from createMasks import createLBmask

# load sunTrackingData used for the LadyBug simulation:
with open(paths['geo'] + '\SunTrackingData.json', 'r') as fp:
    SunTrackingData = json.load(fp)
    fp.close()
    


# create dictionary with ladybug simulation settings:
lb_combSettings = {}

# panelsize used for simulation:
lb_combSettings['panelsize'] = readLayoutAndCombinations(paths['lb_comb'])['panelSize']  

# desired grid point size used for simulation:
lb_combSettings['desiredGridPointSize'] = readLayoutAndCombinations(paths['lb_comb'])['desiredGridPointSize']  

# actual grid point size used for simulation:
lb_combSettings['actualGridPointSize'] = lb_combSettings['panelsize']/(round(lb_combSettings['panelsize']/float(lb_combSettings['desiredGridPointSize'])))

# calculate aperturesize according to pvSizeOption:
lb_combSettings['aperturesize'] = int(lb_combSettings['panelsize'] - pvSizeOption*2*lb_combSettings['actualGridPointSize'])

# define path of geographical location:
paths['geo'] = os.path.join(( paths['data'] + "\geographical_location"), geoLocation)

# load sunTrackingData used for the LadyBug simulation:
with open(paths['geo'] + '\SunTrackingData.json', 'r') as fp:
    SunTrackingData = json.load(fp)
    fp.close()
    
# find the number of hours analysed by ladybug:
lb_combSettings['numHoursLB'] = np.shape(SunTrackingData['HOY'])[0]

# find the number of combinations analysed by ladybug:
lb_combSettings['numCombLB'] = len(CalcXYAnglesAndLocation(readLayoutAndCombinations(paths['lb_comb']))['allAngles'][0])

PV_electricity_results_comb = np.load(paths['electrical_comb'] + '\\aperturesize_' + str(lb_combSettings['aperturesize']) + '\PV_electricity_results.npy').item()
PV_detailed_results_comb = np.load(paths['electrical_comb'] + '\\aperturesize_' + str(lb_combSettings['aperturesize']) + '\PV_detailed_results.npy').item()



# create dictionary with ladybug simulation settings:
lb_trackingSettings = {}

# panelsize used for simulation:
lb_trackingSettings['panelsize'] = readLayoutAndCombinations(paths['lb_tracking'])['panelSize']  

# desired grid point size used for simulation:
lb_trackingSettings['desiredGridPointSize'] = readLayoutAndCombinations(paths['lb_tracking'])['desiredGridPointSize']  

# actual grid point size used for simulation:
lb_trackingSettings['actualGridPointSize'] = lb_trackingSettings['panelsize']/(round(lb_trackingSettings['panelsize']/float(lb_trackingSettings['desiredGridPointSize'])))

# calculate aperturesize according to pvSizeOption:
lb_trackingSettings['aperturesize'] = int(lb_trackingSettings['panelsize'] - pvSizeOption*2*lb_trackingSettings['actualGridPointSize'])

# define path of geographical location:
paths['geo'] = os.path.join(( paths['data'] + "\geographical_location"), geoLocation)

# load sunTrackingData used for the LadyBug simulation:
with open(paths['geo'] + '\SunTrackingData.json', 'r') as fp:
    SunTrackingData = json.load(fp)
    fp.close()
    
# find the number of hours analysed by ladybug:
lb_trackingSettings['numHoursLB'] = np.shape(SunTrackingData['HOY'])[0]

# find the number of combinations analysed by ladybug:
lb_trackingSettings['numCombLB'] = len(CalcXYAnglesAndLocation(readLayoutAndCombinations(paths['lb_tracking']))['allAngles'][0])

PV_electricity_results_tracking = np.load(paths['electrical_tracking'] + '\\aperturesize_' + str(lb_trackingSettings['aperturesize']) + '\PV_electricity_results.npy').item()
PV_detailed_results_tracking = np.load(paths['electrical_tracking'] + '\\aperturesize_' + str(lb_trackingSettings['aperturesize']) + '\PV_detailed_results.npy').item()

monthlyData_comb = {}
monthlyData_comb['efficiencies'] = {}

monthlyData_tracking = {}
monthlyData_tracking['efficiencies'] = {}

monthlyData_comb['PV'], monthlyData_comb['R'], monthlyData_comb['efficiencies']['PV'], \
    monthlyData_comb['R_avg'], monthlyData_comb['R_theo'], monthlyData_comb['PV_avg'], monthlyData_comb['PV_eff'] \
    = prepareMonthlyRadiatonData(PV_electricity_results_comb)

monthlyData_tracking['PV'], monthlyData_tracking['R'], monthlyData_tracking['efficiencies']['PV'], \
    monthlyData_tracking['R_avg'], monthlyData_tracking['R_theo'], monthlyData_tracking['PV_avg'], monthlyData_tracking['PV_eff'] \
                                        = prepareMonthlyRadiatonData(PV_electricity_results_tracking)
                                        
                                        
                                        
import matplotlib.pyplot as plt
import numpy as np
#from auxFunctions import calculate_sum_for_index


R_max_ind = np.argmax(monthlyData_comb['R_avg'],axis=0)
R_range = np.asarray(range(len(R_max_ind)))

PV_max_ind = np.argmax(monthlyData_comb['PV_avg'],axis=0)
PV_range = np.asarray(range(len(R_max_ind)))


shading = 1-monthlyData_comb['R_avg'][R_max_ind, range(len(R_max_ind))]/monthlyData_comb['R_theo'][R_max_ind, range(len(R_max_ind))]

where_are_NaNs = np.isnan(shading)
shading[where_are_NaNs] = 0

fig = plt.figure(figsize=(16, 12))
plt.suptitle('Radiation Analysis for average days')
#calculate_sum_for_index(monthly,Hind)
plt.subplot(3,1,1)
plt.plot(monthlyData_comb['R_avg'][R_max_ind, range(len(R_max_ind))], label='average radiation')
plt.plot(monthlyData_comb['R_theo'][R_max_ind, range(len(R_max_ind))], label = 'radiation without shading')
plt.ylabel('Radiation [W/m2]')
plt.legend()

plt.subplot(3,1,2)
plt.plot(monthlyData_comb['R_theo'][R_max_ind, range(len(R_max_ind))] - monthlyData_comb['R_avg'][R_max_ind, range(len(R_max_ind))])
plt.ylabel('Shading [W/m2]')

plt.subplot(3,1,3)
plt.plot(shading*100)
plt.ylabel('Shading [%]')
plt.xlabel('hours')

#fig.tight_layout()


Radiation_difference_perc = (1-(monthlyData_tracking['R_avg']/monthlyData_comb['R_avg'][R_max_ind, R_range]).transpose())*100
where_are_NaNs = np.isnan(Radiation_difference_perc)
Radiation_difference_perc[where_are_NaNs] = 0
# figure to compare sun-tracking radiation to optimized radiation:
fig = plt.figure(figsize=(16, 12))

plt.subplot(3,1,1)
plt.plot(monthlyData_comb['R_avg'][R_max_ind, R_range], label = 'Radiation optimized')
plt.plot(monthlyData_comb['R_avg'][PV_max_ind, R_range], label = 'PV optimized')
plt.plot(monthlyData_tracking['R_avg'].transpose(), label = 'sun tracking')
plt.title('Comparison of Radiation with sun tracking to optimized solution')
plt.ylabel('Average Radiation [W/m2]')
plt.legend()

plt.subplot(3,1,2)
plt.plot((monthlyData_comb['R_avg'][R_max_ind, R_range]-monthlyData_tracking['R_avg']).transpose())
plt.title('Comparison of Radiation with sun tracking to optimized solution')
plt.ylabel('Average Radiation Difference [W/m2]')


plt.subplot(3,1,3)
plt.plot(Radiation_difference_perc)
plt.title('Comparison of Radiation with sun tracking to optimized solution')
plt.ylabel('Average Radiation Difference [%]')

#fig.tight_layout()



PV_difference_perc = (1-(monthlyData_tracking['PV_avg']/monthlyData_comb['PV_avg'][PV_max_ind, PV_range]).transpose())*100
where_are_NaNs = np.isnan(PV_difference_perc)
PV_difference_perc[where_are_NaNs] = 0
# figure to compare sun-tracking pv production to optimized pv production:
fig = plt.figure(figsize=(16, 12))

plt.subplot(3,1,1)
plt.plot(monthlyData_comb['PV_avg'][PV_max_ind, PV_range], label='optimized')
plt.plot(monthlyData_tracking['PV_avg'].transpose(), label = 'sun tracking' )
plt.title('Comparison of PV with sun tracking to optimized solution')
plt.ylabel('Average PV Energy Production [W/m2]')
plt.legend()

plt.subplot(3,1,2)
plt.plot((monthlyData_comb['PV_avg'][PV_max_ind, PV_range]-monthlyData_tracking['PV_avg']).transpose())
plt.title('Comparison of PV with sun tracking to optimized solution')
plt.ylabel('Average PV Production Difference [W/m2]')

plt.subplot(3,1,3)
plt.plot(PV_difference_perc)
plt.title('Comparison of PV with sun tracking to optimized solution')
plt.ylabel('Average PV Difference [%]')



############# for thesis:
fig = plt.figure(figsize=(16, 12))

plt.subplot(3,1,1)
plt.plot(monthlyData_comb['R_avg'][PV_max_ind, range(len(R_max_ind))], label='optimized for PV')
plt.plot(monthlyData_tracking['R_avg'].transpose(), label = 'sun tracking')
plt.plot(monthlyData_comb['R_theo'][R_max_ind, range(len(R_max_ind))], label = 'without shading')
plt.ylabel('Radiation [W/m2]')
plt.title ('Average Radiation on Panels')
plt.legend()

plt.subplot(3,1,2)
plt.plot(monthlyData_comb['PV_avg'][PV_max_ind, PV_range], label='optimized')
plt.plot(monthlyData_tracking['PV_avg'].transpose(), label = 'sun tracking' )
plt.title('Comparison of PV with sun tracking to optimized solution')
plt.ylabel('Average PV Energy Production [W/m2]')
plt.legend()


plt.subplot(3,1,3)
plt.title('PV Efficiencies')
plt.plot(monthlyData_comb['PV_eff'][PV_max_ind, PV_range], label = 'PV efficiency optimized')
plt.plot(monthlyData_tracking['PV_eff'].transpose(), label = 'PV efficiency tracking')
plt.ylabel('Efficiency [%]')
plt.legend()
plt.grid()


#fig.tight_layout()




fig =plt.figure(figsize=(16, 12))
plt.suptitle('Comparison of PV efficiencies with sun tracking to optimized solution')

plt.subplot(2,1,1)
plt.title('PV Efficiencies')
plt.plot(monthlyData_comb['PV_eff'][PV_max_ind, PV_range], label = 'PV efficiency optimized')
plt.plot(monthlyData_tracking['PV_eff'].transpose(), label = 'PV efficiency tracking')
plt.ylabel('Efficiency [%]')
plt.legend()
plt.grid()

fig.tight_layout()

plt.subplot(2,1,2)
plt.plot((monthlyData_comb['PV_eff'][PV_max_ind, PV_range]-monthlyData_tracking['PV_eff']).transpose())
plt.ylabel('Efficiency Difference [%]')
plt.grid()

    
fig = plt.figure(figsize=(16, 12))
plt.suptitle('Sun Tracking Angles')
plt.subplot(2,1,1)
VisualizeSunTrackingAngles(SunTrackingData, 'x')
plt.title('Altitude Angles')

plt.subplot(2,1,2)
VisualizeSunTrackingAngles(SunTrackingData, 'y')
plt.title('Azimuth Angles')


PV_electricity_results_comb['LayoutAndCombinations'] = readLayoutAndCombinations(paths['lb_comb'])
# calculate angles corresponding to the layoutAndCombination file:
monthlyData_comb['angles'] = CalcXYAnglesAndLocation(PV_electricity_results_comb['LayoutAndCombinations'])
monthlyData_comb['LBmask'] = createLBmask(monthlyData_comb['R'])

fig.tight_layout()


fig = plt.figure(figsize=(16, 12))
plt.suptitle('Radiation Optimization')
plt.subplot(2,1,1)
arg = ['max','R_avg', 'x', 'LB', 0, 0]
pcolorMonths(monthlyData_comb, arg)
plt.title('Altitude Angles')
cbar =plt.colorbar(ticks=range(0,len(monthlyData_comb['angles']['x_angles'])))
cbar.ax.set_yticklabels(monthlyData_comb['angles']['x_angles'])

plt.subplot(2,1,2)
arg = ['max','R_avg', 'y', 'LB', 0, 0]
pcolorMonths(monthlyData_comb, arg)
plt.title('Azimuth Angles')
cbar =plt.colorbar(ticks=range(0,len(monthlyData_comb['angles']['y_angles'])))
cbar.ax.set_yticklabels(monthlyData_comb['angles']['y_angles'])

fig.tight_layout()


fig = plt.figure(figsize=(16, 12))
plt.suptitle('PV Optimization')
plt.subplot(2,1,1)
arg = ['max','PV', 'x', 'LB', 0, 0]
pcolorMonths(monthlyData_comb, arg)
plt.title('Altitude Angles')
cbar =plt.colorbar(ticks=range(0,len(monthlyData_comb['angles']['x_angles'])))
cbar.ax.set_yticklabels(monthlyData_comb['angles']['x_angles'])

plt.subplot(2,1,2)
arg = ['max','PV', 'y', 'LB', 0, 0]
pcolorMonths(monthlyData_comb, arg)
plt.title('Azimuth Angles')
cbar =plt.colorbar(ticks=range(0,len(monthlyData_comb['angles']['y_angles'])))
cbar.ax.set_yticklabels(monthlyData_comb['angles']['y_angles'])

fig.tight_layout()
