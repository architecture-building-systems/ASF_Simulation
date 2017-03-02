#06.01.2016
#Jeremias Schmidli
#Python script that calculates sorts all angles into x- and y-angle lists 
#and locations of angle combinations

#import function that calculates the angles     
from calculate_angles_function import create_ASF_angles   


# define function to make items unique in a list (represent every angle combination)
def unique(items):
    found = set([])
    keep = []

    for item in items:
        if item not in found:
            found.add(item)
            keep.append(item)

    return keep


def CalcXYAnglesAndLocation(ASFarray, XANGLES, YANGLES, NoClusters):
        
    allAngles = create_ASF_angles(ASFarray, XANGLES, YANGLES, NoClusters)
    
    #make NoClusters an integer:
    NoClusters = int(NoClusters)        
    
    # create list with all angles:
    new_list = []
    
    for i in range(len(allAngles[0])):
        new_list.append([])
        for j in range(NoClusters):
            new_list[i].append(allAngles[j][i])
    
    # calculate x-angles
    x_angles=[]
    for i in range(len(new_list)):
        x_angles.append([])
        for j in range(NoClusters):
            x_angles[i].append(new_list[i][j][0])
        x_angles[i] = tuple(x_angles[i])
    x_angles_full = x_angles
    x_angles = unique(x_angles)
    
    # find x angle location
    x_angle_location=[]
    for i in range(len(x_angles_full)):
        x_angle_location.append(0)
        x_angle_location[i]=x_angles.index(x_angles_full[i])
            
    # calculate y-angles:
    y_angles=[]
    for i in range(len(new_list)):
        y_angles.append([])
        for j in range(NoClusters):
            y_angles[i].append(new_list[i][j][1])
        y_angles[i] = tuple(y_angles[i])
    y_angles_full = y_angles
    y_angles = unique(y_angles)
    
    # find y angle location
    y_angle_location=[]
    for i in range(len(y_angles_full)):
        y_angle_location.append(0)
        y_angle_location[i]=y_angles.index(y_angles_full[i])
        
    return (allAngles, x_angles, x_angles_full, x_angle_location, y_angles, y_angles_full, y_angle_location)
    
#x_angles, x_angles_full, x_angle_location, y_angles, y_angles_full, y_angle_location = CalcXYAnglesAndLocation(ASFarray, XANGLES, YANGLES, NoClusters)
