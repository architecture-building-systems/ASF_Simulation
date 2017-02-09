# -*- coding: utf-8 -*-
"""
Created on Fri Feb 03 09:41:42 2017

@author: Assistenz
"""

from sympy import Point, Polygon
import numpy as np
import math

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
    
    elif I_dif != 0 and theta == np.nan:
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
	x=(math.sin(sunAz+panelAz/2)/(math.sin(math.pi/2-sunAz)))*h*math.sin(-panelAz/2)
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
      
def Distance (P1,P2):
    p1, p2 = Point(P1[0], P1[1]), Point(P2[0], P2[1])
    Dis = p1.distance(p2)
    return abs(Dis)

#Test = Distance([1,1],[2,-1])
#
#print Test

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
    
    
def Area(Dict):
    #calcualte area of polygon
    ListASF = Dict
    p1, p2, p3, p4 = map(Point, [(ListASF[0][0], ListASF[0][1]), (ListASF[1][0], ListASF[1][1]), 
                             (ListASF[2][0], ListASF[2][1]), (ListASF[3][0], ListASF[3][1])])
    poly1 = Polygon(p1, p2, p3, p4)
    
    resultASF = abs(round(float(poly1.area),2)) #mm2
    
    return resultASF
    

def CaseA(ind, SunAngles, ASF_dict_prime, PanelNum, row2, col):
    
    Shadow = {}
    ASFArea = {}
    
    #SunAngles['Azimuth'][ind] >= 180
    print '\nCase 1a'
                                
    print 'Altitude', SunAngles['Altitude'][ind]
    print 'Azimuth', SunAngles['Azimuth'][ind]
    
    result1 = Area(Dict = ASF_dict_prime[0])
    print "\nPanel:  0", "- Area: ", result1
    print "Intersection with panel to the left: No"
    
       
    Shadow[0] = 0
    ASFArea[0] = result1
    
    SumArea = 0
    
    
    ShadowLong = {}
    ShadowLat = {}
    
    ShadowLong[0] = 0
    ShadowLat[0] = 0
     
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
            
            Dis1 = Distance(P1 = ASF_dict_prime[ii][0], P2 =  SP2) # latitudinal shading length
            Dis2 = Distance(P1 = ASF_dict_prime[ii][0] , P2 =  ASF_dict_prime[ii][3]) # latitudinal panel length
            ShadowLat[ii] = float(Dis1 / Dis2) # percentage latitudinal shading
            
            print float(Dis1/Dis2)
            
            Dis3 = Distance(P1 = ASF_dict_prime[ii][0], P2 = SP1 )
            Dis4 = Distance(P1 = ASF_dict_prime[ii][0] , P2 =  ASF_dict_prime[ii][1])
            ShadowLong[ii] = float(Dis3 / Dis4)            
            
            totalArea = resultASF - resultShadow
    
            Shadow[ii]= float(resultShadow)
            ASFArea[ii] = resultASF
            
            SumArea += resultASF            
            print "Panel: ", ii , "- Area: ", round(totalArea,3)
            print "Intersection with panel to the left: Yes"    
            
        else:
            
                                        
            result = Area(Dict = ASF_dict_prime[ii])
            print "Panel: ", ii , "- Area: ", round(result,3)
            print "Intersection with panel to the left: No"
            
            SumArea += result 
        
            Shadow[ii]= 0 
            ASFArea[ii] = result
            ShadowLat[ii] = 0
            ShadowLong[ii] = 0
    
    print '\nCase 2a1'
    for ii in range(1,row2): 
        #case: check if the lowest edge of  a panel is intersection with panel below
        for colNum in range(col): 
        
                            
            if (colNum + ii *col) < PanelNum: #skip the last panels 
            
                p = Polygon((ASF_dict_prime[colNum + ii *col][0][0],ASF_dict_prime[colNum + ii *col][0][1]),
                            (ASF_dict_prime[colNum + ii *col][1][0],ASF_dict_prime[colNum + ii *col][1][1]),
                            (ASF_dict_prime[colNum + ii *col][2][0],ASF_dict_prime[colNum + ii *col][2][1]),
                            (ASF_dict_prime[colNum + ii *col][3][0],ASF_dict_prime[colNum + ii *col][3][1]))
    
            
                if p.encloses_point(Point(ASF_dict_prime[(colNum + (ii-1) *col)][3][0], ASF_dict_prime[(colNum + (ii-1) *col)][3][1])):
                    #if Point is in polygon p, than true will be returned
                
    
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
                    
