
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
    
    
def Theta2directions (sunAlti, sunAzi , beta, panelAzi):

    sunAlti = np.deg2rad(sunAlti)
    beta = np.deg2rad(beta) # panelAlti
    sunAzi = np.deg2rad(sunAzi)
    panelAzi = np.deg2rad(panelAzi)
    
      
    theta2 = np.arccos(np.cos(sunAlti) * np.cos(sunAzi-panelAzi) * np.sin(beta) + np.sin(sunAlti)* np.cos(beta))
   
    theta2 = np.rad2deg(theta2)
   
    return theta2 # deg



def RadTilt (I_dirnor, I_dif, ref, theta, beta, sunAlti):
    #calculate radiation on tilt surface
    theta = np.deg2rad(theta)
    beta = np.deg2rad(beta)
    alpha_s = np.deg2rad(sunAlti)

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

  
def PointPro(S1, S2, S3, A, SunVec): #needed
    
    #creates a Projection of A_prime for A on the plane S
    
    #W = math.sqrt((S2[0]-S1[0])**2 + (S2[1]-S1[1])**2 + (S2[2]-S1[2])**2)
    #H = math.sqrt((S3[0]-S1[0])**2 + (S3[1]-S1[1])**2 + (S3[2]-S1[2])**2)
    
    M = [(S2[0] + S3[0])/2.,(S2[1] + S3[1])/2. ,(S2[2] + S3[2])/2. ]
    
    
    a = np.array([[S1[0],S1[1],S1[2]], [S2[0],S2[1],S2[2]],[M[0],M[1],M[2]]])
    b = np.array([1,1,1])
    coef = np.linalg.solve(a, b)
    
    #N = [coef[0]/np.sqrt(coef[0]**2 + coef[1]**2 + coef[2]**2), coef[1]/np.sqrt(coef[0]**2 + coef[1]**2 + coef[2]**2), coef[2]/np.sqrt(coef[0]**2 + coef[1]**2 + coef[2]**2)]
    
    #find projection of A, Aprime
    k = Symbol('k')
    k = solve(coef[0]*(k*SunVec[0]+ A[0]) + coef[1]*(k*SunVec[1]+ A[1]) + coef[2]*(k*SunVec[2] + A[2]) -1, k)
    k = k[0]
        
    APrime = [round( (k*(SunVec[0])+ A[0]),4), round((k*(SunVec[1])+ A[1]),4), round((k*(SunVec[2])+ A[2]),4)] 
    
    return APrime
    

def DisPoints (P1,P2):
    distance = np.sqrt( (P1[0]-P2[0])**2 + (P1[1]-P2[1])**2 + (P1[2]-P2[2])**2)
    #print distance    
    return distance


def Area(Dict):
    #calcualte area of polygon
    ASF_dict = Dict
    p1, p2, p3, p4 = map(Point, [(ASF_dict[0][0], ASF_dict[0][2]), (ASF_dict[1][0], ASF_dict[1][2]), 
                             (ASF_dict[2][0], ASF_dict[2][2]), (ASF_dict[3][0], ASF_dict[3][2])])
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
SunAngles['Azimuth'] = SunAngles['Azimuth'] - 180

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
gamma = 0       # surface azimuth angle, south facing ASF = 180
ref = 0         # reflectivity




TotalArea = {}
RadTilt_dict = {}
RadASF_dict = {}
WindowArea = {}
WindowProArea = {}
WindowRadiation = {}
Percentage2 = {}
RadiationPercentage_dict = {}

PanelNum = len(PanelPoints)/4
#PanelNum = 7

row = 9
col = 6



showFig = False


XANGLES = [0]
YANGLES = [-45,0,45]

