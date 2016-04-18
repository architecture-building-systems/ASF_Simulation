# -*- coding: utf-8 -*-
"""
Created on Fri Apr 01 11:06:47 2016

Create Sun Masks Functions
@author: Assistenz
"""

import numpy as np

def createDIVAmask(L_month):#, rotation_axis, x_angle_location, y_angle_location, allAngles, *arg):
        
    ind=np.argmin(L_month,axis=0)
    
#    z_min=0
    axis_ind = ind
#    z_max=len(allAngles[0])-1

    dx, dy = 1, 1
    
     # generate 2 2d grids for the x & y bounds
    y, x = np.mgrid[slice(0, 24 + dy, dy),
                    slice(0, 12 + dx, dx)]
    z=[]
    
    for i in range(24):
        z.append([])
        for j in range(12):
            z[i].append(axis_ind[24*j + i])
            
            
    z = np.asarray(z)
    
    z3 = np.empty((24,12))*False
    for i in range(24):
       for j in range(12):
           if np.sum(z[0:i+1,j]) == 0 or np.sum(z[i:-1,j])==0:
               z3[i,j] = False
           else:
               z3[i,j] = True
    
    z3[z3 == 0] = np.nan
    
    sunMask=np.isnan(z3)    
#    
#    axis_ind =[]
#    ind=np.argmax(R_month,axis=0)
#    z2_min=0
#    axis_ind = ind
#    z2_max=len(allAngles[0])-1
#
#    dx, dy = 1, 1
#    
#     # generate 2 2d grids for the x & y bounds
#    y, x = np.mgrid[slice(0, 24 + dy, dy),
#                    slice(0, 12 + dx, dx)]
#    z2=[]
#    for i in range(24):
#        z2.append([])
#        for j in range(12):
#            z2[i].append(axis_ind[24*j + i])
#    z2 = np.asarray(z2)
#
#    
#    #zalwaysDay=np.ones((9,12))
#    zalwaysDay=np.ones((6,12))
#    zDay = z
#    #zDay[range(8,17)]=zalwaysDay
#    zDay[range(8,14)]=zalwaysDay
#    
#    zBool = np.ceil(zDay/100.)
#    z2Bool = np.ceil(z2/100.)
#    
#    zDiff = np.abs(zBool-z2Bool)
#    zBooladd = zBool+z2Bool
#    zBool_tot=(zBooladd-zDiff)/2
#    
##    nanSun=np.ones((24,12))
##    for i in z_tot:
##        if i == 0:
##            i=np.nan
#            
##    ztest = z_tot.astype('float')
##    ztest[ztest == 0] = np.nan
##    ztest[ztest >0] = 1
#    
#    zBool_tot[zBool_tot == 0] = np.nan
#    
#    sunMask=np.isnan(zBool_tot)    
#    #sunMask[:,:] = False
    
    return sunMask
    
def createLBmask(R_month):#, rotation_axis, x_angle_location, y_angle_location, allAngles, *arg):
        
        
    R_max=np.max(R_month,axis=0)
    
    dx, dy = 1, 1
    
    # generate 2 2d grids for the x & y bounds
    y, x = np.mgrid[slice(0, 24 + dy, dy),
                    slice(0, 12 + dx, dx)]
    z=[]
    
    for i in range(24):
        z.append([])
        for j in range(12):
            z[i].append(R_max[24*j + i])
            
            
    z = np.asarray(z)
    
    z3 = np.empty((24,12))*False
    for i in range(24):
       for j in range(12):
           if np.sum(z[0:i+1,j]) == 0 or np.sum(z[i:-1,j])==0:
               z3[i,j] = False
           else:
               z3[i,j] = True
    
    z3[z3 == 0] = np.nan
    
    sunMask=np.isnan(z3)    
        
    return sunMask
#        ########
#    ind=np.argmin(L_month,axis=0)
#    
#    z_min=0
#    axis_ind = ind
#    z_max=len(allAngles[0])-1
#
#    dx, dy = 1, 1
#    
#     # generate 2 2d grids for the x & y bounds
#    y, x = np.mgrid[slice(0, 24 + dy, dy),
#                    slice(0, 12 + dx, dx)]
#    z=[]
#    for i in range(24):
#        z.append([])
#        for j in range(12):
#            z[i].append(axis_ind[24*j + i])
#    z = np.asarray(z)
#    
#    axis_ind =[]
#    ind=np.argmax(R_month,axis=0)
#    z2_min=0
#    axis_ind = ind
#    z2_max=len(allAngles[0])-1
#
#    dx, dy = 1, 1
#    
#     # generate 2 2d grids for the x & y bounds
#    y, x = np.mgrid[slice(0, 24 + dy, dy),
#                    slice(0, 12 + dx, dx)]
#    z2=[]
#    for i in range(24):
#        z2.append([])
#        for j in range(12):
#            z2[i].append(axis_ind[24*j + i])
#    z2 = np.asarray(z2)
#
#    
#    #zalwaysDay=np.ones((9,12))
#    zalwaysDay=np.ones((6,12))
#    zDay = z
#    #zDay[range(8,17)]=zalwaysDay
#    zDay[range(8,14)]=zalwaysDay
#    
#    zBool = np.ceil(zDay/100.)
#    z2Bool = np.ceil(z2/100.)
#    
#    zDiff = np.abs(zBool-z2Bool)
#    zBooladd = zBool+z2Bool
#    zBool_tot=(zBooladd-zDiff)/2
#    
#    nanSun=np.ones((24,12))
#    for i in z_tot:
#        if i == 0:
#            i=np.nan
            
#    ztest = z_tot.astype('float')
#    ztest[ztest == 0] = np.nan
#    ztest[ztest >0] = 1
    
#    zBool_tot[zBool_tot == 0] = np.nan
#    
#    sunMask=np.isnan(zBool_tot)    
#    #sunMask[:,:] = False
#    
#    return sunMask
    
#asdf = createLBmask(L_month, R_month, allAngles)
#asdf2 =createDIVAmask(L_month)
#asdf3 =createLBmask(R_month)
