import json,  math_tools
import world_map, entity, animation, player, weapon
import numpy as np
from pygame import image

def read_file(filename, parent_world = None):
    with open(filename) as f:
        loaded_object = json.load(f)
        if loaded_object['type'] == 'entity' or loaded_object['type'] == 'player':
            return _load_entity(loaded_object, loaded_object['type'] == 'player', game_world= parent_world)
        elif loaded_object['type'] == 'weapon':
            return _load_weapon(loaded_object)
        elif loaded_object['type'] == 'map':
            return _load_world(loaded_object)
        else:
            print("object type not found")

def create_template(filename, template_type = 'entity'):
    success = True
    if template_type == 'entity':
        data = {
            "type": "entity",
            "health":100,
            "x_position":1.5,
            "y_position":1.5,
            "frames":{
                "front":{
                    "standing":"",
                    "walking":{
                        "frames":[],
                        "frame_rate":5
                    }
                },
                "rear":{
                    "standing":"",
                    "walking":{
                        "frames":[],
                        "frame_rate":5
                    }
                },
                "left":{
                    "standing":"",
                    "walking":{
                        "frames":[],
                        "frame_rate":5
                    }
                },
                "right":{
                    "standing":"",
                    "walking":{
                        "frames":[],
                        "frame_rate":5
                    }
                }
            }
        }
        success = True
    elif template_type == 'weapon':
        data = {
            "type": "weapon",
            "fire_mode": "full_auto",
            "fire_rate": 800.0,
            "mag_size": 30,
            "damage": 33.4,
            "frames": {
                "hold":{
                    "frames":[],
                    "frame_rate":5
                },
                "firing":{
                    "frames":[],
                    "frame_rate":10
                },
                "reload":{
                    "frames":[],
                    "reload_time":8
                },
                "ground":{
                    "front":{
                        "frames":[],
                        "frame_rate":5
                    },
                    "back": {
                        "frames": [],
                        "frame_rate": 5
                    },
                    "left": {
                        "frames": [],
                        "frame_rate": 5
                    },
                    "right": {
                        "frames": [],
                        "frame_rate": 5
                    }
                }
            }
        }
    elif template_type == 'map':
        #TODO: make map building tool
        data = {
            "type":"map",
            "size":[5, 5],
            "textures":[
                {"path":"",
                 "tile_amount":2.0
                 }
            ],
            "map_data":[
                [1, 1, 1, 1, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 1, 1, 1, 1]
            ]

        }
    else:
        print("Invalid template specifier")
        success = False
    if success:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=True)

if __name__ == "__main__":
    file_directory = input("filename:\n>>> ")
    uIn = input("load or save file?\n>>> ")
    if uIn == "load":
        read_file(file_directory)
    elif uIn == "save":
        template_type = input("template to be generated:\n>>> ")
        create_template(file_directory, template_type)
        print("Created file %s"%file_directory)


def _load_entity(loaded_object, is_player = False, game_world = None):
    initial_x_position = loaded_object['x_position']
    initial_y_position = loaded_object['y_position']

    front_standing_sprites = animation.Animation()
    front_standing_sprites.set_frames(__load_animation_frames(loaded_object['frames']['front']['standing']['frames']), loaded_object['frames']['front']['standing']['frame_rate'])
    rear_standing_sprites = animation.Animation()
    rear_standing_sprites.set_frames(__load_animation_frames(loaded_object['frames']['rear']['standing']['frames']), loaded_object['frames']['rear']['standing']['frame_rate'])
    left_standing_sprites = animation.Animation()
    left_standing_sprites.set_frames(__load_animation_frames(loaded_object['frames']['left']['standing']['frames']), loaded_object['frames']['left']['standing']['frame_rate'])
    right_standing_sprites = animation.Animation()
    right_standing_sprites.set_frames(__load_animation_frames(loaded_object['frames']['right']['standing']['frames']), loaded_object['frames']['right']['standing']['frame_rate'])

    standing_sprites = [front_standing_sprites, rear_standing_sprites, left_standing_sprites, right_standing_sprites]

    front_walking_sprite_filehandles = loaded_object['frames']['front']['walking']['frames']
    rear_walking_sprite_filehandles = loaded_object['frames']['rear']['walking']['frames']
    left_walking_sprite_filehandles = loaded_object['frames']['left']['walking']['frames']
    right_walking_sprite_filehandles = loaded_object['frames']['right']['walking']['frames']

    front_walking_sprites = __load_animation_frames(front_walking_sprite_filehandles)
    rear_walking_sprites = __load_animation_frames(rear_walking_sprite_filehandles)
    left_walking_sprites = __load_animation_frames(left_walking_sprite_filehandles)
    right_walking_sprites = __load_animation_frames(right_walking_sprite_filehandles)

    front_walking_animation = animation.Animation().set_frames(front_walking_sprites,
        loaded_object['frames']['front']['walking']['frame_rate'])
    rear_walking_animation = animation.Animation().set_frames(rear_walking_sprites, loaded_object['frames']['rear']['walking']['frame_rate'])
    left_walking_animation = animation.Animation().set_frames(left_walking_sprites,
        loaded_object['frames']['left']['walking']['frame_rate'])
    right_walking_animation = animation.Animation().set_frames(right_walking_sprites,
        loaded_object['frames']['left']['walking']['frame_rate'])

    front_walking_animation.passed_time = 0
    rear_walking_animation.passed_time = 0
    left_walking_animation.passed_time = 0
    right_walking_animation.passed_time = 0

    outEntity = entity.Entity(initial_x_position, initial_y_position)

    if is_player:
        outEntity = player.Player(game_world, initial_x_position, initial_y_position)

    outEntity.set_sprites(standing_sprites)
    outEntity.walking_sprites = [front_walking_animation, rear_walking_animation, left_walking_animation,
                                 right_walking_animation]
    return outEntity

