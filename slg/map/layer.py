__author__ = 'Den'

from slg.map.tile import Tile
import pygame


class Stub(object):

    __coordinates = [0, 0]
    __display_coordinates = [0, 0]
    __rectangle = [0, 0, 0, 0]
    __dimensions = [0, 0]
    __offset = [0, 0]
    image = None

    def __init__(self):
        self.image = pygame.Surface((64, 32))
        self.image.fill((0, 0, 0))

    def coordinates(self, coordinates):
        self.__coordinates = coordinates

    def get_coordinates(self):
        return self.__coordinates

    def draw(self, surface, renderer):
        pixelCoordinates = renderer.translate(self)
        surface.blit(self.get_image(), pixelCoordinates)

    def get_id(self):
        return 0

    def get_regular_tile_dimensions(self):
        return (64, 32)

    def get_dimensions(self):
        return (64, 32)

    def get_offset(self):
        return (0, 0)

    def get_image(self):
        return self.image


class Layer(object):

    __left = __right = __top = __bottom = 0
    __renderer = None
    __container = [[]]
    __order = 0

    def __init__(self, order):
        self.__order = order
        self._stub = Stub()

    def set_renderer(self, renderer):
        self.__renderer = renderer

    def get_container(self):
        return self.__container

    def set_dimensions(self, dimensions):
        layer_width, layer_height = int(dimensions[0]), int(dimensions[1])
        # world_height = int(dimensions[1])
        self.__container = [[Tile for x in range(0, layer_height)] for x in range(0, layer_width)]

    def set_visible_area(self, visible_area):
        self.__left = visible_area[0]
        self.__right = visible_area[1]
        self.__top = visible_area[2]
        self.__bottom = visible_area[3]

    def draw(self, surface):
        for col in range(self.__top, self.__bottom):
            for row in range(self.__left, self.__right):
                try:
                    # if self.__container[row] is not None and self.__container[row][col] is not None:
                    tile = self.__container[row][col]
                    if (tile.get_id() > 0):
                        tile.draw(surface, self.__renderer)
                except IndexError:
                    self._stub.coordinates([row, col])
                    self._stub.draw(surface, self.__renderer)
                    pass
                except AttributeError:
                    # print(tile, row, col)
                    row, col

    def append(self, tile, tilex, tiley):
        try:
            self.__container[tilex][tiley] = tile
        except IndexError:
            tilex, tiley

    def get(self, coordinates = None):
        if coordinates is not None:
            i = coordinates[0]
            j = coordinates[1]
            return self.__container[i][j]
        else:
            return self.__container
