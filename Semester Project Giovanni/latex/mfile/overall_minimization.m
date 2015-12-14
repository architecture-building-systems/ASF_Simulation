% Overall minimization
% Semester Project
% Author: G.Bianchi
% Email: gibianch@student.ethz.ch

clear all, clc, close all

load(['Users/giovannibianchi/Documents/MATLAB/Comparison_matrix.mat'])

Minimal_value=Minimal_value(:,1:27);

[Y,I] = min(Minimal_value, [], 2);

combination_with_minimal_value=I;

absolute_minimal_value=Y;

save('combination_with_minimal_value','combination_with_minimal_value')