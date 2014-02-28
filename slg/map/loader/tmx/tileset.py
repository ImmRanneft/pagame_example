__author__ = 'Den'

import pygame
import os
from slg.map.locals import *
from slg.map.loader.tmx.tile import Tile


class Tileset(object):

    """
    @param __image - loaded by pygame image surface
    """
    __image = None

    __firstgid = 0
    __lastgid = 0
    __name = "undefined"

    __offset_x = __offset_y = 0
    __image_width = __image_height = 0
    __tile_width = __tile_height = 0
    __tile_storage = list()

    def __init__(self, firstgid, name, identificator):
        self.__firstgid = int(firstgid)
        self.__name = name
        self.__id = identificator

    def set_image(self, image, image_width, image_height):
        self.__image = pygame.image.load(image).convert_alpha()
        self.__image_width = image_width
        self.__image_height = image_height

    def set_offset(self, offset_x, offset_y):
        self.__offset_x, self.__offset_y = offset_x, offset_y

    def set_tile_dimensions(self, tile_width, tile_height):
        self.__tile_width, self.__tile_height = tile_width, tile_height

    def get_tile_dimensions(self):
        return [self.__tile_width, self.__tile_height]

    def get_offsets(self):
        return [self.__offset_x, self.__offset_y]

    def get_image(self):
        return self.__image

    def initiate(self):
        tiles_in_row = int(self.__image_width / self.__tile_width)
        tiles_in_col = int(self.__image_height / self.__tile_height)
        self.__lastgid = self.__firstgid - 1 + int(tiles_in_row * tiles_in_col)
        """
            this would be mush pleasent to create tiles object (or maybe create it on lasy load?)
            and in load_tile only clone already existing objects and set them coordinates only,
            perhaps it will increase performance, cause we do not need to calculate different values in Tile class
            so we have to slice an image and create propper quantity of tiles in tileset storage.
            so right here we can calculate the rectangle for tile
        """
        for tile_row in range(1, tiles_in_row):
            for tile_col in range(1, tiles_in_col):
                tilex = tile_row
                tiley = tile_col
                gid = tile_row + tile_col - 1

                tile = Tile(gid)
                tile.set_tileset(self)
                self.__tile_storage.insert(gid, tile)

        # self.slice_an_image_on_tiles()
        # print(self.__tile_height, self.__tile_width, self.__firstgid, self.__lastgid)

    def get_tile_template(self, tile_gid):
        return self.__tile_storage[tile_gid]

    def get_bounds(self):
        return self.__firstgid, self.__lastgid

    def get_id(self):
        return self.__id