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
from slg.map import TileGroup

BACKGROUND_COLOR = "#004400"


class Camera(object):

    __current_x = __current_y = 0
    __width = __height = 0
    moving_x = moving_y = 0
    __left = __right = __top = __bottom = 0
    __tile_width = __tile_height = 0
    __map_width = __map_height = 0

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

    def set_moving_x(self, movement):
        self.moving_x = movement

    def set_moving_y(self, movement):
        self.moving_y = movement

    def reset_camera_to(self, coordinates):
        if coordinates[0] is not False:
            self.__current_x = coordinates[0] # - self.__width / 2
        if coordinates[1] is not False:
            self.__current_y = coordinates[1] # c- self.__height / 2

    def get_dest(self):
        return self.__current_x, self.__current_y

    def get_dimensions(self):
        return self.__width, self.__height

    def update(self):
        self.__current_x += self.moving_x * self.MOVEMENT_SPEED
        self.__current_y += self.moving_y * self.MOVEMENT_SPEED

    def get_bounds(self):
        left = math.floor(self.__current_x / self.__tile_width - 1)
        right = math.ceil((self.__current_x + self.__width) / self.__tile_width + 1)

        top = math.floor(self.__current_y / self.__tile_height * 4 - 2)
        bottom = math.ceil((self.__current_y + self.__height) / self.__tile_height * 4 + 2)

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
    tile_group = TileGroup()
    loader = slg.map.loader.tmx.TmxLoader()
    l_map = os.path.realpath(os.path.join(os.getcwd(), "data", "maps", l_map))
    world_map = Map(l_map, tile_group, renderer, loader)
    tile_group.set_world_width(world_map.get_map_dimensions())
    camera.set_dimensions(world_map.get_tile_dimensions(), world_map.get_map_dimensions())
    # worldmap.draw()

    # worldmap.generate()
    camera.reset_camera_to((world_map.get_world_center()))
    #
    # tile_group.draw()
    #
    # # camera.reset_camera_to(tile_group.get(1).get_x(), tile_group.get(1).get_y())
    #
    running = True
    #

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
                if e.key == K_c:
                    zz = tile_group.get((0, 0))
                    camera.reset_camera_to((zz.get_x(), zz.get_y()))

        camera.update()
        display.fill(clr)
        world_map.draw()
        left, right, top, bottom = camera.get_bounds()
        tile_group.set_area(left, right, top, bottom)

        pygame.display.update()
        clock.tick(30)
        # running = False

if __name__ == "__main__":
    main()