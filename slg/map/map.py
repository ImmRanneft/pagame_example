__author__ = 'Den'

from slg.map.tile import Tile
from slg.map.locals import *
import pygame
import random


class Map(object):

    def __init__(self, tile_group, renderer):
        self.__tile_group = tile_group
        self.__renderer = renderer
        self.__world_bounding_left = -int(MAP_WIDTH_IN_TILES / 2)
        self.__world_bounding_right = int(MAP_WIDTH_IN_TILES / 2)
        self.__world_bounding_top = -int(MAP_HEIGHT_IN_TILES / 2)
        self.__world_bounding_bottom = int(MAP_HEIGHT_IN_TILES / 2)

    def generate(self):
        image = pygame.image.load('demo1.png').convert_alpha()
        for j in range(self.__world_bounding_top, self.__world_bounding_bottom):
            for i in range(self.__world_bounding_right, self.__world_bounding_left, -1):
                tilex = TILE_WIDTH*i
                tiley = TILE_HEIGHT*j
                if j % 2 == 1:
                    tilex -= TILE_WIDTH/2
                tiley -= j*48
                offset_x = random.randint(0, 2)
                offset_y = random.randint(0, 2)
                tile = Tile(self.__renderer, image, TILE_WIDTH, TILE_HEIGHT, offset_x, offset_y).coordinates(tilex, tiley)
                rect = pygame.Rect((tile.offset_x() * tile.get_width(), tile.offset_y() * tile.get_height()),
                                   (tile.get_width(), tile.get_height()))
                tile.set_rect(rect)
                self.__tile_group.append(tile, j, i)