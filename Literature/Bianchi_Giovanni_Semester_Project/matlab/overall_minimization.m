% Author: G.Bianchi
% Email: gibianch@student.ethz.ch
% Semester Project
clear all, clc, close all

load(['Comparison_matrix.mat'])

Minimal_value=Minimal_value(:,1:27); %remove the counter

[Y,I] = min(Minimal_value, [], 2); %Aquire the best horizontal configuration

%Removing all combinations where Y==0
I=I-(Y==0)

combination_with_minimal_value=I;

absolute_minimal_value=Y;

hours_pumping=sum(Y>0) %The hours of pumping time required per year
Pumping_cost=hours_pumping*(60/23)/1000 %60W pump divided into 23 regions. Cost in kWh

save('combination_with_minimal_value','combination_with_minimal_value')

display('Combination 111 is optimal: (number of times)')
numel(combination_with_minimal_value(combination_with_minimal_value==1))

display('Combination 112 is optimal: (number of times)')
numel(combination_with_minimal_value(combination_with_minimal_value==2))

display('Combination 113 is optimal: (number of times)')
numel(combination_with_minimal_value(combination_with_minimal_value==3))

display('Combination 121 is optimal: (number of times)')
numel(combination_with_minimal_value(combination_with_minimal_value==4))

display('Combination 122 is optimal: (number of times)')
numel(combination_with_minimal_value(combination_with_minimal_value==5))

display('Combination 123 is optimal: (number of times)')
numel(combination_with_minimal_value(combination_with_minimal_value==6))

display('Combination 131 is optimal: (number of times)')
numel(combination_with_minimal_value(combination_with_minimal_value==7))

display('Combination 132 is optimal: (number of times)')
numel(combination_with_minimal_value(combination_with_minimal_value==8))

display('Combination 133 is optimal: (number of times)')
numel(combination_with_minimal_value(combination_with_minimal_value==9))

display('Combination 211 is optimal: (number of times)')
numel(combination_with_minimal_value(combination_with_minimal_value==10))

display('Combination 212 is optimal: (number of times)')
numel(combination_with_minimal_value(combination_with_minimal_value==11))

display('Combination 213 is optimal: (number of times)')
numel(combination_with_minimal_value(combination_with_minimal_value==12))

display('Combination 221 is optimal: (number of times)')
numel(combination_with_minimal_value(combination_with_minimal_value==13))

display('Combination 222 is optimal: (number of times)')
numel(combination_with_minimal_value(combination_with_minimal_value==14))

display('Combination 223 is optimal: (number of times)')
numel(combination_with_minimal_value(combination_with_minimal_value==15))

display('Combination 231 is optimal: (number of times)')
numel(combination_with_minimal_value(combination_with_minimal_value==16))

display('Combination 232 is optimal: (number of times)')
numel(combination_with_minimal_value(combination_with_minimal_value==17))

display('Combination 233 is optimal: (number of times)')
numel(combination_with_minimal_value(combination_with_minimal_value==18))

display('Combination 311 is optimal: (number of times)')
numel(combination_with_minimal_value(combination_with_minimal_value==19))

display('Combination 312 is optimal: (number of times)')
numel(combination_with_minimal_value(combination_with_minimal_value==20))

display('Combination 313 is optimal: (number of times)')
numel(combination_with_minimal_value(combination_with_minimal_value==21))

display('Combination 321 is optimal: (number of times)')
numel(combination_with_minimal_value(combination_with_minimal_value==22))

display('Combination 322 is optimal: (number of times)')
numel(combination_with_minimal_value(combination_with_minimal_value==23))

display('Combination 323 is optimal: (number of times)')
numel(combination_with_minimal_value(combination_with_minimal_value==24))

display('Combination 331 is optimal: (number of times)')
numel(combination_with_minimal_value(combination_with_minimal_value==25))

display('Combination 332 is optimal: (number of times)')
numel(combination_with_minimal_value(combination_with_minimal_value==26))

display('Combination 333 is optimal: (number of times)')
numel(combination_with_minimal_value(combination_with_minimal_value==27))