__author__ = 'Den'

import pygame.sprite
from slg.ui.event import Event


class Widget(pygame.sprite.DirtySprite):

    image = None
    rect = None
    dirty = 1
    visible = 1
    _layer = None

    _class = ''
    _id = ''

    events = ['click', 'close', 'init', 'focus', 'blur']
    default_styles = {'font_size': 32, 'font': 'calibri', 'text_color': (255, 255, 255), 'align': (0, 0), 'padding': (0, 0),
              'border': (0, 0), 'border_color': tuple(c/1.8 for c in (139, 69, 19)), 'bgcolor': (139, 69, 19)}

    styles = dict()

    def __init__(self, *groups, **styles):
        super().__init__(*groups)
        self._class = styles.get('class', '')
        self._id = styles.get('id', '')
        self.styles.update(self.default_styles)
        self.styles.update(styles)

        self.events = {e: Event() for e in self.events}

    def get_layer(self):
        return self._layer