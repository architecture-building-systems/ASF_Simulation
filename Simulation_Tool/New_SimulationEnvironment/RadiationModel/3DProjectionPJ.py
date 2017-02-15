
#http://math.stackexchange.com/questions/164700/how-to-transform-a-set-of-3d-vectors-into-a-2d-plane-from-a-view-point-of-anoth



import sys, os
import math
import numpy as np
import pandas as pd
import time

from sympy.solvers import solve
from sympy import Point, Polygon, pi, Symbol
from scipy.optimize import fsolve

from matplotlib import pyplot
import pylab
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import matplotlib.pyplot as plt



paths = {}

geoLocation = 'Zuerich_Kloten_2013.epw'

# find path of current folder (simulation_environment)
paths['RadModel'] = os.path.abspath(os.path.dirname(sys.argv[0]))

paths['main'] = os.path.dirname(paths['RadModel'])
paths['weather'] = os.path.join(os.path.dirname(paths['main']), 'WeatherData')
paths['location'] = os.path.join(paths['weather'], geoLocation)
paths['scirpt'] =  os.path.join(paths['main'], 'python')
paths['SunData'] = os.path.join(paths['RadModel'], 'SunPosition2.csv')
paths['PanelData'] = os.path.join(paths['RadModel'], 'PanelPostion.csv')
paths['SunAngles'] = os.path.join(paths['RadModel'], 'SunAngles.csv')
paths['Save'] = paths['RadModel']

sys.path.insert(0, paths['scirpt'])
						
from epwreader import epw_reader
#read epw file of needed destination
weatherData = epw_reader(paths['location'])

radiation = weatherData[['year', 'month', 'day', 'hour','dirnorrad_Whm2', 'difhorrad_Whm2','glohorrad_Whm2']]

from ProjectionFunction import CaseA,CaseB, Theta2directions, RadTilt, calcShadow




#Load LB-Files
SolarData = np.load(os.path.join(paths['Save'], 'SolarData.npy')).item()
SolarData_df = pd.DataFrame(SolarData)
SolarData2 = np.load(os.path.join(paths['Save'], 'SolarData2.npy')).item()
SolarData_df2 = pd.DataFrame(SolarData2)
SolarData3 = np.load(os.path.join(paths['Save'], 'SolarData3.npy')).item()
SolarData_df3 = pd.DataFrame(SolarData3)

SolarData_df = pd.concat([SolarData_df,SolarData_df2, SolarData_df3], axis=1)
LB = SolarData_df['00'] * 1000 / (50*0.4*0.4) # kWh in Wh divided through area of panels in m2
LB.columns = ['00']


WindowDataLB = np.load(os.path.join(paths['Save'], 'BuildingData.npy')).item()
BuildingRadLB_df = pd.DataFrame(WindowDataLB)

WindowData2 = np.load(os.path.join(paths['Save'], 'BuildingData2.npy')).item()
BuildingRad2_df = pd.DataFrame(WindowData2)


RadAnalysis = pd.concat([radiation['dirnorrad_Whm2']/LB, radiation['difhorrad_Whm2']/LB,radiation['glohorrad_Whm2']/LB, LB/LB], axis=1)
RadAnalysis.columns = ['direct', 'diffuse', 'global', 'LB']


SunAngles = pd.read_csv(paths['SunAngles'])
SunData = pd.read_csv(paths['SunData'])
SunAngles['Azimuth'] = SunAngles['Azimuth']-180
PanelPoints = pd.read_csv(paths['PanelData'])

TotalHOY = SunData['HOY'].tolist()


RadiationTilt = {}
RadiationASF = {}
RadiationWindow = {}
Percentage = {}
theta_dict = {}
LatShading = {}
LongShading = {}
WindowTilt = {}
InterPoints = {}



########DEPRECIATED
# beta = 90       # slope of tilt surface
# gamma = 180       # surface azimuth angle, south facing ASF = 180
reflectance = 0         # reflectivity # 0.2



#set Room Properties
room_height = 3100.
room_depth = 7000.
room_width = 4900.

gpW =  0.92 #glazing_percentage_w
gpH =  0.97 #glazing_percentage_h


#Set Panel Properties
PanelSize = 400. #mm
DistWindow = 300 #Distance from the Glazed Surface

