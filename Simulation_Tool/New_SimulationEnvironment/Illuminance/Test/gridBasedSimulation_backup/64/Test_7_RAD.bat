SET RAYPATH=.;c:\radiance\lib
PATH=c:\radiance\bin\;$PATH
C:
cd C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\Illuminance\Test\gridBasedSimulation\
rtrace -I  -h -dp 64 -ds 0.5 -dt 0.5 -dc 0.25 -dr 0 -st 0.85 -lr 4 -lw 0.05 -ab 2 -ad 1000 -as 128 -ar 300 -aa 0.1  -e error.log Test_RAD.oct < Test_7.pts > Test_7.res
