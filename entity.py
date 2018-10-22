import camera, world_map, math, animation, math_tools
from pygame import Surface
import numpy as np

#For positional viewing, 0 is front, 1 is back, 2 is left, 3 is right



class Entity(camera.Camera):

    FRONT = 0
    BACK = 1
    REAR = 1
    LEFT = 2
    RIGHT = 3
    EPSILON = 0.00001

    def __init__(self, posX=0, posY=0) -> None:
        super().__init__(posX, posY)

        self.standing_sprites = []
        self.walking_sprites = []
        self.width = 0
        self.sprite_percentage = 0
        self.health = 100
        self.max_health = 100
        self.velocity = np.zeros((2,), np.float32)
        self.path = []
        self.destination = None

    def get_sprite(self, viewer_vector):
        view_index = self.get_facing_index(viewer_vector)
        moving_speed = math.hypot(self.velocity[0], self.velocity[1])
        if moving_speed > 0.2:
            return self.walking_sprites[view_index].get_frame()
        else:
            outputImage = self.standing_sprites[view_index]
            if type(outputImage)== Surface:
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
        #print(self.pos)
        if self.destination is not None:
            self.pathfind(worldMap.map_data, self.destination, deltatime)

        self.velocity *= velocity_reduction_scalar
        if self.velocity[0] ** 2 < Entity.EPSILON:
            self.velocity[0] = 0
        if self.velocity[1] ** 2 < Entity.EPSILON:
            self.velocity[1] = 0

        newpos = self.pos + self.velocity * deltatime
        if worldMap.map_data[int(np.floor(newpos[0]))][int(np.floor(newpos[1]))] != 0:
            self.velocity[0] = 0
            self.velocity[1] = 0
            self.pos = np.round(self.pos, 2)
        else:
            self.pos = newpos
        for i in self.standing_sprites:
            i.update(deltatime)
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
        angle = math_tools.angle_between(self.facing_vector, viewer_vector)

        #based on the angle you're looking at, a different side will be shown to you
        if abs(angle) < 45:
            return Entity.REAR
        elif abs(angle) > 135:
            return Entity.FRONT
        else:
            if angle < 0:
                return Entity.LEFT
            else:
                return Entity.RIGHT

    def damage(self, damage_amount):
        if self.health is not None:
            self.health-=damage_amount

    def rotate_camera(self, angle_degrees):
        super().rotate_camera(angle_degrees)
        return self

    def set_destination(self, destination):
        self.destination = destination
        return self

    def pathfind(self, world_grid, destination, deltatime):
        self.path = self._find_steps_to_coordinate(world_grid, destination)
        if self.path is None or len(self.path) <= 1: # if there is only 1 element, your position is the destination
            return

        next_position = (self.path[1][0]+0.5, self.path[1][1]+0.5) #all points are moved by 0.5 so the entity is in the center of the cube
        position_relative_to_self = (self.pos[0]-next_position[0], self.pos[1] - next_position[1])

        #if entity is close enough to destination in a certain position, move it inline with the destination
        if abs(position_relative_to_self[0]) < Entity.EPSILON:
            self.pos[0] = next_position[0]
            self.velocity[0] = 0
        if abs(position_relative_to_self[1]) < Entity.EPSILON:
            self.pos[1] = next_position[1]
            self.velocity[1] = 0

        position_relative_to_self = (next_position[0] - self.pos[0], next_position[1] - self.pos[1])

        angle_to_destination = math_tools.angle_between(self.facing_vector, position_relative_to_self)

        if abs(angle_to_destination) < 2:
            self.rotate_camera(-angle_to_destination)
            self.move_forward(1)
        else:
            if abs(angle_to_destination) <= 40:
                rotate_amount = 3
            elif abs(angle_to_destination) <=20:
                rotate_amount = 1
            else:
                rotate_amount = 5

            if angle_to_destination < 0:
                self.rotate_camera(rotate_amount)
            else:
                self.rotate_camera(-rotate_amount)

    def _find_steps_to_coordinate(self, map :np.ndarray, destination):
        #A* algorithm, some optimizations may be needed in respect to the data structures used
        # move from my position to destination using a*
        start_pos = tuple(self.pos.astype(np.int32))
        end_pos = (int(destination[0]), int(destination[1]))
        closed_set = set()
        open_set = [start_pos] #when in use, these values will be shifted by [0.5, 0.5] so the entity will be in the center of the block
        came_from = dict()
        gScore = dict()
        gScore[start_pos] = 0

        fScore = dict()
        fScore[start_pos] = math_tools.distance_manhattan(start_pos, destination)

        while len(open_set) > 0:
            current_check_node = open_set[0]
            for i in open_set:
                if fScore[i] < fScore[current_check_node]:
                    current_check_node = i

            if current_check_node == end_pos:
                return _reconstruct_path(came_from, end_pos) #replace with reconstruct_path

            open_set.remove(current_check_node)
            closed_set.add(current_check_node)

            neighbour_coordinates = [(1,0), (-1,0), (0,1), (0,-1)]

            #remove coordinates that are either out of bounds or in a wall
            for i in range(len(neighbour_coordinates)-1, -1, -1):
                potential_neighbour_position = (neighbour_coordinates[i][0]+current_check_node[0], neighbour_coordinates[i][1] + current_check_node[1])
                if potential_neighbour_position[0] < map.shape[0] and potential_neighbour_position[1] < map.shape[1]:
                    if map[potential_neighbour_position[0]][potential_neighbour_position[1]] != 0:
                        del neighbour_coordinates[i]
                else:
                    del neighbour_coordinates[i]

            for i in neighbour_coordinates:
                neighbour_pos = (current_check_node[0]+i[0], current_check_node[1] + i[1])
                if neighbour_pos in closed_set:
                    continue

                tentative_gscore = gScore[current_check_node] + math_tools.distance_manhattan(current_check_node, neighbour_pos)

                if neighbour_pos not in open_set:
                    open_set.append(neighbour_pos)
                else:
                    if neighbour_pos in gScore:
                        if tentative_gscore >= gScore[neighbour_pos]:
                            continue
                came_from[neighbour_pos] = current_check_node
                gScore[neighbour_pos] = tentative_gscore
                fScore[neighbour_pos] = gScore[neighbour_pos] + math_tools.distance_manhattan(neighbour_pos, destination)


def _reconstruct_path(came_from :dict, current_pos):
    total_path = [current_pos]

    destination = current_pos

    while destination in came_from.keys():
        destination = came_from[destination] #change destination to the node that leads to destination
        total_path.append(destination)
    total_path.reverse()
    return total_path