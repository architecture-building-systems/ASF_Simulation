import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
from j_paths import PATHS
import re as re
import csv
import os, sys
from j_schedulemaker import*
from j_epw_import_tools import*

paths = PATHS()

def full_date(weather_path,month,day):
		year = pd.read_csv(weather_path, skiprows=8, header=None, names=epw_labels)['year']
		return pd.datetime(year[1],month,day)

def build_schedules(BuildingData):
	start = full_date(paths['Weatherfile'],1,1)
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

	#occ_m2p = gross floor area per person [m2/p]
	occ_m2p = ArchT_df.drop_duplicates('code1')
	occ_m2p = occ_m2p.set_index('code1')
	occ_m2p = occ_m2p.Occ_m2p
	#occ_pm2 = persons per m2 in a given occupancy type
	occ_pm2 = 1/occ_m2p
	#set path for export
 	os.mkdir(paths['data'])
	#Iterate through each occupancy type
	for column in occ_df:
			# occ (probability distribution of occupancy) * persons per m2 = probable number of people per m2
			occ1 = pd.concat([occ_df[column]],axis=1, keys=['People'])*occ_pm2[column]
			occ1['People'].to_csv('schedules_occ_%s.csv'%column,header=True, index = False)
			el1 =pd.concat([el_df[column]],axis=1, keys=['People'])*occ_pm2[column]
			el1['People'].to_csv('schedules_el_%s.csv'%column, header=True, index = False)
		
