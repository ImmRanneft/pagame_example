__author__ = 'Den'


class Layer(object):

    __left = __right = __top = __bottom = 0
    __renderer = None
    __container = [[]]
    __order = 0

    def __init__(self, order):
        self.__order = order

    def set_renderer(self, renderer):
        self.__renderer = renderer

    def get_container(self):
        return self.__container

    def set_dimensions(self, dimensions):
        layer_width, layer_height = int(dimensions[0]), int(dimensions[1])
        # world_height = int(dimensions[1])
        self.__container = [[0 for x in range(0, layer_height)] for x in range(0, layer_width)]

    def set_visible_area(self, visible_area):
        self.__left = visible_area[0]
        self.__right = visible_area[1]
        self.__top = visible_area[2]
        self.__bottom = visible_area[3]

    def draw(self):
        for col in range(self.__top, self.__bottom):
            for row in range(self.__left, self.__right):
                try:
                    # if self.__container[row] is not None and self.__container[row][col] is not None:
                    tile = self.__container[row][col]
                    if (tile.get_id() > 0):
                        self.__renderer.draw(tile)
                except IndexError:
                    # print(row, col)
                    (row, col)
                except AttributeError:
                    print(tile, row, col)

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
