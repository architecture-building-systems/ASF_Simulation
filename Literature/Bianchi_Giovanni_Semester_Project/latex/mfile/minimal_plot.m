% Minimal plot
% Semester Project
% Author: G.Bianchi 
% Email: gibianch@student.ethz.ch

clc, close all
M=zeros(24,365);

M(:,1)=Index_with_minimal_value(1:24,1);

for j =1:364;
    n=j*24;
    M(:,j+1)=Index_with_minimal_value(n+1:n+24,1);
end

plot_title='Cooling:EnergyTransfer [J](Hourly) ';

figure
pcolor(M)
title(plot_title,'FontSize',20)
ylabel('Hour','FontSize',20);
xlabel('Day (of a year)','FontSize',20);
labels = {'Position -75°','Position -60°','Position -45°','Position -30°', ...
    'Position -15°','Position 0°','Position 15°','Position 30','Position 45°', ...
    'Position 60°','Position 75°','Position 90°'};
colorbar('YTickLabel',labels,'FontSize',20);
