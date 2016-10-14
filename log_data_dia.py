
clear all;

for yy=7:7

if yy==1
filename_panels = 'panels_dia_south_165_0643.txt';
filename_shadows = 'panels_dia_shadowmatrix_south_165_0643.txt'; 
elseif yy==2
filename_panels = 'panels_dia_south_165_0743.txt';
filename_shadows = 'panels_dia_shadowmatrix_south_165_0743.txt'; 
elseif yy==3
filename_panels = 'panels_dia_south_165_0843.txt';
filename_shadows = 'panels_dia_shadowmatrix_south_165_0843.txt';  
elseif yy==4
filename_panels = 'panels_dia_south_165_0943.txt';
filename_shadows = 'panels_dia_shadowmatrix_south_165_0943.txt';
elseif yy==5
filename_panels = 'panels_dia_south_165_1043.txt';
filename_shadows = 'panels_dia_shadowmatrix_south_165_1043.txt';
elseif yy==6
filename_panels = 'panels_dia_south_165_1143.txt';
filename_shadows = 'panels_dia_shadowmatrix_south_165_1143.txt';
elseif yy==7
filename_panels = 'panels_dia_south_165_1243.txt';
filename_shadows = 'panels_dia_shadowmatrix_south_165_1243.txt';
elseif yy==8
filename_panels = 'panels_dia_south_165_1343.txt';
filename_shadows = 'panels_dia_shadowmatrix_south_165_1343.txt';
elseif yy==9
filename_panels = 'panels_dia_south_165_1443.txt';
filename_shadows = 'panels_dia_shadowmatrix_south_165_1443.txt';
elseif yy==10
filename_panels = 'panels_dia_south_165_1543.txt';
filename_shadows = 'panels_dia_shadowmatrix_south_165_1543.txt';
elseif yy==11
filename_panels = 'panels_dia_south_165_1643.txt';
filename_shadows = 'panels_dia_shadowmatrix_south_165_1643.txt';
elseif yy==12
filename_panels = 'panels_dia_south_165_1743.txt';
filename_shadows = 'panels_dia_shadowmatrix_south_165_1743.txt';
elseif yy==13
filename_panels = 'panels_dia_south_165_1843.txt';
filename_shadows = 'panels_dia_shadowmatrix_south_165_1843.txt';
end

% load module insolation data
% dni, glo, dif
ins_clear_day_june=[0,0,0;0,0,0;0,0,0;0,2,2;471,101,35;713,260,44;839,438,49;892,608,63;920,759,79;924,869,97;933,941,106;935,963,109;937,937,104;930,859,93;914,738,77;893,588,60;828,413,49;685,236,44;441,84,32;0,1,1;0,0,0;0,0,0;0,0,0];

irr_dni_vec=ins_clear_day_june(:,1);
irr_gl_vec=ins_clear_day_june(:,2);
irr_dif_vec=ins_clear_day_june(:,3);

AA = importdata(filename_panels,' ',21);
BB = AA.data;
Bs = BB;
shadFrac=Bs(:,1);
projSurf=Bs(:,18);
% skyFrac=Bs(:,19);
skyFrac_ns=0.6;
skyFrac_sh=0.4;
skyFrac_all=0.5;
albedo=0.2;

% time setting
yy2=yy+5;

% insolation by panel
mod_area=0.4*0.4;

irr_dir_mod_all=irr_dni_vec(yy2)'.*(1-shadFrac).*projSurf.*mod_area;
irr_dir_mod_all(irr_dir_mod_all<0)=0;
irr_dif_mod_all=irr_dif_vec(yy2)'.*skyFrac_all.*mod_area;
irr_dif_mod_all(irr_dif_mod_all<0)=0;
irr_ref_mod_all=irr_gl_vec(yy2)'.*(1-skyFrac_all).*mod_area.*albedo;
irr_ref_mod_all(irr_ref_mod_all<0)=0;
irr_tot_mod_all_dia(:,yy)=irr_dir_mod_all+irr_dif_mod_all+irr_ref_mod_all;

