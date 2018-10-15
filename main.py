from pygame import *
import numpy as np
import player, entity, game_world
font.init()
running = True

screen = display.set_mode((1280,800))

arialFont = font.SysFont("Arial", 20)

gameworld = game_world.GameWorld().load_world_from_file("dat/world2.txt")


#gameworld.add_entity(entity.Entity(None, 15, 12))

player = player.Player(1.5, 1.5)
player.rotate_camera(180)
gameworld.add_entity(player)
gameworld.set_camera(player)
clockity = time.Clock()

keysDown = [False, False, False, False]

lockMouse = True
showHud = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                lockMouse = not lockMouse
            elif e.key == K_F1:
                showHud = not showHud
            else:
                player.handle_key(e.key, True)
        elif e.type == KEYUP:
            player.handle_key(e.key, False)
    screen.fill((0,0,0))

    mouse.set_visible(not lockMouse)
    event.set_grab(lockMouse)
    if lockMouse:
        player.rotate_camera(mouse.get_rel()[0]/15)

    gameworld.update_world(clockity.get_time()/1000)

    render_size = (640, 360)
    drawSurf = Surface(render_size)
    gameworld.draw_world(drawSurf)

    screen.blit(transform.scale(drawSurf, (render_size[0]*2, render_size[1]*2)), (0,0))


    if showHud:
        draw.line(screen, (255,255,255), (render_size[0]+5, render_size[1]), (render_size[0]-5, render_size[1]), 2)
        draw.line(screen, (255, 255, 255), (render_size[0], render_size[1]+5), (render_size[0], render_size[1]-5), 2)

        screen.blit(arialFont.render("FPS: %.2f"%clockity.get_fps(), True, (255,255,255), (0,0,0)), (5,5))


    display.flip()

    clockity.tick(30)