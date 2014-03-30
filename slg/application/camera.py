__author__ = 'Den'

import math

import pygame.mouse
import pygame.rect

from slg.locals import *


class Camera(object):

    __current_x = __current_y = 0
    coordinates = [0, 0]
    __width = __height = 0
    __width_in_tiles = __height_in_tiles = 0

    _renderer = None

    __tile_width, __tile_height = 64, 32

    __map_width = __map_height = 0
    _virtual_map_width = _virtual_map_height = 0

    __edges = {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}

    (DEFAULT_MOVEMENT_SPEED, ) = (0.4, )
    moving_x = moving_y = 0
    movement_speed = 0.4
    mouse_moving = False
    keyboard_moving_x, keyboard_moving_y = False, False
    (MOVEMENT_POSITIVE, MOVEMENT_NEGATIVE, MOVEMENT_STOP) = (1, -1, 0)

    def __init__(self, display):
        [self.__width, self.__height] = display

    def set_renderer(self, renderer):
        self._renderer = renderer
        self._renderer.set_camera(self)

    def set_dimensions(self, tile_dimensions, map_dimensions):
        [self.__tile_width, self.__tile_height] = self._renderer.calculate_tile_dimensions(tile_dimensions)
        [self.__map_width, self.__map_height] = map_dimensions

        if self.__map_width < self.__width / self.__tile_width:
            self._virtual_map_width = int(self.__width / self.__tile_width) + 1
        else:
            self._virtual_map_width = self.__map_width

        if self.__map_height < self.__height / self.__tile_height:
            self._virtual_map_height = int(self.__height / self.__tile_height) + 1
        else:
            self._virtual_map_height = self.__map_height

        self.__width_in_tiles = self.__width / self.__tile_width
        self.__height_in_tiles = self.__height / self.__tile_height  # it`s isometric world, babe!

        self.movement_speed = ((self.__tile_width+self.__tile_height)/(FPS/TPS*2))

        self.__edges['left'] = -self.__map_width / 2
        self.__edges['top'] = 0
        self.__edges['right'] = self.__map_width / 2
        self.__edges['bottom'] = self._virtual_map_height

    def m_speed(self):
        if self.mouse_moving:
            return self.movement_speed / 2
        else:
            return self.movement_speed

    def set_mouse_moving(self, mouse_moving):
        self.mouse_moving = bool(mouse_moving)

    def set_moving_x(self, movement):
        self.moving_x = movement

    def set_moving_y(self, movement):
        self.moving_y = movement

    def get_dest(self):
        return self.__current_x, self.__current_y

    def get_dimensions(self):
        return self.__width, self.__height

    def update(self):
        if self.moving_x or self.moving_y:

            # self.coordinates[0] += self.moving_x * self.m_speed()
            # if self.coordinates[0] - self.m_speed() < self.__edges['left']:
            #     print(self.coordinates)
            #     self.coordinates[0] = self.__edges['left']
            # elif self.coordinates[0] + self.__width_in_tiles + self.m_speed() > self.__edges['right']:
            #     print(self.coordinates)
            #     self.coordinates[0] = self.__edges['right']
            #
            # self.coordinates[1] += self.moving_y * self.m_speed()
            # if self.coordinates[1] - self.m_speed() < self.__edges['top']:
            #     self.coordinates[1] = self.__edges['top']
            # elif self.coordinates[1] + self.__height_in_tiles + self.m_speed() > self.__edges['bottom']:
            #     self.coordinates[1] = self.__edges['bottom']

            self.__current_x += self.m_speed() * self.moving_x * self.__tile_width
            if self.__current_x < -self.__map_width * self.__tile_width / 2 + self.__tile_width / 2:
                self.__current_x = -self.__map_width * self.__tile_width / 2 + self.__tile_width / 2
            elif self.__current_x + self.__width > self.__map_width * self.__tile_width / 2 + self.__tile_width / 2:
                self.__current_x = self.__map_width * self.__tile_width / 2 - self.__width + self.__tile_width / 2
            self.__current_y += self.m_speed() * self.moving_y * self.__tile_height
            if self.__current_y < 0:
                self.__current_y = 0
            elif self.__current_y + self.__height > self.__map_height * self.__tile_height:
                self.__current_y = self.__map_height * self.__tile_height - self.__height

    def get_bounds(self):
        topleft = (self.__current_x, self.__current_y)
        topright = (self.__current_x + self.__width, self.__current_y)
        bottomleft = (self.__current_x, self.__current_y + self.__height)
        bottomright = (self.__current_x + self.__width, self.__current_y + self.__height)

        td = [self.__tile_width, self.__tile_height]
        # map half width in tiles
        mhwt = self.__map_width / 2
        # map half height in tiles
        mhht = self.__map_height / 2



        left = math.ceil(topleft[0]/td[0] + topleft[1]/td[1] - 2)
        right = math.ceil(bottomright[0]/td[0] + bottomright[1]/td[1] + 2)
        top = math.ceil((topright[1]/td[1] - topright[0]/td[0] - 2))
        bottom = math.ceil((bottomleft[1]/td[1] - bottomleft[0]/td[0] + 2))

        left = left if left > 0 else 0
        right = right if right < self.__map_width else self.__map_width
        top = top if top > 0 else 0
        bottom = bottom if bottom < self.__map_height else self.__map_height

        ret = {'left': left, 'right': right, 'top': top, 'bottom': bottom}
        return ret

    def set_movement_speed(self, movement_speed=DEFAULT_MOVEMENT_SPEED):
        self.movement_speed = movement_speed

    def handle_events(self, events, manager):
        for e in events:
            if manager.state != GAME_STATE_PAUSED:
                if e.type == KEYDOWN:
                    if e.key == K_DOWN:
                        self.set_moving_y(self.MOVEMENT_POSITIVE*2)
                        self.keyboard_moving_y = True
                    if e.key == K_UP:
                        self.set_moving_y(self.MOVEMENT_NEGATIVE*2)
                        self.keyboard_moving_y = True
                    if e.key == K_RIGHT:
                        self.set_moving_x(self.MOVEMENT_POSITIVE)
                        self.keyboard_moving_x = True
                    if e.key == K_LEFT:
                        self.set_moving_x(self.MOVEMENT_NEGATIVE)
                        self.keyboard_moving_x = True
                if e.type == KEYUP:
                    if e.key == K_UP or e.key == K_DOWN:
                        self.set_moving_y(self.MOVEMENT_STOP)
                        self.keyboard_moving_y = False
                    if e.key == K_LEFT or e.key == K_RIGHT:
                        self.set_moving_x(self.MOVEMENT_STOP)
                        self.keyboard_moving_x = False

        keyboard_moving = self.keyboard_moving_x or self.keyboard_moving_y

        mouse_moving_x, mouse_moving_y = False, False
        if manager.state == GAME_STATE_RUNNING and not keyboard_moving:
            vp = self.get_dimensions()
            mouse_pos = pygame.mouse.get_pos()

            padding = (vp[0] + vp[1])/40
            focused = pygame.mouse.get_focused()
            if 0 <= mouse_pos[0] < 0 + padding and focused:
                self.set_moving_x(self.MOVEMENT_NEGATIVE)
                mouse_moving_x = True
            elif vp[0] >= mouse_pos[0] > vp[0] - padding and focused:
                self.set_moving_x(self.MOVEMENT_POSITIVE)
                mouse_moving_x = True
            else:
                self.set_moving_x(self.MOVEMENT_STOP)

            if 0 <= mouse_pos[1] < 0 + padding and focused:
                self.set_moving_y(self.MOVEMENT_NEGATIVE*2)
                mouse_moving_y = True
            elif vp[1] >= mouse_pos[1] > vp[1] - padding and focused:
                self.set_moving_y(self.MOVEMENT_POSITIVE*2)
                mouse_moving_y = True
            else:
                self.set_moving_y(self.MOVEMENT_STOP)

        mouse_moving = (mouse_moving_x or mouse_moving_y)

        self.set_mouse_moving(mouse_moving)
        self.set_movement_speed()
