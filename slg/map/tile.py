__author__ = 'den'


import pygame.rect
import pygame.sprite


class Tile(pygame.sprite.Sprite):

    def __init__(self, *groups):
        self.image = None
        self.rect = None
        self.base_rect = None
        self._template = None
        self._coordinates = [0, 0]
        self._layer = 0
        super().__init__(*groups)

    def get_id(self):
        return self._template.gid

    def coordinates(self, coordinates: list, z=0):
        self._coordinates = coordinates
        self._layer = coordinates[0]+coordinates[1]+z

    def get_coordinates(self):
        return self._coordinates

    def get_dimensions(self):
        return self._template.get_dimensions()

    def get_offset(self):
        return self._template.get_offset()

    def get_regular_tile_dimensions(self):
        return self._template.get_regular_tile_dimensions()

    def set_template(self, template):
        self._template = template
        self.image = template.get_image()
        self.base_rect = template.get_rect()
        self.rect = template.get_rect()

    def __repr__(self):
        return super().__repr__() \
               + 'coords' + str(self._coordinates[0]) + ', ' + str(self._coordinates[1]) \
               + ' order: ' + str(self._layer) + "\r\n"