__author__ = 'Den'


class Layer(object):

    name = 'layer'
    __order = 0
    __raw_data = None

    def __init__(self, order, raw_data, name = 'layer'):
        self.name = name
        self.__order = order
        self.__raw_data = raw_data
        self.__dimensions = [int(raw_data.attributes['width'].value), int(raw_data.attributes['height'].value)]

    def get_dimensions(self):

        return self.__tileset.get_tile_dimensions()

    def get_offset(self):
        return self.__tileset.get_offsets()

    def get_image(self):
        return self.__tileset.get_image()

    def get_image_offsets(self):
        return self.__tileset.get_image_offsets(self.gid)