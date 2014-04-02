__author__ = 'den'


import os

from xml.dom import minidom

from slg.locals import *
from slg.map.loader.tmx.tileset import Tileset
from slg.map.layer import Layer
from slg.map.tile import Tile


class Tmx(object):

    _map_object = None
    __map = None
    __orientation = 'staggered'
    __tile_dimensions = [64, 32]
    __map_dimensions = [0, 0]
    __sets = list()
    __sets_ranges = dict()
    __layers = list()
    __tiles = list()

    def __init__(self):
        pass

    def load(self, map_object):
        self._map_object = map_object
        print(map_object.get_name()+' loading...')
        pj = os.path.join(MAP_DIR, map_object.get_name())
        self.__map = minidom.parse(pj)
        self.__load_map()
        self.__load_sets()
        self.__load_layers()

    def __load_map(self):
        raw_map = self.__map.getElementsByTagName('map')[0]
        self.__orientation = raw_map.attributes['orientation'].value
        self._map_object.switch_renderer(self.__orientation)
        tile_width = int(raw_map.attributes['tilewidth'].value)
        tile_height = int(raw_map.attributes['tileheight'].value)
        map_width = int(raw_map.attributes['width'].value)
        map_height = int(raw_map.attributes['height'].value)
        self.__map_dimensions = [map_width, map_height]
        self.__tile_dimensions = [tile_width, tile_height]
        self._map_object.set_dimensions(self.__map_dimensions, self.__tile_dimensions)

    def __load_sets(self):
        i = 0
        for raw_tileset in self.__map.getElementsByTagName('tileset'):
            tileset = Tileset(raw_tileset.attributes['firstgid'].value, raw_tileset.attributes['name'].value, i, self)
            i += 1
            image = raw_tileset.getElementsByTagName('image')[0]
            image_name = image.attributes['source'].value
            image_x, image_y = int(image.attributes['width'].value), int(image.attributes['height'].value)
            tileset.set_image(os.path.realpath(os.path.join(DATA_DIR, 'tiles', image_name)), image_x, image_y)

            tileoffset = raw_tileset.getElementsByTagName('tileoffset')
            if(len(tileoffset) > 0):
                tileoffset = tileoffset[0]
                offset_x, offset_y = int(tileoffset.attributes['x'].value), int(tileoffset.attributes['y'].value)
            else:
                offset_x, offset_y = 0, 0
            tileset.set_offset(offset_x, offset_y)

            tile_width = int(raw_tileset.attributes['tilewidth'].value)
            tile_height = int(raw_tileset.attributes['tileheight'].value)
            tileset.set_tile_dimensions(tile_width, tile_height)

            tileset.initiate()
            self.__sets.insert(tileset.get_id(), tileset)

        for tileset in self.__sets:
            self.__sets_ranges[0] = 0
            i, j = tileset.get_bounds()
            for tile_gid in range(i, j+1):
                self.__sets_ranges[tile_gid] = tileset.get_id()

    def __load_layers(self):
        layers = self.__map.getElementsByTagName('layer')
        i = 0
        for raw_layer in layers:
            layer = Layer()
            layer.name = raw_layer.attributes['name'].value
            self._map_object.add_layer(layer)
            layer_width = int(raw_layer.attributes['width'].value)
            layer_height = int(raw_layer.attributes['height'].value)
            layer.set_renderer(self._map_object.get_renderer())
            layer.set_dimensions([layer_width, layer_height], self.__tile_dimensions)
            layer.set_order(i)
            self.__load_tiles(layer, raw_layer)
            i += 1

    def get_layers(self):
        return self.__layers

    def __load_tiles(self, layer, raw_layer):
        tiles = raw_layer.getElementsByTagName('tile')
        l_w, l_h = int(raw_layer.attributes['width'].value), int(raw_layer.attributes['height'].value)
        x, y = 0, 0
        for raw_tile in tiles:
            tile_gid = int(raw_tile.attributes['gid'].value)
            if tile_gid > 0:
                coordinates = [x, y]
                tileset = self.__sets[self.__sets_ranges[tile_gid]]
                tile_template = tileset.get_tile_template(tile_gid)
                [tile_width, tile_height] = tile_template.get_dimensions()
                tile = Tile()
                # tile._layer = layer.get_order()
                tile.set_template(tile_template)
                tile.coordinates(coordinates, layer.order)
                tile.base_rect = self._map_object.get_renderer().map_to_screen(tile)
                layer.append(tile, x, y)
            x += 1
            if x >= l_w:
                x = 0
                y += 1

    def get_tilesets(self):
        return self.__sets

    def get_tiles(self):
        return self.__tiles

    def get_tile_dimensions(self):
        return self.__tile_dimensions

    def get_map_dimensions(self):
        return self.__map_dimensions