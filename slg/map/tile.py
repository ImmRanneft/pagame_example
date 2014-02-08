__author__ = 'Den'

import pygame


class Tile(object):
    __renderer = None
    __image = None
    __tile_width = 0
    __tile_height = 0

    __offset_x = 0
    __offset_y = 0

    __tile_x = 0
    __tile_y = 0

    def __init__(self, renderer, image, tile_width, tile_height, offset_x=0, offset_y=0):
        # self.__surface = surface
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

    def load_tile(self, image_name):
        self.__image = pygame.image.load(image_name).convert_alpha()
        return self

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