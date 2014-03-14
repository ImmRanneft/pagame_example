__author__ = 'Den'

import os

from slg.ui.text import Text
from slg.locals import *
from slg.ui.textwidget import TextWidget


class Selector(Text):

    def __init__(self, surface, *groups, **styles):
        maps = list()
        maps.append('Список карт: ')
        for root, dirs, files in os.walk(MAP_DIR):
            for file in files:
                name, ext = os.path.splitext(os.path.join(MAP_DIR, file))
                if ext == '.tmx':
                    maps.append(os.path.basename(name)+ext)
        string_to_render = "\n".join(maps)
        super().__init__(string_to_render, surface, *groups, **styles)

