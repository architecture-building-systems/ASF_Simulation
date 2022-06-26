"""
created: 05.05.2022
Jasmine de Riedmatten


Compute the self consumtion of electricity. If production and demand occur at the same time, cover the demande with the produced electricity. 
If the production is higher than the demand, export the electricity to the grid. 
If the production is smaller than the demand, import electricity from the grid.

"""

import os, sys
from turtle import position
import numpy as np
import time
import pandas as pd


def computeSelfConsumption(SimulationData_dict):
	Energy_Flow = {}
	Energy_Flow['import_elec'] = {}
	Energy_Flow['import_fossil'] = {}
	Energy_Flow['export_elec'] = {}
	Energy_Flow['total_consumption_elec'] = {}
	Energy_Flow['total_production_PV'] = {}
	Energy_Flow['self_consumption_elec'] = {}
	Energy_Flow['Elec_tot'] = {}

	for hour_of_year in range(0,8760):
		Energy_Flow['Elec_tot'][hour_of_year] = SimulationData_dict['H_elec'][hour_of_year] + SimulationData_dict['L'][hour_of_year] + SimulationData_dict['C'][hour_of_year] + SimulationData_dict['AE'][hour_of_year]
		if type(SimulationData_dict['PV'][hour_of_year]) is str:
			SimulationData_dict['PV'][hour_of_year] = SimulationData_dict['PV'][hour_of_year].replace("[", "")
			SimulationData_dict['PV'][hour_of_year] = SimulationData_dict['PV'][hour_of_year].replace("]", "")
			SimulationData_dict['PV'][hour_of_year] = float(SimulationData_dict['PV'][hour_of_year])

		Energy_Flow['import_fossil'][hour_of_year] = SimulationData_dict['H_fossil'][hour_of_year]
		Energy_Flow['total_consumption_elec'][hour_of_year] = Energy_Flow['Elec_tot'][hour_of_year]
		Energy_Flow['total_production_PV'][hour_of_year] = SimulationData_dict['PV'][hour_of_year]
		
		if (Energy_Flow['Elec_tot'][hour_of_year] - float(SimulationData_dict['PV'][hour_of_year])) <= 0:
			Energy_Flow['import_elec'][hour_of_year] = 0
			Energy_Flow['export_elec'][hour_of_year] = -float(Energy_Flow['Elec_tot'][hour_of_year] - SimulationData_dict['PV'][hour_of_year])
			Energy_Flow['self_consumption_elec'][hour_of_year] = Energy_Flow['Elec_tot'][hour_of_year]
		else: 
			Energy_Flow['import_elec'][hour_of_year] = float(Energy_Flow['Elec_tot'][hour_of_year] - SimulationData_dict['PV'][hour_of_year])
			Energy_Flow['export_elec'][hour_of_year] = 0
			Energy_Flow['self_consumption_elec'][hour_of_year] = SimulationData_dict['PV'][hour_of_year]
			
	Energy_Flow_df = pd.DataFrame(Energy_Flow)

	return Energy_Flow_df


