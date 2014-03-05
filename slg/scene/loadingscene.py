__author__ = "Den"

import pygame
from slg.scene.scene import Scene
import slg.ui as ui
import os

class LoadingScene(Scene):

    def __init__(self, vp, app):
        super().__init__(vp, app)
        image = pygame.image.load(os.path.join(os.getcwd(), 'data', 'gui', 'loading_screen.jpg'))
        self.surface = pygame.Surface(vp)
        self.surface.blit(image, (0, 0))

    def draw(self, surface=None):
        if surface is not None:
            self.set_target(surface)
        if self._target is not None:
            self._target.blit(self.surface, (0, 0))
