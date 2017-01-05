"""
Zurich 2013
"""



import os,sys
import pandas as pd
import time
import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib as mpl



 
ScriptPath = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\python'
sys.path.insert(0, ScriptPath)

from calculateHOY import calcHOY

def Evaluation(path = None, project= None):
        #read Data from DaySim
        
        path1 = os.path.join(path, project) + r"\output\ASF1\res\ASF1.csv"
        path2 = os.path.join(path, project) + r"\output\ASF2\res\ASF2.csv"
        path3 = os.path.join(path, project) + r"\output\ASF3\res\ASF3.csv"
        path4 = os.path.join(path, project) + r"\output\ASF4\res\ASF4.csv"
        
        ASF1 = pd.read_csv(path1)
        ASF2 = pd.read_csv(path2)
        ASF3 = pd.read_csv(path3)
        ASF4 = pd.read_csv(path4)
        
        df1 = ASF1 + ASF2 + ASF3 + ASF4
        Default_df = df1 * 8./(50*400/25.*400/25. * 1000) # sum of Daysim values * 8 m^2 / numberPanels * sensorPoints per Panel * in kWh
        
        df = pd.DataFrame([0], columns = [0.0])
        Default_df = df.append(Default_df, ignore_index=True)
        
        return Default_df

def EvaluationWindow(path = None, project= None):
        #read Data from DaySim
        
        path1 = os.path.join(path, project) + r"\output\Window\res\Window.csv"
        Win1 = pd.read_csv(path1)
        
        Win_df = Win1 * (4900./1000. * 0.92 * 3100./1000. * 0.97)/ (4900./1000. * 0.92/0.2 * 3100./1000. * 0.97/0.2 *1000)# Daysim values * WindoArea / sensorPoints * in kWh
        
        df = pd.DataFrame([0], columns = [0.0])
        Win_df = df.append(Win_df, ignore_index=True)
        
        return Win_df


