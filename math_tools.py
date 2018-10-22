import numpy as np
import math
from pygame import transform, Surface, SRCALPHA

#unit_vector and angle_between are from
# https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python/13849249#13849249

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    dot_product = np.dot(v1, v2)
    determinant = np.linalg.det((v1, v2))
    angle = math.atan2(determinant, dot_product)
    angle = math.degrees(angle)
    return angle

def scale_image(surfIn :Surface, scale_amount):
    new_size = (surfIn.get_width()*scale_amount, surfIn.get_height()*scale_amount)

    return transform.scale(surfIn, new_size)

def tile_image(to_tile :Surface, tile_amount :int):
    '''
    Tiles int(tile_amount) times
    :param to_tile: Surface
    :param tile_amount: int
    :return: Surface, to_tile tiled tile_amount times
    '''

    tile_amount = int(tile_amount)
    out_surf = Surface((to_tile.get_width()*tile_amount, to_tile.get_height()*tile_amount), SRCALPHA)

    for i in range(tile_amount):
        for j in range(tile_amount):
            out_surf.blit(to_tile, (to_tile.get_width()*j, to_tile.get_height()*i))
    return out_surf


def distance_manhattan(start_pos, end_pos):
    combined_distance = abs(start_pos[0]-end_pos[0]) + abs(start_pos[1]-end_pos[1])
    return combined_distance

def distance_euclidean(start_pos, end_pos):
    distance = math.hypot(start_pos[0]-end_pos[0], start_pos[1]-end_pos[1])
    return distance

