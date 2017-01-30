
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



def ThetaAngle (alpha_s, gamma_s, beta, gamma):

    theta_z = 90 - alpha_s 

    theta_z = np.deg2rad(theta_z)
    beta = np.deg2rad(beta)
    gamma_s = np.deg2rad(gamma_s)
    gamma = np.deg2rad(gamma)
    
      
    theta = np.arccos(np.cos(theta_z) * np.cos(beta) + np.sin(theta_z)* np.sin(beta) * np.cos(gamma_s -gamma))
   
    theta = np.rad2deg(theta)
   
    return theta # deg


def RadTilt (I_dirnor, I_dif, ref, theta, beta, alpha_s):
    #calculate radiation on tilt surface
    theta = np.deg2rad(theta)
    beta = np.deg2rad(beta)
    alpha_s = np.deg2rad(alpha_s)

    I_tot = I_dif + I_dirnor * np.sin(alpha_s)
    
    Rad_tilt = I_dirnor * np.cos(theta) + I_dif * ((1+np.cos(beta))/2) + I_tot * ref * ((1- np.cos(beta))/2)
    
    if Rad_tilt < 0:
        Rad_tilt = np.nan
    
    return Rad_tilt # W/m2
    
#test = ThetaAngle(alpha_s = 57.5, gamma_s = -55.5, beta = 25, gamma = 45)
#
#print 'Test', test # value 43.69 deg
  
    

def ProjPlane(S1, n): #needed
        # S1 Start Point
        # n sun vector
    
    S = {1: np.array(S1), 2: np.array(n)}
    
    def FunctionSolv(w, S):
        x = w[0]
        y = w[1]
        z = w[2]
        
        size = 5000.
        
        S1 = S[1]
        n = S[2]
        
        F = np.empty((3))
        F[0] = np.sqrt(pow(x-S1[0],2)+pow(y-S1[1],2) + pow(z-S1[2],2))-size
        F[1] = n[0]*x + n[1]*y + n[2]*z - 0
        F[2] = z -10
        return F
    
    


    zGuess = np.array([1,1,1])
    w = fsolve(FunctionSolv, zGuess, S)
   
    
    return w

  
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

	"""
	     S2
	    /\
	   /S0\
	S1 \' / S2
	    \/
	    S4  
	"""
	S2=[S0[0], S0[1]+h+y] # changed not dividing through 2
	S3=[S0[0]+h+x,S0[1]]
	S4=[S0[0],S0[1]-h-y]
	S1=[S0[0]-h-x,S0[1]]


	return S0,S1,S2,S3,S4

def DisPoints (P1,P2):
    distance = np.sqrt( (P1[0]-P2[0])**2 + (P1[1]-P2[1])**2 + (P1[2]-P2[2])**2)
    #print distance    
    return distance


def Area(Dict):
    #calcualte area of polygon
    ListASF = Dict
    p1, p2, p3, p4 = map(Point, [(ListASF[0][0], ListASF[0][1]), (ListASF[1][0], ListASF[1][1]), 
                             (ListASF[2][0], ListASF[2][1]), (ListASF[3][0], ListASF[3][1])])
    poly1 = Polygon(p1, p2, p3, p4)
    
    resultASF = abs(round(float(poly1.area),2)) #mm2
    return resultASF

def Area3D(poly):
#calculate area of 3D polygon
#determinant of matrix a
    def det(a):
        return np.linalg.det(a)
    
    #unit normal vector of plane defined by points a, b, and c
    def unit_normal(a, b, c):
        x = det([[1,a[1],a[2]],
                 [1,b[1],b[2]],
                 [1,c[1],c[2]]])
        y = det([[a[0],1,a[2]],
                 [b[0],1,b[2]],
                 [c[0],1,c[2]]])
        z = det([[a[0],a[1],1],
                 [b[0],b[1],1],
                 [c[0],c[1],1]])
        magnitude = (x**2 + y**2 + z**2)**.5
        return (x/magnitude, y/magnitude, z/magnitude)
    
    #dot product of vectors a and b
    def dot(a, b):
        return np.dot(a,b)
    
    #cross product of vectors a and b
    def cross(a, b):

        return np.cross(a,b)
    
    #area of polygon poly
    def area(poly):
        if len(poly) < 3: # not a plane - no area
            return 0
    
        total = [0, 0, 0]
        for i in range(len(poly)):
            vi1 = poly[i]
            if i is len(poly)-1:
                vi2 = poly[0]
            else:
                vi2 = poly[i+1]
            prod = cross(vi1, vi2)
            total[0] += prod[0]
            total[1] += prod[1]
            total[2] += prod[2]
        result = dot(total, unit_normal(poly[0], poly[1], poly[2]))
        return result
        
    result = area(poly)
    
    return round(abs(result/2),0) #* 10**(-6) #m2       
    
    

