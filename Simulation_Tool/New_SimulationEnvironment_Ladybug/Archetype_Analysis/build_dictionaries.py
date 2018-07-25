import pandas as pd
import re as re
import sys

from j_paths import \
    PATHS  # TODO: Convert to setup.py or something equivalent http://docs.python-guide.org/en/latest/writing/structure/

paths = PATHS()

sys.path.insert(0, paths['5R1C_ISO_simulator'])

from supplySystem import *
from emissionSystem import *



# TODO: Rename to BuildArchetypeDict
def BuildArchetypeDict(BuildingData):
    """
    Reads the CEA database excel sheet and extracts necessary information to conduct and archetype evaluation
    :param BuildingData: A dictionary containing the necessary room dimension
    :return: A dataframe with archetype data for ASF evaluation
    """

    #Manually Set Lighting Control
    lighting_control_d = {  
    "MULTI_RES": 250.,
    "OFFICE": 350.,
    "SCHOOL": 350.,
    }

    #Set Mean Occupancy as calculated from occupancy profiles. Maybe redundant
    mean_occupancy_d = { 
    "MULTI_RES": 0.014355,
    "OFFICE": 0.009951,
    "SCHOOL": 0.010913,
    }

    #Recreated the above dictionary into a dataframe manually because im an idiot and short of time
    mean_occupancy_df = pd.DataFrame({"Code": ["MULTI_RES","OFFICE","SCHOOL"], "people_sqm": [0.014355,0.009951,0.010913]})

    volume = (BuildingData['room_width'] / 1000.) * (BuildingData['room_depth'] / 1000.) * (
        BuildingData['room_height'] / 1000.)
    area = (BuildingData['room_width'] / 1000.) * (BuildingData['room_depth'] / 1000.)

    # read thermal properties for RC model
    arch = pd.read_excel(paths['Archetypes_properties'], sheetname='THERMAL')
    r = re.compile("([a-zA-Z_]+)")  # generate regular expression of letters to strip numbers

    # Strip numbers off the building archetypes for matching later on
    arch["code1"] = pd.DataFrame([r.match(string).groups() for string in arch.Code])
    arch.set_index(['code1'], inplace=True)
    print arch

    # Delete uneeded archetypes and
    arch.drop(['SERVERROOM', 'PARKING', 'SWIMMING', 'COOLROOM', "SINGLE_RES", "HOTEL", "RETAIL", "FOODSTORE", "RESTAURANT", "INDUSTRIAL", "HOSPITAL", "GYM"], inplace=True)
    arch.reset_index(drop=False, inplace=True)
    arch.drop('Es', axis=1, inplace=True)  # Ratio of floor area that has electricity not needed
    arch.drop('Hs', axis=1, inplace=True)  # ratio of gross floor area heated or cooled not needed
    arch.drop('U_roof', axis=1, inplace=True)  # roof u value not needed, assume only facade loss
    arch.drop('U_base', axis=1, inplace=True)  # heat transfer through basement not needed

    # read internal loads for RC model from CEA excel sheet and keep necessary loads
    int_loads = pd.read_excel(paths['Archetypes_properties'], sheetname='INTERNAL_LOADS')
    int_loads = int_loads[['Code', 'Qs_Wp', 'Ea_Wm2', 'El_Wm2']]

    # read thermal set points and ventilation rates
    thermal_setpoint_ventelation = pd.read_excel(paths['Archetypes_properties'], sheetname='INDOOR_COMFORT')

    thermal_setpoint_ventelation = thermal_setpoint_ventelation.merge(mean_occupancy_df)

    #Set a ventilation rate in air changes per hour. However this doesn't work with average occupancy
    #TODO: Set a dynamic ventilation strategy in the ASF Simulation Model
    #thermal_setpoint_ventelation['ACH_vent']=thermal_setpoint_ventelation['Ve_lps']*thermal_setpoint_ventelation['people_sqm'] * area * 3.6/volume

    # Combine everything into a single dataframe
    b_props = arch.merge(int_loads, how='left', left_on='code1', right_on='Code')
    b_props = b_props.merge(thermal_setpoint_ventelation, how='left', left_on='code1', right_on='Code')


    b_props = b_props.drop(['Code_y', 'Code'], axis=1)

    # Create set back temperature definition to match with the ASF_Simulation
    b_props['setBackTempC'] = b_props['Tcs_setb_C'] - b_props['Tcs_set_C']
    b_props['setBackTempH'] = b_props['Ths_set_C'] - b_props['Ths_setb_C']



    #Ventilation rate per person
    b_props['ACH_vent'] = b_props['Ve_lps'] * 3.6 / volume

    # Assign values for Cm from ISO13790:2008, Table 12, based on archetypes
    c_m = []
    for i in range(0, len(b_props['th_mass'])):
        # c_m.append(165.0*10**3) just testing default value
        if b_props['th_mass'][i] == "T1":
            c_m.append(110.0 * 10 ** 3)  # Light
        elif b_props['th_mass'][i] == "T2":
            c_m.append(165.0 * 10 ** 3)  # Medium
        elif b_props['th_mass'][i] == "T3":
            c_m.append(260.0 * 10 ** 3)  # Heavy
    b_props['c_m_A_f'] = pd.DataFrame(c_m)

    # declare variables
    occupancy = []
    lighting_control = []
    mean_occupancy = []
    # declare constants
    glass_solar_transmittance = []
    glass_light_transmittance = []
    Lighting_Utilisation_Factor = []
    Lighting_Maintenance_Factor = []
    ACH_vent = []
    ACH_infl = []
    ventilation_efficiency = []
    phi_c_max_A_f = []
    phi_h_max_A_f = []
    heatingSupplySystem = []
    coolingSupplySystem = []
    heatingEmissionSystem = []
    coolingEmissionSystem = []
    heatingEfficiency = []
    coolingEfficiency = []
    ActuationEnergy = []
    COP_H = []
    COP_C = []

    print b_props['code1']
    #TODO: Change a lot of thees with df.assign(column_name=constant)
    for code in b_props['code1']:
        # variables
        occupancy.append('schedules_occ_%s.csv' % code)
        lighting_control.append(lighting_control_d.get(code))
        mean_occupancy.append(mean_occupancy_d.get(code))
        glass_solar_transmittance.append(0.6)
        glass_light_transmittance.append(0.6)
        Lighting_Utilisation_Factor.append(0.45)
        Lighting_Maintenance_Factor.append(0.9)
        ACH_vent.append(2.0)  # TODO: Shoudlnt this be a variable
        ACH_infl.append(0.5)
        ventilation_efficiency.append(0.6)
        phi_c_max_A_f.append(-np.inf)
        phi_h_max_A_f.append(np.inf)
        heatingSupplySystem.append(COP42Heater)  # DirectHeater, #ResistiveHeater #HeatPumpHeater
        coolingSupplySystem.append(COP81Cooler)  # DirectCooler, #HeatPumpCooler
        heatingEmissionSystem.append(FloorHeating)
        coolingEmissionSystem.append(FloorHeating)
        heatingEfficiency.append(1.0)
        coolingEfficiency.append(1.0)
        ActuationEnergy.append(False)
        COP_H.append(1.0)
        COP_C.append(1.0)


    b_props['Qs_Wm2'] = mean_occupancy * b_props['Qs_Wp']  # occupancy: p/m2, qs_wp: W/p
    b_props['Occupancy'] = occupancy
    b_props['ActuationEnergy'] = ActuationEnergy


    #Build Building Properties dataframe with building inputs with the same variable definition as the ASF simulation engine
    BuildingPropertiesDF = pd.DataFrame({'Code': []})
    BuildingPropertiesDF['Code'] = b_props.loc[:, 'Code_x']
    BuildingPropertiesDF.loc[:, 'lighting_load'] = b_props.loc[:, 'El_Wm2']
    BuildingPropertiesDF.loc[:, 'lighting_control'] = lighting_control
    BuildingPropertiesDF.loc[:, 'U_em'] = b_props.loc[:, 'U_wall']
    BuildingPropertiesDF.loc[:, 'U_w', ] = b_props.loc[:, 'U_win']
    BuildingPropertiesDF.loc[:, 'theta_int_h_set'] =b_props.loc[:,'Ths_set_C'].apply(pd.to_numeric)
    BuildingPropertiesDF.loc[:, 'theta_int_c_set'] = b_props.loc[:, 'Tcs_set_C'].apply(pd.to_numeric)
    BuildingPropertiesDF.loc[:, 'c_m_A_f'] = b_props.loc[:, 'c_m_A_f']
    BuildingPropertiesDF.loc[:, 'Qs_Wp'] = b_props.loc[:, 'Qs_Wp']
    BuildingPropertiesDF.loc[:, 'Ea_Wm2'] = b_props.loc[:, 'Ea_Wm2']
    BuildingPropertiesDF.loc[:, 'glass_solar_transmittance'] = glass_solar_transmittance
    BuildingPropertiesDF.loc[:, 'glass_light_transmittance'] = glass_light_transmittance
    BuildingPropertiesDF.loc[:, 'Lighting_Utilisation_Factor'] = Lighting_Utilisation_Factor
    BuildingPropertiesDF.loc[:, 'Lighting_Maintenance_Factor'] = Lighting_Maintenance_Factor
    BuildingPropertiesDF.loc[:, 'ACH_vent'] = ACH_vent
    BuildingPropertiesDF.loc[:, 'ACH_infl'] = ACH_infl
    BuildingPropertiesDF.loc[:, 'ventilation_efficiency'] = ventilation_efficiency
    BuildingPropertiesDF.loc[:, 'phi_c_max_A_f'] = phi_c_max_A_f
    BuildingPropertiesDF.loc[:, 'phi_h_max_A_f'] = phi_h_max_A_f
    BuildingPropertiesDF.loc[:, 'heatingSupplySystem'] = heatingSupplySystem
    BuildingPropertiesDF.loc[:, 'coolingSupplySystem'] = coolingSupplySystem
    BuildingPropertiesDF.loc[:, 'heatingEmissionSystem'] = heatingEmissionSystem
    BuildingPropertiesDF.loc[:, 'coolingEmissionSystem'] = coolingEmissionSystem
    # BuildingPropertiesDF.loc[:, 'heatingEfficiency'] = heatingEfficiency
    # BuildingPropertiesDF.loc[:, 'coolingEfficiency'] = coolingEfficiency
    # BuildingPropertiesDF.loc[:, 'COP_H'] = COP_H
    # BuildingPropertiesDF.loc[:, 'COP_C'] = COP_C
    BuildingPropertiesDF.set_index(['Code'], inplace=True)

    #Build Simulation Options dataframe with the same variable definitions as the ASF Simulation tool
    SimulationOptionsDF = b_props[['Code_x', 'setBackTempC', 'setBackTempH', 'Occupancy', 'ActuationEnergy']]
    SimulationOptionsDF= SimulationOptionsDF.assign(human_heat_emission = 0.12)
    SimulationOptionsDF= SimulationOptionsDF.assign(Temp_start = 20.0)
    SimulationOptionsDF.set_index(['Code_x'], inplace=True)

    # Temp: only analyse the first two lines for testing purposes. Delete the next two lines:
    SimulationOptionsDF = SimulationOptionsDF[12:18]
    BuildingPropertiesDF=BuildingPropertiesDF[12:18]
    # Temp complete

    print BuildingPropertiesDF
    print SimulationOptionsDF

    #Convert dataframes to dictionaries
    SimulationOptions = SimulationOptionsDF.to_dict(orient='index')
    BuildingProperties = BuildingPropertiesDF.to_dict(orient='index')
    BuildingPropertiesDF.to_csv('Builtdictionaries2.csv')
    SimulationOptionsDF.to_csv('SOdictionaries.csv')

    return BuildingProperties, SimulationOptions


if __name__ == '__main__':
    BuildingData = {
        "room_width": 3000,
        "room_height": 2100,
        "room_depth": 4000,
        "glazing_percentage_w": 0.92,
        "glazing_percentage_h": 0.97}

    b_data = BuildArchetypeDict(BuildingData)
    print b_data
