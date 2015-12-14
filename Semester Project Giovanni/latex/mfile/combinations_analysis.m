% Combination Analysis
% Semester Project
% Author: G.Bianchi
% Email: gibianch@student.ethz.ch
clear all, clc, close all
Minimal_value=zeros(8760,28);
Index_with_minimal_value=zeros(8760,28);

% Chose the parameter to plot (2-5)    
%Coulum i=2 for: Heating, EnergyTransfer [J](Hourly)
%Coulum i=3 for: Cooling, EnergyTransfer [J](Hourly)
%Coulum i=4 for: InteriorLights, Electricity [J](Hourly)
i=4
% Chose the comb to import: e.g. '232'
orizontal_comb = ['332'];  
load(['/Users/giovanni/Documents/MATLAB/Workspace_' orizontal_comb '.mat'])

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
[Y,I] = min(A, [], 2);
Minimal_value=Y;
Index_with_minimal_value=I;
save('Index_with_minimal_value_332','Index_with_minimal_value_332')
