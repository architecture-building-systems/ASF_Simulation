
"""
===========================
Query schedules according to database
===========================
J. Fonseca  script development          26.08.2015
D. Thomas   documentation               10.08.2016
"""

from __future__ import division
from j_paths import PATHS
import pandas as pd
import numpy as np

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2015, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "thomas@arch.ethz.ch"
__status__ = "Production"

"""
=========================================
Occupancy
=========================================
"""
paths = PATHS()

def schedule_maker(dates, list_uses):
    def get_yearly_vectors(dates, occ_schedules, el_schedules, dhw_schedules, pro_schedules, month_schedule):
        occ = []
        el = []
        dhw = []
        pro = []

        if dhw_schedules[0].sum() != 0:
            dhw_weekday_sum = dhw_schedules[0].sum() ** -1
        else: dhw_weekday_sum = 0

        if dhw_schedules[1].sum() != 0:
            dhw_sat_sum = dhw_schedules[1].sum() ** -1
        else: dhw_sat_sum = 0

        if dhw_schedules[2].sum() != 0:
            dhw_sun_sum = dhw_schedules[2].sum() ** -1
        else: dhw_sun_sum = 0

        for date in dates:
            month_year = month_schedule[date.month - 1]
            hour_day = date.hour
            dayofweek = date.dayofweek
            if 0 <= dayofweek < 5:  # weekday
                occ.append(occ_schedules[0][hour_day] * month_year)
                el.append(el_schedules[0][hour_day] * month_year)
                dhw.append(dhw_schedules[0][hour_day] * month_year * dhw_weekday_sum) # normalized dhw demand flow rates
                pro.append(pro_schedules[0][hour_day] * month_year)
            elif dayofweek is 5:  # saturday
                occ.append(occ_schedules[1][hour_day] * month_year)
                el.append(el_schedules[1][hour_day] * month_year)
                dhw.append(dhw_schedules[1][hour_day] * month_year * dhw_sat_sum) # normalized dhw demand flow rates
                pro.append(pro_schedules[1][hour_day] * month_year)
            else:  # sunday
                occ.append(occ_schedules[2][hour_day] * month_year)
                el.append(el_schedules[2][hour_day] * month_year)
                dhw.append(dhw_schedules[2][hour_day] * month_year * dhw_sun_sum) # normalized dhw demand flow rates
                pro.append(pro_schedules[2][hour_day] * month_year)

        return occ, el, dhw, pro

    schedules = []
    for use in list_uses:
        # Read from archetypes_schedules
        x = pd.read_excel(paths['Archetypes_schedules'], use).T

        # read lists of every daily profile
        occ_schedules, el_schedules, dhw_schedules, pro_schedules, month_schedule = read_schedules(use, x)

        schedule = get_yearly_vectors(dates, occ_schedules, el_schedules, dhw_schedules, pro_schedules, month_schedule)
        schedules.append(schedule)

    return schedules


def read_schedules(use, x):
    occ = [x['Weekday_1'].values, x['Saturday_1'].values, x['Sunday_1'].values]
    el = [x['Weekday_2'].values, x['Saturday_2'].values, x['Sunday_2'].values]
    dhw = [x['Weekday_3'].values, x['Saturday_3'].values, x['Sunday_3'].values]
    month = x['month'].values

    if use is "INDUSTRIAL":
        pro = [x['Weekday_4'].values, x['Saturday_4'].values, x['Sunday_4'].values]
    else:
        pro = [np.zeros(24), np.zeros(24), np.zeros(24)]

    return [occ,el,dhw,pro,month]
