# RC_BuildingSimulator

Simulates the energy balance of a single zone room based on an RC model. This project is still under development

## RC Model used
![RC Model](./Images/1c_rc_circuit.png)

`T_out`: External temperature in C extracted from an EPW weather file

`T_in`: Calculated internal temperature

`R_env`: Resistance of the envelope. Must be caluclated by hand and inputted into the `Building` class in `BuildingProperties.py`

`R_infl`: Equivalent resistance due to infiltration. This is calculated within `BuildingProperties.py`

`R_vent`: Equivalent resistance due to ventelation. A variable resistance calculated by the `setVentelation` method in within the `Building` class of `BuildingProperties.py`

`Cm`: Capacitance of the room. Must be caluclated by hand and inputted into the `Building` class in `BuildingProperties.py`

`Q_Heat`: Heat energy supplied or removed by the heater or cooler. This is determined through a controller based on the temperature set points

`Q_rad`: Heat energy to the sun. Hourly radiation data through the windows must be determined in advance and read through the `read_transmittedR` funtion of `input_data.py`

`Q_gains`: Internal heat gains of people. Determined through the occupancy profile which is read in through the `read_occupancy` function of `input_data.py`


##How it Works

###Running your Simulation `Main.py`

This is the main file which you will modify and run. 

####Step 1: Import the data. 
The first lines should run the various methods form `import_data.py` and read in the necessary data. Read the instructions about this file below for more information 

####Step 2: Set the Room Building Parameters
Simply typing `Office=Building()` will initialise your building with default parameters. If you want to specialise your building then you can set them in the arguments. Default arguments are:

```python
Building(Fenst_A=13.5 , Room_Depth=7 , Room_Width=4.9 ,Room_Height=3.1 ,glass_solar_transmitance=0.687 ,
glass_light_transmitance=0.744 ,LightLoad=0.0117 , LightingControl = 300,Cm=2.07, R_env=42, 
Infl=0.5, vent_Pp=0.016)
```

`Infl`: [ACH/hr] Air changes per hour, Infiltration

`vent_Pp`: [m3/s/person]Is the ventilation rate per person

`Lighting Control` [Lux]: Lighting control set point. Lights will turn on if the illuminance drops below this value

`Lighting Load` [kW/m2]: Energy consumption of the lighting

All dimenions are in [m] meters. All other variables are described in the RC section above.

####Step 3: Calculate the room illuminance
This is calculated based off the formula determined in `Equate_Ill` funciton of `input_data.py`. Note that this is rough and maybe causing the light loads to be lower than what EnergyPlus is calculating **To_Do**

####Step 4: Hack some set points
The Occupancy data file which is read in has some issues with the set point. We therefore manually set some fixed set points here. Fix this. Low priority **TO_DO**

####Step 5: Calculate Heat Gains
* Solar Gains: We have external radiation on the window. Simply multiply this by the transmittance rate. **Note**: The radiation values imported from the file are for a specific building case. If you want to simulate your own building then you will have to generate your own radiation file. We generated our file using LadyBug. **To_Do**: Find a way of calculating the radiation transfer through the building
* Human Heast Gains: Based off the occupancy profile. Calculated in `input_data.py`

Note that the heat gains value `Q` is an array of size 8760. 

**To_Do**: Add heat gains from lighting and equipment

####Step 6: Set initial conditions. Most important is the starting internal temperature `T_in`
`T_in` = 20C (Default)

####Step 7: Tune PI controller for heating and cooling
Default settings are 
```P=1, I=0.08, D=0``` for heating
```P=2, I=1.0, D=0``` for cooling
The PID was copied from [here](http://code.activestate.com/recipes/577231-discrete-pid-controller/)

Note that the PID controller still needs some work as a lot of unecessary energy may be lost **To_Do**

####Step 8: Differentiate! The heart of the program

```python
dT_in=((Q.iat[ii,0]+Q_heat+Q_cool)/(Office.Cm) + (1/(Office.Cm*Office.R_i))*(float(T_out[ii])-T_in))*dt
````

This equation was derived from the single capacitance model shown above. I will need to write another document on how to dervie it, let me know if you are interested in this!

####Step 9: Control the Heating, Cooling and Lighting
If the `T_in` internal temperature is not within the setpoints then the cooling or heating system is activated for that specific timestep. The amount of heating/cooling that is provided demends on the PI control output. **Note:** There is no maximum heating or cooling capacity set. We assume a system that is capable of providing infite amount of power. **To_Do:** Set some limitations on the Q_heat and Q_cool

The lighting control is a simple on off situation depending on the lighting levels and the occupants in the room. **Note:** This value is about 1/2 the energyplus output. This could be due to the control system, or the basic illuminance calculation


### Reading External Data Files `input_data.py`
`input_data.py` contains the methods required to read epw weather files, radiation files and occupancy profiles

`read_EWP`: Reads the EPW file and outputs the average external temperature `T_out`, Global Irradiance, and Global Illuminance 

`read_transmittedMonthlyR`: Reads a radiation file outputted from Jeremias' ladybug script. The radiation file contains hourly radiation data for a day for each month. The data therefore needs to be converted into hourly data for the whole year

`read_transmittedR`: Reads radiation value outputted from a standard ladybug script. The radiation file should contain hourly radiation data for the whole year

`read_occupancy`: Reads the occupancy file used by the [CEA](https://github.com/architecture-building-systems/CEAforArcGIS/tree/master/cea/db/Schedules) tool.

`Equate_Ill`: measures the global irradiation and global illuminance of the weather file to obtain a formula of the type
$$Ill=Rad*x + y$$

This formula will then be used to determine the illuminance of room based off the radiaion supplied. NOTE: This is a bit of a hack. Try find a more elegant way of calculating the solar illumination of the room. **TO_DO**


### Setting your Building Parameters `BuildingProperties.py`
This script contains a `Building` class which sets your building parameters. Default values are already provided. Do not modify any of the parameters here. You will create an instance of this class in the `Main.py` file

`setVentilation`: A method which outputs the resistance between the inside and outside air temperatures. This is the combination of `R_env`, `R_vent` and `R_infl` as described in the RC Model Above



##References

Madsen, Henrik, and Jan Holst. "Estimation of continuous-time models for the heat dynamics of a building." Energy and Buildings 22.1 (1995): 67-79.

Bacher, Peder, and Henrik Madsen. "Identifying suitable models for the heat dynamics of buildings." Energy and Buildings 43.7 (2011): 1511-1522.

Sonderegger, Robert. "Diagnostic tests determining the thermal response of a house." Lawrence Berkeley National Laboratory (2010).
