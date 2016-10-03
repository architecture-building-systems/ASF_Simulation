#13.10.2015
#Prageeth Jayathissa
#Python script to produce all possible angle combinations of the facade

#Status: Complete but difficult to read

#Warning: If NoCluster>2 then the program becomes slow

#------------------------------------------------
'''README

This code can be read as three chapters

Chapter1: Produces a list of possible angle combinations for a single panel
    Output: ANGLES - a list of all possible angle combinations

Chapter2: Splits the facade into independant clusters of rows. 
    Output: rowsplit - a list of intergers that indicate the start and end point
        of clusters
    Example: If a facade with 9 rows is split into 2 clusters, rowsplit=[0,4,9]
        this indicates that one cluser starts at 0 and ends at 4
        the second cluster starts at 4 and ends at 9

Chapter3: Itterates through all possible panel combinations and produces an output
    list which contains each outputASFangle combination
    Output: ListASFangles - a list of all possible ASFangles
    
Chapter4: Determines that combination of Angles should be recorded for each itteration
    How it works: In priciple, this is a counter where base= Number of angle combinations
    Example: If number of angles =10 and number of clusters =2 this would be a normal 2digit base10 counter
    rowVal=[0,0]
    rowVal=[0,1]
    ...
    rowVal=[0,9]
    rowVal=[1,0]
    
    if number of angles =49 then
    rowVal=[0,0]
    rowVal=[0,1]
    ...
    rowVal=[0,48]
    rowVal=[1,0]
    rowVal=[1,1] etc
    
    This numer rowVal is then used to call on the ANGLE list produced in Chapter 1
    which is then fed into Chapter 3
        
        '''

def NoClusters_mauro(XANGLES, YANGLES, NoClusters):


    from prepareData import readLayoutAndCombinations
    
    
    paths = {}
    
    
    paths['radiation_results'] = 'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\\radiation_results'
    
    # panelsize used for simulation:
    #NoClusters = 2#readLayoutAndCombinations(paths['radiation_results'])['NoClusters']  
        
    # desired grid point size used for simulation:
    ASFarray = readLayoutAndCombinations(paths['radiation_results'])['ASFarray']
    
    #XANGLES = readLayoutAndCombinations(paths['radiation_results'])['XANGLES']
    #YANGLES = readLayoutAndCombinations(paths['radiation_results'])['YANGLES']
    
    #XANGLES=[67.5]
    #YANGLES= [-22.5,22.5]
    
    combination = len(XANGLES) * len(YANGLES)
    
    
    #Import Modules------------------------------------------------
    
    import json
    import math
    import copy
    ####---CHAPTER1-------------------------
    
    #unpack json file and coppy ASF array to create an empty anglearray
    
    ASFangles=copy.deepcopy(ASFarray)
    
    
    #Possible Angles in simulation
    #XANGLES=[0,30,45,60,90]#[0,45,90]#[0,15,30,45,60,75,90]
    #YANGLES=[0]#[-45,0,45]#[-45,-30,-15,0,15,30,45]
    #exec XANGLES
    #exec YANGLES
    
    #XANGLES = [XANGLES]
    #YANGLES = [YANGLES]
    
    print XANGLES
    print YANGLES
    
    #Array to hold final list
    ListASFangles=[]
    
    #Number of groups that the facade can exist in (now input to function)
    NoClusters=int(NoClusters)
    #NoClusters=1
    #Number of angle combinations
    NoAngles=len(XANGLES)*len(YANGLES)
    
    #Define the angle value that a row is in
    #the value is between 0 and NoAngles
    rowVal=[0]*NoClusters
    
    #Make a list of all angle combinations
    ANGLES= [(x, y) for x in XANGLES for y in YANGLES]
    
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
        
    #outputListASFangles=json.dumps(ListASFangles)
    
    
    ##This has been commented out as it is not used in Combination Selector
    #if combination<len(ListASFangles):
    #    outputASFangles=json.dumps(ListASFangles[int(combination)])
    #else:
    #    outputASFangles=json.dumps(ListASFangles[0])
    #    
    #print ListASFangles
    
    maxcomb=NoAngles**NoClusters
    
    print 'max number of combinations is', maxcomb
    if combination>combcount:
        print 'Warning! Requested Combination is not available'
    
    outputASFangles=json.dumps(ASFangles)
    
    return outputASFangles

