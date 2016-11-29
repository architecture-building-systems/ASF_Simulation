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



paths = {}
 # define path of weather file:
paths['weather'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\WeatherData\Zuerich_Kloten_2013.epw' #paths['epw_name']

paths['main'] = os.path.abspath(os.path.dirname(sys.argv[0]))

# define paths of subfolders:
paths['data'] =os.path.join(paths['main'], 'data')
paths['python'] = os.path.join(paths['main'], 'python')
paths['data'] = paths['main'] + '\IlluminanceResults\Data'


# add python_path to system path, so that all files are available:

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
    for hour in range(8,19):

        HOY = calcHOY(month, day, hour)
        z_i[month][hour] = weatherData['glohorillum_lux'][HOY]
        w_i[month][hour] = weatherData['dirnorillum_lux'][HOY]
        

illuGlo = pd.DataFrame(z_i).T
illuDir = pd.DataFrame(w_i).T


#############################


from carpetplotIlluminance import carpetPlotIlluminance


illuGH = np.load(os.path.join(paths['data'], 'IlluminanceGH.npy')).item()
illuWin = np.load(os.path.join(paths['data'], 'IlluminanceWindow.npy')).item()
illuFun  = np.load(os.path.join(paths['data'], 'IlluminanceFunctionRadiation.npy')).item()

RadFun  = np.load(os.path.join(paths['data'], 'RadiationWindow.npy')).item()


illuGH_dict = np.load(os.path.join(paths['data'], 'IlluminanceGHDict.npy')).item()
illuWin_dict  = np.load(os.path.join(paths['data'], 'IlluminanceWindowDict.npy')).item()
illuFun_dict  = np.load(os.path.join(paths['data'], 'IlluminanceFunctionDict.npy')).item()
print '\nData loaded from Folder:'


#for angle in [0,90]:
#    for month in range(1,13):
#        for hour in [17,18]:
#    
#            a = illuFun_dict[angle][month][hour] 
#            illuFun_dict[angle][month][hour] = illuFun_dict[angle][month][hour-9]
#            illuFun_dict[angle][month][hour-9] = a

#illuFun2 = {}
#for x_angle in [0,90]:
#    z = []
#    for monthi in range(1,13):
#        
#        z.append(illuFun_dict[x_angle][monthi][18])
#        z.append(illuFun_dict[x_angle][monthi][17])
#        for HOD in range(8,17):  
#            z.append(illuFun_dict[x_angle][monthi][HOD])
#        
#    z = np.array(z)
#    
#    illuFun2[x_angle]= np.reshape(z,(12,11))
#
#        
#illuFun = illuFun2

GH_df = pd.DataFrame(illuGH_dict)
Win_df = pd.DataFrame(illuWin_dict)
Fun_df = pd.DataFrame(illuFun_dict) 
#
#def df(X):
#    
#    X_0 =  pd.DataFrame(X[0])
#    X_90 =  pd.DataFrame(X[90])
#    
#    return X_0, X_90
#
#
#LB_0, LB_90 = df(X = illuLB_dict)
#Fun_0, Fun_90 = df(X = illuFun_dict)
#Win_0, Win_90 = df(X = illuWin_dict)
#
#
##calculate Mean Bias Error [%]
##postive value, over-prediction of the results
#def MBE(P,O):
#    # P = predicted/simulated values
#    # O = observed/measured values
#    
#    MBE = (P.subtract(O).sum()).sum()/(O.sum()).sum() * 100
#    
#    MBE_2 = (P.subtract(O)).divide(O) * 100
#    
#    return MBE, MBE_2
#
##MBE0,MBE20 = MBE(Fun_0,LB_0)
##MBE90, MBE290 = MBE(Fun_90, LB_90)
##
##print MBE0
##print MBE20
#
#MBE0, MBE20 = MBE(Win_0,LB_0)
#MBE90, MBE290 = MBE(Win_90, LB_90)
##
#print MBE0
#print MBE20
##
##MBE0 = MBE(LB_0,LB_0)
##MBE90 = MBE(LB_90, LB_90)
##
##print MBE0
##print MBE90
#
#



df={}
df[0] = pd.DataFrame(illuGH[0]).T
df[90] = pd.DataFrame(illuGH[90]).T

#df = pd.DataFrame(df)

Rad = {}
IlluWindow = {}
GH = {}
Fun = {}
for x_angle in [0,90]:
    z = []
    d = []
    e = []
    f = []
    for monthi in range(1,13):
        for HOD in range(8,19):  
            z.append(RadFun[x_angle][monthi][HOD])
            d.append(illuWin_dict[x_angle][monthi][HOD])
            e.append(illuGH_dict[x_angle][monthi][HOD])
            f.append(illuFun_dict[x_angle][monthi][HOD-2])
    
    Rad[x_angle]= np.array(z)
    IlluWindow[x_angle] = np.array(d)
    GH[x_angle] = np.array(e)
    Fun[x_angle] = np.array(f)

#Result = abs(IlluWindow[0] - GH[0])/GH[0]


plt.style.use('ggplot')


import numpy as np
import matplotlib.pyplot as plt

fig2 = plt.figure(figsize=(8, 4))

plt.subplot(1,2,1)

x= Fun[0]
y = GH[0]
plt.title('Closed ASF Configuration')
plt.plot(x, y, "ro")
plt.xlabel('Linear Regression Method [Lux]')
plt.ylabel('HoneyBee [Lux]')
#plt.xticks([0,4000,8000,12000])
plt.xticks([0,3000,6000,9000,12000,15000])
plt.yticks([0,3000,6000,9000,12000,15000])

plt.subplot(1,2,2)

x1= Fun[90]
y1 = GH[90]

plt.title('Open ASF Configuration')
plt.plot(x1, y1, "ko")
plt.xlabel('Linear Regression Method [Lux]')
plt.xticks([0,3000,6000,9000,12000,15000])
plt.yticks([0,3000,6000,9000,12000,15000])
#plt.ylabel('HoneyBee [Lux]')
fig2.tight_layout()


fig1 = plt.figure(figsize=(8, 4))
#plt.suptitle('Illuminance Comparison')

plt.subplot(1,2,1)


x= Fun[0]
y = GH[0]
plt.title('Closed ASF Configuration')
plt.plot(x, y, "ro")
plt.xlabel('Linear Regression Method [Lux]')
plt.ylabel('HoneyBee [Lux]')
plt.ylim(0,1500)
plt.xlim(0,1500)
plt.xticks([0,300,600,900,1200,1500])
plt.yticks([0,300,600,900,1200,1500])


plt.subplot(1,2,2)

x1= Fun[90]
y1 = GH[90]

plt.title('Open ASF Configuration')
plt.plot(x1, y1, "ko")
plt.xlabel('Linear Regression Method [Lux]')
plt.ylim(0,1500)
plt.xlim(0,1500)
plt.xticks([0,300,600,900,1200,1500])
plt.yticks([0,300,600,900,1200,1500])
#plt.ylabel('HoneyBee [Lux]')

fig1.tight_layout()

#create Plot if set to True
Plot = True
Save = True


if Plot == True:
    
    z_min = 0
    z_max = 6000 #300
   
    fig = plt.figure(figsize=(16, 8))
    
    plt.style.use('ggplot')    
    
    plt.subplot(2,3,1)
    
    carpetPlotIlluminance(z =illuGH[0], z_min = z_min, z_max= z_max, title = '(a) HoneyBee (closed)')
    plt.ylabel("Hour of the Day",size=14)
    
    plt.subplot(2,3,2)
    carpetPlotIlluminance(z = illuWin[0], z_min = z_min, z_max= z_max, title = "(b) Total Flux Method (closed)")
    
    
    plt.subplot(2,3,3)
    carpetPlotIlluminance(z = illuFun[0], z_min = z_min, z_max= z_max, title = "(c) Linear Regression Method (closed)")
    
    
    plt.subplot(2,3,4)
    carpetPlotIlluminance(z = illuGH[90],  z_min = z_min, z_max= z_max, title = "(d) HoneyBee (open)")
    plt.xlabel("Month of the Year",size=14)
    plt.ylabel("Hour of the Day",size=14)
    
    plt.subplot(2,3,5)
    carpetPlotIlluminance(z = illuWin[90],  z_min = z_min, z_max= z_max, title = "(e) Total Flux Method (open)")
    plt.xlabel("Month of the Year",size=14)
    
    
    plt.subplot(2,3,6)
    carpetPlotIlluminance(z = illuFun[90], z_min = z_min, z_max= z_max, title = "(f) Linear Regression Method (open)")
    plt.xlabel("Month of the Year",size=14)    
    
    
    
    
    #space between the y-axes of the plots
    fig.tight_layout()
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
    
       
    
    GH_df.to_csv(paths['result'] + '\\illuminance_GH.csv')
    Win_df.to_csv(paths['result'] + '\\illuminance_GHWindow.csv')                      
    Fun_df.to_csv(paths['result'] + '\\illuminance_LinearFunction.csv') 
    
    #create folder to save figures as png:
    paths['png'] =paths['result'] + '\\png'
    
    os.makedirs(paths['png'])
    fig.savefig(paths['png'] + '\\figure0' + '.png')
    fig1.savefig(paths['png'] + '\\figure1' + '.png')
    fig2.savefig(paths['png'] + '\\figure2' + '.png')
    
    path = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\PlotMidTerm'
    fig.savefig(path + '\\figure0' + '.pdf')
    fig1.savefig(path + '\\figure1' + '.pdf')
    fig2.savefig(path + '\\figure2' + '.pdf')
        
    
    print '\nResults are saved!'

else:
    pass       
    
print "Program Finished"                

