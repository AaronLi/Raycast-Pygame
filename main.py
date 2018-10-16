from pygame import *
import game_world, filereader
import numpy as np
font.init()
running = True

screen = display.set_mode((1280,800))

arialFont = font.SysFont("Arial", 20)

gameworld = game_world.GameWorld().load_world_from_file("dat/world1.txt")

debug_sprite = image.load("textures/test_sprite.png").convert_alpha()




gameworld.add_entity(filereader.read_file("doom_demon.json"))
gameworld.add_entity(filereader.read_file("standing_target.json"))

#gameworld.entities[0].rotate_camera(180)

player = filereader.read_file("player.json")
player.rotate_camera(180)
player.held_weapon = filereader.read_file("doom_shotgun.json")
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
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1 and player.can_fire():
                player.fire_weapon()
            player.handle_mouse_botton(e.button, True)
        elif e.type == MOUSEBUTTONUP:
            player.handle_mouse_botton(e.button, False)
    screen.fill((0,0,0))
    deltatime = clockity.get_time()/1000

    mouse.set_visible(not lockMouse)
    event.set_grab(lockMouse)
    if lockMouse:
        player.rotate_camera(mouse.get_rel()[0]/15)


    gameworld.update_world(deltatime)

    render_size = (640, 360)
    drawSurf = Surface(render_size)
    gameworld.draw_world(drawSurf)


    screen.blit(transform.scale(drawSurf, (render_size[0]*2, render_size[1]*2)), (0,0))


    if showHud:
        player.draw_hud(screen)
        screen.blit(arialFont.render("FPS: %.2f" % clockity.get_fps(), True, (255, 255, 255), (0, 0, 0)), (5, 5))
    display.flip()

    clockity.tick(30)