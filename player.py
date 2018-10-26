import numpy as np

import entity, pygame, math_tools, math, animation, weapon, world_map
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
        self.weapon_shake = 0
        self.held_weapon_time = 0

    def set_weapon(self, new_weapon):
        self.held_weapon_time = 0
        self.held_weapon = new_weapon
        self.held_weapon.set_mouse_button_listener(self.mouse_buttons_down, self.old_mouse_buttons)

    def handle_key(self, key_value, key_state):
        self.keysdown[key_value] = key_state

    def handle_mouse_botton(self, mouse_button, mouse_button_state):
        self.mouse_buttons_down[mouse_button] = mouse_button_state

    def update(self, worldMap: world_map.World_Map, deltatime: float):
        self.pickup_items()

        self.move_player()

        if not self.held_weapon.is_reloading() and self.keysdown[pygame.K_r]:
            self.held_weapon.current_mag = 0
        super().update(worldMap, deltatime)
        if self.held_weapon.try_to_shoot():
            self.check_hitscan_hits()
        self.held_weapon.update(deltatime)
        for i, v in enumerate(self.mouse_buttons_down):
            self.old_mouse_buttons[i] = v
        self.held_weapon_time += deltatime


    def check_hitscan_hits(self):
        for i in self.sprites_in_view:
            if self.is_looking_at(i):
                i.damage(self.held_weapon.damage)

    def can_fire(self):
        return self.held_weapon.can_fire()

    def draw_hud(self, draw_surface):

        render_size = (draw_surface.get_width()//2, (draw_surface.get_height()-80)//2)


        shoot_frame = math_tools.scale_image(self.held_weapon.get_frame(), 3)

        #center bottom of screen
        shoot_frame_pos = [draw_surface.get_width()//2 - shoot_frame.get_width()//2, draw_surface.get_height()-80 - shoot_frame.get_height()]

        #move weapon around to make it seem more lively
        LIFT_WEAPON_TIME = 0.5

        if self.held_weapon_time >= LIFT_WEAPON_TIME:
            shoot_frame_pos[0] -= 20*math.sin(math.radians(20*self.weapon_shake))
            shoot_frame_pos[1] += 20 * abs(math.sin(math.radians(20 * self.weapon_shake)))
            self.held_weapon_time = LIFT_WEAPON_TIME
        else:
            shoot_frame_pos[1] = draw_surface.get_height()-80 - shoot_frame.get_height()*(self.held_weapon_time/LIFT_WEAPON_TIME)


        draw_surface.blit(shoot_frame, shoot_frame_pos)

        draw.rect(draw_surface, (0,0,0), (0, draw_surface.get_height()-80, draw_surface.get_width(), 80))

        ammoCounter= uiFont.render("%02d/%02d"%(self.held_weapon.current_mag, self.held_weapon.mag_size), True, (255,255,255))
        draw_surface.blit(ammoCounter, (5, draw_surface.get_height()-ammoCounter.get_height()-5))

        draw.line(draw_surface, (255,255,255), (render_size[0]+5, render_size[1]), (render_size[0]-5, render_size[1]), 2)
        draw.line(draw_surface, (255, 255, 255), (render_size[0], render_size[1]-5), (render_size[0], render_size[1]+5), 2)



    def pickup_items(self):
        for i in range(len(self.colliding_sprites) - 1, -1, -1):
            collidedEntity = self.colliding_sprites[i]
            if type(collidedEntity) == weapon.Weapon_Entity:
                if collidedEntity.can_pick_up():
                    print("Blah")
                    collidedEntity.health = 0
                    new_entity = self.held_weapon.get_floor_entity(self.pos[0], self.pos[1])
                    new_entity.facing_vector = self.facing_vector
                    new_entity.move_forward(20)
                    self.parent_world.entities.append(new_entity)
                    self.set_weapon(collidedEntity.weapon)

    def move_player(self):
        move_vector = np.zeros((2), np.int32)

        if self.keysdown[pygame.K_w]:
            move_vector[0]+=1
        elif self.keysdown[pygame.K_s]:
            move_vector[0]-=1
        if self.keysdown[pygame.K_a]:
            move_vector[1]+=1
        if self.keysdown[pygame.K_d]:
            move_vector[1]-=1
        angle = math_tools.angle_between(move_vector, (1,0))
        magnitude = 1.2
        if self.keysdown[pygame.K_LSHIFT]:
            magnitude = 1.7
        if any(move_vector):
            self.weapon_shake+=magnitude
            self.move_forward(magnitude*math.cos(math.radians(angle)))
            self.move_sideways(magnitude*math.sin(math.radians(angle)))