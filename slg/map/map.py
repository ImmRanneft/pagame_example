__author__ = 'Den'

from slg.map.tile import Tile
from slg.map.locals import *
import pygame
import random

class Map(object):

    __layer = __renderer = __loader = None
    __layers = list()

    __world_bounding_left = __world_bounding_right = 0
    __world_bounding_top = __world_bounding_bottom = 0
    __world_center_x = __world_center_y = 0

    def __init__(self, l_map, renderer, loader):
        self.__loader = loader
        self.__renderer = renderer
        self.l_map = l_map

    def load(self):
        self.__loader.load(self.l_map)
        [self.__world_center_x, self.__world_center_y] = self.__loader.get_map_dimensions()
        self.__world_center_x /= 2
        self.__world_center_y /= 2

        for layer in self.__loader.get_layers():
            layer.set_renderer(self.__renderer)
            self.__layers.append(layer)

        for tile in self.__loader.get_tiles():
            [x, y] = tile.get_coordinates()
            self.__layer.append(tile, x, y)

    def get_world_center(self):
        return self.__world_center_x, self.__world_center_y

    def draw(self, visible_area):
        for layer in self.get_layers():
            layer.set_visible_area(visible_area)
            layer.draw()

    def get_layers(self):
        return self.__layers

    def get_tile_dimensions(self):
        return self.__loader.get_tile_dimensions()

    def get_map_dimensions(self):
        return self.__loader.get_map_dimensions()