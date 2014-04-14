__author__ = 'Den'

import pygame.event

from slg.locals import *


class LoadMap(object):

    _map_name = ''
    _event = pygame.event.Event

    def __init__(self, map_name):
        self._map_name = map_name

    def post(self):
        self._event = pygame.event.Event(EVENT_LOAD_MAP, map_name=self._map_name)
        pygame.event.post(self._event)