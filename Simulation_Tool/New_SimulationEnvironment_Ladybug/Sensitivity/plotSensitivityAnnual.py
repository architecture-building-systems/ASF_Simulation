import os
import sys
import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import seaborn as sns

def sensitivityPlots():

	plt.style.use('seaborn-whitegrid')
	ASFsimData=pd.read_csv('Sensitivity_ZH_U_env_COP3_1.csv')
	ASFsimData.set_index(['U_envelope'], inplace=True)

	ASFsimDataStatic=pd.read_csv('Sensitivity_ZH_U_env_COP3_1_static.csv')
	ASFsimDataStatic.set_index(['U_envelope'], inplace=True)

	EnergySavings=ASFsimDataStatic-ASFsimData

	#sns.set(style="darkgrid")



	# Plot the response with standard error

	ax=EnergySavings.plot(y=["E","PV","C","H","L"])
	ax.legend(labels=["Net Energy", "PV Supply", "Cooling", "Heating", "Lighting"], loc=2)
	ax.set_ylabel('Energy Consumption [kWh/year]')


	#plt.savefig('energySaving_COP1_3_static.pdf', bbox_inches='tight')
	plt.show()


if __name__ == '__main__':
	sensitivityPlots()