#panelSpacing = 500 # in x y dirction[mm]
#ReCalcPanelSpacing = math.sqrt(2*(panelSpacing**2))
#panelSpacing = int(ReCalcPanelSpacing)

panelSpacing = 707

xArray= 6 # Number of Panels in x direction
yArray= 9 # number of rows


XANGLES = [0]
YANGLES = [-45]

#XANGLES=[0]
#YANGLES=[-45]

#Select shading cases which should be evaluated
ShadingCase = ['1','2','3']


TimePeriod1 = range(175,186)
TimePeriod2 = range(4460,4481)

TimePeriod = TimePeriod2 #TimePeriod2 + 

print TimePeriod

showFig = False

for HOY in TimePeriod:
	
	#HOY -= 1
	
	#panelSpacing = 566 #Just for shading analysis, to be deleted later
	print panelSpacing
	
	RadiationTilt[HOY] = {}
	RadiationASF[HOY] = {}
	WindowTilt[HOY] = {}    
	RadiationWindow[HOY] = {}
	Percentage[HOY] = {}
	theta_dict[HOY] = {}
	LatShading[HOY] = {}
	LongShading[HOY] = {}
	InterPoints[HOY] = {}
	
	if HOY in TotalHOY:
		
		ind = TotalHOY.index(HOY)
			
		for x_angle in XANGLES:
			for y_angle in YANGLES:
				
				
				print '\nStart Calculation'
				print 'Time: ' + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
				
				print 'HOY', HOY
				print 'ii', ind
				
				tic = time.time()
				
				print str(x_angle), str(y_angle)
				
					
				#Calculate angle of incidence
				#Angle Definition: -90 East, 0 South, 90 West
				theta = Theta2directions (sunAlt = SunAngles['Altitude'][ind] , sunAzi = SunAngles['Azimuth'][ind], panelAlt = (90 - x_angle), panelAzi = -y_angle)
				thetaWindow = Theta2directions (sunAlt = SunAngles['Altitude'][ind] , sunAzi = SunAngles['Azimuth'][ind], panelAlt = 90, panelAzi = -y_angle)
    
					
				#Calculate Radiation on tilt ASF surface
				RadiationTilt[HOY][str(x_angle) + str(y_angle)] = RadTilt (I_dirnor = radiation['dirnorrad_Whm2'][HOY], I_dif = radiation['difhorrad_Whm2'][HOY], 
                                                                                    ref = reflectance, theta = theta, panelAlt = (90 - x_angle), sunAlt = SunAngles['Altitude'][ind])          
				 
    					
				#Calculate Radiation on tilt ASF surface
				WindowTilt[HOY][str(x_angle) + str(y_angle)] = RadTilt (I_dirnor = radiation['dirnorrad_Whm2'][HOY], I_dif = radiation['difhorrad_Whm2'][HOY], 
                                                                                ref = reflectance, theta = thetaWindow, panelAlt = 90, sunAlt = SunAngles['Altitude'][ind])          
				
				
				
				#Calculate ASF Geometry
				#The adaptive solar facade is represented by an array of coordinates and panel size
				h=math.sqrt(2*(PanelSize/2)**2) #distance from centre of panel to corner [mm]
				
			   

				ASFArray=[] # create array with all panel centerpoints with x and y-coordination
				for ii in range(yArray):
					ASFArray.append([])
					for jj in range (xArray):
						if ii%2==0:
							ASFArray[ii].append([jj*panelSpacing,ii*panelSpacing/2])
						else:
							if jj==xArray-1:
								pass
							else:
								ASFArray[ii].append([jj*panelSpacing+panelSpacing/2,ii*panelSpacing/2])
				
                        #change order of the panels, start from top left to bottom right
				ASFArray2 = [] #What is ASFArray2? Is it inverting the ASF Array?
				for ii in range(yArray-1,-1,-1):
					ASFArray2.append(ASFArray[ii])

				
				#Calculate Shadow Pattern
				ASF_Projection = {}
				count = 0
				shadowData=[]
				for ii,row in enumerate(ASFArray2):
					shadowData.append([])
	
					for jj,P in enumerate(row):
		   
						##TODO: Check that the angles in calc shadow are accurate. There is a large probability of error here
						S0,S1,S2,S3,S4=calcShadow(P0 = P, sunAz = math.radians(SunAngles['Azimuth'][ind]), sunAlt = math.radians(SunAngles['Altitude'][ind]), 
                                                            panelAz = -math.radians(y_angle), panelAlt = math.radians(x_angle), h = h, d = DistWindow)
                                                            
						shadowData[ii].append([S1,S2,S3,S4])

						ASF_Projection[count] = [S1,S2,S3,S4] 
						count +=1
		
				if showFig == True:
					#Plot Data
					for ii,row in enumerate(shadowData):
						#print 'new row'
						for jj, Shadow in enumerate(row):
							#Plot Shadow Pattern
							# x,y = zip(*Shadow)
							# plt.scatter(x,y, c=np.random.rand(3,1))
							# plt.axis('equal')
							pass
					#plt.show()
					
				#Calculate Number of Panels
				PanelNum = len(ASF_Projection)
				WindowArea = room_width/1000.0 * room_height/1000.0 * gpH * gpW
    
    
				  
				
				print 'time passed before overlap', time.time()-tic
				if SunAngles['Azimuth'][ind] > 90 or SunAngles['Azimuth'][ind] < -90:
					#no direct radiation, therefore no overlap
					Percentage[HOY][str(x_angle) + str(y_angle)] = 1
	
				
				else: 
					print "\nStart Geometry Analysis"
					print "Sun Angle Is", SunAngles['Azimuth'][ind]
					if SunAngles['Azimuth'][ind] >= 0: 
						Percentage[HOY][str(x_angle) + str(y_angle)], LatShading[HOY][str(x_angle) + str(y_angle)], LongShading[HOY][str(x_angle) + str(y_angle)], InterPoints[HOY][str(x_angle) + str(y_angle)] = CaseA (ind = ind, SunAngles = SunAngles, ASF_dict_prime = ASF_Projection, PanelNum = PanelNum, row2 = yArray, col = xArray, Case = ShadingCase)
						
					elif SunAngles['Azimuth'][ind] < 0: 
						Percentage[HOY][str(x_angle) + str(y_angle)], LatShading[HOY][str(x_angle) + str(y_angle)], LongShading[HOY][str(x_angle) + str(y_angle)] = CaseB (ind = ind, SunAngles = SunAngles, ASF_dict_prime = ASF_Projection, PanelNum = PanelNum, row2 = yArray, col = xArray, Case = ShadingCase)
				
				
				ReductionWindow = np.cos(math.radians(x_angle)- math.radians(SunAngles['Altitude'][ind])) * np.cos(-math.radians(y_angle) - math.radians(SunAngles['Azimuth'][ind]))
				print ReductionWindow
    
				#Calculate Radiation on ASF
				RadiationASF[HOY][str(x_angle) + str(y_angle)] = round(PanelNum * (PanelSize**2/10**(6)) * Percentage[HOY][str(x_angle) + str(y_angle)] * RadiationTilt[int(HOY)][str(x_angle) + str(y_angle)] * 0.001 ,3) # area in m2 * Wh/m2 in KWh
				RadiationWindow[HOY][str(x_angle) + str(y_angle)] = round((WindowArea - (PanelNum * PanelSize**2/(10**(6)) * Percentage[HOY][str(x_angle) + str(y_angle)] * ReductionWindow)) * WindowTilt[HOY][str(x_angle) + str(y_angle)] * 0.001 ,3) # area in m2 * Wh/m2 in KWh
			   
				toc = time.time() - tic
				print 'time passed (sec): ' + str(round(toc,2))
		
	else:
		print 'HOY', HOY
		print 'No Radiation'
		# case with no radiation
		for x_angle in XANGLES:
			for y_angle in YANGLES:
						
				RadiationASF[HOY][str(x_angle) + str(y_angle)] = 0
				Percentage[HOY][str(x_angle) + str(y_angle)] = 1
				RadiationWindow[HOY][str(x_angle) + str(y_angle)] = 0


