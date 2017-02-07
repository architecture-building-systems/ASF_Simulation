
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


RadAnalysis = pd.concat([radiation['dirnorrad_Whm2']/LB, radiation['difhorrad_Whm2']/LB,radiation['glohorrad_Whm2']/LB, LB/LB], axis=1)
RadAnalysis.columns = ['direct', 'diffuse', 'global', 'LB']


SunAngles = pd.read_csv(paths['SunAngles'])
SunData = pd.read_csv(paths['SunData'])
SunAngles['Azimuth'] = SunAngles['Azimuth']
PanelPoints = pd.read_csv(paths['PanelData'])

TotalHOY = SunData['HOY'].tolist()



RadiationTilt = {}
RadiationASF = {}
RadiationWindow = {}
Percentage = {}
theta_dict = {}
LatShading = {}
LongShading = {}

#gamma_s = sun azimuth angle
#alpha_s = sun altitude angle

beta = 90       # slope of tilt surface
gamma = 180       # surface azimuth angle, south facing ASF = 180
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

panelSpacing = 500 # in x y dirction[mm]

xArray= 6 # Number of Panels in x direction
yArray= 9 # number of rows


XANGLES = [0,30,45,60]
YANGLES = [-45,0,15,30]

TimePeriod = range(4473,4477)

showFig = True

for HOY in TimePeriod:
    
    RadiationTilt[int(HOY)] = {}
    RadiationASF[int(HOY)] = {}

    
    RadiationWindow[int(HOY)] = {}

    Percentage[HOY] = {}
    theta_dict[HOY] = {}
    LatShading[HOY] = {}
    LongShading[HOY] = {}
    
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
                theta = Theta2directions (sunAlti = SunAngles['Altitude'][ind] , sunAzi = SunAngles['Azimuth'][ind] -180, beta = (beta - x_angle), panelAzi = -y_angle)
                theta_dict[HOY][str(x_angle) + str(y_angle)] = theta
                
                if SunAngles['Azimuth'][ind] > 270 or SunAngles['Azimuth'][ind] < 90:
            
                    #Calculate Radiation on tilt surface
                    Rad_tilt = RadTilt (I_dirnor = 0, I_dif = radiation['difhorrad_Whm2'][HOY], ref = reflectance, theta = np.nan, beta = (beta - x_angle), sunAlti = SunAngles['Altitude'][ind])          
                    RadiationTilt[HOY][str(x_angle) + str(y_angle)] = Rad_tilt
                else:
                    #Calculate Radiation on tilt surface
                    Rad_tilt = RadTilt (I_dirnor = radiation['dirnorrad_Whm2'][HOY], I_dif = radiation['difhorrad_Whm2'][HOY], ref = reflectance, theta = theta, beta = (beta - x_angle), sunAlti = SunAngles['Altitude'][ind])          
                    RadiationTilt[HOY][str(x_angle) + str(y_angle)] = Rad_tilt
               
                
                #Set Sun Position
                sunAz=math.radians(SunAngles['Azimuth'][ind])
                sunAlt=math.radians(SunAngles['Altitude'][ind])
            
            	   #Set Panel Position (note that this should be an array in the future)
                panelAz=math.radians(-y_angle)
                panelAlt=math.radians(x_angle) # beta - x_angle
                
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
                
                ASFArray2 = []
                for ii in range(yArray-1,-1,-1):
            		ASFArray2.append(ASFArray[ii])

            	
                #Calculate Shadow Pattern
                ASF_dict_prime = {}
                count = 0
                shadowData=[]
                for ii,row in enumerate(ASFArray2):
            		shadowData.append([])
    
            		for jj,P in enumerate(row):
           
                  
            			S0,S1,S2,S3,S4=calcShadow(P0 = P, sunAz = sunAz, sunAlt = sunAlt, panelAz = panelAz, panelAlt = panelAlt, h = h, d = DistWindow)
            			shadowData[ii].append([S1,S2,S3,S4])

            			ASF_dict_prime[count] = [S1,S2,S3,S4]
            			count +=1
        
                if showFig == True:
                    #Plot Data
                    for ii,row in enumerate(shadowData):
                		#print 'new row'
                		for jj, Shadow in enumerate(row):
                			#print Shadow
                			x,y = zip(*Shadow)
                			plt.scatter(x,y, c=np.random.rand(3,1))
                			plt.axis('equal')
                    plt.show()
            		
                #Calculate Number of Panels
                PanelNum = len(ASF_dict_prime)
                WindowArea = room_width/1000.0 * room_height/1000.0 * gpH * gpW
                
                if y_angle == 0 and x_angle == 0:
                    Percentage[HOY][str(x_angle) + str(y_angle)] = 1                    
                

                elif SunAngles['Azimuth'][ind] > 270 or SunAngles['Azimuth'][ind] < 90:
    
                    #no direct radiation, therefore no overlap
                    Percentage[HOY][str(x_angle) + str(y_angle)] = 1
                    
                else: 
                    print "\nStart Geometry Analysis"
    
                    if SunAngles['Azimuth'][ind] >= 180: 
                        Percentage[HOY][str(x_angle) + str(y_angle)], LatShading[HOY][str(x_angle) + str(y_angle)], LongShading[HOY][str(x_angle) + str(y_angle)] = CaseA (ind = ind, SunAngles = SunAngles, ASF_dict_prime = ASF_dict_prime, PanelNum = PanelNum, row2 = yArray, col = xArray)
                        
                    elif SunAngles['Azimuth'][ind] < 180: 
                        Percentage[HOY][str(x_angle) + str(y_angle)], LatShading[HOY][str(x_angle) + str(y_angle)], LongShading[HOY][str(x_angle) + str(y_angle)] = CaseB (ind = ind, SunAngles = SunAngles, ASF_dict_prime = ASF_dict_prime, PanelNum = PanelNum, row2 = yArray, col = xArray)
                
                
                #Calculate Radiation on ASF
                RadiationASF[HOY][str(x_angle) + str(y_angle)] = round(PanelNum * (PanelSize**2/10**(6)) * Percentage[HOY][str(x_angle) + str(y_angle)] * RadiationTilt[int(HOY)][str(x_angle) + str(y_angle)] * 0.001 ,3) # area in m2 * Wh/m2 in KWh
                RadiationWindow[HOY][str(x_angle) + str(y_angle)] = round((WindowArea - PanelNum * (PanelSize**2/10**(6)) * Percentage[HOY][str(x_angle) + str(y_angle)]) * RadiationTilt[int(HOY)][str(x_angle) + str(y_angle)] * 0.001 * Percentage[HOY][str(x_angle) + str(y_angle)],3) # area in m2 * Wh/m2 in KWh
               
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