def monthlyAndYearlyFLows(Energy_Flow_df): # prepareResultsSelfConsumption(flow_elec_df):
	from prepareData_mauro import sum_monthly
	
	monthlyData = {}
	totalMonthlyData = {}
	yearlyData = {}

	#in kWh/DaysPerMonth
	monthlyData['total_consumption_elec'] = sum_monthly(X = np.array(Energy_Flow_df['total_consumption_elec'] *0.001)) #W
	monthlyData['import_elec'] = sum_monthly(X = np.array(Energy_Flow_df['import_elec'] *0.001)) #W
	monthlyData['export_elec'] = sum_monthly(X = np.array(Energy_Flow_df['export_elec'] *0.001)) #W
	monthlyData['self_consumption_elec'] = sum_monthly(X = np.array(Energy_Flow_df['self_consumption_elec'] *0.001)) #W
	monthlyData['total_production_PV'] = sum_monthly(X = np.array(Energy_Flow_df['total_production_PV'] *0.001)) #W
	monthlyData['import_fossil'] = sum_monthly(X = np.array(Energy_Flow_df['import_fossil'] *0.001)) #W

	#in kWh per month
	totalMonthlyData['total_consumption_elec'] ={}
	totalMonthlyData['self_consumption_elec'] = {}
	totalMonthlyData['total_production_PV'] = {}
	totalMonthlyData['import_elec'] = {}
	totalMonthlyData['export_elec'] = {}
	totalMonthlyData['import_fossil'] = {}

	for month in range(1, 13): 
		totalMonthlyData['total_consumption_elec'][month] = 0
		totalMonthlyData['self_consumption_elec'][month] = 0
		totalMonthlyData['total_production_PV'][month] = 0
		totalMonthlyData['import_elec'][month] = 0
		totalMonthlyData['export_elec'][month] = 0
		totalMonthlyData['import_fossil'][month] = 0

	monthi = 0
	for hour in range(len(monthlyData['total_consumption_elec'])):
		if hour%24 == 0: 
			monthi+=1
		totalMonthlyData['total_consumption_elec'][monthi] += monthlyData['total_consumption_elec'][hour] #W
		totalMonthlyData['self_consumption_elec'][monthi] += monthlyData['self_consumption_elec'][hour] #W
		totalMonthlyData['total_production_PV'][monthi] += monthlyData['total_production_PV'][hour] #W
		totalMonthlyData['import_elec'][monthi] += monthlyData['import_elec'][hour] #W
		totalMonthlyData['export_elec'][monthi] += monthlyData['export_elec'][hour] #W
		totalMonthlyData['import_fossil'][monthi] += monthlyData['import_fossil'][hour] #W
		

	#in kWh/year
	yearlyData['total_consumption_elec'] =  monthlyData['total_consumption_elec'].sum() #W
	yearlyData['self_consumption_elec'] =  monthlyData['self_consumption_elec'].sum() ##W
	yearlyData['total_production_PV'] =  monthlyData['total_production_PV'].sum() #W
	yearlyData['import_elec'] =  monthlyData['import_elec'].sum()  #W
	yearlyData['export_elec'] =  monthlyData['export_elec'].sum()  #W
	yearlyData['import_fossil'] =  monthlyData['import_fossil'].sum()  #W
	#totalMonthlyData_df = pd.DataFrame(totalMonthlyData)

	monthlyData['total_consumption_elec'] = monthlyData['total_consumption_elec'].tolist() #W
	monthlyData['import_elec'] = monthlyData['import_elec'].tolist() #W
	monthlyData['export_elec'] = monthlyData['export_elec'].tolist()#W
	monthlyData['self_consumption_elec'] = monthlyData['self_consumption_elec'].tolist() #W
	monthlyData['total_production_PV'] = monthlyData['total_production_PV'].tolist() #W
	monthlyData['import_fossil'] = monthlyData['import_fossil'].tolist() #W

	

	return monthlyData, totalMonthlyData, yearlyData


