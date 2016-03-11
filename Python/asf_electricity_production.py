# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 18:27:17 2016

Calculate Electrical Power of ASF

Authors: Johannes Hofer, Jeremias Schmidli

"""

from pylab import *

clear(mstring('all'))
# close all

create_plots_flag = True

#Simulation_Data_Folder = 'C:\Users\Assistenz\Documents\MT_Jeremias\Simulation_Data\RadiationEvaluation\Radiation_electrical_sunTracking';
Simulation_Data_Folder = ('C:\\Users\\Assistenz\\Documents\\MT_Jeremias\\Simulation_Data\\RadiationEvaluation\\Radiation_electrical_sunTracking_allFiles_sameHour')
Read_json_Folder = ('C:\\Users\\Assistenz\\Documents\\MT_Jeremias\\python-matlab-bridge-master\\pymatbridge\\matlab')

addpath(Simulation_Data_Folder)
addpath(Read_json_Folder)

filename = mstring('RadiationResultsElectrical_tracking')
filetype = mstring('.csv')

# load irradiance lookup table
# load('curr_model_submod_lookup2')
# load('curr_model_submod_lookup2_constTemp')
load(mstring('curr_model_submod_lookup3'))
curr_model_submod_lookup2 = curr_model_submod_lookup3(mslice[:], 9)

# % load irradiance data 
# str11=[10:10:90]';
# str11=num2str(str11);
# str12=[100:10:180]';
# str12=num2str(str12);
# str21='hoy_3391_angle_';
# str22='.txt';
# b1=strcat(str21,str11,str22);
# b2=strcat(str21,str12,str22);
# numroofit=length(b1(:,1))+length(b1(:,1))+1;

numASFit = 5

# filenames = {'RadiationResultsElectrical_test12.csv'};
filenames = cell(1, numASFit)

for i in mslice[1:numASFit]:
    filenames(1, i).lvalue = mcat([filename, num2str(i - 1), filetype])
    end

    # filenames = {'RadiationResultsElectrical_test12.csv'};


    # module and cell dimensions

    # ncell = 44;
    # nparcell = 2;
    # panelwidth=0.37;
    # panellength=1.7;
    # panelsize=panelwidth*panellength;
    # apertwidth=0.37-0.04;
    # apertlength=1.7-0.1;
    # apertsize=apertwidth*apertlength;
    ncell = 48
    nparcell = 16
    cellsPerGridpoint = 3
    panelwidth = 0.4
    panellength = 0.4
    panelsize = panelwidth * panellength
    # apertwidth=panelwidth-0.02;
    # apertlength=panellength-0.02;
    # apertsize=apertwidth*apertlength;
    scellsize = (panelwidth / ncell) * (panellength / nparcell)

    varPVsize = 0#change the size of the PV area, this is done in steps of 2
    # times the radiation gridsize, so 0 corresponds a PV-size of 400mm, 
    # 1 corresponds to PV-size of 350mm, 2 corresponds to 300mm etc. 
    varncell = ncell - varPVsize * 2 * cellsPerGridpoint
    varnparcell = nparcell - varPVsize * 2
    apertsize = varnparcell / nparcell * panelwidth * varncell / ncell * panellength

    # reference module
    refmodwidth = 0.294
    refmodlength = 1.260
    refmodsize = refmodwidth * refmodlength
    refncell = 42
    refnparcell = 180
    refscellwidth = refmodwidth / refncell
    refscelllength = refmodlength / refnparcell
    refscellsize = refscellwidth * refscelllength
    scellscale_factor = scellsize / refscellsize

    # lookup iv curve 
    temp = 25 + 273.15
    vmin = -6 * varncell
    vmax = 0.8 * varncell#30
    volt_model_var = linspace(vmin, vmax, 1000)

    # module efficiency 
    insrefind = 201# 1000 w/m2
    trefind = 1
    # apertscale=panelsize/apertsize;
    apertscale = apertsize / panelsize
    modmpprating = 40#module maximum power point rating
    modmppsim = max(volt_model_var *elmul* curr_model_submod_lookup2(insrefind, trefind))#module maximum power point simulation
    currscale = modmpprating / modmppsim
    
    # model setting
    mod_diodes = 1# 1 = w/o bd, 2 = with bd
    
    # load temperature corresponding to Simulation Data:
    temp_amb = json_read(mstring('TempTracking.json'))
    
    # number of panels in evaluated ASF:
    panelnum = 50
    
    # preallocate data for speed:
    Pmod_mpp = NaN(numASFit, panelnum)
    Vmod_mpp = NaN(numASFit, panelnum)
    Imod_mpp = NaN(numASFit, panelnum)
    Ins_mod = NaN(numASFit, panelnum)
    Ins_mod_mean = NaN(numASFit, panelnum)
    Ins_mod_rmsd = NaN(numASFit, panelnum)
    
    
    Ins_mod_maxdiff = NaN(numASFit, panelnum)
    
    Ins_sum_roof = NaN(numASFit)
    Ins_avg_roof = NaN(numASFit)
    Pmpp_sum_roof = NaN(numASFit)
    Pmpp_avg_roof = NaN(numASFit)
    effap_arr = NaN(numASFit)
    effmod_arr = NaN(numASFit)
    ins_rmsd_avg = NaN(numASFit)
    
    # for rorient = 1:numroofit
    for rorient in mslice[1:numASFit]:
    
        tic
        #     if rorient==1
        #     endata = importdata(char(filenames(rorient)),',',3);
        #     elseif (rorient>1)&&(rorient<(length(b1(:,1))+2))
        #     endata = importdata(b1(rorient-1,:),' ',7);
        #     elseif rorient>(length(b1(:,1))+1)
        #     endata = importdata(b2(rorient-(length(b1(:,1))+1),:),' ',7);
        #     end
    
    
        end
        ata = importdata(char(filenames(rorient)), mstring(','), 7); print ata
    
    
        # irrtot = str2num(cell2mat(endata.textdata(2))); % Wh/h total
        B = end; print B
        ata.data
    
        #     B=ones(50,256);
        #     panelnum = length(B(:,1));
        #     Bs(1:panelnum,:) = B;    
        Bs = B
    
        # trisurf=0.5*panellength/ncell*2*panelwidth; % triangle size
        trisurf = panellength / nparcell * panelwidth / nparcell# triangle size
        irr_tri = Bs *elmul* trisurf# Wh/h per unit
        irr_pan2 = sum(irr_tri, 2).cT
    
    
        Vmod_tot = NaN(panelnum, length(volt_model_var))
        Imod_tot = NaN(panelnum, length(volt_model_var))
        Pmod_tot = NaN(panelnum, length(volt_model_var))
    
    
        for mod_sel in mslice[1:panelnum]:    # module iteration
    
            # select irradiance per module
            irr_mod_sel = 1 / trisurf *elmul* irr_tri(mod_sel, mslice[:])
    
            # irr_mod_p1 = sum(reshape(irr_mod_sel,2,length(irr_mod_sel)/2))/2; % [(It1+It2)/2, (It3+It4)/2, (It5+It6)/2, etc]
            # irr_mod_p2 = irr_mod_sel(1:2:end); % [It1, It3, It5, etc]
            # irr_mod_p3 = irr_mod_sel(2:2:end); % [It2, It4, It6, etc]
            # 
            # irr_mod_mat(:,1) = reshape([irr_mod_p2; irr_mod_p1],[],1);
            # irr_mod_mat(:,2) = reshape([irr_mod_p1; irr_mod_p3],[],1);
            irr_mod_mat_rnd = round(vec2mat(irr_mod_sel, nparcell) * 1000)    # create a grid with all radiation points first (16x16)
            irr_mod_mat_rnd = irr_mod_mat_rnd(mslice[1 + varPVsize:end - varPVsize], mslice[1 + varPVsize:end - varPVsize])
    
            ins_module = sum(sum(irr_mod_mat_rnd)) * trisurf    # insolation per module [Wh]
            ins_modarea = ins_module / panelsize    # insolation per module area [Wh/m2]
    
            # bypass diode setting
            # jjmax=22; % jj=number of bypass diodes per module
            # jjstep=ncell/jjmax; % number of cells per bd
            curr_model_submod = cell(length(irr_mod_mat_rnd))
            for i in mslice[1:length(irr_mod_mat_rnd(mslice[:], 1))]:
                for j in mslice[1:length(irr_mod_mat_rnd(1, mslice[:]))]:
                    insind = round(irr_mod_mat_rnd(i, j) / 5) + 1
                    curr_model_submod(i, j).lvalue = scellscale_factor * currscale *elmul* curr_model_submod_lookup2(insind, trefind)
    #        end
    #        end
    
            # cell reverse characteristics
            vol_bd = -6.1
            miller_exp = 3
    
            # calculate subcell forward and reverse iv curve
            # for jj=1:length(irr_mod_mat(:,1))
            Vmod = volt_model_var
            Imod = cell(varnparcell)
    
            #         Vscell = volt_model_var./ncell;
            Vscell = volt_model_var /eldiv/ refncell
            Iscell = NaN(varnparcell, varnparcell, length(curr_model_submod_lookup2(1, 1)))
            RevScale = 1. / (1 - (abs(Vscell) /eldiv/ -vol_bd) **elpow** miller_exp)
    
            for ii in mslice[1:varnparcell]:
                for jj in mslice[1:varnparcell]:
                    #        Vmod(ii,jj)=volt_model_var;
                    Imod(ii, jj).lvalue = curr_model_submod(ii, jj).cT
                    #                Iscell(ii,jj,:)=curr_model_submod{ii,jj}.*RevScale./nparcell;
                    Iscell(ii, jj, mslice[:]).lvalue = curr_model_submod(ii, jj) *elmul* RevScale /eldiv/ refnparcell
    
                    #        Vmod(:,jj)=volt_model_var;
                    #        Imod(:,jj)=curr_model_submod{jj,1}';
                    #        Vscell(:,jj)=volt_model_var./ncell;
                    #        RevScale=1./(1-(abs(Vscell(:,jj))./-vol_bd).^miller_exp);
                    #        Iscell(:,jj)=curr_model_submod{jj,1}'.*RevScale./nparcell;
    
                    # Vmod_2(:,jj)=volt_model_var;
                    # Imod_2(:,jj)=curr_model_submod{jj,2}';
                    # Vscell_2(:,jj)=volt_model_var./ncell;
                    # RevScale=1./(1-(abs(Vscell_2(:,jj))./-vol_bd).^miller_exp);
                    # Iscell_2(:,jj)=curr_model_submod{jj,2}'.*RevScale./nparcell;
    #        end
    #        end
    
            # module calculation
    
            # jj=1; %module number
            Icell_comb = cell(varncell, 1)
            #  add currents of subcells per cell
            pointCounter = 0
            for kk in mslice[1:varncell]:
                if mod(kk - 1, 3) == 0:
                    pointCounter = pointCounter + 1
    #            end
                #     Vcell_comb{kk,jj} = volt_model_var';
                #             Icell_comb{kk,1} = Iscell{:,kk} + Iscell_2(:,kk); 
                Icell_comb(kk, 1).lvalue = squeeze(sum(Iscell(pointCounter, mslice[:], mslice[:]), 2))
    
    #        end
    
            # without bypass diodes
            if mod_diodes == 1:                                # add voltage from cell to cell
                curr_int_points_cell = linspace(-0.5, 5, 1000)
                #             curr_int_points_cell=linspace(-0.5*nparcell,5.5*nparcell,1000);
    
                Vcell_comb_int = cell(varncell, 1)
                Vmod_curr = cell(varncell - 1, 1)
                Imod_curr = cell(varncell - 1, 1)
                Vmod_curr_int = cell(varncell - 1, 1)
                Pmod_curr = cell(varncell - 1, 1)
    
                for kk in mslice[1:(varncell - 1)]:
                    if kk == 1:
                        Vcell_comb_int(kk, 1).lvalue = interp1(Icell_comb(kk, 1), Vscell, curr_int_points_cell)
                        Vcell_comb_int(kk + 1, 1).lvalue = interp1(Icell_comb(kk + 1, 1), Vscell, curr_int_points_cell)
                        Vmod_curr(kk, 1).lvalue = Vcell_comb_int(kk, 1) + Vcell_comb_int(kk + 1, 1)
                        Imod_curr(kk, 1).lvalue = curr_int_points_cell
                    elif kk > 1:
                        Vmod_curr_int(kk, 1).lvalue = interp1(Imod_curr(kk - 1, 1), Vmod_curr(kk - 1, 1), curr_int_points_cell)
                        Vcell_comb_int(kk + 1, 1).lvalue = interp1(Icell_comb(kk + 1, 1), Vscell, curr_int_points_cell)
                        Vmod_curr(kk, 1).lvalue = Vmod_curr_int(kk, 1) + Vcell_comb_int(kk + 1, 1)
                        Imod_curr(kk, 1).lvalue = curr_int_points_cell
                        Pmod_curr(kk, 1).lvalue = Imod_curr(kk, 1) *elmul* Vmod_curr(kk, 1)
    #                end
                    #                 if kk==1
                    #                     Vcell_comb_int{kk,jj}=interp1(Icell_comb{kk,jj},Vscell(:,1),curr_int_points_cell);
                    #                     Vcell_comb_int{kk+1,jj}=interp1(Icell_comb{kk+1,jj},Vscell(:,1),curr_int_points_cell);
                    #                     Vmod_curr{kk,jj}=Vcell_comb_int{kk,jj}+Vcell_comb_int{kk+1,jj};
                    #                     Imod_curr{kk,jj}=curr_int_points_cell;  
                    #                 elseif kk>1
                    #                     Vmod_curr_int{kk,jj}=interp1(Imod_curr{kk-1,jj},Vmod_curr{kk-1,jj},curr_int_points_cell);
                    #                     Vcell_comb_int{kk+1,jj}=interp1(Icell_comb{kk+1,jj},Vscell(:,1),curr_int_points_cell);
                    #                     Vmod_curr{kk,jj}=Vmod_curr_int{kk,jj}+Vcell_comb_int{kk+1,jj};
                    #                     Imod_curr{kk,jj}=curr_int_points_cell; 
                    #                     Pmod_curr{kk,jj}=Imod_curr{kk,jj}.*Vmod_curr{kk,jj};
                    #                 end
                end
    
                Vmod = Vmod_curr(kk, 1)
                Imod = Imod_curr(kk, 1)
                Pmod = Pmod_curr(kk, 1)
    
                # the following is commented for debugging reasons (the values are assigned
                # later):
    
                # [Pmod_mpp(rorient) Pmodmpp_ind]= max(Pmod);
                # Vmod_mpp(rorient) = Vmod(Pmodmpp_ind);
                # Imod_mpp(rorient) = Imod(Pmodmpp_ind);
                # 
                # Vmod_s{rorient} = Vmod;
                # Imod_s{rorient} = Imod;
                # Pmod_s{rorient} = Vmod.*Imod;
    
                # with bypass diodes 
            elif mod_diodes == 2:
                disp(mstring('bypass diodes not yet implemented for asf analysis with honeybee'))
                #             curr_int_points_cell=linspace(-0.5,5,300000);
                # 
                #             % add voltage from cell to cell
                #             jj=1;
                #             jjstep1=3;
                #             for kk=1:(jjstep1-1)
                #                 if kk==1
                #                     Vcell_comb_int{kk,jj}=interp1(Icell_comb{kk+jjstep1*(jj-1),1},Vscell(:,1),curr_int_points_cell);
                #                     Vcell_comb_int{kk+1,jj}=interp1(Icell_comb{kk+jjstep1*(jj-1)+1,1},Vscell(:,1),curr_int_points_cell);
                #                     Vmod_curr{kk,jj}=Vcell_comb_int{kk,jj}+Vcell_comb_int{kk+1,jj};
                #                     Imod_curr{kk,jj}=curr_int_points_cell;  
                #                 elseif kk>1
                #                     Vmod_curr_int{kk,jj}=interp1(Imod_curr{kk-1,jj},Vmod_curr{kk-1,jj},curr_int_points_cell);
                #                     Vcell_comb_int{kk+1,jj}=interp1(Icell_comb{kk+jjstep1*(jj-1)+1,1},Vscell(:,1),curr_int_points_cell);
                #                     Vmod_curr{kk,jj}=Vmod_curr_int{kk,jj}+Vcell_comb_int{kk+1,jj};
                #                     Imod_curr{kk,jj}=curr_int_points_cell; 
                #                     Pmod_curr{kk,jj}=Imod_curr{kk,jj}.*Vmod_curr{kk,jj};
                #                 end
                #             end
                # 
                #             jjmax=22;
                #             jjstep2=2;
                #             for jj=[2:(jjmax-1)]
                #                 for kk=1:(jjstep2-1)
                #                     if kk==1
                #                         Vcell_comb_int{kk,jj}=interp1(Icell_comb{kk+jjstep2*(jj-2)+jjstep1,1},Vscell(:,1),curr_int_points_cell);
                #                         Vcell_comb_int{kk+1,jj}=interp1(Icell_comb{kk+jjstep2*(jj-2)+jjstep1,1},Vscell(:,1),curr_int_points_cell);
                #                         Vmod_curr{kk,jj}=Vcell_comb_int{kk,jj}+Vcell_comb_int{kk+1,jj};
                #                         Imod_curr{kk,jj}=curr_int_points_cell;  
                #                     elseif kk>1
                #                         Vmod_curr_int{kk,jj}=interp1(Imod_curr{kk-1,jj},Vmod_curr{kk-1,jj},curr_int_points_cell);
                #                         Vcell_comb_int{kk+1,jj}=interp1(Icell_comb{kk+jjstep2*(jj-2)+jjstep1,1},Vscell(:,1),curr_int_points_cell);
                #                         Vmod_curr{kk,jj}=Vmod_curr_int{kk,jj}+Vcell_comb_int{kk+1,jj};
                #                         Imod_curr{kk,jj}=curr_int_points_cell; 
                #                         Pmod_curr{kk,jj}=Imod_curr{kk,jj}.*Vmod_curr{kk,jj};
                #                     end
                #                 end
                #             end
                # 
                #             jj=jjmax;
                #             kk=1;
                #             Vcell_comb_int{kk,jj}=interp1(Icell_comb{kk+jjstep2*(jj-2)+jjstep1,1},Vscell(:,1),curr_int_points_cell);
                #             Vmod_curr{kk,jj}=Vcell_comb_int{kk,jj};
                #             Imod_curr{kk,jj}=curr_int_points_cell;  
                # 
                #             % add bypass diode by sub-module 
                #             for jj=1:jjmax
                #                 if jj==1
                #                     kk=2;
                #                 else
                #                     kk=1;
                #                 end
                #                 sel_range{jj}=Vmod_curr{kk,jj}>-2;
                #                 Vmod_sel{jj}=Vmod_curr{kk,jj}(sel_range{jj});
                #                 Imod_sel{jj}=Imod_curr{kk,jj}(sel_range{jj});
                #                 diode_current=1.*10^-7.*exp(-Vmod_sel{jj}/(1.7.*10^-2));
                #                 Imod_sel_wbd{jj} = Imod_sel{jj} + diode_current;
                #             end
                # 
                #             % add sub-module voltages
                #             curr_int_points_sm=linspace(-0.5,5,300000);
                #             for jj=1:jjmax
                #                 volt_sm_int{jj}=interp1(Imod_sel_wbd{jj},Vmod_sel{jj},curr_int_points_sm);
                #             end
                # 
                #             for jj=1:jjmax
                #                 Vmod_sub(jj,:)=volt_sm_int{jj}; 
                #             end
                # 
                #             Vmod=sum(Vmod_sub);
                #             Imod=curr_int_points_sm; 
                #             Pmod=Vmod.*Imod;
#            end
    
            Vmod_tot(mod_sel, mslice[:]).lvalue = Vmod
            Imod_tot(mod_sel, mslice[:]).lvalue = Imod
            Pmod_tot(mod_sel, mslice[:]).lvalue = Pmod
    
            [Pmod_mpp(rorient, mod_sel), Pmodmpp_ind] = max(Pmod)                                        # [W]
            Vmod_mpp(rorient, mod_sel).lvalue = Vmod(Pmodmpp_ind)
            Imod_mpp(rorient, mod_sel).lvalue = Imod(Pmodmpp_ind)
            Ins_mod(rorient, mod_sel).lvalue = sum(sum(irr_mod_mat_rnd)) * trisurf                                        # insolation per module [Wh]
            Ins_mod_mean(rorient, mod_sel).lvalue = (sum(sum(irr_mod_mat_rnd))) / (length(irr_mod_sel))                                        # insolation per module [Wh/m2]
            Ins_mod_rmsd(rorient, mod_sel).lvalue = (sum(sum((irr_mod_mat_rnd - Ins_mod_mean(rorient, mod_sel)) **elpow** 2)) /eldiv/ (length(irr_mod_sel))) **elpow** (1 / 2)
    
    
            Ins_mod_maxdiff(rorient, mod_sel).lvalue = max(max(irr_mod_mat_rnd) - min(irr_mod_mat_rnd))                                        # max diff insolation  [Wh/m2]
            #         Ins_mod_maxdiff2(rorient, mod_sel) =(max(sum(irr_mod_mat_rnd'./2))-min(sum(irr_mod_mat_rnd'./2))); % max diff insolation btw cells [Wh/m2]
            # 
            #         Vmod_s{rorient, mod_sel} = Vmod;
            #         Imod_s{rorient, mod_sel} = Imod;
            #         Pmod_s{rorient, mod_sel} = Vmod.*Imod;

#        end

    Ins_sum_roof(rorient).lvalue = sum(Ins_mod(rorient, mslice[:]))                                        # sum insolation
    #     Ins_avg_roof(i)=sum(Ins_mod(i,:)./panelsize)/numpanels(i); % W/m2 average
    Ins_avg_roof(rorient).lvalue = sum(Ins_mod_mean(rorient, mslice[:])) / panelnum                                        # W/m2 average
    Pmpp_sum_roof(rorient).lvalue = sum(Pmod_mpp(rorient, mslice[:]))                                        # sum power
    Pmpp_avg_roof(rorient).lvalue = sum(Pmod_mpp(rorient, mslice[:]) /eldiv/ panelsize) / panelnum                                        # W/m2 average
    effap_arr(rorient).lvalue = Pmpp_sum_roof(rorient) / Ins_sum_roof(rorient) *elmul* 100. * apertscale                                        #
    effmod_arr(rorient).lvalue = Pmpp_sum_roof(rorient) / Ins_sum_roof(rorient) *elmul* 100
    ins_rmsd_avg(rorient).lvalue = sum(Ins_mod_rmsd(rorient, mslice[:])) / panelnum

    toc()
#end
    
    
if create_plots_flag:

    #several corrections in the following code for plotting, old code is
    #commented
    figure()
    subplot(2, 2, 1)
    #plot(Ins_mod./panelsize,'-b') % either this or the xlabel is wrong
    plot(Ins_mod.cT /eldiv/ panelsize, mstring('-b'))
    xlim(mcat([0, 50]))
    xlabel(mstring('Module number'), mstring('FontSize'), 12)
    ylabel(mstring('Module insolation (W/m2)'), mstring('FontSize'), 12)

    subplot(2, 2, 2)
    #plot(Pmod_mpp,'-b')  % either this or the xlabel is wrong
    plot(Pmod_mpp.cT /eldiv/ panelsize.cT, mstring('-b'))
    xlim(mcat([0, 50]))
    xlabel(mstring('Module number'), mstring('FontSize'), 12)
    #ylabel('RMSD (W/m2)', 'FontSize',12)
    ylabel(mstring('Module power (W/m2)'), mstring('FontSize'), 12)

    subplot(2, 2, 3)
    #plot(Ins_mod_rmsd,'-b')% either this or the xlabel is wrong
    plot(Ins_mod_rmsd.cT)

    xlabel(mstring('Module number'), mstring('FontSize'), 12)
    ylabel(mstring('RMSD (W/m2)'), mstring('FontSize'), 12)

    subplot(2, 2, 4)
    plot(Pmod_mpp.cT /eldiv/ Ins_mod.cT *elmul* 100. * apertscale, mstring('--b'))
    hold("on")
    plot(Pmod_mpp.cT /eldiv/ Ins_mod.cT *elmul* 100, mstring('-b'))
    xlim(mcat([0, 50]))
    #     legend('Aperture efficiency', 'Module efficiency')
    legend(mstring('Module efficiency'), mstring('Aperture efficiency'))
    xlabel(mstring('Module number'), mstring('FontSize'), 12)
    ylabel(mstring('Efficiency (%)'), mstring('FontSize'), 12)
                        