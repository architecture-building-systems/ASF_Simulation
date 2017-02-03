
import math
import numpy as np

#http://math.stackexchange.com/questions/164700/how-to-transform-a-set-of-3d-vectors-into-a-2d-plane-from-a-view-point-of-anoth
room_height = 3100.
room_depth = 7000.
room_width = 4900.


S1 = [-4000,4000,0]
S2 = [40000,5000,0]
S3 = [-4000,4000,5000]

S4 = np.array(S2) - (np.array(S1)-np.array(S3))


PanelSize = 400.

Hyp = np.sin(45)*PanelSize
DistWindow = 500.
xAngle = 0
yAngle = 0

xAngle = np.deg2rad(xAngle)
yAngle = np.deg2rad(yAngle)


xR = 0 + 15000
yR = 0
zR = 0
room= [[xR, yR, zR],
        [xR + room_width, yR, zR],
        #[xR + room_width, yR- room_depth, zR],
        #[xR, yR - room_depth, zR],
        [xR, yR, zR + room_height],
        [xR + room_width, yR, zR + room_height],
        #[xR + room_width, yR- room_depth, zR + room_height],
        #[xR, yR - room_depth, zR + room_height],
        ]

ASF = [[xR + room_width/2-np.sqrt(2)/2*PanelSize, yR , zR + room_height/2],
        [xR + room_width/2, yR, zR + room_height/2 + np.sqrt(2)/2*PanelSize],
        [xR + room_width/2 + np.sqrt(2)/2*PanelSize,yR, zR + room_height/2],
        [xR + room_width/2, yR, zR + room_height/2 - np.sqrt(2)/2*PanelSize]]

ASF_dict = {}

for jj in range(4):
    
    xR = [-room_width/4 + 15000, room_width * 1/4. + 15000 , -room_width/4. + 15000, room_width * 1/4. + 15000]
    yR = [DistWindow]* 4
    zR = [room_height/4. ,room_height/4., -room_height/4. , -room_height/4.]
    
    # 2   
    #1 3   
    # 4   
    ASF_dict[jj] = [[xR[jj] + room_width/2 - np.sqrt(2)/2*PanelSize + (Hyp- np.cos(yAngle)*Hyp),    yR[jj] + np.sin(yAngle)* Hyp ,     zR[jj] + room_height/2], #1
                    [xR[jj] + room_width/2 ,                            yR[jj] - np.sin(xAngle)*Hyp,                            zR[jj] + room_height/2 + np.sqrt(2)/2*PanelSize - (Hyp- np.cos(xAngle)*Hyp)],#2
                    [xR[jj] + room_width/2 + np.sqrt(2)/2*PanelSize - (Hyp- np.cos(yAngle)*Hyp),    yR[jj] - np.sin(yAngle)* Hyp ,      zR[jj] + room_height/2], #3
                    [xR[jj] + room_width/2 ,                            yR[jj] + np.sin(xAngle)*Hyp,                            zR[jj] + room_height/2 - np.sqrt(2)/2*PanelSize + (Hyp- np.cos(xAngle)*Hyp)]] #4

SunVec = [0.92, -0.35,-0.2]


def PointPro(S1, S2, S3, A, SunVec):
    
    
    
    #creates a Projection of A_prime for A on the plane S
    W = math.sqrt((S2[0]-S1[0])**2 + (S2[1]-S1[1])**2 + (S2[2]-S1[2])**2)
    H = math.sqrt((S3[0]-S1[0])**2 + (S3[1]-S1[1])**2 + (S3[2]-S1[2])**2)
    
    M = [(S2[0] + S3[0])/2.,(S2[1] + S3[1])/2. ,(S2[2] + S3[2])/2. ]
    
    
    a = np.array([[S1[0],S1[1],S1[2]], [S2[0],S2[1],S2[2]],[M[0],M[1],M[2]]])
    b = np.array([1,1,1])
    coef = np.linalg.solve(a, b)
    #print coef
    #
    #print np.allclose(np.dot(a, coef), b)
    
    N = [coef[0]/np.sqrt(coef[0]**2 + coef[1]**2 + coef[2]**2), coef[1]/np.sqrt(coef[0]**2 + coef[1]**2 + coef[2]**2), coef[2]/np.sqrt(coef[0]**2 + coef[1]**2 + coef[2]**2)]
    #Camera Point    
    #C = [M[0]+ h*N[0], M[1]+ h*N[1] , M[2]+ h*N[2]]
    
    
    
    from sympy.solvers import solve
    from sympy import Symbol
    
    #find projection of A, Aprime
    k = Symbol('k')
    k = solve(coef[0]*(k*SunVec[0]+ A[0]) + coef[1]*(k*SunVec[1]+ A[1]) + coef[2]*(k*SunVec[2] + A[2]) -1, k)
    k = k[0]
        
    APrime = [(k*(SunVec[0])+ A[0]), (k*(SunVec[1])+ A[1]), (k*(SunVec[2])+ A[2])] 
        
    
    
    #find projection of A, Aprime
