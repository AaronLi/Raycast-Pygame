import numpy as np

import entity, pygame, math_tools, math, animation
from pygame import image, draw

firing_gun_animation = animation.Animation(animation.ONE_WAY).set_frames([image.load("textures/doom_sg/doom_shotgun%03d.png"%(i)) for i in range(0, 14)], 8)

holding_gun = math_tools.scale_image(image.load("textures/doom_sg/doom_shotgun_default.png"), 3)


class Player(entity.Entity):
    def __init__(self, posX=0, posY=0) -> None:
        super().__init__(posX, posY)
        self.keysdown = [False for i in range(pygame.K_LAST)]
        self.mouse_buttons_down = [False for i in range(6)]
        self.old_mouse_buttons = [False for i in range(6)]

    def handle_key(self, key_value, key_state):
        self.keysdown[key_value] = key_state

    def handle_mouse_botton(self, mouse_button, mouse_button_state):
        self.mouse_buttons_down[mouse_button] = mouse_button_state

    def update(self, worldMap: np.ndarray, deltatime: float):

        if self.keysdown[pygame.K_w]:
            self.move_forward(1)
        if self.keysdown[pygame.K_a]:
            self.move_sideways(-1)
        if self.keysdown[pygame.K_s]:
            self.move_forward(-1)
        if self.keysdown[pygame.K_d]:
            self.move_sideways(1)
        super().update(worldMap, deltatime)
        firing_gun_animation.update(deltatime)
        self.check_hitscan_hits()

        for i, v in enumerate(self.mouse_buttons_down):
            self.old_mouse_buttons[i] = v

    def check_hitscan_hits(self):
        for i in self.sprites_in_view:
            angle_deviation = math.degrees(math_tools.angle_between(i.pos-self.pos, self.facing_vector))

            position_difference = i.pos - self.pos

            distance = math.hypot(position_difference[0], position_difference[1])

            current_deviation_max = (21.5*i.sprite_percentage)/distance
            if current_deviation_max>angle_deviation and self.mouse_buttons_down[1] and not self.old_mouse_buttons[1]:
                i.health -= 80

    def fire_weapon(self):
        firing_gun_animation.start_animation()

    def can_fire(self):
        return firing_gun_animation.animation_done_running()

    def draw_hud(self, draw_surface):

        render_size = (draw_surface.get_width()//2, (draw_surface.get_height()-80)//2)

        if not firing_gun_animation.animation_done_running():
            shoot_frame = math_tools.scale_image(firing_gun_animation.get_frame(), 3)
            draw_surface.blit(shoot_frame, (draw_surface.get_width()//2 - shoot_frame.get_width()//2, draw_surface.get_height()-80 - shoot_frame.get_height()))
        else:
            draw_surface.blit(holding_gun, (draw_surface.get_width()//2 - holding_gun.get_width()//2, draw_surface.get_height()-80 - holding_gun.get_height()))

        draw.line(draw_surface, (255,255,255), (render_size[0]+5, render_size[1]), (render_size[0]-5, render_size[1]), 2)
        draw.line(draw_surface, (255, 255, 255), (render_size[0], render_size[1]-5), (render_size[0], render_size[1]+5), 2)



        