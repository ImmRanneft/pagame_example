__author__ = 'Den'

from xml.dom import minidom
from slg.map.loader.tmx import Tileset
from slg.map.loader.tmx import DATA_DIR
from slg.map import Tile
import os


class TmxLoader(object):

    __sets_ranges = list()
    __sets = list()
    __tiles = list()
    __objects = list()
    __map = None
    # __data_dir = os.path.realpath(__file__)

    def __init__(self):
        # self.__data_dir = data_dir
        pass

    def load(self, map):
        print('Map ', map, 'loading')
        self.__map = minidom.parse(map)
        self.__load_sets()
        self.__load_tiles()

    def __load_sets(self):
        i = 0
        for raw_tileset in self.__map.getElementsByTagName('tileset'):
            # print(raw_tileset.attributes['firstgid'].value, raw_tileset.attributes['name'].value)
            # exit()
            tileset = Tileset(raw_tileset.attributes['firstgid'].value, raw_tileset.attributes['name'].value, i)
            i += 1

            image = raw_tileset.getElementsByTagName('image')[0]
            image_name = image.attributes['source'].value
            image_x, image_y = int(image.attributes['width'].value), int(image.attributes['height'].value)
            tileset.set_image(os.path.realpath(os.path.join(DATA_DIR, 'tiles', image_name)), image_x, image_y)

            tileoffset = raw_tileset.getElementsByTagName('tileoffset')[0]
            offset_x, offset_y = int(tileoffset.attributes['x'].value), int(tileoffset.attributes['y'].value)
            tileset.set_offset(offset_x, offset_y)

            tile_width = int(raw_tileset.attributes['tilewidth'].value)
            tile_height = int(raw_tileset.attributes['tileheight'].value)
            tileset.set_tile_dimensions(tile_width, tile_height)

            tileset.initiate()
            self.__sets.insert(tileset.get_id(), tileset)

        for tileset in self.__sets:
            i, j = tileset.get_bounds()
            for tile_gid in range(i, j):
                self.__sets_ranges.insert(tile_gid, tileset.get_id())

    def __load_tiles(self):
        position = 0
        layers = self.__map.getElementsByTagName('layer')
        for raw_layer in layers:
            tiles = raw_layer.getElementsByTagName('tile')

            l_w, l_h = int(raw_layer.attributes['width'].value), int(raw_layer.attributes['height'].value)
            x, y = 0, 0
            for raw_tile in tiles:
                tile_gid = int(raw_tile.attributes['gid'].value)
                coordinates = [x, y]
                tileset = self.__sets[self.__sets_ranges[tile_gid - 1]]
                tile_template = tileset.get_tile_template(tile_gid)
                [tile_width, tile_height] = tile_template.get_dimensions()
                tile = Tile(tile_template)
                tile.coordinates(coordinates)
                rect = ((x * tile_width, y * tile_height), (tile_width, tile_height))
                tile.set_rect(rect)
                x += 1
                if x >= l_w:
                    x = 0
                    y += 1

                self.__tiles.append(tile)

        for tile in self.__tiles:
            print(tile.get_coordinates(), tile.get_template().gid)

    def get_tilesets(self):
        return self.__sets

    def get_tiles(self):
        return self.__tiles