% insolation panel shaded/non-shaded
irr_dir_mod=irr_dni_vec(yy2)*projSurf(1);
irr_dir_mod(irr_dir_mod<0)=0;
irr_dif_mod_ns=irr_dif_vec(yy2)*skyFrac_ns;
irr_dif_mod_sh=irr_dif_vec(yy2)*skyFrac_sh;
irr_ref_mod_ns=irr_gl_vec(yy2)*(1-skyFrac_ns)*albedo;
irr_ref_mod_sh=irr_gl_vec(yy2)*(1-skyFrac_sh)*albedo;
irr_tot_mod_ns=irr_dir_mod+irr_dif_mod_ns+irr_ref_mod_ns;
irr_tot_mod_sh=irr_dif_mod_sh+irr_ref_mod_sh;


% load module shading data
shading_vec = importdata(filename_shadows);
shading_vec_form=double(char(shading_vec));
shading_vec_form(shading_vec_form==70)=0; % False (unverschattet)
shading_vec_form(shading_vec_form==84)=1; % True (verschattet)
shading_vec_new=shading_vec_form(:,1);

num_panels=50;
num_points=50;
num_segments=num_points.*num_points;
shading_mat=reshape(shading_vec_new,num_segments,num_panels);
for i=1:num_panels
shading_mat_panel{i}=reshape(shading_mat(:,i),num_points,num_points);
shading_mat_panel2{i}=reshape(shading_mat(:,i),num_points,num_points);
shading_mat_panel2{1,i}(1,1)=1;
shading_mat_panel2{1,i}(50,50)=0;
end

