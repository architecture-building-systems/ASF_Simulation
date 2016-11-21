#epw_reader adapted from https://github.com/architecture-building-systems/CEAforArcGIS/blob/master/cea/utilities/epwreader.py

import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
#import cdecimal as dec
import re as re
import csv
import os, sys

weather_path = "C:\Users\Zghiru\Documents\GitHub\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\data\Zuerich_Kloten_2005\Zuerich_Kloten_2005.epw"
occupancy_path = 'C:\Users\Zghiru\Documents\GitHub\RC_BuildingSimulator\Justin_Semseter_Project\data\Occupancy_COM.csv'
radiation_path = r'C:\Users\Zghiru\Documents\GitHub\RC_BuildingSimulator\Justin_Semseter_Project\data\radiation_Building_Zh.csv'

epw_labels = ['year', 'month', 'day', 'hour', 'minute', 'datasource', 'drybulb_C', 'dewpoint_C', 'relhum_percent',
                   'atmos_Pa', 'exthorrad_Whm2', 'extdirrad_Whm2', 'horirsky_Whm2', 'glohorrad_Whm2',
                   'dirnorrad_Whm2', 'difhorrad_Whm2', 'glohorillum_lux', 'dirnorillum_lux','difhorillum_lux',
                   'zenlum_lux', 'winddir_deg', 'windspd_ms', 'totskycvr_tenths', 'opaqskycvr_tenths', 'visibility_km',
                   'ceiling_hgt_m', 'presweathobs', 'presweathcodes', 'precip_wtr_mm', 'aerosol_opt_thousandths',
                   'snowdepth_cm', 'days_last_snow', 'Albedo', 'liq_precip_depth_mm', 'liq_precip_rate_Hour']


def epw_reader(weather_path):
    start = full_date(weather_path,1,1)
    result = pd.read_csv(weather_path, skiprows=8, header=None, names=epw_labels).drop('datasource', axis=1)
    result['dayofyear'] = pd.date_range(start, periods=8760, freq='H').dayofyear  
    result['date'] = pd.date_range(start, periods=8760, freq='H')
    #esult['ratio_diffhout'] = result['difhorrad_Whm2']/result['glohorrad_Whm2']
    result['index'] = result.index
    return result

def radiation(radiation_path):
    df = pd.read_csv(radiation_path,header=None)
    df = df.T
    return df

def full_date(weather_path,month,day):
    year = pd.read_csv(weather_path, skiprows=8, header=None, names=epw_labels)['year']
    return pd.datetime(year[1],month,day)

def epw_year(weather_path):
    df = epw_reader(weather_path)  
    df['date'] = pd.to_datetime(df['date'])
    return df['year'][0]

def epw_data(field = []): 
    series = epw_reader(weather_path) 
    field.insert(0,'date')
    series = series[field]
    return series 

def date_range(startdate,enddate,series):
    year = epw_year(weather_path)
    start = str(startdate)+ '/' + str(year)+' 00:00:00'
    start = pd.to_datetime(start)
    end =  str(enddate)+ '/' + str(year)+' 00:00:00'
    end = pd.to_datetime(end)

    series['index'] = series.index
    series = series.set_index(['date'],drop=False)  
    series = series[start:end]
    series = series.set_index(['index']) 
    return series

def resample(dataframe,dt):    
    if dt > 1:
        resample_value = str(dt)+'H'
    elif dt < 1:
        resample_value = str(int(dt*60))+'Min'     
    elif dt == 1:
        resample_value = '1H'
    dataframe = dataframe.set_index(['date']) #use date as index. this allows for time resampling
    dataframe = dataframe.resample(resample_value).mean()  
    dataframe = dataframe.interpolate()   
    dataframe = dataframe.reset_index(drop=False)     
    return dataframe

def occupancy(occupancy_path):
    df = pd.read_csv(occupancy_path, header=0,keep_default_na=False)[:8760]
    occupancy = pd.DataFrame({'occupancy':df['People']})  
    return occupancy