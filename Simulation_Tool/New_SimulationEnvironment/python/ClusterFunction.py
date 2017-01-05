#13.10.2015
#Prageeth Jayathissa
#Python script to produce all possible angle combinations of the facade

#Status: Complete but difficult to read

#Warning: If NoCluster>2 then the program becomes slow
#Functioning ASFanlges calculaion

#------------------------------------------------
      




def NoClusters(XANGLES,YANGLES,NoClusters, paths):


    from prepareData import readLayoutAndCombinations

        
    # panelsize used for simulation:
    #    NoClusters = 5 #readLayoutAndCombinations(paths['radiation_results'])['NoClusters']  
        
    # desired grid point size used for simulation:
    ASFarray = readLayoutAndCombinations(paths)['ASFarray']
    
    #    XANGLES=[90]
    #    YANGLES= [0,45]
    #    
    combination = len(XANGLES) * len(YANGLES)
    
    
    #Import Modules------------------------------------------------
    
    import json
    import math
    import copy
    ####---CHAPTER1-------------------------
    
    #unpack json file and coppy ASF array to create an empty anglearray
    
    ASFangles=copy.deepcopy(ASFarray)
    
      
    #Array to hold final list
    #ListASFangles=[]
    
    #Number of groups that the facade can exist in (now input to function)
    NoClusters=int(NoClusters)
    #NoClusters=1
    #Number of angle combinations
    NoAngles=len(XANGLES)*len(YANGLES)
    
    maxcomb=NoAngles**NoClusters
    
    #Define the angle value that a row is in
    #the value is between 0 and NoAngles
    #rowVal=[0]*NoClusters
    
    
    output = {}
    
    
    #Make a list of all angle combinations
    ANGLES= [[x, y] for x in XANGLES for y in YANGLES]
    
    ANGLEScomb = {}
    count = 0
    
    for ii in range(combination):
        ANGLEScomb[count] = ANGLES[ii]
        count += 1
        
    #for one cluster
    if NoClusters == 1:
        count1 = 0
        total = {}
        for qq in range(0,len(ANGLEScomb)):
            total[count1] =[ANGLEScomb[qq]]
            count1 += 1
     
    
    #for two clusters
    elif NoClusters == 2:
        count1 = 0
        total = {}
        for qq in range(0,len(ANGLEScomb)):
            for ww in range(0,len(ANGLEScomb)):
                total[count1] =[ANGLEScomb[qq],ANGLEScomb[ww]]
                count1 += 1
     
    #for three Clusters
    elif NoClusters == 3:
                 
        count1 = 0
        total = {}
        for qq in range(len(ANGLEScomb)):
            for ww in range(len(ANGLEScomb)):
                for ee in range(len(ANGLEScomb)):
                    total[count1] =[ANGLEScomb[qq],ANGLEScomb[ww],ANGLEScomb[ee]]
                    count1 += 1
                     
    elif NoClusters == 4:
                 
        count1 = 0
        total = {}
        for qq in range(len(ANGLEScomb)):
            for ww in range(len(ANGLEScomb)):
                for ee in range(len(ANGLEScomb)):
                    for rr in range(len(ANGLEScomb)):
                        total[count1] =[ANGLEScomb[qq],ANGLEScomb[ww],ANGLEScomb[ee], ANGLEScomb[rr]]
                        count1 += 1
    
    elif NoClusters == 5:
              
        count1 = 0
        total = {}
        for qq in range(len(ANGLEScomb)):
            for ww in range(len(ANGLEScomb)):
                for ee in range(len(ANGLEScomb)):
                    for rr in range(len(ANGLEScomb)):
                        for tt in range(len(ANGLEScomb)):                    
                            total[count1] =[ANGLEScomb[qq],ANGLEScomb[ww],ANGLEScomb[ee], ANGLEScomb[rr], ANGLEScomb[tt]]
                            count1 += 1
        
     ####---CHAPTER2-------------------------
    
    #Deside which rows to break according to the Number
    #of clusters
    #How many items do we split the ASF into
    rowdivide=int(math.floor(len(ASFangles)/NoClusters))
    #What is remaining
    rowremain=len(ASFangles)%NoClusters
    #print rowdivide
    #print rowremain
    rowsplit=[]
    ii=0
    #These are positions within ASF array where we split
    for ii in range(NoClusters-1):
        rowsplit.append(rowdivide*(ii+1)+1) #a =y, b=2y...
    rowsplit.append(rowdivide*(ii+2)+rowremain) #c=2y+x
    #Add a 0 at the start of the list to indicate the top row is 0
    rowsplit = [0] + rowsplit
    #Bypass funciton if the number of clusters is 1
    if NoClusters==1:
        rowsplit=[]
        rowsplit.append(rowdivide) #Note rowdivide=Number of rows
        rowsplit = [0] + rowsplit
    
      
    
    
      
    for index in range(0,maxcomb):
        
        for yy in range(NoClusters):
            for zz in range(rowsplit[yy],rowsplit[yy+1]):
                for xx in range(len(ASFangles[zz])):
                    ASFangles[zz][xx]= total[index][yy]
                
        output[index] = copy.deepcopy(ASFangles)
    
    
    return output                 



output = NoClusters(XANGLES= [0,30],YANGLES = [45] , NoClusters = 3, paths = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\radiation_results_ZH13_49comb_test')

import json

path_main = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment'

for ii in range(8):
    print output[ii]
    
    with open(path_main + '\\Cluster.json','w') as f:
        f.write(json.dumps(output[5]))