assloc=reshape((repmat([50:-10:10],10,1)-repmat([0:9]',1,5))',1,50);

tic
electric_model_dia
toc

end

save('irr_tot_mod_all_dia_iv','irr_tot_mod_all_dia')
save('dia_config_save_iv','dia_config_save')

load dia_config_save_iv
load irr_tot_mod_all_dia_iv

for inst=9:9
mpparr_dia_nobp_min45_str5ser(inst) = dia_config_save{inst,1}{1,11};
mpparr_dia_1bp_min45_str5ser(inst) = dia_config_save{inst,2}{1,11};
mpparr_dia_2bp_min45_str5ser(inst) = dia_config_save{inst,3}{1,11};
mpparr_dia_nobp_plus45_str5ser(inst) = dia_config_save{inst,4}{1,11};
mpparr_dia_1bp_plus45_str5ser(inst) = dia_config_save{inst,5}{1,11};
mpparr_dia_2bp_plus45_str5ser(inst) = dia_config_save{inst,6}{1,11};
mpparr_dia_nobp_min45_str10ser(inst) = dia_config_save{inst,7}{1,11};
mpparr_dia_1bp_min45_str10ser(inst) = dia_config_save{inst,8}{1,11};
mpparr_dia_2bp_min45_str10ser(inst) = dia_config_save{inst,9}{1,11};
mpparr_dia_nobp_plus45_str10ser(inst) = dia_config_save{inst,10}{1,11};
mpparr_dia_1bp_plus45_str10ser(inst) = dia_config_save{inst,11}{1,11};
mpparr_dia_2bp_plus45_str10ser(inst) = dia_config_save{inst,12}{1,11};
end 

sum_mpparr_dia_nobp_min45_str5ser=sum(mpparr_dia_nobp_min45_str5ser);
sum_mpparr_dia_1bp_min45_str5ser=sum(mpparr_dia_1bp_min45_str5ser);
sum_mpparr_dia_2bp_min45_str5ser=sum(mpparr_dia_2bp_min45_str5ser);
sum_mpparr_dia_nobp_plus45_str5ser=sum(mpparr_dia_nobp_plus45_str5ser);
sum_mpparr_dia_1bp_plus45_str5ser=sum(mpparr_dia_1bp_plus45_str5ser);
sum_mpparr_dia_2bp_plus45_str5ser=sum(mpparr_dia_2bp_plus45_str5ser);
sum_mpparr_dia_nobp_min45_str10ser=sum(mpparr_dia_nobp_min45_str10ser);
sum_mpparr_dia_1bp_min45_str10ser=sum(mpparr_dia_1bp_min45_str10ser);
sum_mpparr_dia_2bp_min45_str10ser=sum(mpparr_dia_2bp_min45_str10ser);
sum_mpparr_dia_nobp_plus45_str10ser=sum(mpparr_dia_nobp_plus45_str10ser);
sum_mpparr_dia_1bp_plus45_str10ser=sum(mpparr_dia_1bp_plus45_str10ser);
sum_mpparr_dia_2bp_plus45_str10ser=sum(mpparr_dia_2bp_plus45_str10ser);
sum_mpparr_dia_comb=[sum_mpparr_dia_nobp_min45_str5ser,sum_mpparr_dia_1bp_min45_str5ser,sum_mpparr_dia_2bp_min45_str5ser,sum_mpparr_dia_nobp_plus45_str5ser,sum_mpparr_dia_1bp_plus45_str5ser,sum_mpparr_dia_2bp_plus45_str5ser,sum_mpparr_dia_nobp_min45_str10ser,sum_mpparr_dia_1bp_min45_str10ser,sum_mpparr_dia_2bp_min45_str10ser,sum_mpparr_dia_nobp_plus45_str10ser,sum_mpparr_dia_1bp_plus45_str10ser,sum_mpparr_dia_2bp_plus45_str10ser]./1000;


% module peak efficiency
mpp_mod_1000=14;
mod_area_active=(50*0.7)^2; % 0.1225 m2
mod_area_real=0.4^2; % 0.16 m2
peakeff_mod_active=0.1143;
peakeff_mod_real=0.0875;

% array efficiency
irr_mod_sum_dia = sum(irr_tot_mod_all_dia);
eff_arr_dia_avg =sum_mpparr_dia_comb./sum(irr_mod_sum_dia).*100;
eff_dia_nobp_min45_str5ser = mpparr_dia_nobp_min45_str5ser./irr_mod_sum_dia.*100;
eff_dia_1bp_min45_str5ser = mpparr_dia_1bp_min45_str5ser./irr_mod_sum_dia.*100;
eff_dia_2bp_min45_str5ser = mpparr_dia_2bp_min45_str5ser./irr_mod_sum_dia.*100;
eff_dia_nobp_plus45_str5ser = mpparr_dia_nobp_plus45_str5ser./irr_mod_sum_dia.*100;
eff_dia_1bp_plus45_str5ser = mpparr_dia_nobp_plus45_str5ser./irr_mod_sum_dia.*100;
eff_dia_2bp_plus45_str5ser = mpparr_dia_nobp_plus45_str5ser./irr_mod_sum_dia.*100;
eff_dia_nobp_min45_str10ser = mpparr_dia_nobp_min45_str10ser./irr_mod_sum_dia.*100;
eff_dia_1bp_min45_str10ser = mpparr_dia_1bp_min45_str10ser./irr_mod_sum_dia.*100;
eff_dia_2bp_min45_str10ser = mpparr_dia_2bp_min45_str10ser./irr_mod_sum_dia.*100;
eff_dia_nobp_plus45_str10ser = mpparr_dia_nobp_plus45_str10ser./irr_mod_sum_dia.*100;
eff_dia_1bp_plus45_str10ser = mpparr_dia_nobp_plus45_str10ser./irr_mod_sum_dia.*100;
eff_dia_2bp_plus45_str10ser = mpparr_dia_nobp_plus45_str10ser./irr_mod_sum_dia.*100;



figure
subplot(1,2,1)
plot(mpparr_dia_nobp_min45_str5ser,'-sb','LineWidth',1.5), hold on
plot(mpparr_dia_1bp_min45_str5ser,'--sb','LineWidth',1.5)
plot(mpparr_dia_2bp_min45_str5ser,':sb','LineWidth',1.5)
plot(mpparr_dia_nobp_plus45_str5ser,'-sm','LineWidth',1.5)
plot(mpparr_dia_1bp_plus45_str5ser,'--sm','LineWidth',1.5)
plot(mpparr_dia_2bp_plus45_str5ser,':sm','LineWidth',1.5)
legend('No bypass diode / -45 degree','One bypass diode / -45 degree','Two bypass diodes / -45 degree', 'No bypass diode / +45 degree','One bypass diode / +45 degree','Two bypass diodes / +45 degree')
xlabels={'6','7','8','9','10','11','12','13','14','15','16','17','18'};
set(gca, 'XTick',[1:13])
set(gca, 'XTickLabel', xlabels,'FontSize',9,'FontWeight','bold')
grid on
xlim([0 14])
ylim([0 600])
xlabel('Solar time (h)', 'FontSize',10,'FontWeight','bold')
ylabel('Maximum power point (W)', 'FontSize',10,'FontWeight','bold')
set(gca, 'FontSize',9,'FontWeight','bold')

% subplot(1,2,2)
% plot(eff_dia_nobp_min45_str5ser,'-sb','LineWidth',1.5), hold on
% plot(eff_dia_1bp_min45_str5ser,'--sb','LineWidth',1.5)
% plot(eff_dia_2bp_min45_str5ser,':sb','LineWidth',1.5)
% plot(eff_dia_nobp_plus45_str5ser,'-sm','LineWidth',1.5)
% plot(eff_dia_1bp_plus45_str5ser,'--sm','LineWidth',1.5)
% plot(eff_dia_2bp_plus45_str5ser,':sm','LineWidth',1.5)
% xlabels={'6','7','8','9','10','11','12','13','14','15','16','17','18'};
% set(gca, 'XTick',[1:13])
% set(gca, 'XTickLabel', xlabels,'FontSize',9,'FontWeight','bold')
% grid on
% xlim([0 14])
% ylim([0 15])
% xlabel('Solar time (h)', 'FontSize',10,'FontWeight','bold')
% ylabel('Modules average operating efficiency (%)', 'FontSize',10,'FontWeight','bold')
% set(gca, 'FontSize',9,'FontWeight','bold')


subplot(1,2,2)
plot(mpparr_dia_nobp_min45_str10ser,'-sb','LineWidth',1.5), hold on
plot(mpparr_dia_1bp_min45_str10ser,'--sb','LineWidth',1.5)
plot(mpparr_dia_2bp_min45_str10ser,':sb','LineWidth',1.5)
plot(mpparr_dia_nobp_plus45_str10ser,'-sm','LineWidth',1.5)
plot(mpparr_dia_1bp_plus45_str10ser,'--sm','LineWidth',1.5)
plot(mpparr_dia_2bp_plus45_str10ser,':sm','LineWidth',1.5)
legend('No bypass diode / -45 degree','One bypass diode / -45 degree','Two bypass diodes / -45 degree', 'No bypass diode / +45 degree','One bypass diode / +45 degree','Two bypass diodes / +45 degree')
xlabels={'6','7','8','9','10','11','12','13','14','15','16','17','18'};
set(gca, 'XTick',[1:13])
set(gca, 'XTickLabel', xlabels,'FontSize',9,'FontWeight','bold')
grid on
xlim([0 14])
ylim([0 600])
xlabel('Solar time (h)', 'FontSize',10,'FontWeight','bold')
ylabel('Maximum power point (W)', 'FontSize',10,'FontWeight','bold')
set(gca, 'FontSize',9,'FontWeight','bold')

% subplot(1,2,2)
% plot(eff_dia_nobp_min45_str10ser,'-sb','LineWidth',1.5), hold on
% plot(eff_dia_1bp_min45_str10ser,'--sb','LineWidth',1.5)
% plot(eff_dia_2bp_min45_str10ser,':sb','LineWidth',1.5)
% plot(eff_dia_nobp_plus45_str10ser,'-sm','LineWidth',1.5)
% plot(eff_dia_1bp_plus45_str10ser,'--sm','LineWidth',1.5)
% plot(eff_dia_2bp_plus45_str10ser,':sm','LineWidth',1.5)
% xlabels={'6','7','8','9','10','11','12','13','14','15','16','17','18'};
% set(gca, 'XTick',[1:13])
% set(gca, 'XTickLabel', xlabels,'FontSize',9,'FontWeight','bold')
% grid on
% xlim([0 14])
% ylim([0 15])
% xlabel('Solar time (h)', 'FontSize',10,'FontWeight','bold')
% ylabel('Modules average operating efficiency (%)', 'FontSize',10,'FontWeight','bold')
% set(gca, 'FontSize',9,'FontWeight','bold')



figure
bar(sum_mpparr_dia_comb)


export_electric_dia=[sum_mpparr_dia_comb',eff_arr_dia_avg'];








