import numpy as np
from math import *

# Flat shading function
def flats(canvas, vertices, vcolors):
    """
    Calculates the color for every pixel of a given image and returns the updated array.

    :param canvas: array, the initial image canvas.
    :param vertices: array, the coordinates of every point of every triangle.
    :param vcolors: array, the color of every point, given in RGB format.

    :return: array, the updated canvas with the new values for the colors.
    """

    # initialize the updated canvas
    updatedcanvas = np.copy(canvas)

    # initialize and sort vertices
    index = np.argsort(vertices[:, 1])
    vertices = vertices[index]
    vcolors = vcolors[index]
    vrt1, vrt2, vrt3 = vertices[0], vertices[1], vertices[2]

    # initialize the color array
    color = np.array([0, 0, 0])

    # in flat shading the color is the mean color
    color = np.mean(vcolors, axis=0)

    # calculate edge slopes, through finding same line points
    slope1 = 0
    slope2 = 0
    slope3 = 0
    if (vrt3[0] - vrt1[0]) == 0:
        slope1 = np.inf
    else:
        slope1 = (vrt3[1] - vrt1[1]) / (vrt3[0] - vrt1[0])
    if (vrt3[0] - vrt2[0]) == 0:
        slope2 = np.inf
    else:
        slope2 = (vrt3[1] - vrt2[1]) / (vrt3[0] - vrt2[0])
    if (vrt2[0] - vrt1[0]) == 0:
        slope3 = np.inf
    else:
        slope3 = (vrt2[1] - vrt1[1]) / (vrt2[0] - vrt1[0])

    # paint function
    def draw_point(x, y):
        # in flat mode the color is the same
        updatedcanvas[x][y] = color

    # paint function for each point of the scanline
    def draw_scanline(x1, x2, y):
        if x1 <= x2:
            xmin = x1
            xmax = x2
        else:
            xmin = x2
            xmax = x1

        for x in range(ceil(xmin), floor(xmax) + 1):
            draw_point(x, y)

    # paint function for triangle with flat top edge
    def paint_top_flat(v1, v2, v3):
        g1 = (v2[0] - v1[0]) / (v2[1] - v1[1])
        g2 = (v3[0] - v1[0]) / (v3[1] - v1[1])

        # set x1 and x2 equal
        x1 = v1[0]
        x2 = v1[0]
        for y in range(int(v1[1]), int(v2[1]) + 1):
            draw_scanline(x1, x2, y)
            x1 += g1
            x2 += g2

    # paint function for triangle with flat bottom edge
    def paint_bottom_flat(v1, v2, v3):
        g1 = (v3[0] - v1[0]) / (v3[1] - v1[1])
        g2 = (v3[0] - v2[0]) / (v3[1] - v2[1])

        # set xmin and xmax equal
        xmin = v3[0]
        xmax = v3[0]
        for y in range(int(v3[1]), int(v1[1]), -1):
            draw_scanline(xmin, xmax, y)
            xmin -= g1
            xmax -= g2

    # case 1: check if the triangle is a point
    if vertices[0][1] == vertices[1][1] == vertices[2][1] or vertices[0][0] == vertices[1][0] == vertices[2][0]:
        pass

    # case 2: check if the triangle is a line
    elif slope1 == slope2 or slope2 == slope3 or slope3 == slope1:
        pass

    # case 3: check if the triangle is a triangle
    else:
        # cases 4 and 5: check if there is a top or bottom flat triangle
        if vrt2[1] == vrt3[1]:
            paint_top_flat(vrt1, vrt2, vrt3)
        elif vrt1[1] == vrt2[1]:
            paint_bottom_flat(vrt1, vrt2, vrt3)

        # case 6
        else:
            # divide triangle into two flat triangles and paint them separately:
            v4 = [vrt1[0] + ((vrt2[1] - vrt1[1]) / (vrt3[1] - vrt1[1])) * (vrt3[0] - vrt1[0]), vrt2[1]]
            paint_top_flat(vrt1, vrt2, v4)
            paint_bottom_flat(vrt2, v4, vrt3)

    return updatedcanvas
