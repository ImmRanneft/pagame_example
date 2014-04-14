__author__ = "Den"

import os.path
import math

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

    movement_speed = 0.1  # 0.05
    moving_x = moving_y = 0
    _map_object = None
    directions = {
        K_a & K_s: 'west',
        K_a: 'northwest',
        K_a & K_w: 'north',
        K_w: 'northeast',
        K_w & K_d: 'east',
        K_d: 'southeast',
        K_s & K_d: 'south',
        K_s: 'southwest',
    }

    @staticmethod
    def get_id():
        return 999999

    def __init__(self, *groups):
        super().__init__(*groups)
        self.manager = None
        self.direction = 'west'
        self.x, self.y = 0, 13
        self.next_x = self.x
        self.next_y = self.y
        self.moving_x_key = 0
        self.moving_y_key = 0

        image = pygame.image.load(os.path.join(DATA_DIR, 'monsters', 'zombie.png'))
        image.convert_alpha()
        self.image = pygame.Surface((128, 128), SRCALPHA | HWSURFACE)
        # self.cl = pygame.Surface((32, 64), SRCALPHA | HWSURFACE)
        # self.cl.fill((255, 0, 0, 128))
        # self.image.blit(self.cl, (48, 40))
        self.image.blit(image, (0, 0), (0, 0, 128, 128))

        self.rect = pygame.rect.Rect((0, 0), self.image.get_size())
        self.base_rect = pygame.rect.Rect((0, 0), self.image.get_size())

        self._manager = None
        self.z = 0
        self._layer = self.x + self.y + self.z

    def set_manager(self, manager):
        self._manager = manager
        self._camera = self._manager.get_camera()

    def set_map(self, map_object):
        self._map_object = map_object
        self.z = self._map_object.object_layer
        self._layer = self.x + self.y + self.z
        self._map_object.add(self)
        self._map_object.change_layer(self, self._layer)
        self._renderer = self._map_object.get_renderer()

    def render(self):
        renderer = self._map_object.get_renderer()
        self.base_rect = renderer.map_to_screen(self)
        self.rect = renderer.adjust_with_cam(self.base_rect)

    def update(self):
        if self.moving_x != self._camera.MOVEMENT_STOP or self.moving_y != self._camera.MOVEMENT_STOP:
            self.next_x = self.x + self.moving_x * self.movement_speed
            self.next_y = self.y + self.moving_y * self.movement_speed
            if self.can_move():
                self.x = self.next_x
                self.y = self.next_y
                self._layer = self.x + self.y + 3  # same as object layer
                self._map_object.change_layer(self, self._layer)
        self.render()
        self.update_camera()

    def can_move(self):
        # origin diamond size is 32 x 16 so it`s +0.5 both coordinates
        ceil_coordinates = math.ceil(self.next_x), math.ceil(self.next_y)
        floor_coordinates = math.floor(self.next_x+0.5), math.floor(self.next_y+0.5)
        # print(bool(self._manager.check_collide(ceil_coordinates[0], ceil_coordinates[1])), bool(self._manager.check_collide(floor_coordinates[0], floor_coordinates[1])))
        return not(bool(self._map_object.check_collide(ceil_coordinates[0], ceil_coordinates[1])) or bool(self._map_object.check_collide(floor_coordinates[0], floor_coordinates[1])))

    def __repr__(self):
        return self.rect.__repr__() + "\r\n" + \
            self.base_rect.__repr__() + "\r\n" +\
            str(self.x) + ' ' +\
            str(self.y) + " " + \
            str(self._layer) + " " + \
            self.direction

    def handle_events(self, events):
        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_p:
                    print(self)
                if e.key == K_c:
                    print(self._camera.get_dest(), self.rect.x, self.rect.y)
                if e.key == K_t and (pygame.key.get_mods() & KMOD_ALT) and (pygame.key.get_mods() & KMOD_SHIFT):
                    self.x = 0
                    self.y = 0
                    break
            if self._manager.state != GAME_STATE_PAUSED:
                if e.type == KEYDOWN:
                    if e.key == K_s:
                        self.set_moving_y(self._camera.MOVEMENT_POSITIVE)
                        self.moving_y_key = K_s
                    if e.key == K_w:
                        self.set_moving_y(self._camera.MOVEMENT_NEGATIVE)
                        self.moving_y_key = K_w
                    if e.key == K_d:
                        self.set_moving_x(self._camera.MOVEMENT_POSITIVE)
                        self.moving_x_key = K_d
                    if e.key == K_a:
                        self.set_moving_x(self._camera.MOVEMENT_NEGATIVE)
                        self.moving_x_key = K_a
                if e.type == KEYUP:
                    if (e.key == K_w or e.key == K_s) and e.key == self.moving_y_key:
                        self.set_moving_y(self._camera.MOVEMENT_STOP)
                    if (e.key == K_a or e.key == K_d) and e.key == self.moving_x_key:
                        self.set_moving_x(self._camera.MOVEMENT_STOP)
                self.direction = self.directions.get(self.moving_x_key & self.moving_y_key, 'west')

    def update_camera(self):
        if self.moving_x != self._camera.MOVEMENT_STOP or self.moving_y != self._camera.MOVEMENT_STOP:
            camera_dim = self._camera.get_dimensions()
            edge_offset = (camera_dim[0] + camera_dim[1]) / 20
            if self.rect.left < 0 + edge_offset and (self.moving_y == self._camera.MOVEMENT_POSITIVE
                                                     or self.moving_x == self._camera.MOVEMENT_NEGATIVE):
                self._camera.set_moving_x(self._camera.MOVEMENT_NEGATIVE)
                self._camera.set_movement_speed(self.movement_speed)
                self._camera.update()
            if self.rect.right > camera_dim[0] - edge_offset and (self.moving_y == self._camera.MOVEMENT_NEGATIVE
                                                                  or self.moving_x == self._camera.MOVEMENT_POSITIVE):
                self._camera.set_moving_x(self._camera.MOVEMENT_POSITIVE)
                self._camera.set_movement_speed(self.movement_speed)
                self._camera.update()
            if self.rect.top < 0 + edge_offset and self.moving_y == self._camera.MOVEMENT_NEGATIVE:
                self._camera.set_moving_y(self._camera.MOVEMENT_NEGATIVE)
                self._camera.set_movement_speed(self.movement_speed)
                self._camera.update()
            if self.rect.bottom > camera_dim[1] - edge_offset and self.moving_y == self._camera.MOVEMENT_POSITIVE:
                self._camera.set_moving_y(self._camera.MOVEMENT_POSITIVE)
                self._camera.set_movement_speed(self.movement_speed)
                self._camera.update()

    def get_regular_tile_dimensions(self):
        return self._map_object.get_tile_dimensions()

    def get_dimensions(self):
        return self.image.get_size()

    @staticmethod
    def get_offset():
        return (32, 16)

    def get_coordinates(self):
        x = self.x
        y = self.y
        return [x, y]

    def set_moving_x(self, movement):
        self.moving_x = movement

    def set_moving_y(self, movement):
        self.moving_y = movement