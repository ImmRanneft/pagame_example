__author__ = 'Den'

import os

from slg.ui.text import Text
from slg.locals import *
from slg.ui.textwidget import TextWidget
from slg.event.changestate import ChangeState
from slg.event.loadmap import LoadMap


class Selector(Text):

    def __init__(self, surface, *groups):
        maps = list()
        maps.append('Список карт: ')
        for root, dirs, files in os.walk(MAP_DIR):
            for file in files:
                name, ext = os.path.splitext(os.path.join(MAP_DIR, file))
                if ext == '.tmx':
                    maps.append(os.path.basename(name)+ext)
        string_to_render = "\n".join(maps)
        styles = {'font_size': 18, 'font': 'calibrii', 'text_color': (255, 255, 255), 'border': (5, 5),
                  'align': (ALIGN_LEFT, ALIGN_TOP)}
        super().__init__(string_to_render, surface, *groups, **styles)

    def _click(self, *args, **kwargs):
        rect = self.get_close_button()
        if rect.collidepoint(*kwargs['mouse_pos']):
            self.visible = 0
            self.dirty = 1
            self.kill()
            ChangeState(GAME_STATE_PAUSED).post()
        elif self.rect.collidepoint(*kwargs['mouse_pos']):
            ChangeState(GAME_STATE_LOADING).post()
            LoadMap('iso1.tmx').post()
