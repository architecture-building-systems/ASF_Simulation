
% clear all

% standard module PVsyst (Shell Solar ST 40, 40 Wp, Voc=23.3V, Isc=2.68)
Rp_ref = 380; % ohm
Rs = 0.8; % ohm
gamma = 1.435;
IoRef = 766*10^(-9); % A
Tc_ref = 25 + 273.15;
egap = 1.12*1.6*10^-19; 
Ncs = 42; 
Isc = 2.68;
Voc = 23.3;
Impp = 2.248;
Vmpp = 16.46;
% muVoc = -0.3/100*Voc; % V/K
% muIsc = 0.03/100*IoRef; % A/K
muVoc = -76*10^-3; % V/K
muIsc = 1.3*10^-3; % A/K

modparams = [Isc,Ncs,Tc_ref,muIsc,egap];
fitparam = [Rs, Rp_ref, gamma, IoRef]; 

% evaluate fit 
ins_ns = [1000,irr_tot_mod_ns];
ins_sh = [1000,irr_tot_mod_sh];
temp = 25 + 273.15;
vmin = -6*42; 
vmax = 40; 
volt_model_var=linspace(vmin, vmax, 1000);
curr_model_ns=diode_equation_var(fitparam, volt_model_var, modparams, ins_ns, temp);
curr_model_sh=diode_equation_var(fitparam, volt_model_var, modparams, ins_sh, temp);

#% module and cell dimensions
length=1260; % cell length, cell orientation along module length
width=294; % cells width
ncell_org = 42;
nparscell_org = 180;
scell_length = 7; % mm
scell_width = 7;

#% cell reverse characteristics
vol_bd = -7;
miller_exp = 3;

#% calculate subcell forward and reverse characteristic
jj=1;
Vmod_ns(:,jj)=volt_model_var;
Imod_ns(:,jj)=curr_model_ns(jj,:)';
Vscell_ns(:,jj)=volt_model_var./ncell_org;
RevScale=1./(1-(abs(Vscell_ns(:,jj))./-vol_bd).^miller_exp);
Iscell_ns(:,jj)=curr_model_ns(jj,:)'.*RevScale./nparscell_org;
 
Vmod_sh(:,jj)=volt_model_var;
Imod_sh(:,jj)=curr_model_sh(jj,:)';
Vscell_sh(:,jj)=volt_model_var./ncell_org;
RevScale=1./(1-(abs(Vscell_sh(:,jj))./-vol_bd).^miller_exp);
Iscell_sh(:,jj)=curr_model_sh(jj,:)'.*RevScale./nparscell_org;


#% facade and module configuration
mod_length = 400; #% cell orientation along module length
mod_width = 400; 

nscell_len = round(mod_length./scell_length)-7;
nscell_wid = round(mod_length./scell_length)-7;
ncell = nscell_len;

#
#% calculate module and array IV curves based on shading matrix and module interconnection

for str_config=1:2 % string configuration 5/10 modules in series

for orient=1:2 % cell orientation horizontal (45 left or -45) / vertical (45 right or +45) 

for mod_diodes=1:3 #% no/one/two module bypass diodes, mod_diodes = 2 is relevant for the needed case, one bypass diode per module 

tt = mod_diodes + (orient-1)*3 + (str_config-1)*6;

#% calculate cell and module IV curves by module
for jj=1:num_panels

#% cell orientation (1=horizontal, 2=vertical on image)
if orient==1
cell_orient(jj)=1; 
elseif orient==2
cell_orient(jj)=2;
end

shading_matrix = shading_mat_panel{jj};
if cell_orient(jj)==1
sh_vec_curr(:,jj) = sum(shading_matrix,2); % sh_vec indicates number of shaded subcells per cell
elseif cell_orient(jj)==2
sh_vec_curr(:,jj) = sum(shading_matrix,1);
end
ns_vec_curr(:,jj)=ncell-sh_vec_curr(:,jj);

for kk=1:ncell
    Vcell_sh{kk,jj} = {Vscell_sh};
    Vcell_ns{kk,jj} = {Vscell_ns};
    Icell_sh{kk,jj} = {sh_vec_curr(kk,jj).*Iscell_sh};
    Icell_ns{kk,jj} = {ns_vec_curr(kk,jj).*Iscell_ns};    
end

#%  add currents of subcells per cell
for kk=1:ncell    
    Vcell_comb{kk,jj} = {Vscell_ns};
    Icell_comb{kk,jj} = Icell_sh{kk,jj}{1,1}+Icell_ns{kk,jj}{1,1}; 
end

#% clear workspace
clear Vcell_comb_int Vmod_curr Imod_curr Pmod_curr
clear Vcell_comb_int_1 Vmod_curr_1 Imod_curr_1 Vmod_curr_int_1 Vcell_comb_int_1 Vmod_curr_1 Imod_curr_1 Pmod_curr_1
clear Vcell_comb_int_2 Vmod_curr_2 Imod_curr_2 Vmod_curr_int_2 Vcell_comb_int_2 Vmod_curr_2 Imod_curr_2 Pmod_curr_2
clear sel_range_1 Vmod_sel_1 Imod_sel_1 Imod_sel_1_wbd 
clear sel_range_2 Vmod_sel_2 Imod_sel_2 Imod_sel_2_wbd 
clear volt_sm1_int volt_sm2_int


