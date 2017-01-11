# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 12:12:30 2016

@author: Assistenz
"""

from pyepw.epw import EPW
import numpy as np


#epwPath = r'C:\Users\Assistenz\Desktop\Mauro\radiation_visualization\ASF_TestEPW\input\Zuerich_Kloten_2005.epw'
#epwPath = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\WeatherData\USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw'


epwPath = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\WeatherData\CHE_Geneva.067000_IWEC.epw'
SaveEPW = r'C:\Users\Assistenz\Desktop\Mauro\radiation_visualization\WeatherData\Test.epw'

epw = EPW()
epw.read(epwPath)
#epw.read(SaveEPW)

#for wd in epw.weatherdata:
#    print wd.year, wd.month, wd.day, wd.hour, wd.minute, wd.dry_bulb_temperature

sunnySom = {}
sunnyWin = {}
cloudySom = {}
cloudyWin = {}

#for wd in epw.weatherdata:
    
#    print wd.dry_bulb_temperature
#    print wd.direct_normal_radiation 

#    wd.dry_bulb_temperature = 20
#    wd.direct_normal_radiation = 30 
#    wd.diffuse_horizontal_radiation = 40 
#    wd.global_horizontal_radiation = 70
    
    #print wd.month, wd.day, wd.hour, wd.dry_bulb_temperature, wd.direct_normal_radiation, wd.diffuse_horizontal_radiation, wd.global_horizontal_radiation
    
count = 0   
for wd in epw.weatherdata:
    count += 1
    
    
    if wd.month == 2 and wd.day == 1:
        sunnyWin[wd.hour] = {'dir' : wd.direct_normal_radiation, 'dif' : wd.diffuse_horizontal_radiation, 'glo' : wd.global_horizontal_radiation, 'total_sky_cover': wd.total_sky_cover, 'opaque' :wd.opaque_sky_cover, 'visibility': wd.visibility}
        
    elif wd.month == 1 and wd.day == 21:
        cloudyWin[wd.hour] = {'dir' : wd.direct_normal_radiation, 'dif' : wd.diffuse_horizontal_radiation, 'glo' : wd.global_horizontal_radiation, 'total_sky_cover': wd.total_sky_cover, 'opaque' :wd.opaque_sky_cover, 'visibility': wd.visibility} 
    
    elif wd.month == 5 and wd.day == 25:
        sunnySom[wd.hour] = {'dir' : wd.direct_normal_radiation, 'dif' : wd.diffuse_horizontal_radiation, 'glo' : wd.global_horizontal_radiation, 'total_sky_cover': wd.total_sky_cover, 'opaque' :wd.opaque_sky_cover, 'visibility': wd.visibility}
    
    elif wd.month == 5 and wd.day == 23:
        cloudySom[wd.hour] = {'dir' : wd.direct_normal_radiation, 'dif' : wd.diffuse_horizontal_radiation, 'glo' : wd.global_horizontal_radiation, 'total_sky_cover': wd.total_sky_cover, 'opaque' :wd.opaque_sky_cover, 'visibility': wd.visibility}
        
#    if count < 1000:
#        wd.dry_bulb_temperature = 0
#        wd.direct_normal_radiation = 0 
#        wd.diffuse_horizontal_radiation = 0 
#        wd.global_horizontal_radiation = 0
#        
#    if count >2000 and count < 3000:
#        
#        wd.albedo= 0
#    if count >3000 and count < 4000:
#        
#        wd.total_sky_cover = 0
#    if count >4000 and count < 5000:
#        wd.opaque_sky_cover = 0
#        
#    if count >5000 and count < 6000:
#        
#        wd.visibility = 0
        
       # print wd.month, wd.day, wd.hour, wd.dry_bulb_temperature, wd.direct_normal_radiation, wd.diffuse_horizontal_radiation, wd.global_horizontal_radiation    
print count


#epw.save(SaveEPW)

#r(self.data_source_and_uncertainty_flags))
#out.append(self._to_str(self.dry_bulb_temperature))
#out.append(self._to_str(self.dew_point_temperature))
#out.append(self._to_str(self.relative_humidity))
#out.append(self._to_str(self.atmospheric_station_pressure))
#out.append(self._to_str(self.extraterrestrial_horizontal_radiation))
#out.append(self._to_str(self.extraterrestrial_direct_normal_radiation))
#out.append(self._to_str(self.horizontal_infrared_radiation_intensity))
#out.append(self._to_str(self.global_horizontal_radiation))
#out.append(self._to_str(self.direct_normal_radiation))
#out.append(self._to_str(self.diffuse_horizontal_radiation))
#out.append(self._to_str(self.global_horizontal_illuminance))
#out.append(self._to_str(self.direct_normal_illuminance))
#out.append(self._to_str(self.diffuse_horizontal_illuminance))
#out.append(self._to_str(self.zenith_luminance))
#out.append(self._to_str(self.wind_direction))
#out.append(self._to_str(self.wind_speed))
#out.append(self._to_str(self.total_sky_cover))
#out.append(self._to_str(self.opaque_sky_cover))
#out.append(self._to_str(self.visibility))
#out.append(self._to_str(self.ceiling_height))
#out.append(self._to_str(self.present_weather_observation))
#out.append(self._to_str(self.present_weather_codes))
#out.append(self._to_str(self.precipitable_water))
#out.append(self._to_str(self.aerosol_optical_depth))
#out.append(self._to_str(self.snow_depth))
#out.append(self._to_str(self.days_since_last_snowfall))
#out.append(self._to_str(self.albedo))
#out.append(self._to_str(self.liquid_precipitation_depth))
#out.append(self._to_str(self.liquid_precipitation_quantity))