def impacts_energy_flows(paths, monthlyData):
	from prepareData_mauro_static import average_monthly

	impacts_electricty_data_df = pd.read_csv(os.path.join(paths['CO2_electricity'], 'CH_year_2015_2016.csv'), sep = ';') #kg CO2-eq per kWh

	hourly_impact_el = {}
	hourly_impact_el['GWP'] = impacts_electricty_data_df['GWP [kg CO2eq/kWh]'].values
	hourly_impact_el['CED'] = impacts_electricty_data_df['CED [Mjeq/kWh]'].values
	hourly_impact_el['CEDnr'] = impacts_electricty_data_df['CEDnr [Mjeq/kWh]'].values

	av_hourly_impact_el = {}
	av_hourly_impact_el['GWP']=average_monthly(hourly_impact_el['GWP'])
	av_hourly_impact_el['CED']=average_monthly(hourly_impact_el['CED'])
	av_hourly_impact_el['CEDnr']=average_monthly(hourly_impact_el['CEDnr'])

	import_elec_monthly = monthlyData['import_elec']
	export_elec_monthly = monthlyData['export_elec']

	av_monthly_impact_el = {}
	av_monthly_impact_el['GWP'] = {}
	av_monthly_impact_el['CED'] = {}
	av_monthly_impact_el['CEDnr'] = {}

	hourlyImpactFlows = {}
	monthlyImpactFlows = {}
	yearlyImpactFlows = {}

	hourlyImpactFlows['GWP_imports'] = {}
	hourlyImpactFlows['GWP_exports'] = {}
	hourlyImpactFlows['CED_imports'] = {}
	hourlyImpactFlows['CED_exports'] = {}
	hourlyImpactFlows['CEDnr_imports'] = {}
	hourlyImpactFlows['CEDnr_exports'] = {}

	monthlyImpactFlows['GWP_imports'] = {}
	monthlyImpactFlows['GWP_exports'] = {}
	monthlyImpactFlows['CED_imports'] = {}
	monthlyImpactFlows['CED_exports'] = {}
	monthlyImpactFlows['CEDnr_imports'] = {}
	monthlyImpactFlows['CEDnr_exports'] = {}

	yearlyImpactFlows['GWP_imports'] = 0
	yearlyImpactFlows['GWP_exports'] = 0
	yearlyImpactFlows['CED_imports'] = 0
	yearlyImpactFlows['CED_exports'] = 0
	yearlyImpactFlows['CEDnr_imports'] = 0
	yearlyImpactFlows['CEDnr_exports'] = 0

	for hour in range(len(av_hourly_impact_el['GWP'])):
		hourlyImpactFlows['GWP_imports'][hour] = av_hourly_impact_el['GWP'][hour]*import_elec_monthly[hour]
		hourlyImpactFlows['CED_imports'][hour] = av_hourly_impact_el['CED'][hour]*import_elec_monthly[hour]
		hourlyImpactFlows['CEDnr_imports'][hour] = av_hourly_impact_el['CEDnr'][hour]*import_elec_monthly[hour]
		hourlyImpactFlows['GWP_exports'][hour] = av_hourly_impact_el['GWP'][hour] * export_elec_monthly[hour]
		hourlyImpactFlows['CED_exports'][hour] = av_hourly_impact_el['CED'][hour] * export_elec_monthly[hour]
		hourlyImpactFlows['CEDnr_exports'][hour] = av_hourly_impact_el['CEDnr'][hour] * export_elec_monthly[hour]
		
	for month in range(1, 13): 
		av_monthly_impact_el['GWP'][month] = 0
		av_monthly_impact_el['CED'][month] = 0
		av_monthly_impact_el['CEDnr'][month] = 0

		monthlyImpactFlows['GWP_imports'][month] = 0
		monthlyImpactFlows['CED_imports'][month] = 0
		monthlyImpactFlows['CEDnr_imports'][month] = 0
		monthlyImpactFlows['GWP_exports'][month] = 0
		monthlyImpactFlows['CED_exports'][month] = 0
		monthlyImpactFlows['CEDnr_exports'][month] = 0

	monthi = 0
	for hour in range(len(hourlyImpactFlows['GWP_imports'])):
		if hour%24 == 0:
			monthi+=1

		monthlyImpactFlows['GWP_imports'][monthi] += hourlyImpactFlows['GWP_imports'][hour]
		monthlyImpactFlows['CED_imports'][monthi] += hourlyImpactFlows['CED_imports'][hour]
		monthlyImpactFlows['CEDnr_imports'][monthi] += hourlyImpactFlows['CEDnr_imports'][hour]
		monthlyImpactFlows['GWP_exports'][monthi] += hourlyImpactFlows['GWP_exports'][hour]
		monthlyImpactFlows['CED_exports'][monthi] += hourlyImpactFlows['CED_exports'][hour]
		monthlyImpactFlows['CEDnr_exports'][monthi] += hourlyImpactFlows['CEDnr_exports'][hour]

		av_monthly_impact_el['GWP'][monthi] += av_hourly_impact_el['GWP'][hour]
		av_monthly_impact_el['CED'][monthi] += av_hourly_impact_el['CED'][hour]
		av_monthly_impact_el['CEDnr'][monthi] += av_hourly_impact_el['CEDnr'][hour]


	for month in range(1, 13):
		av_monthly_impact_el['GWP'][month] = av_monthly_impact_el['GWP'][month]/24
		av_monthly_impact_el['CED'][month] = av_monthly_impact_el['CED'][month]/24
		av_monthly_impact_el['CEDnr'][month] = av_monthly_impact_el['CEDnr'][month]/24

		yearlyImpactFlows['GWP_imports'] += monthlyImpactFlows['GWP_imports'][month]
		yearlyImpactFlows['GWP_exports'] += monthlyImpactFlows['GWP_exports'][month]
		yearlyImpactFlows['CED_imports'] += monthlyImpactFlows['CED_imports'][month]
		yearlyImpactFlows['CED_exports'] += monthlyImpactFlows['CED_exports'][month]
		yearlyImpactFlows['CEDnr_imports'] += monthlyImpactFlows['CEDnr_imports'][month]
		yearlyImpactFlows['CEDnr_exports'] += monthlyImpactFlows['CEDnr_exports'][month]

	return monthlyImpactFlows, av_monthly_impact_el, yearlyImpactFlows


