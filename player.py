import numpy as np

import entity, pygame


class Player(entity.Entity):
    def __init__(self, posX=0, posY=0) -> None:
        super().__init__(None, posX, posY)
        self.keysdown = [False for i in range(pygame.K_LAST)]

    def handle_key(self, key_value, key_state):
        self.keysdown[key_value] = key_state

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

