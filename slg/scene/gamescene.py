__author__ = 'Den'

import codecs

import pygame.rect
import pygame.mouse
import pygame.image
import pygame.sprite

import slg.ui.text
import slg.ui.lifebar
import slg.map.map
import slg.renderer.staggered
import slg.entities.player

from slg.locals import *
from slg.scene.helper.gamemenu import GameMenu
from slg.event.changestate import ChangeState
from slg.scene.abstractscene import AbstractScene
from slg.scene.group.gamescenegroup import GameSceneGroup


class GameScene(AbstractScene):

    """
    @type group: GameSceneGroup
    """
    group = None
    keyboard_moving_x, keyboard_moving_y = False, False
    map_object = None
    renderer = None
    camera = None

    _instance = None

    def __init__(self, manager):
        super().__init__(manager)

    def set_map(self, map_object):
        self.map_object = map_object
        self.renderer = map_object.get_renderer()
        self.camera = self._manager.get_camera()

    def handle_events(self, events):
        self._manager.get_camera().handle_events(events, self._manager)
        self._manager.get_camera().update()
        for e in events:
            if e.type == KEYDOWN:
                self.handle_keypress(e.key, pygame.key.get_mods())

    def handle_keypress(self, key, modificated):
        if key == K_SPACE and self._manager.state < GAME_STATE_LOADING:
            ChangeState(int(not bool(self._manager.state))).post()

        if key == K_ESCAPE:
            GameMenu(self._manager.get_display(), self._manager, self.group)
            ChangeState(GAME_STATE_PAUSED).post()

    def draw(self):
        self._manager.get_display().fill((0, 0, 0))
        self.map_object.empty()
        self.map_object.update()
        self.map_object.draw(self._manager.get_display())