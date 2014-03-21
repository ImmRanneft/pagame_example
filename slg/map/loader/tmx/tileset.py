__author__ = 'Den'

import pygame
import pygame.rect
from pygame.locals import *
from slg.map.loader.tmx.tile import Tile


class Tileset(object):

    """
    @type __image: pygame.Surface - loaded by pygame image surface
    @type __first_gid: int
    """
    __image = None

    __first_gid = 0
    __last_gid = 0
    __name = "undefined"

    __offset_x = __offset_y = 0
    __image_width = __image_height = 0
    __tile_width = __tile_height = 0
    __tile_storage = dict()
    __tiles_in_row, __tiles_in_col = 0, 0

    def __init__(self, firstgid, name, identificator, loader):
        self.__loader = loader
        self.__first_gid = int(firstgid)
        self.__name = name
        self.__id = identificator

    def set_image(self, image, image_width, image_height):
        self.__image = pygame.image.load(image)
        self.__image.convert_alpha()
        self.__image_width = image_width
        self.__image_height = image_height

    def set_offset(self, offset_x, offset_y):
        self.__offset_x, self.__offset_y = offset_x, offset_y

    def set_tile_dimensions(self, tile_width, tile_height):
        self.__tile_width, self.__tile_height = tile_width, tile_height

    def get_tile_dimensions(self):
        return [self.__tile_width, self.__tile_height]

    def get_offset(self):
        return [self.__offset_x, self.__offset_y]

    def get_image(self, gid=-1):
        if gid > -1:
            return self.__tile_storage[gid].image
        return self.__image

    def get_rect(self, gid=-1):
        if gid > -1:
            return self.__tile_storage[gid].rect
        return self.__image.get_rect()

    def initiate(self):
        self.__tiles_in_row = tiles_in_row = int(self.__image_width / self.__tile_width)
        self.__tiles_in_col = tiles_in_col = int(self.__image_height / self.__tile_height)
        self.__last_gid = self.__first_gid - 1 + int(tiles_in_row * tiles_in_col)

        dim = self.get_tile_dimensions()

        gid = self.__first_gid
        for tile_row in range(0, tiles_in_row):
            for tile_col in range(0, tiles_in_col):
                tile = Tile(gid)
                tile.set_tileset(self)
                cell = self.get_image_cell(gid)
                tile.image = pygame.Surface(dim, HWSURFACE | SRCALPHA)
                tile.rect = pygame.rect.Rect((dim[0]*cell[0], dim[1]*cell[1]), tuple(dim))
                tile.image.blit(self.__image, (0, 0), tile.rect)
                self.__tile_storage[gid] = tile
                gid += 1

        # self.slice_an_image_on_tiles()
        # print(self.__tile_height, self.__tile_width, self.__first_gid, self.__last_gid)

    def get_tile_template(self, tile_gid):
        return self.__tile_storage[tile_gid]

    def get_bounds(self):
        return self.__first_gid, self.__last_gid

    def get_id(self):
        return self.__id

    def get_image_cell(self, tile_gid):
        tiles_in_col = self.__tiles_in_col
        tiles_in_row = self.__tiles_in_row
        tile_row = 0
        tile_col = 0
        for i in range(self.__first_gid, tile_gid):
            tile_row += 1
            if tile_row == tiles_in_row:
                tile_row = 0
                tile_col += 1
            if tile_col == tiles_in_col:
                tile_col = 0

        #print(tile_gid, tile_row, tile_col)
        return tile_row, tile_col

    def get_regular_tile_dimensions(self):
        return self.__loader.get_tile_dimensions()