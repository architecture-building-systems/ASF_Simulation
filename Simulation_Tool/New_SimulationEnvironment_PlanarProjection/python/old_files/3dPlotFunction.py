# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 08:56:37 2016

@author: Mauro
"""
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


def create3Dplot(Data):
    
    dataList = []    
    
    for ii in range(49):
        dataList.append(Data[ii])
      
    reData = np.reshape(dataList, (7, 7))
  
    figA = plt.figure(figsize=(10, 10))
    ax = figA.add_subplot(111,  projection='3d') #, projection='3d'
    
    X,Y = np.meshgrid(range(0,105,15),range(-45,60,15))
    
       
    surf = ax.plot_surface(X,Y,reData, cmap = cm.pink_r, rstride=1, cstride=1)
    
    #plt.title('Hourly Solar Energy Evaluation')
    plt.xlabel('Altitude Angle [deg]',  fontsize=16)
    plt.xticks([0,15,30,45,60,75,90])
    plt.ylabel('Azimuth Angle [deg]',  fontsize=16)
    plt.yticks([-45,-30,-15,0,15,30,45])
    
    ax.set_zlim(250, 600)
    ax.set_zlabel('Solar Electricity Production [Wh]',  fontsize=16)
   
    
#    ax.zaxis.set_major_locator(LinearLocator(10))
#    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    #fig.colorbar(surf, shrink=0.5, aspect=5)
    ax.view_init(45,45)
    #ax.view_init(130,45)

    plt.tight_layout()
    plt.draw()
    
    return figA



