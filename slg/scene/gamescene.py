__author__ = 'Den'

import codecs

import pygame.rect
import pygame.mouse
import pygame.image
import pygame.sprite

import slg.ui.text
import slg.ui.lifebar
import slg.map.map

from slg.locals import *
from slg.map.selector import Selector
from slg.event.changestate import ChangeState
from slg.scene.abstractscene import AbstractScene
from slg.scene.group.gamescenegroup import GameSceneGroup


class GameScene(AbstractScene):

    """
    @type group: GameSceneGroup
    """
    group = None
    keyboard_moving_x, keyboard_moving_y = False, False

    _instance = None

    def __init__(self, manager):
        super().__init__(manager)

        self.group = GameSceneGroup(self)

        display_surface = self._manager.get_display()

        self.bg = pygame.Surface(display_surface.get_size())
        self.bg.fill((0, 0, 0))
        styles = {'font_size': 14, 'font': 'calibrii', 'text_color': (255, 255, 255), 'border': (5, 5)}
        slg.ui.lifebar.Lifebar(display_surface, self.group, **styles)
        string = codecs.open(os.path.join(TEXTS_DIR, 'welcome.txt'), 'r', encoding='UTF-8').read()
        styles = {'font_size': 18, 'align': (ALIGN_LEFT, ALIGN_TOP)}
        slg.ui.text.Text(string, display_surface, self.group, **styles)
        self.map = slg.map.map.Map()
        self.map.load('test6.tmx')

    def get_group(self):
        return self.group

    def handle_events(self, events):
        self.group.handle_events(events)
        camera = self._manager.get_camera()
        camera.handle_events(events, self._manager)
        for e in events:
            if e.type == KEYDOWN:
                self.handle_keypress(e.key, pygame.key.get_mods())

    def handle_keypress(self, key, modificated):
        if key == K_SPACE and self._manager.state < GAME_STATE_LOADING:
            ChangeState(int(not bool(self._manager.state))).post()

        if key == K_m and modificated and pygame.KMOD_CTRL:
            Selector(self._manager.get_display(), self.group)
            ChangeState(GAME_STATE_PAUSED).post()

    def draw(self):
        display_surface = self._manager.get_display()

        self.group.clear(display_surface, self.bg)
        self.group.draw(display_surface)
        self.group.update(display_surface)

    def update(self):
        pass