# -*- coding: utf-8 -*-
"""
Created on Tue Jan 05 14:16:24 2016

Function to read .epw file
takes one value for radiation in epw file for every hour which is used as a 
reference on whether there is radiation or not. should probably include more values

@author: Jeremias Schmidli
"""

import csv

def isTheSunRisen(path, filename):

    with open(path + filename, 'rb') as f:
        reader = csv.reader(f)
        yearly_values = list(reader)
    for i in range(0,8):
        del yearly_values[0]
    
    sun_risen = []        
    for i in range(0,len(yearly_values)):
        if yearly_values[i][13]=='0':
            sun_risen.append(0)
        else:
            sun_risen.append(1)
            
    f.close()
    ind=[]
    for i in range(0,len(sun_risen)):
        if sun_risen[i]!=0:
            ind.append(i)
            
    with open(path + filename+'HoursThatSunIsRisen.csv', 'w') as g:
#        csv_writer = csv.writer(g)
#        strInd = str(ind)
#
#        csv_writer.writerow(strInd)
        for i in range(0,len(ind)):
            g.write(str(ind[i]) + '\n')
    g.close()
    return sun_risen, ind
    
path = "C:/Users/Assistenz/ASF_Simulation/WeatherData/"
filename = "CHE_Geneva.067000_IWEC.epw"
(sunRisen, ind) = isTheSunRisen(path, filename)
