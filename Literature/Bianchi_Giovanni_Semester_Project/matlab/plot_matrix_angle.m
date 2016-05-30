% Author: G.Bianchi 
% Email: gibianch@student.ethz.ch

% Semester Project

clc,
close all,
clear all

%% Choose the matrix to plot & the title of the plot:

load('/Users/giovannibianchi/Documents/MATLAB/Results/Index_with_minimal_value_222.mat')

B = Index_with_minimal_value;

g_title='Heating, EnergyTransfer [J](Hourly) ';
%g_title='Cooling, EnergyTransfer [J](Hourly) ';
%g_title='InteriorLights, Electricity [J](Hourly) ';

%% RUN

M=zeros(24,365);
M(:,1)=B(1:24,1);

for j =1:364;
    n=j*24;
    M(:,j+1)=B(n+1:n+24,1);
end

figure
pcolor(M)
title(g_title,'FontSize',20)
ylabel('Hour','FontSize',20);
xlabel('Day (of a year)','FontSize',20);
labels = {'rotation -75°','rotation -60°','rotation -45°','rotation -30°','rotation -15°'...
    'rotation 0','rotation 15°','rotation 30°','rotation 45°','rotation 60°','rotation 75°','rotation 90°'};
colorbar('YTick',1:12,'YTickLabel',labels)

