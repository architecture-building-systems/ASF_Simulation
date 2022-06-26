import os, sys
from turtle import position
import numpy as np
import time
import pandas as pd

paths = {}
print os.path.dirname(__file__)
paths['main'] = os.path.abspath(os.path.dirname(__file__))
paths['CO2_electricity'] = os.path.join(paths['main'],'CO2_electricity')

CO2_electricty_data_df = pd.read_csv(os.path.join(paths['CO2_electricity'], 'CH_year_2015_2016.csv'), sep = ';')  
CO2_electricty_data_df['Time reference [GMT+1]'] = pd.to_datetime(CO2_electricty_data_df['Time reference [GMT+1]'])
#CO2_data_dic = CO2_electricty_data_df.to_dict()['GWP [kg CO2eq/kWh]']
CO2_data_hourly = CO2_electricty_data_df['GWP [kg CO2eq/kWh]'].values
#print CO2_data_hourly
print type(CO2_data_hourly)
