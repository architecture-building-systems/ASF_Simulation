
clear all

% load irradiance lookup table
% load('curr_model_submod_lookup2')

str1=[3437:3452]';
str1=num2str(str1);
str21=[2 5]';
str22=[10 15 20]';
str21=num2str(str21);
str22=num2str(str22);
str3='hoy_';
str4='_curv_';
str5='.txt';
b11=strcat(str3,str1,str4,str21(1,:),str5);
b12=strcat(str3,str1,str4,str21(2,:),str5);
b13=strcat(str3,str1,str4,str22(1,:),str5);
b14=strcat(str3,str1,str4,str22(2,:),str5);
b15=strcat(str3,str1,str4,str22(3,:),str5);
b21=[b11;b12];
b22=[b13;b14;b15];
numit1=length(b21(:,1));
numit2=length(b22(:,1));
numit=numit1+numit2;

for timeit = 1:16
    
timeit 
    
if timeit<(numit1+1)
endata = importdata(b21(timeit,:),' ',5);
B = reshape(endata.data,44,9);
elseif timeit>numit1
endata = importdata(b22(timeit-numit1,:),' ',5);
B = reshape(endata.data,44,9);
end

inscells=B(:,1);
numcells=44;

panelwidth=0.33;
panellength=1.6;
modarea=panelwidth.*panellength;
cellsurf = panellength/numcells*panelwidth;
irr_tri = inscells.*cellsurf; % Wh/h per unit
irr_pan = sum(irr_tri');

inscells_save(:,timeit)=inscells;

% module and cell dimensions
ncell = 44;
nparcell = 1;

mod_diodes=2; % 1 = w/o bd, 2 = with bd 
jjmax=22; % jj=number of bypass diodes per module
jjstep=ncell/jjmax; % number of cells per bd

% fit to Miasole module
modparams = [2.69,44,298.15,0.0002,1.792e-19]; % [Isc,Ncs,Tc_ref,muIsc,egap]
fitparam = [0.16,429,1.8868,2.569e-05]; % [Rs, Rp_ref, gamma, IoRef]

% evaluate model by insolation

% evaluate fit 
temp = 25 + 273.15;
vmin = -6*ncell; 
vmax = 30; 
volt_model_var = linspace(vmin, vmax, 1000);

for i=1:length(inscells)
tic
ins_submod = [1000,inscells(i)];
curr_model_submod{i} = diode_equation_var_2(fitparam, volt_model_var, modparams, ins_submod, temp);
toc
end

% cell reverse characteristics
vol_bd = -6.1;
miller_exp = 3;

% calculate subcell forward and reverse characteristic
for jj=1:length(inscells)
Vmod_1(:,jj)=volt_model_var;
Imod_1(:,jj)=curr_model_submod{jj}';
Vscell_1(:,jj)=volt_model_var./ncell;
RevScale=1./(1-(abs(Vscell_1(:,jj))./-vol_bd).^miller_exp);
Iscell_1(:,jj)=curr_model_submod{jj}'.*RevScale./nparcell;
end

% figure
% subplot(1,2,1)
% for i=1:length(inscells)
% plot(Vscell_1(:,i),Iscell_1(:,i),'-b'), hold on
% end
% title('Subcell IV curves', 'FontSize',10,'FontWeight','bold')
% xlabel('Voltage (V)', 'FontSize',10,'FontWeight','bold')
% ylabel('Current (A)', 'FontSize',10,'FontWeight','bold')
% axis([-6 1 0 5])
% set(gca,'FontSize',9,'FontWeight','bold')
% 
% subplot(1,2,2)
% for i=1:length(inscells)
% plot(Vmod_1(:,i),Imod_1(:,i),'-b'), hold on
% end
% title('Module 1 IV curves', 'FontSize',10,'FontWeight','bold')
% xlabel('Voltage (V)', 'FontSize',10,'FontWeight','bold')
% ylabel('Current (A)', 'FontSize',10,'FontWeight','bold')
% axis([0 30 0 2.5])
% set(gca,'FontSize',9,'FontWeight','bold')


% module calculation

jj=1; %module number

%  add currents of subcells per cell
for kk=1:ncell   
    Vcell_comb{kk,jj} = Vscell_1(:,kk);
    Icell_comb{kk,jj} = Iscell_1(:,kk); 
end

% without bypass diodes
if mod_diodes==1 % add voltage from cell to cell 
curr_int_points_cell=linspace(-0.5,5,100000);

for kk=1:(ncell-1)
    if kk==1
    Vcell_comb_int{kk,jj}=interp1(Icell_comb{kk,jj},Vcell_comb{1,1},curr_int_points_cell);
    Vcell_comb_int{kk+1,jj}=interp1(Icell_comb{kk+1,jj},Vcell_comb{1,1},curr_int_points_cell);
    Vmod_curr{kk,jj}=Vcell_comb_int{kk,jj}+Vcell_comb_int{kk+1,jj};
    Imod_curr{kk,jj}=curr_int_points_cell;  
    elseif kk>1
    Vmod_curr_int{kk,jj}=interp1(Imod_curr{kk-1,jj},Vmod_curr{kk-1,jj},curr_int_points_cell);
    Vcell_comb_int{kk+1,jj}=interp1(Icell_comb{kk+1,jj},Vcell_comb{1,1},curr_int_points_cell);
    Vmod_curr{kk,jj}=Vmod_curr_int{kk,jj}+Vcell_comb_int{kk+1,jj};
    Imod_curr{kk,jj}=curr_int_points_cell; 
    Pmod_curr{kk,jj}=Imod_curr{kk,jj}.*Vmod_curr{kk,jj};
    end
end

Vmod=Vmod_curr{kk,1}; 
Imod=Imod_curr{kk,1}; 
Pmod=Pmod_curr{kk,1};

[Pmod_mpp(timeit) Pmodmpp_ind]= max(Pmod);
Vmod_mpp(timeit) = Vmod(Pmodmpp_ind);
Imod_mpp(timeit) = Imod(Pmodmpp_ind);

Vmod_s{timeit} = Vmod;
Imod_s{timeit} = Imod;
Pmod_s{timeit} = Vmod.*Imod;


% with bypass diodes 
elseif mod_diodes==2 

curr_int_points_cell=linspace(-0.5,5,300000);

% add voltage from cell to cell
jj=1;
jjstep1=3;
for kk=1:(jjstep1-1)
    if kk==1
    Vcell_comb_int{kk,jj}=interp1(Icell_comb{kk+jjstep1*(jj-1),1},Vcell_comb{1,1},curr_int_points_cell);
    Vcell_comb_int{kk+1,jj}=interp1(Icell_comb{kk+jjstep1*(jj-1)+1,1},Vcell_comb{1,1},curr_int_points_cell);
    Vmod_curr{kk,jj}=Vcell_comb_int{kk,jj}+Vcell_comb_int{kk+1,jj};
    Imod_curr{kk,jj}=curr_int_points_cell;  
    elseif kk>1
    Vmod_curr_int{kk,jj}=interp1(Imod_curr{kk-1,jj},Vmod_curr{kk-1,jj},curr_int_points_cell);
    Vcell_comb_int{kk+1,jj}=interp1(Icell_comb{kk+jjstep1*(jj-1)+1,1},Vcell_comb{1,1},curr_int_points_cell);
    Vmod_curr{kk,jj}=Vmod_curr_int{kk,jj}+Vcell_comb_int{kk+1,jj};
    Imod_curr{kk,jj}=curr_int_points_cell; 
    Pmod_curr{kk,jj}=Imod_curr{kk,jj}.*Vmod_curr{kk,jj};
    end
end

jjmax=22;
jjstep2=2;
for jj=[2:(jjmax-1)]
for kk=1:(jjstep2-1)
    if kk==1
    Vcell_comb_int{kk,jj}=interp1(Icell_comb{kk+jjstep2*(jj-2)+jjstep1,1},Vcell_comb{1,1},curr_int_points_cell);
    Vcell_comb_int{kk+1,jj}=interp1(Icell_comb{kk+jjstep2*(jj-2)+jjstep1,1},Vcell_comb{1,1},curr_int_points_cell);
    Vmod_curr{kk,jj}=Vcell_comb_int{kk,jj}+Vcell_comb_int{kk+1,jj};
    Imod_curr{kk,jj}=curr_int_points_cell;  
    elseif kk>1
    Vmod_curr_int{kk,jj}=interp1(Imod_curr{kk-1,jj},Vmod_curr{kk-1,jj},curr_int_points_cell);
    Vcell_comb_int{kk+1,jj}=interp1(Icell_comb{kk+jjstep2*(jj-2)+jjstep1,1},Vcell_comb{1,1},curr_int_points_cell);
    Vmod_curr{kk,jj}=Vmod_curr_int{kk,jj}+Vcell_comb_int{kk+1,jj};
    Imod_curr{kk,jj}=curr_int_points_cell; 
    Pmod_curr{kk,jj}=Imod_curr{kk,jj}.*Vmod_curr{kk,jj};
    end
end
end

jj=jjmax;
kk=1;
Vcell_comb_int{kk,jj}=interp1(Icell_comb{kk+jjstep2*(jj-2)+jjstep1,1},Vcell_comb{1,1},curr_int_points_cell);
Vmod_curr{kk,jj}=Vcell_comb_int{kk,jj};
Imod_curr{kk,jj}=curr_int_points_cell;  

% add bypass diode by sub-module 
for jj=1:jjmax
    if jj==1
        kk=2;
    else
        kk=1;
    end
sel_range{jj}=Vmod_curr{kk,jj}>-2;
Vmod_sel{jj}=Vmod_curr{kk,jj}(sel_range{jj});
Imod_sel{jj}=Imod_curr{kk,jj}(sel_range{jj});
diode_current=1.*10^-7.*exp(-Vmod_sel{jj}/(1.7.*10^-2));
Imod_sel_wbd{jj} = Imod_sel{jj} + diode_current;
end

% add sub-module voltages
curr_int_points_sm=linspace(-0.5,5,300000);
for jj=1:jjmax
volt_sm_int{jj}=interp1(Imod_sel_wbd{jj},Vmod_sel{jj},curr_int_points_sm);
end

for jj=1:jjmax
Vmod_sub(jj,:)=volt_sm_int{jj}; 
end
Vmod=sum(Vmod_sub);
Imod=curr_int_points_sm; 
Pmod=Vmod.*Imod;

[Pmod_mpp(timeit) Pmodmpp_ind]= max(Pmod);
Vmod_mpp(timeit) = Vmod(Pmodmpp_ind);
Imod_mpp(timeit) = Imod(Pmodmpp_ind);

Vmod_s{timeit} = Vmod;
Imod_s{timeit} = Imod;
Pmod_s{timeit} = Vmod.*Imod;

end


end 

% 
% figure
% subplot(2,2,1)
% boxplot(inscells_save)
% xlabel('Hour','FontSize',14)
% ylabel('W/m^2','FontSize',14)
% set(gca,'FontSize',12)
% % set(gca, 'XTickLabel', [1:124])
% % xticklabel_rotate([1:panelnum],90)
% 
% subplot(2,2,2)
% plot(Pmod_mpp,'-sb'), hold on
% xlabel('Voltage (V)', 'FontSize',10,'FontWeight','bold')
% ylabel('Power at MPP (W)', 'FontSize',10,'FontWeight','bold')
% set(gca,'FontSize',9,'FontWeight','bold')
% axis([1 14 0 60])
% set(gca,'FontSize',9,'FontWeight','bold')
% 
% subplot(2,2,3)
% for i=1:timeit
% plot(Vmod_s{i},Imod_s{i},'-b'), hold on
% end
% title('Module IV curve', 'FontSize',10,'FontWeight','bold')
% xlabel('Voltage (V)', 'FontSize',10,'FontWeight','bold')
% ylabel('Current (A)', 'FontSize',10,'FontWeight','bold')
% set(gca,'FontSize',9,'FontWeight','bold')
% axis([0 30 0 3])
% set(gca,'FontSize',9,'FontWeight','bold')


ins_resh=reshape(sum(inscells_save)./44,16,5);
ins_resh(7,1)=1.15*ins_resh(7,1);
elprod_org=reshape(Pmod_mpp,16,5);
elprod_org(7,1)=1.165*elprod_org(7,1);
effscale = 0.125/(max(smooth(elprod_org(2:15,1)))/(max(smooth(ins_resh(2:15,1)))*modarea));
elprod_resh = effscale.*elprod_org;
eff_resh = elprod_resh./(ins_resh.*modarea).*100;
% eff_resh = effscale.*reshape(Pmod_mpp./(sum(inscells_save)./44.*modarea),16,5).*100;
insdist_sel1 = inscells_save(:,17:(2*16));
insdist_sel2 = inscells_save(:,(4*16+1):(5*16));

save('res_ws3');


figure
subplot(1,3,1)
plot((ins_resh(2:15,1)),'-sk','LineWidth',1.5), hold on
plot((ins_resh(2:15,2)),'-ob','LineWidth',1.5)
plot((ins_resh(2:15,3)),'--oc','LineWidth',1.5)
plot((ins_resh(2:15,4)),'-.og','LineWidth',1.5)
plot((ins_resh(2:15,5)),':or','LineWidth',1.5)
ylabel('Average insolation (W/m2)', 'FontSize',14)
xlabel('Time (h)', 'FontSize',14)
set(gca,'Xtick',[1:14])
set(gca,'Xticklabel',{'6','7','8','9','10','11','12','13','14','15','16','17','18','19'});
xlim([0 15])
ylim([0 1100])
legend('Flat','Cat1','Cat2','Cat3','Cat4')
set(gca,'FontSize',12)

subplot(1,3,2)
plot((elprod_resh(2:15,1)),'-sk','LineWidth',1.5), hold on
plot((elprod_resh(2:15,2)),'-ob','LineWidth',1.5)
plot((elprod_resh(2:15,3)),'--oc','LineWidth',1.5)
plot((elprod_resh(2:15,4)),'-.og','LineWidth',1.5)
plot((elprod_resh(2:15,5)),':or','LineWidth',1.5)
ylabel('Module power at MPP (W)', 'FontSize',14)
xlabel('Time (h)', 'FontSize',14)
set(gca,'Xtick',[1:14])
set(gca,'Xticklabel',{'6','7','8','9','10','11','12','13','14','15','16','17','18','19'});
xlim([0 15])
ylim([0 70])
set(gca,'FontSize',12)

subplot(1,3,3)
plot((eff_resh(2:15,1)),'-sk','LineWidth',1.5), hold on
plot((eff_resh(2:15,2)),'-ob','LineWidth',1.5)
plot((eff_resh(2:15,3)),'--oc','LineWidth',1.5)
plot((eff_resh(2:15,4)),'-.og','LineWidth',1.5)
plot((eff_resh(2:15,5)),':or','LineWidth',1.5)
ylabel('Average efficiency (%)', 'FontSize',14)
xlabel('Time (h)', 'FontSize',14)
set(gca,'Xtick',[1:14])
set(gca,'Xticklabel',{'6','7','8','9','10','11','12','13','14','15','16','17','18','19'});
xlim([0 15])
ylim([0 14])
set(gca,'FontSize',12)


figure
subplot(2,1,1)
boxplot(insdist_sel1)
xlabel('Hour','FontSize',14)
ylabel('W/m^2','FontSize',14)
set(gca,'FontSize',12)

subplot(2,1,2)
boxplot(insdist_sel2)
xlabel('Hour','FontSize',14)
ylabel('W/m^2','FontSize',14)
set(gca,'FontSize',12)

% set(gca, 'XTickLabel', [1:124])
% xticklabel_rotate([1:panelnum],90)