ResultASF_df = pd.DataFrame(RadiationASF).T
ResultWindow_df = pd.DataFrame(RadiationWindow).T
Percentage_df = pd.DataFrame(Percentage).T



n_panel = 0.1 # 10 Precent


PowerLoss = pd.read_csv(os.path.join(paths['RadModel'], 'powerloss.csv'))
#longitude = pd.read_csv(os.path.join(paths, 'longitude.csv'))
#latitude = pd.read_csv(os.path.join(paths, 'latitude.csv'))

PowerLoss.columns = [range(50)]


Long = np.array(range(0,100,2))/100.
Lat = np.array(range(0,100,2))/100.

Long = Long.tolist()
Lat = Lat.tolist()

import math

def round_up_to_even(number):
	return math.ceil(number/ 2.) * 2

def round_down_to_even(number):
	return math.ceil(number/ 2.) * 2 - 2    
	
PV = {}
PV2 = {}
shading_loss = {}
Window = {}

shading = True

for HOY in TimePeriod:
	PV[HOY] = np.array([])
	PV2[HOY] = {}
	shading_loss[HOY] = {}
	Window[HOY] = np.array([])
	
	for x_angle in XANGLES:
		for y_angle in YANGLES:
			shading_loss[HOY][str(x_angle) + str(y_angle)] = {}
			
			PV_sum = 0
			if Percentage[HOY][str(x_angle) + str(y_angle)] == 1:
				PV_sum = RadiationASF[HOY][str(x_angle) + str(y_angle)] * n_panel
			else:                
				#TODO: Radiation on a panel is averaged               
				Radiation = RadiationASF[HOY][str(x_angle) + str(y_angle)]/float(PanelNum)
				LatNum = LatShading[HOY][str(x_angle) + str(y_angle)] 
				LongNum = LongShading[HOY][str(x_angle) + str(y_angle)]
	
				for ind in range(PanelNum):
					shading_loss[HOY][str(x_angle) + str(y_angle)][ind] = {}
					
					if LatNum[ind] > 0.98:
						n_shading = 90
					elif LongNum[ind] > 0.98:
						n_shading = 90
					else:
						#shading is rounded up to the next even number
						valueLat = round_up_to_even(LatNum[ind] *100)
						lat_index = Lat.index(valueLat/100.)
						
						#shading is rounded up to the next even number
						valueLong = round_up_to_even(LongNum[ind] *100)
						long_index = Lat.index(valueLong/100.)
					
						n_shading = PowerLoss[long_index][lat_index]
						
					shading_loss[HOY][str(x_angle) + str(y_angle)][ind] = n_shading    
