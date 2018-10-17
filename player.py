import numpy as np

import entity, pygame, math_tools, math, animation, weapon
from pygame import image, draw, font

font.init()

uiFont = font.SysFont("Arial", 20)

firing_gun_animation = animation.Animation(animation.ONE_WAY).set_frames([image.load("textures/doom_sg/doom_shotgun%03d.png"%(i)) for i in range(0, 14)], 8)

holding_gun = math_tools.scale_image(image.load("textures/doom_sg/doom_shotgun_default.png"), 3)


class Player(entity.Entity):
    def __init__(self, parent_world, posX=0, posY=0) -> None:
        super().__init__(posX, posY)
        self.parent_world = parent_world
        self.keysdown = [False for i in range(pygame.K_LAST)]
        self.mouse_buttons_down = [False for i in range(6)]
        self.old_mouse_buttons = [False for i in range(6)]
        self.held_weapon = None

    def set_weapon(self, new_weapon):
        self.held_weapon = new_weapon
        self.held_weapon.set_mouse_button_listener(self.mouse_buttons_down, self.old_mouse_buttons)

    def handle_key(self, key_value, key_state):
        self.keysdown[key_value] = key_state

    def handle_mouse_botton(self, mouse_button, mouse_button_state):
        self.mouse_buttons_down[mouse_button] = mouse_button_state

    def update(self, worldMap: np.ndarray, deltatime: float):
        self.pickup_items()
        if self.keysdown[pygame.K_w]:
            self.move_forward(1)
        if self.keysdown[pygame.K_a]:
            self.move_sideways(-1)
        if self.keysdown[pygame.K_s]:
            self.move_forward(-1)
        if self.keysdown[pygame.K_d]:
            self.move_sideways(1)
        if not self.held_weapon.is_reloading() and self.keysdown[pygame.K_r]:
            self.held_weapon.current_mag = 0
        super().update(worldMap, deltatime)
        if self.held_weapon.try_to_shoot():
            self.check_hitscan_hits()
        self.held_weapon.update(deltatime)
        for i, v in enumerate(self.mouse_buttons_down):
            self.old_mouse_buttons[i] = v


    def check_hitscan_hits(self):
        for i in self.sprites_in_view:
            angle_deviation = math.degrees(math_tools.angle_between(i.pos-self.pos, self.facing_vector))

            position_difference = i.pos - self.pos

            distance = math.hypot(position_difference[0], position_difference[1])

            current_deviation_max = (21.5*i.sprite_percentage)/distance
            if current_deviation_max>angle_deviation:
                i.damage(self.held_weapon.damage)

    def can_fire(self):
        return self.held_weapon.can_fire()

    def draw_hud(self, draw_surface):

        render_size = (draw_surface.get_width()//2, (draw_surface.get_height()-80)//2)


        shoot_frame = math_tools.scale_image(self.held_weapon.get_frame(), 3)
        draw_surface.blit(shoot_frame, (draw_surface.get_width()//2 - shoot_frame.get_width()//2, draw_surface.get_height()-80 - shoot_frame.get_height()))

        ammoCounter= uiFont.render("%02d/%02d"%(self.held_weapon.current_mag, self.held_weapon.mag_size), True, (255,255,255))
        draw_surface.blit(ammoCounter, (5, draw_surface.get_height()-ammoCounter.get_height()-5))

        draw.line(draw_surface, (255,255,255), (render_size[0]+5, render_size[1]), (render_size[0]-5, render_size[1]), 2)
        draw.line(draw_surface, (255, 255, 255), (render_size[0], render_size[1]-5), (render_size[0], render_size[1]+5), 2)



    def pickup_items(self):
        for i in range(len(self.colliding_sprites) - 1, -1, -1):
            collidedEntity = self.colliding_sprites[i]
            if type(collidedEntity) == weapon.Weapon_Entity:
                if collidedEntity.can_pick_up():
                    collidedEntity.health = 0
                    self.parent_world.entities.append(self.held_weapon.get_floor_entity(self.pos[0], self.pos[1]))
                    self.held_weapon = collidedEntity.weapon
                    self.held_weapon.set_mouse_button_listener(self.mouse_buttons_down, self.old_mouse_buttons)
