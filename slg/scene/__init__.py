__author__ = "Den"

import pygame


class Scene(pygame.sprite.Sprite):

    image = _target = None
    rect = None
    _app = None

    def __init__(self, display: pygame.display, app):
        self.image = pygame.Surface(display.get_size())
        self.rect = self.image.get_rect()
        self.set_app(app)

    def set_app(self, app):
        self._app = app

    def set_target(self, surface):
        self._target = surface

    def update(self, surface=None):
        if surface:
            self.set_target(surface)
        if self._target is not None:
            self._target.blit(self.image, (0, 0))

    def append(self, surface, dest):
        self.image.blit(surface, dest)

    def get_surface(self):
        return self.image

    def poll_events(self, events):
        pass