% Author: G.Bianchi
% Email: gibianch@student.ethz.ch
% Semester Project
clear all, clc, close all

for t=1:3
   clc
   t=num2str(t);
    
    % DIVA PERIMETER ZONE:
    %Coulum i=1 for: Zone Mean Air Temperature [C](Hourly)
    %Coulum i=2 for: Heating, EnergyTransfer [J](Hourly)
    %Coulum i=3 for: Cooling, EnergyTransfer [J](Hourly)
    %Coulum i=4 for: InteriorLights, Electricity [J](Hourly)
    %Coulum i=5 for: InteriorEquipment:Electricity [J](Hourly)  

    % Chose the parameter to plot (2-5)
    i=4
    
    % chose the comb to import: e.g. '23'
    orizontal_comb = ['33',t];

    % in the first iteration: inizialize Minimal_value(1,28), else load

    if orizontal_comb == '111' 
        Minimal_value=zeros(8760,28);
        Index_with_minimal_value=zeros(8760,28);
        Minimal_value(1,28)=1
    else
        load(['Comparison_matrix.mat'])
    end
    
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

[Y,I] = min(A, [], 2);

% Minimal_value=Y;
% Index_with_minimal_value=I;
%save('Index_with_minimal_value_333','Index_with_minimal_value_333')

Minimal_value(:,Minimal_value(1,28))=Y;
Index_with_minimal_value(:,Minimal_value(1,28))=I;

Minimal_value(1,28)=Minimal_value(1,28)+1;

save('Comparison_matrix','Minimal_value','Index_with_minimal_value')
end