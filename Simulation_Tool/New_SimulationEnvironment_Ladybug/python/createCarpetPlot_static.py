# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 09:44:38 2016

@author: Mauro
"""

import matplotlib.pyplot as plt
import numpy as np

from carpetPlot import carpetPlot, carpetPlotMask

def createCarpetPlot (monthlyData, roomFloorArea, H, C, E, E_HCL):
    
    z_max = max(monthlyData[E])/roomFloorArea
    z_min = min(monthlyData['PV'])/roomFloorArea
    
    print 'z_min', z_min
    
    if z_min > 0.25:
        z_min = -0.25

    """z_min = -0.30
    z_max = 0.4
    """
    z_min = -0.40
    z_max = 0.8
   
    fig = plt.figure(figsize=(16, 8))
    #    plt.suptitle("Optimum Altitude and Azimuth Orientation", size=16)
    plt.subplot(2,3,1)
    carpetPlot(X = monthlyData[H], z_min = z_min, z_max= z_max, title = '(a) Heating Demand', roomFloorArea = roomFloorArea)
    plt.ylabel("Hour of the Day",size=16)
    
    plt.subplot(2,3,2)
    carpetPlot(X = monthlyData[C], z_min = z_min, z_max= z_max, title = '(b) Cooling Demand', roomFloorArea = roomFloorArea)
    
    plt.subplot(2,3,3)
    carpetPlot(X = monthlyData['L'], z_min = z_min, z_max= z_max, title = '(c) Lighting Demand', roomFloorArea = roomFloorArea)
    
    plt.subplot(2,3,4)
    carpetPlot(X = monthlyData['PV'], z_min = z_min, z_max= z_max, title = '(d) PV Supply', roomFloorArea = roomFloorArea)
    plt.xlabel("Month of the Year",size=16)
    plt.ylabel("Hour of the Day",size=16)
    
    plt.subplot(2,3,5)
    carpetPlot(X = monthlyData[E_HCL], z_min = z_min, z_max= z_max, title = '(e) Building Demand', roomFloorArea = roomFloorArea)
    plt.xlabel("Month of the Year",size=16)    
    
    plt.subplot(2,3,6)   
    carpetPlot(X = monthlyData[E], z_min = z_min, z_max= z_max, title = 'Net Energy Demand', roomFloorArea = roomFloorArea)
    plt.xlabel("Month of the Year",size=16)


    #space between the y-axes of the plots
    fig.tight_layout()
    fig.subplots_adjust(right = 0.8)
    
    #setting for the legend
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    tick = np.arange(z_min, z_max, 0.2)
    cbar = plt.colorbar(cax=cbar_ax, ticks = tick) #[0.4,0.3,0.2,0.1,0.0,-0.1,-0.2,-0.3])
    cbar.solids.set_rasterized(True) 
    cbart = plt.title("Net Energy [kWh/m2]", fontsize=14)
    cbart.set_position((1.1,1.02))
    cbar.ax.tick_params(labelsize=14)
    
    #plt.tight_layout()
    plt.show()       
    
                
    return fig


def createCarpetPlotXAngles(x_angle_array, hour_in_month, H, C, E, E_HCL):  
   
    fig = plt.figure(figsize=(16, 8))
    #    plt.suptitle("Optimum Altitude and Azimuth Orientation", size=16)
    plt.subplot(2,3,1)
    carpetPlotMask(X = x_angle_array[H], z_min = 0, z_max= 90, title = '(a) Heating Optimization', hour_in_month = hour_in_month)
    plt.ylabel("Hour of the Day",size=16)
    
    plt.subplot(2,3,2)
    carpetPlotMask(X = x_angle_array[C], z_min = 0, z_max= 90, title = '(b) Cooling Optimization', hour_in_month = hour_in_month)
    
    plt.subplot(2,3,3)
    carpetPlotMask(X = x_angle_array['Lighting'], z_min = 0, z_max= 90, title = '(c) Lighting Optimization', hour_in_month = hour_in_month)
    
    #plt.subplot(2,3,4)
    #carpetPlotMask(X = x_angle_array['SolarEnergy'], z_min = 0, z_max= 90, title = '(d) PV Supply Optimization', hour_in_month = hour_in_month)
    #plt.xlabel("Month of the Year",size=16)
    #plt.ylabel("Hour of the Day",size=16)
    
    plt.subplot(2,3,5)
    carpetPlotMask(X = x_angle_array[E_HCL], z_min = 0, z_max= 90, title = '(e) Building Demand Optimization', hour_in_month = hour_in_month)
    plt.xlabel("Month of the Year",size=16)    
    
    plt.subplot(2,3,6)   
    carpetPlotMask(X = x_angle_array[E], z_min = 0, z_max= 90, title = '(f) Net Optimization Including PV', hour_in_month = hour_in_month)
    plt.xlabel("Month of the Year",size=16)


    #space between the y-axes of the plots
    fig.tight_layout()
    fig.subplots_adjust(right = 0.8)
    
    #setting for the legend
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    cbar = plt.colorbar(cax=cbar_ax, ticks = [0,20,40,60,80,100]) #[0,15,30,45,60,75,90])
    cbar.ax.set_yticklabels(['0 (open)','20', '40', '60','80', '100 (close)'])#['0 (closed)', '15', '30', '45', '60', '75', '90 (open)'])
    cbar.solids.set_rasterized(True) 
    cbart = plt.title("Percent window covered\nwith blinds [%]", fontsize=14)
    cbart.set_position((1.1,1.02))
    cbar.ax.tick_params(labelsize=14)
    #plt.tight_layout()
    plt.show()       
    
                
    return fig
    
#def createCarpetPlotXAngles2(x_angle_array, hour_in_month, H, C, E, E_HCL):  
#    
#    """
#    6 plots in row
#    """
#   
#    fig = plt.figure(figsize=(4, 30))
#    #    plt.suptitle("Optimum Altitude and Azimuth Orientation", size=16)
#    plt.subplot(6,1,1)
#    carpetPlotMask(X = x_angle_array[H], z_min = 0, z_max= 90, title = '(a) Heating Optimization', hour_in_month = hour_in_month)
#    plt.ylabel("Hour of the Day",size=14)
#    
#    plt.subplot(6,1,2)
#    carpetPlotMask(X = x_angle_array[C], z_min = 0, z_max= 90, title = '(b) Cooling Optimization', hour_in_month = hour_in_month)
#    plt.ylabel("Hour of the Day",size=14)
#    
#    plt.subplot(6,1,3)
#    carpetPlotMask(X = x_angle_array['Lighting'], z_min = 0, z_max= 90, title = '(c) Lighting Optimization', hour_in_month = hour_in_month)
#    plt.ylabel("Hour of the Day",size=14)    
#    
#    plt.subplot(6,1,4)
#    carpetPlotMask(X = x_angle_array['SolarEnergy'], z_min = 0, z_max= 90, title = '(d) PV Supply Optimization', hour_in_month = hour_in_month)
#    plt.ylabel("Hour of the Day",size=14)
#    
#    plt.subplot(6,1,5)
#    carpetPlotMask(X = x_angle_array[E_HCL], z_min = 0, z_max= 90, title = '(e) Building Demand Optimization', hour_in_month = hour_in_month)
#    plt.ylabel("Hour of the Day",size=14)    
#    
#    plt.subplot(6,1,6)   
#    carpetPlotMask(X = x_angle_array[E], z_min = 0, z_max= 90, title = '(f) Net Optimization Including PV', hour_in_month = hour_in_month)
#    plt.xlabel("Month of the Year",size=14)
#    plt.ylabel("Hour of the Day",size=14)
#
#    #space between the y-axes of the plots
#    fig.tight_layout()
#    fig.subplots_adjust(right = 0.8)
#    
#    #setting for the legend
#    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#    cbar = plt.colorbar(cax=cbar_ax, ticks = [0,15,30,45,60,75,90])
#    cbar.ax.set_yticklabels(['0 (closed)', '15', '30', '45', '60', '75', '90 (open)'])
#    cbar.solids.set_rasterized(True) 
#    cbart = plt.title("Altitude Angle [deg]", fontsize=12)
#    cbart.set_position((1.1,1.02))
#    cbar.ax.tick_params(labelsize=14)
#    #plt.tight_layout()
#    plt.show()       
#    
#                
#    return fig
   

