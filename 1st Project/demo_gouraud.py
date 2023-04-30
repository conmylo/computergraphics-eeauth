# The following is a script to demonstrate the use of the implemented functions
# This script is using the gouraud shading technique

from render import render
import numpy as np
import matplotlib.pyplot as plt

# load the data from the given array
data = np.load("h1.npy", allow_pickle=True)
vertices = data[()]['verts2d']
vcolors = data[()]['vcolors']
faces = data[()]['faces']
depth = data[()]['depth']

# rearrange the vertices array
temp = np.copy(vertices[:, 0])
vertices[:, 0] = vertices[:, 1]
vertices[:, 1] = temp

# call render function with gouraud shading technique
y = render(vertices, faces, vcolors, depth, 'gouraud')

# display image
imgplot = plt.imshow(y)
plt.show()
