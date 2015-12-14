% Author: G.Bianchi 
% Email: gibianch@student.ethz.ch
% Modified by PJ

% Semester Project

clc,
close all,

%% Choose the matrix to plot & the title of the plot:
load(['/Users/jayathip/Documents/01_SuAt/01_Hilo/04_Facade/Semester Project Giovanni/matlab/combination_with_minimal_value'])

%i=3
%Setting the titles based on the data set imported
%Coulum 2
if i==2
    g_title='Heating:EnergyTransfer';
    s_title='Heating'
end
%Coulum 3
if i==3
    g_title='Cooling:EnergyTransfer';
    s_title='Cooling'
end
%Coulum 4
if i==4
    g_title='InteriorLights:Electricity';
    s_title='Lighting'
end

if i==6
    g_title='Optimimal Horizontal Configurations ';
    s_title='optimal'
end

%% RUN

M=zeros(24,365);
N=zeros(24,365);
M(:,1)=combination_with_minimal_value(1:24,1);

for j =1:364;
    n=j*24;
    M(:,j+1)=combination_with_minimal_value(n+1:n+24,1);
end


for jj=1:365;
    for kk=1:24;
        if combination_with_minimal_value(24*(jj-1)+kk)==0
            N(kk,jj)=0;
        else
        N(kk,jj)=combination_with_minimal_value(24*(jj-1)+kk);
        end
    end
end

h=figure('Position',[100,100,700,400]);
h=pcolor(N)
shading interp
set(h, 'EdgeColor', 'none')
colormap jet
h=title(g_title,'FontSize',20)
h=ylabel('Hour','FontSize',20);
h=xlabel('Day (of a year)','FontSize',20);
labels = {'config 111','config 112','config 113','config 121','config 122','config 123',...
    'config 131','config 132','config 133','config 211','config 212','config 213',...
    'config 221','config 222','config 223','config 231','config 232','config 233',...
    'config 311','config 312','config 313','config 321','config 322','config 323',...
    'config 331','config 332','config 333'};
colorbar('YTick',1:27,'YTickLabel',labels)
savefig(sprintf('Figures/%s_config.fig',s_title));
saveas(h,sprintf('Figures/%s_config.eps',s_title),'epsc');

