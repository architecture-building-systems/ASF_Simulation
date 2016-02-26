# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 15:28:16 2016

plot total radiation on panels for average/specific day 

@author: Jeremias
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# import days per month
path = "C:/Users/Assistenz/ASF_Simulation/Python/"
filename = "days_per_month.csv"
daysPerMonth=np.genfromtxt(path + filename, delimiter=',')
daysPerMonth=np.asarray(daysPerMonth, dtype='int32')

m2Flag = False


path = "C:/Users/Assistenz/Documents/MT_Jeremias/Simulation_Data/RadiationEvaluation/dailyTotalRadiation/"

if m2Flag:
    path = "C:/Users/Assistenz/Documents/MT_Jeremias/Simulation_Data/RadiationEvaluation/dailyTotalRadiation_1m2/"
    
#Import data from csv
DailyTotRad=np.genfromtxt(path + 'TotalRadiation_deleteDouble.csv',delimiter=',')

#startHour = int(min(DailyTotRad[:,0]))
#endHour = int(max(DailyTotRad[:,0]))
numberOfComb = int(max(DailyTotRad[:,1]+1))
if m2Flag:
    numberOfComb = 1
numberOfHours = 24
#numberOfTestSizes = 5



## create custum colormap:
#cdict1 = {'red':   ((0.0, 0.0, 0.0),
#                   (0.5, 0.0, 0.1),
#                   (1.0, 1.0, 1.0)),
#
#         'green': ((0.0, 0.0, 0.0),
#                   (1.0, 0.0, 0.0)),
#
#         'blue':  ((0.0, 0.0, 1.0),
#                   (0.5, 0.1, 0.0),
#                   (1.0, 0.0, 0.0))
#        }
#
#blue_red1 = LinearSegmentedColormap('BlueRed1', cdict1)

Radiation_days = [[],[],[],[]]
Radiation_day = []
Hcounter=0
for h in range(len(Radiation_days)):
    Radiation_day = []
    for i in range(numberOfHours):
                
        for j in range(numberOfComb):
            if i == 0:
                Radiation_day.append([])
            print (h*numberOfHours+i)*numberOfComb +j
            Radiation_day[j].append(DailyTotRad[(h*numberOfHours+i)*numberOfComb +j][3])
#            Hcounter+=1
    Radiation_days[h]=np.array(Radiation_day)
    
            
#            for k in range(numberOfTestSizes):
#                Radiation_days[i][j].append(DailyTotRad[i*numberOfComb*numberOfTestSizes+j*numberOfTestSizes +k][3])
#            Radiation_days[i][j].append(DailyTotRadSmall[i*numberOfComb+j][3])

R_specific = []
for i in range(16):
    R_specific.append([])
    for j in range(9):
        R_specific[i].append(gridConvergenceRad[i][j][5])
R_specific = np.array(R_specific).T
R_specific_day = np.zeros((9,24))
R_specific_day[:,5:21] = R_specific

def radiation_average_day(R_monthly,month,combination, daysPerMonth):
   
    Rind = np.argmax(R_monthly,axis=0)
    R_day = R_monthly[:,range(24*(month-1),24*month)]
    Rind_day = Rind[range(24*(month-1),24*month)]
    
    R_plot = []
    if combination == 'optimal':
        for i in range(np.shape(R_day)[1]):
            R_plot.append(R_day[Rind_day[i]][i])
        R_plot=np.array(R_plot)/daysPerMonth[month-1]
    else:
        R_plot=np.array(R_day[combination])/daysPerMonth[month-1]
    
    return R_plot

def radiation_specific_day(Rad,combination):
     
    Rind = np.argmax(Rad,axis=0)
#    R_day = Rad[:,range(24*(month-1),24*month)]
#    Rind_day = Rind[range(24*(month-1),24*month)]
    
    R_plot = []
    if combination == 'optimal':
        for i in range(np.shape(Rad)[1]):
            R_plot.append(Rad[Rind[i]][i])
        R_plot=np.array(R_plot)
    else:
        R_plot=np.array(Rad[combination])
    
    return R_plot
    

