#13.10.2015
#Prageeth Jayathissa
#Python script to produce all possible angle combinations of the facade

#Status: Complete but difficult to read

#Warning: If NoCluster>2 then the program becomes slow
#Functioning ASFanlges calculaion

#------------------------------------------------
      




def NoClusters_mauro(XANGLES,YANGLES,NoClusters, paths):


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



output = NoClusters_mauro(XANGLES= [0,30],YANGLES = [45] , NoClusters = 3, paths = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\radiation_results_ZH13_49comb_test')

for ii in range(8):
    print output[ii]

"""
for index in range(0,maxcomb):
    ANGLES = total[index]
    print "total", ANGLES
    
    
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
    
    
    
    #print rowsplit
    
    ####---CHAPTER3-------------------------
    
    #Loop through all combinations of the facade
    keepLooping=True
    combcount=0
    while keepLooping:
        #If we have reached the maximum number of combinations then break the main loop
        if rowVal==[NoAngles-1]*NoClusters: #eg: if [48,48,48]==[48,48,48]
            keepLooping=False
        #re-initialise jj  jcount and icount 
        jj=0
        jcount=0
        icount=0
        
        
         
        if combcount==combination:
        
            #Script to make the ASFAngle matrix
            #Loop through the number of divisions in the facade
            rscount=0 
            #print 'hello'
            #loop through ASFangles matrix to substitute values
            for icount,ii in enumerate(ASFangles):
                for jcount,jj in enumerate(ii):
                    
                    #if the row is at the point that it should go to the next rowsplit combiniation
                    #eg, rowsplit =[0,4,9]
                    #+1 is required because icount and rscount start at 0
                    if icount+1==rowsplit[rscount+1]: #eg if 4==4
                        #if it is not the last element because otherwise rscount is out of bounds
                        if rowsplit[-2]!=rowsplit[rscount]:
                            #move to the next rowsplit value
                            rscount+=1
                            
                    #Replace ASFAngle unit with angle
                    #rowVal: is the ANGLE element identifier between 1,49
                    #eg: rowVal=[5,29] the first element is the angle identifier for the top cluster, 
                        #the second element is the angle identifier for the second cluster
                    #rscount: is rowVal element identifier        
                    ASFangles[icount][jcount]=ANGLES[rowVal[rscount]]
            
              
                   
                
    
        ####---CHAPTER4-------------------------
    
        #Find the next itteration or rowVal, the Agnel element identifier
        #Process: very similar to a counter where the base=NoAngles, eg base49
        for jcount,jj in enumerate(rowVal):
            #if the number of the position has it its maximum, set to zero
            #and itterate the next column
            if jj==NoAngles-1:
                rowVal[jcount]=0
            #if the number is not the maximum, then increase once more and break the loop
            else:
                rowVal[jcount]+=1
                break
        combcount+=1
        
        
    a = str(ASFangles)
    output[index]=a            
        
        
    #outputListASFangles=json.dumps(ListASFangles)
    
    
    ##This has been commented out as it is not used in Combination Selector
    #if combination<len(ListASFangles):
    #    outputASFangles=json.dumps(ListASFangles[int(combination)])
    #else:
    #    outputASFangles=json.dumps(ListASFangles[0])
    #    
    #print ListASFangles
    
       
    
    print "asf", ASFangles
    print output[index]
    print "out", output
print 'combinations is', maxcomb
        #return outputASFangles

#if NoClusters == 1:
#    rows = len(ASFangles)
#    columns = len(ASFangles[0])
#     
#    for index in range(combination):
#        for yy in range(rows):
#            for xx in range(columns):
#                ASFangles[yy][xx]= ANGLEScomb[index]
#        output[index]=str(ASFangles)
"""