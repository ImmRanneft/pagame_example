__author__ = 'Den'

import pygame


class Tile(object):
    __renderer = __image = __rect = None
    __tile_width = __tile_height = __offset_x = __offset_y = __tile_x = __tile_y = 0

    def __init__(self, renderer, image, tile_width, tile_height, offset_x=0, offset_y=0):
        self.__renderer = renderer
        self.__image = image
        self.__tile_width = tile_width
        self.__tile_height = tile_height
        self.__offset_x = offset_x
        self.__offset_y = offset_y

    def coordinates(self, x, y):
        self.__tile_x, self.__tile_y = x, y
        return self

    def get_coordinates(self):
        return self.__tile_x, self.__tile_y

    def draw(self):
        self.__renderer.draw(self)
        return self

    def offset_x(self):
        return self.__offset_x

    def offset_y(self):
        return self.__offset_y

    def get_width(self):
        return self.__tile_width

    def get_height(self):
        return self.__tile_height

    def get_x(self):
        return self.__tile_x

    def get_y(self):
        return self.__tile_y

    def get_image(self):
        return self.__image

    def set_rect(self, rect):
        self.__rect = rect
        return self

    def get_rect(self):
        return self.__rect