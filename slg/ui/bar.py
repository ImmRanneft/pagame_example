__author__ = 'Den'

import pygame
import pygame.rect

from slg.ui.widget import Widget


class Bar(Widget):

    """
    simple bar
    @type _name: str
    @type _layer: str
    @type color: tuple
    @type bg: tuple
    @type _type: str
    """

    _layer = 'gui'
    _name = 'bar'
    _type = ''

    def __init__(self, name, size, *groups, **styles):
        self._name = name
        super().__init__(*groups, **styles)
        self.image = pygame.Surface(size)
        self.image.fill(self.styles['border_color'])
        rect = self.image.get_rect().inflate(*tuple([-1*x for x in self.styles['border']]))
        pygame.draw.rect(self.image, self.styles['bgcolor'], rect)
        self.rect = pygame.rect.Rect(self.image.get_rect())