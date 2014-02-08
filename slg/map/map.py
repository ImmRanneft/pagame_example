__author__ = 'Den'

from slg.map.tile import Tile
from slg.map.locals import *
import pygame
import random


class Map(object):

    def __init__(self, tile_group, renderer):
        self.__tile_group = tile_group
        self.__renderer = renderer
        self.__world_center_x = 0  # int(float(WORLD_WIDTH / 2))
        self.__world_center_y = 0  # int(float(WORLD_HEIGHT / 2))
        self.__world_bounding_left, self.__world_bounding_right = -int(float(MAP_WIDTH_IN_TILES / 2)), int(float(MAP_WIDTH_IN_TILES / 2))
        self.__world_bounding_top, self.__world_bounding_bottom = -int(float(MAP_HEIGHT_IN_TILES / 2)), int(float(MAP_HEIGHT_IN_TILES / 2))
        print(self.__world_bounding_left, self.__world_bounding_right)

    def generate(self):
        image = pygame.image.load('demo1.png').convert_alpha()
        for j in range(self.__world_bounding_left, self.__world_bounding_right):
            for i in range(self.__world_bounding_top, self.__world_bounding_bottom, -1):
                tilex = TILE_WIDTH*i
                tiley = TILE_HEIGHT*j
                if j % 2 == 1:
                    tilex -= TILE_WIDTH/2
                tiley -= j*48
                offset_x = random.randint(0, 2)
                offset_y = random.randint(0, 2)
                tile = Tile(self.__renderer, image, TILE_WIDTH, TILE_HEIGHT, offset_x, offset_y).coordinates(tilex, tiley)
                self.__tile_group.append(tile)

    def get_world_center(self):
        return self.__world_center_x, self.__world_center_y

    def get_world_bounding_box(self):
        return self.__world_bounding_left * TILE_WIDTH, \
               self.__world_bounding_right * TILE_WIDTH, \
               self.__world_bounding_top * TILE_HEIGHT * 3 / 4, \
               self.__world_bounding_bottom * TILE_HEIGHT * 3 / 4