def createCarpetPlotYAngles(y_angle_array, hour_in_month, H, C, E, E_HCL):  
   
    fig = plt.figure(figsize=(16, 8))
    #    plt.suptitle("Optimum Altitude and Azimuth Orientation", size=16)
    plt.subplot(2,3,1)
    carpetPlotMask(X = y_angle_array[H], z_min = 0, z_max= 90, title = '(a) Heating Optimization', hour_in_month = hour_in_month)
    plt.ylabel("Hour of the Day",size=14)
    
    plt.subplot(2,3,2)
    carpetPlotMask(X = y_angle_array[C], z_min = 0, z_max= 90, title = '(b) Cooling Optimization',hour_in_month = hour_in_month)
    
    plt.subplot(2,3,3)
    carpetPlotMask(X = y_angle_array['Lighting'],z_min = 0, z_max= 90, title = '(c) Lighting Optimization', hour_in_month = hour_in_month)
    
    """plt.subplot(2,3,4)
    carpetPlotMask(X = y_angle_array['SolarEnergy'], z_min = 0, z_max= 90, title = '(d) PV Supply Optimization', hour_in_month = hour_in_month)
    plt.xlabel("Month of the Year",size=14)
    plt.ylabel("Hour of the Day",size=14)"""
    
    plt.subplot(2,3,5)
    carpetPlotMask(X = y_angle_array[E_HCL], z_min = 0, z_max= 90, title = '(e) Building Demand Optimization', hour_in_month = hour_in_month)
    plt.xlabel("Month of the Year",size=14)    
    
    plt.subplot(2,3,6)   
    carpetPlotMask(X = y_angle_array[E], z_min = 0, z_max= 90, title = '(f) Net Optimization Including PV', hour_in_month = hour_in_month)
    plt.xlabel("Month of the Year",size=14)


    #space between the y-axes of the plots
    fig.tight_layout()
    fig.subplots_adjust(right = 0.8)
    
    #setting for the legend
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    cbar = plt.colorbar(cax=cbar_ax, ticks = [ 0, 45,90]) #[-45,-30,-15,0,15,30,45])
    cbar.ax.set_yticklabels(['0 (closed)', '45', '90 (open)']) #['-45 (SW)', '-30', '-15', '0 (S)', '15', '30', '45 (SE)'])
    cbar.solids.set_rasterized(True) 
    cbart = plt.title("Tilt angle [deg]", fontsize=14)
    cbart.set_position((1.1,1.02))
    cbar.ax.tick_params(labelsize=14)
    #plt.tight_layout()
    plt.show()       
    
                
    return fig

