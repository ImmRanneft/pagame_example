__author__ = 'den'


class Tmx(object):

    _map_object = None

    def __init__(self):
        pass

    def load(self, map_object):
        self._map_object = map_object
        print(map_object.get_name()+' loading...')
