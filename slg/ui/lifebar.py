__author__ = 'Den'

import pygame.sprite
import pygame.rect
import pygame.draw

from slg.ui import TextWidget

import slg.ui.bar


class Lifebar(slg.ui.bar.Bar):

    def __init__(self, surface, *groups, **styles):
        name = 'lifebar'
        size = [100, 40]
        super().__init__(name, size, *groups, **styles)

        surface_rect = pygame.rect.Rect(surface.get_rect())
        self.rect.move_ip(surface_rect.left + 20, surface_rect.bottom - 20 - self.rect.height)

        text = TextWidget(*groups, **styles)
        text.set_text(self._name)
        text.draw(self.image)

