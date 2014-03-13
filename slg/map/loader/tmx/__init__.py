__author__ = 'den'

from slg.map.map import Map

class Tmx(object):

    _map_object = Map

    def __init__(self):
        pass

    def load(self, map_object):
        self._map_object = map_object
        print(map_object.get_name()+' loading...')
