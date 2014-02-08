__author__ = 'Den'


class TileGroup(object):

    def __init__(self):
        self.__container = list()

    def draw(self):
        for t in self.__container:
            t.draw()

    def append(self, tile):
        self.__container.append(tile)

    def get(self, i=None):
        print(self.__container)
        if i is not None:
            return self.__container[i]
        else:
            return self.__container
