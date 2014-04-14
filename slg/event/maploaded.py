__author__ = 'Den'

import pygame.event

from slg.locals import *


class MapLoaded(object):

    _event = pygame.event.Event

    def __init__(self, map_object):
        self.map_object = map_object

    def post(self):
        self._event = pygame.event.Event(EVENT_MAP_LOADED, map_object = self.map_object)
        pygame.event.post(self._event)