#Load LB-Files
SolarData = np.load(os.path.join(paths['Save'], 'SolarData.npy')).item()
SolarData_df = pd.DataFrame(SolarData)
SolarData2 = np.load(os.path.join(paths['Save'], 'SolarData2.npy')).item()
SolarData_df2 = pd.DataFrame(SolarData2)
SolarData3 = np.load(os.path.join(paths['Save'], 'SolarData3.npy')).item()
SolarData_df3 = pd.DataFrame(SolarData3)

SolarData_df = pd.concat([SolarData_df,SolarData_df2, SolarData_df3], axis=1)
LB = SolarData_df['00'] * 1000 / (50*0.4*0.4) # kWh in Wh divided through area of panels in m2

WindowDataLB = np.load(os.path.join(paths['Save'], 'BuildingData.npy')).item()
BuildingRadLB_df = pd.DataFrame(WindowDataLB)


RadData_df = pd.concat([radiation, LB], axis=1)

start = 0
end = 8760
RadAnalysis = pd.concat([radiation['dirnorrad_Whm2']/LB, radiation['difhorrad_Whm2']/LB,radiation['glohorrad_Whm2']/LB, LB/LB], axis=1)
RadAnalysis.columns = ['direct', 'diffuse', 'global', 'LB']

#RadAnalysis[start:end].plot(kind='line', title = 'Radiation Analysis', grid = True) 



SunAngles = pd.read_csv(paths['SunAngles'])
SunData = pd.read_csv(paths['SunData'])
SunAngles['Azimuth'] = SunAngles['Azimuth']

Sun = pd.concat([SunAngles, SunData], axis = 1)

PanelPoints = pd.read_csv(paths['PanelData'])



TotalHOY = SunData['HOY'].tolist()


room_height = 3100.
room_depth = 7000.
room_width = 4900.

gpW =  0.92 #glazing_percentage_w
gpH =  0.97 #glazing_percentage_h

PanelSize = 400. #mm
    
Hyp = np.sin(np.deg2rad((45)))*PanelSize
DistWindow = 100. # distance of panels from Window surface

        
xR = 0 
yR = 1 
zR = 0



#gamma_s = sun azimuth angle
#alpha_s = sun altitude angle

beta = 90       # slope of tilt surface
gamma = 180       # surface azimuth angle, south facing ASF = 180
ref = 0         # reflectivity




TotalArea = {}
RadTilt_dict = {}
RadASF_dict = {}
WindowArea = {}
WindowProArea = {}
WindowRadiation = {}

PanelNum = len(PanelPoints)/4
#PanelNum = 7

row2 = 9
col = 6



showFig = False


XANGLES = [0,15,30,45,60,75,90]
YANGLES = [-45,-30,-15,0,15,30,45]

