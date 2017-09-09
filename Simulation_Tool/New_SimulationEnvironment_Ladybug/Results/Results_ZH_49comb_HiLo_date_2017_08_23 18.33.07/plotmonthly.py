import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd


def carpetPlot(X, z_min, z_max, title, roomFloorArea):
       
    z= np.reshape(X,(12,24)).T
    z = z/roomFloorArea
    

    dx, dy = 1, 1
    
    # generate 2 2d grids for the x & y bounds:
    y, x = np.mgrid[slice(0, 24 + dy, dy),
                    slice(0, 12 + dx, dx)]
    
    
    # define the location of the middle number (where 0 is):
    z_middle = float(abs(z_min)) / (z_max-z_min) 
                
    cmap = LinearSegmentedColormap.from_list('mycmap', [(0, 'navy'), (z_middle, 'white'), (1, 'firebrick')])
                

    if z_min ==0:
        cmap = LinearSegmentedColormap.from_list('mycmap', [(0, 'white'),(1, 'firebrick')])
    else:
        pass
    
    # define what happens to bad data (i.e. data outside the mask):
    cmap.set_bad('grey',1.)
    
    # create the carpet plot:
    plt.pcolormesh(x, y, z, cmap=cmap, vmin=z_min, vmax=z_max)
    
    # set the limits of the plot to the limits of the data
    plt.axis([x.min(), x.max(), 3, 22])
    plt.tick_params(axis=u'both',labelsize=14)
    plt.title(title, fontsize = 18)



results = np.load("monthlyData.npy")

results_static = np.load("monthlyDataStatic.npy")

actuation = np.reshape(results[0][0],(12,24))
cooling = np.reshape(results[1][0],(12,24))
e_tot = np.reshape(results[2][0],(12,24))
e_hcl= np.reshape(results[3][0],(12,24))
heating = np.reshape(results[4][0],(12,24))
lighting = np.reshape(results[5][0],(12,24))
pv = np.reshape(results[6][0],(12,24))

cooling_static = np.reshape(results_static[1][0],(12,24))
e_tot_static = np.reshape(results_static[2][0],(12,24))
e_hcl_static= np.reshape(results_static[3][0],(12,24))
heating_static = np.reshape(results_static[4][0],(12,24))
lighting_static = np.reshape(results_static[5][0],(12,24))
pv_static = np.reshape(results_static[6][0],(12,24))



e_hcl_diff = e_hcl - e_hcl_static

for ii,row in enumerate(pv):
	for jj,value in enumerate(row):
		if pv[ii][jj] > -0.001:
			e_hcl_diff[ii][jj] = 0.0

#carpetPlot(X=e_hcl_diff, z_min = -20, z_max= 20, title = '(a) difference', roomFloorArea = 1)
#plt.show()

annual_hcl_savings =  np.sum(-e_hcl_diff, axis = 1)
annual_cooling_static =  np.sum(cooling_static, axis = 1)
annual_heating_static =  np.sum(heating_static, axis = 1)
annual_lighting_static = np.sum(lighting_static, axis = 1)
annual_pv_static = np.sum(-pv_static, axis=1)

annual_cooling =  np.sum(cooling, axis = 1)
annual_heating =  np.sum(heating, axis = 1)
annual_lighting = np.sum(lighting, axis = 1)

annual_pv = np.sum(-pv, axis=1)

annual_actuation = np.sum(-actuation, axis=1)


FinalResults = pd.DataFrame({'heating':annual_heating,'cooling':annual_cooling, 'lighting':annual_lighting ,'heating_static':annual_heating_static,'cooling_static':annual_cooling_static, 'lighting_static':annual_lighting_static , 'pv':annual_pv , 'pv_static': annual_pv_static,'hvac_saving':annual_hcl_savings, 'actuation_energy': annual_actuation})

FinalResults.to_csv('Energy_Results.csv')
