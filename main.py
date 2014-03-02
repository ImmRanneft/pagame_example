#!C:\Python33\python.exe
# -*- coding: utf-8 -*-

import slg
import pygame
import math
import os
import configparser
from slg.map.locals import *
from pygame.locals import *
from slg.map.map import Map
from slg.renderer import Renderer
from slg.map.layer import Layer

BACKGROUND_COLOR = "#004400"


class Camera(object):

    __current_x = __current_y = 0
    __width = __height = 0
    moving_x = moving_y = 0
    __left = __right = __top = __bottom = 0
    __tile_width = __tile_height = 0
    __map_width = __map_height = 0

    __edges = {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}

    MOVEMENT_SPEED = 40
    MOVEMENT_POSITIVE = 1
    MOVEMENT_NEGATIVE = -1
    MOVEMENT_STOP = 0

    def __init__(self, display):
        self.__width = display[0]
        self.__height = display[1]

    def set_dimensions(self, tile_dimensions, map_dimensions):
        self.__tile_width = tile_dimensions[0]
        self.__tile_height = tile_dimensions[1]
        self.__map_width = map_dimensions[0]
        self.__map_height = map_dimensions[1]

        self.__edges['left'] = tile_dimensions[0]/2
        self.__edges['top'] = tile_dimensions[1]/2
        self.__edges['right'] = map_dimensions[0] * tile_dimensions[0] - tile_dimensions[0]/2
        self.__edges['bottom'] = map_dimensions[1] * tile_dimensions[1] / 2 - tile_dimensions[1]/2

    def set_moving_x(self, movement):
        self.moving_x = movement

    def set_moving_y(self, movement):
        self.moving_y = movement

    def reset_camera_to(self, coordinates):
        if coordinates[0] is not False:
            self.__current_x = coordinates[0] * self.__tile_width - self.__width / 2
        if coordinates[1] is not False:
            self.__current_y = coordinates[1] * self.__tile_height / 2  - 3 / 2 * self.__height

    def get_dest(self):
        return self.__current_x, self.__current_y

    def get_dimensions(self):
        return self.__width, self.__height

    def update(self):
        self.__current_x += self.moving_x * self.MOVEMENT_SPEED
        if self.__current_x < self.__edges['left'] - 200:
            self.__current_x = self.__tile_width
        if self.__current_x + self.__width > self.__edges['right']:
            self.__current_x = self.__edges['right'] - self.__width - self.__tile_width / 2
        self.__current_y += self.moving_y * self.MOVEMENT_SPEED
        if self.__current_y < self.__edges['top'] - 200:
            self.__current_y = self.__tile_height
        if self.__current_y + self.__height > self.__edges['bottom']:
            self.__current_y = self.__edges['bottom'] - self.__height - self.__tile_height / 2

    def get_bounds(self):
        left = math.floor(self.__current_x / self.__tile_width - 1)
        left = left if 0 < left else 0
        right = math.ceil((self.__current_x + self.__width) / self.__tile_width + 1)
        right = right if right < self.__map_width else self.__map_width
        top = math.floor(self.__current_y / self.__tile_height - 1)
        top = top if 0 < top else 0
        bottom = math.ceil((self.__current_y + self.__height) / (self.__tile_height / 2) + 1)
        bottom = bottom if bottom < self.__map_height else self.__map_height

        return left, right, top, bottom


def main():
    config = configparser.ConfigParser()
    config.sections()
    config.read(os.path.join(os.getcwd(), "config", "main.ini"))
    l_map = config['MAIN']['map']
    config_display = config['DISPLAY']
    display_width = int(config_display.get('width', 800))
    display_height = int(config_display.get('height', 600))

    pygame.init()
    # videoinfo = pygame.display.Info()
    display_tup = (display_width, display_height)

    display = pygame.display.set_mode(display_tup)

    clr = (0, 0, 0)
    clock = pygame.time.Clock()

    camera = Camera(display_tup)
    renderer = Renderer(display, camera)

    loader = slg.map.loader.tmx.TmxLoader()

    l_map = os.path.realpath(os.path.join(os.getcwd(), "data", "maps", l_map))
    world_map = Map(l_map, renderer, loader)

    camera.set_dimensions(world_map.get_tile_dimensions(), world_map.get_map_dimensions())
    camera.reset_camera_to((world_map.get_world_center()))

    running = True

    while running:
        for e in pygame.event.get():
            if e.type == KEYDOWN:
                if (e.key == K_F4 and pygame.key.get_mods() and pygame.KMOD_ALT) or e.key == K_ESCAPE:
                    running = False
                if e.key == K_DOWN:
                    camera.set_moving_y(camera.MOVEMENT_POSITIVE)
                if e.key == K_UP:
                    camera.set_moving_y(camera.MOVEMENT_NEGATIVE)
                if e.key == K_RIGHT:
                    camera.set_moving_x(camera.MOVEMENT_POSITIVE)
                if e.key == K_LEFT:
                    camera.set_moving_x(camera.MOVEMENT_NEGATIVE)
            if e.type == KEYUP:
                if e.key == K_UP or e.key == K_DOWN:
                    camera.set_moving_y(camera.MOVEMENT_STOP)
                if e.key == K_LEFT or e.key == K_RIGHT:
                    camera.set_moving_x(camera.MOVEMENT_STOP)
                # if e.key == K_c:
                #     zz = layer.get([0, 0])
                #     camera.reset_camera_to((zz.get_x(), zz.get_y()))

        camera.update()
        display.fill(clr)
        visible_area = camera.get_bounds()
        world_map.draw(visible_area)

        pygame.display.update()
        clock.tick(30)
        # running = False

if __name__ == "__main__":
    main()