__author__ = 'den'

import pygame
import pygame.sprite
import pygame.rect
import slg.renderer.staggered
from pygame.locals import *


class Layer(pygame.sprite.Sprite):
    """
    Simple layer, that holds all this tiles and determinates which of them have to be drawn depending in visible_area
    @type _name: str
    @type _order: int
    @type image: pygame.SurfaceType
    @type rect: pygame.rect.Rect
    """

    _name = ''

    _order = 0
    _layer = 'bg'
    dirty = 0

    _visible_area = {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}

    _container = [[]]
    _dimensions = []
    _tile_dimensions = []
    image = None
    rect = None
    _map_object = None
    _renderer = None

    def __init__(self, *groups):
        super().__init__(*groups)

    # setters and getters
    def get_name(self):
        return self._name

    def set_name(self, name: str):
        self._name = name

    name = property(get_name, set_name)

    def set_renderer(self, renderer):
        self._renderer = renderer

    def set_dimensions(self, dimensions, tile_dimensions):
        self._dimensions = dimensions
        self._tile_dimensions = tile_dimensions

        layer_width, layer_height = int(dimensions[0]), int(dimensions[1])
        layer_surface_dimensions = self._renderer.calculate_surface_dimensions(dimensions, tile_dimensions)
        self.image = pygame.Surface(layer_surface_dimensions, SRCALPHA | HWSURFACE)
        self.rect = self.image.get_rect()

        self._container = [[None for x in range(0, layer_height)] for x in range(0, layer_width)]

    def get_dimensions(self):
        return self._dimensions

    def set_map(self, map_object):
        self._map_object = map_object

    def get_order(self):
        return self._order

    def set_order(self, order: int):
        self._order = order

    def update(self):
        camera_bounds = self._renderer.get_camera_bounds()
        for key in camera_bounds.keys():
            if self._visible_area[key] != camera_bounds[key]:
                self._visible_area[key] = camera_bounds[key]
                self.dirty = 1
        if self.dirty > 0:
            # self.dirty = 0
            # print('draw')
            self._render()

    def _render(self):
        self._renderer.draw_map(self, self._map_object)

    def append(self, tile, tile_x, tile_y):
        try:
            self._container[tile_x][tile_y] = tile
        except IndexError:
            print('append_error:', tile_x, tile_y)

    def get(self, coordinates = None):
        if coordinates is not None:
            i = coordinates[0]
            j = coordinates[1]
            return self._container[i][j]
        else:
            return self._container

    order = property(get_order, set_order)
