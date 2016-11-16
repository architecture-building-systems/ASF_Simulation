import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
import cdecimal as dec
import re as re
import csv
import os, sys
from j_schedulemaker import*
from j_epw_import import*

########################################################Build occupancy schedules from CEA databases and export as .csv
start = full_date(weather_path,1,1)
date = pd.date_range(start, periods=8760, freq='H')

ArchT_df = ArchT_build_df(BuildingData)
ArchT_typologies = ArchT_df.code1.unique()

list_uses = ArchT_typologies

schedules = schedule_maker(date, list_uses)
schedules = zip(*schedules)

occ = schedules[0]
el = schedules[1]
dhw = schedules[2]
pro = schedules[3]

occ_df = pd.DataFrame({'0':range(0,8760)})
el_df = pd.DataFrame({'0':range(0,8760)})
dhw_df = pd.DataFrame({'0':range(0,8760)})
pro_df = pd.DataFrame({'0':range(0,8760)})

for i in range(0,len(occ)):
    occ_df[list(list_uses)[i]] = occ[i]
    el_df[list(list_uses)[i]] = el[i]
    dhw_df[list(list_uses)[i]] = dhw[i]
    pro_df[list(list_uses)[i]] = pro[i]
 
occ_df = occ_df.set_index('0',drop=True)
el_df = el_df.set_index('0',drop=True)
dhw_df = dhw_df.set_index('0',drop=True)
pro_df = pro_df.set_index('0',drop=True)

occ_df.to_csv('schedules_occ.csv')
el_df.to_csv('schedules_el.csv')     
dhw_df.to_csv('schedules_dhw.csv')
pro_df.to_csv('schedules_pro.csv')


#################################################### 
def ArchT_build_df(BuildingData):

    arch = pd.read_excel(archetypes_properties_path,sheetname='THERMAL')
    r = re.compile("([a-zA-Z_]+)")
    m = r.match(arch["Code"][1])
    
    arch["code1"] = pd.DataFrame([r.match(string).groups() for string in arch.Code])
    arch = arch.set_index(['code1'])  
    arch = arch.drop(['SERVERROOM','PARKING','SWIMMING','COOLROOM'])
    arch = arch.reset_index(drop=False)
    arch = arch.drop('Es',axis=1)
    arch = arch.drop('Hs',axis=1)
    arch = arch.drop('U_roof',axis=1)
    arch = arch.drop('U_base',axis=1)
    
    int_loads = pd.read_excel(archetypes_properties_path,sheetname='INTERNAL_LOADS')
    int_loads = int_loads.set_index(['Code'])
    int_loads = int_loads['El_Wm2']
    int_loads = int_loads.reset_index(drop=False)

    T_sp = pd.read_excel(archetypes_properties_path,sheetname='INDOOR_COMFORT')

    b_data = arch.merge(int_loads,how='left', left_on='code1', right_on='Code')
    b_data = b_data.merge(T_sp,how='left', left_on='code1', right_on='Code')
    b_data = b_data.drop('Code_y',axis=1)
    b_data = b_data.drop('Code',axis=1)
    b_data['Tcs_setb'] = b_data['Tcs_setb_C']-b_data['Tcs_set_C']
    b_data['Ths_setb'] = b_data['Ths_set_C']-b_data['Ths_setb_C']
    
    volume = (BuildingData['room_width']/1000)*(BuildingData['room_depth']/1000)*(BuildingData['room_height']/1000)
    b_data['ACH'] = b_data['Ve_lps']*3.6/volume
    
    #Assign values for Cm from ISO13790:2008, Table 12, based on archetypes
    th_mass = b_data['th_mass']
    c_m = []
    for i in range(0,len(th_mass)):
        if th_mass[i] == "T1":
            c_m.append(110*10**3) #Light
        elif th_mass[i] == "T2":
            c_m.append(165 * 10**3) #Medium
        elif th_mass[i] == "T3":
            c_m.append(260*10**3) #Heavy
    b_data['c_m_A_f'] = pd.DataFrame(c_m)
    return b_data

#Create dictionaries for Archetypes:
def At_Dict_Building_properties(b_data):
 
    b_data_dict = b_data[['Code_x',
                          'El_Wm2',
                          'U_wall',
                          'U_win',
                          'Ths_set_C',
                          'Ths_setb',
                          'Tcs_set_C',
                          'Tcs_setb',
                          'ACH',
                          'c_m_A_f']]
    
    b_data_dict = b_data_dict.rename(index=str,columns={'Code_x':'Code',
                                                        'El_Wm2':'lighting_load',
                                                        'U_win':'U_w',
                                                        'c_m_A_f':'c_m_A_f',
                                                        'U_wall':'U_em',
                                                        'Ths_set_C':'theta_int_h_set',
                                                        'Tcs_set_C':'theta_int_c_set'})
    b_data_dict = b_data_dict.set_index(['Code'])
    b_dict = b_data_dict.to_dict(orient='index')
    return b_dict

def At_Dict_Simulation_Options(b_data):
    b_data_dict = b_data[['Code_x',
                          'El_Wm2',
                          'U_wall',
                          'U_win',
                          'Ths_set_C',
                          'Ths_setb',
                          'Tcs_set_C',
                          'Tcs_setb',
                          'ACH_vent_m3ph',
                          'c_m_A_f']]

#ArchT_df = ArchT_build_df(BuildingData)
#ArchT_dict = At_Dict_Building_properties(ArchT_df)
#ArchT_typologies = ArchT_df.code1.unique()


