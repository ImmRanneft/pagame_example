__author__ = 'Den'

import pygame.event

from slg.locals import *


class MainMenu(object):

    _event = pygame.event.Event

    def post(self):
        self._event = pygame.event.Event(EVENT_MAIN_MENU)
        pygame.event.post(self._event)