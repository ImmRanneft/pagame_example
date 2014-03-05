__author__ = 'den'


import pygame
import slg.map.loader.tmx
from slg.renderer import Renderer
from slg.camera import Camera
from slg.scene.scene import Scene
from slg.scene.loadingscene import LoadingScene
from slg.map.map import Map
from slg import RUNNING, PAUSED, LOADING
from pygame.locals import *
import threading

class MapScene(Scene):

    _map_surface = None
    _world_map = None
    _updated = False
    loading = False

    def __init__(self, display: pygame.display, app):
        self.display = display
        display_size = display.get_size()

        super().__init__(display_size, app)

        self._map_surface = pygame.Surface(display_size)
        self.camera = Camera(display_size)
        self.renderer = Renderer(self._map_surface, self.camera)
        self.loader = slg.map.loader.tmx.TmxLoader()

    def set_map(self, map_name):
        self._world_map = Map(map_name, self.renderer, self.loader)
        self.loading = True
        self._app.set_state(LOADING)
        self.loading_thread = threading.Thread(self._world_map.load(self._app))
        self.loading_thread.start()
        self.camera.set_dimensions(self._world_map.get_tile_dimensions(), self._world_map.get_map_dimensions())
        self.camera.reset_camera_to((0, 0))

    def poll_events(self, events):
        for e in events:
            if self._app.get_state() != PAUSED:
                if e.type == KEYDOWN:
                    if e.key == K_DOWN:
                        self.camera.set_moving_y(self.camera.MOVEMENT_POSITIVE)
                    if e.key == K_UP:
                        self.camera.set_moving_y(self.camera.MOVEMENT_NEGATIVE)
                    if e.key == K_RIGHT:
                        self.camera.set_moving_x(self.camera.MOVEMENT_POSITIVE)
                    if e.key == K_LEFT:
                        self.camera.set_moving_x(self.camera.MOVEMENT_NEGATIVE)
                if e.type == KEYUP:
                    if e.key == K_UP or e.key == K_DOWN:
                        self.camera.set_moving_y(self.camera.MOVEMENT_STOP)
                    if e.key == K_LEFT or e.key == K_RIGHT:
                        self.camera.set_moving_x(self.camera.MOVEMENT_STOP)
                    if e.key == K_c:
                        self.camera.reset_camera_to((self._world_map.get_world_center()))

    def draw(self, surface: pygame.Surface=None):
        if surface is not None:
            self.set_target(surface)
        if self._target is not None:
            if self.loading and self.loading_thread.isAlive():
                self._app.set_state(LOADING)
            else:
                self.loading = False
                self._app.set_state(PAUSED)
                visible_area = self.camera.get_bounds()
                self._world_map.draw(visible_area)
                self.camera.update()
                self._target.blit(self._map_surface, (0, 0))

