"""
Make a pie chart - see
http://matplotlib.sf.net/matplotlib.pylab.html#-pie for the docstring.

This example shows a basic pie chart with labels optional features,
like autolabeling the percentage, offsetting a slice with "explode",
adding a shadow, and changing the starting angle.

"""
from pylab import *

plt.style.use('seaborn-white')

# make a square figure and axes
figure(1, figsize=(8,8))
ax = axes([0.1, 0.1, 0.8, 0.8])

import matplotlib as mpl
mpl.rcParams['font.size'] = 15

Data = yearlyData['E_total']

# The slices will be ordered and plotted counter-clockwise.
labels = 'Heating', 'Cooling', 'Actuation', 'Lighting'
fracs = [Data['H'], Data['C'], Data['AE'], Data['L'], ]
explode=(0.1, 0.1, 0.1 , 0.1)

cs=cm.Set1(np.arange(4)/4.)

pie(fracs, explode=explode, labels=labels,
                autopct='%1.1f%%', shadow=True, startangle=90, colors = ["r", "b", "k", "y"])
                # The default startangle is 0, which would start
                # the Frogs slice on the x-axis.  With startangle=90,
                # everything is rotated counter-clockwise by 90 degrees,
                # so the plotting starts on the positive y-axis.

title('Relative Net Energy Demand')

show()

path = r'C:\Users\Assistenz\Desktop\Mauro\ASF_Simulation\Simulation_Tool\New_SimulationEnvironment\PlotMidTerm'
savefig(path + '\\RelativeNetEnergyDemand.png')

