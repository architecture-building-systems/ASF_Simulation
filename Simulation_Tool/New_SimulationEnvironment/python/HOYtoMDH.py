# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 15:13:44 2016

@author: Assistenz
"""

import numpy as np
import sys
from calculateHOY import calcHOY 



HOY = 755

print HOY
#print (HOY)
#hour = 24  #hour of the day (i.e between 0:00 and 1:00 corresponds to value 1)
#HOY = 1
#HOY = 8760

#hour 0 represents the hour 23 to 24 at this day

def HOYtoMonthDayHour(HOY):
    
    if HOY == 0:
        print HOY, 'does not exist, choose 1 instead'
        sys.exit()
    
    elif HOY > 8760:
        print HOY, 'exceeded possible range of hours per year, try again'
        sys.exit()
    #calculate the month, day and hour from given hour of the year
    #daysPerMonth = np.array([31,28,31,30,31,30,31,31,30,31,30,31])
                         
    # sum of passed days for each month in year
    sumDays = {1:0 , 2: 31, 3: 59, 4: 90, 5: 120, 6: 151, 7: 181, 8: 212, 9: 243, 10: 273, 11: 304, 12: 334}#, 12: 365}
    
    #calculate the number of days
    H = HOY /24.
        
    if H <= sumDays[2]:
        month = 1
    elif H > sumDays[12]:
        month = 12
    else:
        for ii in range(2,12):
            if H > sumDays[ii] and H <= sumDays[ii+1]:
                month = ii
                break
            else:
                pass
    
    #calculate the corresponding day    
    day = int(H-sumDays[month])
    
    #calculate the corresponding hour
    hour = int(24*(H - sumDays[month] - day))
    
    if hour == 0:
        hour = 24
        day -= 1        
        
    day += 1
    
    print month,day, hour
    return month, day, hour

month, day, hour = HOYtoMonthDayHour(HOY = HOY)

HOY2= calcHOY(month,day,hour)
#HOY3= calcHOY(7,4,24)

#print HOY2
print HOY2