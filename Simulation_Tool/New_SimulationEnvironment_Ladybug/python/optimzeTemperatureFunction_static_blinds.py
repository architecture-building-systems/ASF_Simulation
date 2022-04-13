# -*- coding: utf-8 -*-
"""
Created on Wed Nov 09 18:55:35 2016

@author: Mauro
"""
#Tmax = 26
#Tmin = 20
#
#DataTemp = {0: 18.59}

def optimzeTemp(DataTemp, Tmax, Tmin):
    
    Tavg = (Tmax + Tmin)/2.    
    difference = {}

    data_length = [hh for hh in DataTemp]
    data_length.sort()

    for ii in data_length:
        
        difference[ii] = abs(Tavg-DataTemp[ii])
    
    BestTempComb = min(difference, key=lambda ii:difference[ii]) 
            
    return BestTempComb
    
#Key = optimzeTemp(DataTemp,Tmax, Tmin)


def checkEqual(Data):

    equal = None    
    data_length = [hh for hh in Data]
    data_length.sort()

    for ii in data_length:
        for jj in data_length:
            if Data[ii] != Data[jj]:
                equal = False
                break                
            else:
                equal = True
    
    return equal
    
    
#equal = checkEqual(DataTemp)
    
                