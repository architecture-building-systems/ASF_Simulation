% Author: G.Bianchi
% Email: gibianch@student.ethz.ch
% Semester Project
clear all, clc, close all

% DIVA PERIMETER ZONE:
%Coulum i=1 for: Zone Mean Air Temperature [C](Hourly)
%Coulum i=2 for: Heating, EnergyTransfer [J](Hourly)
%Coulum i=3 for: Cooling, EnergyTransfer [J](Hourly)
%Coulum i=4 for: InteriorLights, Electricity [J](Hourly)
%Coulum i=5 for: InteriorEquipment:Electricity [J](Hourly)  

% Chose the parameter to plot (2-5)
i=4
% Chose the combination e.g: '213'
orizontal_comb = '333';

% in the first iteration: inizialize Minimal_value(1,28), else load
%Minimal_value=zeros(8760,28);
%load(['Users/giovannibianchi/Documents/MATLAB/Comparison_matrix.mat'])

load(['Workspace_' orizontal_comb '.mat'])

orizontal_comb=str2num(orizontal_comb);

eval(sprintf('vm7 = Matrix_%d_m75(:,i)', orizontal_comb));
eval(sprintf('vm6 = Matrix_%d_m60(:,i)', orizontal_comb));
eval(sprintf('vm4 = Matrix_%d_m45(:,i)', orizontal_comb));
eval(sprintf('vm3 = Matrix_%d_m30(:,i)', orizontal_comb));
eval(sprintf('vm1 = Matrix_%d_m15(:,i)', orizontal_comb));
eval(sprintf('v0 = Matrix_%d_00(:,i)', orizontal_comb));
eval(sprintf('v1 = Matrix_%d_15(:,i)', orizontal_comb));
eval(sprintf('v3 = Matrix_%d_30(:,i)', orizontal_comb));
eval(sprintf('v4 = Matrix_%d_45(:,i)', orizontal_comb));
eval(sprintf('v6 = Matrix_%d_60(:,i)', orizontal_comb));
eval(sprintf('v7 = Matrix_%d_75(:,i)', orizontal_comb));
eval(sprintf('v9 = Matrix_%d_90(:,i)', orizontal_comb));

A=[vm7 vm6 vm4 vm3 vm1 v0 v1 v3 v4 v6 v7 v9];
A=v0 %take only the one vertical combination.Comment this out if you want vertical combinations to work

[Y,I] = min(A, [], 2);

Index_with_minimal_value=I;

% Minimal_value(1,28)=Minimal_value(1,28)+1;
% c=Minimal_value(1,28);
% 
% Minimal_value(:,c)=Y;

save('Comparison_matrix','Index_with_minimal_value')

Energy=sum(Y)
hours_pumping=sum(Y>0) %The hours of pumping time required per year
Pumping_cost=hours_pumping*(60/23)/1000 %60W pump divided into 23 regions. Cost in kWh

% display('Position -75? is optimal: (number of times)')
% numel(Index_with_minimal_value(Index_with_minimal_value==1))
% 
% display('Position -60? is optimal: (number of times)')
% numel(Index_with_minimal_value(Index_with_minimal_value==2))
% 
% display('Position -45? is optimal: (number of times)')
% numel(Index_with_minimal_value(Index_with_minimal_value==3))
% 
% display('Position -30? is optimal: (number of times)')
% numel(Index_with_minimal_value(Index_with_minimal_value==4))
% 
% display('Position -15? is optimal: (number of times)')
% numel(Index_with_minimal_value(Index_with_minimal_value==5))
% 
% display('Position 0? is optimal: (number of times)')
% numel(Index_with_minimal_value(Index_with_minimal_value==6))
% 
% display('Position 15? is optimal: (number of times)')
% numel(Index_with_minimal_value(Index_with_minimal_value==7))
% 
% display('Position 30 is optimal: (number of times)')
% numel(Index_with_minimal_value(Index_with_minimal_value==8))
% 
% display('Position 45 is optimal: (number of times)')
% numel(Index_with_minimal_value(Index_with_minimal_value==9))
% 
% display('Position 60 is optimal: (number of times)')
% numel(Index_with_minimal_value(Index_with_minimal_value==10))
% 
% display('Position 75 is optimal: (number of times)')
% numel(Index_with_minimal_value(Index_with_minimal_value==11))
% 
% display('Position 90 is optimal: (number of times)')
% numel(Index_with_minimal_value(Index_with_minimal_value==12))