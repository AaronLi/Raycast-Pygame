import numpy as np
import camera, pygame

pygame.font.init()

debugFont = pygame.font.SysFont("Consolas", 30)

class GameWorld:
    def __init__(self) -> None:
        self.entities = []
        self.world = np.ndarray((32, 32), np.int32)
        self.camera = None

    def set_world(self, new_world):
        for i,v in enumerate(new_world):
            self.world[i] = v

    def set_camera(self, entity :camera.Camera):
        self.camera = entity

    def update_world(self, delta_time):
        for i in self.entities:
            i.update(self.world, delta_time)

    def draw_world(self, surface):
        if self.camera is not None:
            self.camera.render_scene(surface, self.world, self.entities)
        else:
            renderFont = debugFont.render("No camera assigned", True, (255,255,255), (0,0,0))

            surface.blit(renderFont, (surface.get_width()//2 - renderFont.get_width()//2, surface.get_height()//2 - renderFont.get_height()//2))

    def load_world_from_file(self, filename):
        with open(filename) as f:
            for i,v in enumerate(f):
                for j,w in enumerate(v.split()):
                    self.world[i, j] = int(w)
        return self

    def add_entity(self, entity):
        self.entities.append(entity)

    def get_world(self):
        return self.world

    def get_entities(self):
        return self.entities