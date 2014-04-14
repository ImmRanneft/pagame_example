__author__ = 'Den'


class Event(object):

    def __init__(self):
        self.slots = []

    def connect(self, slot):
        assert callable(slot)
        self.slots.append(slot)

    def __call__(self, *args, **kwargs):
        for slot in self.slots:
            slot(*args, **kwargs)