#                    print 'shading', n_shading
#                    print 'Radiaiton', Radiation                    
#                    print 'PV',PV_sum
					
					if shading == True:
						
						PV_sum += (n_panel * (1-n_shading/100.) * Radiation) 
						
					else:
						PV_sum += (n_panel * 1 * Radiation) 
						
			PV2[HOY][str(x_angle) + str(y_angle)] = round(PV_sum * 1000,3) 
			
			PV[HOY] = np.append(PV[HOY], PV_sum * 1000)
			Window[HOY] = np.append(Window[HOY], RadiationWindow[HOY][str(x_angle) + str(y_angle)] * 1000)
			
		   

PV_dict = PV2
PV_list = PV
Window_list = Window




   


fig, axes = plt.subplots(nrows=2, ncols=5, figsize=(16, 8))

fig.subplots_adjust(right=0.8)
plt.style.use('seaborn-white')

plt.rcParams['axes.grid'] = True
plt.rcParams['axes.grid.which'] = 'both'
plt.rcParams['xtick.minor.visible'] = True

#ResultAnalysis = pd.concat([radiation['glohorrad_Whm2'], SolarData_df['00'], ResultASF_df['00'], SolarData_df['0-45'], ResultASF_df['0-45'],   SolarData_df['045'], ResultASF_df['045']], axis=1)
#
TimePeriod2 = range(4478,4484)

PlotData1 = pd.concat([ResultASF_df['00'][TimePeriod2]/SolarData_df['00'][TimePeriod]], axis = 1)
PlotData1.columns = ['rad00']
PlotData1.plot(ax=axes[1,0], kind='line', title = 'Relative 0/0', legend = False, grid = True)


PlotData2 = pd.concat([ResultASF_df['0-45'][TimePeriod2]/SolarData_df['0-45'][TimePeriod]], axis = 1)
PlotData2.columns = ['rad0_45']
PlotData2.plot(ax=axes[1,1], kind='line', title = 'Relative 0/-45', legend = False, grid = True)


PlotData3 = pd.concat([ResultASF_df['045'][TimePeriod2]/SolarData_df['045'][TimePeriod]], axis = 1)
PlotData3.columns = ['rad045']
PlotData3.plot(ax=axes[1,2], kind='line', title = 'Relative 0/45', legend = False, grid = True)