for HOY in range(24):
    
    RadTilt_dict[int(HOY)] = {}
    RadASF_dict[int(HOY)] = {}
    TotalArea[int(HOY)] = {}
    WindowArea[int(HOY)] = {}
    WindowProArea[int(HOY)] = {}
    WindowRadiation[int(HOY)] = {}
    Percentage2[HOY] = {}
    RadiationPercentage_dict[int(HOY)] = {}
    
    if HOY in TotalHOY:
        
        ii = TotalHOY.index(HOY)
        
        SunVec = np.array([SunData['xV'][ii], SunData['yV'][ii], SunData['zV'][ii]])

    
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
               
                
                #Calculate angle of incidence
                #theta = ThetaAngle(alpha_s = SunAngles['Altitude'][ii], gamma_s = SunAngles['Azimuth'][ii], beta = beta - x_angle, gamma = gamma)
                theta2 = Theta2directions (sunAlti = SunAngles['Altitude'][ii], sunAzi = SunAngles['Azimuth'][ii] , beta = (beta - x_angle), panelAzi = y_angle)
                
                print 'theta', theta2
        
                #Calculate Radiation on tilt surface
                Rad_tilt = RadTilt (I_dirnor = radiation['dirnorrad_Whm2'][HOY], I_dif = radiation['difhorrad_Whm2'][HOY], ref = ref, theta = theta2, beta = (beta - x_angle), sunAlti = SunAngles['Altitude'][ii])          
                RadTilt_dict[int(HOY)][str(x_angle) + str(y_angle)] = Rad_tilt
                
                print 'Rad_tilt', Rad_tilt
             
             
                
                xAngle = np.deg2rad(-x_angle)
                yAngle = np.deg2rad(y_angle) 
                
        

                
                #projection plane
                S1 = [10, -10,    10]
                S2 = [10, -10, 50010]
                S3 = ProjPlane(S1 = S1, n = SunVec)
                S3 = [50010, -10, 50010]

        
                
                Window = [[xR + ((1-gpW)/2 * room_width),                yR,    zR + ((1-gpH)/2 * room_height)],
                          [xR + room_width - ((1-gpW)/2 * room_width),   yR,    zR + ((1-gpH)/2 * room_height)],
                          [xR + ((1-gpW)/2 * room_width),                yR,    zR + room_height - ((1-gpH)/2 * room_height)],
                          [xR + room_width- ((1-gpW)/2 * room_width),    yR,    zR + room_height - ((1-gpH)/2 * room_height)]]    
                          
                          
                WindowPrime = []
                ListX, ASFX = [], []
                ListY, ASFY = [], []
                ListZ, ASFZ = [], []
                
                for ii in Window:
                    Prime = PointPro(S1 = S1, S2 = S2, S3= S3, A = ii, SunVec = SunVec)
                    WindowPrime.append(Prime)
                    ListX.append(Prime[0])
                    ListY.append(Prime[1])
                    ListZ.append(Prime[2])
                    
                    
        
                ASF_dict = {}
                ASF_dict_prime = {}
                
                for dot in range(PanelNum):
                    
                    # 1   
                    #0 2   
                    # 3 
                    
                    #change order of dots
                    ASF_dict[dot] = [[PanelPoints['x'][(dot*4) + 0] + (Hyp- np.cos(yAngle)*Hyp)     ,PanelPoints['y'][(dot*4) + 0] - np.sin(yAngle)* Hyp,   PanelPoints['z'][(dot*4) + 0]], 
                                     [PanelPoints['x'][(dot*4) + 1]                                 ,PanelPoints['y'][(dot*4) + 1] - np.sin(xAngle)* Hyp,   PanelPoints['z'][(dot*4) + 1] - (Hyp- np.cos(xAngle)*Hyp)],
                                     [PanelPoints['x'][(dot*4) + 3] - (Hyp- np.cos(yAngle)*Hyp)     ,PanelPoints['y'][(dot*4) + 3] + np.sin(yAngle)* Hyp,   PanelPoints['z'][(dot*4) + 3]],
                                     [PanelPoints['x'][(dot*4) + 2]                                 ,PanelPoints['y'][(dot*4) + 2] + np.sin(xAngle)* Hyp,   PanelPoints['z'][(dot*4) + 2] + (Hyp- np.cos(xAngle)*Hyp)]]
                    
        #            ASF_dict[dot] = [[PanelPoints['x'][(dot*4) + 0]  ,PanelPoints['y'][(dot*4) + 0], PanelPoints['z'][(dot*4) + 0 ]], 
        #                             [PanelPoints['x'][(dot*4) + 1]  ,PanelPoints['y'][(dot*4) + 1], PanelPoints['z'][(dot*4) + 1]],
        #                             [PanelPoints['x'][(dot*4) + 3]  ,PanelPoints['y'][(dot*4) + 3], PanelPoints['z'][(dot*4) + 3]],
        #                             [PanelPoints['x'][(dot*4) + 2]  ,PanelPoints['y'][(dot*4) + 2], PanelPoints['z'][(dot*4) + 2]]] 
            
                count = 0
                for ii in range(PanelNum):    
                    ASFPrime = []
                    
                    for jj in range(4):
                        
                        Prime = PointPro(S1 = S1, S2 = S2, S3= S3, A = ASF_dict[ii][jj], SunVec = SunVec)
                        ASFPrime.append(Prime)
                        
                        ASFX.append(Prime[0])
                        ASFX.append(ASF_dict[ii][jj][0])
                    
                        ASFY.append(Prime[1])
                        ASFY.append(ASF_dict[ii][jj][1])
                    
                        ASFZ.append(Prime[2])
                        ASFZ.append(ASF_dict[ii][jj][2])        
                        count += 1
                        
                    ASF_dict_prime[ii] = ASFPrime  
                    
                    
                
                
                if showFig == True:
                    # figure 2
                    fig = pylab.figure()
                    ax = Axes3D(fig)
                    
                    x_vals = np.array(ASFX) 
                    y_vals = np.array(ASFY) 
                    z_vals = np.array(ASFZ) 
    
                    
                    Num = 8
                    colors1 = cm.rainbow(np.linspace(0, 1, len(x_vals)/Num))
            
                    
                    for ii in range(len(x_vals)/Num):
                        
                        ax.scatter(x_vals[ii* Num + 0: ii* Num + Num], y_vals[ii* Num + 0: ii* Num + Num], z_vals[ii* Num + 0: ii* Num + Num], s=15, color=colors1[ii])
                    
                    
                    ax.set_xlabel('X Label')
                    ax.set_ylabel('Y Label')
                    ax.set_zlabel('Z Label')
                    
                    
                    pyplot.show()
                
                
                
                
                print "\nStart Geometry Analysis"
                
                Shadow = {}
                ASFArea = {}
                
                if SunAngles['Azimuth'][ii] >= 0: 
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
                        p = Polygon((ASF_dict_prime[ii][0][0],ASF_dict_prime[ii][0][2]),
                                    (ASF_dict_prime[ii][1][0],ASF_dict_prime[ii][1][2]),
                                    (ASF_dict_prime[ii][2][0],ASF_dict_prime[ii][2][2]),
                                    (ASF_dict_prime[ii][3][0],ASF_dict_prime[ii][3][2]))
                        
                        if p.encloses_point(Point(ASF_dict_prime[ii-1][2][0], ASF_dict_prime[ii-1][2][2])):
                            #if Point is in polygon p, than true will be returned
                            #test if far right point of asf porjection lies in the panel right to the existing one
                            
                            #Calculate Intersection     
                           
                            p1, p2, p3, p4 = map(Point, [(ASF_dict_prime[ii][0][0], ASF_dict_prime[ii][0][2]), (ASF_dict_prime[ii][1][0], ASF_dict_prime[ii][1][2]), 
                                                 (ASF_dict_prime[ii][2][0], ASF_dict_prime[ii][2][2]), (ASF_dict_prime[ii][3][0], ASF_dict_prime[ii][3][2])])
                    
                    
                            p5, p6, p7, p8 = map(Point, [(ASF_dict_prime[ii-1][0][0], ASF_dict_prime[ii-1][0][2]), (ASF_dict_prime[ii-1][1][0], ASF_dict_prime[ii-1][1][2]),
                                                 (ASF_dict_prime[ii-1][2][0], ASF_dict_prime[ii-1][2][2]), (ASF_dict_prime[ii-1][3][0], ASF_dict_prime[ii-1][3][2])])
                    
                            poly1 = Polygon(p1, p2, p3, p4)
                            poly2 = Polygon(p5, p6, p7, p8)
                    
                            a =  poly1.intersection(poly2)
                            SP1 = a[0]
                            SP2 = a[1]
                            
                            
                            resultShadow = abs(Polygon((SP2[0],SP2[1]), (ASF_dict_prime[ii-1][2][0], ASF_dict_prime[ii-1][2][2]), (SP1[0],SP1[1]),
                                        (ASF_dict_prime[ii][0][0], ASF_dict_prime[ii][0][2])).area)
                            
                            resultASF = abs(poly1.area)
                            
                            totalArea = resultASF - resultShadow
                    
                            Shadow[ii]= float(resultShadow)
                            ASFArea[ii] = resultASF
                            
                            SumArea += resultASF            
                            print "ASF: ", ii , "- Area: ", round(totalArea,3)
                            print "Intersection with panel to the left: Yes"    
                            
                        else:
                            
                            resultTest = Area3D(poly = ASF_dict_prime[ii])
                            print 'Test', resultTest  
                            
                            result = Area(Dict = ASF_dict_prime[ii])
                            print "ASF: ", ii , "- Area: ", round(result,3)
                            print "Intersection with panel to the left: No"
                            
                            SumArea += result 
                        
                            Shadow[ii]= 0 
                            ASFArea[ii] = result
                    
                    print '\nCase 2a'
                    for ii in range(1,row): #2
                        #case: check if the lowest edge of  a panel is intersection with panel below
                        for colNum in range(col): #4
                        
                                            
                            if (colNum + ii *col) < PanelNum: #skip the last panels 
                            
                                p = Polygon((ASF_dict_prime[colNum + ii *col][0][0],ASF_dict_prime[colNum + ii *col][0][2]),
                                            (ASF_dict_prime[colNum + ii *col][1][0],ASF_dict_prime[colNum + ii *col][1][2]),
                                            (ASF_dict_prime[colNum + ii *col][2][0],ASF_dict_prime[colNum + ii *col][2][2]),
                                            (ASF_dict_prime[colNum + ii *col][3][0],ASF_dict_prime[colNum + ii *col][3][2]))
                
                            
                                if p.encloses_point(Point(ASF_dict_prime[(colNum + (ii-1) *col)][3][0], ASF_dict_prime[(colNum + (ii-1) *col)][3][2])):
                                    #if Point is in polygon p, than true will be returned
                                
        #                            print 'Num Check Panel', str(colNum + ii *col)
        #                            print 'Num2 Panel above', str(colNum + (ii-1) *col)
        
                                    #Calculate Intersection               
                                    p1, p2, p3, p4 = map(Point, [(ASF_dict_prime[colNum + ii *col][0][0], ASF_dict_prime[colNum + ii *col][0][2]), (ASF_dict_prime[colNum + ii *col][1][0], ASF_dict_prime[colNum + ii *col][1][2]), 
                                                         (ASF_dict_prime[colNum + ii *col][2][0], ASF_dict_prime[colNum + ii *col][2][2]), (ASF_dict_prime[colNum + ii *col][3][0], ASF_dict_prime[colNum + ii *col][3][2])])
                            
                            
                                    p5, p6, p7, p8 = map(Point, [(ASF_dict_prime[(colNum + (ii-1) *col)][0][0], ASF_dict_prime[(colNum + (ii-1) *col)][0][2]), (ASF_dict_prime[(colNum + (ii-1) *col)][1][0], ASF_dict_prime[(colNum + (ii-1) *col)][1][2]),
                                                         (ASF_dict_prime[(colNum + (ii-1) *col)][2][0], ASF_dict_prime[(colNum + (ii-1) *col)][2][2]), (ASF_dict_prime[(colNum + (ii-1) *col)][3][0], ASF_dict_prime[(colNum + (ii-1) *col)][3][2])])
                            
                                    poly1 = Polygon(p1, p2, p3, p4)
                                    poly2 = Polygon(p5, p6, p7, p8)
                            
                                    a =  poly1.intersection(poly2)
                                    SP1 = a[0]
                                    SP2 = a[1]
                                    
                                           
                                    
                                    resultShadow2 = abs(10**(-6)* Polygon((SP2[0],SP2[1]), (ASF_dict_prime[colNum + ii *col][1][0], ASF_dict_prime[colNum + ii *col][1][2]), (SP1[0],SP1[1]),
                                                             (ASF_dict_prime[(colNum + (ii-1) *col)][3][0], ASF_dict_prime[(colNum + (ii-1) *col)][3][2])).area)
                            
                                            
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
                
                elif SunAngles['Azimuth'][ii] < 0: 
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
                        p = Polygon((ASF_dict_prime[ii-1][0][0],ASF_dict_prime[ii-1][0][2]),
                                    (ASF_dict_prime[ii-1][1][0],ASF_dict_prime[ii-1][1][2]),
                                    (ASF_dict_prime[ii-1][2][0],ASF_dict_prime[ii-1][2][2]),
                                    (ASF_dict_prime[ii-1][3][0],ASF_dict_prime[ii-1][3][2]))
                        
                        if p.encloses_point(Point(ASF_dict_prime[ii][0][0], ASF_dict_prime[ii][0][2])):
                            #if Point is in polygon p, than true will be returned
                            #test if far right point of asf porjection lies in the panel right to the existing one
                            
                            #Calculate Intersection     
                           
                            p1, p2, p3, p4 = map(Point, [(ASF_dict_prime[ii][0][0], ASF_dict_prime[ii][0][2]), (ASF_dict_prime[ii][1][0], ASF_dict_prime[ii][1][2]), 
                                                 (ASF_dict_prime[ii][2][0], ASF_dict_prime[ii][2][2]), (ASF_dict_prime[ii][3][0], ASF_dict_prime[ii][3][2])])
                    
                    
                            p5, p6, p7, p8 = map(Point, [(ASF_dict_prime[ii-1][0][0], ASF_dict_prime[ii-1][0][2]), (ASF_dict_prime[ii-1][1][0], ASF_dict_prime[ii-1][1][2]),
                                                 (ASF_dict_prime[ii-1][2][0], ASF_dict_prime[ii-1][2][2]), (ASF_dict_prime[ii-1][3][0], ASF_dict_prime[ii-1][3][2])])
                    
                            poly1 = Polygon(p1, p2, p3, p4)
                            poly2 = Polygon(p5, p6, p7, p8)
                    
                            a =  poly1.intersection(poly2)
                            SP1 = a[0]
                            SP2 = a[1]
                            
                            
                            resultShadow = abs(Polygon((SP2[0],SP2[1]), (ASF_dict_prime[ii-1][2][0], ASF_dict_prime[ii-1][2][2]), (SP1[0],SP1[1]),
                                        (ASF_dict_prime[ii][0][0], ASF_dict_prime[ii][0][2])).area)
                            
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
                    
                    for ii in range(1,row): #2
                        #case: check if the lowest edge of  a panel is intersection with panel below
                        for colNum in range(col): #4
                        
                                            
                            if (colNum-1) + ii *col < PanelNum: #skip the last panels 
                                
