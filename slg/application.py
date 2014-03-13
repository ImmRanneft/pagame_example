__author__ = 'Den'

import pygame
from pygame.locals import *

from slg.locals import *
import slg.event


class Application(object):

    _config = None
    _display = None

    _state = GAME_STATE_LOADING
    _run = False

    def __init__(self, config):
        self._config = config
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

        map_name = self._config['MAIN']['map']
        slg.event.LoadMap(map_name).post()

    def running(self):
        return bool(self._run)

    def run(self, run=False):
        self._run = run
        while self.running():
            events = pygame.event.get()
            for e in events:
                if e.type == QUIT:
                    self._run = False
                if e.type == KEYDOWN:
                    if (e.key == K_F4 and pygame.key.get_mods() and pygame.KMOD_ALT) or e.key == K_ESCAPE:
                        self._run = False
                if e.type == EVENT_LOAD_MAP:
                    print(e.map_name)

