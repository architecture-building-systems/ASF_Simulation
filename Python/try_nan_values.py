# -*- coding: utf-8 -*-
"""
Created on Wed Feb 03 18:43:02 2016

@author: Assistenz
"""
import numpy as np
import matplotlib.pyplot as plt
#
f = plt.figure()
ax = f.add_subplot(111)
a = np.arange(25).reshape((5,5)).astype(float)
a[3,:] = np.nan
masked_array = np.ma.array (a, mask=mask)#=np.isnan(a))
cmap = plt.cm.afmhot
cmap.set_bad('grey',1.)
ax.imshow(masked_array, interpolation='nearest', cmap=cmap)
f.canvas.draw()
#
#masked_array = np.ma.array (z, mask=np.isnan(z))
#cmap = plt.cm.jet
#cmap.set_bad('w',1.)
#ax.imshow(masked_array, interpolation='nearest', cmap=cmap)
#sunNan = []
for i in range(len(sunRisen)):
    if sunRisen[i] == 0:
        sunNan.append(np.nan)
    else:
        sunNan.append(1)
        
SunAround = []
for i in range(25):
    SunAround.append(np.array(sunNan))
    
SunAround = np.array(SunAround)

def createMonthsNan(L_month, R_month):#, rotation_axis, x_angle_location, y_angle_location, allAngles, *arg):
        
    ind=np.argmin(L_month,axis=0)
    
    z_min=0
    axis_ind = ind
    z_max=len(allAngles[0])-1

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
    
    axis_ind =[]
    ind=np.argmax(R_month,axis=0)
    z2_min=0
    axis_ind = ind
    z2_max=len(allAngles[0])-1

    dx, dy = 1, 1
    
     # generate 2 2d grids for the x & y bounds
    y, x = np.mgrid[slice(0, 24 + dy, dy),
                    slice(0, 12 + dx, dx)]
    z2=[]
    for i in range(24):
        z2.append([])
        for j in range(12):
            z2[i].append(axis_ind[24*j + i])
    z2 = np.asarray(z2)
    
    z_tot=z+z2
    
#    nanSun=np.ones((24,12))
#    for i in z_tot:
#        if i == 0:
#            i=np.nan
            
    ztest = z_tot.astype('float')
    ztest[ztest == 0] = np.nan
    ztest[ztest >0] = 1
    
    sunMask=np.isnan(ztest)    
    
    return sunMask
   
sunMask = createMonthsNan(L_month, R_month)
#   # z_min, z_max = 0, len()
#    #print z_min, z_max
#    
#    #plt.pcolor(x, y, z, cmap='jet', vmin=z_min, vmax=z_max)
#    plt.pcolor(x, y, ztest, cmap=cmap, vmin=z_min, vmax=z_max)
#    #plt.pcolor(x, y, z, cmap='CMRmap', vmin=z_min, vmax=z_max)
#
#    #plt.pcolor(x, y, z, cmap='nipy_spectral', vmin=z_min, vmax=z_max)
#
#    #plt.title('pcolor')
##    plt.xlabel("Day of the Year")
##    plt.ylabel("Hour of the Day")
#    # set the limits of the plot to the limits of the data
#    plt.axis([x.min(), x.max(), y.min(), y.max()])


# # Optimal x-angle combinations for every hour of the year
#figcounter+=1
#fig = plt.figure(num = figcounter, figsize=(16, 12))
#plt.suptitle("Angle Distribution around x-axis", size=16)
#p1 = plt.subplot(2,3,1)
#pcolorMonths(H_month, 'x', x_angle_location, y_angle_location, allAngles)
#plt.title("Heating Demand")
#p1 = plt.subplot(2,3,2)
#pcolorMonths(C_month, 'x', x_angle_location, y_angle_location, allAngles)
#plt.title("Cooling Demand")
#p1 = plt.subplot(2,3,3)
#pcolorMonths(L_month, 'x', x_angle_location, y_angle_location, allAngles)
#plt.title("Lighting Demand")
#p1 = plt.subplot(2,3,4)
#pcolorMonths(R_month, 'x', x_angle_location, y_angle_location, allAngles, 'max')
#plt.title("PV Electricity Production")
#p1 = plt.subplot(2,3,5)
#pcolorMonths(E_month, 'x', x_angle_location, y_angle_location, allAngles)
#plt.title("Total Thermal/Lighting Demand")
#p1 = plt.subplot(2,3,6)
#pcolorMonths(E_month_withPV, 'x', x_angle_location, y_angle_location, allAngles)
#plt.title("Net Demand with PV")
#fig.subplots_adjust(right=0.8)
#cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(x_angles)))
#cbar.ax.set_yticklabels(x_angles)
#plt.show()   
#
## Energy Use at opmtimum angle combination for the hole year:
#figcounter+=1
#fig = plt.figure(num = figcounter, figsize=(16, 12))
#plt.suptitle("Energy Use at optimum angle combination", size=16)
#plt.subplot(2,2,1)
#pcolorEnergyDays(SunAround)
#plt.title("Heating Demand")
#plt.subplot(2,2,2)
#pcolorEnergyDays(C)
#plt.title("Cooling Demand")
#plt.subplot(2,2,3)
#pcolorEnergyDays(L)
#plt.title("Lighting Demand")
#plt.subplot(2,2,4)
#pcolorEnergyDays(E)
#plt.title("Total Energy Demand")
#fig.subplots_adjust(right=0.8)
#cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#cbar = plt.colorbar(cax=cbar_ax, ticks=np.asarray(range(0,int(E_month.max()*10)))/10.)
#cbar.set_label('Power Use in kWh', rotation=270, labelpad=20)
#plt.show()