def plotCO2(totalMonthlyData, FloorArea):
	import matplotlib.pyplot as plt 
	
	totalMonthlyData_df = pd.DataFrame(totalMonthlyData)
	totalMonthlyData_df = totalMonthlyData_df.div(FloorArea)

	#totalMonthlyData_df = totalMonthlyData_df.rename(columns = {'self_elec':'self-consumption','consumed_elec':'total consumption','import_elec':'imported electricity', 'export_elec':'exported electricity', 'self_prod':'PV production'})
	#bar = totalMonthlyData_df.plot(kind='bar', title= 'electricity flows', figsize = (16, 8) )
	#bar.set_ylabel('kWh/month')
	#fig = bar[0].get_figure()
	#labels = [1,2,3,4,5,6,7,8,9,10,11,12]
	fig = plt.figure(figsize=(16, 8))
	#totalMonthlyData_df[['self_elec', 'import_elec']].plot.bar(stacked=True, width = 0.1, position=-1, ax=ax, alpha=0.7)
	#totalMonthlyData_df[['self_prod', 'export_elec']].plot.bar(stacked=True, width = 0.1, position=1, ax=ax, alpha=0.7)

	"""
	totalMonthlyData_df['total_consumption_elec'].plot.bar(width = 0.3, color = 'green', position=0, legend = 'self-consumption')
	totalMonthlyData_df['import_elec'].plot.bar( width = 0.3, color = 'orange', position=0, bottom = totalMonthlyData_df['self-consumption'], legend='imported electricity')
	totalMonthlyData_df['total_production_PV'].plot.bar(width = 0.3, color = 'yellow', position=-1, legend='PV production')
	totalMonthlyData_df['export_elec'].plot.bar(width = 0.3, color = 'blue',position=-1, bottom = totalMonthlyData_df['PV production'], legend='exported electricity')"""
	plt.axhline(0, color='k', linewidth=0.8)
	totalMonthlyData_df['export_elec']=-totalMonthlyData_df['export_elec']
	totalMonthlyData_df['self_consumption_elec'].plot.bar(width = 0.3, color = 'orange', position=0, label = 'self-consumption')
	totalMonthlyData_df['import_elec'].plot.bar( width = 0.3, color = 'tomato', position=0, bottom = totalMonthlyData_df['self_consumption_elec'], label='imported electricity')
	totalMonthlyData_df['import_fossil'].plot.bar( width = 0.3, color = 'silver', position=0, bottom = totalMonthlyData_df['import_elec']+totalMonthlyData_df['self_consumption_elec'], label='imported fossil energy')
	totalMonthlyData_df['export_elec'].plot.bar(width = 0.3, color = 'royalblue',position=0, label='exported electricity')
	plt.legend()
	plt.ylabel("kWh/m2 per month")
	plt.xlabel('Month')
	plt.title('{}\nelectricity flows'.format(FolderName))
	#plt.show()
	return fig #bar

