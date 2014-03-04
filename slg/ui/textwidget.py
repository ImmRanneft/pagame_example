__author__ = "Den"

CENTER = 0
TOP = 1
BOTTOM = 2
LEFT = 3
RIGHT = 4

import pygame

pygame.font.init()


class TextWidget(object):

    font = None
    color = (0, 0, 0)
    text = ""
    align = [CENTER, CENTER]
    font_size = 32
    text_surfaces = list()
    text_surface = None

    def __init__(self, text, color=(0, 0, 0), align=[CENTER, CENTER], font_size = 32, font=None):
        self.text = text.split("\n")
        if font is None:
            self.font = pygame.font.SysFont('arial', font_size)
        self.color = color
        self.align = align
        self.font_size = font_size

    def draw_to(self, surface):

        surf_rect = surface.get_rect()
        w, h = surf_rect.width, surf_rect.height
        main_surface_height = 0
        main_surface_width = 0
        for text in self.text:
            font_render = self.font.render(text, True, self.color)
            font_rect = font_render.get_rect()
            main_surface_height += font_rect.height
            main_surface_width = max(font_rect.width, main_surface_width)
            self.text_surfaces.append(font_render)

        main_surface = pygame.Surface((main_surface_width, main_surface_height))
        cur_height = 0
        for text_surface in self.text_surfaces:
            dest = [0, 0]
            dest[0] = (main_surface_width - text_surface.get_rect().width) / 2
            cur_height += text_surface.get_rect().height + self.font_size / 4
            dest[1] = cur_height
            main_surface.blit(text_surface, dest)

        padding = ((w-main_surface_width)/2, (h-main_surface_height)/2)
        surface.blit(text_surface, padding)