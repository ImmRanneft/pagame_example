__author__ = 'Den'

import pygame.rect
import pygame.draw

import slg.ui.bar
from slg.locals import *
from slg.ui.textwidget import TextWidget
from slg.event import ChangeState


class Dialog(slg.ui.bar.Bar):

    _layer = 'gui'

    _type = ''

    def __init__(self, name, size, surface, *groups, **styles):
        close_styles = {'text_color': styles.get('border_color', self.styles['border_color']),
                  'font_size': int(styles.get('font_size', self.styles['font_size']) +
                                   styles.get('font_size', self.styles['font_size']) * 20 / 100),
                  'font': 'alger',
                  'align': (TextWidget.RIGHT, TextWidget.TOP),
                  'border': styles.get('border', self.styles['border'])}
        self.close_button = TextWidget(*groups, **close_styles)
        self.close_button.set_text('X')
        size = (size[0]+self.close_button.get_rect().width, max(size[1], self.close_button.get_rect().height))
        self.image = pygame.Surface(size)

        super().__init__(name, size, *groups, **styles)
        surface_rect = pygame.rect.Rect(surface.get_rect())
        self.rect.move_ip(surface_rect.centerx - self.rect.w/2, surface_rect.centery - self.rect.h/2)
        self.close_button.draw(self.image)
        ChangeState(GAME_STATE_PAUSED).post()
        self.events['click'].connect(self._click)

    def _click(self, *args, **kwargs):
        rect = self.get_close_button()
        if rect.collidepoint(*kwargs['mouse_pos']):
            self.visible = 0
            self.dirty = 1
            self.kill()
            ChangeState(GAME_STATE_RUNNING).post()

    def get_name(self):
        return self._name

    def get_type(self):
        return self._type


