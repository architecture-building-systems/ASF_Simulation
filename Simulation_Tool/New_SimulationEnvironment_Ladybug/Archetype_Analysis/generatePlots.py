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

	dataPath=os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','CEA_Archetypes_CH','Archetypes_ZH_COP1.csv'))
	print dataPath
	data=pd.read_csv(dataPath)
	data.set_index(['Name'], inplace=True)


	archetypes = ["MULTI_RES", "SINGLE_RES","HOTEL","OFFICE","RETAIL","FOODSTORE","RESTAURANT","INDUSTRIAL","SCHOOL","HOSPITAL","GYM"]
	yearsConstructed=[1000,1200,1300,1400,1500,1600]

	PJlist=[]




	for ii,archetype in enumerate(archetypes):
		#PJlist.append([])
		for jj in range(1,13):
			selectType="{0}{1}".format(archetype,str(jj))
			#print data.loc[selectType,["E"]]
			#PJdataFrame.append(data.loc[selectType,["E"]])
			#generate numpy array here

	#Conver np.random.radn(5,11) with a numpy array generated from the nested forloop
	PJdf = pd.DataFrame(np.random.randn(6,11), index=yearsConstructed, columns=archetypes)


	print PJdf

	sns.heatmap(PJdf, linewidths=.5)

	plt.show()


if __name__ == '__main__':
	archetypePlots()