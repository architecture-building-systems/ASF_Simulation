%one comb analysis total
%Prageeth Jayathissa
%23.01.2015

% DIVA PERIMETER ZONE:
%Coulum i=1 for: Zone Mean Air Temperature [C](Hourly)
%Coulum i=2 for: Heating, EnergyTransfer [J](Hourly)
%Coulum i=3 for: Cooling, EnergyTransfer [J](Hourly)
%Coulum i=4 for: InteriorLights, Electricity [J](Hourly)
%Coulum i=5 for: InteriorEquipment:Electricity [J](Hourly)  

% Chose the parameter to plot (2-5)
i=6

% Chose the combination e.g: '213'
orizontal_comb = '111';

% in the first iteration: inizialize Minimal_value(1,28), else load
%Minimal_value=zeros(8760,28);
%load(['Users/giovannibianchi/Documents/MATLAB/Comparison_matrix.mat'])

load(['Workspace_' orizontal_comb '.mat'])

orizontal_comb=str2num(orizontal_comb);

eval(sprintf('vm7 = Matrix_%d_m75(:,2)', orizontal_comb));
            eval(sprintf('vm6 = Matrix_%d_m60(:,2)', orizontal_comb));
            eval(sprintf('vm4 = Matrix_%d_m45(:,2)', orizontal_comb));
            eval(sprintf('vm3 = Matrix_%d_m30(:,2)', orizontal_comb));
            eval(sprintf('vm1 = Matrix_%d_m15(:,2)', orizontal_comb));
            eval(sprintf('v0 = Matrix_%d_00(:,2)', orizontal_comb));
            eval(sprintf('v1 = Matrix_%d_15(:,2)', orizontal_comb));
            eval(sprintf('v3 = Matrix_%d_30(:,2)', orizontal_comb));
            eval(sprintf('v4 = Matrix_%d_45(:,2)', orizontal_comb));
            eval(sprintf('v6 = Matrix_%d_60(:,2)', orizontal_comb));
            eval(sprintf('v7 = Matrix_%d_75(:,2)', orizontal_comb));
            eval(sprintf('v9 = Matrix_%d_90(:,2)', orizontal_comb));
            
            A=[vm7 vm6 vm4 vm3 vm1 v0 v1 v3 v4 v6 v7 v9]; %for a COP of 5
            
            eval(sprintf('vm7 = Matrix_%d_m75(:,3)', orizontal_comb));
            eval(sprintf('vm6 = Matrix_%d_m60(:,3)', orizontal_comb));
            eval(sprintf('vm4 = Matrix_%d_m45(:,3)', orizontal_comb));
            eval(sprintf('vm3 = Matrix_%d_m30(:,3)', orizontal_comb));
            eval(sprintf('vm1 = Matrix_%d_m15(:,3)', orizontal_comb));
            eval(sprintf('v0 = Matrix_%d_00(:,3)', orizontal_comb));
            eval(sprintf('v1 = Matrix_%d_15(:,3)', orizontal_comb));
            eval(sprintf('v3 = Matrix_%d_30(:,3)', orizontal_comb));
            eval(sprintf('v4 = Matrix_%d_45(:,3)', orizontal_comb));
            eval(sprintf('v6 = Matrix_%d_60(:,3)', orizontal_comb));
            eval(sprintf('v7 = Matrix_%d_75(:,3)', orizontal_comb));
            eval(sprintf('v9 = Matrix_%d_90(:,3)', orizontal_comb));
            
            A=[vm7 vm6 vm4 vm3 vm1 v0 v1 v3 v4 v6 v7 v9]+A;
            
            eval(sprintf('vm7 = Matrix_%d_m75(:,4)', orizontal_comb));
            eval(sprintf('vm6 = Matrix_%d_m60(:,4)', orizontal_comb));
            eval(sprintf('vm4 = Matrix_%d_m45(:,4)', orizontal_comb));
            eval(sprintf('vm3 = Matrix_%d_m30(:,4)', orizontal_comb));
            eval(sprintf('vm1 = Matrix_%d_m15(:,4)', orizontal_comb));
            eval(sprintf('v0 = Matrix_%d_00(:,4)', orizontal_comb));
            eval(sprintf('v1 = Matrix_%d_15(:,4)', orizontal_comb));
            eval(sprintf('v3 = Matrix_%d_30(:,4)', orizontal_comb));
            eval(sprintf('v4 = Matrix_%d_45(:,4)', orizontal_comb));
            eval(sprintf('v6 = Matrix_%d_60(:,4)', orizontal_comb));
            eval(sprintf('v7 = Matrix_%d_75(:,4)', orizontal_comb));
            eval(sprintf('v9 = Matrix_%d_90(:,4)', orizontal_comb));
            
            A=[vm7 vm6 vm4 vm3 vm1 v0 v1 v3 v4 v6 v7 v9] + A;
%A=v0 %take only the one vertical combination.Comment this out if you want vertical combinations to work

[Y,I] = min(A, [], 2);

Index_with_minimal_value=I;

% Minimal_value(1,28)=Minimal_value(1,28)+1;
% c=Minimal_value(1,28);
% 
% Minimal_value(:,c)=Y;

save('Comparison_matrix','Index_with_minimal_value')

Energy=sum(Y)