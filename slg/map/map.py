__author__ = 'den'

import threading
from collections import OrderedDict

import pygame
from pygame.locals import *

from slg.map.loader.tmx import Tmx
from slg.map.layer import Layer
from slg.map.objectgroup import ObjectGroup


class Map(object):
    """
    Map object, holds layers and objects
    """

    _layers = OrderedDict()

    _object_groups = OrderedDict()

    _loader = None

    _map_name = ''
    _tile_dimensions = [0, 0]
    _map_dimensions = [0, 0]

    map_surface = None

    def __init__(self):
        pass

    def load(self, map_name):
        self._map_name = map_name
        self._guess_loader().load(self)

    def set_dimensions(self, map_dimensions, tile_dimensions):
        self._map_dimensions = map_dimensions
        self._tile_dimensions = tile_dimensions
        self.map_surface = pygame.Surface(map_dimensions, SRCALPHA | HWSURFACE)

    def get_tile_dimensions(self):
        return self._tile_dimensions

    def get_map_dimensions(self):
        return self._map_dimensions

    def _guess_loader(self):
        if self._map_name != '':
            self._loader = Tmx()
        return self._loader

    def add_layer(self, layer: Layer):
        self._layers[layer.get_name()] = layer

    def get_layers(self):
        return self._layers.values()

    def add_object_group(self, object_group: ObjectGroup):
        self._layers[object_group.get_name()] = object_group

    def get_name(self):
        return self._map_name

    def render(self, renderer):
        for layer in self.get_layers():
            layer.draw(renderer)
            self.map_surface.blit(layer.image, layer.rect)

    def draw(self, surface, camera):
        for layer in self.get_layers():
            layer.update(camera)
            self.map_surface.blit(layer.image, layer.rect)
        surface.blit(self.map_surface, (0, 0))


class MapLoadingThread(threading.Thread):

    def __init__(self, map_name, map_object):
        self._map_name = map_name
        self._map_object = map_object
        super().__init__()
