
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

paths['weather'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\WeatherData'
paths['scirpt'] =  r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\python'
paths['location'] = os.path.join(paths['weather'], geoLocation)
paths['SunData'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RadiationModel\SunPosition2.csv'
paths['PanelData'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RadiationModel\PanelPostion.csv'
paths['SunAngles'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RadiationModel\SunAngles.csv'
paths['Save'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RadiationModel'

sys.path.insert(0, paths['scirpt'])
						
from epwreader import epw_reader
#read epw file of needed destination
weatherData = epw_reader(paths['location'])
radiation = weatherData[['year', 'month', 'day', 'hour','dirnorrad_Whm2', 'difhorrad_Whm2','glohorrad_Whm2']]

from ProjectionFunction import CaseA,CaseB




def Theta2directions (sunAlti, sunAzi , beta, panelAzi):

    sunAlti = np.deg2rad(sunAlti)
    beta = np.deg2rad(beta) # panelAlti
    sunAzi = np.deg2rad(sunAzi)
    panelAzi = np.deg2rad(panelAzi)
    
      
    theta2 = np.arccos(np.cos(sunAlti) * np.cos(sunAzi-panelAzi) * np.sin(beta) + np.sin(sunAlti)* np.cos(beta))
    
    if sunAzi >= np.deg2rad(90) or sunAzi <= np.deg2rad(-90):
        theta2 = np.nan
    else:
        theta2 = np.rad2deg(theta2)
   
    return theta2 # deg



def RadTilt (I_dirnor, I_dif, ref, theta, beta, sunAlti):
    #calculate radiation on tilt surface
    theta = np.deg2rad(theta)
    beta = np.deg2rad(beta)
    alpha_s = np.deg2rad(sunAlti)

    I_tot = I_dif + I_dirnor * np.sin(alpha_s)
    
    if theta == np.nan:
        Rad_tilt = I_dif * ((1+np.cos(beta))/2) + I_tot * ref * ((1- np.cos(beta))/2)    
    else:
        Rad_tilt = I_dirnor * np.cos(theta) + I_dif * ((1+np.cos(beta))/2) + I_tot * ref * ((1- np.cos(beta))/2)
    
    if Rad_tilt < 0:
        Rad_tilt = np.nan
    
    return Rad_tilt # W/m2
    


  
def calcShadow(P0,sunAz,sunAlt,panelAz,panelAlt,h,d):
	

	#Calculate Centre of Shadow
	S0=[0,0] #initialise Centre of Shadow
	S0[0]=P0[0]+d*math.tan(sunAz)
	S0[1]=P0[1]-d*math.tan(sunAlt)


	#Calcuate the contraction or expansion of the shadow in the x and y directions due to the actuation
	#The difference is relative to the flat panel position
	y=(math.sin(sunAlt-panelAlt/2)/(math.sin(math.pi/2-sunAlt)))*h*math.sin(panelAlt/2) 
	#print y
	x=(math.sin(sunAz-panelAz/2)/(math.sin(math.pi/2-sunAz)))*h*math.sin(panelAz/2)
	#print x

	
#	     S2
#	    /\
#	   /S0\
#	S1 \' / S2
#	    \/
#	    S4  
	
	S2=[S0[0], S0[1]+h+y] # changed not dividing through 2
	S3=[S0[0]+h+x,S0[1]]
	S4=[S0[0], S0[1]-h-y]
	S1=[S0[0]-h-x,S0[1]]


	return S0,S1,S2,S3,S4

    
    

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

WindowArea = {}
WindowProArea = {}
WindowRadiation = {}

Percentage = {}


#gamma_s = sun azimuth angle
#alpha_s = sun altitude angle

beta = 90       # slope of tilt surface
gamma = 180       # surface azimuth angle, south facing ASF = 180
ref = 0         # reflectivity # 0.2



PanelNum = len(PanelPoints)/4

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


XANGLES = [0]
YANGLES = [-45,0,45]

TimePeriod = range(4051,4070)

showFig = False

for HOY in TimePeriod:
    
    RadiationTilt[int(HOY)] = {}
    RadiationASF[int(HOY)] = {}

    WindowArea[int(HOY)] = {}
    WindowProArea[int(HOY)] = {}
    WindowRadiation[int(HOY)] = {}

    Percentage[HOY] = {}
    
    if HOY in TotalHOY:
        
        ind = TotalHOY.index(HOY)
            
        for x_angle in XANGLES:
            for y_angle in YANGLES:
                
                if x_angle == 0 and y_angle == 0 and SunAngles['Azimuth'][ind] > 89 and SunAngles['Azimuth'][ind] < 91:
                    print 'Break', x_angle, SunAngles['Azimuth'][ind]                    
                    continue
                else:
                       
                
                    print '\nStart Calculation'
                    print 'Time: ' + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
                    
                    print 'HOY', HOY
                    print 'ii', ind
                    
                    tic = time.time()
                    
                    print str(x_angle), str(y_angle)
                                    
                    
                    #Calculate angle of incidence
                    theta = Theta2directions (sunAlti = SunAngles['Altitude'][ind] , sunAzi = SunAngles['Azimuth'][ind] -180, beta = (beta - x_angle), panelAzi = -y_angle)
            
                    #Calculate Radiation on tilt surface
                    Rad_tilt = RadTilt (I_dirnor = radiation['dirnorrad_Whm2'][HOY], I_dif = radiation['difhorrad_Whm2'][HOY], ref = ref, theta = theta, beta = (beta - x_angle), sunAlti = SunAngles['Altitude'][ind])          
                    RadiationTilt[int(HOY)][str(x_angle) + str(y_angle)] = Rad_tilt
                   
                    
                    #Set Sun Position
                    sunAz=math.radians(SunAngles['Azimuth'][ind])
                    sunAlt=math.radians(SunAngles['Altitude'][ind])
                
                	   #Set Panel Position (note that this should be an array in the future)
                    panelAz=math.radians(y_angle)
                    panelAlt=math.radians(y_angle)
                    
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
               
                      
                			S0,S1,S2,S3,S4=calcShadow(P= P, sunAz = sunAz, sunAlt = sunAlt, panelAz = panelAz, panelAlt = panelAlt, h = h, d = DistWindow)
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
                			
                   
                   
                    print "\nStart Geometry Analysis"
                    
                    if SunAngles['Azimuth'][ind] > 270 or SunAngles['Azimuth'][ind] < 90:
        
                        #no direct radiation, therefore no overlap
                        Percentage[HOY][str(x_angle) + str(y_angle)] = 1
                        continue
                    
                    else: 
        
                        if SunAngles['Azimuth'][ind] >= 180: 
                            Percentage[HOY][str(x_angle) + str(y_angle)] = CaseA (ind = ind, SunAngles = SunAngles, ASF_dict_prime = ASF_dict_prime, PanelNum = PanelNum, row2 = yArray, col = xArray)
                            
                        elif SunAngles['Azimuth'][ind] < 180: 
                            Percentage[HOY][str(x_angle) + str(y_angle)] = CaseB (ind = ind, SunAngles = SunAngles, ASF_dict_prime = ASF_dict_prime, PanelNum = PanelNum, row2 = yArray, col = xArray)
  
                    #Calculate Radiation on ASF
                    RadiationASF[int(HOY)][str(x_angle) + str(y_angle)] = round(PanelNum * (PanelSize**2/10**(-6)) * RadiationTilt[int(HOY)][str(x_angle) + str(y_angle)] * 0.001 * Percentage[HOY][str(x_angle) + str(y_angle)],3) # area in m2 * Wh/m2 in KWh
                   
                   
                    toc = time.time() - tic
                    print 'time passed (sec): ' + str(round(toc,2))
        
    else:
        print 'HOY', HOY
        print 'No Radiation'
        # case with no radiation
        for x_angle in XANGLES:
            for y_angle in YANGLES:
                        
                RadiationASF[int(HOY)][str(x_angle) + str(y_angle)] = 0
                Percentage[HOY][str(x_angle) + str(y_angle)] = np.nan
       
  
ResultASF_df = pd.DataFrame(RadiationASF).T
ResultWindow_df = pd.DataFrame(WindowRadiation).T



ResultAnalysis = pd.concat([radiation['glohorrad_Whm2'], SolarData_df['00'], ResultASF_df['00'], SolarData_df['0-45'], ResultASF_df['0-45'],   SolarData_df['045'], ResultASF_df['045']], axis=1)

PlotData1 = pd.concat([np.abs(SolarData_df['00'] -ResultASF_df['00'])/SolarData_df['00']], axis = 1)
PlotData1 = pd.concat([SolarData_df['00']/ResultASF_df['00']], axis = 1)
PlotData1.columns = ['rad1']
df = PlotData1[PlotData1.rad1 <= 2]

df.plot()

PlotData2 = pd.concat([SolarData_df['0-45']/ResultASF_df['0-45']], axis = 1)
PlotData2.columns = ['rad2']
df = PlotData2[PlotData2.rad2 <= 2]
df.plot()


PlotData3 = pd.concat([SolarData_df['045']/ResultASF_df['045']], axis = 1)
PlotData3.columns = ['rad3']
df = PlotData3[PlotData3.rad3 <= 2]
df.plot()


PlotData4 = pd.concat([ResultASF_df['045'],SolarData_df['045']], axis = 1)
PlotData4.columns = ['Geo', 'LB']
PlotData4.plot()

PlotData5 = pd.concat([ResultASF_df['0-45'],SolarData_df['0-45']], axis = 1)
PlotData5.columns = ['Geo', 'LB']
PlotData5.plot()






#pathSave = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RadiationModel'
#ResultAnalysis[4200:4400].to_csv(os.path.join(pathSave, 'ResultProPJ.csv'))