def _load_weapon(loaded_object):
    outWeapon = weapon.Weapon()

    # single variable parameters
    outWeapon.set_mag_size(loaded_object["mag_size"])
    outWeapon.damage = loaded_object['damage']
    outWeapon.set_fire_rate(loaded_object['fire_rate'])

    #holding firing and reloading animations
    outWeapon.holding_animation.set_frames(__load_animation_frames(loaded_object['frames']['hold']['frames']), loaded_object['frames']['hold']['frame_rate'])
    outWeapon.firing_animation.set_frames(__load_animation_frames(loaded_object['frames']['firing']['frames']), loaded_object['frames']['firing']['frame_rate'])

    reloadFrames = [image.load(i).convert_alpha() for i in loaded_object['frames']['reload']['frames']]
    reload_fps = len(reloadFrames)/loaded_object['frames']['reload']['reload_time']
    outWeapon.reload_animation.set_frames(reloadFrames, reload_fps)

    #fire mode parameter
    loaded_weapon_fire_mode = loaded_object['fire_mode'].lower().strip()
    if loaded_weapon_fire_mode == 'semi_auto':
        outWeapon.fire_mode = weapon.SEMI_AUTO
    elif loaded_weapon_fire_mode == 'full_auto':
        outWeapon.fire_mode = weapon.FULL_AUTO

    #on ground animations
    on_ground_front = __load_animation_frames(loaded_object['frames']['ground']['front']['frames'])
    on_ground_left = __load_animation_frames(loaded_object['frames']['ground']['left']['frames'])
    on_ground_right = __load_animation_frames(loaded_object['frames']['ground']['right']['frames'])
    on_ground_back = __load_animation_frames(loaded_object['frames']['ground']['back']['frames'])

    outWeapon.ground_animations[0].set_frames(on_ground_front, loaded_object['frames']['ground']['front']['frame_rate'])
    outWeapon.ground_animations[1].set_frames(on_ground_back, loaded_object['frames']['ground']['back']['frame_rate'])
    outWeapon.ground_animations[2].set_frames(on_ground_left, loaded_object['frames']['ground']['left']['frame_rate'])
    outWeapon.ground_animations[3].set_frames(on_ground_right, loaded_object['frames']['ground']['right']['frame_rate'])
    return outWeapon

def _load_world(loaded_object):
    textures = [None]+[math_tools.tile_image(image.load(i['path']).convert_alpha(), i['tile_amount']) for i in loaded_object['textures']]

    map_data = np.zeros(loaded_object['size'], np.int32)

    for i,v in enumerate(loaded_object['map_data']):
        for j,w in enumerate(v):
            map_data[i,j] = w
    out_map = world_map.World_Map()

    out_map.textures = textures
    out_map.map_data = map_data

    return out_map

def __load_animation_frames(file_locations):

    frames = []

    for i in file_locations:
        frames.append(image.load(i).convert_alpha())


    return frames