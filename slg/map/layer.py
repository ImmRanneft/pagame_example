__author__ = 'den'


class Layer(object):
    """
    Simple layer, that holds all this tiles and determinates which of them have to be drawn depending in visible_area
    """

    _name = ''

    _order = 0

    _visible_area = {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}

    _container = [[]]

    def __init__(self):
        pass

    # setters and getters
    def get_name(self):
        return self._name

    def set_name(self, name: str):
        self._name = name

    name = property(get_name, set_name)

    def get_order(self):
        return self._order

    def set_order(self, order: int):
        self._order = order

    order = property(get_order, set_order)
