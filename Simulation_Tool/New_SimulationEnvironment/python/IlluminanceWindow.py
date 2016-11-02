# -*- coding: utf-8 -*-
"""
Created on Tue Nov 01 17:06:28 2016

@author: Mauro

The total flux method
S. 105


"""



# E = illuminance on work plane (lux)
# E_w = illuminance on face of window
# UF = utilisation factor
# M = maintenance factor
# G = glass factor
# B = framing factor
# A_f = area of floor


A_f = 7. * 4.9 # m2
A_w = 13.5 #m2
M = 0.9 #S.127
G = 0.85 # S.127
B = 1 # S.127
UF = 0.15
E_w = 2000 #lux


def illuminanceCalc(E_w, A_w, UF, M, G, B, A_f):
    E = E_w * A_w * UF * M * G * B * 1/(A_f)
    
    return E

E = illuminanceCalc(E_w, A_w, UF, M, G, B, A_f)


print "E work plane: ", E