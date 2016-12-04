@echo off 
echo.
 echo HELLO ZGHIRU! DO NOT CLOSE THIS WINDOW. 
echo.
echo IT WILL BE CLOSED AUTOMATICALLY WHEN THE CALCULATION IS OVER!
echo.
echo AND MAY TAKE FEW MINUTES...
echo.
echo CALCULATING DIFFUSE COMPONENT OF THE SKY...
C:\Users\Zghiru\Documents\GitHub\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\data\gendaymtx -m 1 -s -O1 C:\Users\Zghiru\Documents\GitHub\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\data\Zuerich_Kloten_2013\Zuerich_Kloten_2013.wea> C:\Users\Zghiru\Documents\GitHub\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\data\Zuerich_Kloten_2013\Zuerich_Kloten_2013_dif_1.mtx
echo.
echo CALCULATING DIRECT COMPONENT OF THE SKY...
C:\Users\Zghiru\Documents\GitHub\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\data\gendaymtx -m 1 -d -O1 C:\Users\Zghiru\Documents\GitHub\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\data\Zuerich_Kloten_2013\Zuerich_Kloten_2013.wea> C:\Users\Zghiru\Documents\GitHub\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\data\Zuerich_Kloten_2013\Zuerich_Kloten_2013_dir_1.mtx