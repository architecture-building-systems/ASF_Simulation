"""
Created on March 28 2017

@author: PJ


"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import kendalltau


def archetypePlots():

	ASFsimDataPath=os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','CEA_Archetypes_CH','Archetypes_ZH_COP1.csv'))
	StaticsimDataPath=os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','CEA_Archetypes_CH','Archetypes_ZH_COP1_static.csv'))
	print ASFsimDataPath
	ASFsimData=pd.read_csv(ASFsimDataPath)
	ASFsimData.set_index(['Name'], inplace=True)

	StaticsimData=pd.read_csv(StaticsimDataPath)
	StaticsimData.set_index(['Name'], inplace=True)


	#Define Archetypes for plotting axis labels
	archetypes = ["MULTI_RES", "SINGLE_RES","HOTEL","OFFICE","RETAIL","FOODSTORE","RESTAURANT","INDUSTRIAL","SCHOOL","HOSPITAL","GYM"]
	


	#Define years constructed for axes labels
	yearsConstructed=['2020-2030', '2005-2020', '1980-2005', '1970-1980', '1920-1970', '-1920']
	#yearsConstructed=["-1920","1920-1970","1970-1980","1980-2005","2005-2020","2020-2030"]

	#prepare empty numpy array for heatmap
	ASFResults=np.zeros([6,11])
	StaticResults=np.zeros([6,11])

	#loop through all archetypes and place into heatmap in the correct location
	for ii,archetype in enumerate(archetypes):
		#PJlist.append([])
		for jj in range(1,7):
			selectType="{0}{1}".format(archetype,str(jj))
			ASFResults[7-jj-1,ii]=ASFsimData.loc[selectType,["E"]]
			StaticResults[7-jj-1,ii]=StaticsimData.loc[selectType,["E"]]


	energySaving=StaticResults-ASFResults
	#Convert to dataframe for seaborn heatmap input
	plottingDF = pd.DataFrame(energySaving, index=yearsConstructed, columns=archetypes)


	ax=sns.heatmap(plottingDF, linewidths=.5, cbar_kws={'label': 'Energy Saving Potential [kWh/year]'})

	plt.show()


if __name__ == '__main__':
	archetypePlots()