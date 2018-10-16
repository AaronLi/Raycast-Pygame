import json, entity, animation, player
from pygame import image

def read_file(filename):
    with open(filename) as f:
        loaded_object = json.load(f)
        if loaded_object['type'] == 'entity' or loaded_object['type'] == 'player':

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

            front_walking_animation = animation.Animation().set_frames(front_walking_sprites, int(loaded_object['frames']['front']['walking']['frame_rate']))
            rear_walking_animation = animation.Animation().set_frames(rear_walking_sprites, int(loaded_object['frames']['rear']['walking']['frame_rate']))
            left_walking_animation = animation.Animation().set_frames(left_walking_sprites, int(loaded_object['frames']['left']['walking']['frame_rate']))
            right_walking_animation = animation.Animation().set_frames(right_walking_sprites, int(loaded_object['frames']['left']['walking']['frame_rate']))

            front_walking_animation.passed_time = 0
            rear_walking_animation.passed_time = 0
            left_walking_animation.passed_time = 0
            right_walking_animation.passed_time = 0

            outEntity = entity.Entity(initial_x_position, initial_y_position)

            if loaded_object['type'] == 'player':
                outEntity = player.Player(initial_x_position, initial_y_position)

            outEntity.set_sprites(standing_sprites)
            outEntity.walking_sprites = [front_walking_animation, rear_walking_animation, left_walking_animation, right_walking_animation]
            return outEntity

def create_template(filename, template_type = 'entity'):
    with open(filename, 'w') as f:
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
            json.dump(data, f, indent=True)
        else:
            f.write("Incorrectly specified template...")



if __name__ == "__main__":
    file_directory = input("filename:\n>>> ")
    uIn = input("load or save file?\n>>> ")
    if uIn == "load":
        read_file(file_directory)
    elif uIn == "save":
        template_type = input("template to be generated:\n>>> ")
        create_template(file_directory, template_type)
        print("Created file %s"%file_directory)