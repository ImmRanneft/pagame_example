__author__ = 'Den'

import pygame
from pygame.time import Clock
from pygame.locals import *

import slg.map.map

from slg.locals import *
from slg.event import *
from slg.application.camera import Camera
from slg.application.manager import Manager
from slg.scene.abstractscene import AbstractScene
from slg.scene.mainmenuscene import MainMenuScene


class Application(object):
    """
    @type _config: configparser.ConfigParser
    @type _display: pygame.Surface
    @type _manager: Manager
    @type _scene: AbstractScene
    @type _clock: Clock
    @type _camera: Camera
    @type _run: bool
    @type _state: int
    """

    _config = None
    _display = None
    _manager = None
    _scene = None
    _clock = None
    _camera = None

    _state = GAME_STATE_LOADING
    _run = False

    def __init__(self, config):
        """
        @type config: configparser.ConfigParser
        """
        self._config = config
        self._manager = Manager(self)
        pygame.mixer.init()
        pygame.init()

    def init(self):
        config_display = self._config['DISPLAY']
        display_width = int(config_display.get('width', 800))
        display_height = int(config_display.get('height', 600))
        display_tup = (display_width, display_height)
        pygame.init()

        fullscreen = int(config_display.get('fullscreen', 0))
        display_flags = DOUBLEBUF | HWSURFACE
        if fullscreen == 1:
            display_flags |= FULLSCREEN
            videoinfo = pygame.display.Info()
            # we have to limit our display to FullHD, to use only one monitor untill pygame with SDL > 1.2.14 released
            display_tup = (min(videoinfo.current_w, 1920), min(videoinfo.current_h, 1080))

        self._display = pygame.display.set_mode(display_tup, display_flags)
        self._camera = Camera(self._display.get_size())
        self._clock = Clock()
        self.set_scene(self._manager.get_scene(MainMenuScene))

    def get_display(self):
        return self._display

    def get_camera(self):
        return self._camera

    def set_state(self, state):
        """
        @type state: int
        """
        self._state = state

    def get_state(self):
        return self._state

    def set_scene(self, scene: AbstractScene):
        self._scene = scene

    def running(self):
        return bool(self._run)

    def run(self, run=False):
        self._run = run
        while self.running():
            events = pygame.event.get()
            for e in events:
                if e.type == EVENT_LOAD_MAP:
                    self.map = slg.map.map.Map(self._manager)
                    camera = self._manager.get_camera()
                    map_loading_thread = slg.map.map.MapLoadingThread(e.map_name, self.map, camera)
                    map_loading_thread.start()
                if e.type == QUIT:
                    self._run = False
                if e.type == KEYDOWN:
                    if e.key == K_F4 and pygame.key.get_mods() and pygame.KMOD_ALT:
                        self._run = False
                    if e.key == K_s and pygame.key.get_mods() and pygame.KMOD_ALT:
                        print(self.get_state())
            self._manager.handle(events)
            if self._scene:
                self._scene.handle_events(events)
                self._scene.update()
                self._scene.draw()
                pygame.display.update()
                pygame.display.set_caption("FPS: %.2f" % (self._clock.get_fps())
                           + 'ticks: %.2f' % (self._clock.tick(FPS)))