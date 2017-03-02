# -*- coding: utf-8 -*-
"""
Created on Wed May 04 19:46:28 2016

@author: Assistenz
"""

import numpy as np
import matplotlib.pyplot as plt

fig,ax = plt.subplots(1)
ax.set_aspect('equal')

# The data array
m1 = np.random.rand(5,5)
# The alpha array. Normalize your map2 to the range 0,1
m2 = np.linspace(0,1,25).reshape(5,5) 

p = ax.pcolormesh(m1)
plt.savefig('myfig.png')

for i,j in zip(p.get_facecolors(),m2.flatten()):
    i[3] = j # Set the alpha value of the RGBA tuple using m2

plt.savefig('myfig.png')