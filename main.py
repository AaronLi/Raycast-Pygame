from pygame import *
import numpy as np
import camera

running = True

screen = display.set_mode((1280, 720))

mapSimple = [
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,6,6,6,6,6,6,6,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,6,0,0,0,6,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,6,0,0,0,5,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,6,0,0,6,0,0,0,4,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,6,0,0,0,3,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,6,0,0,0,2,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,6,0,0,6,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,6,0,0,0,2,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,6,6,6,6,3,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

workMap = np.ndarray((24,24), dtype=np.int32)

for i,v in enumerate(mapSimple):
    workMap[i] = v

cam = camera.Camera(12, 12)

clockity = time.Clock()

keysDown = [False, False, False, False]

lockMouse = True

while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        elif e.type == KEYDOWN:
            if e.key == K_w:
                keysDown[0] = True
            elif e.key == K_a:
                keysDown[1] = True
            elif e.key == K_s:
                keysDown[2] = True
            elif e.key == K_d:
                keysDown[3] = True
            elif e.key == K_ESCAPE:
                lockMouse = not lockMouse
        elif e.type == KEYUP:
            if e.key == K_w:
                keysDown[0] = False
            elif e.key == K_a:
                keysDown[1] = False
            elif e.key == K_s:
                keysDown[2] = False
            elif e.key == K_d:
                keysDown[3] = False
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 4:
                cam.facing_vector*=1.1
            elif e.button == 5:
                cam.facing_vector*=1/1.1
    screen.fill((0,0,0))
    if keysDown[0]:
        cam.move_forward(0.1)
    if keysDown[1]:
        cam.move_sideways(-0.1)
    if keysDown[2]:
        cam.move_forward(-0.1)
    if keysDown[3]:
        cam.move_sideways(0.1)
    mouse.set_visible(not lockMouse)
    event.set_grab(lockMouse)
    if lockMouse:
        cam.rotate_camera(mouse.get_rel()[0]/15)

    drawSurf = Surface((512, 288))
    cam.render_scene(drawSurf, workMap)

    screen.blit(transform.scale(drawSurf, (1280,720)), (0,0))
    display.flip()

    clockity.tick(20)
    display.set_caption(str(clockity.get_fps()))