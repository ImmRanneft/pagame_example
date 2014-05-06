__author__ = 'den'

import threading
from collections import OrderedDict

import pygame
from pygame.locals import *

import slg.renderer.staggered
import slg.renderer.isometric
import slg.renderer.orthogonal

from slg.map.loader.tmx import Tmx
from slg.map.layer import Layer
from slg.map.objectgroup import ObjectGroup
from slg.event.maploaded import MapLoaded


class Map(pygame.sprite.LayeredUpdates):
    """
    Map object, holds layers and objects
    """

    _layers = OrderedDict()

    _object_groups = OrderedDict()

    _loader = None
    _renderer = None

    dirty = 1

    _map_name = ''
    _tile_dimensions = [0, 0]
    _map_dimensions = [0, 0]

    map_surface = None

    def __init__(self, manager):
        super().__init__()
        self._manager = manager
        self.l = []
        self.object_layer = 1
        self._collider = dict()

    def get_manager(self):
        return self._manager

    def load(self, map_name):
        self._map_name = map_name
        self._guess_loader().load(self)

    def set_dimensions(self, map_dimensions, tile_dimensions):
        self._map_dimensions = map_dimensions
        self._tile_dimensions = tile_dimensions

    def get_tile_dimensions(self):
        return self._tile_dimensions

    def get_map_dimensions(self):
        return self._map_dimensions

    def _guess_loader(self):
        if self._map_name != '':
            self._loader = Tmx()
        return self._loader

    def update_collider(self, x, y, delete=False):
        if delete is False:
            self._collider[self._map_dimensions[0]*y+x] = 1
        else:
            del self._collider[self._map_dimensions[0]*y+x]

    def check_collide(self, x, y):
        return self._collider.get(self._map_dimensions[0]*y+x, 0)

    def switch_renderer(self, renderer):
        if renderer == 'staggered':
            self.set_renderer(slg.renderer.staggered.Staggered())
        elif renderer == 'isometric':
            self.set_renderer(slg.renderer.isometric.Isometric())
        elif renderer == 'orthogonal':
            self.set_renderer(slg.renderer.orthogonal.Orthogonal())

        self._manager.get_camera().set_renderer(self.get_renderer())

        return self.get_renderer()

    def set_renderer(self, renderer):
        self._renderer = renderer

    def get_renderer(self):
        return self._renderer

    def add_layer(self, layer: Layer):
        self._layers[layer.get_name()] = layer
        layer.set_map(self)

    def get_layers(self):
        return self._layers.values()

    def add_object_group(self, object_group: ObjectGroup):
        self._layers[object_group.get_name()] = object_group

    def get_name(self):
        return self._map_name

    def update(self):
        for layer in self.get_layers():
            layer.update()

    def sort(self):
        self.l = sorted(self.l, key=lambda spr: spr.order)

    # def empty(self):
    #     self.l = []

    # def add(self, *sprites):
    #     for sprite in sprites:
    #         self.l.append(sprite)

    # def draw(self, surface):
    #     blit = surface.blit
    #     for sprite in self.l:
    #         blit(sprite.image, sprite.rect)


class MapLoadingThread(threading.Thread):
    def __init__(self, map_name, map_object, camera):
        self._map_name = map_name
        self._map_object = map_object
        self._camera = camera
        super().__init__()

    def run(self):
        print('start loading map ' + self._map_name)
        self._map_object.load(self._map_name)
        self._camera.set_dimensions(self._map_object.get_tile_dimensions(), self._map_object.get_map_dimensions())
        self._camera.update()
        MapLoaded(self._map_object).post()
        print('finished loading map ' + self._map_name)
