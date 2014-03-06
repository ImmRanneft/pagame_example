__author__ = 'Den'

from slg.map.tile import *
from slg.map.layer import *
from slg.map.map import *
from slg.map.locals import *
from slg.map.loader.tmx import *
from slg.renderer import Renderer
from slg.ui import *
import slg.scene
import slg.scene.manager
import pygame
from pygame.locals import *
from collections import OrderedDict

PAUSED = 0
RUNNING = 1
LOADING = 2


class Application(object):

    _scenes_to_render = OrderedDict()
    _state = LOADING
    _run = False
    _manager = display = None

    def __init__(self, config):
        self.config = config
        self.clock = pygame.time.Clock()

    def init(self):
        music = os.path.join(os.getcwd(), "data", 'sound', "tristram.mp3")
        # display config
        config_display = self.config['DISPLAY']
        display_width = int(config_display.get('width', 800))
        display_height = int(config_display.get('height', 600))
        display_tup = (display_width, display_height)

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(music)
        # pygame.mixer.music.play()

        fullscreen = int(config_display.get('fullscreen', 0))
        display_flags = DOUBLEBUF | HWSURFACE
        if fullscreen == 1:
            display_flags |= FULLSCREEN
            videoinfo = pygame.display.Info()
            # we have to limit our display to FullHD, to use only one monitor untill pygame with SDL > 1.2.14 released
            display_tup = (min(videoinfo.current_w, 1920), min(videoinfo.current_h, 1080))

        display = pygame.display.set_mode(display_tup, display_flags)
        self.display = display
        self._manager = slg.scene.manager.Manager(self)

    def push_scene(self, scene: slg.scene.Scene):
        scene.set_app(self)
        length = len(self._scenes_to_render)
        self._scenes_to_render[length] = scene

    def update(self):
        events = pygame.event.get()
        for e in events:
            if e.type == QUIT:
                self._run = False
            if e.type == KEYDOWN:
                if (e.key == K_F4 and pygame.key.get_mods() and pygame.KMOD_ALT) or e.key == K_ESCAPE:
                    self._run = False
            if e.type == KEYUP:
                if e.key == K_p:
                    if self.get_state() == PAUSED:
                        self.set_state(RUNNING)
                        print('running')
                    else:
                        self.set_state(PAUSED)
                        print('paused')

        while self._scenes_to_render:
            # we use FIFO style
            key, scene_to_render = self._scenes_to_render.popitem(False)
            scene_to_render.poll_events(events)
            scene_to_render.update()

        pygame.display.update()

    def running(self, run=None):
        if run is not None:
            self._run = run
        return self._run

    def set_state(self, state):
        self._state = state

    def get_state(self):
        return self._state

    def run(self):
        while self.running():
            self.display.fill((0, 0, 0))
            self._manager.update()
            self.update()
            pygame.display.update()
            self.clock.tick(60)