n_panel = 0.1 # 10 Precent


paths = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RadiationModel'
PowerLoss = pd.read_csv(os.path.join(paths, 'powerloss.csv'))
#longitude = pd.read_csv(os.path.join(paths, 'longitude.csv'))
#latitude = pd.read_csv(os.path.join(paths, 'latitude.csv'))

PowerLoss.columns = [range(50)]

#PowerLoss2 = np.matrix(PowerLoss)
#logitude2 = np.matrix(longitude)
#latidude2 = np.matrix(latitude)

Long = np.array(range(0,100,2))/100.
Lat = np.array(range(0,100,2))/100.

Long = Long.tolist()
Lat = Lat.tolist()

import math

def round_up_to_even(number):
    return math.ceil(number / 2.) * 2
    
    
PV = {}
PV2 = {}

for HOY in TimePeriod:
    PV[HOY] = []
    PV2[HOY] = {}
    for x_angle in XANGLES:
        for y_angle in YANGLES:
            
            PV_sum = 0
            if Percentage[HOY][str(x_angle) + str(y_angle)] == 1:
                PV_sum = RadiationASF[HOY][str(x_angle) + str(y_angle)] * n_panel
            else:                
                Radiation = RadiationASF[HOY][str(x_angle) + str(y_angle)]/float(PanelNum)
                LatNum = LatShading[HOY][str(x_angle) + str(y_angle)] 
                LongNum = LongShading[HOY][str(x_angle) + str(y_angle)]
    
                for ind in range(PanelNum):
                    if LatNum[ind] > 0.98:
                        n_shading = 100
                    elif LongNum[ind] > 0.98:
                        n_shading = 100
                    else:
                        valueLat = round_up_to_even(LatNum[ind] *100)
                        lat_index = Lat.index(valueLat/100.)
                    
                        valueLong = round_up_to_even(LongNum[ind] *100)
                        long_index = Lat.index(valueLong/100.)
                    
                        n_shading = PowerLoss[long_index][lat_index]
                    print 'shading', n_shading
                    print 'panel', n_panel
                    print 'Radiaiton', Radiation
                    PV_sum += (n_panel * (1-n_shading/100.) * Radiation) 
                    print 'PV',PV_sum
            PV2[HOY][str(x_angle) + str(y_angle)] = round(PV_sum * 1000,3) 
            PV[HOY].append(round(PV_sum * 1000,3))
                

Hallo = PV2

"""
#ResultAnalysis = pd.concat([radiation['glohorrad_Whm2'], SolarData_df['00'], ResultASF_df['00'], SolarData_df['0-45'], ResultASF_df['0-45'],   SolarData_df['045'], ResultASF_df['045']], axis=1)
#
PlotData1 = pd.concat([SolarData_df['00']/ResultASF_df['00']], axis = 1)
PlotData1.columns = ['rad00']
df = PlotData1[PlotData1.rad00 <= 2]
df.plot()


PlotData2 = pd.concat([SolarData_df['0-45']/ResultASF_df['0-45']], axis = 1)
PlotData2.columns = ['rad0_45']
df = PlotData2[PlotData2.rad0_45 <= 2]
df.plot()


PlotData3 = pd.concat([SolarData_df['045']/ResultASF_df['045']], axis = 1)
PlotData3.columns = ['rad045']
df = PlotData3[PlotData3.rad045 <= 2]
df.plot()


PlotData4 = pd.concat([ResultASF_df['045'],SolarData_df['045'][TimePeriod]], axis = 1)
PlotData4.columns = ['Geo045', 'LB']
PlotData4.plot()

PlotData5 = pd.concat([ResultASF_df['0-45'],SolarData_df['0-45'][TimePeriod]], axis = 1)
PlotData5.columns = ['Geo0-45', 'LB']
PlotData5.plot()

PlotData6 = pd.concat([ResultASF_df['00'],SolarData_df['00'][TimePeriod]], axis = 1)
PlotData6.columns = ['Geo00', 'LB']
PlotData6.plot()

PlotData7 = pd.concat([ResultASF_df['450'],SolarData_df['450'][TimePeriod]], axis = 1)
PlotData7.columns = ['Geo450', 'LB']
PlotData7.plot()

PlotData8 = pd.concat([ResultASF_df['900'],SolarData_df['900'][TimePeriod]], axis = 1)
PlotData8.columns = ['Geo900', 'LB']
PlotData8.plot()

#pathSave = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RadiationModel'
#ResultAnalysis[4200:4400].to_csv(os.path.join(pathSave, 'ResultProPJ.csv'))


"""