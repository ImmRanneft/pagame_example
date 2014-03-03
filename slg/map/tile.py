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
        if self.__template.gid == 89:
            print(self.__rect)
            exit()
        return self.__rect

    def get_x(self):
        tile_x = self.__template.get_dimensions()[0] * self.get_coordinates()[0]
        if self.get_coordinates()[1] % 2 == 1:
            tile_x += self.__template.get_dimensions()[0]/2
        return tile_x

    def get_y(self):
        tile_y = self.__template.get_dimensions()[1] * self.get_coordinates()[1]
        tile_y -= self.__template.get_offset()[1]
        gid = self.__template.gid
        if gid == 697 or gid == 698 or gid == 699:
            print(gid)
            tile_y -= self.get_coordinates()[1] * (self.__template.get_dimensions()[1] - 12 + self.__template.get_offset()[1])
        else:
            tile_y -= self.get_coordinates()[1] * (self.__template.get_dimensions()[1] / 2 + self.__template.get_offset()[1])
        return tile_y

    def get_id(self):
        return self.__template.gid