#% bypass diodes, this part has to be added for mod_diodes = 2
if (mod_diodes==1)||(mod_diodes==2)
#% add voltage from cell to cell (no bypass diode)
curr_int_points_cell=linspace(1,-0.5,10000);
for kk=1:(ncell-1)
    if kk==1
    Vcell_comb_int{kk,jj}=interp1(Icell_comb{kk,jj},Vscell_ns(:,1),curr_int_points_cell);
    Vcell_comb_int{kk+1,jj}=interp1(Icell_comb{kk+1,jj},Vscell_ns(:,1),curr_int_points_cell);
    Vmod_curr{kk,jj}=Vcell_comb_int{kk,jj}+Vcell_comb_int{kk+1,jj};
    Imod_curr{kk,jj}=curr_int_points_cell;  
    elseif kk>1
    Vmod_curr_int{kk,jj}=interp1(Imod_curr{kk-1,jj},Vmod_curr{kk-1,jj},curr_int_points_cell);
    Vcell_comb_int{kk+1,jj}=interp1(Icell_comb{kk+1,jj},Vscell_ns(:,1),curr_int_points_cell);
    Vmod_curr{kk,jj}=Vmod_curr_int{kk,jj}+Vcell_comb_int{kk+1,jj};
    Imod_curr{kk,jj}=curr_int_points_cell; 
    Pmod_curr{kk,jj}=Imod_curr{kk,jj}.*Vmod_curr{kk,jj};
    end
end

Vmod{jj}=Vmod_curr{kk,jj}; 
Imod{jj}=Imod_curr{kk,jj}; 
Pmod{jj}=Pmod_curr{kk,jj};

#%deleted mod_diodes = 3
#
#% add voltage from cell to cell (second part)
curr_int_points_cell=linspace(1,-0.5,10000);
for kk=1:24
    if kk==1
    Vcell_comb_int_2{kk,jj}=interp1(Icell_comb{kk+25,jj},Vscell_ns(:,1),curr_int_points_cell);
    Vcell_comb_int_2{kk+1,jj}=interp1(Icell_comb{kk+26,jj},Vscell_ns(:,1),curr_int_points_cell);
    Vmod_curr_2{kk,jj}=Vcell_comb_int_2{kk,jj}+Vcell_comb_int_2{kk+1,jj};
    Imod_curr_2{kk,jj}=curr_int_points_cell;  
    elseif kk>1
    Vmod_curr_int_2{kk,jj}=interp1(Imod_curr_2{kk-1,jj},Vmod_curr_2{kk-1,jj},curr_int_points_cell);
    Vcell_comb_int_2{kk+1,jj}=interp1(Icell_comb{kk+26,jj},Vscell_ns(:,1),curr_int_points_cell);
    Vmod_curr_2{kk,jj}=Vmod_curr_int_2{kk,jj}+Vcell_comb_int_2{kk+1,jj};
    Imod_curr_2{kk,jj}=curr_int_points_cell; 
    Pmod_curr_2{kk,jj}=Imod_curr_2{kk,jj}.*Vmod_curr_2{kk,jj};
    end
end

#% add bypass diode by sub-module 
sel_range_1{jj}=Vmod_curr_1{kk,jj}>-5;
Vmod_sel_1{jj}=Vmod_curr_1{kk,jj}(sel_range_1{jj});
Imod_sel_1{jj}=Imod_curr_1{kk,jj}(sel_range_1{jj});
diode_current_1=1.*10^-7.*exp(-Vmod_sel_1{jj}/(1.5*28.*10^-3));
Imod_sel_1_wbd{jj} = Imod_sel_1{jj} + diode_current_1;

sel_range_2{jj}=Vmod_curr_2{kk,jj}>-5;
Vmod_sel_2{jj}=Vmod_curr_2{kk,jj}(sel_range_2{jj});
Imod_sel_2{jj}=Imod_curr_2{kk,jj}(sel_range_2{jj});
diode_current_2=1.*10^-7.*exp(-Vmod_sel_2{jj}/(1.5*28.*10^-3));
Imod_sel_2_wbd{jj} = Imod_sel_2{jj} + diode_current_2;

#% add sub-module voltages
curr_int_points_sm=linspace(-1,1.5,1000);
volt_sm1_int{jj}=interp1(Imod_sel_1_wbd{jj},Vmod_sel_1{jj},curr_int_points_sm);
volt_sm2_int{jj}=interp1(Imod_sel_2_wbd{jj},Vmod_sel_2{jj},curr_int_points_sm);

Vmod{jj}=volt_sm1_int{jj}+volt_sm2_int{jj}; 
Imod{jj}=curr_int_points_sm; 
Pmod{jj}=Vmod{jj}.*Imod{jj};

end

end


for ff=1:num_panels
pmax_mod(ff)=max(Pmod{ff});
end
 
#% module interconnection

