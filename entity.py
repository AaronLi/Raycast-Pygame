import camera, math_tools, math
from pygame import image
import numpy as np



class Entity(camera.Camera):
    def __init__(self,sprites, posX=0, posY=0) -> None:
        super().__init__(posX, posY)
        self.sprites = [image.load('textures/sprite_stand.png').convert_alpha(), image.load("textures/sprite_stand_back.png").convert_alpha(), image.load("textures/sprite_stand_left.png").convert_alpha(), image.load("textures/sprite_stand_right.png").convert_alpha()]
        self.velocity = np.zeros((2,), np.float32)

    def get_sprite(self, viewer_vector, viewer_pos):
        dot_product = np.dot(viewer_vector, self.facing_vector)
        determinant = np.linalg.det((viewer_vector, self.facing_vector))
        angle = math.atan2(determinant, dot_product)
        angle = math.degrees(angle)

        if abs(angle) < 45:
            return self.sprites[1]
        elif abs(angle) > 135:
            return self.sprites[0]
        else:
            if angle > 0:
                return self.sprites[2]
            else:
                return self.sprites[3]