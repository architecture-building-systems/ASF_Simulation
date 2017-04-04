import os
import sys
import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import seaborn as sns

def sensitivityPlots():

	plt.style.use('seaborn-whitegrid')
	ASFsimData=pd.read_csv('Sensitivity_ZH_Infl_COP3_1.csv')
	ASFsimData.set_index(['Infiltration'], inplace=True)

	ASFsimDataStatic=pd.read_csv('Sensitivity_ZH_Infl_COP3_1_static.csv')
	ASFsimDataStatic.set_index(['Infiltration'], inplace=True)

	ASFsimDataNoASF=pd.read_csv('Sensitivity_ZH_Infl_COP3_1_NoASF.csv')
	ASFsimDataNoASF.set_index(['Infiltration'], inplace=True)

	EnergySavingsStatic=ASFsimDataStatic-ASFsimData
	EnergySavingsNoASF=ASFsimDataNoASF-ASFsimData

	#sns.set(style="darkgrid")



	# Plot the response with standard error

	ax1=ASFsimData.plot(y=["E","PV","C","H","L"])
	ax1.legend(labels=["Net Energy", "PV Supply", "Cooling", "Heating", "Lighting"], loc=2)
	ax1.set_ylabel('Energy Consumption [kWh/year]')
	plt.savefig('Sensitivity_ZH_Infl_COP3_1_ASF.pdf', bbox_inches='tight')

	ax2=ASFsimDataStatic.plot(y=["E","PV","C","H","L"])
	ax2.legend(labels=["Net Energy", "PV Supply", "Cooling", "Heating", "Lighting"], loc=2)
	ax2.set_ylabel('Energy Consumption [kWh/year]')
	plt.savefig('Sensitivity_ZH_Infl_COP3_1_Static.pdf', bbox_inches='tight')

	ax3=ASFsimDataNoASF.plot(y=["E","PV","C","H","L"])
	ax3.legend(labels=["Net Energy", "PV Supply", "Cooling", "Heating", "Lighting"], loc=2)
	ax3.set_ylabel('Energy Consumption [kWh/year]')
	plt.savefig('Sensitivity_ZH_Infl_COP3_1_NoASF.pdf', bbox_inches='tight')

	ax4=EnergySavingsStatic.plot(y=["E","PV","C","H","L"])
	ax4.legend(labels=["Net Energy", "PV Supply", "Cooling", "Heating", "Lighting"], loc=2)
	ax4.set_ylabel('Energy Saving [kWh/year]')
	plt.savefig('Sensitivity_ZH_Infl_COP3_1EnergySavingStatic.pdf', bbox_inches='tight')

	ax5=EnergySavingsNoASF.plot(y=["E","PV","C","H","L"])
	ax5.legend(labels=["Net Energy", "PV Supply", "Cooling", "Heating", "Lighting"], loc=2)
	ax5.set_ylabel('Energy Saving [kWh/year]')
	plt.savefig('Sensitivity_ZH_Infl_COP3_1EnergySavingNoASF.pdf', bbox_inches='tight')


	#plt.savefig('energySaving_COP1_3_static.pdf', bbox_inches='tight')
	plt.show()


if __name__ == '__main__':
	sensitivityPlots()