__author__ = 'den'

from collections import OrderedDict

import pygame
import pygame.rect
import pygame.sprite

from slg.ui.bar import Bar
from slg.locals import *
from slg.ui.listitem import ListItem


class ListView(Bar, pygame.sprite.Group):

    _layer = 'gui'

    _type = ''

    def __init__(self, name, size, surface, *groups, **styles):
        self.image = pygame.Surface(size)
        super(Bar, ListView).__init__(name, size, *groups, **styles)
        super(pygame.sprite.Sprite, ListView).__init__()
        surface_rect = pygame.rect.Rect(surface.get_rect())
        self.rect.move_ip(surface_rect.centerx - self.rect.w/2, surface_rect.centery - self.rect.h/2)
        self.events['click'].connect(self._click)

    def _click(self, *args, **kwargs):
        print(args, kwargs)

    def get_name(self):
        return self._name

    def get_type(self):
        return self._type