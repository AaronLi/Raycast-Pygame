from pygame import *
import game_world, filereader

font.init()

running = True

screen = display.set_mode((1280,800))

event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP])

arialFont = font.SysFont("Arial", 20)

gameworld = game_world.GameWorld()
gameworld.world = filereader.read_file("world2.json")

debug_sprite = image.load("textures/test_sprite.png").convert_alpha()

gameworld.add_entity(filereader.read_file("doom_demon.json").rotate_camera(-90))
#gameworld.add_entity(filereader.read_file("standing_target.json"))
#gameworld.add_entity(filereader.read_file("standing_target2.json"))

gameworld.add_entity(filereader.read_file("assault_rifle.json").get_floor_entity(5.5, 3.5))

player = filereader.read_file("player.json", gameworld)
#gameworld.entities[0].rotate_camera(90)
player.rotate_camera(90)
player.set_weapon(filereader.read_file("doom_shotgun.json"))
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

    #todo: make settings menu to change resolution
    render_size = (640,360)
    drawSurf = Surface(render_size)
    gameworld.draw_world(drawSurf)
    screen.blit(transform.scale(drawSurf, (1280, 720)), (0,0))

    gameworld.entities[0].in_line_of_sight(player, gameworld)

    if showHud:
        player.draw_hud(screen)
        screen.blit(arialFont.render("FPS: %.2f" % clockity.get_fps(), True, (255, 255, 255), (0, 0, 0)), (5, 5))
    display.flip()

    clockity.tick(30)