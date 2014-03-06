__author__ = "Den"

import pygame
import pygame.transform
from slg.scene import Scene
import slg.ui as ui
import os


class LoadingScene(Scene):

    def __init__(self, display: pygame.display, app):
        super().__init__(display, app)
        image = pygame.image.load(os.path.join(os.getcwd(), 'data', 'gui', 'loading_screen.jpg'))
        self.surface = pygame.Surface(display.get_size())
        image_size = image.get_size()
        surface_size = self.surface.get_size()

        x = int((image_size[0] - surface_size[0]) / 2)
        y = int((image_size[1] - surface_size[1]) / 2)
        if x < 0 and y < 0:
            image = pygame.transform.scale(image, surface_size)
            x, y = 0, 0
        elif x <= 0 and y >= 0:
            image = pygame.transform.scale(image, (surface_size[0], image_size[1]))
            x = 0
        elif x >= 0 and y <= 0:
            image = pygame.transform.scale(image, (image_size[0], surface_size[1]))
            y = 0

        self.surface.blit(image, (-x, -y))
        self.label = ui.TextWidget((0, 100, 100), font_size=60)
        self.label.set_text('Loading, please wait')
        self.label.set_target(self.surface)
        self.label.draw()

    def draw(self, surface=None):
        if surface is not None:
            self.set_target(surface)
        if self._target is not None:
            self._target.blit(self.surface, (0, 0))
