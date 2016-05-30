% Author: G.Bianchi 
% Email: gibianch@student.ethz.ch
% Semester Project

clc,
close all,

M=zeros(24,365);
N=zeros(24,365);
%i=3
H_config=1

M(:,1)=Index_with_minimal_value(1:24,H_config);

for j =1:364;
    n=j*24;
    M(:,j+1)=Index_with_minimal_value(n+1:n+24,H_config);
end

%Looping through all 8760 days and catergorising them into a table with
%hours on the y axis and days on the y axis
%Note: 24*(jj-1)+kk is the hour in the year. It is like a counter


if min(size(Index_with_minimal_value))~=1
for jj=1:365;
    for kk=1:24;
        if combination_with_minimal_value(24*(jj-1)+kk)==0 %Index_with_minimal_value(24*(jj-1)+kk,combination_with_minimal_value(24*(jj-1)+kk))==0;
            N(kk,jj)=NaN;
        else
        N(kk,jj)=Index_with_minimal_value(24*(jj-1)+kk,combination_with_minimal_value(24*(jj-1)+kk));
        end
    end
end
end

%Coulum 2
if i==2
    g_title='Heating:EnergyTransfer [J](Hourly) ';
    s_title='Heating'
end
%Coulum 3
if i==3
    g_title='Cooling:EnergyTransfer [J](Hourly) ';
    s_title='Cooling'
end
%Coulum 4
if i==4
    g_title='InteriorLights:Electricity [J](Hourly) ';
    s_title='Lighting'
end

if i==6
    g_title='Optimimal Vertical Configurations ';
    s_title='optimal'
end

h=figure('Position',[100,100,700,400]);
h=pcolor(M)
shading interp
set(h, 'EdgeColor', 'none')
colormap jet
title(g_title,'FontSize',20)
ylabel('Hour','FontSize',20);
xlabel('Day (of a year)','FontSize',20);
labels = {'Position -75^{\circ}','Position -60^{\circ}','Position -45^{\circ}','Position -30^{\circ}', ...
    'Position -15^{\circ}','Position 0^{\circ}','Position 15^{\circ}','Position 30','Position 45^{\circ}', ...
    'Position 60^{\circ}','Position 75^{\circ}','Position 90^{\circ}'};
colorbar('YTickLabel',labels,'FontSize',20);
savefig(sprintf('Figures/%s_vert.fig',s_title));
saveas(h,sprintf('Figures/%s_vert.eps',s_title),'epsc');
