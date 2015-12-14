% Author: G.Bianchi 
% Email: gibianch@student.ethz.ch

% Semester Project
% recursion to import all the simulation file

for t=1:3
    
    t=num2str(t);
    % chose the comb to import: e.g. '23'
    orizontal_comb = ['23',t];
    
    for j = -75:15:90
        clc
        vertical_rot=num2str(j);
        run('import_skript') ;
    end


    orizontal_comb=num2str(orizontal_comb);

    Workspace_name=['Workspace_' orizontal_comb];

    save(Workspace_name)
    clc
    clear all

end