for HOY in range(4460,4486):
    
    RadTilt_dict[int(HOY)] = {}
    RadASF_dict[int(HOY)] = {}
    TotalArea[int(HOY)] = {}
    WindowArea[int(HOY)] = {}
    WindowProArea[int(HOY)] = {}
    WindowRadiation[int(HOY)] = {}
    
    if HOY in TotalHOY:
        
        ii = TotalHOY.index(HOY)
            

        #Calculate angle of incidence
        theta = ThetaAngle(alpha_s = SunAngles['Altitude'][ii], gamma_s = SunAngles['Azimuth'][ii], beta = beta, gamma = gamma)
        
        #Calculate Radiation on tilt surface
        Rad_tilt = RadTilt (I_dirnor = radiation['dirnorrad_Whm2'][HOY], I_dif = radiation['difhorrad_Whm2'][HOY], ref = ref, theta = theta, beta = beta, alpha_s = SunAngles['Altitude'][ii])          
        RadTilt_dict[int(HOY)] = Rad_tilt
        
        SunVec = np.array([SunData['xV'][ii], SunData['yV'][ii], SunData['zV'][ii]])
#        SunPos = np.array([SunData['xP'][ii], SunData['yP'][ii], SunData['zP'][ii]])
    
        print 'Altitude', SunAngles['Altitude'][ii]
        print 'Azimuth', SunAngles['Azimuth'][ii]
        
        for x_angle in XANGLES:
            for y_angle in YANGLES:
                
                print '\nStart Calculation'
                print 'Time: ' + time.strftime("%Y_%m_%d %H.%M.%S", time.localtime())
                
                print 'HOY', HOY
                print 'ii', ii
                
                tic = time.time()
                
                print str(x_angle), str(y_angle)
                                
                
                


            	#Set Panel Properties
                h=math.sqrt(2*(400/2)**2) #distance from centre of panel to corner [mm]
                d=300 #Distance from the Glazed Surface
            
            	#Calculate ASF Geometry
            	#The adaptive solar facade is represented by an array of coordinates and panel size
                panelSpacing=600 # in x y dirction[mm]
            
                xArray= 6 # Number of Panels in x direction
                yArray= 9 # number of rows
             
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
                count2 = 0
                ASFArray2 = []
                for ii in range(yArray-1,-1,-1):
            		ASFArray2.append(ASFArray[ii])

            	#Set Sun Position
                sunAz=math.radians(SunAngles['Azimuth'][ii])
                sunAlt=math.radians(SunAngles['Altitude'][ii])
            
            	#Set Panel Position (note that this should be an array in the future)
                panelAz=math.radians(y_angle)
                panelAlt=math.radians(y_angle)
            
                
                #Calculate Shadow Pattern
                
                ASF_dict_prime = {}
                count = 0
                shadowData=[]
                for ii,row in enumerate(ASFArray2):
            		shadowData.append([])
    
            		for jj,P in enumerate(row):
           
                  
            			S0,S1,S2,S3,S4=calcShadow(P,sunAz,sunAlt,panelAz,panelAlt,h,d)
            			shadowData[ii].append([S1,S2,S3,S4])
