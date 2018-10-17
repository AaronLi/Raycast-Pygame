import camera, pygame

pygame.font.init()

debugFont = pygame.font.SysFont("Consolas", 30)

class GameWorld:
    def __init__(self) -> None:
        self.entities = []
        self.world = None
        self.camera = None

    def set_world(self, new_world):
        self.world = new_world

    def set_camera(self, entity :camera.Camera):
        self.camera = entity

    def update_world(self, delta_time):
        for i in range(len(self.entities)-1, -1, -1):
            if self.entities[i].health is not None:
                if self.entities[i].health <=0:
                    print('ded')
                    del self.entities[i]
                    continue
            self.entities[i].update(self.world, delta_time)

    def draw_world(self, surface):
        if self.camera is not None:
            self.camera.render_scene(surface, self.world, self.entities)
        else:
            renderFont = debugFont.render("No camera assigned", True, (255,255,255), (0,0,0))

            surface.blit(renderFont, (surface.get_width()//2 - renderFont.get_width()//2, surface.get_height()//2 - renderFont.get_height()//2))

    def add_entity(self, entity):
        self.entities.append(entity)

    def get_world(self):
        return self.world

    def get_entities(self):
        return self.entities