__author__ = 'den'


from collections import OrderedDict
from slg.map.layer import Layer
from slg.map.objectgroup import ObjectGroup


class Map(object):
    """
    Map object, holds layers and objects
    """

    _layers = OrderedDict

    _object_groups = OrderedDict

    _loader = None

    def __init__(self):
        pass

    def load(self):

    def add_layer(self, layer: Layer):
        self._layers[layer.get_name()] = layer

    def add_object_group(self, object_group: ObjectGroup):
        self._layers[object_group.get_name()] = object_group
