__author__ = 'Den'


class TileGroup(object):

    __left = __right = __top = __bottom = 0
    __renderer = None
    __container = [[]]

    def __init__(self, renderer):
        self.__renderer = renderer

    def get_container(self):
        return self.__container

    def set_world_dimensions(self, world_dimensions):
        world_width = int(world_dimensions[0])
        world_height = int(world_dimensions[1])
        self.__container = [[0 for x in range(0, world_height)] for x in range(0, world_width)]

    def set_area(self, left, right, top, bottom):
        self.__left, self.__right, self.__top, self.__bottom = left, right, top, bottom

    def draw(self):
        for col in range(self.__top, self.__bottom):
            for row in range(self.__left, self.__right):
                try:
                    # if self.__container[row] is not None and self.__container[row][col] is not None:
                    self.__renderer.draw(self.__container[row][col])
                except IndexError:
                    # print(row, col)
                    (row, col)

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
