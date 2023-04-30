from flats import flats
from gourauds import gourauds
import numpy as np

# Render function
def render(verts2d, faces, vcolors, depth, shade_t):
    """
    Renders the image, colored according to the shading algorithm.

    :param verts2d: array, description in assignment PDF.
    :param faces: array, description in assignment PDF.
    :param vcolors: array, description in assignment PDF.
    :param depth: array, description in assignment PDF.
    :param shade_t: array, description in assignment PDF.

    :return: array, description in assignment PDF.
    """

    # keep the vertices in an array, in order to find the maximum vertex
    faces_depth = []
    for face in faces:
        faces_depth.append(max(depth[face]))

    # sorting faces by depth form the array faces_depth
    faces_depth = np.array(faces_depth)
    indexes = faces_depth.argsort()
    faces_depth = faces_depth[indexes[::-1]]
    faces = faces[indexes[::-1]]

    # initialize the canvas, size is given
    M = 512
    N = 512
    img = np.ones((M, N, 3))

    # shading technique according to shade_t variable
    for face in faces:
        if shade_t == 'flat':
            img = flats(img, verts2d[face], vcolors[face])
        elif shade_t == 'gouraud':
            img = gourauds(img, verts2d[face], vcolors[face])

    return img
