__author__ = 'den'


import threading

import pygame
import pygame.mouse
from pygame.locals import *

import slg.map.loader.tmx
import slg

from slg.renderer import Renderer
from slg.camera import Camera
from slg.scene import Scene
from slg.map.map import Map


class MapScene(Scene):

    _map_surface = None
    image = None
    _world_map = None
    _updated = False
    loading_thread = None
    keyboard_moving_x = keyboard_moving_y = False

    def __init__(self, display: pygame.display, app):
        self.display = display
        display_size = display.get_size()

        super().__init__(display, app)

        self.image = self._map_surface = pygame.Surface(display_size)
        self.rect = self.image.get_rect()

        self.camera = Camera(display_size)
        self.renderer = Renderer(self._map_surface, self.camera)
        self.loader = slg.map.loader.tmx.TmxLoader()

    def set_map(self, map_name):
        self._world_map = Map(map_name, self.renderer, self.loader)
        self.loading_thread = LoadingThread(self._world_map, self._app, self.camera)
        self._app.set_state(slg.LOADING)
        self.loading_thread.start()

    def poll_events(self, events):

        mouse_moving_x = mouse_moving_y = False

        for e in events:
            if self._app.get_state() != slg.PAUSED:
                if e.type == KEYDOWN:
                    if e.key == K_DOWN:
                        self.camera.set_moving_y(self.camera.MOVEMENT_POSITIVE)
                        self.keyboard_moving_y = True
                    if e.key == K_UP:
                        self.camera.set_moving_y(self.camera.MOVEMENT_NEGATIVE)
                        self.keyboard_moving_y = True
                    if e.key == K_RIGHT:
                        self.camera.set_moving_x(self.camera.MOVEMENT_POSITIVE)
                        self.keyboard_moving_x = True
                    if e.key == K_LEFT:
                        self.camera.set_moving_x(self.camera.MOVEMENT_NEGATIVE)
                        self.keyboard_moving_x = True
                if e.type == KEYUP:
                    if e.key == K_UP or e.key == K_DOWN:
                        self.camera.set_moving_y(self.camera.MOVEMENT_STOP)
                        self.keyboard_moving_y = False
                    if e.key == K_LEFT or e.key == K_RIGHT:
                        self.camera.set_moving_x(self.camera.MOVEMENT_STOP)
                        self.keyboard_moving_x = False
                    if e.key == K_c:
                        self.camera.reset_camera_to((self._world_map.get_world_center()))

        keyboard_moving = self.keyboard_moving_x or self.keyboard_moving_y

        if self._app.get_state() == slg.RUNNING and not keyboard_moving:
            vp = self.camera.get_dimensions()
            mouse_pos = pygame.mouse.get_pos()

            padding = (vp[0] + vp[1])/40
            focused = pygame.mouse.get_focused()
            if 0 <= mouse_pos[0] < 0 + padding and focused:
                self.camera.set_moving_x(self.camera.MOVEMENT_NEGATIVE)
                mouse_moving_x = True
            elif vp[0] >= mouse_pos[0] > vp[0] - padding and focused:
                self.camera.set_moving_x(self.camera.MOVEMENT_POSITIVE)
                mouse_moving_x = True
            else:
                self.camera.set_moving_x(self.camera.MOVEMENT_STOP)

            if 0 <= mouse_pos[1] < 0 + padding and focused:
                self.camera.set_moving_y(self.camera.MOVEMENT_NEGATIVE)
                mouse_moving_y = True
            elif vp[1] >= mouse_pos[1] > vp[1] - padding and focused:
                self.camera.set_moving_y(self.camera.MOVEMENT_POSITIVE)
                mouse_moving_y = True
            else:
                self.camera.set_moving_y(self.camera.MOVEMENT_STOP)

        mouse_moving = (mouse_moving_x or mouse_moving_y)

        self.camera.set_mouse_moving(mouse_moving)

    def update(self, surface: pygame.Surface=None):
        if surface is not None:
            self.set_target(surface)
        if self._target is not None:
            visible_area = self.camera.get_bounds()
            self._world_map.draw(visible_area, self._map_surface)
            self.camera.update()
            self._target.blit(self._map_surface, (0, 0))


class LoadingThread(threading.Thread):

    _world_map = None

    def __init__(self, world_map, app, camera):
        threading.Thread.__init__(self)
        self._world_map = world_map
        self._app = app
        self.camera = camera

    def run(self):
        self._world_map.load()
        self.camera.set_dimensions(self._world_map.get_tile_dimensions(), self._world_map.get_map_dimensions())
        self.camera.reset_camera_to((0, 0))
        self._app.set_state(slg.PAUSED)
