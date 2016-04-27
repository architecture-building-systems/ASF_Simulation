# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 12:11:49 2016

Tradeoff Funtions

@author: Jeremias
"""
import numpy as np
import matplotlib.pyplot as plt

from auxFunctions import calculate_sum_for_index, create_evalList


def compareTotalEnergy(monthlyData, createPlots, tradeoffPeriod, auxVar):
    """
    function that calculates and plots the total energy for monthlyData during 
    a certain time period given in tradeoffPeriod
    """
    
    # assign data:
    H_data = monthlyData['H']
    C_data = monthlyData['C']
    L_data = monthlyData['L']
    PV_data = monthlyData['PV']

     # assign what efficiencies were used for evaluation:  
    if monthlyData['changedEfficiency'] == True:
        usedEfficiencies = monthlyData['efficiencyChanges']
    else:
        usedEfficiencies = monthlyData['efficiencies']

    # assign choose data (of evaluation period if demanded):
    if tradeoffPeriod['enabled']:
        print 'showing tradeoffs for month: ' + str(tradeoffPeriod['month']) + ', hours: ' +  str(tradeoffPeriod['startHour']) +'-' +  str(tradeoffPeriod['endHour']) 
        evalList = create_evalList('monthly', tradeoffPeriod['month'], tradeoffPeriod['startHour'], tradeoffPeriod['endHour'])
        H = H_data[:,evalList]
        C = C_data[:,evalList]
        L = L_data[:,evalList]
        PV = PV_data[:,evalList]
    else:
        print 'showing tradeoffs for the whole year'
        
        H = H_data
        C = C_data
        L = L_data
        PV = PV_data
    
    # sum individual data
    E_HCL = H+C+L
    
    if auxVar['combineResults']:
        E_tot = E_HCL+PV
    else:
        E_tot = E_HCL*np.nan
    
    # find indices
    Hind = np.argmin(H,axis=0)
    Cind = np.argmin(C,axis=0)
    Lind = np.argmin(L,axis=0)
    PVind = np.argmin(PV,axis=0)
    E_HCLind = np.argmin(E_HCL,axis=0)
    
    if auxVar['combineResults']:
        E_totind = np.argmin(E_tot,axis=0)
        if len(monthlyData['angles']['x_angles']) > 1:
            ind_0_0 =  monthlyData['angles']['allAngles'][0].index((0,0))
            ind_45_0 =  monthlyData['angles']['allAngles'][0].index((45,0))
            ind_90_0 =  monthlyData['angles']['allAngles'][0].index((90,0))
        else:
            ind_0_0 =  None
            ind_45_0 =  None
            ind_90_0 =  None
    else:
        ind_0_0 =  monthlyData['divaAngles']['allAngles'][0].index((0,0))
        ind_45_0 =  monthlyData['divaAngles']['allAngles'][0].index((45,0))
        ind_90_0 =  monthlyData['divaAngles']['allAngles'][0].index((90,0))
    
    # find energy use of indices:
    
    H_opt = calculate_sum_for_index(H,Hind)
    H_HCL = calculate_sum_for_index(H,E_HCLind)
    H_C = calculate_sum_for_index(H,Cind)
    if auxVar['combineResults']:
        H_PV = calculate_sum_for_index(H,PVind)
        H_tot = calculate_sum_for_index(H,E_totind)
    else:
        H_PV = H_opt*np.nan
        H_tot = H_opt*np.nan
    H_90 = calculate_sum_for_index(H,ind_90_0)
    H_45 = calculate_sum_for_index(H,ind_45_0)
    H_0 = calculate_sum_for_index(H,ind_0_0)
    
    TotalHbyPos=[H_opt, H_HCL, H_C, H_PV, H_tot, H_90, H_45, H_0]
    DiffH = TotalHbyPos-H_opt
    
    C_opt = calculate_sum_for_index(C,Cind)
    C_HCL = calculate_sum_for_index(C,E_HCLind)
    C_C = calculate_sum_for_index(C,Cind)
    if auxVar['combineResults']:
        C_PV = calculate_sum_for_index(C,PVind)
        C_tot = calculate_sum_for_index(C,E_totind)
    else:
        C_PV = C_opt*np.nan
        C_tot = C_opt*np.nan
    C_90 = calculate_sum_for_index(C,ind_90_0)
    C_45 = calculate_sum_for_index(C,ind_45_0)
    C_0 = calculate_sum_for_index(C,ind_0_0)
    
    TotalCbyPos=[C_opt, C_HCL, C_C, C_PV, C_tot, C_90, C_45, C_0]
    DiffC = TotalCbyPos - C_opt
    
    L_opt = calculate_sum_for_index(L,Lind)
    L_HCL = calculate_sum_for_index(L,E_HCLind)
    L_C = calculate_sum_for_index(L,Cind)
    L_PV = calculate_sum_for_index(L,PVind)
    if auxVar['combineResults']:
        L_PV = calculate_sum_for_index(L,PVind)
        L_tot = calculate_sum_for_index(L,E_totind)
    else:
        L_PV = L_opt*np.nan
        L_tot = L_opt*np.nan
    L_90 = calculate_sum_for_index(L,ind_90_0)
    L_45 = calculate_sum_for_index(L,ind_45_0)
    L_0 = calculate_sum_for_index(L,ind_0_0)
    
    TotalLbyPos=[L_opt, L_HCL, L_C, L_PV, L_tot, L_90, L_45, L_0]
    DiffL = TotalLbyPos - L_opt

    if auxVar['combineResults']:
        PV_opt = calculate_sum_for_index(PV,PVind)
        PV_HCL = calculate_sum_for_index(PV,E_HCLind)
        PV_C = calculate_sum_for_index(PV,Cind)
        PV_PV = calculate_sum_for_index(PV,PVind)
        PV_tot = calculate_sum_for_index(PV,E_totind)
        PV_90 = calculate_sum_for_index(PV,ind_90_0)
        PV_45 = calculate_sum_for_index(PV,ind_45_0)
        PV_0 = calculate_sum_for_index(PV,ind_0_0)
    else:
        PV_opt = calculate_sum_for_index(PV,PVind)
        PV_PV = calculate_sum_for_index(PV,PVind)
        PV_HCL = PV_opt*np.nan
        PV_C =  PV_opt*np.nan
        PV_tot = PV_opt*np.nan
        PV_90 = PV_opt*np.nan
        PV_45 = PV_opt*np.nan
        PV_0 = PV_opt*np.nan
        
    TotalPVbyPos=[PV_opt, PV_HCL, PV_C, PV_PV, PV_tot, PV_90, PV_45, PV_0]    
    DiffPV = TotalPVbyPos - PV_opt

    
    E_HCL_HCL = calculate_sum_for_index(E_HCL,E_HCLind)
    E_HCL_C = calculate_sum_for_index(E_HCL,Cind)
    if auxVar['combineResults']:
        E_HCL_PV = calculate_sum_for_index(E_HCL,PVind)
        E_HCL_tot = calculate_sum_for_index(E_HCL,E_totind)
    else:
        E_HCL_PV = E_HCL_HCL*np.nan
        E_HCL_tot = E_HCL_HCL*np.nan
    E_HCL_90 = calculate_sum_for_index(E_HCL,ind_90_0)
    E_HCL_45 = calculate_sum_for_index(E_HCL,ind_45_0)
    E_HCL_0 = calculate_sum_for_index(E_HCL,ind_0_0)
    
    TotalE_HCLbyPos=[E_HCL_HCL, E_HCL_HCL, E_HCL_C, E_HCL_PV, E_HCL_tot, E_HCL_90, E_HCL_45, E_HCL_0]
    DiffE_HCL = TotalE_HCLbyPos - E_HCL_HCL
    
    if auxVar['combineResults']:
        E_tot_HCL = calculate_sum_for_index(E_tot,E_HCLind)
        E_tot_C = calculate_sum_for_index(E_tot,Cind)
        E_tot_PV = calculate_sum_for_index(E_tot,PVind)
        E_tot_tot = calculate_sum_for_index(E_tot,E_totind)
        E_tot_90 = calculate_sum_for_index(E_tot,ind_90_0)
        E_tot_45 = calculate_sum_for_index(E_tot,ind_45_0)
        E_tot_0 = calculate_sum_for_index(E_tot,ind_0_0)
        
        TotalE_totbyPos=[E_tot_tot, E_tot_HCL, E_tot_C, E_tot_PV, E_tot_tot, E_tot_90, E_tot_45, E_tot_0]
        DiffE_tot = TotalE_totbyPos- E_tot_tot
    else:
        E_tot_HCL = np.nan
        E_tot_C = np.nan
        E_tot_PV = np.nan
        E_tot_tot = np.nan
        E_tot_90 = np.nan
        E_tot_45 = np.nan
        E_tot_0 = np.nan
        
        TotalE_totbyPos=[E_tot_tot, E_tot_HCL, E_tot_C, E_tot_PV, E_tot_tot, E_tot_90, E_tot_45, E_tot_0]
        DiffE_tot = [E_tot_tot, E_tot_HCL, E_tot_C, E_tot_PV, E_tot_tot, E_tot_90, E_tot_45, E_tot_0]

    
    if createPlots:
        
        # assign number of groups to be plotted:
        n_groups = 8
        
        # create figure:
#        fig, ax = plt.subplots()
        fig = plt.figure(figsize=(16, 8))
        plt.subplot(2,1,1)
        
        index = np.arange(n_groups)
        bar_width = 0.15
        
        opacity = 0.4
        
        plt.bar(index, TotalHbyPos, bar_width,
                         alpha=opacity,
                         color='r',
                         label='H (COP=' + str(usedEfficiencies['H_COP']) + ')')
        
        plt.bar(index+ bar_width, TotalCbyPos, bar_width,
                         alpha=opacity,
                         color='b',
                         label='C (COP=' + str(usedEfficiencies['C_COP']) + ')')
                         
        plt.bar(index+ bar_width*2, TotalLbyPos, bar_width,
                         alpha=opacity,
                         color='g',
                         label='L (Load=' + str(usedEfficiencies['L_Load']) + ' W/m2)')
                         
        if usedEfficiencies['PV'] == 1 or not monthlyData['changedEfficiency'] :
            plt.bar(index+ bar_width*3, TotalPVbyPos, bar_width,
                         alpha=opacity,
                         color='c',
                         label='PV')
        else:
            plt.bar(index+ bar_width*3, TotalPVbyPos, bar_width,
                         alpha=opacity,
                         color='c',
                         label='PV (multiplied by ' + str(usedEfficiencies['PV']) + ')')           
                         
        plt.bar(index+ bar_width*4, TotalE_HCLbyPos, bar_width,
                         alpha=opacity,
                         color='m',
                         label='E_HCL')
        if auxVar['combineResults']:
            plt.bar(index+ bar_width*5, TotalE_totbyPos, bar_width,
                            alpha=opacity,
                            color='k',
                            label='E_tot')
        
        plt.xlabel('Combinations')
        plt.ylabel('Energy [kWh]')
        plt.title('Energy Dependency on Angle Combinations')
        plt.xticks(index + bar_width*3, ('opt', 'optE_HCL', 'optE_C', 'optE_PV', 'optE_tot', '90 deg', '45 deg', '0 deg'))
        plt.legend(loc=0)
        
        plt.tight_layout()
        plt.grid()
        
        
        plt.subplot(2,1,2)
        
        index = np.arange(n_groups)
        bar_width = 0.15
        
        opacity = 0.4
        
        plt.bar(index, DiffH, bar_width,
                         alpha=opacity,
                         color='r',
                         label='H (COP=' + str(usedEfficiencies['H_COP']) + ')')
        
        plt.bar(index+ bar_width, DiffC, bar_width,
                         alpha=opacity,
                         color='b',
                         label='C (COP=' + str(usedEfficiencies['C_COP']) + ')')
                         
        plt.bar(index+ bar_width*2, DiffL, bar_width,
                         alpha=opacity,
                         color='g',
                         label='L (Load=' + str(usedEfficiencies['L_Load']) + ' W/m2)')
                         
                         
        if usedEfficiencies['PV'] == 1 or not monthlyData['changedEfficiency'] :
            plt.bar(index+ bar_width*3, DiffPV, bar_width,
                         alpha=opacity,
                         color='c',
                         label='PV')
        else:
            plt.bar(index+ bar_width*3, DiffPV, bar_width,
                         alpha=opacity,
                         color='c',
                         label='PV (multiplied by ' + str(usedEfficiencies['PV']) + ')')           
                         
        plt.bar(index+ bar_width*4, DiffE_HCL, bar_width,
                         alpha=opacity,
                         color='m',
                         label='E_HCL')
    
        if auxVar['combineResults']:
            plt.bar(index+ bar_width*5, DiffE_tot, bar_width,
                             alpha=opacity,
                             color='k',
                             label='E_tot')
                         
                         
        plt.xlabel('Combinations')
        plt.ylabel('$\Delta$ Energy [kWh]')
        plt.title('Energy Difference Dependency on Angle Combinations')
        plt.xticks(index + bar_width*3, ('opt', 'optE_HCL', 'optE_C', 'optE_PV', 'optE_tot', '90 deg', '45 deg', '0 deg'))
        plt.legend(loc=0)
        
        plt.tight_layout()
        plt.grid()
        plt.show()
        
    else:
        fig = None
        
    # save data to dictionaries
    energy_optHCL = {'H': H_HCL, 'C': C_HCL, 'L': L_HCL, 'E_HCL': E_HCL_HCL, 'E_tot': E_tot_HCL, 'PV': PV_HCL}
    energy_optPV = {'H': H_PV, 'C': C_PV, 'L': L_PV, 'E_HCL': E_HCL_PV, 'E_tot': E_tot_PV, 'PV': PV_PV}
    energy_opttot = {'H': H_tot, 'C': C_tot, 'L': L_tot, 'E_HCL': E_HCL_tot, 'E_tot': E_tot_tot, 'PV': PV_tot}
    energy_90 = {'H': H_90, 'C': C_90, 'L': L_90, 'E_HCL': E_HCL_90, 'E_tot': E_tot_90, 'PV': PV_90}
    energy_45 = {'H': H_45, 'C': C_45, 'L': L_45, 'E_HCL': E_HCL_45, 'E_tot': E_tot_45, 'PV': PV_45}
    energy_0 = {'H': H_0, 'C': C_0, 'L': L_0, 'E_HCL': E_HCL_0, 'E_tot': E_tot_0, 'PV': PV_0}
    tradeoff_results = {'energy_optHCL': energy_optHCL, 'energy_optPV':energy_optPV, 'energy_opttot': energy_opttot, 'energy_90': energy_90, 'energy_45':energy_45, 'energy_0': energy_0,}

    # return the results:    
    return tradeoff_results, fig
    
def compareTotalEnergy25comb(monthlyData, efficiencyChanges, createPlots, tradeoffPeriod):
    
    # assign data:
    H_data = monthlyData['H']
    H_COP_data = monthlyData['efficiencies']['H_COP']
    C_data = monthlyData['C']
    C_COP_data = monthlyData['efficiencies']['C_COP']
    L_data = monthlyData['L']
    L_power_data = monthlyData['efficiencies']['L_Load']
    PV_data = monthlyData['PV']
    PV_eff_data = monthlyData['efficiencies']['PV']


    
    # set changes if demanded:
    if efficiencyChanges['changeEfficiency']:
        H_COP_eval = efficiencyChanges['H_COP']
        C_COP_eval = efficiencyChanges['C_COP']
        L_power_eval = efficiencyChanges['L_Load']
        PV_eff_eval = PV_eff_data*efficiencyChanges['PV']
    else:
        H_COP_eval = H_COP_data
        C_COP_eval = C_COP_data
        L_power_eval = L_power_data
        PV_eff_eval = PV_eff_data
    
    if tradeoffPeriod['enabled']:
        print 'showing tradeoffs for month: ' + str(tradeoffPeriod['month']) + ', hours: ' +  str(tradeoffPeriod['startHour']) +'-' +  str(tradeoffPeriod['endHour']) 
        evalList = create_evalList('monthly', tradeoffPeriod['month'], tradeoffPeriod['startHour'], tradeoffPeriod['endHour'])
        H = H_data[:,evalList]*H_COP_data/H_COP_eval
        C = C_data[:,evalList]*C_COP_data/C_COP_eval
        L = L_data[:,evalList]*L_power_eval/L_power_data
        PV = PV_data[:,evalList]*PV_eff_eval/PV_eff_data
    else:
        print 'showing tradeoffs for the whole year'
        
        H = H_data*H_COP_data/H_COP_eval
        C = C_data*C_COP_data/C_COP_eval
        L = L_data*L_power_eval/L_power_data
        PV = PV_data*PV_eff_eval/PV_eff_data
        
#    if len(evalList[0])>0:
#        print 'there is an evalList'
#        evalList = evalList[0]
#        H = H_data[:,evalList]*H_COP_data/H_COP_eval
#        C = C_data[:,evalList]*C_COP_data/C_COP_eval
#        L = L_data[:,evalList]*L_power_eval/L_power_data
#        PV = PV_data[:,evalList]*PV_eff_eval/PV_eff_data
#    else:
#        print 'there is no evalList or it is empty, results will be shown for the whole year'
#        
#        H = H_data*H_COP_data/H_COP_eval
#        C = C_data*C_COP_data/C_COP_eval
#        L = L_data*L_power_eval/L_power_data
#        PV = PV_data*PV_eff_eval/PV_eff_data
    
    E_HCL = H+C+L
    E_tot = E_HCL+PV
    
    
    Hind = np.argmin(H,axis=0)
    Cind = np.argmin(C,axis=0)
    Lind = np.argmin(L,axis=0)
    PVind = np.argmin(PV,axis=0)
    E_HCLind = np.argmin(E_HCL,axis=0)
    E_totind = np.argmin(E_tot,axis=0)

    H_opt = calculate_sum_for_index(H,Hind)
    H_HCL = calculate_sum_for_index(H,E_HCLind)
    H_C = calculate_sum_for_index(H,Cind)
    H_PV = calculate_sum_for_index(H,PVind)
    H_tot = calculate_sum_for_index(H,E_totind)
    H_90 = calculate_sum_for_index(H,22)
    H_675 = calculate_sum_for_index(H,17)
    H_45 = calculate_sum_for_index(H,12)
    H_225 = calculate_sum_for_index(H,17)
    H_0 = calculate_sum_for_index(H,2)
    
    TotalHbyPos=[H_opt, H_HCL, H_C, H_PV, H_tot, H_90, H_675, H_45, H_225, H_0]
    DiffH = TotalHbyPos-H_opt
    
    C_opt = calculate_sum_for_index(C,Cind)
    C_HCL = calculate_sum_for_index(C,E_HCLind)
    C_C = calculate_sum_for_index(C,Cind)
    C_PV = calculate_sum_for_index(C,PVind)
    C_tot = calculate_sum_for_index(C,E_totind)
    C_90 = calculate_sum_for_index(C,22)
    C_675 = calculate_sum_for_index(C,17)
    C_45 = calculate_sum_for_index(C,12)
    C_225 = calculate_sum_for_index(C,7)
    C_0 = calculate_sum_for_index(C,2)
    
    TotalCbyPos=[C_opt, C_HCL, C_C, C_PV, C_tot, C_90, C_675, C_45, C_225, C_0]
    DiffC = TotalCbyPos - C_opt
    
    L_opt = calculate_sum_for_index(L,Lind)
    L_HCL = calculate_sum_for_index(L,E_HCLind)
    L_C = calculate_sum_for_index(L,Cind)
    L_PV = calculate_sum_for_index(L,PVind)
    L_tot = calculate_sum_for_index(L,E_totind)
    L_90 = calculate_sum_for_index(L,22)
    L_675 = calculate_sum_for_index(L,17)
    L_45 = calculate_sum_for_index(L,12)
    L_225 = calculate_sum_for_index(L,7)
    L_0 = calculate_sum_for_index(L,2)
    
    TotalLbyPos=[L_opt, L_HCL, L_C, L_PV, L_tot, L_90, L_675, L_45, L_225, L_0]
    DiffL = TotalLbyPos - L_opt

    
    PV_opt = calculate_sum_for_index(PV,PVind)
    PV_HCL = calculate_sum_for_index(PV,E_HCLind)
    PV_C = calculate_sum_for_index(PV,Cind)
    PV_PV = calculate_sum_for_index(PV,PVind)
    PV_tot = calculate_sum_for_index(PV,E_totind)
    PV_90 = calculate_sum_for_index(PV,22)
    PV_675 = calculate_sum_for_index(PV,17)
    PV_45 = calculate_sum_for_index(PV,12)
    PV_225 = calculate_sum_for_index(PV,7)
    PV_0 = calculate_sum_for_index(PV,2)
    
    TotalPVbyPos=[PV_opt, PV_HCL, PV_C, PV_PV, PV_tot, PV_90, PV_675, PV_45, PV_225, PV_0]    
    DiffPV = TotalPVbyPos - PV_opt

    
    
    E_HCL_HCL = calculate_sum_for_index(E_HCL,E_HCLind)
    E_HCL_C = calculate_sum_for_index(E_HCL,Cind)
    E_HCL_PV = calculate_sum_for_index(E_HCL,PVind)
    E_HCL_tot = calculate_sum_for_index(E_HCL,E_totind)
    E_HCL_90 = calculate_sum_for_index(E_HCL,22)
    E_HCL_675 = calculate_sum_for_index(E_HCL,17)
    E_HCL_45 = calculate_sum_for_index(E_HCL,12)
    E_HCL_225 = calculate_sum_for_index(E_HCL,7)
    E_HCL_0 = calculate_sum_for_index(E_HCL,2)
    
    TotalE_HCLbyPos=[E_HCL_HCL, E_HCL_HCL, E_HCL_C, E_HCL_PV, E_HCL_tot, E_HCL_90, E_HCL_675, E_HCL_45, E_HCL_225, E_HCL_0]
    DiffE_HCL = TotalE_HCLbyPos - E_HCL_HCL
    
    
    E_tot_HCL = calculate_sum_for_index(E_tot,E_HCLind)
    E_tot_C = calculate_sum_for_index(E_tot,Cind)
    E_tot_PV = calculate_sum_for_index(E_tot,PVind)
    E_tot_tot = calculate_sum_for_index(E_tot,E_totind)
    E_tot_90 = calculate_sum_for_index(E_tot,22)
    E_tot_675 = calculate_sum_for_index(E_tot,17)
    E_tot_45 = calculate_sum_for_index(E_tot,12)
    E_tot_225 = calculate_sum_for_index(E_tot,7)
    E_tot_0 = calculate_sum_for_index(E_tot,2)
    
    TotalE_totbyPos=[E_tot_tot, E_tot_HCL, E_tot_C, E_tot_PV, E_tot_tot, E_tot_90, E_tot_675, E_tot_45, E_tot_225, E_tot_0]
    DiffE_tot = TotalE_totbyPos- E_tot_tot
    
    
    n_groups = 10
    
    fig = plt.figure(figsize=(16, 8))
#    fig, ax = plt.subplots()
    p1 = plt.subplot(2,1,1)
    
    index = np.arange(n_groups)
    bar_width = 0.15
    
    opacity = 0.4
    error_config = {'ecolor': '0.3'}
    
    rects1 = plt.bar(index, TotalHbyPos, bar_width,
                     alpha=opacity,
                     color='r',
                     label='H')
    
    rects2 = plt.bar(index+ bar_width, TotalCbyPos, bar_width,
                     alpha=opacity,
                     color='b',
                     label='C')
                     
    rects3 = plt.bar(index+ bar_width*2, TotalLbyPos, bar_width,
                     alpha=opacity,
                     color='g',
                     label='L')
                     
    rects4 = plt.bar(index+ bar_width*3, TotalPVbyPos, bar_width,
                     alpha=opacity,
                     color='c',
                     label='PV')
                     
    rects5 = plt.bar(index+ bar_width*4, TotalE_HCLbyPos, bar_width,
                     alpha=opacity,
                     color='m',
                     label='E_HCL')
                     
    rects6 = plt.bar(index+ bar_width*5, TotalE_totbyPos, bar_width,
                     alpha=opacity,
                     color='k',
                     label='E_tot')
    
    plt.xlabel('Combinations')
    plt.ylabel('Energy [kWh]')
    plt.title('Energy Dependency on Angle Combinations')
    plt.xticks(index + bar_width*3, ('opt', 'optE_HCL', 'optE_C', 'optE_PV', 'optE_tot', '90 deg', '67.5 deg', '45 deg', '22.5 deg', '0 deg'))
    plt.legend(loc=0)
    
    plt.tight_layout()
    
    
    p2 = plt.subplot(2,1,2)
    
    index = np.arange(n_groups)
    bar_width = 0.15
    
    opacity = 0.4
    error_config = {'ecolor': '0.3'}
    
    rects1 = plt.bar(index, DiffH, bar_width,
                     alpha=opacity,
                     color='r',
                     label='H')
    
    rects2 = plt.bar(index+ bar_width, DiffC, bar_width,
                     alpha=opacity,
                     color='b',
                     label='C')
                     
    rects3 = plt.bar(index+ bar_width*2, DiffL, bar_width,
                     alpha=opacity,
                     color='g',
                     label='L')
                     
    rects4 = plt.bar(index+ bar_width*3, DiffPV, bar_width,
                     alpha=opacity,
                     color='c',
                     label='PV')
                     
    rects5 = plt.bar(index+ bar_width*4, DiffE_HCL, bar_width,
                     alpha=opacity,
                     color='m',
                     label='E_HCL')
                     
    rects6 = plt.bar(index+ bar_width*5, DiffE_tot, bar_width,
                     alpha=opacity,
                     color='k',
                     label='E_tot')
                     
                     
    plt.xlabel('Combinations')
    plt.ylabel('$\Delta$ Energy [kWh]')
    plt.title('Energy Difference Dependency on Angle Combinations')
    plt.xticks(index + bar_width*3, ('opt', 'optE_HCL', 'optE_C', 'optE_PV', 'optE_tot', '90 deg', '67.5 deg', '45 deg', '22.5 deg', '0 deg'))
    plt.legend(loc=0)
    
    plt.tight_layout()
    plt.show()
        
    energy_optHCL = {'H_HCL': H_HCL, 'C_HCL': C_HCL, 'L_HCL': L_HCL, 'E_HCL_HCL': E_HCL_HCL, 'E_tot_HCL': E_tot_HCL, 'PV_HCL': PV_HCL}
    energy_optPV = {'H_PV': H_PV, 'C_PV': C_PV, 'L_PV': L_PV, 'E_HCL_PV': E_HCL_PV, 'E_tot_PV': E_tot_PV, 'PV_PV': PV_PV}
    energy_opttot = {'H_tot': H_tot, 'C_tot': C_tot, 'L_tot': L_tot, 'E_HCL_tot': E_HCL_tot, 'E_tot_tot': E_tot_tot, 'PV_tot': PV_tot}
    tradeoff_results = {'energy_optHCL': energy_optHCL, 'energy_optPV':energy_optPV, 'energy_opttot': energy_opttot}
    return tradeoff_results

#dataType='monthly'
#month=7
#startHour=21
#endHour=22
#
#evalList = []
#evalList = create_evalList(dataType, month, startHour, endHour)
##
##H_COP_data = 4
##H_COP_eval = 4
##C_COP_data = 3
##C_COP_eval = 3
##L_power_data = 11.74    # [W/m^2]
##L_power_eval = 11.74    # [W/m^2]
##PV_eff_data = 0.072     # = 0.08*0.9
##PV_eff_eval = 0.072
#
#tradeoff_results = compareTotalEnergy(monthlyData, efficiencyChanges, createPlots, evalList)


#TotalHeating = np.sum(np.min(H_month, axis=0))
#TotalCooling = np.round(np.sum(np.min(C_month, axis=0)), decimals=1)
#TotalLighting = np.round(np.sum(np.min(L_month, axis=0)), decimals=1)
#TotalEnergy = np.round(np.sum(np.min(E_month, axis=0)), decimals=1)
#TotalPV = np.round(np.sum(np.max(PV_month, axis=0)), decimals=1)
#TotalR = np.round(np.sum(np.max(R_month, axis=0)), decimals=1)
#TotalR_LB = np.round(np.sum(np.max(R_monthlyLB, axis=0)), decimals=1)
#TotalEnergy_withPV = np.round(np.sum(np.min(E_month_withPV, axis=0)), decimals=1)
#TradeoffLosses = np.round(TotalEnergy-TotalLighting-TotalCooling-TotalHeating, decimals=2)

# H = H_month
# C = C_month
# L = L_month
# PV = PV_month
# E = E_month_withPV