def plotAver_CO2(monthlyAvCO2): 
	import matplotlib.pyplot as plt

	fig= plt.figure(figsize = (16, 8))
	month = np.arange(1, 13)
	width = 0.25
	average = []
	for i in monthlyAvCO2['GWP']: 
		average.append(monthlyAvCO2['GWP'][i])


	plt.bar(month, average ,width,  align='center', color = 'orange', label='Averaged CO2 content el. mix')
	plt.ylabel("kg CO2-eq/month")
	plt.title('Averaged CO2 content el. mix')
	plt.xlabel("Month of the year")
	plt.show()
	#plt.plot(month, list(monthlyAvCO2), kind = 'bar', color = 'orange', label='Averaged CO2 content el. mix')

	return fig #bar

def plotFlowElec(Energy_Flow_df, monthlyData, yearlyData, totalMonthlyData, FloorArea):
	import matplotlib.pyplot as plt
	
	"""
	plt.subplot(2,3,1)
	plt.plot(monthlyData['self_elec'])
	plt.plot(monthlyData['import_elec'])
	plt.plot(monthlyData['export_elec'])

	plt.subplot(2,3,2)"""
	
	totalMonthlyData_df = pd.DataFrame(totalMonthlyData)
	totalMonthlyData_df = totalMonthlyData_df.div(FloorArea)

	#totalMonthlyData_df = totalMonthlyData_df.rename(columns = {'self_elec':'self-consumption','consumed_elec':'total consumption','import_elec':'imported electricity', 'export_elec':'exported electricity', 'self_prod':'PV production'})
	"""bar = totalMonthlyData_df.plot(kind='bar', title= 'electricity flows', figsize = (16, 8) )
	bar.set_ylabel('kWh/month')"""
	#fig = bar[0].get_figure()
	#labels = [1,2,3,4,5,6,7,8,9,10,11,12]
	fig = plt.figure(figsize=(16, 8))
	"""totalMonthlyData_df[['self_elec', 'import_elec']].plot.bar(stacked=True, width = 0.1, position=-1, ax=ax, alpha=0.7)
	totalMonthlyData_df[['self_prod', 'export_elec']].plot.bar(stacked=True, width = 0.1, position=1, ax=ax, alpha=0.7)"""


	"""totalMonthlyData_df['self_elec'].plot.bar(width = 0.3, color = 'green', position=0, legend = 'self-consumption')
	totalMonthlyData_df['import_elec'].plot.bar( width = 0.3, color = 'orange', position=0, bottom = totalMonthlyData_df['self-consumption'], legend='imported electricity')
	totalMonthlyData_df['self_prod'].plot.bar(width = 0.3, color = 'yellow', position=-1, legend='PV production')
	totalMonthlyData_df['export_elec'].plot.bar(width = 0.3, color = 'blue',position=-1, bottom = totalMonthlyData_df['PV production'], legend='exported electricity')"""
	plt.axhline(0, color='k', linewidth=0.8)
	totalMonthlyData_df['export_elec']=-totalMonthlyData_df['export_elec']
	totalMonthlyData_df['self_consumption_elec'].plot.bar(width = 0.3, color = 'orange', position=0, label = 'self-consumption')
	totalMonthlyData_df['import_elec'].plot.bar( width = 0.3, color = 'tomato', position=0, bottom = totalMonthlyData_df['self_consumption_elec'], label='imported electricity')
	totalMonthlyData_df['export_elec'].plot.bar(width = 0.3, color = 'royalblue',position=0, label='exported electricity')
	plt.legend()
	plt.ylabel("kWh/m2 per month")
	plt.xlabel('Month')
	plt.title('electricity flows')
	plt.show()
	return fig #bar