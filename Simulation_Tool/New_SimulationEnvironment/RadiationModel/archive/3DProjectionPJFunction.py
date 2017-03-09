
#http://math.stackexchange.com/questions/164700/how-to-transform-a-set-of-3d-vectors-into-a-2d-plane-from-a-view-point-of-anoth



import sys, os
import math
import numpy as np
import pandas as pd
import time

from sympy.solvers import solve
from sympy import Point, Polygon, pi, Symbol
from scipy.optimize import fsolve
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



SunAngles = pd.read_csv(paths['SunAngles'])#, index_col = 0


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
#
panelSpacingDiag = 500 # diagonal


xArray= 6 # Number of Panels in x direction
yArray= 9 # number of rows


XANGLES = [0,15,30,45,60,75,90]
YANGLES = [-45,-30,-15,0,15,30,45]

#Select shading cases which should be evaluated
ShadingCase = ['1','2','3']

shadingPV = True






from ProjectionFunction import CaseA,CaseB, Theta2directions, RadTilt, calcShadow



def PlanarProjection(start, end, XANGLES, YANGLES, xArray, yArray, ShadingCase, panelSpacingDiag, weatherData, SunAngles):
    
    panelSpacing = int(math.sqrt(2*(panelSpacingDiag**2))) # in x y horizontal/ vertical direction[mm]
    
    radiation = weatherData[['year', 'month', 'day', 'hour','dirnorrad_Whm2', 'difhorrad_Whm2','glohorrad_Whm2']]
    SunAngles['Azimuth'] = SunAngles['Azimuth']-180

    TotalHOY = SunAngles['HOY'].tolist()
    
    
    RadiationASF = {}
    RadiationWindow = {}
    Percentage = {}
    
    LatShading = {}
    LongShading = {}
    
    WindowTilt = {}
    RadiationTilt = {}
    
    for HOY in [start, end + 1]:
        
    	RadiationTilt[HOY] = {}
    	RadiationASF[HOY] = {}
    	WindowTilt[HOY] = {}    
    	RadiationWindow[HOY] = {}
    	Percentage[HOY] = {}
    	LatShading[HOY] = {}
    	LongShading[HOY] = {}
    	
    	
    	if HOY in TotalHOY:
    		
    		ind = TotalHOY.index(HOY)
    			
    		for x_angle in XANGLES:
    			for y_angle in YANGLES:
    				
    				
    				print '\nStart Calculation'
    				print 'Time: ' + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
    				tic = time.time()
    
    					
    				#Calculate angle of incidence
    				#Angle Definition: -90 East, 0 South, 90 West
    				theta = Theta2directions (sunAlt = SunAngles['Altitude'][ind] , sunAzi = SunAngles['Azimuth'][ind], panelAlt = (90 - x_angle), panelAzi = -y_angle)
    				thetaWindow = Theta2directions (sunAlt = SunAngles['Altitude'][ind] , sunAzi = SunAngles['Azimuth'][ind], panelAlt = 90, panelAzi = 0)
        
    					
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
    				ASFArray2 = [] 
    				for ii in range(yArray-1,-1,-1):
    					ASFArray2.append(ASFArray[ii])
    
        				
    				#Calculate Shadow Pattern on projection plane
    				ASF_Projection = {}
    				count = 0
    				shadowData=[]
    				for ii,row in enumerate(ASFArray2):
    					shadowData.append([])
    	
    					for jj,P in enumerate(row):
    		   
    						S0,S1,S2,S3,S4, DeltaY, DeltaX =calcShadow(P0 = P, sunAz = math.radians(SunAngles['Azimuth'][ind]), sunAlt = math.radians(SunAngles['Altitude'][ind]), 
                                                                panelAz = -math.radians(y_angle), panelAlt = math.radians(x_angle), h = h, d = DistWindow)
                                                                
    						shadowData[ii].append([S1,S2,S3,S4])
    
    						ASF_Projection[count] = [S1,S2,S3,S4] 
    						count +=1
    		
    
    				PanelNum = len(ASF_Projection)
    				WindowArea = room_width/1000.0 * room_height/1000.0 * gpH * gpW
    				ASFArea = PanelNum * PanelSize**2/(10**(6))
    
    				
    				print 'time passed before overlap', time.time()-tic
    				if SunAngles['Azimuth'][ind] > 90 or SunAngles['Azimuth'][ind] < -90:
    					#no direct radiation, therefore no overlap
    					Percentage[HOY][str(x_angle) + str(y_angle)] = 1
    	
    				
    				else: 
    					print "\nStart Geometry Analysis"
    					print "Sun Angle Is", SunAngles['Azimuth'][ind]
    					print 'HOY', HOY
    			
    					print str(x_angle), str(y_angle)
         
    					if SunAngles['Azimuth'][ind] >= 0: 
    						Percentage[HOY][str(x_angle) + str(y_angle)], LatShading[HOY][str(x_angle) + str(y_angle)], LongShading[HOY][str(x_angle) + str(y_angle)] = CaseA (ind = ind, SunAngles = SunAngles, ASF_dict_prime = ASF_Projection, PanelNum = PanelNum, row2 = yArray, col = xArray, Case = ShadingCase)
    						
    					elif SunAngles['Azimuth'][ind] < 0: 
    						Percentage[HOY][str(x_angle) + str(y_angle)], LatShading[HOY][str(x_angle) + str(y_angle)], LongShading[HOY][str(x_angle) + str(y_angle)] = CaseB (ind = ind, SunAngles = SunAngles, ASF_dict_prime = ASF_Projection, PanelNum = PanelNum, row2 = yArray, col = xArray, Case = ShadingCase)
    
                            #calculate the ASF area reduction respective to is its positon and the sun postion
    				ReductionASF = np.cos(math.radians(x_angle)- math.radians(SunAngles['Altitude'][ind])) * np.cos(-math.radians(y_angle) - math.radians(SunAngles['Azimuth'][ind]))
    				
    				#calculate Radiation on the window surface, take into account ASF rduction area and the amount of shading    
    				RadiationWindow[HOY][str(x_angle) + str(y_angle)] = (WindowArea - ASFArea* ReductionASF)*Percentage[HOY][str(x_angle) + str(y_angle)] * WindowTilt[HOY][str(x_angle) + str(y_angle)] * 0.001    				
        
    				#Calculate Radiation on ASF
    				RadiationASF[HOY][str(x_angle) + str(y_angle)] = ASFArea* Percentage[HOY][str(x_angle) + str(y_angle)] * RadiationTilt[int(HOY)][str(x_angle) + str(y_angle)] * 0.001 # area in m2 * Wh/m2 in KWh
    				
    				toc = time.time() - tic
    				print 'time passed (sec): ' + str(round(toc,2))
    		
    	else:
    		print 'HOY', HOY
    		print 'No Radiation'
    		# case with no radiation
    		for x_angle in XANGLES:
    			for y_angle in YANGLES:
    						
    				RadiationASF[HOY][str(x_angle) + str(y_angle)] = 0
    				RadiationWindow[HOY][str(x_angle) + str(y_angle)] = 0
    				Percentage[HOY][str(x_angle) + str(y_angle)] = 1
      
    				
    
    
    
    
    return RadiationASF, RadiationWindow, Percentage, LatShading, LongShading




