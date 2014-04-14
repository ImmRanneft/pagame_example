__author__ = 'den'


class ObjectGroup(object):
    """
    Just holder for objects
    """
    _name = ''

    def __init__(self, name):
        self.set_name(name)
        pass

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    name = property(get_name, set_name)