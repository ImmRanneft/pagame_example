__author__ = 'Den'

import pygame.event

from slg.locals import *


class MapLoaded(object):

    _event = pygame.event.Event

    def post(self):
        self._event = pygame.event.Event(EVENT_MAP_LOADED)
        pygame.event.post(self._event)