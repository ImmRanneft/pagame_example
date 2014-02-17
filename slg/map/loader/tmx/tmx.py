__author__ = 'Den'

from slg.map.loader.tmx import *


class TmxLoader(object):

    __sets = __tiles = __objects = list()
    # __data_dir = os.path.realpath(__file__)

    def __init__(self):
        # self.__data_dir = data_dir
        pass

    def load(self, map):
        self.__load_sets()

    def __load_sets(self):
        tileset = Tileset()
        self.__sets.append(tileset)

    def __load_tiles(self):
        tile = Tile()
        print(self.__tiles)
        self.__tiles.append(tile)

    def get_tilesets(self):
        return self.__sets

    def get_tiles(self):
        return self.__tiles

