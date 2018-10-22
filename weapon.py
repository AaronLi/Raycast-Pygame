import numpy as np

import animation, entity

SEMI_AUTO = 0
FULL_AUTO = 1

class Weapon():

    def __init__(self) -> None:
        self.mouse_buttons = [False for i in range(6)]
        self.reload_animation = animation.Animation(animation.ONE_WAY)
        self.firing_animation = animation.Animation(animation.ONE_WAY)
        self.holding_animation = animation.Animation()
        self.ground_animations = [animation.Animation() for i in range(4)]

        self.mag_size = 30
        self.damage = 80
        self.current_mag = 30
        self.was_reloading = False
        self.fire_mode = SEMI_AUTO
        self.fire_cooldown = 0.5
        self.current_fire_countdown = 0
        self.old_button_states = []

    def set_mag_size(self, mag_size):
        self.mag_size = mag_size
        self.current_mag = mag_size

    def update(self, deltatime):
        self.current_fire_countdown -= deltatime
        self.reload_animation.update(deltatime)
        self.firing_animation.update(deltatime)
        self.holding_animation.update(deltatime)
        for i in self.ground_animations:
            i.update(deltatime)

        if self.current_mag == 0 and self.reload_animation.animation_done_running() and self.firing_animation.animation_done_running():
            if self.was_reloading:
                self.current_mag = self.mag_size
                self.was_reloading = False
            else:
                self.reload_animation.start_animation()
                self.was_reloading = True


    def try_to_shoot(self):
        if self.can_fire() and self.mouse_buttons[1]:
            self.current_mag-=1
            self.current_fire_countdown = self.fire_cooldown
            if self.firing_animation.animation_done_running():
                self.firing_animation.start_animation()
            return True
        return False

    def set_fire_rate(self, rounds_per_minute):
        rounds_per_second = rounds_per_minute/60
        seconds_per_round = 1/rounds_per_second
        self.fire_cooldown = seconds_per_round

    def get_frame(self):
        if not self.reload_animation.animation_done_running():
            return self.reload_animation.get_frame()
        elif not self.firing_animation.animation_done_running():
            return self.firing_animation.get_frame()
        else:
            return self.holding_animation.get_frame()

    def can_fire(self):
        cooldown_met = self.current_fire_countdown<=0
        has_rounds = self.current_mag>0
        not_reloading = self.reload_animation.animation_done_running()
        mouse_just_pressed = not self.old_button_states[1] and self.mouse_buttons[1]

        able_to_fire = cooldown_met and has_rounds and not_reloading
        if self.fire_mode == SEMI_AUTO:
            able_to_fire = able_to_fire and mouse_just_pressed

        return able_to_fire


    def is_reloading(self):
        return not self.reload_animation.animation_done_running()

    def set_mouse_button_listener(self, mouse_buttons, old_mouse_buttons):
        self.mouse_buttons = mouse_buttons
        self.old_button_states = old_mouse_buttons

    def get_floor_entity(self,initial_pos_x, initial_pos_y):
        entityOut = Weapon_Entity(self, initial_pos_x, initial_pos_y)
        entityOut.health = None
        return entityOut

class Weapon_Entity(entity.Entity):
    def __init__(self,weapon, posX=0, posY=0) -> None:
        super().__init__(posX, posY)
        self.weapon = weapon
        self.standing_sprites = self.weapon.ground_animations
        self.walking_sprites = self.weapon.ground_animations
        self.cooldown = 2
        self.health = None
        self.weapon.current_mag = 0

    def update(self, worldMap: np.ndarray, deltatime: float, velocity_reduction_scalar = 0.6):
        super().update(worldMap, deltatime, velocity_reduction_scalar)
        self.cooldown-=deltatime


    def can_pick_up(self):
        #the pickup cooldown is done and this object isn't marked for deletion
        return self.cooldown <=0 and self.health is None