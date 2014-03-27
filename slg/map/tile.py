__author__ = 'den'


import pygame.rect
import pygame.sprite


class Tile(pygame.sprite.Sprite):

    image = None
    rect = None
    image_rect = None
    _template = None
    _coordinates = [0, 0]

    def get_id(self):
        return self._template.gid

    def coordinates(self, coordinates: list):
        self._coordinates = coordinates

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
        self.rect = template.get_rect()