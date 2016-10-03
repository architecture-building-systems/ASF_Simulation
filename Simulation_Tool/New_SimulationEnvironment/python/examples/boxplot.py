import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
data = [np.random.normal(0, std, 1000) for std in range(1, 6)]

box = plt.boxplot(data, notch=True, patch_artist=True)

colors = ['cyan', 'lightblue', 'lightgreen', 'tan', 'pink']
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)

plt.show()