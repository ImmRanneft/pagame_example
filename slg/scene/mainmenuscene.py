__author__ = 'Den'

import codecs

import pygame
import pygame.rect

import slg.ui.listview
import slg.ui.text
from slg.event.changestate import ChangeState
from slg.locals import *
from slg.map.selector import Selector
from slg.scene.abstractscene import AbstractScene
from slg.scene.group.gamescenegroup import GameSceneGroup


class MainMenuScene(AbstractScene):
    """
    @type image: SurfaceType
    @type rect: pygame.rect.RectType
    """

    image = None
    rect = None

    def __init__(self, manager):
        super().__init__(manager)
        self.group = GameSceneGroup(self)
        display_surface = self._manager.get_display()
        self.bg = pygame.Surface(display_surface.get_size())
        ChangeState(GAME_STATE_PAUSED).post()
        showMainText(display_surface, self.group)
        slg.ui.listview.ListView('Map list', [200, 200], display_surface, self.group)

    def handle_events(self, events):
        self.group.handle_events(events)
        for e in events:
            if e.type == KEYDOWN:
                self.handle_keypress(e.key, pygame.key.get_mods())

    def handle_keypress(self, key, modificated):
        if key == K_m and modificated & pygame.KMOD_ALT:
            Selector(self._manager.get_display(), self.group)
        if key == K_F1:
            showMainText(self._manager.get_display(), self.group)

    def draw(self):
        display_surface = self._manager.get_display()
        display_surface.blit(self.bg, (0, 0))
        self.group.update(display_surface)
        self.group.draw(display_surface)


def showMainText(display_surface, group):
    string = codecs.open(os.path.join(TEXTS_DIR, 'welcome.txt'), 'r', encoding='UTF-8').read()
    styles = {'font_size': 18, 'align': (ALIGN_LEFT, ALIGN_TOP), 'border': (10, 10)}
    txt = slg.ui.text.Text(string, display_surface, group, **styles)