# plot radiation for an average day:
month = 10

fig = plt.figure(figsize=(16, 12))
plt.suptitle('Average Radiation on Panels', size = 16)
plt.subplot(2,2,1)
month = 3
plt.title('Average Radiation on Panels for Month ' + np.str(month), size = 14)
R_plot = radiation_average_day(R_monthly,month,'optimal', daysPerMonth)

plt.plot(range(24),R_plot, label='optimal angle')

for i in range(5):
    R_plot = radiation_average_day(R_monthly,month,i*5+2, daysPerMonth)
    plt.plot(range(24),R_plot, label='combination: ' + np.str(i*5+2))

plt.xlabel('hour of the day')
plt.ylabel('Average Radiation [kWh]')
plt.legend()

plt.subplot(2,2,2)
month = 6
plt.title('Average Radiation on Panels for Month ' + np.str(month), size = 14)
R_plot = radiation_average_day(R_monthly,month,'optimal', daysPerMonth)

plt.plot(range(24),R_plot, label='optimal angle')

for i in range(5):
    R_plot = radiation_average_day(R_monthly,month,i*5+2, daysPerMonth)
    plt.plot(range(24),R_plot, label='combination: ' + np.str(i*5+2))

plt.xlabel('hour of the day')
plt.ylabel('Average Radiation [kWh]')
plt.legend()

plt.subplot(2,2,3)
month = 9
plt.title('Average Radiation on Panels for Month ' + np.str(month), size = 14)
R_plot = radiation_average_day(R_monthly,month,'optimal', daysPerMonth)

plt.plot(range(24),R_plot, label='optimal angle')

for i in range(5):
    R_plot = radiation_average_day(R_monthly,month,i*5+2, daysPerMonth)
    plt.plot(range(24),R_plot, label='combination: ' + np.str(i*5+2))

plt.xlabel('hour of the day')
plt.ylabel('Average Radiation [kWh]')
plt.legend()

plt.subplot(2,2,4)
month = 12
plt.title('Average Radiation on Panels for Month ' + np.str(month), size = 14)
R_plot = radiation_average_day(R_monthly,month,'optimal', daysPerMonth)

plt.plot(range(24),R_plot, label='optimal angle')

for i in range(5):
    R_plot = radiation_average_day(R_monthly,month,i*5+2, daysPerMonth)
    plt.plot(range(24),R_plot, label='combination: ' + np.str(i*5+2))

plt.xlabel('hour of the day')
plt.ylabel('Average Radiation [kWh]')
plt.legend()
plt.show()


# plot radiation for a specific day (july 1st for now)

R_specific = []
for i in range(16):
    R_specific.append([])
    for j in range(9):
        R_specific[i].append(gridConvergenceRad[i][j][5])
R_specific = np.array(R_specific).T
R_specific_day = np.zeros((9,24))
R_specific_day[:,5:21] = R_specific
        

fig = plt.figure(figsize=(16, 12))
plt.suptitle('Total Radiation on Panels for July 1st', size = 16)

R_plot = radiation_specific_day(R_specific_day,'optimal')

plt.plot(range(24),R_plot, label='optimal angle')

for i in range(9):
    R_plot = radiation_specific_day(R_specific_day,i)
    plt.plot(range(24),R_plot, label='combination: ' + np.str(i))



fig = plt.figure(figsize=(16, 12))
plt.suptitle('Total Radiation on Panels', size = 16)
titles = ['March 11', 'June 11', 'September 4', 'December 31']
for i in range(4):
    plt.subplot(2,2,i+1)
    R_plot = radiation_specific_day(Radiation_days[i],'optimal')
    plt.plot(range(24),R_plot, label='optimal angle')
    
    for j in range(numberOfComb):
        R_plot = radiation_specific_day(Radiation_days[i],j)
        plt.plot(range(24),R_plot, label='combination: ' + np.str(j))

    plt.title(titles[i], size = 14)
    plt.xlabel('hour of the day', size =14)
    plt.ylabel('Total Radiation [kWh]', size=14)
    plt.legend()

plt.show()