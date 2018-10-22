import camera, world_map, math, animation, math_tools
from pygame import image, Surface
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
        self.velocity = np.zeros((2,), np.float32)

    def get_sprite(self, viewer_vector):
        view_index = self.get_facing_index(viewer_vector)
        moving_speed = math.hypot(self.velocity[0], self.velocity[1])
        if moving_speed > 0.2:
            return self.walking_sprites[view_index].get_frame()
        else:
            outputImage = self.standing_sprites[view_index]
            if  type(outputImage)== Surface:
                return self.standing_sprites[view_index]
            elif type(outputImage) == animation.Animation:
                return self.standing_sprites[view_index].get_frame()

    def set_sprites(self, sprites):
        self.standing_sprites = sprites

        front_sprite = self.standing_sprites[0].get_frame()

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

    def update(self, worldMap: world_map.World_Map, deltatime: float, velocity_reduction_scalar = 0.6):
        self.velocity *= velocity_reduction_scalar
        if self.velocity[0] ** 2 < 0.0000000001:
            self.velocity[0] = 0
        if self.velocity[1] ** 2 < 0.0000000001:
            self.velocity[1] = 0

        newpos = self.pos + self.velocity * deltatime
        if worldMap.map_data[int(np.floor(newpos[0]))][int(np.floor(newpos[1]))] != 0:
            self.velocity[0] = 0
            self.velocity[1] = 0
            self.pos = np.round(self.pos, 2)
        else:
            self.pos = newpos
        for i in self.walking_sprites:
            i.update(deltatime)

    def move_forward(self, magnitude):
        facing_vector_magnitude = math.hypot(self.facing_vector[0], self.facing_vector[1])
        self.velocity += self.facing_vector * magnitude/facing_vector_magnitude

    def move_sideways(self, magnitude):
        facing_vector_magnitude = math.hypot(self.facing_vector[0], self.facing_vector[1])
        perpVector = np.ndarray((2,), np.float32)

        perpVector[0] = self.facing_vector[1]
        perpVector[1] = -self.facing_vector[0]

        self.velocity += perpVector * magnitude / facing_vector_magnitude

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

    def damage(self, damage_amount):
        if self.health is not None:
            self.health-=damage_amount

    def rotate_camera(self, angle_degrees):
        super().rotate_camera(angle_degrees)
        return self

    def find_steps_to_coordinate(self, map :np.ndarray, destination):
        # move from my position to destination using a*
        closed_set = {}
        open_set = {self.pos.astype(np.int32)}

