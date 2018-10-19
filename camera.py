from pygame import Surface, draw, image, transform, SRCALPHA, surfarray, BLEND_MULT
import numpy as np
import math, world_map


def double_tile_surface(surfaceIn :Surface):
    surfaceOut = Surface((surfaceIn.get_width()*2, surfaceIn.get_height()*2), SRCALPHA)
    surfaceOut.blit(surfaceIn, (0,0))
    surfaceOut.blit(surfaceIn, (surfaceIn.get_width(), 0))
    surfaceOut.blit(surfaceIn, (0, surfaceIn.get_height()))
    surfaceOut.blit(surfaceIn, (surfaceIn.get_width(), surfaceIn.get_height()))
    return surfaceOut

class Camera:
    NORTH_SOUTH = True
    EAST_WEST = False

    def __init__(self, posX = 0, posY = 0) -> None:
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

        self.sprites_in_view = []
        self.colliding_sprites = []


    # camera has absolute position movement
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


    def render_scene(self,surface :Surface, w_map :world_map.World_Map, sprites :list, FLOORCAST = False):
        """
        renders the world using raycasting
        :param surface:
        :param world:
        :param sprites:
        :param FLOORCAST:
        :return: None
        """


        self.sprites_in_view = []
        self.colliding_sprites = []
        check_position = np.ndarray((2,), np.float32)

        step_direction = np.ndarray((2,), np.int32)

        zbuffer = np.ndarray((surface.get_width(),), np.float32)

        draw.rect(surface, (20, 20, 20), (0, 0, surface.get_width(), surface.get_height()//2))
        draw.rect(surface, (40, 40, 40), (0, surface.get_height()//2, surface.get_width(), surface.get_height() // 2))


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

                if w_map.map_data[map_pos[0]][map_pos[1]] != 0:
                    hit = True

            if hit_direction == Camera.EAST_WEST:
                distance = (map_pos[0] - self.pos[0] + (1 - step_direction[0]) / 2) / ray_direction[0]
            else:
                distance = (map_pos[1] - self.pos[1] + (1 - step_direction[1]) / 2) / ray_direction[1]


            #distance to surface has been found, now to calculate the height of the wall onscreen

            if distance == 0:
                distance = 1

            lineHeight = surface.get_height() // distance

            hit_data = w_map.map_data[map_pos[0]][map_pos[1]]

            start_y = int(surface.get_height()//2 - lineHeight//2)

            end_y = int(surface.get_height()//2 + lineHeight//2)


            if hit_direction == Camera.EAST_WEST:
                pixel_pos = self.pos[1] + distance*ray_direction[1]
            else:
                pixel_pos = self.pos[0] + distance*ray_direction[0]
            pixel_pos = (pixel_pos-math.floor(pixel_pos))
            blitPixels = w_map.textures[hit_data].subsurface((int(pixel_pos * w_map.textures[hit_data].get_width()), 0, 1, w_map.textures[hit_data].get_height())).copy()
            if hit_direction == Camera.EAST_WEST:
                darkenSurf = Surface((1, blitPixels.get_height()))
                darkenSurf.set_alpha(128)
                blitPixels.blit(darkenSurf, (0,0))
            darkenSurf = Surface((1, blitPixels.get_height()))
            darkenSurf.set_alpha(min(20*distance, 255))
            blitPixels.blit(darkenSurf, (0, 0))

            scaled_pixels = transform.scale(blitPixels, (1, min(end_y - start_y, 50000)))


            surface.blit(scaled_pixels, (screen_x, start_y))

            # fill in z buffer

            zbuffer[screen_x] = distance

            # floor casting
            if FLOORCAST:
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

                drawBuf = surfarray.pixels3d(surface)
                for screen_y in range(end_y, surface.get_height()):
                    current_distance = surface.get_height() / (
                            2 * screen_y - surface.get_height())

                    weight = (current_distance - distance_from_player) / (distance_to_wall - distance_from_player)

                    current_floor_pos = weight * floor_texture_coordinate + (1 - weight) * self.pos

                    floor_texture_pos = np.ndarray((2,), np.int32)

                    floor_texture_pos[0] = int(current_floor_pos[0] * w_map.textures[4].get_width()) % w_map.textures[4].get_width()
                    floor_texture_pos[1] = int(current_floor_pos[1] * w_map.textures[4].get_height()) % w_map.textures[
                        4].get_height()
                    col = w_map.textures[4].get_at((floor_texture_pos[0], floor_texture_pos[1]))

                    drawBuf[screen_x][screen_y] = col[:3]
                    drawBuf[screen_x][surface.get_height() - screen_y] = col[:3]

                del drawBuf
        # sprite casting
        sprites = [s for s in sprites if s != self]


        sprite_draw_order = [(0, 0) for i in range(len(sprites))]

        for i, sprite in enumerate(sprites):
            sprite_draw_order[i] = (((self.pos[0] - sprite.pos[0])**2 + (self.pos[1] - sprite.pos[1])**2), i)

        sprite_draw_order.sort(reverse=True)

        for i,v in enumerate(sprite_draw_order):
            seen_sprite = False
            draw_sprite = sprites[v[1]].get_sprite(self.facing_vector)
            sprite_pos_rel_to_camera = sprites[v[1]].pos - self.pos
            if(sprite_pos_rel_to_camera[0] == 0 and sprite_pos_rel_to_camera[1] == 0):
                sprite_pos_rel_to_camera[0] = 0.01
                sprite_pos_rel_to_camera[1] = 0.01

            if math.hypot(sprite_pos_rel_to_camera[0], sprite_pos_rel_to_camera[1]) < 0.4:
                self.colliding_sprites.append(sprites[v[1]])

            invDet = 1 / (self.camera_plane[0] * self.facing_vector[1] - self.facing_vector[0] * self.camera_plane[1])

            transformX = invDet * (self.facing_vector[1] * sprite_pos_rel_to_camera[0] - self.facing_vector[0] * sprite_pos_rel_to_camera[1])
            transformY = invDet * (-self.camera_plane[1] * sprite_pos_rel_to_camera[0] + self.camera_plane[0] * sprite_pos_rel_to_camera[1])
            spriteScreenPos = int((surface.get_width()/2) * (1+transformX/transformY))

            sprite_height = abs(int(surface.get_height()/transformY))

            sprite_width = abs(int(surface.get_height()/transformY))

            start_x = spriteScreenPos - sprite_width//2
            if start_x < 0:
                start_x = 0

            end_x = spriteScreenPos + sprite_width//2
            if end_x > surface.get_width():
                end_x = surface.get_width()-1

            for draw_stripe_x in range(start_x, end_x):
                textureX = int(256*(draw_stripe_x - (-sprite_width / 2 + spriteScreenPos)) * draw_sprite.get_width() / sprite_width) / 256
                if 0 < transformY and 0 < draw_stripe_x:
                    if transformY< zbuffer[draw_stripe_x]  and draw_stripe_x < surface.get_width():

                        spriteSlice = transform.scale(draw_sprite.subsurface((textureX, 0, 1, draw_sprite.get_height())).copy(), (1, min(sprite_height, 50000)))

                        shaderSurf = Surface((1, min(spriteSlice.get_height(), 400)), SRCALPHA)
                        shade_val = min(22*math.hypot(sprite_pos_rel_to_camera[0], sprite_pos_rel_to_camera[1]), 255)

                        shaderSurf.fill([255-shade_val, 255-shade_val, 255-shade_val])

                        spriteSlice.blit(shaderSurf, (0,0), (0, 0)+shaderSurf.get_size(), BLEND_MULT) # blend mult multiplies each rgb value by the blitter's rgb/255 value

                        surface.blit(spriteSlice, (draw_stripe_x, surface.get_height()//2 - spriteSlice.get_height()//2))

                        if draw_stripe_x == int(surface.get_width()//2): # if the stripe goes through the user's crosshairs
                            seen_sprite = True
            if seen_sprite:
                self.sprites_in_view.append(sprites[v[1]])

        return surface

if __name__ == "__main__":
    cam = Camera()