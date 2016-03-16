# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 18:27:17 2016

Calculate Electrical Power of ASF

Authors: Johannes Hofer, Jeremias Schmidli

"""


import json
import numpy as np
import time
#import csv
import matplotlib.pyplot as plt
from scipy import interpolate

create_plots_flag = True

#Simulation_Data_Folder = 'C:\Users\Assistenz\Documents\MT_Jeremias\Simulation_Data\RadiationEvaluation\Radiation_electrical_sunTracking';
Simulation_Data_Folder = ('C:\\Users\\Assistenz\\Documents\\MT_Jeremias\\Simulation_Data\\RadiationEvaluation\\Radiation_electrical_sunTracking_allFiles_sameHour')
Read_json_Folder = ('C:\\Users\\Assistenz\\Documents\\MT_Jeremias\\python-matlab-bridge-master\\pymatbridge\\matlab')

filename = ('RadiationResultsElectrical_tracking')
filetype = ('.csv')

# load irradiance lookup table
# load('curr_model_submod_lookup2')
# load('curr_model_submod_lookup2_constTemp')
#load('C:/Users/Assistenz/ASF_Simulation/Python/curr_model_submod_lookup.npy','r')
curr_model_submod_lookup = np.load('C:/Users/Assistenz/ASF_Simulation/Python/' + 'curr_model_submod_lookup.npy','r')
pointsPerLookupCurve = np.shape(curr_model_submod_lookup)[2]
#curr_model_submod_lookup2 = curr_model_submod_lookup3(mslice[:], 9)

numASFit = 5

filenames = []

for i in range(numASFit):
    filenames.append(filename + str(i) + filetype)



# module and cell dimensions

ncell = 48
nparcell = 16
cellsPerGridpoint = 3
panelwidth = 0.4
panellength = 0.4
panelsize = panelwidth * panellength

scellsize = (panelwidth / ncell) * (panellength / nparcell)

varPVsize = 1#change the size of the PV area, this is done in steps of 2
# times the radiation gridsize, so 0 corresponds a PV-size of 400mm, 
# 1 corresponds to PV-size of 350mm, 2 corresponds to 300mm etc. 

varncell = ncell - varPVsize * 2 * cellsPerGridpoint
varnparcell = nparcell - varPVsize * 2
apertsize = float(varnparcell) / nparcell * panelwidth * varncell / ncell * panellength

# reference module
refmodwidth = 0.294
refmodlength = 1.260
refmodsize = refmodwidth * refmodlength
refncell = 42
refnparcell = 180
refscellwidth = refmodwidth / refncell
refscelllength = refmodlength / refnparcell
refscellsize = refscellwidth * refscelllength
scellscale_factor = scellsize / refscellsize

# lookup iv curve 
temp = 25 + 273.15
vmin = -6 * varncell
vmax = 0.8 * varncell#30
volt_model_var = np.linspace(vmin, vmax, 1000)

# module efficiency 
insrefind = 200 # corresponds to 1000 W/m2
trefind = 9 # corresponds to 25°C 

alwaysUseReferenceTemperature = False # set False if temperature of the cells should be included in analysis

# apertscale=panelsize/apertsize;
apertscale = float(apertsize) / panelsize
modmpprating = 40 # module maximum power point rating
modmppsim = max(volt_model_var * curr_model_submod_lookup[insrefind, trefind,:])#module maximum power point simulation
currscale = modmpprating / modmppsim

# load temperature corresponding to Simulation Data:
with open('C:/Users/Assistenz/Documents/MT_Jeremias/Simulation_Data/RadiationEvaluation/' + 'SunTrackingData.json', 'r') as fp:
    SunTrackingData = json.load(fp)
    fp.close()
    
temp_amb = SunTrackingData['TempTracking']

# number of panels in evaluated ASF:
panelnum = 50

# preallocate data for speed:
Pmod_mpp = np.empty((numASFit, panelnum))*np.nan
Vmod_mpp = np.empty((numASFit, panelnum))*np.nan
Imod_mpp = np.empty((numASFit, panelnum))*np.nan
Ins_mod = np.empty((numASFit, panelnum))*np.nan
Ins_mod_mean = np.empty((numASFit, panelnum))*np.nan
Ins_mod_rmsd = np.empty((numASFit, panelnum))*np.nan


Ins_mod_maxdiff = np.empty((numASFit, panelnum))*np.nan

Ins_sum_roof = np.empty(numASFit)*np.nan
Ins_avg_roof = np.empty(numASFit)*np.nan
Pmpp_sum_roof = np.empty(numASFit)*np.nan
Pmpp_avg_roof = np.empty(numASFit)*np.nan
effap_arr = np.empty(numASFit)*np.nan
effmod_arr = np.empty(numASFit)*np.nan
ins_rmsd_avg = np.empty(numASFit)*np.nan

# loop through simulation data files:
for SimulationNumber in range(numASFit):

    tic = time.time()
    
    endata = np.genfromtxt(Simulation_Data_Folder + '/' + filenames[SimulationNumber], delimiter=',', skip_header=7)

    gridPsize = panellength / nparcell * panelwidth / nparcell# size of each gridpoint
    irr_gridP = endata * gridPsize # Wh/h per gridpoint
    irr_pan2 = sum(irr_gridP, 1) # Wh/h per panel

    Vmod_tot = np.empty((panelnum, len(volt_model_var)))*np.nan
    Imod_tot = np.empty((panelnum, len(volt_model_var)))*np.nan
    Pmod_tot = np.empty((panelnum, len(volt_model_var)))*np.nan

    
    for mod_sel in range(panelnum):    # module iteration

        # select irradiance per module
        irr_mod_sel = np.array(1 / gridPsize *irr_gridP[mod_sel, :])
        
        # create a grid with all radiation points (nparcellxnparcell)
        irr_mod_mat_rnd = np.round(irr_mod_sel * 1000)   
        irr_mod_mat_rnd.resize(nparcell, nparcell)        
        
        # delete 2 times number of columns and rows specified in varPVsize 
        if varPVsize > 0:
            irr_mod_mat_rnd = irr_mod_mat_rnd[ varPVsize: - varPVsize,varPVsize:- varPVsize]

        ins_module = sum(sum(irr_mod_mat_rnd)) * gridPsize    # insolation per module [Wh]
        ins_modarea = ins_module / panelsize    # insolation per module area [Wh/m2]

        # preallocate data for currents at each gridpoint:
        curr_model_submod = np.empty((len(irr_mod_mat_rnd),len(irr_mod_mat_rnd),pointsPerLookupCurve))*np.nan
        
        # lookup current for each gridpoint:     
        for i in range(np.shape(irr_mod_mat_rnd)[0]):
            for j in range(np.shape(irr_mod_mat_rnd)[1]):
                insind = int(round(irr_mod_mat_rnd[i, j] / 5.0))
                tempind = int(round((20 + temp_amb[SimulationNumber] + 0.0225*irr_mod_mat_rnd[i, j])/5.0))
                if alwaysUseReferenceTemperature:
                    tempind = trefind
                curr_model_submod[i, j, :] = scellscale_factor * currscale * curr_model_submod_lookup[insind, tempind,:]

        # cell reverse characteristics
        vol_bd = -6.1
        miller_exp = 3

        # calculate subcell forward and reverse iv curve
        Vscell = volt_model_var / refncell
        Iscell = np.empty((varnparcell, varnparcell, pointsPerLookupCurve))
        RevScale = 1. / (1 - (abs(Vscell) /-vol_bd) ** miller_exp)

        for ii in range(varnparcell):
            for jj in range(varnparcell):

                Iscell[ii, jj,:] = curr_model_submod[ii, jj,:] * RevScale /refnparcell

        Icell_comb = np.empty((varncell, pointsPerLookupCurve))*np.nan
        
        #  add currents of subcells per cell
        pointCounter = 0
        for kk in range(varncell):
            if kk % 3 == 0:
                pointCounter = pointCounter + 1

            Icell_comb[kk, :] = np.sum(Iscell[pointCounter-1, :, :], axis = 0)

        # add voltage from cell to cell
        curr_int_points_cell = np.linspace(-0.5, 5, 1000)

        Vcell_comb_int = np.empty((varncell,pointsPerLookupCurve))*np.nan
        Vmod_curr = np.empty((varncell-1,pointsPerLookupCurve))*np.nan
        Imod_curr =  np.empty((varncell-1,pointsPerLookupCurve))*np.nan
        Vmod_curr_int =  np.empty((varncell-1,pointsPerLookupCurve))*np.nan
        Pmod_curr =  np.empty((varncell-1,pointsPerLookupCurve))*np.nan

        for kk in range(varncell - 1):
            if kk == 0:
                interpFunction = interpolate.interp1d( Icell_comb[kk, :], Vscell)
                Vcell_comb_int[kk, :] = interpFunction(curr_int_points_cell)
                interpFunction = interpolate.interp1d( Icell_comb[kk+1, :], Vscell)
                Vcell_comb_int[kk + 1, :] = interpFunction(curr_int_points_cell)
                Vmod_curr[kk, :] = Vcell_comb_int[kk, :] + Vcell_comb_int[kk + 1, :]
                Imod_curr[kk, :] = curr_int_points_cell
            elif kk > 0:
                interpFunction = interpolate.interp1d(Imod_curr[kk - 1, :], Vmod_curr[kk - 1, :])
                Vmod_curr_int[kk, :] = interpFunction(curr_int_points_cell)
                interpFunction = interpolate.interp1d( Icell_comb[kk+1, :], Vscell)
                Vcell_comb_int[kk + 1, :] = interpFunction(curr_int_points_cell)
                Vmod_curr[kk, :] = Vmod_curr_int[kk, :] + Vcell_comb_int[kk + 1, :]
                Imod_curr[kk, :] = curr_int_points_cell
                Pmod_curr[kk, :] = Imod_curr[kk, :] * Vmod_curr[kk, :]

        Vmod = Vmod_curr[kk, :]
        Imod = Imod_curr[kk, :]
        Pmod = Pmod_curr[kk, :]

        Vmod_tot[mod_sel,:] = Vmod
        Imod_tot[mod_sel,:] = Imod
        Pmod_tot[mod_sel,:] = Pmod

        Pmod_mpp[SimulationNumber, mod_sel]= np.max(Pmod) # [W]
        Pmodmpp_ind = np.argmax(Pmod)                                   
        Vmod_mpp[SimulationNumber, mod_sel] = Vmod[Pmodmpp_ind]
        Imod_mpp[SimulationNumber, mod_sel] = Imod[Pmodmpp_ind]
        Ins_mod[SimulationNumber, mod_sel] = sum(irr_mod_mat_rnd) * gridPsize # insolation per module [Wh]
        Ins_mod_mean[SimulationNumber, mod_sel] = sum(irr_mod_mat_rnd) / (len(irr_mod_sel)) # insolation per module [Wh/m2]


    Ins_sum_roof[SimulationNumber] = sum(Ins_mod[SimulationNumber,:])                                        # sum insolation
    #     Ins_avg_roof(i)=sum(Ins_mod(i,:)./panelsize)/numpanels(i); % W/m2 average
    Ins_avg_roof[SimulationNumber] = sum(Ins_mod_mean[SimulationNumber,:]) / panelnum                                        # W/m2 average
    Pmpp_sum_roof[SimulationNumber] = sum(Pmod_mpp[SimulationNumber, :])                                        # sum power
    Pmpp_avg_roof[SimulationNumber] = sum(Pmod_mpp[SimulationNumber, :] / panelsize) / panelnum                                        # W/m2 average
    effap_arr[SimulationNumber] = Pmpp_sum_roof[SimulationNumber] / Ins_sum_roof[SimulationNumber]* 100. * apertscale                                        #
    effmod_arr[SimulationNumber] = Pmpp_sum_roof[SimulationNumber] / Ins_sum_roof[SimulationNumber]* 100
    
    toc = time.time() - tic
    
    print toc

    
if create_plots_flag:

    #several corrections in the following code for plotting, old code is
    #commented
    plt.figure()
    plt.subplot(2, 2, 1)
    #plot(Ins_mod./panelsize,'-b') % either this or the xlabel is wrong
    plt.plot(range(1,panelnum+1), np.transpose(Ins_mod) / panelsize)
    plt.xlim(([0, panelnum]))
    plt.xlabel(('Module number'), fontsize = 12)
    plt.ylabel(('Module insolation (W/m2)'), fontsize = 12)

    plt.subplot(2, 2, 2)
    #plot(Pmod_mpp,'-b')  % either this or the xlabel is wrong
    plt.plot(range(1,panelnum+1), np.transpose(Pmod_mpp)/panelsize)
    plt.xlim([0, panelnum])
    plt.xlabel(('Module number'), fontsize = 12)
    #ylabel('RMSD (W/m2)', 'FontSize',12)
    plt.ylabel(('Module power (W/m2)'), fontsize = 12)

    plt.subplot(2, 2, 3)
    plt.plot(np.transpose(Pmod_mpp)/np.transpose(Ins_mod)* 100.)
#    plt.hold("on")
#    plt.plot(np.transpose(Pmod_mpp)/np.transpose(Ins_mod)* 100.)
    plt.xlim(([0, 50]))
    #     legend('Aperture efficiency', 'Module efficiency')
#    plt.legend(('Module efficiency'), ('Aperture efficiency'))
    plt.xlabel(('Module number'), fontsize = 12)
    plt.ylabel(('Module Efficiency (%)'), fontsize =  12)


    plt.subplot(2, 2, 4)
    plt.plot(np.transpose(Pmod_mpp)/np.transpose(Ins_mod)* 100. * apertscale)
#    plt.hold("on")
#    plt.plot(np.transpose(Pmod_mpp)/np.transpose(Ins_mod)* 100.)
    plt.xlim(([0, 50]))
    #     legend('Aperture efficiency', 'Module efficiency')
#    plt.legend(('Module efficiency'), ('Aperture efficiency'))
    plt.xlabel(('Module number'), fontsize = 12)
    plt.ylabel(('Aperture Efficiency (%)'), fontsize =  12)
                        