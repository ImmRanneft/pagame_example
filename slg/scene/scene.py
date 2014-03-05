__author__ = "Den"

import pygame


class Scene(object):

    _surface = _target = None

    def __init__(self, vp):
        self._surface = pygame.Surface(vp)

    def set_target(self, surface):
        self._target = surface

    def draw(self, surface=None):
        if surface:
            self.set_target(surface)
        if self._target is not None:
            self._target.blit(self._surface, (0, 0))

    def append(self, surface, dest):
        self._surface.blit(surface, dest)

    def get_surface(self):
        return self._surface