#                    print 'SP1_0', float(SP1[0])
#                    print 'SP1_1', float(SP1[1])  
#                    
#                    print 'SP2_0', float(SP2[0])
#                    print 'SP2_1', float(SP2[1])     
                    
                    resultShadow2 = abs(Polygon((SP2[0],SP2[1]), (ASF_dict_prime[colNum + ii *col][1][0], ASF_dict_prime[colNum + ii *col][1][1]), (SP1[0],SP1[1]),
                                             (ASF_dict_prime[(colNum + (ii-1) *col)][3][0], ASF_dict_prime[(colNum + (ii-1) *col)][3][1])).area)
            
                            
                    Shadow[colNum + ii *col] += float(resultShadow2)
                    
                    Dis1 = Distance(P1 = ASF_dict_prime[colNum + ii *col][1], P2 =  SP2) # latitudinal shading length
                    Dis2 = Distance(P1 = ASF_dict_prime[colNum + ii *col][1], P2 =  ASF_dict_prime[colNum + ii *col][2]) # latitudinal panel length
                    ShadowLat[colNum + ii *col] += float(Dis1/Dis2) # percentage latitudinal shading
            
                    Dis3 = Distance(P1 = ASF_dict_prime[colNum + ii *col][1], P2 =  SP1)
                    Dis4 = Distance(P1 = ASF_dict_prime[colNum + ii *col][1] ,P2 =  ASF_dict_prime[colNum + ii *col][0])
                    ShadowLong[colNum + ii *col] += float(Dis3/Dis4)      
            
            
                        
                    print "Panel: ", colNum + ii *col
                    print "Intersection with upper panel: Yes" 
                    
                else:
                    result1 = Area(Dict = ASF_dict_prime[colNum + ii *col])
                    print "Panel: ", colNum + ii *col
                    print "Intersection with upper panel: No"
                    Shadow[colNum + ii *col]+= 0
            else:
                pass
                   
                    
    print '\nCase 2a2'              
                      
    for ii in range(2,row2): #row2 = yArray, col = xArray
    
            #case: check if the lowest edge of  a panel is intersection with panel below
        for colNum in range(col): 
        
            if (colNum + ii *col-1) < PanelNum: #skip the last panels 
                
                dot = colNum + ii *col -1
            
                p = Polygon((ASF_dict_prime[dot][0][0],ASF_dict_prime[dot][0][1]),
                            (ASF_dict_prime[dot][1][0],ASF_dict_prime[dot][1][1]),
                            (ASF_dict_prime[dot][2][0],ASF_dict_prime[dot][2][1]),
                            (ASF_dict_prime[dot][3][0],ASF_dict_prime[dot][3][1]))
                
            
                if p.encloses_point(Point(ASF_dict_prime[(colNum + (ii-2) *col)][3][0], ASF_dict_prime[(colNum + (ii-2) *col)][3][1])):
                    #if Point is in polygon p, than true will be returned
                
    
                    #Calculate Intersection               
                    p1, p2, p3, p4 = map(Point, [(ASF_dict_prime[dot][0][0], ASF_dict_prime[dot][0][1]), (ASF_dict_prime[dot][1][0], ASF_dict_prime[dot][1][1]), 
                                         (ASF_dict_prime[dot][2][0], ASF_dict_prime[dot][2][1]), (ASF_dict_prime[dot][3][0], ASF_dict_prime[dot][3][1])])
            
            
                    p5, p6, p7, p8 = map(Point, [(ASF_dict_prime[(colNum + (ii-2) *col)][0][0], ASF_dict_prime[(colNum + (ii-2) *col)][0][1]), (ASF_dict_prime[(colNum + (ii-2) *col)][1][0], ASF_dict_prime[(colNum + (ii-2) *col)][1][1]),
                                         (ASF_dict_prime[(colNum + (ii-2) *col)][2][0], ASF_dict_prime[(colNum + (ii-2) *col)][2][1]), (ASF_dict_prime[(colNum + (ii-2) *col)][3][0], ASF_dict_prime[(colNum + (ii-2) *col)][3][1])])
            
                    poly1 = Polygon(p1, p2, p3, p4)
                    poly2 = Polygon(p5, p6, p7, p8)
            
                    a =  poly1.intersection(poly2)
                    SP1 = a[0]
                    SP2 = a[1]
                    
   
                    
                    resultShadow2 = abs(Polygon((SP2[0],SP2[1]), (ASF_dict_prime[dot][1][0], ASF_dict_prime[dot][1][1]), (SP1[0],SP1[1]),
                                             (ASF_dict_prime[(colNum + (ii-2) *col)][3][0], ASF_dict_prime[(colNum + (ii-2) *col)][3][1])).area)
            
                    
                    Shadow[dot] += float(resultShadow2)
                    
                    Dis1 = Distance(P1 = ASF_dict_prime[dot][1], P2 =  SP2) # latitudinal shading length
                    Dis2 = Distance(P1 =  ASF_dict_prime[dot][1], P2 =  ASF_dict_prime[dot][2]) # latitudinal panel length
                    ShadowLat[dot] += float(Dis1 / Dis2) # percentage latitudinal shading
            
                    Dis3 = Distance(P1 = ASF_dict_prime[dot][1], P2 =  SP1)
                    Dis4 = Distance(P1 = ASF_dict_prime[dot][1] , P2 =  ASF_dict_prime[dot][0])  
                    ShadowLong[dot] += float(Dis3 / Dis4)
                        
                    print "Panel: ", dot
                    print "Intersection with second upper panel: Yes" 
                    
    
                    
                else:
                    result1 = Area(Dict = ASF_dict_prime[dot])
                    print "Panel: ", dot
                    print "Intersection with second upper panel: No"
                    Shadow[dot]+= 0
            else:
                pass
            
    #print '\nSummary of Solar Radiation Analysis'                
                        
    sumArea = 0
    for ii in range(PanelNum):       
           #print "Panel: ", ii, "- Area: ", round(ASFArea[ii]-Shadow[ii],3)
           sumArea += ASFArea[ii]-Shadow[ii]
           
    
    #Calculate Percentage of overlapped area
    BestKey = max(ASFArea, key=ASFArea.get)
    Percentage = round(sumArea/(ASFArea[BestKey] * PanelNum),4)
    

    
    return Percentage, ShadowLat, ShadowLong   
    

