# -*- coding: utf-8 -*-
"""
Created on Fri Feb 03 09:41:42 2017

@author: Assistenz
"""
from sympy.solvers import solve
from sympy import Point, Polygon, pi, Symbol
from scipy.optimize import fsolve
import numpy as np

def DisPoints (P1,P2):
    distance = np.sqrt( (P1[0]-P2[0])**2 + (P1[1]-P2[1])**2 + (P1[2]-P2[2])**2)
    #print distance    
    return distance

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
            
    print '\nSummary of Solar Radiation Analysis'                
                        
    sumArea = 0
    for ii in range(PanelNum):       
           print "ASF: ", ii, "- Area: ", round(ASFArea[ii]-Shadow[ii],3)
           sumArea += ASFArea[ii]-Shadow[ii]
           
    
    #Calculate Percentage of overlapped area
    BestKey = max(ASFArea, key=ASFArea.get)
    Percentage = round(sumArea/(ASFArea[BestKey] * PanelNum),4)
    
    return Percentage   
    

def CaseB(ind, SunAngles, ASF_dict_prime, PanelNum, row2, col):

    Shadow = {}
    ASFArea = {}
    
    #SunAngles['Azimuth'][ind] < 180
    print '\nCase 1b'
                            
    print 'Altitude', SunAngles['Altitude'][ind]
    print 'Azimuth', SunAngles['Azimuth'][ind]
    
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
                
            
                p = Polygon((ASF_dict_prime[(colNum-1) + ii *col][0][0],ASF_dict_prime[(colNum-1) + ii *col][0][1]),
                            (ASF_dict_prime[(colNum-1) + ii *col][1][0],ASF_dict_prime[(colNum-1) + ii *col][1][1]),
                            (ASF_dict_prime[(colNum-1) + ii *col][2][0],ASF_dict_prime[(colNum-1) + ii *col][2][1]),
                            (ASF_dict_prime[(colNum-1) + ii *col][3][0],ASF_dict_prime[(colNum-1) + ii *col][3][1]))

            
                if p.encloses_point(Point(ASF_dict_prime[(colNum + (ii-1) *col)][3][0], ASF_dict_prime[(colNum + (ii-1) *col)][3][1])):
                    #if Point is in polygon p, than true will be returned
                

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
                        
    sumArea = 0
    for ii in range(PanelNum):       
           print "ASF: ", ii, "- Area: ", round(ASFArea[ii]-Shadow[ii],3)
           sumArea += ASFArea[ii]-Shadow[ii]
           
    
    #Calculate Percentage of overlapped area
    BestKey = max(ASFArea, key=ASFArea.get)
    Percentage = round(sumArea/(ASFArea[BestKey] * PanelNum),4)
    
    return Percentage                                  