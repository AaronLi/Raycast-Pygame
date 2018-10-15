from pygame import *
import numpy as np
import player, entity
font.init()
running = True

screen = display.set_mode((1280,800))

arialFont = font.SysFont("Arial", 20)

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
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,6,6,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,6,0,0,0,5,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,6,0,0,6,0,0,0,4,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,6,0,0,0,3,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,6,0,0,0,2,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,6,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,6,0,0,0,2,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,6,6,6,6,3,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

workMap = np.ndarray((24,24), dtype=np.int32)

for i,v in enumerate(mapSimple):
    workMap[i] = v

#enemySprite = image.load("textures/sprite_stand.png").convert_alpha()

entities = []

entities.append(entity.Entity(None, 15, 12))

player = player.Player(14, 3)
entities.append(player)

clockity = time.Clock()

keysDown = [False, False, False, False]

lockMouse = True
showHud = True
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
            elif e.key == K_F1:
                showHud = not showHud
        elif e.type == KEYUP:
            if e.key == K_w:
                keysDown[0] = False
            elif e.key == K_a:
                keysDown[1] = False
            elif e.key == K_s:
                keysDown[2] = False
            elif e.key == K_d:
                keysDown[3] = False

    screen.fill((0,0,0))
    if keysDown[0]:
        player.move_forward(1)
    if keysDown[1]:
        player.move_sideways(-1)
    if keysDown[2]:
        player.move_forward(-1)
    if keysDown[3]:
        player.move_sideways(1)
    mouse.set_visible(not lockMouse)
    event.set_grab(lockMouse)
    if lockMouse:
        player.rotate_camera(mouse.get_rel()[0]/15)

    player.update(mapSimple, clockity.get_time()/1000)
    render_size = (640, 360)
    drawSurf = Surface(render_size)
    player.render_scene(drawSurf, mapSimple, entities)


    screen.blit(transform.scale(drawSurf, (render_size[0]*2, render_size[1]*2)), (0,0))
    if showHud:
        draw.line(screen, (255,255,255), (render_size[0]+5, render_size[1]), (render_size[0]-5, render_size[1]), 2)
        draw.line(screen, (255, 255, 255), (render_size[0], render_size[1]+5), (render_size[0], render_size[1]-5), 2)

        screen.blit(arialFont.render("FPS: %.2f"%clockity.get_fps(), True, (255,255,255), (0,0,0)), (5,5))


    display.flip()

    clockity.tick(30)