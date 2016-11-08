# -*- coding: utf-8 -*-
"""
Created on Thu Nov 03 15:27:04 2016

@author: Mauro

Main file to evaluate different illuminance methods
"""

import matplotlib.pyplot as plt
import sys,os
import pandas as pd
import numpy as np
import time

now = time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())

#create Plot if set to True
Plot = True
Save = True

paths = {}
 # define path of weather file:
paths['weather'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\WeatherData\Zuerich_Kloten_2013.epw' #paths['epw_name']

paths['main'] = os.path.abspath(os.path.dirname(sys.argv[0]))

# define paths of subfolders:
paths['data'] =os.path.join(paths['main'], 'data')
paths['python'] = os.path.join(paths['main'], 'python')


# add python_path to system path, so that all files are available:
sys.path.insert(0, paths['python'] + '\\aux_files')
sys.path.insert(0, paths['python'])
sys.path.insert(0, paths['main'])
############################

from epwreader import epw_reader
#read epw file of needed destination
weatherData = epw_reader(paths['weather'])


glbIll = weatherData['glohorillum_lux']

from calculateHOY import calcHOY

day = 15

z_i = {}
w_i = {}

for month in range(1,13):
    z_i[month] = {}
    w_i[month] = {}
    for hour in [8,10,12,14,16,18]:

        HOY = calcHOY(month, day, hour)
        z_i[month][hour] = weatherData['glohorillum_lux'][HOY]
        w_i[month][hour] = weatherData['dirnorillum_lux'][HOY]
        

illuGlo = pd.DataFrame(z_i).T
illuDir = pd.DataFrame(w_i).T


#############################


from carpetplotIlluminance import carpetPlotIlluminance

from IlluminanceWindow import IlluminanceWindow
from IlluminanceFunction import IlluminanceFunction
from IlluminanceCalculationAnalysis import IlluminanceCalculationAnalysis



illuLB, illuLB_dict = IlluminanceCalculationAnalysis()
illuWin, illuWin_dict = IlluminanceWindow()
illuFun, illuFun_dict, RadiationData = IlluminanceFunction()


LB_df = pd.DataFrame(illuLB_dict)
Win_df = pd.DataFrame(illuWin_dict)
Fun_df = pd.DataFrame(illuFun_dict) 

def df(X):
    
    X_0 =  pd.DataFrame(X[0])
    X_90 =  pd.DataFrame(X[90])
    
    return X_0, X_90


LB_0, LB_90 = df(X = illuLB_dict)
Fun_0, Fun_90 = df(X = illuFun_dict)
Win_0, Win_90 = df(X = illuWin_dict)


#calculate Mean Bias Error [%]
#postive value, over-prediction of the results
def MBE(P,O):
    # P = predicted/simulated values
    # O = observed/measured values
    
    MBE = (P.subtract(O).sum()).sum()/(O.sum()).sum() * 100
    
    MBE_2 = (P.subtract(O)).divide(O) * 100
    
    return MBE, MBE_2

#MBE0,MBE20 = MBE(Fun_0,LB_0)
#MBE90, MBE290 = MBE(Fun_90, LB_90)
#
#print MBE0
#print MBE20

MBE0, MBE20 = MBE(Win_0,LB_0)
MBE90, MBE290 = MBE(Win_90, LB_90)
#
print MBE0
print MBE20
#
#MBE0 = MBE(LB_0,LB_0)
#MBE90 = MBE(LB_90, LB_90)
#
#print MBE0
#print MBE90






if Plot == True:
    
    z_min = 0.0
    z_max = 300.0
   
    fig = plt.figure(figsize=(16, 8))
    
    plt.subplot(2,3,1)
    carpetPlotIlluminance(z =illuLB[0], z_min = z_min, z_max= z_max, title = '(a) Calculation with LadyBug (closed)')
    plt.ylabel("Hour of the Day",size=14)
    
    plt.subplot(2,3,2)
    carpetPlotIlluminance(z = illuWin[0], z_min = z_min, z_max= z_max, title = "(b) Total Flux Method (closed)")
    
    
    plt.subplot(2,3,3)
    carpetPlotIlluminance(z = illuFun[0], z_min = z_min, z_max= z_max, title = "(c) Linear Regression Method (closed)")
    
    
    plt.subplot(2,3,4)
    carpetPlotIlluminance(z = illuLB[90],  z_min = z_min, z_max= z_max, title = "(d) Calculation with LadyBug (open)")
    plt.xlabel("Month of the Year",size=14)
    plt.ylabel("Hour of the Day",size=14)
    
    plt.subplot(2,3,5)
    carpetPlotIlluminance(z = illuWin[90],  z_min = z_min, z_max= z_max, title = "(e) Total Flux Method (open)")
    plt.xlabel("Month of the Year",size=14)
    
    
    plt.subplot(2,3,6)
    carpetPlotIlluminance(z = illuFun[90], z_min = z_min, z_max= z_max, title = "(f) Linear Regression Method (open)")
    plt.xlabel("Month of the Year",size=14)    
    
    
    
    
    #space between the y-axes of the plots
    #fig.tight_layout()
    fig.subplots_adjust(right = 0.8)
    
    #setting for the legend
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    cbar = plt.colorbar(cax=cbar_ax)
    cbar.solids.set_rasterized(True) 
    cbart = plt.title("Illuminance [Lux]", fontsize=14)
    cbart.set_position((1.1,1.02))
    #        cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(allAngles[0])))
        #cbar.ax.set_yticklabels(AnglesString)
    cbar.ax.tick_params(labelsize=14)
    
    plt.show()
else:
    pass    

if Save == True and Plot == True:
    
    paths['result']= os.path.join('C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\IlluminanceResults', 'Results_Illuminance_' + now)

    
    os.makedirs(paths['result'])
    
       
    
    LB_df.to_csv(paths['result'] + '\\illuminance_LadyBug.csv')
    Win_df.to_csv(paths['result'] + '\\illuminance_LadyBugWindow.csv')                      
    Fun_df.to_csv(paths['result'] + '\\illuminance_LinearFunction.csv') 
    
    #create folder to save figures as png:
    paths['png'] =paths['result'] + '\\png'
    
    os.makedirs(paths['png'])
    fig.savefig(paths['png'] + '\\figure0' + '.png')
    
    print '\nResults are saved!'

else:
    pass       
    
print "Program Finished"                

