__author__ = "Den"

import pygame
import pygame.rect

from slg.ui.widget import Widget
from slg.locals import *

pygame.font.init()


class TextWidget(Widget):

    CENTER = ALIGN_CENTER
    TOP = ALIGN_TOP
    BOTTOM = ALIGN_BOTTOM
    LEFT = ALIGN_LEFT
    RIGHT = ALIGN_RIGHT

    font = None
    color = (0, 0, 0)
    text = ""
    align = [CENTER, CENTER]
    additional_padding = [0, 0]
    font_size = 32
    text_surfaces = list()
    text_surface = None
    padding = (0, 0)
    __target = None
    main_surface_width, main_surface_height = 0, 0

    def __init__(self, *groups, **styles):
        super().__init__(**styles)
        self.font = pygame.font.Font(os.path.join(FONTS_DIR, self.styles['font'] + '.ttf'), self.styles['font_size'])
        self.color = self.styles['text_color']
        self.align = self.styles['align']
        self.font_size = self.styles['font_size']
        self.additional_padding = self.styles['border']

    def set_text(self, text: str):
        self.text = text.split("\n")
        self.text_surfaces = list()
        self._render()

    def get_size(self):
        return self.main_surface_width, self.main_surface_height

    def _render(self):
        # bg = tuple(c/1.5 for c in self.color)
        for text in self.text:
            font_render = self.font.render(text, True, self.color)
            # colorkey = font_render.get_at((0, 0))
            # font_render.set_colorkey(colorkey)
            # font_render.convert_alpha()
            font_rect = font_render.get_rect()
            self.main_surface_height += self.font.get_linesize()
            self.main_surface_width = max(font_rect.width, self.main_surface_width)
            self.text_surfaces.append(font_render)
        self.main_surface_width += self.additional_padding[0]
        self.main_surface_height += self.additional_padding[1]

    def draw(self, surface):
        surf_rect = pygame.rect.Rect(surface.get_rect())
        w, h = surf_rect.width, surf_rect.height
        [h_align, v_align] = list(self.align)
        for index, text_surface in enumerate(self.text_surfaces):
            text_surface_rect = pygame.rect.Rect(text_surface.get_rect())
            x = (self.main_surface_width - text_surface_rect.width) / 2
            y = index * self.font.get_linesize()
            if h_align == self.CENTER:
                padding_x = x + (w-self.main_surface_width)/2 + self.additional_padding[0]/2
            elif h_align == self.RIGHT:
                padding_x = surf_rect.right - 1 - text_surface_rect.width - self.additional_padding[0]/2
            else:
                padding_x = 1 + self.additional_padding[0]/2
            if v_align == self.CENTER:
                padding_y = y + (h-self.main_surface_height)/2 + self.additional_padding[1]/2
            elif v_align == self.BOTTOM:
                padding_y = surf_rect.bottom - 1 - text_surface_rect.height - self.additional_padding[1]/2
            else:
                padding_y = y + self.additional_padding[1]/2
            self.padding = (padding_x + surf_rect.x, padding_y + surf_rect.y)
            surface.blit(text_surface, (padding_x, padding_y))

    def get_rect(self):
        return pygame.rect.Rect(self.padding, (self.main_surface_width, self.main_surface_height))