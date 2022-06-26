import os, sys
import numpy as np
import json
import time
import warnings
import csv
import matplotlib.pyplot as plt
import pandas as pd

#sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'Results')) 

from createCarpetPlot_electricityFlow import createCarpetPlot, createCarpetPlotXAngles, createCarpetPlotYAngles

def MonthlyFlowElec_Plot (monthlyFlowElec):
	fig0 = createCarpetPlot (monthlyData = monthlyFlowElec['E_total'], roomFloorArea = roomFloorArea)
	plt.show()
	return

def CO2_plot():
	CO2_electricty_data_df = pd.read_csv(os.path.join(paths['CO2_electricity'], 'CH_year_2015_2016.csv'), sep = ';') #kg CO2-eq per kWh
	fig = plt.figure(figsize=(16, 8))
	hour = np.arange(0, 8760)
	plt.plot(hour, CO2_electricty_data_df['GWP [kg CO2eq/kWh]'])
	plt.title('Dynamic CO2-eq content of Swiss el. mix')
	plt.ylabel('kg CO2-eq/kWh')
	plt.xlabel('hour of the year')
	plt.show()
	fig.savefig(os.path.join(paths['CO2_electricity'], 'figure0' + '.pdf'))
	fig.savefig(os.path.join(paths['CO2_electricity'], 'figure0' + '.png'))
	return

def EnergyConsumption_plot(monthlyData, FloorArea):
	Heating_elec = np.zeros(12)
	Heating_fossil = np.zeros(12)
	Cooling_elec = np.zeros(12)
	Lightning_elec = np.zeros(12)
	AE_elec =np.zeros(12)

	for month in range(12):
		Heating_elec[month] = 0
		Heating_fossil[month] = 0
		Cooling_elec[month] = 0
		Lightning_elec[month] = 0
		AE_elec[month] = 0

	month = 0
	for i in range(len(monthlyData['E_total'][u'H'])):
		if i!=0 and i%24==0:
			month +=1
	
		Heating_elec[month] += monthlyData['E_total'][u'H_elec'][i]/FloorArea #kWh/m2
		Heating_fossil[month] += monthlyData['E_total'][u'H_fossil'][i]/FloorArea #kWh/m2
		Cooling_elec[month] += monthlyData['E_total'][u'C'][i]/FloorArea #kWh/m2
		Lightning_elec[month] += monthlyData['E_total'][u'L'][i]/FloorArea #kWh/m2
		AE_elec[month] += monthlyData['E_total'][u'AE'][i]/FloorArea #kWh/m2

	
	consumption_dict = {'Heating_elec': Heating_elec, 
				'Heating_fossil': Heating_fossil,
				'Cooling_elec': Cooling_elec,
				'Lightning_elec': Lightning_elec,
				'AE_elec': AE_elec}	
	
	consumption_df = pd.DataFrame(consumption_dict)

	months = np.arange(1, 13)
	width = 0.35 

	fig, ax = plt.subplots()
	if max (Cooling_elec)!= 0 : 
		if max(Heating_elec)!=0 and max(Heating_fossil)!=0:
			ax.bar(months, Heating_elec, width, label='Heating electricity')
			ax.bar(months, Heating_fossil, width, bottom=Heating_elec, label='Heating fossil')
			ax.bar(months, Cooling_elec, width, bottom=Heating_elec+Heating_fossil, label='Cooling electricity')
			ax.bar(months, Lightning_elec, width, bottom=Heating_elec+Heating_fossil+Cooling_elec, label='Lightning electricity')
			ax.bar(months, AE_elec, width, bottom=Heating_elec+Heating_fossil+Cooling_elec+Lightning_elec, label='Actuation electricity')

		elif max(Heating_elec)==0 and max(Heating_fossil)!=0:
			ax.bar(months, Heating_fossil, width, label='Heating fossil')
			ax.bar(months, Cooling_elec, width, bottom=Heating_fossil, label='Cooling electricity')
			ax.bar(months, Lightning_elec, width, bottom=Heating_fossil+Cooling_elec, label='Lightning electricity')
			ax.bar(months, AE_elec, width, bottom=Heating_fossil+Cooling_elec+Lightning_elec, label='Actuation electricity')
		elif max(Heating_elec)!=0 and max(Heating_fossil)==0:
			ax.bar(months, Heating_elec, width, label='Heating electricity')
			ax.bar(months, Cooling_elec, width, bottom=Heating_elec, label='Cooling electricity')
			ax.bar(months, Lightning_elec, width, bottom=Heating_elec+Cooling_elec, label='Lightning electricity')
			ax.bar(months, AE_elec, width, bottom=Heating_elec+Cooling_elec+Lightning_elec, label='Actuation electricity')

		else:
			ax.bar(months, Cooling_elec, width,  label='Cooling electricity')
			ax.bar(months, Lightning_elec, width, bottom=Cooling_elec, label='Lightning electricity')
			ax.bar(months, AE_elec, width, bottom=Cooling_elec+Lightning_elec, label='Actuation electricity')
	else: 
		if max(Heating_elec)!=0 and max(Heating_fossil)!=0:
			ax.bar(months, Heating_elec, width, label='Heating electricity')
			ax.bar(months, Heating_fossil, width, bottom=Heating_elec, label='Heating fossil')
			ax.bar(months, Lightning_elec, width, bottom=Heating_elec+Heating_fossil, label='Lightning electricity')
			ax.bar(months, AE_elec, width, bottom=Heating_elec+Heating_fossil+Lightning_elec, label='Actuation electricity')

		elif max(Heating_elec)==0 and max(Heating_fossil)!=0:
			ax.bar(months, Heating_fossil, width, label='Heating fossil')
			ax.bar(months, Lightning_elec, width, bottom=Heating_fossil, label='Lightning electricity')
			ax.bar(months, AE_elec, width, bottom=Heating_fossil+Lightning_elec, label='Actuation electricity')

		elif max(Heating_elec)!=0 and max(Heating_fossil)==0:
			ax.bar(months, Heating_elec, width, label='Heating electricity')
			ax.bar(months, Lightning_elec, width, bottom=Heating_elec, label='Lightning electricity')
			ax.bar(months, AE_elec, width, bottom=Heating_elec+Lightning_elec, label='Actuation electricity')

		else:
			ax.bar(months, Lightning_elec, width, label='Lightning electricity')
			ax.bar(months, AE_elec, width, bottom=Lightning_elec, label='Actuation electricity')
	ax.set_ylabel('Energy [kWh/m2]')
	ax.set_xlabel('Month')
	ax.set_title('Needed energy per month')
	ax.legend()

	#plt.show()


	return fig, consumption_df

