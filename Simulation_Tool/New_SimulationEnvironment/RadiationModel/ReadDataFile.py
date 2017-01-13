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
        
def EvaluationAngle(project_folder = None, project_name= None, x_angle = 0, y_angle = 0):
        #read Data from DaySim

        location1 = os.path.join(os.path.join(os.path.join('output', 'ASF1_' + str(x_angle) + '_' + str(y_angle)), 'res'), 'ASF1_' + str(x_angle) + '_' + str(y_angle) + '.ill')
        location2 = os.path.join(os.path.join(os.path.join('output', 'ASF2_' + str(x_angle) + '_' + str(y_angle)), 'res'), 'ASF2_' + str(x_angle) + '_' + str(y_angle) + '.ill')
        location3 = os.path.join(os.path.join(os.path.join('output', 'ASF3_' + str(x_angle) + '_' + str(y_angle)), 'res'), 'ASF3_' + str(x_angle) + '_' + str(y_angle) + '.ill')
        location4 = os.path.join(os.path.join(os.path.join('output', 'ASF4_' + str(x_angle) + '_' + str(y_angle)), 'res'), 'ASF4_' + str(x_angle) + '_' + str(y_angle) + '.ill')
        
        path1 = os.path.join(os.path.join(project_folder, project_name), location1)
        path2 = os.path.join(os.path.join(project_folder, project_name), location2)
        path3 = os.path.join(os.path.join(project_folder, project_name), location3)
        path4 = os.path.join(os.path.join(project_folder, project_name), location4)

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
#    paths['radiation_results'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\radiation_results_ZH13_3comb_year'
#    paths['radiation_wall'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\radiation_wall_ZH13_3comb_year'
    
    paths['radiation_results'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\radiation_results_ZH13_45_0'
    paths['radiation_wall'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\radiation_wall_ZH13_45_0'

#    paths['radiation_results'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\radiation_results_ZH13_90_0'
#    paths['radiation_wall'] = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\radiation_wall_ZH13_90_0'
    
    
    SimulationPeriod = {
        'FromMonth': 1, #
        'ToMonth': 12,#12,
        'FromDay': 1,  
        'ToDay': 28,#28,
        'FromHour': 8,
        'ToHour': 18}
        
#    SimulationPeriod = {     
#        'FromMonth': 1, #7, #1,
#        'ToMonth': 12,#7, #1,
#        'FromDay': 1, #6, #8,
#        'ToDay': 15, #28,
#        'FromHour': 8,#5
#        'ToHour': 18, #20
#        'Temp_start' : 18}#20
    daysPerMonth = np.array([31,28,31,30,31,30,31,31,30,31,30,31])
    
    XANGLES = [45]
    YANGLES = [0] #-45,0,
    
    for x_angle in XANGLES:
        for y_angle in YANGLES:
            
            x_angle = 45
            y_angle = 0
#            
            print str(x_angle)+str(y_angle)
            
            BuilData[str(x_angle)+str(y_angle)] = {}
            SolarData[str(x_angle)+str(y_angle)]= {}
            
    
            for monthi in range(SimulationPeriod['FromMonth'], SimulationPeriod['ToMonth']+1): #month:
                
                BuilRadData[monthi]= {}
                SolarRadData[monthi]= {}
                
                for day in range(SimulationPeriod['FromDay'], daysPerMonth[monthi-1] + 1):      
            
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
    
    #np.save(os.path.join(pathSave,'SolarData.npy'),SolarData)  
    np.save(os.path.join(pathSave,'SolarData2.npy'),SolarData)   
    #np.save(os.path.join(pathSave,'SolarData3.npy'),SolarData)       
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
    
        Box[i]=(BoxData[i])/(BoxData[Num-1])
    
        #Box[i]=(BoxData[i])/(BoxData[((int(i)/3+1)*3)-1])
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

#Function to read LB-files and save them

#SolarData_df, SolarData = LB()


# default rad param, mat= albedo mix
ASF_0_45_AM = Evaluation(path = pathFolder, project = 'ASF_0_45_AM')
ASF_0_Minus45_AM = Evaluation(path = pathFolder, project = 'ASF_0_-45_AM')
ASF_0_0_AM = Evaluation(path = pathFolder, project = 'ASF_0_0_AM' )
ASF_45_0_AM = Evaluation(path = pathFolder, project = 'ASF_45_0_AM') 
ASF_0_0_AM = Evaluation(path = pathFolder, project = 'ASF_0_0_AM')
ASF_90_0_AM = Evaluation(path = pathFolder, project = 'ASF_90_0_AM' ) 

# default rad param, mat= 0 albedo
ASF_0_45_All0 = Evaluation(path = pathFolder, project = 'ASF_0_45_All0' )
ASF_0_Minus45_All0 = Evaluation(path = pathFolder, project = 'ASF_0_-45_All0' ) 
ASF_0_0_All0 = Evaluation(path = pathFolder, project = 'ASF_0_0_All0' ) 
ASF_45_0_All0 = Evaluation(path = pathFolder, project = 'ASF_45_0_All0' ) 
ASF_90_0_All0 = Evaluation(path = pathFolder, project = 'ASF_90_0_All0' ) 


ASF_0_45_AB1 = Evaluation(path = pathFolder, project = 'ASF_0_45_AB1')
ASF_0_45_AB2 = Evaluation(path = pathFolder, project = 'ASF_0_45_AB2')
ASF_0_45_AB4 = Evaluation(path = pathFolder, project = 'ASF_0_45_AB4')
ASF_0_45_AB6 = Evaluation(path = pathFolder, project = 'ASF_0_45_AB6')
ASF_0_45_AB8 = Evaluation(path = pathFolder, project = 'ASF_0_45_AB8')

ASF_0_45_Con066 = Evaluation(path = pathFolder, project = 'ASF_0_45_Con0.66')
ASF_0_45_Con0 = Evaluation(path = pathFolder, project = 'ASF_0_45_Con0')
ASF_0_45_Win0 = Evaluation(path = pathFolder, project = 'ASF_0_45_Win0')
ASF_0_45_ASF0 = Evaluation(path = pathFolder, project = 'ASF_0_45_ASF0')
ASF_0_45_Ro0 = Evaluation(path = pathFolder, project = 'ASF_0_45_Ro0')


ASF_0_45_Con1 = Evaluation(path = pathFolder, project = 'ASF_0_45_Con1')
ASF_0_45_Win1 = Evaluation(path = pathFolder, project = 'ASF_0_45_Win1')
ASF_0_45_ASF1 = Evaluation(path = pathFolder, project = 'ASF_0_45_ASF1')
ASF_0_45_Ro1 = Evaluation(path = pathFolder, project = 'ASF_0_45_Ro1')



# default rad param with ab=8, mat= albedo mix
ASF_0_45_AB8 = Evaluation(path = pathFolder, project = 'ASF_0_45_AB8')
ASF_0_Minus45_AB8 = Evaluation(path = pathFolder, project = 'ASF_0_-45_AB8')
ASF_0_0_AB8 = Evaluation(path = pathFolder, project = 'ASF_0_0_AB8')


Win_0_0 = EvaluationWindow(path = pathFolder, project = 'ASF_0_0_AM' )
Win_0_45 = EvaluationWindow(path = pathFolder, project = 'ASF_0_45_AM' )
Win_0_Minus45 =  EvaluationWindow(path = pathFolder, project = 'ASF_0_-45_AM' )


ASF_0_0_EPW = Evaluation(path = pathFolder, project = 'ASF_0_0_EPW')



ASF_45_0_All1 = Evaluation(path = pathFolder, project = 'ASF_45_0_All1' ) # mat-values = [ASF: 0.6, win: 0.7, con/room: 0.8], ab= 4
ASF_45_0_2All0 = Evaluation(path = pathFolder, project = 'ASF_45_0_2All0' ) #ab = 1
ASF_45_0_2All1 = Evaluation(path = pathFolder, project = 'ASF_45_0_2All1' ) #ab = 1
ASF_45_0_2AM = Evaluation(path = pathFolder, project = 'ASF_45_0_2AM' ) #mat-values = [ASF: 0.2, win: 0.5, con/room: 0.5], ab= 1
ASF_45_0_Mat02 = Evaluation(path = pathFolder, project = 'ASF_45_0_Mat02') # mat-values = [ASF: 0.2, win: 0.7, con/room: 0.8], ab= 4
ASF_45_0_All1ab8 = Evaluation(path = pathFolder, project = 'ASF_45_0_All1ab8')
ASF_45_0_AMab8 = Evaluation(path = pathFolder, project = 'ASF_45_0_AMab8') # mat-values = [ASF: 0.2, win: 0.5, con/room: 0.5], ab= 4


ASF_0_0_All1 = Evaluation(path = pathFolder, project = 'ASF_0_0_All1' ) # mat-values = [ASF: 0.6, win: 0.7, con/room: 0.8], ab= 4
ASF_0_0_2All0 = Evaluation(path = pathFolder, project = 'ASF_0_0_2All0' ) #ab = 1
ASF_0_0_2All1 = Evaluation(path = pathFolder, project = 'ASF_0_0_2All1' ) #ab = 1
ASF_0_0_2AM = Evaluation(path = pathFolder, project = 'ASF_0_0_2AM' ) #mat-values = [ASF: 0.2, win: 0.5, con/room: 0.5], ab= 1
ASF_0_0_MinRad = Evaluation(path = pathFolder, project = 'ASF_0_0_MinRad') # mat-values = [0], Minimum Rad values  
ASF_0_0_1MinRad = Evaluation(path = pathFolder, project = 'ASF_0_0_1MinRad') # mat-values = [0], Minimum Rad values  









#Load LB-Files
SolarData = np.load(os.path.join(pathSave, 'SolarData.npy')).item()
SolarData_df = pd.DataFrame(SolarData)
SolarData2 = np.load(os.path.join(pathSave, 'SolarData2.npy')).item()
SolarData_df2 = pd.DataFrame(SolarData2)
SolarData3 = np.load(os.path.join(pathSave, 'SolarData3.npy')).item()
SolarData_df3 = pd.DataFrame(SolarData3)


SolarData_df = pd.concat([SolarData_df,SolarData_df2, SolarData_df3], axis=1)

#different number of bounces for one combination
result045Bounce = pd.concat([ASF_0_45_AB1, ASF_0_45_AB2, ASF_0_45_AB4, ASF_0_45_AB6, ASF_0_45_AB8], axis=1)
result045Bounce.columns = ['0/45_AB1', '0/45_AB2','0/45_AB4','0/45_AB6','0/45_AB8']
#data = BoxPlot(data =result045Bounce, title = 'Analysis of the Ambient Bounces', index = ('0/45_AB1', '0/45_AB2','0/45_AB4','0/45_AB6','0/45_AB8'))


#different material values for one combination
result045Mat = pd.concat([ASF_0_45_Con0, ASF_0_45_Con066, ASF_0_45_Con1, ASF_0_45_Win0, ASF_0_45_Win1, ASF_0_45_ASF0, ASF_0_45_ASF1, ASF_0_45_Ro0, ASF_0_45_Ro1, ASF_0_45_AM], axis=1)
result045Mat.columns = ['0/45_Con0', '0/45_Con0.66', '0/45_Con1', '0/45_Win0', '0/45_Win1', '0/45_ASF0', '0/45_ASF1', '0/45_Ro0', '0/45_Ro1', '0/45_AM']
#data = BoxPlot(data =result045Mat, title = 'Material Analysis - Combination 0/45', index = ('0/45_Con0', '0/45_Con0.66', '0/45_Con1', '0/45_Win0', '0/45_Win1', '0/45_ASF0', '0/45_ASF1', '0/45_Ro0', '0/45_Ro1', '0/45_AM'))


start = 0
end = 8760

result045_Mat = pd.concat([ASF_0_45_Con0/ASF_0_45_AM, ASF_0_45_Con066/ASF_0_45_AM, ASF_0_45_Con1/ASF_0_45_AM, ASF_0_45_Win0/ASF_0_45_AM, ASF_0_45_Win1/ASF_0_45_AM, ASF_0_45_ASF0/ASF_0_45_AM, ASF_0_45_ASF1/ASF_0_45_AM, ASF_0_45_AM/ASF_0_45_AM], axis=1)
result045_Mat.columns = ['0/45_Con0', '0/45_Con0.66', '0/45_Con1', '0/45_Win0', '0/45_Win1', '0/45_ASF0', '0/45_ASF1','0/45_AM']
result045_Mat[start:end].plot(kind='line') 

result045Bounce_2 = pd.concat([ASF_0_45_AB1/ASF_0_45_AB4, ASF_0_45_AB2/ASF_0_45_AB4, ASF_0_45_AB4/ASF_0_45_AB4, ASF_0_45_AB6/ASF_0_45_AB4, ASF_0_45_AB8/ASF_0_45_AB4], axis=1)
result045Bounce_2.columns = ['0/45_AB1', '0/45_AB2','0/45_AB4','0/45_AB6','0/45_AB8']
result045Bounce_2[start:end].plot(kind='line') 

Result = {}

Result['045'] = pd.concat([ASF_0_45_AM, ASF_0_45_All0, SolarData_df['045']], axis=1)
Result['045'].columns = ['ASF0/45_AM', 'ASF0/45_All0','LB-0/45']
#
Result['00'] = pd.concat([ASF_0_0_AM,  ASF_0_0_All0, SolarData_df['00']], axis=1)
Result['00'].columns = ['ASF0/0_AM','ASF0/0_All0','LB-0/0']

Result['0-45'] = pd.concat([ASF_0_Minus45_AM, ASF_0_Minus45_All0, SolarData_df['0-45']], axis=1)
Result['0-45'].columns = ['ASF0/-45_AM',  'ASF0/-45_All0','LB-0/-45']

Result['450'] = pd.concat([ ASF_45_0_AM, ASF_45_0_All0,  SolarData_df['450']] , axis=1)
Result['450'].columns = ['ASF45/0_AlbedoMix','ASF45/0_All0',  'LB-45/0']

Result['900'] = pd.concat([ ASF_90_0_AM, ASF_90_0_All0,  SolarData_df['900']] , axis=1)
Result['900'].columns = ['90/0_AM','90/0_All0',  'LB-90/0']



sum_045 = Result['045'][start:end].sum()
sum_00 = Result['00'][start:end].sum()
sum_0Minus45 = Result['0-45'][start:end].sum()


result045 = Result['045']
result045_6 = pd.concat([result045['ASF0/45_AM'][start:end]/result045['ASF0/45_All0'][start:end], result045['LB-0/45'][start:end]/result045['ASF0/45_All0'][start:end], result045['ASF0/45_All0'][start:end]/result045['ASF0/45_All0'][start:end]], axis=1)
result045_6.columns = ['Ratio', 'RatioLB', 'ASF0/45_All0']
#result045_6[start:end].plot(kind='line') 

result00 = Result['00']
result00_6 = pd.concat([result00['ASF0/0_AM'][start:end]/result00['ASF0/0_All0'][start:end], result00['LB-0/0'][start:end]/result00['ASF0/0_All0'][start:end], result00['ASF0/0_All0'][start:end]/result00['ASF0/0_All0'][start:end]], axis=1)
result00_6.columns = ['Ratio', 'RatioLB', 'ASF0/0_All0']
#result00_6[start:end].plot(kind='line') 

res = Result['0-45']
result0Minus45_6 = pd.concat([res['ASF0/-45_AM'][start:end]/res['ASF0/-45_All0'][start:end], res['LB-0/-45'][start:end]/res['ASF0/-45_All0'][start:end], res['ASF0/-45_All0'][start:end]/res['ASF0/-45_All0'][start:end]], axis=1)
result0Minus45_6.columns = ['Ratio', 'RatioLB', 'ASF0/-45_All0']
#result0Minus45_6[start:end].plot(kind='line') 

#result00[0:800].plot(kind='line', yticks= range(0,8)) 
#result0Minus45[0:800].plot(kind='line', yticks= range(0,8)) 

#
#resultCom = pd.concat([result045, result00, result0Minus45] , axis=1)
#data2 = BoxPlot(data =resultCom, title = 'Comparison of Different Angle Combinations', index = ('0/45_AM', '0/45_All0','LB-0/45', '0/0_AM','0/0_All0','LB-0/0', '0/-45_AM', '0/-45_All0','LB-0/-45', '45/0_AM','45/0_All0',  'LB-45/0', '90/0_AM','90/0_All0',  'LB-90/0'))
#
#resultCom3 = pd.concat([result450, result900] , axis=1)
#data3 = BoxPlot(data =resultCom3, title = 'Comparison of Different Angle Combinations', index = ('45/0_AM','45/0_All0','LB-45/0', '90/0_AM','90/0_All0',  'LB-90/0'))

#result045_5 = pd.concat([ASF_0_45_AM/ASF_0_45_All0, ASF_0_45_All0], axis=1)
#result045_5.columns = ['Ratio', 'ASF0/45_All0']
#
#result045_5[4000:4200].plot(kind='line', yticks= range(0,8)) 

#result045[4000:4050].plot(kind='line', yticks= range(0,8)) 
#result045[:400].plot(kind='line', yticks= range(0,8)) 

#result00[4000:4050].plot(kind='line', yticks= range(0,8)) 
#result00[:400].plot(kind='line', yticks= range(0,8)) 

#result0Minus45[4000:4400].plot(kind='line', yticks= range(0,8)) 
#result0Minus45[:400].plot(kind='line',yticks= range(0,8)) 
#
#result450[4000:4400].plot(kind='line', yticks= range(0,8)) 
#result450[:400].plot(kind='line',yticks= range(0,8)) 
#
#result900[4000:4400].plot(kind='line', yticks= range(0,8)) 
#result900[:400].plot(kind='line',yticks= range(0,8)) 
#


#ax = s.hist()  # s is an instance of Series
#fig = ax.get_figure()
#fig.savefig('/path/to/figure.pdf')





#Combination x= 45, y = 0

#result045_2 = pd.concat([ASF_0_45, ASF_0_45_AB8, ASF_0_45_All0, SolarData_df['045']], axis=1)
#result045_2.columns = ['ASF0/45_default', 'ASF0/45_AB8','ASF0/45_Mat0','LB-Data0/45']

result450_1 = pd.concat([ASF_45_0_AM, ASF_45_0_AMab8, ASF_45_0_All1ab8, SolarData_df['450']] , axis=1)
result450_1.columns = ['ASF45/0_AM', 'ASF45/0_AM_ab8', 'ASF45/0_All1_ab8', 'LB']

result450_2 = pd.concat([ASF_45_0_2AM, ASF_45_0_2All1, ASF_45_0_2All0, SolarData_df['450']] , axis=1)
result450_2.columns = ['ASF45/0_AM_AB1', 'ASF45/0_All1_AB1', 'ASF45/0_All0_AB1', 'LB']


"""
BoxPlot(data = result450, title = 'Combination 45/0 - AB=4', index = ('ASF45/0_AlbedoMix','ASF45/0_All0',  'LB-45/0'))
BoxPlot(data = result450_1, title = 'Combination 45/0 - AB=8', index = ('ASF45/0_AM', 'ASF45/0_AM_ab8', 'ASF45/0_All1_ab8', 'LB'))
BoxPlot(data = result450_2, title = 'Combination 45/0 - AB=1', index = ('ASF45/0_AM_AB1', 'ASF45/0_All1_AB1', 'ASF45/0_All0_AB1', 'LB'))
"""

"""
#result450_3 = pd.concat([result450, result450_2] , axis=1)
#BoxPlot(data = result450_3, title = 'Combination 45/0', index = ('default', 'All0', 'All1', 'MatASF_02', 'AlbedoMix','NoAB','AlbedoMix_NoAB', 'All1_NoAB', 'All0_NoAB'))

result00_2 = pd.concat([ASF_0_0_All0, ASF_0_0_2All0, ASF_0_0_AM, ASF_0_0_2AM, ASF_0_0_All1, ASF_0_0_2All1, SolarData_df['00']] , axis=1)
result00_2.columns = ['All0', 'NoAB_All0', 'AlbedoMix', 'NoAB_AlbedoMix', 'All1', 'NoAB_All1',  'LB']
#BoxPlot(data = result00_2, title = 'Combination 0/0', index = ('All0', 'NoAB_All0', 'AlbedoMix', 'NoAB_AlbedoMix','default', 'NoAB', 'All1', 'NoAB_All1',  'LB' ))

result00_3 = pd.concat([ASF_0_0_AM, ASF_0_0_All0, SolarData_df['00']] , axis=1)
result00_3.columns = ['AlbedoMix', 'DefaultRad_All0', 'LB' ]
#BoxPlot(data = result00_3, title = 'Combination 0/0', index = (['AlbedoMix', 'DefaultRad_All0', 'LB']))

#result450[4300:4400].plot()
#result450_1[4300:4400].plot()   
#result450_2[4300:4400].plot() 

#result450_3[4200:4400].plot() 


#result00_2[:1000].plot(kind='line') 
#
#result00_3[4200:4800].plot(kind = 'line') 
#result00_3[:400].plot(kind = 'line') 
#result00_3.plot(kind = 'line') 

"""