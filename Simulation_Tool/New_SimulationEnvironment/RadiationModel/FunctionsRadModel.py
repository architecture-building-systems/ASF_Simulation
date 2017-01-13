# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 14:43:32 2017

@author: Assistenz
"""

"""
#4 panels
for jj in range(PanelNum):
    
    #determine the location of the panels
    xR1 = [-room_width * 1/4. + xR, room_width * 1/4. + xR , -room_width * 1/4. + xR, room_width * 1/4. + xR]
    yR1 = [DistWindow + yR]* 4 
    zR1 = [room_height/4. + zR ,room_height/4. + zR, -room_height/4. + zR, -room_height/4. + zR]
    
    # 1   
    #0 2   
    # 3 
    #calculate edges for each panel
    ASF_dict[jj] = [[xR1[jj] + room_width/2 - np.sqrt(2)/2*PanelSize + (Hyp- np.cos(yAngle)*Hyp),    yR1[jj] + np.sin(yAngle)* Hyp ,     zR1[jj] + room_height/2], #1
                    [xR1[jj] + room_width/2 ,                                                        yR1[jj] - np.sin(xAngle)*Hyp,       zR1[jj] + room_height/2 + np.sqrt(2)/2*PanelSize - (Hyp- np.cos(xAngle)*Hyp)],#2
                    [xR1[jj] + room_width/2 + np.sqrt(2)/2*PanelSize - (Hyp- np.cos(yAngle)*Hyp),    yR1[jj] - np.sin(yAngle)* Hyp,      zR1[jj] + room_height/2], #3
                    [xR1[jj] + room_width/2 ,                                                        yR1[jj] + np.sin(xAngle)*Hyp,       zR1[jj] + room_height/2 - np.sqrt(2)/2*PanelSize + (Hyp- np.cos(xAngle)*Hyp)]] #4

#8 panels
for jj in range(PanelNum):
    
    #determine the location of the panels
    xR1 = [-room_width * 4/PanelNum + xR, -room_width * 2/PanelNum + xR,  xR, room_width * 2/PanelNum + xR, room_width * 4/PanelNum + xR, 
           -room_width * 4/PanelNum + xR, -room_width * 2/PanelNum + xR,  xR, room_width * 2/PanelNum + xR, room_width * 4/PanelNum + xR]
    yR1 = [DistWindow + yR]* PanelNum 
    zR1 = [room_height/PanelNum + zR ,room_height/PanelNum + zR, room_height/PanelNum + zR ,room_height/PanelNum + zR, room_height/PanelNum + zR,
           -room_height/PanelNum + zR, -room_height/PanelNum + zR, -room_height/PanelNum + zR, -room_height/PanelNum + zR, -room_height/PanelNum + zR]
    
    # 1   
    #0 2   
    # 3 
    #calculate edges for each panel
    ASF_dict[jj] = [[xR1[jj] + room_width/2 - np.sqrt(2)/2*PanelSize + (Hyp- np.cos(yAngle)*Hyp),    yR1[jj] + np.sin(yAngle)* Hyp ,     zR1[jj] + room_height/2], #1
                    [xR1[jj] + room_width/2 ,                            yR1[jj] - np.sin(xAngle)*Hyp,                            zR1[jj] + room_height/2 + np.sqrt(2)/2*PanelSize - (Hyp- np.cos(xAngle)*Hyp)],#2
                    [xR1[jj] + room_width/2 + np.sqrt(2)/2*PanelSize - (Hyp- np.cos(yAngle)*Hyp),    yR1[jj] - np.sin(yAngle)* Hyp ,      zR1[jj] + room_height/2], #3
                    [xR1[jj] + room_width/2 ,                            yR1[jj] + np.sin(xAngle)*Hyp,                            zR1[jj] + room_height/2 - np.sqrt(2)/2*PanelSize + (Hyp- np.cos(xAngle)*Hyp)]] #4

"""

def AreaCalc(poly):
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
    
    return abs(result/2) #* 10**(-6) #m2       
    
    
def Intersect(n, a, vec, vecSt):
    #intersection between plane and vector
    #plane normal vector n, a = result of plane equation
    #vecSt = startpoint, vec = vector

    lamb = Symbol('lamb')
    lamb = solve((vecSt[0] + lamb *vec[0])*n[0] + (vecSt[1] + lamb*vec[1])*n[1] + (vecSt[2] + lamb*vec[2])*n[2] - a, lamb)
    lamb = lamb[0]
    IntPoint = [vecSt[0] + lamb* vec[0], vecSt[1] + lamb* vec[1], vecSt[2] + lamb* vec[2]]
    #print IntPoint
    return IntPoint


 def LineInter(C1,C2,C3,C4):
    #create lines from two points c1 and c2 / c3 and c4
    #find intersection of lines
    R1 = [round(C2[0]- C1[0],2), round(C2[1]- C1[1],2), round(C2[2]- C1[2],2)] # C1 + lambda * R1
    R2 = [round(C4[0]- C3[0],2), round(C4[1]- C3[1],2), round(C4[2]- C3[2],2)] # C3 + lambda * R2
    
    
    def SolveLine(w):
        t = w[0]
        s = w[1]
                       
        F = np.empty((2))
        F[0] = C1[0]+ t* R1[0] - C3[0] + s * R2[0]
        F[1] = C1[1]+ t* R1[1] - C3[1] + s * R2[1]
        
        return F

    zGuess = np.array([1,1])
    w = fsolve(SolveLine, zGuess)
    InterPoint = [round(C1[0] + w[0] * R1[0],2), round(C1[1] + w[0] * R1[1],2), round(C1[2] + w[0] * R1[2],2)]
    
    
    return InterPoint
    
        
 def Area2D(P1, P2, P3):
    from numpy import linalg as LA
    # calculate area of 3 dots, use for window surface, input mm output m2
    vec1 = [P1[0]-P2[0], P1[1]-P2[1], P1[2]-P2[2]]
    vec2 = [P1[0]-P3[0], P1[1]-P3[1], P1[2]-P3[2]]    
    
    n = np.cross(vec1, vec2)
    Len_N = LA.norm(n) * 10**(-6) #m2
    
    return Len_N

def createPlane(P1, P2, P3):
    # P1 + lambda* r1 + mü * r2, parameterform
    R1 = []
    R2 = []
    
    R1 = [P2[0]-P3[0], P2[1]-P3[1], P2[2]-P3[2]]
     
    R2 = [P2[0]-P1[0], P2[1]-P1[1], P2[2]-P1[2]]
    
    
    #coordinates of plane
    n = np.cross(R1,R2)
    
    #value of plane
    a = np.dot(n,P1)
#    print n
#    print a
    return n, a
        