import numpy as np
from math import *

# Gouraud shading function
def gourauds(canvas, vertices, vcolors):
    """
    Calculates the color for every pixel of a given image and returns the updated array.

    :param canvas: array, the initial image canvas.
    :param vertices: array, the coordinates of every point of every triangle.
    :param vcolors: array, the color of every point, given in RGB format.

    :return: array, the updated canvas with the new values for the colors.
    """

    # initialize the updated canvas
    updatedcanvas = np.copy(canvas)

    # initialize vertices with ascending order according to y
    index = np.argsort(vertices[:, 1])
    vertices = vertices[index]
    vcolors = vcolors[index]
    vrt1, vrt2, vrt3 = vertices[0], vertices[1], vertices[2]

    # getting  the slopes of the sides
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
        # check if point is on edges of triangle or on random vertices
        if y == vrt1[1] == vrt2[1]:
            updatedcanvas[x][y] = interpolate_color(vrt1, vrt2, [x, y], vcolors[0], vcolors[1])
        elif y == vrt1[1]:
            updatedcanvas[x][y] = vcolors[0]
        elif y == vrt3[1] == vrt2[1]:
            updatedcanvas[x][y] = interpolate_color(vrt2, vrt3, [x, y], vcolors[1], vcolors[2])
        elif y == vrt3[1]:
            updatedcanvas[x][y] = vcolors[2]

        # check if point is between edge and vertex
        elif y == vrt2[1]:
            p = [vrt1[0] + (1 / slope1)*(y - vrt1[1]), y]
            c = interpolate_color(vrt1, vrt3, p, vcolors[0], vcolors[2])
            updatedcanvas[x][y] = interpolate_color(p, vrt2, [x, y], c, vcolors[1])

        # twice linear interpolation as described in the algorithm
        elif y < vrt2[1]:
            p1 = [vrt1[0] + (1 / slope1)*(y - vrt1[1]), y]
            color1 = interpolate_color(vrt1, vrt3, p1, vcolors[0], vcolors[2])
            p2 = [vrt1[0] + (1 / slope3)*(y - vrt1[1]), y]
            color2 = interpolate_color(vrt1, vrt2, p2, vcolors[0], vcolors[1])
            updatedcanvas[x][y] = interpolate_color(p1, p2, [x, y], color1, color2)
        elif y > vrt2[1]:
            p1 = [vrt1[0] + (1 / slope1)*(y - vrt1[1]), y]
            color1 = interpolate_color(vrt1, vrt3, p1, vcolors[0], vcolors[2])
            p2 = [vrt2[0] + (1 / slope2)*(y - vrt2[1]), y]
            color2 = interpolate_color(vrt2, vrt3, p2, vcolors[1], vcolors[2])
            updatedcanvas[x][y] = interpolate_color(p1, p2, [x, y], color1, color2)

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

    # interpolation function
    def interpolate_color(x1, x2, x, color1, color2):
        value0 = ((x1[0] - x2[0]) ** 2 + (x1[1] - x2[1]) ** 2) ** 0.5
        value1 = ((x1[0] - x[0]) ** 2 + (x1[1] - x[1]) ** 2) ** 0.5

        colorFinal = np.subtract(color2, color1)

        # linear interpolation between color1 and color2
        value = np.add(color1, np.multiply(colorFinal, value1 / value0))

        return value

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

