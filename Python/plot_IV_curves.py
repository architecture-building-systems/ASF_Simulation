# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 16:03:03 2016

@author: Assistenz
"""
from pylab import *

figure()
for i in range(20):
    plot(volt_model_var,curr_model_submod_lookup[201,i,:])