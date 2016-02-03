# -*- coding: utf-8 -*-
"""
Created on Tue Jan 05 14:16:24 2016

Functions to read RadiationResults.csv

@author: Jeremias Schmidli
"""

import csv
import numpy as np

# function to read results for one panel (without looping, might need to be updated)
def import_radiation(path, filename):

    with open(path + filename, 'rb') as f:
        reader = csv.reader(f)
        Radiation_string = list(reader)
    total_radiation = float(Radiation_string[1][0])
    panel_size = float(Radiation_string[3][0])
    for i in range(0,5):
        del Radiation_string[0]
        
    Radiation=[]
    for j in range(0,len(Radiation_string)):
        Radiation.append([])
        
        for k in Radiation_string[j]:
            Radiation[j].append(float(k))
    f.close()
    return (Radiation, total_radiation, panel_size)
        
        
# function to read iterated radiation results
def import_radiation_year(path, filename):

    #open file to read
    with open(path + filename, 'rb') as f:
        reader = csv.reader(f)
        Radiation_string = list(reader)
    
    #save header as list and then delete it
    header = []
    for i in range(0,4):
        header.append(Radiation_string[0])
        del Radiation_string[0]
    
    #save Iteration Number and Radiation Data seperately:
    counter=0
    IterationNumbers = []
    RadiationData = []
    for i in range(0,len(Radiation_string),53):
        for j in range(0,53):
            line = i + j
            
            if j==1:
                IterationNumbers.append(int(Radiation_string[line][0]))
                RadiationData.append([])
            elif j>2:
                RadiationData[counter].append(float(Radiation_string[line][0]))
        counter += 1
        
    #find missing Iterations:
    missingIteration=[]
    numberOfMissingIterations = []
    for i in range(1,len(IterationNumbers)):
        if not IterationNumbers[i]==IterationNumbers[i-1]+1:
            numberMissing = IterationNumbers[i]-IterationNumbers[i-1]-1
            numberOfMissingIterations.append(numberMissing)
            missingIteration.append(IterationNumbers[i]-numberMissing)
            if numberMissing > 1:
                for j in range(1,numberMissing):
                    missingIteration.append(IterationNumbers[i]-numberMissing+j)
            
    #replace missing Iterations with zeros:
    zeroRadiation = [0.0]*50
    for missing in missingIteration:
        RadiationData.insert(missing,zeroRadiation)
                

    f.close()
    return (RadiationData, missingIteration, IterationNumbers, header)
    
# function to read iterated radiation results for average day during month
def import_radiation_monthly(path, filename):

    #open file to read
    with open(path + filename, 'rb') as f:
        reader = csv.reader(f)
        Radiation_string = list(reader)
    
    #save header as list and then delete it
    header = []
    for i in range(0,4):
        header.append(Radiation_string[0])
        del Radiation_string[0]
    
    #save Iteration Number and Radiation Data seperately:
    counter=0
    IterationNumbers = []
    RadiationData = []
    for i in range(0,len(Radiation_string),53):
        for j in range(0,53):
            line = i + j
            
            if j==1:
                IterationNumbers.append(int(Radiation_string[line][0]))
                RadiationData.append([])
            elif j>2:
                RadiationData[counter].append(float(Radiation_string[line][0]))
        counter += 1
        
    #find missing Iterations:
    missingIteration=[]
    numberOfMissingIterations = []
    for i in range(1,len(IterationNumbers)):
        if not IterationNumbers[i]==IterationNumbers[i-1]+1:
            numberMissing = IterationNumbers[i]-IterationNumbers[i-1]-1
            numberOfMissingIterations.append(numberMissing)
            missingIteration.append(IterationNumbers[i]-numberMissing)
            if numberMissing > 1:
                for j in range(1,numberMissing):
                    missingIteration.append(IterationNumbers[i]-numberMissing+j)
            
    #replace missing Iterations with zeros:
    zeroRadiation = [0.0]*50
    for missing in missingIteration:
        RadiationData.insert(missing,zeroRadiation)
                

    f.close()
    return (RadiationData, missingIteration, IterationNumbers, header)
    
def import_radiation_week(path, filename):

    #open file to read
    with open(path + filename, 'rb') as f:
        reader = csv.reader(f)
        Radiation_string = list(reader)
    
    #save header as list and then delete it
    header = []
    for i in range(0,4):
        header.append(Radiation_string[0])
        del Radiation_string[0]
    
    #save Iteration Number and Radiation Data seperately:
    counter=0
    IterationNumbers = []
    RadiationData = []
    for i in range(0,len(Radiation_string),53):
        for j in range(0,53):
            line = i + j
            
            if j==1:
                IterationNumbers.append(int(Radiation_string[line][0]))
                RadiationData.append([])
            elif j>2:
                RadiationData[counter].append(float(Radiation_string[line][0]))
        counter += 1
        
    #find missing Iterations:
    missingIteration=[]
    numberOfMissingIterations = []
    for i in range(1,len(IterationNumbers)):
        if not IterationNumbers[i]==IterationNumbers[i-1]+1:
            numberMissing = IterationNumbers[i]-IterationNumbers[i-1]-1
            numberOfMissingIterations.append(numberMissing)
            missingIteration.append(IterationNumbers[i]-numberMissing)
            if numberMissing > 1:
                for j in range(1,numberMissing):
                    missingIteration.append(IterationNumbers[i]-numberMissing+j)
            
    #replace missing Iterations with zeros:
    zeroRadiation = [0.0]*50
    for missing in missingIteration:
        RadiationData.insert(missing,zeroRadiation)
                

    f.close()
    return (RadiationData, missingIteration, IterationNumbers, header)
    
def add_hours_without_sun(RadiationData, sunRisen):
    
    Radiation = []
    hoursWithSun = 0
    hoursWithoutSun = 0
    for i in sunRisen:
        if i==0:
            hoursWithoutSun +=1
        elif i==1:
            hoursWithSun +=1
            
    numberOfCombinations = len(RadiationData)/hoursWithSun
    zeroRadiation = [0.0]*50    
    combination=0
    RadiationDataCounter=0
    for i in range(numberOfCombinations):
        for j in range(len(sunRisen)):
            if sunRisen[j]==0:
                Radiation.append(zeroRadiation)
            else:
                Radiation.append(RadiationData[RadiationDataCounter])
                RadiationDataCounter+=1
    
    return Radiation
        
def create_npArray_with_total_Radiation(Radiation,panelSize,numberOfPanels, *arg):
    if arg[0]=='monthly':
        numberOfHours = 288
        numberOfLines = len(Radiation)/numberOfHours
    elif arg[0]=='year':
        numberOfHours=8760
        numberOfLines=len(Radiation)/numberOfHours
    else:
        raise ValueError("additional argument must be defined")
    totRad=[]
#    counter=0
    for i in range(numberOfLines):
        totRad.append([])
        for j in range(numberOfHours):
            totRad[i].append(sum(Radiation[8760*i+j])*(panelSize/1000)**2)
    R=np.array(totRad)
    return R
    
    
        
    
    
    
#path = 'C:/Users/Assistenz/Documents/MT_Jeremias/Simulation_Data/RadiationEvaluation/Radiation_yearly_25_angles_incomplete/'
#filename = 'RadiationResultsForPY.csv'

#RadiationData, missingIteration, IterationNumbers, header = import_radiation_year(path, filename)

#add_hours_without_sun(RadiationData, sunRisen)
