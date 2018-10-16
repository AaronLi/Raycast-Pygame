import json, entity, animation, player, weapon
from pygame import image

def read_file(filename):
    with open(filename) as f:
        loaded_object = json.load(f)
        if loaded_object['type'] == 'entity' or loaded_object['type'] == 'player':
            return _load_entity(loaded_object, loaded_object['type'] == 'player')
        if loaded_object['type'] == 'weapon':
            return _load_weapon(loaded_object)


def create_template(filename, template_type = 'entity'):
    success = False
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
        success = True
    else:
        print("Invalid template specifier")
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


def _load_entity(loaded_object, is_player = False):
    initial_x_position = loaded_object['x_position']
    initial_y_position = loaded_object['y_position']

    front_standing_sprite = image.load(loaded_object['frames']['front']['standing']).convert_alpha()
    rear_standing_sprite = image.load(loaded_object['frames']['rear']['standing']).convert_alpha()
    left_standing_sprite = image.load(loaded_object['frames']['left']['standing']).convert_alpha()
    right_standing_sprite = image.load(loaded_object['frames']['right']['standing']).convert_alpha()

    standing_sprites = [front_standing_sprite, rear_standing_sprite, left_standing_sprite, right_standing_sprite]

    front_walking_sprite_filehandles = loaded_object['frames']['front']['walking']['frames']
    rear_walking_sprite_filehandles = loaded_object['frames']['rear']['walking']['frames']
    left_walking_sprite_filehandles = loaded_object['frames']['left']['walking']['frames']
    right_walking_sprite_filehandles = loaded_object['frames']['right']['walking']['frames']

    front_walking_sprites = []
    rear_walking_sprites = []
    left_walking_sprites = []
    right_walking_sprites = []

    for i in front_walking_sprite_filehandles:
        front_walking_sprites.append(image.load(i).convert_alpha())

    for i in rear_walking_sprite_filehandles:
        rear_walking_sprites.append(image.load(i).convert_alpha())

    for i in left_walking_sprite_filehandles:
        left_walking_sprites.append(image.load(i).convert_alpha())

    for i in right_walking_sprite_filehandles:
        right_walking_sprites.append(image.load(i).convert_alpha())

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
        outEntity = player.Player(initial_x_position, initial_y_position)

    outEntity.set_sprites(standing_sprites)
    outEntity.walking_sprites = [front_walking_animation, rear_walking_animation, left_walking_animation,
                                 right_walking_animation]
    return outEntity

def _load_weapon(loaded_object):
    outWeapon = weapon.Weapon()
    outWeapon.set_mag_size(loaded_object["mag_size"])
    outWeapon.damage = loaded_object['damage']

    outWeapon.holding_animation.set_frames([image.load(i).convert_alpha() for i in loaded_object['frames']['hold']['frames']], loaded_object['frames']['hold']['frame_rate'])
    outWeapon.firing_animation.set_frames([image.load(i).convert_alpha() for i in loaded_object['frames']['firing']['frames']], loaded_object['frames']['firing']['frame_rate'])

    reloadFrames = [image.load(i).convert_alpha() for i in loaded_object['frames']['reload']['frames']]
    reload_fps = len(reloadFrames)/loaded_object['frames']['reload']['reload_time']
    outWeapon.reload_animation.set_frames(reloadFrames, reload_fps)



    return outWeapon