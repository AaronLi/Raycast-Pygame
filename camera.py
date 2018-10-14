from pygame import Surface, draw
import numpy as np
import math

class Camera:
    NORTH_SOUTH = True
    EAST_WEST = False

    def __init__(self, posX = 0, posY = 0) -> None:
        self.pos = np.ndarray((2,), np.float32)

        self.pos[0] = posX

        self.pos[1] = posY

        self.facing_vector = np.ndarray((2,), np.float32) # essentially a vector that points in the direction the camera faces
        self.camera_plane = np.ndarray((2,), np.float32)

        self.facing_vector[0] = -1
        self.facing_vector[1] = 0

        # ~ the camera plane is always perpendicular to the facing vector
        # ~ changing the ratio between the facing vector and camera plane will change the FOV.
        # ~ centering is handled by the reflection that will occur in the render method where
        #   the camera plane will be reflected upon the facing vector

        # change the camera plane magnitude to change fov

        self.camera_plane[0] = 0
        self.camera_plane[1] = 0.66

    def move_forward(self, move_distance):
        self.pos+=self.facing_vector*move_distance

    def rotate_camera(self, angle_degrees):
        rotate_matrix = np.ndarray((2,2), np.float32)

        ang_rad = math.radians(angle_degrees)
        rotate_matrix[0] = [math.cos(ang_rad), -math.sin(ang_rad)]
        rotate_matrix[1] = [math.sin(ang_rad), math.cos(ang_rad)]

        self.facing_vector = np.dot(self.facing_vector, rotate_matrix)
        self.camera_plane = np.dot(self.camera_plane, rotate_matrix)

    def render_scene(self, surface :Surface, world :np.ndarray):

        check_position = np.ndarray((2,), np.float32)

        step_direction = np.ndarray((2,), np.int32)

        for screen_x in range(surface.get_width()):
            map_pos = self.pos.astype(np.int32)

            # screen_x is the column of pixels on the screen whose rendering info is being checked

            direction_variation = 2*(screen_x/surface.get_width())-1 # a scalar that represents the amount of deviation a raycasted vector will have from the facing vector

            # both x and y can be calculated in one line because of numpy magic :D
            ray_direction = self.facing_vector + self.camera_plane * direction_variation # the facing vector + the direction variation scaled by the camera plane

            distance_between_gridline_x_y = np.absolute(1/ray_direction)

            hit = False

            #setup initial ray cast

            if ray_direction[0] < 0: #casting leftwards
                step_direction[0] = -1
                check_position[0] = (self.pos[0] - map_pos[0]) * distance_between_gridline_x_y[0] # distance from a point within the square outwards to the left side of the square
            else: #casting rightwards
                step_direction[0] = 1
                check_position[0] = (map_pos[0] + 1 - self.pos[0]) * distance_between_gridline_x_y[0]

            if ray_direction[1] < 0:
                step_direction[1] = -1
                check_position[1] = (self.pos[1] - map_pos[1]) * distance_between_gridline_x_y[1]
            else:
                step_direction[1] = 1
                check_position[1] = (map_pos[1] + 1 - self.pos[1]) * distance_between_gridline_x_y[1]

            #begin casting ray

            while not hit:

                if check_position[0] < check_position[1]:
                    check_position[0] += distance_between_gridline_x_y[0]
                    map_pos[0]+=step_direction[0]
                    hit_direction = Camera.EAST_WEST
                else:
                    check_position[1] += distance_between_gridline_x_y[1]
                    map_pos[1] += step_direction[1]
                    hit_direction = Camera.NORTH_SOUTH

                if world[map_pos[0], map_pos[1]] != 0:
                    hit = True

            if hit_direction == Camera.EAST_WEST:
                distance = (map_pos[0] - self.pos[0] + (1 - step_direction[0]) / 2) / ray_direction[0]
            else:
                distance = (map_pos[1] - self.pos[1] + (1 - step_direction[1]) / 2) / ray_direction[1]


            #distance to surface has been found, now to calculate the height of the wall onscreen

            if distance == 0:
                distance = 1

            lineHeight = surface.get_height() // distance

            hit_data = world[map_pos[0], map_pos[1]]

            colour = (0,0,0)

            if hit_data == 1:
                colour = (255,0,0)
            elif hit_data == 2:
                colour = (0,255,0)
            elif hit_data == 3:
                colour = (0,0,255)
            elif hit_data == 4:
                colour = (255,255,255)
            elif hit_data == 5:
                colour = (255,255,0)

            if hit_direction == Camera.EAST_WEST:
                colour = (colour[0]/2, colour[1]/2, colour[2]/2) #make north south face darker for pseudo lighting

            start_y = surface.get_height()//2 - lineHeight//2
            if start_y<0:
                start_y = 0

            end_y = surface.get_height()//2 + lineHeight//2
            if end_y >= surface.get_height():
                start_y = surface.get_height()-1

            draw.line(surface, colour, (screen_x, start_y), (screen_x, end_y))

if __name__ == "__main__":
    cam = Camera()
    print(cam.facing_vector)