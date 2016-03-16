# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 16:03:03 2016

@author: Assistenz
"""
from pylab import *

figure()
for i in range(20):
    plot(volt_model_var,curr_model_submod_lookup[70,i,:])
    
figure()

plot(volt_model_var,curr_model_test)

figure()

plot(Vmod,Imod)

figure()

plot(Vmod,Pmod)

figure()

plot(Vcell_comb_int[kk,:],curr_int_points_cell)

efficiencies_lookup = np.empty((301,20))*np.nan
ref_power_lookup = np.empty(301)
for i in range(301):
    ref_power_lookup[i] =  1 + (i) * 5
    for j in range(20):
        efficiencies_lookup[i,j]=max(curr_model_submod_lookup[i,j]*volt_model_var)/ref_power_lookup[i]*100.
        