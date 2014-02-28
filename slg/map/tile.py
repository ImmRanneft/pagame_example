__author__ = 'Den'

import pygame


class Tile(object):

    __coordinates = [0, 0]
    __display_coordinates = [0, 0]
    __rectangle = [0, 0, 0, 0]
    __dimensions = [0, 0]
    __offset = [0, 0]
    __template = None

    def __init__(self, template):
        self.__template = template

    def get_template(self):
        return self.__template

    def coordinates(self, coordinates):
        self.__coordinates = coordinates

    def get_coordinates(self):
        return self.__coordinates

    def get_dimensions(self):
        return self.__template.get_dimensions()

    def get_offset(self):
        return self.__template.get_offset()

    def get_image(self):
        return self.__template.get_image()

    def set_rect(self, rect):
        self.__rect = rect
        return self

    def get_rect(self):
        return self.__rect

    def get_x(self):
        tile_x = self.__template.get_dimensions()[0] * self.get_coordinates()[0]
        if self.get_coordinates()[1] % 2 == 1:
            tile_x -= self.__template.get_dimensions()[0]/2
        return tile_x

    def get_y(self):
        tile_y = self.__template.get_dimensions()[1] * self.get_coordinates()[1]
        tile_y -= self.get_coordinates()[1] * self.__template.get_offset()[1]*3
        return tile_y