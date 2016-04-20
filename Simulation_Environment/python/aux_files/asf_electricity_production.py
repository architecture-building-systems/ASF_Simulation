# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 18:27:17 2016

Calculate Electrical Power of ASF

Authors: Johannes Hofer, Jeremias Schmidli

"""
def asf_electricity_production(createPlots=False, lb_radiation_path=None, panelsize = 400, pvSizeOption=0, save_results_path = None, lookup_table_path = None, geo_path = None):
    import json
    import numpy as np
    import time
    import warnings
    import matplotlib.pyplot as plt
    from scipy import interpolate
    from average_monthly import daysPassedMonth
    from prepareData import readLayoutAndCombinations, CalcXYAnglesAndLocation
    
    create_plots_flag = createPlots
    Simulation_Data_Folder = lb_radiation_path
    
    filename = ('RadiationResultsElectrical_monthly_hourIt_combIt_')
    filetype = ('.csv')
    
    # load irradiance lookup table
    # load('curr_model_submod_lookup2')
    # load('curr_model_submod_lookup2_constTemp')
    #load('C:/Users/Assistenz/ASF_Simulation/Python/curr_model_submod_lookup.npy','r')
    curr_model_submod_lookup = np.load(lookup_table_path + '\curr_model_submod_lookup.npy','r')
    pointsPerLookupCurve = np.shape(curr_model_submod_lookup)[2]
    #curr_model_submod_lookup2 = curr_model_submod_lookup3(mslice[:], 9)
    
    # load weather file data corresponding to Simulation Data:
    with open(geo_path + '\SunTrackingData.json', 'r') as fp:
        SunTrackingData = json.load(fp)
        fp.close()
        
     # find the number of hours analysed by ladybug:
    numHours = np.shape(SunTrackingData['HOY'])[0]
    
    # find the number of combinations analysed by ladybug:
    numCombPerHour = len(CalcXYAnglesAndLocation(readLayoutAndCombinations(lb_radiation_path))['allAngles'][0])
    
    # set numCombPerHour to 1 if it appears to be zero (this is the case for suntracking)
    if numCombPerHour == 0:
        numCombPerHour = 1
    
   
    numASFit = numHours*numCombPerHour
    
    
    filenames = []
    
    for i in range(numASFit):
    #    filenames.append(filename + str(i) + filetype)
        filenames.append(filename + str(i/numCombPerHour) + '_' + str(i%numCombPerHour) + filetype)
    
    
    
    # module and cell dimensions:
    
     # panelsize used for simulations (sidelength in mm):
    panelsize = readLayoutAndCombinations(lb_radiation_path)['panelSize']  
    
    # gridpoint size input of GH, not equal to the actual grid point size if the panelsize is not a multiple of 25mm:
    desiredGridPointSize = readLayoutAndCombinations(lb_radiation_path)['desiredGridPointSize']  
    
    nparcell = int(round(panelsize/float(desiredGridPointSize)))
    cellsPerGridpoint = 3
    ncell = nparcell*cellsPerGridpoint
    panelwidth = panelsize/1000.
    panellength = panelsize/1000.
    panelarea = panelwidth * panellength
    
    scellsize = (panelwidth / ncell) * (panellength / nparcell)
    
    varPVsize = pvSizeOption#change the size of the PV area, this is done in steps of 2
    # times the radiation gridsize, so 0 corresponds a PV-size of 400mm, 
    # 1 corresponds to PV-size of 350mm, 2 corresponds to 300mm etc. 
    
    varncell = ncell - varPVsize * 2 * cellsPerGridpoint
    varnparcell = nparcell - varPVsize * 2
    apertsize = float(varnparcell) / nparcell * panelwidth * varncell / ncell * panellength
    
    # reference module
    refmodwidth = 0.294
    refmodlength = 1.260
    #refmodsize = refmodwidth * refmodlength
    refncell = 42
    refnparcell = 180
    refscellwidth = refmodwidth / refncell
    refscelllength = refmodlength / refnparcell
    refscellsize = refscellwidth * refscelllength
    scellscale_factor = scellsize / refscellsize
    
    # lookup iv curve 
    #temp = 25 + 273.15
    vmin = -6 * varncell
    vmax = 0.8 * varncell#30
    volt_model_var = np.linspace(vmin, vmax, 1000)
    
    # module efficiency 
    insrefind = 200 # corresponds to 1000 W/m2
    trefind = 9 # corresponds to 25°C 
    
    alwaysUseReferenceTemperature = False # set False if temperature of the cells should be included in analysis
    
    # apertscale=panelarea/apertsize;
    apertscale = float(apertsize) / panelarea
    modmpprating = 40 # module maximum power point rating
    modmppsim = max(volt_model_var * curr_model_submod_lookup[insrefind, trefind,:])#module maximum power point simulation
    currscale = modmpprating / modmppsim
    
        
    temp_amb = SunTrackingData['TempTracking']
    
    # load days per month
    days_passed_month, days_per_month =  daysPassedMonth()
    
    # number of panels in evaluated ASF:
    panelnum = 50
    
    # preallocate data for speed:
    Pmod_mpp = np.empty((numASFit, panelnum))*np.nan
    Vmod_mpp = np.empty((numASFit, panelnum))*np.nan
    Imod_mpp = np.empty((numASFit, panelnum))*np.nan
    Ins_ap = np.empty((numASFit, panelnum))*np.nan
    Ins_ap_mean = np.empty((numASFit, panelnum))*np.nan
    #Ins_ap_rmsd = np.empty((numASFit, panelnum))*np.nan
    
    
    #Ins_ap_maxdiff = np.empty((numASFit, panelnum))*np.nan
    
    Ins_sum = np.empty(numASFit)*np.nan
    Ins_avg = np.empty(numASFit)*np.nan
    Pmpp_sum = np.empty(numASFit)*np.nan
    Pmpp_avg = np.empty(numASFit)*np.nan
    effap_arr = np.empty(numASFit)*np.nan
    effmod_arr = np.empty(numASFit)*np.nan
    #ins_rmsd_avg = np.empty(numASFit)*np.nan
    theoreticalMaxRad = np.empty(numASFit)*np.nan
    
    radiationYear = 0
    pvYear = 0
    
    #start iteration somewhere in the middle:
    startIt = 0
    if startIt !=0 :
        warnings.warn("Warning: the Iteration Starts at a number other than 0, some data will be ignored, check the variable startIt")
        
    tic = time.time()
    
    # loop through simulation data files:
    for SimulationNumber in range(startIt,numASFit):
    
        
        endata = np.genfromtxt(Simulation_Data_Folder + '/' + filenames[SimulationNumber], delimiter=',', skip_header=7)
        maxRadPoint = np.max(endata)*1000 # Wh/(m2*h)
        theoreticalMaxRad[SimulationNumber] = maxRadPoint/ days_per_month[SunTrackingData['MonthTracking'][SimulationNumber/numCombPerHour]-1] # Wh/h per gridpoint
        gridPsize = panellength / nparcell * panelwidth / nparcell# size of each gridpoint
        irr_gridP = endata * gridPsize / days_per_month[SunTrackingData['MonthTracking'][SimulationNumber/numCombPerHour]-1] # Wh/h per gridpoint
        #irr_pan2 = sum(irr_gridP, 1) # Wh/h per panel
    
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
    
    
            # set results for very small radiation equal to zero
    #        if np.mean(irr_mod_mat_rnd)<10:
    #            Pmod_tot[mod_sel,:] = 0
    #            break
                
            #Ins_apule = sum(sum(irr_mod_mat_rnd)) * gridPsize    # insolation per module [Wh]
            #Ins_aparea = Ins_apule / panelarea    # insolation per module area [Wh/m2]
    
            # preallocate data for currents at each gridpoint:
            curr_model_submod = np.empty((len(irr_mod_mat_rnd),len(irr_mod_mat_rnd),pointsPerLookupCurve))*np.nan
            
            # lookup current for each gridpoint:     
            for i in range(np.shape(irr_mod_mat_rnd)[0]):
                for j in range(np.shape(irr_mod_mat_rnd)[1]):
                    insind = int(round(irr_mod_mat_rnd[i, j] / 5.0))
                    tempind = int(round((20 + temp_amb[SimulationNumber/numCombPerHour] + 0.0225*irr_mod_mat_rnd[i, j])/5.0))
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
            curr_int_points_cell = np.linspace(-0.0, np.min([np.min(np.max(Icell_comb,1)),5]), 1000)
            #curr_int_points_cell = np.linspace(-0.5, 5, 1000)
    
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
            Ins_ap[SimulationNumber, mod_sel] = np.sum(irr_mod_mat_rnd) * gridPsize # insolation per aperture [Wh]
            Ins_ap_mean[SimulationNumber, mod_sel] = np.mean(irr_mod_mat_rnd) # average insolation per aperture [Wh/m2]
    
    
        Ins_sum[SimulationNumber] = np.sum(Ins_ap[SimulationNumber,:]) # sum insolation
        #     Ins_avg(i)=sum(Ins_ap(i,:)./panelarea)/numpanels(i); % W/m2 average
        Ins_avg[SimulationNumber] = np.sum(Ins_ap_mean[SimulationNumber,:]) / panelnum  # W/m2 average
        Pmpp_sum[SimulationNumber] = np.sum(Pmod_mpp[SimulationNumber, :])    # sum power
        Pmpp_avg[SimulationNumber] = np.sum(Pmod_mpp[SimulationNumber, :] / apertsize) / panelnum   # W/m2 average
        effap_arr[SimulationNumber] = Pmpp_sum[SimulationNumber] / Ins_sum[SimulationNumber]* 100.  #
        effmod_arr[SimulationNumber] = Pmpp_sum[SimulationNumber] / Ins_sum[SimulationNumber]* 100* apertscale 
        
        #add total energy (radiation and pv) and multiply by days in month
        radiationYear += Ins_sum[SimulationNumber]/1000.* days_per_month[SunTrackingData['MonthTracking'][SimulationNumber/numCombPerHour]-1] #kWh
        pvYear += Pmpp_sum[SimulationNumber]/1000.*days_per_month[SunTrackingData['MonthTracking'][SimulationNumber/numCombPerHour]-1] #kWh
        
        
        toc = time.time() - tic
        
        print 'time passed (min): ' + str(toc/60.)
        print 'iteration number: ' + str(SimulationNumber) + ' of ' + str(numASFit)
    
    
    PV_electricity_results = {'numComb': numCombPerHour, 'numHours': numHours, 'Ins_sum': Ins_sum, 'Ins_avg': Ins_avg, 'theoreticalMaxRad': theoreticalMaxRad, 'Pmpp_sum': Pmpp_sum, 'Pmpp_avg': Pmpp_avg, 'eff_ap' : effap_arr, 'eff_mod': effmod_arr, 'hour_in_month': SunTrackingData['HoursInMonthTracking'], 'month':  SunTrackingData['MonthTracking'],'days_per_month':days_per_month}
    np.save(save_results_path + '\PV_electricity_results.npy',PV_electricity_results)    
    
    PV_detailed_results = {'numComb': numCombPerHour, 'numHours': numHours, 'Ins_ap': Ins_ap, 'Pmod_mpp': Pmod_mpp, 'hour_in_month': SunTrackingData['HoursInMonthTracking'], 'month':  SunTrackingData['MonthTracking'],'days_per_month':days_per_month}
    np.save(save_results_path + '\PV_detailed_results.npy',PV_detailed_results)    
    
    if create_plots_flag:
        
        fig1 = plt.figure()
        
        plt.subplot(2, 2, 1)
        plt.plot(range(1,panelnum+1), np.transpose(Ins_ap) / apertsize)
        plt.xlim(([0, panelnum]))
        plt.xlabel(('Module number'), fontsize = 12)
        plt.ylabel(('aperture insolation (W/m2)'), fontsize = 12)
    
        plt.subplot(2, 2, 2)
        plt.plot(range(1,panelnum+1), np.transpose(Pmod_mpp)/ apertsize)
        plt.xlim([0, panelnum])
        plt.xlabel(('Module number'), fontsize = 12)
        plt.ylabel(('aperture power (W/m2)'), fontsize = 12)
    
        plt.subplot(2, 2, 3)
        plt.plot(np.transpose(Pmod_mpp)/np.transpose(Ins_ap)* 100.)
        plt.xlim(([0, 50]))
        plt.xlabel(('Module number'), fontsize = 12)
        plt.ylabel(('Aperture Efficiency (%)'), fontsize =  12)
    
    
        plt.subplot(2, 2, 4)
        plt.plot(np.transpose(Pmod_mpp)/np.transpose(Ins_ap)* 100. * apertscale)
        plt.xlim(([0, 50]))
        plt.xlabel(('Module number'), fontsize = 12)
        plt.ylabel(('Module Efficiency (%)'), fontsize =  12)
                 
                 
                 
        fig2 = plt.figure()
        
        plt.subplot(2, 2, 1)
        plt.plot(range(numASFit), np.squeeze(Ins_avg),label='average Insolation')
        plt.hold(True)
        plt.plot(range(numASFit), np.squeeze(theoreticalMaxRad), label='theoretical maximum Insolation')
        plt.xlim(([0, numASFit]))
        plt.legend()
        plt.xlabel(('Iteration number'), fontsize = 12)
        plt.ylabel(('Aperture insolation (W/m2)'), fontsize = 12)
    
        plt.subplot(2, 2, 2)
        plt.plot(range(numASFit), Pmpp_avg)
        plt.xlim([0, numASFit])
        plt.xlabel(('Iteration number'), fontsize = 12)
        plt.ylabel(('Average Aperture Power (W/m2)'), fontsize = 12)
    
        plt.subplot(2, 2, 3)
        plt.plot(range(numASFit), effap_arr)
        plt.xlim(([0, numASFit]))
        plt.xlabel(('Iteration number'), fontsize = 12)
        plt.ylabel(('Aperture Efficiency (%)'), fontsize =  12)
    
    
        plt.subplot(2, 2, 4)
        plt.plot(range(numASFit), effmod_arr)
        plt.xlim(([0, numASFit]))
        plt.xlabel(('Iteration number'), fontsize = 12)
        plt.ylabel(('Module Efficiency (%)'), fontsize =  12)
        
        print 'PV production succesfully calculated'
        return PV_electricity_results, PV_detailed_results, fig1, fig2
    
    else:
        print 'PV production succesfully calculated'
        return PV_electricity_results, PV_detailed_results