PlotData3b = pd.concat([ResultASF_df['450'][TimePeriod2]/SolarData_df['450'][TimePeriod]], axis = 1)
PlotData3b.columns = ['rad450']
PlotData3b.plot(ax=axes[1,3], kind='line', title = 'Relative 45/0', legend = False, grid = True)


PlotData3a = pd.concat([ResultASF_df['900'][TimePeriod2]/SolarData_df['900'][TimePeriod]], axis = 1)
PlotData3a.columns = ['rad900']
PlotData3a.plot(ax=axes[1,4], kind='line', title = 'Relative 90/0', legend = False, grid = True)





PlotData6 = pd.concat([ResultASF_df['00'][TimePeriod2],SolarData_df['00'][TimePeriod]], axis = 1)
PlotData6.columns = ['Geo00', 'LB']
PlotData6.plot(ax=axes[0,0], kind='line', title = '0/0', legend = False, grid = True)

PlotData5 = pd.concat([ResultASF_df['0-45'][TimePeriod2],SolarData_df['0-45'][TimePeriod]], axis = 1)
PlotData5.columns = ['Geo0-45', 'LB']
PlotData5.plot(ax=axes[0,1], kind='line', title = '0/-45', legend = False, grid = True)

PlotData4 = pd.concat([ResultASF_df['045'][TimePeriod2],SolarData_df['045'][TimePeriod]], axis = 1)
PlotData4.columns = ['Geo045', 'LB']
PlotData4.plot(ax=axes[0,2], kind='line', title = '0/45', legend = False, grid = True)


PlotData7 = pd.concat([ResultASF_df['450'][TimePeriod2],SolarData_df['450'][TimePeriod]], axis = 1)
PlotData7.columns = ['Geo450', 'LB']
PlotData7.plot(ax=axes[0,3], kind='line', title = '45/0', legend = False, grid = True)

PlotData8 = pd.concat([ResultASF_df['900'][TimePeriod2],SolarData_df['900'][TimePeriod]], axis = 1)
PlotData8.columns = ['Geometrical Model', 'LadyBug']
PlotData8.plot(ax=axes[0,4], kind='line', title = '90/0', legend = False, grid = True)


axes[1,0].set_ylabel('Normalized Radiaiton [-]')
axes[0,0].set_ylabel('Solar Radiation [Wh]')
axes[1,0].set_xlabel('Hour of Year')
axes[1,1].set_xlabel('Hour of Year')
axes[1,2].set_xlabel('Hour of Year')
axes[1,3].set_xlabel('Hour of Year')
axes[1,4].set_xlabel('Hour of Year')
axes[1,0].set_xticks(TimePeriod)
axes[1,1].set_xticks(TimePeriod)
axes[1,2].set_xticks(TimePeriod)
axes[1,3].set_xticks(TimePeriod)
axes[1,4].set_xticks(TimePeriod)
axes[0,0].set_xticks(TimePeriod)
axes[0,1].set_xticks(TimePeriod)
axes[0,2].set_xticks(TimePeriod)
axes[0,3].set_xticks(TimePeriod)
axes[0,4].set_xticks(TimePeriod)
axes[0,4].legend(bbox_to_anchor=(1.05, 0), loc='lower left', borderaxespad=0.)
#axes[1,4].legend(bbox_to_anchor=(1.05, 0), loc='upper left', borderaxespad=0.)

#Percentage_df.to_csv('Percentage_' + str(time.time()) + '.csv')

#fig.savefig(os.path.join(paths['RadModel'], 'SunnyWinterDayComparisonNew.pdf'), format='pdf')
#fig.savefig(os.path.join(paths['RadModel'], 'SunnyWinterDayComparisonNew.png'), format='png')

saveNPY = False

if saveNPY == True:

    np.save('RadPanels_Winter.npy',RadiationASF)    
    np.save('RadWindow_Winter.npy',RadiationWindow)        
	
	
    np.save('PV_Winter.npy',PV_list)    
    np.save('Window_Winter.npy',Window_list)        
    Percentage_df.to_csv('Percentage_' + str(time.time()) + '.csv')

    fig.savefig(os.path.join(paths['RadModel'], 'SunnySummerDay2.pdf'), format='pdf')
    fig.savefig(os.path.join(paths['RadModel'], 'SunnySummerDay2.png'), format='png')


