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
    __target = None
    main_surface_width, main_surface_height = 0, 0

    def __init__(self, color: tuple=(0, 0, 0), align: list=[CENTER, CENTER],
                 font_size: int=32, font: pygame.font.Font=None):
        """
        @type text str
        @type text tuple
        @type align bytearray
        @type font_size int
        @type font pygame.font.Font|None
        """

        if font is None:
            self.font = pygame.font.SysFont('arial', font_size)
        self.color = color
        self.align = align
        self.font_size = font_size

    def set_text(self, text: str):
        self.text = text.split("\n")
        self.text_surfaces = list()
        self._render()

    def set_target(self, surface: pygame.SurfaceType):
        self.__target = surface

    def _render(self):
        for text in self.text:
            font_render = self.font.render(text, True, self.color)
            font_rect = font_render.get_rect()
            self.main_surface_height += self.font.get_linesize()
            self.main_surface_width = max(font_rect.width, self.main_surface_width)
            self.text_surfaces.append(font_render)

    def draw(self):
        padding = (0, 0)
        surf_rect = self.__target.get_rect()
        w, h = surf_rect.width, surf_rect.height
        y = 0
        for index, text_surface in enumerate(self.text_surfaces):
            x = (self.main_surface_width - text_surface.get_rect().width) / 2
            y = index * self.font.get_linesize()
            padding = (x + (w-self.main_surface_width)/2, y + (h-self.main_surface_height)/2)
            self.__target.blit(text_surface, padding)
        print(w, h, x, y, padding, self.font_size)