#                                print colNum + (ii-1) *col
#                                print (colNum-1) + ii *col
                            
                                p = Polygon((ASF_dict_prime[(colNum-1) + ii *col][0][0],ASF_dict_prime[(colNum-1) + ii *col][0][2]),
                                            (ASF_dict_prime[(colNum-1) + ii *col][1][0],ASF_dict_prime[(colNum-1) + ii *col][1][2]),
                                            (ASF_dict_prime[(colNum-1) + ii *col][2][0],ASF_dict_prime[(colNum-1) + ii *col][2][2]),
                                            (ASF_dict_prime[(colNum-1) + ii *col][3][0],ASF_dict_prime[(colNum-1) + ii *col][3][2]))
                
                            
                                if p.encloses_point(Point(ASF_dict_prime[(colNum + (ii-1) *col)][3][0], ASF_dict_prime[(colNum + (ii-1) *col)][3][2])):
                                    #if Point is in polygon p, than true will be returned
                                
        #                            print 'Num Check Panel', str(colNum + ii *col)
        #                            print 'Num2 Panel above', str(colNum + (ii-1) *col)
        
                                    #Calculate Intersection               
                                    p1, p2, p3, p4 = map(Point, [(ASF_dict_prime[(colNum-1) + ii *col][0][0], ASF_dict_prime[(colNum-1) + ii *col][0][2]), (ASF_dict_prime[(colNum-1) + ii *col][1][0], ASF_dict_prime[(colNum-1) + ii *col][1][2]), 
                                                         (ASF_dict_prime[(colNum-1) + ii *col][2][0], ASF_dict_prime[(colNum-1) + ii *col][2][2]), (ASF_dict_prime[(colNum-1) + ii *col][3][0], ASF_dict_prime[(colNum-1) + ii *col][3][2])])
                            
                            
                                    p5, p6, p7, p8 = map(Point, [(ASF_dict_prime[(colNum + (ii-1) *col)][0][0], ASF_dict_prime[(colNum + (ii-1) *col)][0][2]), (ASF_dict_prime[(colNum + (ii-1) *col)][1][0], ASF_dict_prime[(colNum + (ii-1) *col)][1][2]),
                                                         (ASF_dict_prime[(colNum + (ii-1) *col)][2][0], ASF_dict_prime[(colNum + (ii-1) *col)][2][2]), (ASF_dict_prime[(colNum + (ii-1) *col)][3][0], ASF_dict_prime[(colNum + (ii-1) *col)][3][2])])
                            
                                    poly1 = Polygon(p1, p2, p3, p4)
                                    poly2 = Polygon(p5, p6, p7, p8)
                            
                                    a =  poly1.intersection(poly2)
                                    SP1 = a[0]
                                    SP2 = a[1]
                                    
                                           
                                    
                                    resultShadow2 = abs(10**(-6)* Polygon((SP2[0],SP2[1]), (ASF_dict_prime[(colNum-1) + ii *col][1][0], ASF_dict_prime[(colNum-1) + ii *col][1][2]), (SP1[0],SP1[1]),
                                                             (ASF_dict_prime[(colNum + (ii-1) *col)][3][0], ASF_dict_prime[(colNum + (ii-1) *col)][3][2])).area)
                            
                                            
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
                       
                       poly = ASF_dict[ii]
                       result2 = Area3D(poly = poly)
                       print "ASF real: ", ii, ' Area:', result2
                 

                #save area and total radiation for each hour and angle combination
                TotalArea[HOY][str(x_angle) + str(y_angle)] = round(sumArea2/10**6,2)  #m2
                RadASF_dict[int(HOY)][str(x_angle) + str(y_angle)] = round(sumArea2/10**6 * RadTilt_dict[int(HOY)][str(x_angle) + str(y_angle)] * 0.001,3) # area in m2 * Wh/m2 in KWh
                
                
                BestKey = max(ASFArea, key=ASFArea.get)
                Percentage2[HOY][str(x_angle) + str(y_angle)] = sumArea2/(ASFArea[BestKey] * PanelNum)
                
                #projection plane
                S1 = [10, -10,    10]
                S2 = [10, -10, 50010]
                S3 = ProjPlane(S1 = S1, n = SunVec)
                
                ASF_prime = {}
                for ii in range(PanelNum):    
                    ASFPrime = []
                    
                    for jj in range(4):
                        
                        Prime = PointPro(S1 = S1, S2 = S2, S3= S3, A = ASF_dict[ii][jj], SunVec = SunVec)
                        ASFPrime.append(Prime)
                        
                    ASF_prime[ii] = ASFPrime  
                
                
                sum3D = 0

                for zz in range(PanelNum):
                    result3D = Area3D(poly = ASF_prime[ii])
                    sum3D += result3D

                RadiationPercentage_dict[int(HOY)][str(x_angle) + str(y_angle)] = round(Percentage2[HOY][str(x_angle) + str(y_angle)] * sum3D/10**6 * RadTilt_dict[int(HOY)][str(x_angle) + str(y_angle)] * 0.001,3)
               
                
                #calculate the height and width of the Window and WindoProjection
                p1, p2, p3 = Point(Window[0][0], Window[0][2]), Point(Window[1][0], Window[1][2]), Point(Window[2][0], Window[2][2])
                Dis1 = p1.distance(p2)
                Dis2 = p1.distance(p3)
                
                AreaWindow = Dis1 * Dis2 * 10**(-6) #m2
                print "Room Area:", AreaWindow
                WindowArea[int(HOY)][str(x_angle) + str(y_angle)] = AreaWindow
                
                
                p4, p5, p6 = Point(WindowPrime[0][0], WindowPrime[0][2]), Point(WindowPrime[1][0], WindowPrime[1][2]), Point(WindowPrime[2][0], WindowPrime[2][2])
                Dis1 = p4.distance(p5)
                Dis2 = p4.distance(p6)
                
                AreaWindowPrime = Dis1 * Dis2 * 10**(-6) #m2
                print "RoomProjection Area:", AreaWindowPrime
                WindowProArea[int(HOY)][str(x_angle) + str(y_angle)] =  AreaWindowPrime
                
                WindowRadiation[int(HOY)][str(x_angle) + str(y_angle)] = round((AreaWindowPrime - sumArea2/10**6) * RadTilt_dict[int(HOY)][str(x_angle) + str(y_angle)] * 0.001,3) # area in m2 * Wh/m2 in KWh
                
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
                WindowArea[int(HOY)][str(x_angle) + str(y_angle)] = np.nan
                WindowProArea[int(HOY)][str(x_angle) + str(y_angle)] =  np.nan
                WindowRadiation[int(HOY)][str(x_angle) + str(y_angle)] = 0
    
ResultASF_df = pd.DataFrame(RadASF_dict).T
ResultWindow_df = pd.DataFrame(WindowRadiation).T

#BestComb = max(RadASF_dict[180], key=lambda comb: RadASF_dict[180][comb])



#ResultASF_df.plot() 
#SolarData_df[30:50].plot()
ResultAnalysis = pd.concat([radiation['glohorrad_Whm2'], SolarData_df['00'], ResultASF_df['00'], SolarData_df['0-45'], ResultASF_df['0-45'], SolarData_df['045'], ResultASF_df['045']], axis=1)



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
RadData_df = pd.concat([radiation, LB, ResultASF_df, SunAngles['Azimuth']], axis=1)
#
#RadCom = pd.concat([LB, df], axis=1)
#RadCom.columns = ['LB', 'RadTilt']
#RadCom[0:8760].plot(kind='line', title = 'Radiation Analysis', grid = True) 