#def createCarpetPlotYAngles2(y_angle_array, hour_in_month, H, C, E, E_HCL): 
#    
#    """
#    6 plots in row
#    """
#   
#    fig = plt.figure(figsize=(4, 30))
#    #    plt.suptitle("Optimum Altitude and Azimuth Orientation", size=16)
#    plt.subplot(6,1,1)
#    carpetPlotMask(X = y_angle_array[H], z_min = -45, z_max= 45, title = '(a) Heating Optimization', hour_in_month = hour_in_month)
#    plt.ylabel("Hour of the Day",size=14)
#    
#    plt.subplot(6,1,2)
#    carpetPlotMask(X = y_angle_array[C], z_min = -45, z_max= 45, title = '(b) Cooling Optimization',hour_in_month = hour_in_month)
#    plt.ylabel("Hour of the Day",size=14)
#    
#    plt.subplot(6,1,3)
#    carpetPlotMask(X = y_angle_array['Lighting'],z_min = -45, z_max= 45, title = '(c) Lighting Optimization', hour_in_month = hour_in_month)
#    plt.ylabel("Hour of the Day",size=14)
#    
#    plt.subplot(6,1,4)
#    carpetPlotMask(X = y_angle_array['SolarEnergy'], z_min = -45, z_max= 45, title = '(d) PV Optimization', hour_in_month = hour_in_month)
#    plt.ylabel("Hour of the Day",size=14)
#    
#    plt.subplot(6,1,5)
#    carpetPlotMask(X = y_angle_array[E_HCL], z_min = -45, z_max= 45, title = '(e) Total Thermal/Lighting Optimization', hour_in_month = hour_in_month)
#    plt.ylabel("Hour of the Day",size=14)
#    
#    plt.subplot(6,1,6)   
#    carpetPlotMask(X = y_angle_array[E], z_min = -45, z_max= 45, title = '(f) Net Optimization Including PV', hour_in_month = hour_in_month)
#    plt.xlabel("Month of the Year",size=14)
#    plt.ylabel("Hour of the Day",size=14)
#
#    #space between the y-axes of the plots
#    fig.tight_layout()
#    fig.subplots_adjust(right = 0.8)
#    
#    #setting for the legend
#    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
#    cbar = plt.colorbar(cax=cbar_ax, ticks = [-45,-30,-15,0,15,30,45])
#    cbar.ax.set_yticklabels(['-45 (SW)', '-30', '-15', '0 (S)', '15', '30', '45 (SE)'])
#    cbar.solids.set_rasterized(True) 
#    cbart = plt.title("Azimuth Angle [deg]", fontsize=14)
#    cbart.set_position((1.1,1.02))
##        cbar = plt.colorbar(cax=cbar_ax, ticks=range(0,len(allAngles[0])))
#        #cbar.ax.set_yticklabels(AnglesString)
#    cbar.ax.tick_params(labelsize=14)
#    #plt.tight_layout()
#    plt.show()       
#    
#                
#    return fig
#        
