import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

import pandas as pd
import seaborn as sns



def sensitivityPlots():

	plt.style.use('seaborn-whitegrid')
	ASFsimData=pd.read_csv('Sensitivity_ZH_U_env_COP3_1.csv')
	ASFsimData.set_index(['U_envelope'], inplace=True)

	ASFsimDataStatic=pd.read_csv('Sensitivity_ZH_U_env_COP3_1_static.csv')
	ASFsimDataStatic.set_index(['U_envelope'], inplace=True)

	ASFsimDataNoASF=pd.read_csv('Sensitivity_ZH_U_env_COP3_1_NoASF.csv')
	ASFsimDataNoASF.set_index(['U_envelope'], inplace=True)

	EnergySavingsStatic=ASFsimDataStatic-ASFsimData
	EnergySavingsNoASF=ASFsimDataNoASF-ASFsimData

	#Define matplotlib font size
	matplotlib.rcParams['xtick.labelsize']=20
	matplotlib.rcParams['ytick.labelsize']=20
	matplotlib.rcParams['legend.fontsize']=18
	matplotlib.rcParams['axes.labelsize']=24
	matplotlib.rcParams['lines.linewidth']=5.0
	matplotlib.rcParams['lines.markersize']=20.0

	# set line styles
	styles1 = [sns.xkcd_rgb["midnight"],sns.xkcd_rgb["medium green"],sns.xkcd_rgb["denim blue"],sns.xkcd_rgb["pale red"],sns.xkcd_rgb["dark yellow"]]
	styles1=['k-','-.','.',':','--']

	ax1=ASFsimData.plot(y=["E","PV","C","H","L"], style=styles1)
	ax1.legend(labels=["Net Energy", "PV Supply", "Cooling", "Heating", "Lighting"], loc=2)
	ax1.set_xlabel(r"U_envelope [$Wm^{-2}K^{-1}$]")
	ax1.set_ylabel(r'Energy Consumption [$kWh/year$]')
	plt.savefig('Sensitivity_ZH_U_env_COP3_1_ASF.pdf', bbox_inches='tight')

	ax2=ASFsimDataStatic.plot(y=["E","PV","C","H","L"], style=styles1)
	ax2.legend(labels=["Net Energy", "PV Supply", "Cooling", "Heating", "Lighting"], loc=2)
	ax2.set_xlabel(r"U_envelope [$Wm^{-2}K^{-1}$]")
	ax2.set_ylabel(r'Energy Consumption [$kWh/year$]')
	#plt.savefig('Sensitivity_ZH_U_env_COP3_1_Static.pdf', bbox_inches='tight')

	ax3=ASFsimDataNoASF.plot(y=["E","PV","C","H","L"], style=styles1)
	ax3.legend(labels=["Net Energy", "PV Supply", "Cooling", "Heating", "Lighting"], loc=2)
	ax3.set_xlabel(r"U_envelope [$Wm^{-2}K^{-1}$]")
	ax3.set_ylabel(r'Energy Consumption [$kWh/year$]')
	#plt.savefig('Sensitivity_ZH_U_env_COP3_1_NoASF.pdf', bbox_inches='tight')

	ax4=EnergySavingsStatic.plot(y=["E","PV","C","H","L"], style=styles1, legend=None)
	#ax4.legend(labels=["Net Energy", "PV Supply", "Cooling", "Heating", "Lighting"], loc=2)
	ax4.set_xlabel(r"U_envelope [$Wm^{-2}K^{-1}$]")
	ax4.set_ylabel(r'Energy Saving [$kWh/year$]')
	plt.savefig('Sensitivity_ZH_U_env_COP3_1EnergySavingStatic.pdf', bbox_inches='tight')

	ax5=EnergySavingsNoASF.plot(y=["E","PV","C","H","L"], style=styles1, legend=None)
	#ax5.legend(labels=["Net Energy", "PV Supply", "Cooling", "Heating", "Lighting"], loc=1)
	ax5.set_xlabel(r"U_envelope [$Wm^{-2}K^{-1}$]")
	ax5.set_ylabel(r'Energy Saving [$kWh/year$]')
	plt.savefig('Sensitivity_ZH_U_env_COP3_1EnergySavingNoASF.pdf', bbox_inches='tight')
	print matplotlib.rcParams['font.size']

	
	#plt.savefig('energySaving_COP1_3_static.pdf', bbox_inches='tight')
	plt.show()


if __name__ == '__main__':
	sensitivityPlots()