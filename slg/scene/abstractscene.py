__author__ = 'Den'


class AbstractScene(object):

    """
    @type _manager: slg.application.manager.Manager
    """
    _manager = None

    def __init__(self, manager):
        self._manager = manager

    def handle_events(self, *events):
        raise NotImplemented

    def draw(self):
        raise NotImplemented

    manager = property(lambda self: self._manager, lambda self, v: None, lambda self: None)