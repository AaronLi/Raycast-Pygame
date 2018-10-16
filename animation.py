
LOOPING = 0
ONE_WAY = 1
PING_PONG = 2


class Animation:
    def __init__(self, animation_type = LOOPING) -> None:
        self.passed_time = 99999
        self.frames = []
        self.fps = 5
        self.type = animation_type

    def set_frames(self, frames, fps):
        self.frames = frames
        self.fps = fps
        return self

    def start_animation(self):
        self.passed_time = 0

    def update(self, deltatime):
        if not self.animation_done_running():
            self.passed_time += deltatime

    def get_frame(self):

        return self.frames[self.get_current_frame_index()]

    def get_current_frame_index(self):
        if self.type == LOOPING:
            index = int(self.passed_time*self.fps) % len(self.frames)
            return index
        elif self.type == ONE_WAY:
            return min(len(self.frames)-1, int(self.passed_time*self.fps))
        elif self.type == PING_PONG:
            raise NotImplementedError

    def get_total_animation_duration(self):
        '''
        :return: total time in seconds that the animation will take to run
        '''

        return len(self.frames)/self.fps

    def animation_done_running(self):
        if self.type == ONE_WAY:
            return self.passed_time > self.get_total_animation_duration()
        return False