def LB():
    #LadyBug Calculation
    
    BuilRadData = {}
    SolarRadData = {}
    
    BuilData = {}
    SolarData= {}
    
    TotalHOY = []
    

    paths = {}
    paths['radiation_results'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\radiation_results_ZH13_3comb_year'
    paths['radiation_wall'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\radiation_wall_ZH13_3comb_year'
    
#    paths['radiation_results'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\radiation_results_ZH13_45_0'
#    paths['radiation_wall'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\radiation_wall_ZH13_45_0'
    
    SimulationPeriod = {
        'FromMonth': 1, #
        'ToMonth': 12,#12,
        'FromDay': 1,  
        'ToDay': 28,#28,
        'FromHour': 6,
        'ToHour': 20}
        
#    SimulationPeriod = {     
#        'FromMonth': 1, #7, #1,
#        'ToMonth': 12,#7, #1,
#        'FromDay': 1, #6, #8,
#        'ToDay': 15, #28,
#        'FromHour': 8,#5
#        'ToHour': 18, #20
#        'Temp_start' : 18}#20
    
    XANGLES = [0]
    YANGLES = [-45,0,45] #-45,0,
    
    for x_angle in XANGLES:
        for y_angle in YANGLES:
            
#            x_angle = 45
#            y_angle = 0
#            
            print str(x_angle)+str(y_angle)
            
            BuilData[str(x_angle)+str(y_angle)] = {}
            SolarData[str(x_angle)+str(y_angle)]= {}
    
            for monthi in range(SimulationPeriod['FromMonth'], SimulationPeriod['ToMonth']+1): #month:
                
                BuilRadData[monthi]= {}
                SolarRadData[monthi]= {}
                
                for day in range(SimulationPeriod['FromDay'], SimulationPeriod['ToDay'] + 1):      
            
                    BuilRadData[monthi][day] = {}
                    SolarRadData[monthi][day] = {}
                    
                    for hour in range(SimulationPeriod['FromHour'], SimulationPeriod['ToHour'] + 1):
                        
                        HOY = calcHOY(month = monthi, day = day, hour = hour)
                        TotalHOY.append(HOY)
                        
                        BuildingRadiationData = np.array([])
                        SolarRadiationData = np.array([])            

                            
                        
                        with open(os.path.join(paths['radiation_results'], 'RadiationResults' + '_' + str(hour) + '_' + str(day) + '_' + str(monthi) + '_' + str(x_angle) + '_' + str(y_angle) + '.csv'), 'r') as csvfile:
                                    
                            #print 'RadiationResults' +'_' +  str(hour) + '_' + str(day) + '_' + str(monthi)  + '_' + str(x_angle) + '_' + str(y_angle)+ '.csv'                                    
                            reader = csv.reader(csvfile)
                            for idx,line in enumerate(reader):
                                if idx == 1:
                                    SolarRadiationData = np.append(SolarRadiationData, [float(line[0])])
                                    #print "solar", SolarRadiationData
                                    SolarData[str(x_angle)+str(y_angle)][HOY+1] = SolarRadiationData[0]       
                            
                        """                                                                    
                        #read total radition on wall and save it in BuildingRadiationData              
                        with open(os.path.join(paths['radiation_wall'], 'RadiationWall' + '_' + str(hour) + '_' + str(day) + '_' + str(monthi) + '_' + str(x_angle) + '_' + str(y_angle) + '.csv'), 'r') as csvfile:
                            #print 'RadiationWall' + '_' + str(hour) + '_' + str(day) + '_' + str(monthi) + '_' + str(x_angle) + '_' + str(y_angle) + '.csv'
                            reader = csv.reader(csvfile)
                            for idx,line in enumerate(reader):
                                if idx == 1:
                                    BuildingRadiationData = np.append(BuildingRadiationData, [float(line[0])])
                                    #print "Buil", BuildingRadiationData
                                    BuilData[str(x_angle)+str(y_angle)][HOY+1] = BuildingRadiationData[0] 
                                    #break
                        """
                    #Radiation data is calculated for all days per month, so the data is divided through the amount of days per month
                    
#                    BuilRadData[monthi][day][hour] = BuildingRadiationData  #kW/h

                    SolarRadData[monthi][day][hour]= SolarRadiationData  #kW/h
                    
    pathSave = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RadiationModel'
    
    np.save(os.path.join(pathSave,'SolarData.npy'),SolarData)  
    #np.save(os.path.join(pathSave,'SolarData2.npy'),SolarData)   
    SolarData_df = pd.DataFrame(SolarData)
    #SolarData_df = SolarData_df.T
    
 #   BuildingData_df = pd.DataFrame(BuilData)
    
    
    #BuildingData_df = BuildingData_df.T
    

#    SolarData_df.to_csv(os.path.join(pathSave, 'SolarData.csv'))
#    BuildingData_df.to_csv(os.path.join(pathSave, 'BuildingData.csv'))
    
    return SolarData_df, SolarData #, BuilData, BuildingData_df
    

def BoxPlot(data, title, index):
    
    BoxData = data.values.T.tolist()
    BoxData = np.array(BoxData)
    
    Num = len(BoxData)
    
    Box = []
    for jj in range(Num):    
        for ii in range(8760):
            if BoxData[jj][ii] == 0:
                BoxData[jj][ii] = np.nan
            else:
                pass
            
    for i in range(Num):
        
        
        Box.append([])
        #Box[i]=(BoxData[i]-BoxData[2])/(BoxData[2]) #Mean Bias error
    
        #Box[i]=(BoxData[i])/(BoxData[Num-1])
    
        Box[i]=(BoxData[i])/(BoxData[((int(i)/3+1)*3)-1])
        #Box[i]=(BoxData[i])

    
    #remove nan values
    mask = (~np.isnan(Box[0])) 
    
    data2= []
    for ii in range(Num):
        data2.append(Box[ii][mask])
           
      
    fig = plt.figure(figsize=(6, 6))
    
    #plt.style.use('ggplot')
    
    plt.subplot(1,1,1)
    
    
    xindex = range(1,Num+1)
    
    box = plt.boxplot(data2, notch=True, patch_artist=True, whis = [5,95])
    #plt.xticks(xindex,('400', '200', '100', '50', '25', '12.5'),size = 14)
    plt.title(title)
    plt.xticks(xindex,index,size = 12)
    plt.yticks(size=14)
    plt.yticks([0,1,2,3,4],size=14)
    plt.ylabel('normalized radiation [-]', fontsize = 14)
    plt.xlabel('Radiation Calculation Type', fontsize = 14)
    #colors = ['cyan', 'lightblue', 'lightgreen', 'tan', 'pink', 'red']
    colors = ['pink']*Num
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
    #plt.tight_layout()
    plt.subplots_adjust(hspace=0.22, wspace=0.54, right=0.98, left=0.08, bottom=0.11)
    plt.grid()
    plt.show()
    
    Save = False    
    if Save == True:
        pathSave = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RadiationModel'
        fig.savefig(os.path.join(pathSave, 'figure_BoxPlot.pdf'))

    return data2


pathFolder = r'C:\Users\Assistenz\Desktop\Mauro\radiation_visualization'
pathSave = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\RadiationModel'

# default rad param, mat= albedo mix
ASF_0_45 = Evaluation(path = pathFolder, project = 'ASF_0_45')
ASF_0_Minus45 = Evaluation(path = pathFolder, project = 'ASF_0_-45')
ASF_0_0 = Evaluation(path = pathFolder, project = 'ASF_0_0' )
# default rad param, mat= 0 albedo
ASF_0_45_All0 = Evaluation(path = pathFolder, project = 'ASF_0_45_All0' )
ASF_0_Minus45_All0 = Evaluation(path = pathFolder, project = 'ASF_0_-45_All0' ) 
ASF_0_0_All0 = Evaluation(path = pathFolder, project = 'ASF_0_0_All0' ) 

# default rad param with ab=8, mat= albedo mix
ASF_0_45_AB8 = Evaluation(path = pathFolder, project = 'ASF_0_45_AB8')
ASF_0_Minus45_AB8 = Evaluation(path = pathFolder, project = 'ASF_0_-45_AB8')
ASF_0_0_AB8 = Evaluation(path = pathFolder, project = 'ASF_0_0_AB8')





Win_0_0 = EvaluationWindow(path = pathFolder, project = 'ASF_0_0' )
Win_0_45 = EvaluationWindow(path = pathFolder, project = 'ASF_0_45' )
Win_0_Minus45 =  EvaluationWindow(path = pathFolder, project = 'ASF_0_-45' )


ASF_0_0_EPW = Evaluation(path = pathFolder, project = 'ASF_0_0_EPW')


ASF_45_0_All0 = Evaluation(path = pathFolder, project = 'ASF_45_0_All0' ) # mat-values = [ASF: 0.6, win: 0.7, con/room: 0.8], ab= 4
ASF_45_0_All1 = Evaluation(path = pathFolder, project = 'ASF_45_0_All1' ) # mat-values = [ASF: 0.6, win: 0.7, con/room: 0.8], ab= 4
ASF_45_0_2All0 = Evaluation(path = pathFolder, project = 'ASF_45_0_2All0' ) #ab = 1
ASF_45_0_2All1 = Evaluation(path = pathFolder, project = 'ASF_45_0_2All1' ) #ab = 1
ASF_45_0_2AM = Evaluation(path = pathFolder, project = 'ASF_45_0_2AM' ) #mat-values = [ASF: 0.2, win: 0.5, con/room: 0.5], ab= 1


ASF_45_0_Mat02 = Evaluation(path = pathFolder, project = 'ASF_45_0_Mat02') # mat-values = [ASF: 0.2, win: 0.7, con/room: 0.8], ab= 4
ASF_45_0_All1ab8 = Evaluation(path = pathFolder, project = 'ASF_45_0_All1ab8')
ASF_45_0_AM = Evaluation(path = pathFolder, project = 'ASF_45_0_AM') # mat-values = [ASF: 0.2, win: 0.5, con/room: 0.5], ab= 4
ASF_45_0_AMab8 = Evaluation(path = pathFolder, project = 'ASF_45_0_AMab8') # mat-values = [ASF: 0.2, win: 0.5, con/room: 0.5], ab= 4




ASF_0_0_All1 = Evaluation(path = pathFolder, project = 'ASF_0_0_All1' ) # mat-values = [ASF: 0.6, win: 0.7, con/room: 0.8], ab= 4
ASF_0_0_2All0 = Evaluation(path = pathFolder, project = 'ASF_0_0_2All0' ) #ab = 1
ASF_0_0_2All1 = Evaluation(path = pathFolder, project = 'ASF_0_0_2All1' ) #ab = 1
ASF_0_0_2AM = Evaluation(path = pathFolder, project = 'ASF_0_0_2AM' ) #mat-values = [ASF: 0.2, win: 0.5, con/room: 0.5], ab= 1
ASF_0_0_AM = Evaluation(path = pathFolder, project = 'ASF_0_0_AM') # mat-values = [ASF: 0.2, win: 0.5, con/room: 0.5], ab= 4  

ASF_0_0_MinRad = Evaluation(path = pathFolder, project = 'ASF_0_0_MinRad') # mat-values = [0], Minimum Rad values  
ASF_0_0_1MinRad = Evaluation(path = pathFolder, project = 'ASF_0_0_1MinRad') # mat-values = [0], Minimum Rad values  
#SolarData_df, BuildingData_df, SolarData, BuildingData = LB()

"""
#Function to read LB-files and save them
SolarData_df, SolarData = LB()

"""
#Load LB-Files
SolarData = np.load(os.path.join(pathSave, 'SolarData.npy')).item()
SolarData_df = pd.DataFrame(SolarData)
SolarData2 = np.load(os.path.join(pathSave, 'SolarData2.npy')).item()
SolarData_df2 = pd.DataFrame(SolarData2)

SolarData_df = pd.concat([SolarData_df,SolarData_df2], axis=1)


#result045_2 = pd.concat([ASF_0_45, ASF_0_45_AB8, ASF_0_45_All0, SolarData_df['045']], axis=1)
#result045_2.columns = ['ASF0/45_default', 'ASF0/45_AB8','ASF0/45_Mat0','LB-Data0/45']


result045 = pd.concat([ASF_0_45, ASF_0_45_All0, SolarData_df['045']], axis=1)
result045.columns = ['ASF0/45_AM', 'ASF0/45_All0','LB-Data0/45']

result00 = pd.concat([ASF_0_0,  ASF_0_0_All0, SolarData_df['00']], axis=1)
result00.columns = ['ASF0/0_AM','ASF0/0_All0','LB-Data0/0']

result0Minus45 = pd.concat([ASF_0_Minus45, ASF_0_Minus45_All0, SolarData_df['0-45']], axis=1)
result0Minus45.columns = ['ASF0/-45_AM',  'ASF0/-45_All0','LB-Data0/-45']



resultCom = pd.concat([result045, result00, result0Minus45] , axis=1)
data2 = BoxPlot(data =resultCom, title = 'Comparison of Different Angle Combinations', index = ('0/45_AM', '0/45_All0','LB-0/45', '0/0_AM','0/0_All0','LB-0/0', '0/-45_AM', '0/-45_All0','LB-0/-45'))


#result045[4000:4400].plot(kind='line', yticks= range(0,8)) 
#result045[:400].plot(kind='line', yticks= range(0,8)) 
#
#result00[4000:4400].plot(kind='line', yticks= range(0,8)) 
#result00[:400].plot(kind='line', yticks= range(0,8)) 
#
#result0Minus45[4000:4400].plot(kind='line', yticks= range(0,8)) 
#result0Minus45[:400].plot(kind='line',yticks= range(0,8)) 

#ax = s.hist()  # s is an instance of Series
#fig = ax.get_figure()
#fig.savefig('/path/to/figure.pdf')


"""

BoxPlot(data = result045, title = 'Combination 0/45', index = ('ASF0/45_default', 'ASF0/45_Mat0','LB-Data0/45'))
BoxPlot(data = result00, title = 'Combination 0/0', index = ('ASF0/0_default','ASF0/0_Mat0','LB-Data0/0'))
BoxPlot(data = result0Minus45, title = 'Combination 0/-45', index = ('ASF0/-45_default',  'ASF0/-45_Mat0','LB-Data0/-45'))

result045[4200:4600].plot(kind = 'line') 
result00[4200:4600].plot(kind = 'line') 
result0Minus45[4200:4600].plot(kind = 'line') 

result045[:400].plot(kind = 'line') 
result00[:400].plot(kind = 'line') 
result0Minus45[:400].plot(kind = 'line') 
"""


#Combination x= 45, y = 0

result450 = pd.concat([ASF_45_0_All0,  ASF_45_0_All1, ASF_45_0_Mat02,  ASF_45_0_AM, SolarData_df['450']] , axis=1)
result450.columns = ['ASF45/0_All0', 'ASF45/0_All1', 'ASF45/0_Mat02', 'ASF45/0_AlbedoMix', 'LB']

result450_1 = pd.concat([ASF_45_0_AM, ASF_45_0_AMab8, ASF_45_0_All1ab8, SolarData_df['450']] , axis=1)
result450_1.columns = ['ASF45/0_AlbedoMix', 'ASF45/0_AlbedoMix_ab8', 'ASF45/0_All1_ab8', 'LB']

result450_2 = pd.concat([ASF_45_0_2AM, ASF_45_0_2All1, ASF_45_0_2All0, SolarData_df['450']] , axis=1)
result450_2.columns = ['ASF45/0_AlbedoMix_AB1', 'ASF45/0_All1_AB1', 'ASF45/0_All0_AB1', 'LB']


"""
BoxPlot(data = result450, title = 'Combination 45/0 - AB=4', index = ('ASF45/0_All0', 'ASF45/0_All1', 'ASF45/0_Mat02', 'ASF45/0_AlbedoMix', 'LB'))
BoxPlot(data = result450_1, title = 'Combination 45/0 - AB=8', index = ('ASF45/0_AlbedoMix', 'ASF45/0_AlbedoMix_ab8', 'ASF45/0_All1_ab8', 'LB'))
BoxPlot(data = result450_2, title = 'Combination 45/0 - AB=1', index = ('ASF45/0_AlbedoMix_AB1', 'ASF45/0_All1_AB1', 'ASF45/0_All0_AB1', 'LB'))
"""

#result450_3 = pd.concat([result450, result450_2] , axis=1)
#BoxPlot(data = result450_3, title = 'Combination 45/0', index = ('default', 'All0', 'All1', 'MatASF_02', 'AlbedoMix','NoAB','AlbedoMix_NoAB', 'All1_NoAB', 'All0_NoAB'))

result00_2 = pd.concat([ASF_0_0_All0, ASF_0_0_2All0, ASF_0_0_AM, ASF_0_0_2AM, ASF_0_0,  ASF_0_0_All1, ASF_0_0_2All1, SolarData_df['00']] , axis=1)
result00_2.columns = ['All0', 'NoAB_All0', 'AlbedoMix', 'NoAB_AlbedoMix','default', 'All1', 'NoAB_All1',  'LB']
#BoxPlot(data = result00_2, title = 'Combination 0/0', index = ('All0', 'NoAB_All0', 'AlbedoMix', 'NoAB_AlbedoMix','default', 'NoAB', 'All1', 'NoAB_All1',  'LB' ))

result00_3 = pd.concat([ASF_0_0_AM, ASF_0_0_All0, SolarData_df['00']] , axis=1)
result00_3.columns = ['AlbedoMix', 'DefaultRad_All0', 'LB' ]
#BoxPlot(data = result00_3, title = 'Combination 0/0', index = (['AlbedoMix', 'DefaultRad_All0', 'LB']))

#result450[4300:4400].plot()
#result450_1[4300:4400].plot()   
#result450_2[4300:4400].plot() 

#result450_3[4200:4400].plot() 

"""
result00_2[:1000].plot(kind='line') 

result00_3[4200:4800].plot(kind = 'line') 
result00_3[:400].plot(kind = 'line') 
result00_3.plot(kind = 'line') 

"""