if str_config==1
strcomb1=[repmat([0:4],6,1)+repmat([0:9:45]',1,5); repmat([5:9:41],4,1)+repmat([0:3]',1,5)]+1; % strings with 5 modules horizontal/vertical mixed
num_strings=10;
elseif str_config==2 % strings with 10 modules (oriented vertically + one including top row and outer right column)
strcomb1=[[0:4,13:9:49];[8:9:44,12:9:48];[7:9:43,11:9:47];[6:9:42,10:9:46];[5:9:41,9:9:45]]+1; 
num_strings=5;
end

figure(1)
subplot(2,6,tt)
bar(pmax_mod(strcomb1))
title('comb1')
grid on
xlabel('String number')
ylabel('Module MPP (W)')
 
    

#% clear variables
clear sel_range
clear sel_range_par
clear modvolt_int_ser
clear strcurr_int_par
clear Vmod_sel
clear Imod_sel
clear diode_current
clear Istr_ser_comb
clear Vstr_ser_comb
clear Istr_sel_par
clear Vstr_sel_par
clear Varr_par_comb 
clear Iarr_par_comb


if (mod_diodes==1)||(mod_diodes==3) % without or two bypass diodes

#%deleted mod 1 and 3

elseif (mod_diodes==2) % with one bypass
    
#% string serial connection
curr_int_points=linspace(-1,1.5,1000);
for jj=1:num_panels
sel_range{jj}=Vmod{1,jj}>-5;
Vmod_sel{jj}=Vmod{jj}(sel_range{jj});
Imod_sel{jj}=Imod{jj}(sel_range{jj});
diode_current=1.*10^-9.*exp(-Vmod_sel{jj}/(1.5*28.*10^-3));
Imod_sel_new{jj} = Imod_sel{jj} + diode_current;
modvolt_int_ser(:,jj)=interp1(Imod_sel_new{jj},Vmod_sel{jj},curr_int_points);
Vmod_save{jj}=Vmod_sel{jj};
Imod_save{jj}=Imod_sel_new{jj};
end

for ll=1:num_strings
Istr_ser_comb(ll,:) = curr_int_points;
Vstr_ser_comb(ll,:) = sum(modvolt_int_ser(:,strcomb1(ll,:))');
end

#% string parallel connection
volt_int_points=linspace(-5,280,1000);
for jj=1:num_strings
sel_range_par{jj}=Vstr_ser_comb(jj,:)>-5;
Vstr_sel{jj}=Vstr_ser_comb(jj,sel_range_par{jj});
Istr_sel{jj}=Istr_ser_comb(jj,sel_range_par{jj});
[uni_val uni_ind]=unique(Vstr_sel{jj});
strcurr_int_par(:,jj)=interp1(Vstr_sel{1,jj}(uni_ind),Istr_sel{1,jj}(uni_ind),volt_int_points);
end
Varr_par_comb = volt_int_points;
Iarr_par_comb = sum(strcurr_int_par'); 
end

Parr_par_comb = Varr_par_comb.*Iarr_par_comb;
arr_mpp = max(Parr_par_comb);


#% save data

dia_config_save{yy,tt}={str_config, orient, mod_diodes, strcomb1, pmax_mod, Vstr_ser_comb, Istr_ser_comb, Varr_par_comb, Iarr_par_comb, Parr_par_comb, arr_mpp, Vmod_save, Imod_save, Pmod};

end

end 

end




% figure
% subplot(2,2,1)
% plot(Varr_par_comb_wobd,Iarr_par_comb_wobd), hold on
% for rr=1:num_strings
% plot(Vstr_ser_comb_wobd(rr,:),Istr_ser_comb_wobd(rr,:),'--r'),hold on
% end
% axis([-10 300 0 5])
% legend('string parallel connection','strings')
% 
% subplot(2,2,2)
% plot(Varr_par_comb_wbd,Iarr_par_comb_wbd,'-b'), hold on
% for rr=1:num_strings
% plot(Vstr_ser_comb_wbd(rr,:),Istr_ser_comb_wbd(rr,:),'--r'),hold on
% end
% axis([-10 300 0 5])
% legend('string parallel connection','strings')
% 
% 
% subplot(2,2,3)
% plot(Varr_par_comb_wobd,Varr_par_comb_wobd.*Iarr_par_comb_wobd), hold on
% for rr=1:num_strings
% plot(Vstr_ser_comb_wobd(rr,:),Vstr_ser_comb_wobd(rr,:).*Istr_ser_comb_wobd(rr,:),'--r'),hold on
% end
% axis([-10 300 0 500])
% legend('string parallel connection','strings')
% 
% subplot(2,2,4)
% plot(Varr_par_comb_wbd,Varr_par_comb_wbd.*Iarr_par_comb_wbd,'-b'), hold on
% for rr=1:num_strings
% plot(Vstr_ser_comb_wbd(rr,:),Vstr_ser_comb_wbd(rr,:).*Istr_ser_comb_wbd(rr,:),'--r'),hold on
% end
% axis([-10 300 0 500])
% legend('string parallel connection','strings')
