"""
===========================
SunPosition CSV file reader
===========================

"""
import pandas as pd
import numpy as np



__author__ = "Clayton Miller"
__copyright__ = "Copyright 2014, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Clayton Miller", "Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "thomas@arch.ethz.ch"
__status__ = "Production"



def SunPosition_reader(SunPosition_path):

    sun_labels = ['altitude', 'azimuth'] #'HOY', 
#
#    result = pd.read_csv(SunPosition_path, skiprows=1, header=None, names=epw_labels).drop('datasource', axis=1)
#    result['dayofyear'] = pd.date_range('1/1/2010', periods=8760, freq='H').dayofyear
#    result['ratio_diffhout'] = result['difhorrad_Whm2']/result['glohorrad_Whm2']

    result = pd.read_csv(SunPosition_path, skiprows=1, names=sun_labels)

    
    return result

#def test_reader():
#    
#    locator = cea.inputlocator.InputLocator(r'C:\reference-case\baseline')
#    # for the interface, the user should pick a file out of of those in ...DB/Weather/...
#    weather_path = locator.get_default_weather()
#    epw_reader(weather_path=weather_path)
#    
#if __name__ == '__main__':
#    #test_reader()
#    epw_reader(weather_path=weather_path)
    
