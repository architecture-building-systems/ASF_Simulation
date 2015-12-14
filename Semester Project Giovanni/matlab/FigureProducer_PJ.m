%Figure Producer
%Prageeth Jayathissa
%19.01.2015
clear all
clc

%note that for loops can't be used as the m_files that are being run have
%'clearall' comands embedded within them

%Heating
i=2
[A,Y,I,Index_with_minimal_value,Minimal_value]=func_comb_analysis_PJ(i)
overall_minimization
i=2 %Becuse it gets deleted in 'overall_minimization', and is necessary for the next file
plot_matrix_comb
clear
i=2
[A,Y,I,Index_with_minimal_value]=func_one_comb_analysis_PJ(i,'111')
minimal_plot_PJ


i=3
[A,Y,I,Index_with_minimal_value,Minimal_value]=func_comb_analysis_PJ(i)
overall_minimization
i=3
plot_matrix_comb
clear
i=3
[A,Y,I,Index_with_minimal_value]=func_one_comb_analysis_PJ(i,'111')
minimal_plot_PJ

i=4
[A,Y,I,Index_with_minimal_value,Minimal_value]=func_comb_analysis_PJ(i)
overall_minimization
i=4
plot_matrix_comb
clear
i=4
[A,Y,I,Index_with_minimal_value]=func_one_comb_analysis_PJ(i,'111')
minimal_plot_PJ

i=6
combinations_analysis_PJ_total
i=6
overall_minimization
i=6
plot_matrix_comb
i=6
one_comb_analysis_total_PJ
minimal_plot_PJ
%%
close all
h1=openfig('Figures/Heating_config.fig','reuse');
ax1=gca
h2=openfig('Figures/Cooling_config.fig','reuse');
ax2=gca
h3=openfig('Figures/Lighting_config.fig','reuse');
ax3=gca
h4=openfig('Figures/optimal_config.fig','reuse');
ax4=gca

h5=figure
axes
s1=subplot(2,2,1)
title('Heating Energy Configurations','FontSize',10)
ylabel('Hour','FontSize',10);
xlabel('Day (of a year)','FontSize',10);
s2=subplot(2,2,2)
title('Cooling Energy Configurations','FontSize',10)
ylabel('Hour','FontSize',10);
xlabel('Day (of a year)','FontSize',10);
s3=subplot(2,2,3)
title('Lighting Energy Configurations','FontSize',10)
ylabel('Hour','FontSize',10);
xlabel('Day (of a year)','FontSize',10);
s4=subplot(2,2,4)
title('Optimum Horizontal Configurations','FontSize',10)
ylabel('Hour','FontSize',10);
xlabel('Day (of a year)','FontSize',10);

fig1=get(ax1,'children')
fig2=get(ax2,'children')
fig3=get(ax3,'children')
fig4=get(ax4,'children')

copyobj(fig1,s1)
copyobj(fig2,s2)
copyobj(fig3,s3)
copyobj(fig4,s4)


