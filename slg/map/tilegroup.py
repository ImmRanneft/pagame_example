__author__ = 'Den'


class TileGroup(object):

    __left = __right = __top = __bottom = 0

    def __init__(self, world_width, world_height):
        world_width = int(world_width)
        world_height = int(world_height)
        self.__container = [[0 for x in range(0, world_width)] for x in range(0, world_height)]

    def set_area(self, left, right, top, bottom):
        self.__left, self.__right, self.__top, self.__bottom = left, right, top, bottom
        print(self.__left, self.__right, self.__top, self.__bottom)

    def draw(self):
        # try:
        for i in range(self.__top, self.__bottom):
            for j in range(self.__right, self.__left, -1):
                if self.__container[i] is not None and self.__container[i][j] is not None:
                    self.__container[i][j].draw()
    # except IndexError:
        #     i, j

    def append(self, tile, tilex, tiley):
        self.__container[tilex][tiley] = tile

    def get(self, coordinates = None):
        if coordinates is not None:
            i = coordinates[0]
            j = coordinates[1]
            return self.__container[i][j]
        else:
            return self.__container
