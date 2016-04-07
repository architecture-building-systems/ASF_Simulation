# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 12:07:31 2016

Calculate IV-curves Lookup-Table for ASF electricity production

@authors: Johannes Hofer, Jeremias Schmidli
"""
import numpy as np
import time


def diode_equation(y,Iphi,Io,a,CC,x,AA,BB2):
    return y - Iphi + Io * (np.e**(a/CC*(x + y * AA))-1) + (x + y * AA)/BB2
    

def diode_equation_eval(fitparams=None, x=None, modparams=None, ins=None, temp=None):
    from scipy import optimize

    # general diode equation
    # I = Iphi - Io * (exp(a/gamma*(V + I * Rs))-1) - (V + I * Rs)/Rp
    # Iphi = (phi/phi_ref) * (Iphi_ref + muIsc*(Tc - Tc_ref));
    # Iphi_ref = Isc + Io_ref*(exp(Isc*Rs*a/gamma)-1) + Isc*Rs/Rp_ref
    # Io = Io_ref*(Tc/Tc_ref)^3*exp(b/gamma*(1/Tc_ref-1/Tc));

    # parameters: Rs = AA, rp_ref = BB, gamma = CC
    # I = Iphi - Io * (exp(a/gamma*(V + I * Rs))-1) - (V + I * Rs)/Rp
    # -> 0 = y - Iphi + Io * (exp(a/CC*(x(i) + y * AA))-1) + (x(i) + y * AA)/BB2

    # insolation and temperature
    phi_ref = float(ins[0])
    phi = float(ins[1])
    Tc = float(temp)
    Tc_ref = modparams[2]

    # constants
    k = 1.3806503e-23# boltzmann constant [J/K] ( =8.617e-05 eV/K)
    q = 1.60217646e-19# electron charge [C] ( =1e)

    # module parameters
    Isc = modparams[0]
    Ncs = float(modparams[1])
    muIsc = modparams[3]
    egap = modparams[4]
    a = q / (Ncs * k * Tc)
    b = q * egap / k

    # fit parameters
    AA = fitparams[0]# Rs
    BB = float(fitparams[1])# Rp_ref
    CC = fitparams[2]# gamma
    DD = fitparams[3]# Io_ref

    # shunt resistance scaling
    # Rp_0 = 10*BB;
    Rp_0 = 4 * BB
    Rp = BB + (Rp_0 - BB) * np.e**(-5.5 * (phi / phi_ref))
    BB2 = Rp

    # photocurrent and diode saturation current
    Iphi_ref = Isc + DD * (np.exp(Isc * AA * a / CC) - 1) + Isc * AA / BB
    Iphi = (phi / phi_ref) * (Iphi_ref + muIsc * (Tc - Tc_ref))
    Io = DD * (Tc / Tc_ref) ** 3 * np.exp(b / CC * (1 / Tc_ref - 1 / Tc))

    y =  [0]*len(x)#zeros(size(x))
    NN = len(x)
#    opt = optimset(mstring('display'), mstring('off'))

    for j in range(NN):
        args = (Iphi,Io,a,CC,x[j],AA,BB2)
        y[j] = optimize.fsolve(diode_equation, 1, args )[0]
    
    return y


# tryout different parameters
modparams = ([2.68, 42, 25 + 273.15, 1.3e-03, 1.05])# [Isc,Ncs,Tc_ref,muIsc,egap] modparams = [2.68, 42, 25+273.15, 1.3e-03, 1.05*1.6*10^-19];
fitparam = ([0.8, 380, 1.435, 7.66e-7])# [Rs, Rp_ref, gamma, IoRef]

ncell = 48
vmin = -6 * ncell
vmax = 0.8 * ncell#30
volt_model_var = np.linspace(vmin, vmax, 1000)
curr_model_submod_lookup = np.empty((301, 20, 1000))

print 'calculating lookup-table for electricity production:'
tic = time.time()
for i in range(301):#i=1:301
    
    for t in range(20):#20
        #     for t=9:9
        ins_ref = 1 + (i) * 5
        mod_ref = -20 + (t) * 5
        temp = mod_ref + 273.15
        
        ins_submod = ([1000, ins_ref])
        curr_model_submod_lookup[i, t,:] = diode_equation_eval(fitparam, volt_model_var, modparams, ins_submod, temp)
        curr_model_test = curr_model_submod_lookup[i, t,:]
    toc = time.time() - tic
    print 'time passed: ' + str(toc/60.0) + ' min'
    print 'percentage done: ' + str(i/301.*100) + '%'
    
np.save(data_path + '\python\electrical_simulation\curr_model_submod_lookup',curr_model_submod_lookup)

print 'lookup table succesfuly created and saved'

del modparams, fitparam, ncell, vmin, vmax, volt_model_var, curr_model_submod_lookup, i, t, tic, toc, ins_ref, mod_ref, curr_model_test, ins_submod, temp 