def CaseB(ind, SunAngles, ASF_dict_prime, PanelNum, row2, col):

    Shadow = {}
    ASFArea = {}
    
    #SunAngles['Azimuth'][ind] < 180
    print '\nCase 1b'
                            
    print 'Altitude', SunAngles['Altitude'][ind]
    print 'Azimuth', SunAngles['Azimuth'][ind]
    
    result1 = Area(Dict = ASF_dict_prime[49])
    print "Panel:  49", "- Area: ", result1
    print "Intersection with panel to the right: No"
    
    Shadow[49] = 0
    ASFArea[49] = result1
    
    ShadowLong = {}
    ShadowLat = {}
    
    ShadowLong[49] = 0
    ShadowLat[49] = 0
    
                        
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
            
            Dis1 = Distance(P1 = ASF_dict_prime[ii-1][2], P2 = SP2) # latitudinal shading length
            Dis2 = Distance(P1 = ASF_dict_prime[ii-1][2] ,P2 = ASF_dict_prime[ii-1][3]) # latitudinal panel length
            ShadowLat[ii-1] = float(Dis1/ Dis2) # percentage latitudinal shading
            
            Dis3 = Distance(P1 = ASF_dict_prime[ii-1][1], P2 = SP1)
            Dis4 = Distance(P1 = ASF_dict_prime[ii-1][1], P2 =  ASF_dict_prime[ii][2])
            ShadowLong[ii-1] = float(Dis3 / Dis4)      
            
            SumArea += resultASF            
            print "Panel: ", ii-1, "- Area: ", round(totalArea,3)
            print "Intersection with panel to the right: Yes"    
            
        else:            
            
            result = Area(Dict = ASF_dict_prime[ii-1])

            print "Panel: ", ii-1 , "- Area: ", round(result,3)
            print "Intersection with panel to the right: No"
            
            SumArea += result 
        
            Shadow[ii-1]= 0 
            ASFArea[ii-1] = result
            ShadowLat[ii-1] = 0
            ShadowLong[ii-1] = 0
            
   
    print '\nCase 2b1'
    
    for ii in range(1,row2): #2
        #case: check if the lowest edge of  a panel is intersection with panel below
        for colNum in range(col): #4
        
                            
            if (colNum-1) + ii *col < PanelNum: #skip the last panels 
                
            
                p = Polygon((ASF_dict_prime[(colNum-1) + ii *col][0][0],ASF_dict_prime[(colNum-1) + ii *col][0][1]),
                            (ASF_dict_prime[(colNum-1) + ii *col][1][0],ASF_dict_prime[(colNum-1) + ii *col][1][1]),
                            (ASF_dict_prime[(colNum-1) + ii *col][2][0],ASF_dict_prime[(colNum-1) + ii *col][2][1]),
                            (ASF_dict_prime[(colNum-1) + ii *col][3][0],ASF_dict_prime[(colNum-1) + ii *col][3][1]))

            
                if p.encloses_point(Point(ASF_dict_prime[(colNum + (ii-1) *col)][3][0], ASF_dict_prime[(colNum + (ii-1) *col)][3][1])):
                    #if Point is in polygon p, than true will be returned
                

                    #Calculate Intersection               
                    p1, p2, p3, p4 = map(Point,[(ASF_dict_prime[(colNum-1) + ii *col][0][0], ASF_dict_prime[(colNum-1) + ii *col][0][1]), (ASF_dict_prime[(colNum-1) + ii *col][1][0], ASF_dict_prime[(colNum-1) + ii *col][1][1]), 
                                         (ASF_dict_prime[(colNum-1) + ii *col][2][0], ASF_dict_prime[(colNum-1) + ii *col][2][1]), (ASF_dict_prime[(colNum-1) + ii *col][3][0], ASF_dict_prime[(colNum-1) + ii *col][3][1])])
            
            
                    p5, p6, p7, p8 = map(Point,[(ASF_dict_prime[(colNum + (ii-1) *col)][0][0], ASF_dict_prime[(colNum + (ii-1) *col)][0][1]), (ASF_dict_prime[(colNum + (ii-1) *col)][1][0], ASF_dict_prime[(colNum + (ii-1) *col)][1][1]),
                                         (ASF_dict_prime[(colNum + (ii-1) *col)][2][0], ASF_dict_prime[(colNum + (ii-1) *col)][2][1]), (ASF_dict_prime[(colNum + (ii-1) *col)][3][0], ASF_dict_prime[(colNum + (ii-1) *col)][3][1])])
            
                    poly1 = Polygon(p1, p2, p3, p4)
                    poly2 = Polygon(p5, p6, p7, p8)
            
                    a =  poly1.intersection(poly2)
                    SP1 = a[0]
                    SP2 = a[1]
                    
                           
                    
                    resultShadow2 = abs(Polygon((SP2[0],SP2[1]), (ASF_dict_prime[(colNum-1) + ii *col][1][0], ASF_dict_prime[(colNum-1) + ii *col][1][1]), (SP1[0],SP1[1]),
                                             (ASF_dict_prime[(colNum + (ii-1) *col)][3][0], ASF_dict_prime[(colNum + (ii-1) *col)][3][1])).area)
            
                            
                    Shadow[(colNum-1) + ii *col] += float(resultShadow2)
                    
                    Dis1 = Distance(P1 = ASF_dict_prime[(colNum-1) + ii *col][1], P2 =  SP2) # latitudinal shading length
                    Dis2 = Distance(P1 =  ASF_dict_prime[(colNum-1) + ii *col][1], P2 =  ASF_dict_prime[(colNum-1) + ii *col][2]) # latitudinal panel length
                    ShadowLat[(colNum-1) + ii *col] += float(Dis1 / Dis2) # percentage latitudinal shading
            
                    Dis3 = Distance(P1 = ASF_dict_prime[(colNum-1) + ii *col][1], P2 =  SP1)
                    Dis4 = Distance(P1 = ASF_dict_prime[(colNum-1) + ii *col][1] , P2 =  ASF_dict_prime[(colNum-1) + ii *col][0])
                    ShadowLong[(colNum-1) + ii *col] += float(Dis3 / Dis4)   
            
                        
                    print "Panel: ", (colNum-1) + ii *col
                    print "Intersection with upper panel: Yes"    
                    

                    
                else:
                    result1 = Area(Dict = ASF_dict_prime[(colNum-1) + ii *col])
                    print "Panel: ", (colNum-1) + ii *col
                    print "Intersection with upper panel: No"
                    Shadow[(colNum-1) + ii *col]+= 0
            else:
                pass
            
    print '\nCase 2b2'              
                      
    for ii in range(2,row2): #row2 = yArray, col = xArray
    
            #case: check if the lowest edge of  a panel is intersection with panel below
        for colNum in range(col): 
        
            if (colNum + ii *col-1) < PanelNum: #skip the last panels 
                
                dot = colNum + ii *col -1
            
                p = Polygon((ASF_dict_prime[dot][0][0],ASF_dict_prime[dot][0][1]),
                            (ASF_dict_prime[dot][1][0],ASF_dict_prime[dot][1][1]),
                            (ASF_dict_prime[dot][2][0],ASF_dict_prime[dot][2][1]),
                            (ASF_dict_prime[dot][3][0],ASF_dict_prime[dot][3][1]))
                
            
                if p.encloses_point(Point(ASF_dict_prime[(colNum + (ii-2) *col)][3][0], ASF_dict_prime[(colNum + (ii-2) *col)][3][1])):
                    #if Point is in polygon p, than true will be returned
                
    
                    #Calculate Intersection               
                    p1, p2, p3, p4 = map(Point,[(ASF_dict_prime[dot][0][0], ASF_dict_prime[dot][0][1]), (ASF_dict_prime[dot][1][0], ASF_dict_prime[dot][1][1]), 
                                         (ASF_dict_prime[dot][2][0], ASF_dict_prime[dot][2][1]), (ASF_dict_prime[dot][3][0], ASF_dict_prime[dot][3][1])])
            
            
                    p5, p6, p7, p8 = map(Point,[(ASF_dict_prime[(colNum + (ii-2) *col)][0][0], ASF_dict_prime[(colNum + (ii-2) *col)][0][1]), (ASF_dict_prime[(colNum + (ii-2) *col)][1][0], ASF_dict_prime[(colNum + (ii-2) *col)][1][1]),
                                         (ASF_dict_prime[(colNum + (ii-2) *col)][2][0], ASF_dict_prime[(colNum + (ii-2) *col)][2][1]), (ASF_dict_prime[(colNum + (ii-2) *col)][3][0], ASF_dict_prime[(colNum + (ii-2) *col)][3][1])])
            
                    poly1 = Polygon(p1, p2, p3, p4)
                    poly2 = Polygon(p5, p6, p7, p8)
            
                    a =  poly1.intersection(poly2)
                    SP1 = a[0]
                    SP2 = a[1]
                    

                    
                    resultShadow2 = abs(Polygon((SP2[0],SP2[1]), (ASF_dict_prime[dot][1][0], ASF_dict_prime[dot][1][1]), (SP1[0],SP1[1]),
                                             (ASF_dict_prime[(colNum + (ii-2) *col)][3][0], ASF_dict_prime[(colNum + (ii-2) *col)][3][1])).area)
            
                    
                    Shadow[dot] += float(resultShadow2)
                    
                    Dis1 = Distance(P1 = ASF_dict_prime[dot][1], P2 =  SP2) # latitudinal shading length
                    Dis2 = Distance(P1 =  ASF_dict_prime[dot][1], P2 =  ASF_dict_prime[dot][2]) # latitudinal panel length
                    ShadowLat[dot] += float(Dis1 / Dis2) # percentage latitudinal shading
            
                    Dis3 = Distance(P1 = ASF_dict_prime[dot][1], P2 =  SP1)
                    Dis4 = Distance(P1 = ASF_dict_prime[dot][1] , P2 =  ASF_dict_prime[dot][0])  
                    ShadowLong[dot] += float(Dis3/ Dis4) 
            
                        
                    print "Panel: ", dot
                    print "Intersection with second upper panel: Yes" 
                    
    
                    
                else:
                    result1 = Area(Dict = ASF_dict_prime[dot])
                    print "Panel: ", dot
                    print "Intersection with second upper panel: No"
                    Shadow[dot]+= 0
            else:
                pass
    #print '\nSummary of Solar Radiation Analysis'                
                        
    sumArea = 0
    for ii in range(PanelNum):       
           #print "Panel: ", ii, "- Area: ", round(ASFArea[ii]-Shadow[ii],3)
           sumArea += ASFArea[ii]-Shadow[ii]
           
    
    #Calculate Percentage of overlapped area
    BestKey = max(ASFArea, key=ASFArea.get)
    Percentage = round(sumArea/(ASFArea[BestKey] * PanelNum),4)
    
    return Percentage, ShadowLat, ShadowLong                                  