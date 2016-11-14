# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 15:13:44 2016

@author: Assistenz
"""

import numpy as np

from calculateHOY import calcHOY 

HOY2= calcHOY(7,10,1)
HOY3= calcHOY(7,10,24)

print HOY2
print HOY3

HOY = 5000

#hour = 24  #hour of the day (i.e between 0:00 and 1:00 corresponds to value 1)
#HOY = 1
#HOY = 8760

#hour 0 represents the hour 23 to 24 at this day

def HOYtoMonthDayHour(HOY):
    
    from hourRadiation import sumHours    
    #calculate the month, day and hour from given hour of the year
    daysPerMonth = np.array([31,28,31,30,31,30,31,31,30,31,30,31])
                 
    sumHours = sumHours(daysPerMonth)  
    sumHours = [0, 744. , 1416. , 2160. , 2880. , 3624. , 4344. , 5088. , 5832. , 6552. , 7296. , 8016. , 8760.]
    
    sumDays = {}    
    sumDays = {1: 31, 2: 59, 3: 90, 4: 120, 5: 151, 6: 181, 7: 212, 8: 243, 9: 273, 10: 304, 11: 334, 12: 365}
    
    for ii in range(1,13):
        if ii == 1:
            sumDays[ii] =daysPerMonth[0]
        else:
            sumDays[ii] = sumDays[ii-1] + daysPerMonth[ii-1]
     
       
    print sumHours
    print sumDays
    
    
    
    if HOY <= sumHours[1]:
        month = 1
    
    elif HOY > sumHours[1] and HOY < sumHours[11]:
        for ii in range(1,11):
            if HOY > sumHours[ii] and HOY < sumHours[ii+1]:
                month = ii-1
                break
    else:
        month = 12


    print HOY
    print sumHours[5]
    
    day = int((HOY-sumHours[month])/24.)
    
    hour = int((HOY- (sumHours[month] + (day)*24))) 
    
    
    
    return month, day, hour

month, day, hour = HOYtoMonthDayHour(HOY = HOY)
