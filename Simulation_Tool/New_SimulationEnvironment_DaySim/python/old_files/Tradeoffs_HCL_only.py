# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 12:27:01 2016

@author: Assistenz
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 12:11:49 2016

Tradeoff Funtions

@author: Assistenz
"""
import numpy as np
import matplotlib.pyplot as plt


def calculate_sum_for_index(X,Xind):
    Xsum = []
    
    if not np.shape(Xind)==():
        for i in range(len(Xind)):
            Xsum.append(X[Xind[i]][i])
            sumX = np.sum(Xsum)
    else:
        sumX = np.sum(X[Xind])
        
    return sumX
def create_evalList(dataType, month, startHour, endHour):
    """
    example: \n
    create_evalList('monthly', 6, 12, 13) \n
    outputs a list which corresponds to the monthly data of june for hours between 11:00 and 13:00. 
    Note that month, startHour and endHour correspond to a counter value that starts with 1.
    """
    if dataType == 'monthly':
        evalList=[]
        for i in range(endHour-(startHour-1)):
            evalList.append((month-1)*24 + startHour - 1 + i)
    else:
        raise ValueError("dataType: "+str(dataType)+" not (yet) implemented")
        
    return evalList
    
def compareTotalEnergyHCL(H_data, H_COP_data, H_COP_eval, C_data, C_COP_data, C_COP_eval, L_data, L_power_data, L_power_eval, indices, *evalList):
    
    if len(evalList[0])>0:
        print 'there is an evalList'
        evalList = evalList[0]
        H = H_data[:,evalList]*H_COP_data/H_COP_eval
        C = C_data[:,evalList]*C_COP_data/C_COP_eval
        L = L_data[:,evalList]*L_power_eval/L_power_data
    else:
        print 'there is no evalList or it is empty, results will be shown for the whole year'
        
        H = H_data*H_COP_data/H_COP_eval
        C = C_data*C_COP_data/C_COP_eval
        L = L_data*L_power_eval/L_power_data
    
    E_HCL = H+C+L

    
    Hind = np.argmin(H,axis=0)
    Cind = np.argmin(C,axis=0)
    Lind = np.argmin(L,axis=0)
    E_HCLind = np.argmin(E_HCL,axis=0)
    
    H_opt = calculate_sum_for_index(H,Hind)
    H_HCL = calculate_sum_for_index(H,E_HCLind)
    H_C = calculate_sum_for_index(H,Cind)
    H_90 = calculate_sum_for_index(H,22)
    H_675 = calculate_sum_for_index(H,17)
    H_45 = calculate_sum_for_index(H,12)
    H_225 = calculate_sum_for_index(H,17)
    H_0 = calculate_sum_for_index(H,2)
    
    TotalHbyPos=[H_opt, H_HCL, H_C, H_90, H_675, H_45, H_225, H_0]
    DiffH = TotalHbyPos-H_opt
    
    C_opt = calculate_sum_for_index(C,Cind)
    C_HCL = calculate_sum_for_index(C,E_HCLind)
    C_C = calculate_sum_for_index(C,Cind)
    C_90 = calculate_sum_for_index(C,indices['90'])
    C_675 = calculate_sum_for_index(C,indices['67.5'])
    C_45 = calculate_sum_for_index(C,indices['45'])
    C_225 = calculate_sum_for_index(C,indices['22.5'])
    C_0 = calculate_sum_for_index(C,indices['0'])
    
    TotalCbyPos=[C_opt, C_HCL, C_C, C_90, C_675, C_45, C_225, C_0]
    DiffC = TotalCbyPos - C_opt
    
    L_opt = calculate_sum_for_index(L,Lind)
    L_HCL = calculate_sum_for_index(L,E_HCLind)
    L_C = calculate_sum_for_index(L,Cind)
    L_90 = calculate_sum_for_index(L,22)
    L_675 = calculate_sum_for_index(L,17)
    L_45 = calculate_sum_for_index(L,indices['45'])
    L_225 = calculate_sum_for_index(L,7)
    L_0 = calculate_sum_for_index(L,2)
    
    TotalLbyPos=[L_opt, L_HCL, L_C, L_90, L_675, L_45, L_225, L_0]
    DiffL = TotalLbyPos - L_opt

    
    
    E_HCL_HCL = calculate_sum_for_index(E_HCL,E_HCLind)
    E_HCL_C = calculate_sum_for_index(E_HCL,Cind)
    E_HCL_90 = calculate_sum_for_index(E_HCL,22)
    E_HCL_675 = calculate_sum_for_index(E_HCL,17)
    E_HCL_45 = calculate_sum_for_index(E_HCL,indices['45'])
    E_HCL_225 = calculate_sum_for_index(E_HCL,7)
    E_HCL_0 = calculate_sum_for_index(E_HCL,2)
    
    TotalE_HCLbyPos=[E_HCL_HCL, E_HCL_HCL, E_HCL_C, E_HCL_90, E_HCL_675, E_HCL_45, E_HCL_225, E_HCL_0]
    DiffE_HCL = TotalE_HCLbyPos - E_HCL_HCL
        
    n_groups = len(TotalE_HCLbyPos)
    
#    means_men = (20, 35, 30, 35, 27)
#    std_men = (2, 3, 4, 1, 2)
#    
#    means_women = (25, 32, 34, 20, 25)
#    std_women = (3, 5, 2, 3, 3)
    
    fig, ax = plt.subplots()
    p1 = plt.subplot(2,1,1)
    
    index = np.arange(n_groups)
    bar_width = 0.15
    
    opacity = 0.4
    error_config = {'ecolor': '0.3'}
    
    rects1 = plt.bar(index, TotalHbyPos, bar_width,
                     alpha=opacity,
                     color='r',
    #                 yerr=std_men,
    #                 error_kw=error_config,
                     label='H')
    
    rects2 = plt.bar(index+ bar_width, TotalCbyPos, bar_width,
                     alpha=opacity,
                     color='b',
    #                 yerr=std_men,
    #                 error_kw=error_config,
                     label='C')
                     
    rects3 = plt.bar(index+ bar_width*2, TotalLbyPos, bar_width,
                     alpha=opacity,
                     color='g',
    #                 yerr=std_men,
    #                 error_kw=error_config,
                     label='L')
                                          
    rects5 = plt.bar(index+ bar_width*4, TotalE_HCLbyPos, bar_width,
                     alpha=opacity,
                     color='m',
    #                 yerr=std_men,
    #                 error_kw=error_config,
                     label='E_HCL')
                                          
    #rects2 = plt.bar(index + bar_width, means_women, bar_width,
    #                 alpha=opacity,
    #                 color='r',
    #                 yerr=std_women,
    #                 error_kw=error_config,
    #                 label='Women')
    
    plt.xlabel('Combinations')
    plt.ylabel('Energy [kWh]')
    plt.title('Energy Dependency on Angle Combinations')
    plt.xticks(index + bar_width*3, ('opt', 'optE_HCL', 'optE_C', '90 deg', '67.5 deg', '45 deg', '22.5 deg', '0 deg'))
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
    #                 yerr=std_men,
    #                 error_kw=error_config,
                     label='H')
    
    rects2 = plt.bar(index+ bar_width, DiffC, bar_width,
                     alpha=opacity,
                     color='b',
    #                 yerr=std_men,
    #                 error_kw=error_config,
                     label='C')
                     
    rects3 = plt.bar(index+ bar_width*2, DiffL, bar_width,
                     alpha=opacity,
                     color='g',
    #                 yerr=std_men,
    #                 error_kw=error_config,
                     label='L')
                     
    rects5 = plt.bar(index+ bar_width*4, DiffE_HCL, bar_width,
                     alpha=opacity,
                     color='m',
    #                 yerr=std_men,
    #                 error_kw=error_config,
                     label='E_HCL')
                     
    #rects2 = plt.bar(index + bar_width, means_women, bar_width,
    #                 alpha=opacity,
    #                 color='r',
    #                 yerr=std_women,
    #                 error_kw=error_config,
    #                 label='Women')
    
    plt.xlabel('Combinations')
    plt.ylabel('$\Delta$ Energy [kWh]')
    plt.title('Energy Difference Dependency on Angle Combinations')
    plt.xticks(index + bar_width*3, ('opt', 'optE_HCL', 'optE_C', '90 deg', '67.5 deg', '45 deg', '22.5 deg', '0 deg'))
    plt.legend(loc=0)
    
    plt.tight_layout()
    plt.show()
        
    energy_optHCL = {'H_HCL': H_HCL, 'C_HCL': C_HCL, 'L_HCL': L_HCL, 'E_HCL_HCL': E_HCL_HCL}
    energy_45 = {'H_45': H_45, 'C_45': C_45, 'L_45': L_45, 'E_HCL_45': E_HCL_45}
    tradeoff_results = {'energy_optHCL': energy_optHCL, 'energy_45': energy_45}
    return tradeoff_results

dataType='monthly'
month=7
startHour=21
endHour=21

evalList = []
#evalList = create_evalList(dataType, month, startHour, endHour)
#
H_COP_data = 4
H_COP_eval = 4
C_COP_data = 3
C_COP_eval = 3
L_power_data = 11.74    # [W/m^2]
L_power_eval = 11.74    # [W/m^2]
#indices = {'0':0, '22.5':0, '45':171, '67.5':0, '90':0}
indices = {'0':0, '22.5':0, '45':18, '67.5':0, '90':0}

tradeoff_results2 = compareTotalEnergyHCL(H, H_COP_data, H_COP_eval, C, C_COP_data, C_COP_eval, L, L_power_data, L_power_eval, indices, evalList)


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