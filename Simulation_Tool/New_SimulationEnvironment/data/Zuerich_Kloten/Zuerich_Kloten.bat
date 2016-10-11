@echo off 
echo.
 echo HELLO ASSISTENZ! DO NOT CLOSE THIS WINDOW. 
echo.
echo IT WILL BE CLOSED AUTOMATICALLY WHEN THE CALCULATION IS OVER!
echo.
echo AND MAY TAKE FEW MINUTES...
echo.
echo CALCULATING DIFFUSE COMPONENT OF THE SKY...
C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\data\gendaymtx -m 1 -s -O1 C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\data\Zuerich_Kloten\Zuerich_Kloten.wea> C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\data\Zuerich_Kloten\Zuerich_Kloten_dif_1.mtx
echo.
echo CALCULATING DIRECT COMPONENT OF THE SKY...
C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\data\gendaymtx -m 1 -d -O1 C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\data\Zuerich_Kloten\Zuerich_Kloten.wea> C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\data\Zuerich_Kloten\Zuerich_Kloten_dir_1.mtx