__author__ = "Den"

import os.path

import pygame
import pygame.sprite
import pygame.rect
from pygame.locals import *

import slg.application.camera
import slg.renderer.staggered

from slg.locals import *


class Player(pygame.sprite.Sprite):

    """
    @type: slg.renderer.Renderer
    """
    _camera = _renderer = None
    x, y = 2, 2
    movement_speed = 0.1  # 0.05
    moving_x = moving_y = 0
    _map_object = None
    directions = {
        'west': 0,
        'northwest': 1,
        'north': 2,
        'northeast': 3,
        'east': 4,
        'southeast': 5,
        'south': 6,
        'southwest': 7,
    }


    @staticmethod
    def get_id():
        return 999999

    def __init__(self, *groups):
        super().__init__(*groups)
        image = pygame.image.load(os.path.join(DATA_DIR, 'monsters', 'zombie.png'))
        image.convert_alpha()
        self.image = pygame.Surface((128, 128), SRCALPHA | HWSURFACE)
        self.image.blit(image, (0, 0), (0, 0, 128, 128))
        self.rect = pygame.rect.Rect((0, 0), self.image.get_size())

    def set_map(self, map_object):
        self._map_object = map_object

    def set_camera(self, camera):
        self._camera = camera

    def set_renderer(self, renderer):
        self._renderer = renderer
        # self.movement_speed = camera.movement_speed / 50

    def render(self):
        camera_x, camera_y = self._camera.get_dest()
        camera_dim = self._camera.get_dimensions()
        renderer = self._map_object.get_renderer()
        map_dimensions = renderer.get_layer_surface_dimensions(self._map_object.get_map_dimensions(),
                                              self._map_object.get_tile_dimensions())
        newrect = renderer.map_to_screen(self)
        newrect.x -= camera_x
        newrect.x += map_dimensions[0] / 2
        newrect.y -= camera_y
        # print(newrect, self.x, self.y)
        self.rect = newrect

    def update(self):
        self.x += self.moving_x * self.movement_speed
        self.y += self.moving_y * self.movement_speed
        # camera_bounds = self._camera.get_bounds()
        # if self.moving_x or self.moving_y:
            # dx = (self.moving_x * self.movement_speed)
            # dy = (self.moving_y * self.movement_speed)
            # print('char dy ', dy)
            # if not(camera_bounds['left'] + 2 < self.x) and self.moving_x == self._camera.MOVEMENT_NEGATIVE:
            #     self._camera.set_moving_x(self._camera.MOVEMENT_NEGATIVE)
            #     self._camera.set_movement_speed(self.movement_speed)
            #     # self._camera.update()
            # if not(camera_bounds['right'] - 2 > self.x + self.get_dimensions()[0] / self.get_regular_tile_dimensions()[0]) \
            #         and self.moving_x == self._camera.MOVEMENT_POSITIVE:
            #     self._camera.set_moving_x(self._camera.MOVEMENT_POSITIVE)
            #     self._camera.set_movement_speed(self.movement_speed)
            #     self._camera.update()
            # if not(camera_bounds['top'] + 2 < self.y) and self.moving_y == self._camera.MOVEMENT_NEGATIVE:
            #     self._camera.set_moving_y(self._camera.MOVEMENT_NEGATIVE)
            #     self._camera.set_movement_speed(self.movement_speed)
            #     self._camera.update()
            # if not(camera_bounds['bottom'] - 2 > self.y + self.get_dimensions()[1] / self.get_regular_tile_dimensions()[1] * 2) \
            #         and self.moving_y == self._camera.MOVEMENT_POSITIVE:
            #     self._camera.set_moving_y(self._camera.MOVEMENT_POSITIVE)
            #     self._camera.set_movement_speed(self.movement_speed)
            #     self._camera.update()
        self.render()


    def get_regular_tile_dimensions(self):
        return (64, 32)

    def get_dimensions(self):
        return self.image.get_size()

    @staticmethod
    def get_offset():
        return (0, 0)

    def get_coordinates(self):
        x = self.x
        y = self.y
        return [x, y]

    def set_moving_x(self, movement):
        self.moving_x = movement

    def set_moving_y(self, movement):
        self.moving_y = movement
