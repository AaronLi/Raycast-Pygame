import entity, weapon, math


class WeaponProjectile(entity.Entity):

    unhittable_types = {weapon.Weapon_Entity}

    def __init__(self, posX, posY, facing, velocity, damage) -> None:
        super().__init__(posX, posY)
        self.speed_reduction = 0
        self.facing_vector = facing
        self.velocity = velocity
        self.damage_on_hit = damage
        self.hit_radius = 0.3
        self.health = None

    def check_collisions(self, entities):
        hit_grid = {}
        for i in entities:
            if i is not self:
                hit_grid_pos = (int(i.pos[0]*10), int(i.pos[1]*10))
                if hit_grid_pos in hit_grid:
                    hit_grid[hit_grid_pos].append(i)
                else:
                    hit_grid[hit_grid_pos] = [i]
        projectile_grid_pos = (int(self.pos[0]*10), int(i.pos[1]*10))

        for i in hit_grid[projectile_grid_pos]:
            entity_type = type(i)
            if entity_type != WeaponProjectile and entity_type not in WeaponProjectile.unhittable_types:
                distance_difference = i.pos-self.pos
                distance_from_projectile = math.hypot(distance_difference[0], distance_difference[1])

                if distance_from_projectile < self.hit_radius:
                    i.damage(self.damage_on_hit)
                    self.health = 0
                    break