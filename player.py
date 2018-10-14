import numpy as np
import camera

class Player(camera.Camera):
    def __init__(self, posX=0, posY=0) -> None:
        super().__init__(posX, posY)
        self.velocity = np.zeros((2,), np.float32)

    def move_forward(self, magnitude):
        self.velocity += self.facing_vector * magnitude

    def move_sideways(self, magnitude):
        perpVector = np.ndarray((2,), np.float32)

        perpVector[0] = self.facing_vector[1]
        perpVector[1] = -self.facing_vector[0]

        self.velocity+= perpVector*magnitude

    def update(self, worldMap :np.ndarray, deltatime :float):
        self.velocity *= 0.6
        if self.velocity[0]**2 < 0.0000000001:
            self.velocity[0] = 0
        if self.velocity[1]**2 < 0.0000000001:
            self.velocity[1] = 0

        newpos = self.pos+self.velocity*deltatime
        if worldMap[int(np.floor(newpos[0]))][int(np.floor(newpos[1]))] != 0:
            self.velocity[0] = 0
            self.velocity[1] = 0
            self.pos = np.round(self.pos, 2)
        else:
            self.pos = newpos
