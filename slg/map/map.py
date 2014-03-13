__author__ = 'den'


from collections import OrderedDict

from slg.map.loader.tmx import Tmx
from slg.map.layer import Layer
from slg.map.objectgroup import ObjectGroup


class Map(object):
    """
    Map object, holds layers and objects
    """

    _layers = OrderedDict

    _object_groups = OrderedDict

    _loader = None

    _map_name = ''

    def __init__(self):
        pass

    def load(self, map_name):
        self._map_name = map_name
        self._guess_loader().load(self)

    def _guess_loader(self):
        if self._map_name != '':
            self._loader = Tmx()
        return self._loader

    def add_layer(self, layer: Layer):
        self._layers[layer.get_name()] = layer

    def add_object_group(self, object_group: ObjectGroup):
        self._layers[object_group.get_name()] = object_group

    def get_name(self):
        return self._map_name