#            			ASF_dict_prime[count]= []

            			ASF_dict_prime[count] = [S1,S2,S3,S4]
            			count +=1
        
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
                
                Shadow = {}
                ASFArea = {}
                
                if SunAngles['Azimuth'][ii] >= 180: 
                    print '\nCase 1a'
                    
                    print 'Sun Azimuth:', SunAngles['Azimuth'][ii]
                    
                    result1 = Area(Dict = ASF_dict_prime[0])
                    print "\nASF:  0", "- Area: ", result1
                    print "Intersection with panel to the left: No"
                    
                   
                    Shadow[0] = 0
                    ASFArea[0] = result1
                    
                    SumArea = 0
                     
                    for ii in range(1,PanelNum):
                        
                        #case: if far right point of panel is within the panel to the right
                        p = Polygon((ASF_dict_prime[ii][0][0],ASF_dict_prime[ii][0][1]),
                                    (ASF_dict_prime[ii][1][0],ASF_dict_prime[ii][1][1]),
                                    (ASF_dict_prime[ii][2][0],ASF_dict_prime[ii][2][1]),
                                    (ASF_dict_prime[ii][3][0],ASF_dict_prime[ii][3][1]))
                        
                        if p.encloses_point(Point(ASF_dict_prime[ii-1][2][0], ASF_dict_prime[ii-1][2][1])):
                            #if Point is in polygon p, than true will be returned
                            #test if far right point of asf porjection lies in the panel right to the existing one
                            
                            #Calculate Intersection     
                           
                            p1, p2, p3, p4 = map(Point, [(ASF_dict_prime[ii][0][0], ASF_dict_prime[ii][0][1]), (ASF_dict_prime[ii][1][0], ASF_dict_prime[ii][1][1]), 
                                                 (ASF_dict_prime[ii][2][0], ASF_dict_prime[ii][2][1]), (ASF_dict_prime[ii][3][0], ASF_dict_prime[ii][3][1])])
                    
                    
                            p5, p6, p7, p8 = map(Point, [(ASF_dict_prime[ii-1][0][0], ASF_dict_prime[ii-1][0][1]), (ASF_dict_prime[ii-1][1][0], ASF_dict_prime[ii-1][1][1]),
                                                 (ASF_dict_prime[ii-1][2][0], ASF_dict_prime[ii-1][2][1]), (ASF_dict_prime[ii-1][3][0], ASF_dict_prime[ii-1][3][1])])
                    
                            poly1 = Polygon(p1, p2, p3, p4)
                            poly2 = Polygon(p5, p6, p7, p8)
                    
                            a =  poly1.intersection(poly2)
                            SP1 = a[0]
                            SP2 = a[1]
                            
                            
                            resultShadow = abs(Polygon((SP2[0],SP2[1]), (ASF_dict_prime[ii-1][2][0], ASF_dict_prime[ii-1][2][1]), (SP1[0],SP1[1]),
                                        (ASF_dict_prime[ii][0][0], ASF_dict_prime[ii][0][1])).area)
                            
                            resultASF = abs(poly1.area)
                            
                            totalArea = resultASF - resultShadow
                    
                            Shadow[ii]= float(resultShadow)
                            ASFArea[ii] = resultASF
                            
                            SumArea += resultASF            
                            print "ASF: ", ii , "- Area: ", round(totalArea,3)
                            print "Intersection with panel to the left: Yes"    
                            
                        else:
                            
                                                        
                            result = Area(Dict = ASF_dict_prime[ii])
                            print "ASF: ", ii , "- Area: ", round(result,3)
                            print "Intersection with panel to the left: No"
                            
                            SumArea += result 
                        
                            Shadow[ii]= 0 
                            ASFArea[ii] = result
                
                    print '\nCase 2a'
                    for ii in range(1,row2): #2
                        #case: check if the lowest edge of  a panel is intersection with panel below
                        for colNum in range(col): #4
                        
                                            
                            if (colNum + ii *col) < PanelNum: #skip the last panels 
                            
                                p = Polygon((ASF_dict_prime[colNum + ii *col][0][0],ASF_dict_prime[colNum + ii *col][0][1]),
                                            (ASF_dict_prime[colNum + ii *col][1][0],ASF_dict_prime[colNum + ii *col][1][1]),
                                            (ASF_dict_prime[colNum + ii *col][2][0],ASF_dict_prime[colNum + ii *col][2][1]),
                                            (ASF_dict_prime[colNum + ii *col][3][0],ASF_dict_prime[colNum + ii *col][3][1]))
                
                            
                                if p.encloses_point(Point(ASF_dict_prime[(colNum + (ii-1) *col)][3][0], ASF_dict_prime[(colNum + (ii-1) *col)][3][1])):
                                    #if Point is in polygon p, than true will be returned
                                
        #                            print 'Num Check Panel', str(colNum + ii *col)
        #                            print 'Num2 Panel above', str(colNum + (ii-1) *col)
        
                                    #Calculate Intersection               
                                    p1, p2, p3, p4 = map(Point, [(ASF_dict_prime[colNum + ii *col][0][0], ASF_dict_prime[colNum + ii *col][0][1]), (ASF_dict_prime[colNum + ii *col][1][0], ASF_dict_prime[colNum + ii *col][1][1]), 
                                                         (ASF_dict_prime[colNum + ii *col][2][0], ASF_dict_prime[colNum + ii *col][2][1]), (ASF_dict_prime[colNum + ii *col][3][0], ASF_dict_prime[colNum + ii *col][3][1])])
                            
                            
                                    p5, p6, p7, p8 = map(Point, [(ASF_dict_prime[(colNum + (ii-1) *col)][0][0], ASF_dict_prime[(colNum + (ii-1) *col)][0][1]), (ASF_dict_prime[(colNum + (ii-1) *col)][1][0], ASF_dict_prime[(colNum + (ii-1) *col)][1][1]),
                                                         (ASF_dict_prime[(colNum + (ii-1) *col)][2][0], ASF_dict_prime[(colNum + (ii-1) *col)][2][1]), (ASF_dict_prime[(colNum + (ii-1) *col)][3][0], ASF_dict_prime[(colNum + (ii-1) *col)][3][1])])
                            
                                    poly1 = Polygon(p1, p2, p3, p4)
                                    poly2 = Polygon(p5, p6, p7, p8)
                            
                                    a =  poly1.intersection(poly2)
                                    SP1 = a[0]
                                    SP2 = a[1]
                                    
                                           
                                    
                                    resultShadow2 = abs(10**(-6)* Polygon((SP2[0],SP2[1]), (ASF_dict_prime[colNum + ii *col][1][0], ASF_dict_prime[colNum + ii *col][1][1]), (SP1[0],SP1[1]),
                                                             (ASF_dict_prime[(colNum + (ii-1) *col)][3][0], ASF_dict_prime[(colNum + (ii-1) *col)][3][1])).area)
                            
                                            
                                    Shadow[colNum + ii *col] += float(resultShadow2)
                            
                                        
                                    print "ASF: ", colNum + ii *col
                                    print "Intersection with upper panel: Yes"    
                                    
            
                                    
                                else:
                                    result1 = Area(Dict = ASF_dict_prime[colNum + ii *col])
                                    print "ASF: ", colNum + ii *col
                                    print "Intersection with upper panel: No"
                                    Shadow[colNum + ii *col]+= 0
                            else:
                                pass
                        
                
                elif SunAngles['Azimuth'][ii] < 180: 
                    print '\nCase 1b'
                    
                    print '\nSun Azimuth:', SunAngles['Azimuth'][ii]
                    
                    result1 = Area(Dict = ASF_dict_prime[49])
                    print "ASF:  49", "- Area: ", result1
                    print "Intersection with panel to the right: No"
                    
                    Shadow[49] = 0
                    ASFArea[49] = result1
                    
                                        
                    SumArea = 0
                     
                    for ii in range(1,PanelNum):
                        #case: if far left point of panel is within the panel to the left
                        p = Polygon((ASF_dict_prime[ii-1][0][0],ASF_dict_prime[ii-1][0][1]),
                                    (ASF_dict_prime[ii-1][1][0],ASF_dict_prime[ii-1][1][1]),
                                    (ASF_dict_prime[ii-1][2][0],ASF_dict_prime[ii-1][2][1]),
                                    (ASF_dict_prime[ii-1][3][0],ASF_dict_prime[ii-1][3][1]))
                        
                        if p.encloses_point(Point(ASF_dict_prime[ii][0][0], ASF_dict_prime[ii][0][1])):
                            #if Point is in polygon p, than true will be returned
                            #test if far right point of asf porjection lies in the panel right to the existing one
                            
                            #Calculate Intersection     
                           
                            p1, p2, p3, p4 = map(Point, [(ASF_dict_prime[ii][0][0], ASF_dict_prime[ii][0][1]), (ASF_dict_prime[ii][1][0], ASF_dict_prime[ii][1][1]), 
                                                 (ASF_dict_prime[ii][2][0], ASF_dict_prime[ii][2][1]), (ASF_dict_prime[ii][3][0], ASF_dict_prime[ii][3][1])])
                    
                    
                            p5, p6, p7, p8 = map(Point, [(ASF_dict_prime[ii-1][0][0], ASF_dict_prime[ii-1][0][1]), (ASF_dict_prime[ii-1][1][0], ASF_dict_prime[ii-1][1][1]),
                                                 (ASF_dict_prime[ii-1][2][0], ASF_dict_prime[ii-1][2][1]), (ASF_dict_prime[ii-1][3][0], ASF_dict_prime[ii-1][3][1])])
                    
                            poly1 = Polygon(p1, p2, p3, p4)
                            poly2 = Polygon(p5, p6, p7, p8)
                    
                            a =  poly1.intersection(poly2)
                            SP1 = a[0]
                            SP2 = a[1]
                            
                            
                            resultShadow = abs(Polygon((SP2[0],SP2[1]), (ASF_dict_prime[ii-1][2][0], ASF_dict_prime[ii-1][2][1]), (SP1[0],SP1[1]),
                                        (ASF_dict_prime[ii][0][0], ASF_dict_prime[ii][0][1])).area)
                            
                            resultASF = abs(poly1.area)
                            
                            totalArea = resultASF - resultShadow
                    
                            Shadow[ii-1]= float(resultShadow)
                            ASFArea[ii-1] = resultASF
                            
                            SumArea += resultASF            
                            print "ASF: ", ii-1 , "- Area: ", round(totalArea,3)
                            print "Intersection with panel to the right: Yes"    
                            
                        else:
