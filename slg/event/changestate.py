__author__ = 'Den'


import pygame.event

from slg.locals import *


class ChangeState(object):

    _state = None
    _event = pygame.event.Event

    def __init__(self, state=GAME_STATE_LOADING):
        self._state = state

    def post(self):
        self._event = pygame.event.Event(EVENT_CHANGE_STATE, state=self._state, obj=self)
        pygame.event.post(self._event)