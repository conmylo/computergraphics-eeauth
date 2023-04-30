# Linear interpolation function
def interpolate_color(p1, p2, V1, V2, xy, dim):
    """
    Calculates the vector value at a given point through linear interpolation between 2 other points at the same line.

    :param p1: tuple, the vertices of Point 1.
    :param p2: tuple, the vertices of Point 2.
    :param V1: tuple, the vector values at Point 1.
    :param V2: tuple, the vector values at Point 2.
    :param xy: float, x or y coordinate depending on dim (dimension) value.
    :param dim: int, the dimension in which the xy belongs.

    :return: tuple, the vector value at Point p, calculated through linear interpolation.
    """

    # 2 cases, if dim is 1 or dim is 2
    if dim == 1:
        m = (V2[0] - V1[0]) / (p2[0] - p1[0])
        b = V1[0] - m * p1[0]
        V = m * xy + b
    elif dim == 2:
        m = (V2[1] - V1[1]) / (p2[1] - p1[1])
        b = V1[1] - m * p1[1]
        V = m * xy + b
    else:
        raise ValueError("Invalid dim value: dim must be either 1 or 2.")
    return V
