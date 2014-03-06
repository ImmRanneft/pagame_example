__author__ = 'Den'

from slg.map.tile import *
from slg.map.layer import *
from slg.map.map import *
from slg.map.locals import *
from slg.map.loader.tmx import *
from slg.renderer import Renderer
from slg.ui import *
import slg.scene
import pygame
from pygame.locals import *
from collections import OrderedDict

PAUSED = 0
RUNNING = 1
LOADING = 2


class Application(object):

    _scenes_to_render = OrderedDict()
    _state = LOADING
    run = False

    def __init__(self, display):
        self.display = display
        self.clock = pygame.time.Clock()

    def push_scene(self, scene: slg.scene.Scene):
        scene.set_app(self)
        length = len(self._scenes_to_render)
        self._scenes_to_render[length] = scene

    def update(self):
        events = pygame.event.get()
        for e in events:
            if e.type == QUIT:
                self.run = False
            if e.type == KEYDOWN:
                if (e.key == K_F4 and pygame.key.get_mods() and pygame.KMOD_ALT) or e.key == K_ESCAPE:
                    self.run = False
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
            key, scene = self._scenes_to_render.popitem(False)
            scene.poll_events(events)
            scene.draw(self.display)

        pygame.display.update()

    def running(self, run=None):
        if run is not None:
            self.run = run
        return self.run

    def set_state(self, state):
        self._state = state

    def get_state(self):
        return self._state