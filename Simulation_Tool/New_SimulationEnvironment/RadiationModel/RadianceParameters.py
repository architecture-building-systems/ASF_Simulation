# -*- coding: utf-8 -*-
"""
Created on Mon Jan 09 10:54:21 2017

@author: Assistenz
"""

def Library(RadianceValues = 'Default'):
    
    if RadianceValues == 'Default':
        #params
        print "rad: Default" 
        rad_params = {
            'rad_n': 2,
            'rad_af': 'file',
            'rad_ab': 4,#4
            'rad_ad': 512,
            'rad_as': 256,
            'rad_ar': 128,
            'rad_aa': 0.15,
            'rad_lr': 8,
            'rad_st': 0.15,
            'rad_sj': 0.7,
            'rad_lw': 0.002,
            'rad_dj': 0.7,
            'rad_ds': 0.15,
            'rad_dr': 3,
            'rad_dp': 512,
            }
    elif RadianceValues == 'AB1':
        print "rad_ab = 1"
        #params
        rad_params = {    
            'rad_n': 2,
            'rad_af': 'file',
            'rad_ab': 1,
            'rad_ad': 512,
            'rad_as': 256,
            'rad_ar': 128,
            'rad_aa': 0.15,
            'rad_lr': 8,
            'rad_st': 0.15,
            'rad_sj': 0.7,
            'rad_lw': 0.002,
            'rad_dj': 0.7,
            'rad_ds': 0.15,
            'rad_dr': 3,
            'rad_dp': 512,
                }
    elif RadianceValues == 'MinRad':
        print "Minimum Radiance Values"
        #params
        rad_params = {    
            'rad_n': 2,
            'rad_af': 'file',
            'rad_ab': 0,
            'rad_ad': 0,
            'rad_as': 0,
            'rad_ar': 8,
            'rad_aa': 0.5,
            'rad_lr': 0,
            'rad_st': 1,
            'rad_sj': 1,
            'rad_lw': 0.05,
            'rad_dj': 0,
            'rad_ds': 0,
            'rad_dr': 0,
            'rad_dp': 32,
                }
    elif RadianceValues == 'MaxRad':
        print "Maximum Radiance Values"
        #params
        rad_params = {    
            'rad_n': 2,
            'rad_af': 'file',
            'rad_ab': 6,
            'rad_ad': 4096,
            'rad_as': 1024,
            'rad_ar': 0,
            'rad_aa': 0,
            'rad_lr': 16,
            'rad_st': 0,
            'rad_sj': 1,
            'rad_lw': 0,
            'rad_dj': 1,
            'rad_ds': 0.02,
            'rad_dr': 6,
            'rad_dp': 0,
                }
    elif RadianceValues == 'AB8':
        print "rad_ab = 8"
        #params
        rad_params = {    
            'rad_n': 2,
            'rad_af': 'file',
            'rad_ab': 8,
            'rad_ad': 512,
            'rad_as': 256,
            'rad_ar': 128,
            'rad_aa': 0.15,
            'rad_lr': 8,
            'rad_st': 0.15,
            'rad_sj': 0.7,
            'rad_lw': 0.002,
            'rad_dj': 0.7,
            'rad_ds': 0.15,
            'rad_dr': 3,
            'rad_dp': 512,
                }
    else:
        "Couldn't find the needed Radiance Paramters!"
        rad_params = None
        
    return rad_params