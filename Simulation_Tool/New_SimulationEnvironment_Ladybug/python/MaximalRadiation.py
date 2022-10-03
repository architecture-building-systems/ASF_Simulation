"""
created: 22.06.2022
Jasmine de Riedmatten


Compute the self consumtion of electricity. If production and demand occur at the same time, cover the demande with the produced electricity. 
If the production is higher than the demand, export the electricity to the grid. 
If the production is smaller than the demand, import electricity from the grid.

"""

import os, sys
from turtle import position
import numpy as np
import json
import time
import pandas as pd
from prepareData_mauro import sum_monthly, average_monthly

def MaxRadiationWall(paths, FolderName): 
	paths['sim_results'] = os.path.join(paths['results'], FolderName)
	#Folders = [x[0] for x in os.walk(paths['sim_results'])]
	Folders = os.listdir(paths['sim_results'])
	TotalRadiationWall = 0.0
	for names in Folders: 
		if names[-8:]=="_0_0.csv":
			paths['content'] = os.path.join(paths['sim_results'], names)
			content = pd.read_csv(paths['content'],sep=";")
			RadiationWall = content.iloc[0]['total_radiation_(kWh per year)']
			TotalRadiationWall += float(RadiationWall)



	return TotalRadiationWall

if __name__=='__main__':
	paths = {}

	paths['main'] = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
	paths['results'] = os.path.join(paths['main'], 'RadiationData')


	Results = {}
	FolderNames = os.listdir(paths['results'])
	for FolderName in FolderNames:
		if FolderName[:14] == "radiation_wall":
			TotalRadiationWall = MaxRadiationWall(paths, FolderName)
			Results[FolderName] = TotalRadiationWall
			print FolderName, TotalRadiationWall
	
	Results = pd.DataFrame(Results, index=[0]).T
	Results.to_csv(os.path.join(paths['results'], 'TotalMaxRadiationWall.csv'))

	print "finish"
	"""
	Radiation1 = {}
	Radiation2 = {}
	TotalRadiation1 = 0.0
	TotalRadiation2 = 0.0
	FolderNames = ['radiation_wall_ZH_Classic_without_test', 'radiation_wall_ZH_Classic_with_test']
	paths['sim_results1'] = os.path.join(paths['results'], FolderNames[0])
	paths['sim_results2'] = os.path.join(paths['results'], FolderNames[1])
	Folders1 = os.listdir(paths['sim_results1'])
	Folders2 = os.listdir(paths['sim_results2'])
	for names in Folders1: 
		if names[-7:]=="0_0.csv":
			paths['content1'] = os.path.join(paths['sim_results1'], names)
			paths['content2'] = os.path.join(paths['sim_results2'], names)
			content1 = pd.read_csv(paths['content1'],sep=";")
			content2 = pd.read_csv(paths['content2'],sep=";")
			RadiationWall1 = content1.iloc[0]['total_radiation_(kWh per year)']
			RadiationWall2 = content2.iloc[0]['total_radiation_(kWh per year)']
			TotalRadiation1 += float(RadiationWall1)
			TotalRadiation2 += float(RadiationWall2)
			print RadiationWall1, '   ', RadiationWall2
			Radiation1[names] = RadiationWall1
			Radiation2[names] = RadiationWall2

	print 'Total radiation ', TotalRadiation1, '  ', TotalRadiation2
	"""