def pvProductionPlanarProjeciton(start, end, PanelNum, RadiationASF, RadiationWindow, Percentage,  LatShading, LongShading, shadingPV, paths, FileName):

        PowerLoss = pd.read_csv(os.path.join(paths['RadModel'], 'powerloss.csv'))
        PowerLoss.columns = [range(50)]

        n_panel = 0.1 # 10 Precent
        
        Long = np.array(range(0,100,2))/100.
        Lat = np.array(range(0,100,2))/100.
        
        Long = Long.tolist()
        Lat = Lat.tolist()
        
        
        
        def round_up_to_even(number):
        	return math.ceil(number/ 2.) * 2
        
        
        	
        PV_List = {}
        Window_List = {}
        shading_loss = {}
        
        
        
        for HOY in [start, end + 1]:
        	
        	PV_List[HOY] = np.array([])
        	Window_List[HOY] = np.array([])
        	shading_loss[HOY] = {}
        	
        	
        	for x_angle in XANGLES:
        		for y_angle in YANGLES:
              
        			shading_loss[HOY][str(x_angle) + str(y_angle)] = {}
        			
        			PV_sum = 0
        			if Percentage[HOY][str(x_angle) + str(y_angle)] == 1:
                             #No Shading
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
        					
        					if shadingPV == True:
        						
        						PV_sum += (n_panel * (1-n_shading/100.) * Radiation) 
        						
        					else:
        						PV_sum += (n_panel * 1 * Radiation) 
        						
        			
        			PV_List[HOY] = np.append(PV_List[HOY], PV_sum * 1000) # in Wh
        			Window_List[HOY] = np.append(Window_List[HOY], RadiationWindow[HOY][str(x_angle) + str(y_angle)] * 1000) # in Wh
           
        np.save(os.path.join('PV' + '_' + FileName + '.npy',PV_List))    
        np.save(os.path.join('WindowRadiation' + '_' + FileName + '.npy.',Window_List))

        return PV_List, Window_List, shading_loss



ResultASF_df = pd.DataFrame(RadiationASF).T
ResultWindow_df = pd.DataFrame(RadiationWindow).T
PercentageNonShaded_df = pd.DataFrame(Percentage).T


ResultASF_df.to_csv('ASFFinal.csv')
ResultWindow_df.to_csv('WindowFinal.csv')





saveNPY = False

if saveNPY == True:

    np.save('RadPanels_Final.npy',RadiationASF)    
    np.save('RadWindow_Final.npy',RadiationWindow)        
	
	
            
    #Percentage_df.to_csv('Percentage_' + str(time.time()) + '.csv')

#    fig.savefig(os.path.join(paths['RadModel'], 'SunnySum2.pdf'), format='pdf')
#    fig.savefig(os.path.join(paths['RadModel'], 'SunnySum2.png'), format='png')


