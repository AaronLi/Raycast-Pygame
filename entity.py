import camera, math_tools, math
from pygame import image
import numpy as np

#For positional viewing, 0 is front, 1 is back, 2 is left, 3 is right

class Entity(camera.Camera):

    FRONT = 0
    BACK = 1
    REAR = 1
    LEFT = 2
    RIGHT = 3

    def __init__(self, posX=0, posY=0) -> None:
        super().__init__(posX, posY)

        self.standing_sprites = []
        self.walking_sprites = []
        self.width = 0
        self.sprite_percentage = 0
        self.health = 100
        self.max_health = 100
        self.set_sprites([image.load('textures/girl/sprite_stand.png').convert_alpha(), image.load("textures/girl/sprite_stand_back.png").convert_alpha(), image.load("textures/girl/sprite_stand_left.png").convert_alpha(), image.load("textures/girl/sprite_stand_right.png").convert_alpha()])
        self.velocity = np.zeros((2,), np.float32)

    def get_sprite(self, viewer_vector):
        view_index = self.get_facing_index(viewer_vector)
        moving_speed = math.hypot(self.velocity[0], self.velocity[1])
        if moving_speed > 0.2:
            return self.walking_sprites[view_index].get_frame()
        else:
            return self.standing_sprites[view_index]

    def set_sprites(self, sprites):
        self.standing_sprites = sprites

        front_sprite = self.standing_sprites[0]

        left_side = 0
        right_side = 0

        for i in range(front_sprite.get_width()):
            colour = front_sprite.get_at((i, front_sprite.get_height()//2))
            if colour[3] != 0:
                left_side = i-1
                break
        for i in range(front_sprite.get_width()-1, -1, -1):
            colour = front_sprite.get_at((i, front_sprite.get_height() // 2))
            if colour[3] != 0:
                right_side = i + 1
                break

        self.width = right_side-left_side

        self.sprite_percentage = self.width / front_sprite.get_width() # percentage of the texture that is filled by the sprite

    def update(self, worldMap: np.ndarray, deltatime: float):
        self.velocity *= 0.6
        if self.velocity[0] ** 2 < 0.0000000001:
            self.velocity[0] = 0
        if self.velocity[1] ** 2 < 0.0000000001:
            self.velocity[1] = 0

        newpos = self.pos + self.velocity * deltatime
        if worldMap[int(np.floor(newpos[0]))][int(np.floor(newpos[1]))] != 0:
            self.velocity[0] = 0
            self.velocity[1] = 0
            self.pos = np.round(self.pos, 2)
        else:
            self.pos = newpos
        for i in self.walking_sprites:
            i.update(deltatime)

    def move_forward(self, magnitude):
        self.velocity += self.facing_vector * magnitude

    def move_sideways(self, magnitude):
        perpVector = np.ndarray((2,), np.float32)

        perpVector[0] = self.facing_vector[1]
        perpVector[1] = -self.facing_vector[0]

        self.velocity += perpVector * magnitude

    def get_facing_index(self, viewer_vector):
        dot_product = np.dot(viewer_vector, self.facing_vector)
        determinant = np.linalg.det((viewer_vector, self.facing_vector))
        angle = math.atan2(determinant, dot_product)
        angle = math.degrees(angle)

        if abs(angle) < 45:
            return Entity.REAR
        elif abs(angle) > 135:
            return Entity.FRONT
        else:
            if angle > 0:
                return Entity.LEFT
            else:
                return Entity.RIGHT