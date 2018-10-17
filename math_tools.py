import numpy as np
import math
from pygame import transform, Surface

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
