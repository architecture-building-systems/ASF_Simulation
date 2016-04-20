# -*- coding: utf-8 -*-
"""
Created on Fri Apr 01 11:06:47 2016

Create Sun Masks Functions

@author: Jeremias
"""

import numpy as np

def createDIVAmask(L_month):
    """
    function that creates a mask for the monthly data achieved by DIVA
    """
    
    # find minimum index of lighting data:
    axis_ind=np.argmin(L_month,axis=0)

    # set step size:
    dx, dy = 1, 1
    
    # generate 2 2d grids for the x & y bounds
    y, x = np.mgrid[slice(0, 24 + dy, dy),
                    slice(0, 12 + dx, dx)]
                    
    # create empty list for indices
    z=[]
    
    # fill list with corresponding indices:
    for i in range(24):
        z.append([])
        for j in range(12):
            z[i].append(axis_ind[24*j + i])
            
    # convert list to np.array
    z = np.asarray(z)
    
    # create array for carpet plots (The False may be confusing, can be ignored):
    z3 = np.empty((24,12))*False
    
    # set values to True which correspond to hours without sun (actualy it is set to 1)
    # and the hours with sun to 0 (False)
    for i in range(24):
       for j in range(12):
           if np.sum(z[0:i+1,j]) == 0 or np.sum(z[i:-1,j])==0:
               z3[i,j] = False
           else:
               z3[i,j] = True
    
    # set values to nan wihich are zero:
    z3[z3 == 0] = np.nan
    
    # create sun mask where True corresponds to no sun
    sunMask=np.isnan(z3)    
    
    return sunMask
    
def createLBmask(R_month):
    """
    function that creates a mask for the monthly data achieved by LadyBug
    """
    
    # find maximum index of lighting data:
    R_max=np.max(R_month,axis=0)
    
    # set step size:
    dx, dy = 1, 1
    
    # generate 2 2d grids for the x & y bounds
    y, x = np.mgrid[slice(0, 24 + dy, dy),
                    slice(0, 12 + dx, dx)]
    
    # create empty list for indices:
    z=[]
    
    # fill list with corresponding indices
    for i in range(24):
        z.append([])
        for j in range(12):
            z[i].append(R_max[24*j + i])
            
    # convert list to np.array
    z = np.asarray(z)
    
    # create array for carpet plots (False can be ignored)
    z3 = np.empty((24,12))*False
    
    # set values to True which correspond to hours without sun (actualy it is set to 1)
    # and the hours with sun to 0 (False)
    for i in range(24):
       for j in range(12):
           if np.sum(z[0:i+1,j]) == 0 or np.sum(z[i:-1,j])==0:
               z3[i,j] = False
           else:
               z3[i,j] = True
               
    # set values to nan wihich are zero:
    z3[z3 == 0] = np.nan
    
    # create sun mask where True corresponds to no sun
    sunMask=np.isnan(z3)    
        
    return sunMask

    
#asdf = createLBmask(L_month, R_month, allAngles)
#asdf2 =createDIVAmask(L_month)
#asdf3 =createLBmask(R_month)
