__author__ = 'Den'

import os

import pygame
import pygame.rect
from pygame.surface import Surface

from slg.scene.abstractscene import AbstractScene
from slg.locals import *
from slg.ui.textwidget import TextWidget


class LoadingScene(AbstractScene):
    """
    @type image: SurfaceType
    @type rect: pygame.rect.RectType
    """

    image = None
    rect = None

    def __init__(self, manager):
        """
        @type manager: slg.application.manager.Manager
        """
        super().__init__(manager)
        image = pygame.image.load(os.path.join(GUI_DIR, 'loading_screen.jpg'))
        self.image = Surface(self._manager.get_display().get_size())
        self.rect = pygame.rect.Rect(self.image.get_rect())
        image_size = image.get_size()
        surface_size = self.image.get_size()
        x = int((image_size[0] - surface_size[0]) / 2)
        y = int((image_size[1] - surface_size[1]) / 2)
        if x < 0 and y < 0:
            image = pygame.transform.scale(image, surface_size)
            x, y = 0, 0
        elif x <= 0 <= y:
            image = pygame.transform.scale(image, (surface_size[0], image_size[1]))
            x = 0
        elif y <= 0 <= x:
            image = pygame.transform.scale(image, (image_size[0], surface_size[1]))
            y = 0
        styles = {'font': 'alger'}
        text = TextWidget(**styles)
        text.set_text("""Loading...
Please wait""")
        self.image.blit(image, (-x, -y))
        text.draw(self.image)

    def handle_events(self, events):
        pass

    def draw(self):
        self._manager.get_display().blit(self.image, (0, 0))

    def update(self):
        pass



