__author__ = 'Den'


class TileGroup(object):

    __left = __right = __top = __bottom = 0

    def __init__(self, world_width, world_height):
        world_width = int(world_width/2)
        world_height = int(world_height/2)
        self.__container = [[0 for x in range(-world_width, world_width)] for x in range(-world_height, world_height)]

    def set_area(self, left, right, top, bottom):
        self.__left, self.__right, self.__top, self.__bottom = left, right, top, bottom

    def draw(self):
        try:
            for i in range(self.__top, self.__bottom):
                for j in range(self.__right, self.__left, -1):
                    self.__container[i][j].draw()
        except IndexError:
            pass

    def append(self, tile, tilex, tiley):
        self.__container[tilex][tiley] = tile

    def get(self, i=None):
        print(self.__container)
        if i is not None:
            return self.__container[i]
        else:
            return self.__container
