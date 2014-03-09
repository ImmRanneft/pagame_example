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
        self.image = self.get_image()

    def get_template(self):
        return self.__template

    def coordinates(self, coordinates):
        self.__coordinates = coordinates

    def get_coordinates(self):
        return self.__coordinates

    def set_rect(self, rect):
        self.__rect = rect
        return self

    def get_rect(self):
        return self.__rect

    def get_x(self):
        tile_x = self.__template.get_dimensions()[0] * self.get_coordinates()[0] + \
                 int(self.get_coordinates()[1]) % 2 * self.__template.get_dimensions()[0]/2
        return tile_x

    def get_y(self):
        regular = self.__template.get_regular_tile_dimensions()
        current = self.__template.get_dimensions()
        offset = self.__template.get_offset()
        divider = (current[1] - 2 * offset[1]) / regular[1] * 2
        tile_y = self.__template.get_dimensions()[1] / divider * self.get_coordinates()[1]
        dy = current[1] - regular[1] - offset[1] + offset[1] * self.get_coordinates()[1]
        tile_y -= dy
        return tile_y

    def draw(self, surface, renderer):
        pixelCoordinates = renderer.translate(self)
        surface.blit(self.get_image(), pixelCoordinates, self.get_rect())

    def get_id(self):
        return self.__template.gid

    def get_regular_tile_dimensions(self):
        return self.__template.get_regular_tile_dimensions()

    def get_dimensions(self):
        return self.__template.get_dimensions()

    def get_offset(self):
        return self.__template.get_offset()

    def get_image(self):
        return self.__template.get_image()
