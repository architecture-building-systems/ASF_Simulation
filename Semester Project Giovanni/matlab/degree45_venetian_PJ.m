%45 degree blinds 
%Prageeth Jayathissa
%12.01.2015

clear
clc

load('Workspace_222.mat')

A=Matrix_222_00;


Heating=sum(A(:,2))
Cooling=sum(A(:,3))
Lighting=sum(A(:,4))

Heating_kwh=Heating/(3600000)

Cooling_kwh=Cooling/(3600000)
Lighting_kwh=Lighting/(3600000)