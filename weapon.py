import animation, entity

class Weapon():
    def __init__(self) -> None:
        self.reload_animation = animation.Animation(animation.ONE_WAY)
        self.firing_animation = animation.Animation(animation.ONE_WAY)
        self.holding_animation = animation.Animation()
        self.ground_animations = [animation.Animation() for i in range(4)]

        self.mag_size = 30
        self.damage = 80
        self.current_mag = 30
        self.was_reloading = False

    def set_mag_size(self, mag_size):
        self.mag_size = mag_size
        self.current_mag = mag_size

    def update(self, deltatime):
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


    def fire_weapon(self):
        fired = False
        print(self.current_mag, self.mag_size)
        if self.current_mag > 0 and self.reload_animation.animation_done_running():
            self.current_mag-=1
            self.firing_animation.start_animation()
            fired = True
        return fired

    def get_frame(self):
        if not self.reload_animation.animation_done_running():
            return self.reload_animation.get_frame()
        elif not self.firing_animation.animation_done_running():
            return self.firing_animation.get_frame()
        else:
            return self.holding_animation.get_frame()

class Weapon_Entity(entity.Entity):
    def __init__(self, weapon, posX=0, posY=0) -> None:
        super().__init__(posX, posY)
        self.weapon = weapon