% Import data from text file.
% Initialize variables
    delimiter = ',';
    startRow = 2;
    formatSpec = '%*s%f%f%f%f%f%[^\n\r]';
    
    %orizontal_comb = '112';
    %vertical_rot = '-60';
    
if size(vertical_rot,2)==1
    filename = 'Simulation2_Result/132/0.0/0.0.csv';
    % Open the text file.
    fileID = fopen(filename,'r');
    % Read columns of data according to format string.
    dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'HeaderLines' ,startRow-1, 'ReturnOnError', false);
    % Close the text file.
    fclose(fileID);
    
    orizontal_comb=str2num(orizontal_comb);
    eval(sprintf('Matrix_%d_00 = [dataArray{1:end-1}]', orizontal_comb));
    
elseif size(vertical_rot,2)==2
    filename = ['Simulation2_Result/' orizontal_comb '/' vertical_rot '.0/' vertical_rot '.0.csv'];

    % Open the text file.
    fileID = fopen(filename,'r');

    % Read columns of data according to format string.
    dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'HeaderLines' ,startRow-1, 'ReturnOnError', false);

    % Close the text file.
    fclose(fileID);
    
    % Create output variable
    vertical_rot=str2num(vertical_rot);
    orizontal_comb=str2num(orizontal_comb);
    eval(sprintf('Matrix_%d_%d = [dataArray{1:end-1}]', orizontal_comb, vertical_rot));

elseif size(vertical_rot,2)==3
    filename = ['Simulation2_Result/' orizontal_comb '/' vertical_rot '.0/' vertical_rot '.0.csv'];
    
    % Open the text file.
    fileID = fopen(filename,'r');

    % Read columns of data according to format string.
    dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'HeaderLines' ,startRow-1, 'ReturnOnError', false);

    % Close the text file.
    fclose(fileID);
    
    if vertical_rot == '-15'
    vertical_rot_m= '15'; end

    if vertical_rot == '-30'
    vertical_rot_m= '30'; end

    if vertical_rot == '-45'
    vertical_rot_m= '45'; end

    if vertical_rot == '-60'
    vertical_rot_m= '60'; end

    if vertical_rot == '-75'
    vertical_rot_m= '75'; end

    if vertical_rot == '-90'
    vertical_rot_m= '90'; end

    % Create output variable
    vertical_rot_m=str2num(vertical_rot_m);
    orizontal_comb=str2num(orizontal_comb);
    eval(sprintf('Matrix_%d_m%d = [dataArray{1:end-1}]', orizontal_comb, vertical_rot_m));
    
end

% Clear temporary variables
clearvars filename delimiter startRow formatSpec fileID dataArray vertical_rot ans;
orizontal_comb=num2str(orizontal_comb);