#                            resultTest = Area3D(poly = ASF_dict_prime[ii])
#                            print 'Test', resultTest         
                            
                            
                            result = Area(Dict = ASF_dict_prime[ii])

                            print "ASF: ", ii , "- Area: ", round(result,3)
                            print "Intersection with panel to the right: No"
                            
                            SumArea += result 
                        
                            Shadow[ii-1]= 0 
                            ASFArea[ii-1] = result
                            
                            
               
                    print '\nCase 2b'
                    
                    for ii in range(1,row2): #2
                        #case: check if the lowest edge of  a panel is intersection with panel below
                        for colNum in range(col): #4
                        
                                            
                            if (colNum-1) + ii *col < PanelNum: #skip the last panels 
                                
#                                print colNum + (ii-1) *col
#                                print (colNum-1) + ii *col
                            
                                p = Polygon((ASF_dict_prime[(colNum-1) + ii *col][0][0],ASF_dict_prime[(colNum-1) + ii *col][0][1]),
                                            (ASF_dict_prime[(colNum-1) + ii *col][1][0],ASF_dict_prime[(colNum-1) + ii *col][1][1]),
                                            (ASF_dict_prime[(colNum-1) + ii *col][2][0],ASF_dict_prime[(colNum-1) + ii *col][2][1]),
                                            (ASF_dict_prime[(colNum-1) + ii *col][3][0],ASF_dict_prime[(colNum-1) + ii *col][3][1]))
                
                            
                                if p.encloses_point(Point(ASF_dict_prime[(colNum + (ii-1) *col)][3][0], ASF_dict_prime[(colNum + (ii-1) *col)][3][1])):
                                    #if Point is in polygon p, than true will be returned
                                
        #                            print 'Num Check Panel', str(colNum + ii *col)
        #                            print 'Num2 Panel above', str(colNum + (ii-1) *col)
        
                                    #Calculate Intersection               
                                    p1, p2, p3, p4 = map(Point, [(ASF_dict_prime[(colNum-1) + ii *col][0][0], ASF_dict_prime[(colNum-1) + ii *col][0][1]), (ASF_dict_prime[(colNum-1) + ii *col][1][0], ASF_dict_prime[(colNum-1) + ii *col][1][1]), 
                                                         (ASF_dict_prime[(colNum-1) + ii *col][2][0], ASF_dict_prime[(colNum-1) + ii *col][2][1]), (ASF_dict_prime[(colNum-1) + ii *col][3][0], ASF_dict_prime[(colNum-1) + ii *col][3][1])])
                            
                            
                                    p5, p6, p7, p8 = map(Point, [(ASF_dict_prime[(colNum + (ii-1) *col)][0][0], ASF_dict_prime[(colNum + (ii-1) *col)][0][1]), (ASF_dict_prime[(colNum + (ii-1) *col)][1][0], ASF_dict_prime[(colNum + (ii-1) *col)][1][1]),
                                                         (ASF_dict_prime[(colNum + (ii-1) *col)][2][0], ASF_dict_prime[(colNum + (ii-1) *col)][2][1]), (ASF_dict_prime[(colNum + (ii-1) *col)][3][0], ASF_dict_prime[(colNum + (ii-1) *col)][3][1])])
                            
                                    poly1 = Polygon(p1, p2, p3, p4)
                                    poly2 = Polygon(p5, p6, p7, p8)
                            
                                    a =  poly1.intersection(poly2)
                                    SP1 = a[0]
                                    SP2 = a[1]
                                    
                                           
                                    
                                    resultShadow2 = abs(10**(-6)* Polygon((SP2[0],SP2[1]), (ASF_dict_prime[(colNum-1) + ii *col][1][0], ASF_dict_prime[(colNum-1) + ii *col][1][1]), (SP1[0],SP1[1]),
                                                             (ASF_dict_prime[(colNum + (ii-1) *col)][3][0], ASF_dict_prime[(colNum + (ii-1) *col)][3][1])).area)
                            
                                            
                                    Shadow[(colNum-1) + ii *col] += float(resultShadow2)
                            
                                        
                                    print "ASF: ", (colNum-1) + ii *col
                                    print "Intersection with upper panel: Yes"    
                                    
            
                                    
                                else:
                                    result1 = Area(Dict = ASF_dict_prime[(colNum-1) + ii *col])
                                    print "ASF: ", (colNum-1) + ii *col
                                    print "Intersection with upper panel: No"
                                    Shadow[(colNum-1) + ii *col]+= 0
                            else:
                                pass
                            
              
    
                print '\nSummary of Solar Radiation Analysis'                
                
                sumArea2 = 0
                for ii in range(PanelNum):       
                       print "ASF: ", ii, "- Area: ", round(ASFArea[ii]-Shadow[ii],3)
                       sumArea2 += ASFArea[ii]-Shadow[ii]
                       
                       
                 

                #save area and total radiation for each hour and angle combination
                TotalArea[HOY][str(x_angle) + str(y_angle)] = round(sumArea2/10**6,3)  #m2
                RadASF_dict[int(HOY)][str(x_angle) + str(y_angle)] = round(sumArea2/10**6,3) * RadTilt_dict[int(HOY)] * 0.001 # area in m2 * Wh/m2 in KWh
               
               
                toc = time.time() - tic
                print 'time passed (sec): ' + str(round(toc,2))
            
    else:
        print 'HOY', HOY
        print 'No Radiation'
        # case with no radiation
        for x_angle in XANGLES:
            for y_angle in YANGLES:
                        
                TotalArea[HOY][str(x_angle) + str(y_angle)] = np.nan
                RadASF_dict[int(HOY)][str(x_angle) + str(y_angle)] = 0
               
    