def SaveFig(fig, name, path): 
	fig.savefig(os.path.join(path, name + '.pdf'))
	fig.savefig(os.path.join(path, name + '.png'))
	return 

def importData(paths):
	#monthlyFlowElec = pd.read_csv(os.path.join(paths['sim_results'], 'MonthlyElecFlow.csv'))
	#monthlyData = pd.read_csv(os.path.join(paths['sim_results'], 'monthlyData.csv'))
	with open(os.path.join(paths['sim_results'], 'MonthlyElecFlow.json')) as json_file:
		monthlyFlowElec = json.load(json_file)


	with open(os.path.join(paths['sim_results'], 'monthlyData.json')) as json_file:
		monthlyData = json.load(json_file)
	#monthlyData = pd.read_csv(os.path.join(paths['sim_results'], 'monthlyData.csv'))
	#print monthlyFlowElec['E_total_elec'].keys()
	print monthlyData['E_total'].keys()

	#np_monthlyData = np.load(os.path.join(paths['sim_results'], 'monthlyData.npy'), allow_pickle=True)
	#print monthlyFlowElec
	#print max(monthlyFlowElec['E_total'][u'self_prod'])
	#print np_monthlyData
	#print monthlyData.dtypes
	return monthlyFlowElec, monthlyData

def init():
	paths = {}
	FolderName = 'Results_ZH_ASF_WWR04_ArchF' #Results_ZH_Classic_WWR027_threshold_ArchA, Results_ZH_Classic_WWR031_threshold_ArchB, Results_ZH_Classic_WWR040_threshold_ArchC, Results_ZH_ASF_WWR027_ArchA, Results_ZH_ASF_WWR031_ArchB, Results_ZH_ASF_WWR04_ArchC
	roomFloorArea = 5.23*4.2 #m2


	paths['main'] = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
	paths['results'] = os.path.join(paths['main'], 'Results/AA_ForLCA')
	paths['CO2_electricity'] = os.path.join(paths['main'], 'CO2_electricity')
	paths['sim_results'] = os.path.join(paths['results'], FolderName)
	paths['sim_Figures'] = os.path.join(paths['sim_results'], 'Figures')

	if not os.path.isdir(paths['sim_results']):
		print 'ERROR: no results for this simulation. Check FolderName'

	return paths, roomFloorArea

if __name__=='__main__':

	paths, roomFloorArea = init()

	monthlyFlowElec, monthlyData = importData(paths)

	figA, consumption_df = EnergyConsumption_plot(monthlyData, roomFloorArea) #kWh/m2

	SaveFig(figA, 'EnergyConsumption', paths['sim_Figures'])
	
	consumption_df.to_csv(os.path.join(paths['sim_results'], 'consumption.csv'))
