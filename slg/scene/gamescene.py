__author__ = 'Den'

import threading

import pygame.image
import pygame.mouse
import pygame.rect
import pygame.sprite

import slg.entities.player
import slg.map.map
import slg.renderer.staggered
import slg.ui.lifebar
import slg.ui.text
from slg.event.changestate import ChangeState
from slg.locals import *
from slg.scene.abstractscene import AbstractScene
from slg.scene.group.gamescenegroup import GameSceneGroup
from slg.scene.helper.debuginfo import DebugInfo
from slg.scene.helper.gamemenu import GameMenu


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
        self.map_group = GameSceneGroup(self)
        self.player = slg.entities.player.Player(self.map_group)
        self.player.set_manager(self._manager)

    def set_map(self, map_object):
        self.map_object = map_object
        self.player.set_map(self.map_object)
        self.renderer = map_object.get_renderer()
        self.camera = self._manager.get_camera()
        self.camera.set_dest_to(self.player)
        self.draw()

    def handle_events(self, events):
        self.camera.handle_events(events, self._manager)
        self.player.handle_events(events)
        self.map_group.handle_events(events)
        for e in events:
            if e.type == KEYDOWN:
                self.handle_keypress(e.key, pygame.key.get_mods())

    def handle_keypress(self, key, modificated):
        if key == K_SPACE and self._manager.state < GAME_STATE_LOADING:
            ChangeState(int(not bool(self._manager.state))).post()
        if key == K_F1:
            DebugInfo(self._manager.get_display(), self._manager, self.map_group)
        if key == K_ESCAPE:
            GameMenu(self._manager.get_display(), self._manager, self.map_group)
            ChangeState(GAME_STATE_PAUSED).post()
        if key == K_o:
            print(self.map_object)

    def draw(self):
        self.camera.update()
        self.map_object.update()
        self.map_group.update()
        self._manager.get_display().fill((0, 0, 0))
        self.map_object.draw(self._manager.get_display())
        self.map_group.draw(self._manager.get_display())


class MapUpdatingThread(threading.Thread):
    def __init__(self, map_object, manager):
        self._map_object = map_object
        self._manager = manager
        super().__init__()

    def run(self):
        print('start updating map ')
        self._map_object.update()
        pygame.event.post(EVENT_MAP_UPDATED)
        print('finished updating map ')
