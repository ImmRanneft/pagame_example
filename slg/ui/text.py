__author__ = 'Den'

import pygame.sprite
import pygame.rect
import pygame.draw

from slg.locals import *
from slg.ui import TextWidget
from slg.event.changestate import ChangeState
import slg.ui.dialog


class Text(slg.ui.dialog.Dialog):

    def __init__(self, string_to_render, surface, *groups, **styles):
        name = 'text'
        text = TextWidget(*groups, **styles)
        text.set_text(string_to_render)
        [w, h] = text.get_size()
        size = [w, h]
        super().__init__(name, size, surface, *groups, **styles)
        text.draw(self.image)

    def get_close_button(self):
        close_button_rect = self.close_button.get_rect()
        return pygame.rect.Rect(self.rect.x + close_button_rect.x, self.rect.y + close_button_rect.y,
                                close_button_rect.width, close_button_rect.height)
