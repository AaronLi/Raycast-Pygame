from pygame import Surface, draw, image, transform, SRCALPHA, surfarray
import numpy as np
import math

textures = [
    image.load("textures/cobblestone.png"),
    image.load("textures/cobblestone_mossy.png"),
    image.load("textures/chiseled_stone_bricks.png"),
    image.load("textures/cracked_stone_bricks.png"),
    image.load("textures/mossy_stone_bricks.png"),
    image.load("textures/stone_bricks.png"),
    image.load("textures/stone_slab_top.png")]

def double_tile_surface(surfaceIn :Surface):
    surfaceOut = Surface((surfaceIn.get_width()*2, surfaceIn.get_height()*2), SRCALPHA)
    surfaceOut.blit(surfaceIn, (0,0))
    surfaceOut.blit(surfaceIn, (surfaceIn.get_width(), 0))
    surfaceOut.blit(surfaceIn, (0, surfaceIn.get_height()))
    surfaceOut.blit(surfaceIn, (surfaceIn.get_width(), surfaceIn.get_height()))
    return surfaceOut

for i,v in enumerate(textures):
    textures[i] = double_tile_surface(v)

class Camera:
    NORTH_SOUTH = True
    EAST_WEST = False

    def __init__(self, posX = 0, posY = 0) -> None:
        global placeholder_texture
        self.pos = np.ndarray((2,), np.float32)

        self.pos[0] = posX

        self.pos[1] = posY

        self.facing_vector = np.ndarray((2,), np.float32) # essentially a vector that points in the direction the camera faces
        self.camera_plane = np.ndarray((2,), np.float32)

        #changing the magnitude of this provides a scope zoom in effect
        self.facing_vector[0] = -1
        self.facing_vector[1] = 0

        # ~ the camera plane is always perpendicular to the facing vector
        # ~ changing the ratio between the facing vector and camera plane will change the FOV.
        # ~ centering is handled by the reflection that will occur in the render method where
        #   the camera plane will be reflected upon the facing vector


        self.camera_plane[0] = 0
        self.camera_plane[1] = 0.66

    def move_forward(self, move_distance):
        self.pos+=self.facing_vector*move_distance

    def move_sideways(self, move_distance):
        perpVec = np.ndarray((2,), np.float32)
        perpVec[0] = self.facing_vector[1]
        perpVec[1] = -self.facing_vector[0]
        self.pos+= perpVec*move_distance

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

        drawSurf = Surface(surface.get_size(), SRCALPHA)

        for screen_x in range(surface.get_width()):
            map_pos = self.pos.astype(np.int32)
            precise_ray = self.pos.copy()

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
            precise_ray+=check_position/distance_between_gridline_x_y
            #begin casting ray

            while not hit:

                if check_position[0] < check_position[1]:
                    check_position[0] += distance_between_gridline_x_y[0]
                    map_pos[0]+=step_direction[0]
                    hit_direction = Camera.EAST_WEST
                    precise_ray[0]+=step_direction[0]
                else:
                    check_position[1] += distance_between_gridline_x_y[1]
                    map_pos[1] += step_direction[1]
                    hit_direction = Camera.NORTH_SOUTH
                    precise_ray[1]+=step_direction[1]

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

            start_y = int(surface.get_height()//2 - lineHeight//2)
            if start_y<0:
                start_y = 0

            end_y = int(surface.get_height()//2 + lineHeight//2)
            if end_y >= surface.get_height():
                start_y = surface.get_height()-1

            if hit_direction == Camera.EAST_WEST:
                pixel_pos = self.pos[1] + distance*ray_direction[1]
            else:
                pixel_pos = self.pos[0] + distance*ray_direction[0]
            pixel_pos = (pixel_pos-math.floor(pixel_pos))
            blitPixels = textures[hit_data].subsurface((int(pixel_pos * textures[hit_data].get_width()), 0, 1, textures[hit_data].get_height())).copy()
            if hit_direction == Camera.EAST_WEST:
                darkenSurf = Surface((1, blitPixels.get_height()))
                darkenSurf.set_alpha(128)
                blitPixels.blit(darkenSurf, (0,0))

            surface.blit(transform.scale(blitPixels, (1, end_y - start_y)), (screen_x, start_y))

            # floor casting

            floor_texture_coordinate = np.ndarray((2,), np.float32)

            if hit_direction == Camera.EAST_WEST:
                if ray_direction[0] > 0:
                    floor_texture_coordinate[0] = map_pos[0]
                    floor_texture_coordinate[1] = map_pos[1] + pixel_pos
                else:
                    floor_texture_coordinate[0] = map_pos[0] + 1
                    floor_texture_coordinate[1] = map_pos[1] + pixel_pos
            else:
                if ray_direction[1] > 0:
                    floor_texture_coordinate[0] = map_pos[0] + pixel_pos
                    floor_texture_coordinate[1] = map_pos[1]
                else:
                    floor_texture_coordinate[0] = map_pos[0] + pixel_pos
                    floor_texture_coordinate[1] = map_pos[1] + 1

            distance_to_wall = distance

            distance_from_player = 0
            if end_y < 0:
                end_y = surface.get_height()

            # print(surface.get_bytesize())
            drawBuf = surfarray.pixels3d(surface)
            for screen_y in range(end_y, surface.get_height()):
                current_distance = surface.get_height() / (
                        2 * screen_y - surface.get_height())  # TODO: figure out this equation

                weight = (current_distance - distance_from_player) / (distance_to_wall - distance_from_player)

                current_floor_pos = weight * floor_texture_coordinate + (1 - weight) * self.pos

                floor_texture_pos = np.ndarray((2,), np.int32)

                floor_texture_pos[0] = int(current_floor_pos[0] * textures[4].get_width()) % textures[4].get_width()
                floor_texture_pos[1] = int(current_floor_pos[1] * textures[4].get_height()) % textures[
                    4].get_height()
                col = textures[4].get_at((floor_texture_pos[0], floor_texture_pos[1]))

                drawBuf[screen_x][screen_y] = col[:3]
                drawBuf[screen_x][surface.get_height() - screen_y] = col[:3]

            del drawBuf




if __name__ == "__main__":
    cam = Camera()
    print(cam.facing_vector)