ResultASF_df = pd.DataFrame(RadASF_dict).T
ResultWindow_df = pd.DataFrame(WindowRadiation).T

ResultAnalysis = pd.concat([radiation['glohorrad_Whm2'], SolarData_df['00'], ResultASF_df['00'],  SolarData_df['0-45'], ResultASF_df['0-45'],  SolarData_df['045'], ResultASF_df['045']], axis=1)

"""

#ResultASF_df.plot() 
#SolarData_df[30:50].plot()

"""

#ResultASF_df['00'].plot()
#ResultASF_df['045'].plot()

#ResultAnalysis[4200:5000]['0-45'].plot()
#pathSave = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RadiationModel'
#ResultAnalysis[4200:5000].to_csv(os.path.join(pathSave, 'ResultPro.csv'))

#SolarData_df[9:35].plot()

#Radiation Analysis

#Tilt_df = pd.DataFrame(RadTilt_dict.items(), columns=['Index','RadiationTilt'])
#
#df=pd.DataFrame(RadTilt_dict.items())
#df.set_index(0, inplace=True)
#
#
#RadCom = pd.concat([LB, df], axis=1)
#RadCom.columns = ['LB', 'RadTilt']
#RadCom[0:8760].plot(kind='line', title = 'Radiation Analysis', grid = True) 