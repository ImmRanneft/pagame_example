__author__ = 'den'


import pygame.rect


class Tile(object):

    image = None
    rect = None
    image_rect = None
    _template = None
    _coordinates = [0, 0]

    def get_id(self):
        return self._template.gid

    def coordinates(self, coordinates: tuple):
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
        # think about cache, or maybe we have to draw all images in some dict
        # like slice an image, and then jus get them.
        # yep looks like good idea, so we do not need
        # _loader_.tile.Tile, only tileset, if you wish
        # it will be simpler, just blit the image and that`s all
        # no we can`t remove _template, but it`s a good idea to slice image right in tileset
        self.image = template.get_image()
        self.rect = template.get_rect()