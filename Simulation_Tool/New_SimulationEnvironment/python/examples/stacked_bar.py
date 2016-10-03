import numpy as np
import matplotlib.pyplot as plt

N = 5
H = (130, 90, 70, 64, 55)
C = (120, 85, 62, 50, 53)
L = (100, 70, 60, 45, 50)
PV = (-130, -80, -70, -60, -45)

ind = np.arange(N) + .15 # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, H, width, color='r', alpha = 0.3, label = 'H') 
rects2 = ax.bar(ind, C, width, color='b', alpha = 0.3, label = 'C') 
rects3 = ax.bar(ind, L, width, color='g', alpha = 0.3, label = 'L')
rects4 = ax.bar(ind, PV, width, color='cyan', alpha = 0.3, label = 'PV') 

TotE = (140, 90, 78, 65, 50)


xtra_space = 0.05
rects2 = ax.bar(ind + width + xtra_space , TotE, width, color='black', alpha = 0.3, label = 'TotE') 



# add some text for labels, title and axes ticks
ax.set_ylabel('Energy [kWh]')
ax.set_title('Energy Dependency on Building Orientation')

ax.set_xticks(ind+width+xtra_space)
ax.set_xticklabels( ('W', 'SW', 'S', 'SE', 'E') )

plt.legend()

plt.show()