#    k = Symbol('k')
#    k = solve(coef[0]*(k*(C[0]-A[0])+ A[0]) + coef[1]*(k*(C[1]-A[1])+ A[1]) + coef[2]*(k*(C[2]-A[2])+ A[2]) -1, k)
#    k = k[0]
#    print k
#    
#    APrime = [(k*(C[0]-A[0])+ A[0]), (k*(C[1]-A[1])+ A[1]), (k*(C[2]-A[2])+ A[2])] 
    
    
   
    
    n2 = (W* np.sqrt( int((APrime[0]-S1[0])**2 + (APrime[1]-S1[1])**2 + (APrime[2]-S1[2])**2)))
    
    #cos(u)
    n3 = ((S2[0]-S1[0])*(APrime[0]-S1[0]) + (S2[1]-S1[1])*(APrime[1]-S1[1])+ (S2[2]-S1[2])*(APrime[2]-S1[2]))/n2
    
    u = np.arccos(round(n3,4))
    
    m = np.sqrt(round((APrime[0]-S1[0])**2 + (APrime[1]-S1[1])**2 + (APrime[2]-S1[2])**2, 4)) * n3
    
    n = np.sqrt(round((APrime[0]-S1[0])**2 + (APrime[1]-S1[1])**2 + (APrime[2]-S1[2])**2, 4)) * np.sin(u)
    
    #APrime = ((k*(C[0]-A[0])+ A[0]), (k*(C[1]-A[1])+ A[1]), (k*(C[2]-A[2])+ A[2]))
    
    
    return APrime, C
    

#def CalculateArea(Points):
    


RoomPrime = []
ListX, ASFX = [], []
ListY, ASFY = [], []
ListZ, ASFZ = [], []

for ii in room:
    Prime, C = PointPro(S1 = S1, S2 = S2, S3= S3, A = ii, SunVec = SunVec)
    RoomPrime.append(Prime)
    ListX.append(Prime[0])
    ListY.append(Prime[1])
    ListZ.append(Prime[2])

#for ii in ASF:
#    Prime, C = PointPro(S1 = S1, S2 = S2, S3= S3, A = ii, h = h)
#    ASFPrime.append(Prime)
#    ASFX.append(Prime[0])
#    ASFY.append(Prime[1])
#    ASFZ.append(Prime[2])


ASF_dict_prime = {}

count = 0    
for ii in range(len(ASF_dict)):
    ASFPrime = []
    
    for jj in range(4):
        Prime, C = PointPro(S1 = S1, S2 = S2, S3= S3, A = ASF_dict[ii][jj], SunVec = SunVec)
        ASFPrime.append(Prime)
        
        ASFX.append(Prime[0])
        ASFX.append(ASF_dict[ii][jj][0])

        ASFY.append(Prime[1])
        ASFY.append(ASF_dict[ii][jj][1])

        ASFZ.append(Prime[2])
        ASFZ.append(ASF_dict[ii][jj][2])        
        count += 1
        
    ASF_dict_prime[ii] = ASFPrime

        
        




from matplotlib import pyplot
import pylab
from mpl_toolkits.mplot3d import Axes3D



fig = pylab.figure()
ax = Axes3D(fig)



x_vals = ASFX + ListX +  [SunVec[0]] #[S1[0], S2[0], S3[0], S4[0],
y_vals = ASFY + ListY + [SunVec[1]] #S1[1], S2[1], S3[1], S4[1], 
z_vals = ASFZ + ListZ + [SunVec[2]] #S1[2], S2[2], S3[2], S4[2], 

for nn in range(len(room)):
    x_vals.append(room[nn][0])
    y_vals.append(room[nn][1])
    z_vals.append(room[nn][2])
    
#for nn in range(len(ASF)):
#    x_vals.append(ASF[nn][0])
#    y_vals.append(ASF[nn][1])
#    z_vals.append(ASF[nn][2])    
    

#x_vals = np.append(roomX[0], np.array(ListX, dtype = np.float64), np.array([S1[0], S2[0], S3[0], S4[0], C[0]]))
#y_vals = np.append(roomY[0], np.array(ListY, dtype = np.float64), np.array([S1[1], S2[1], S3[1], S4[1], C[1]]))
#z_vals = np.append(roomZ[0], np.array(ListZ, dtype = np.float64), np.array([S1[2], S2[2], S3[2], S4[2], C[2]]))


ax.scatter(x_vals, y_vals, z_vals, s=3)
#ax.scatter(ListX, ListY, ListZ)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
#ax.view_init(45,60)
ax.view_init(0,90)
pyplot.show()


def AreaCalc(poly):
    #determinant of matrix a
    def det(a):
        return a[0][0]*a[1][1]*a[2][2] + a[0][1]*a[1][2]*a[2][0] + a[0][2]*a[1][0]*a[2][1] - a[0][2]*a[1][1]*a[2][0] - a[0][1]*a[1][0]*a[2][2] - a[0][0]*a[1][2]*a[2][1]
    
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
        return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
    
    #cross product of vectors a and b
    def cross(a, b):
        x = a[1] * b[2] - a[2] * b[1]
        y = a[2] * b[0] - a[0] * b[2]
        z = a[0] * b[1] - a[1] * b[0]
        return (x, y, z)
    
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
    
    return abs(result/2) * 10**(-6) #m2

for tt in range(len(ASF_dict)):
    result1 = AreaCalc(poly = ASF_dict[tt])
    print "ASF", result1    
    result2 = AreaCalc(poly = ASF_dict_prime[tt])
    print "Prime", result2     
   