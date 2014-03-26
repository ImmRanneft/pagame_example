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
    _map_object = None

    _instance = None

    def __init__(self, manager):
        super().__init__(manager)

        self.group = GameSceneGroup(self)
        self.map_group = GameSceneGroup(self)

        self.player_group = GameSceneGroup(self)
        self.player = slg.entities.player.Player(self.player_group)
        self.player.set_camera(self._manager.get_camera())

        display_surface = self._manager.get_display()

        self.bg = pygame.Surface(display_surface.get_size())

        styles = {'font_size': 14, 'font': 'calibrii', 'text_color': (255, 255, 255), 'border': (5, 5)}
        slg.ui.lifebar.Lifebar(display_surface, self.group, **styles)

    def set_map(self, map_object):
        self._map_object = map_object
        self.player.set_map(map_object)
        for layer in self._map_object.get_layers():
            layer.add(self.map_group)
            layer.update(self._manager.get_camera())
            layer.draw(self._manager.get_display(), self._manager.get_camera())

    def get_group(self):
        return self.group

    def handle_events(self, events):
        self.group.handle_events(events)
        self.handle_player_events(events)
        # self.map_group.handle_events(events)
        camera = self._manager.get_camera()
        camera.update()
        camera.handle_events(events, self._manager)
        for e in events:
            if e.type == KEYDOWN:
                self.handle_keypress(e.key, pygame.key.get_mods())

    def handle_player_events(self, events):
        for e in events:
            if self._manager.state != GAME_STATE_PAUSED:
                if e.type == KEYDOWN:
                    if e.key == K_s:
                        self.player.set_moving_y(self._manager.get_camera().MOVEMENT_POSITIVE)
                        self.moving_y_key = K_s
                        print('moving down')
                    if e.key == K_w:
                        self.player.set_moving_y(self._manager.get_camera().MOVEMENT_NEGATIVE)
                        self.moving_y_key = K_w
                        print('moving up')
                    if e.key == K_d:
                        self.player.set_moving_x(self._manager.get_camera().MOVEMENT_POSITIVE)
                        self.moving_x_key = K_d
                        print('moving right')
                    if e.key == K_a:
                        self.player.set_moving_x(self._manager.get_camera().MOVEMENT_NEGATIVE)
                        self.moving_x_key = K_a
                        print('moving left')
                if e.type == KEYUP:
                    if (e.key == K_w or e.key == K_s) and e.key == self.moving_y_key:
                        self.player.set_moving_y(self._manager.get_camera().MOVEMENT_STOP)
                    if (e.key == K_a or e.key == K_d) and e.key == self.moving_x_key:
                        self.player.set_moving_x(self._manager.get_camera().MOVEMENT_STOP)

    def handle_keypress(self, key, modificated):
        if key == K_SPACE and self._manager.state < GAME_STATE_LOADING:
            ChangeState(int(not bool(self._manager.state))).post()

        if key == K_ESCAPE:
            GameMenu(self._manager.get_display(), self._manager, self.group)
            ChangeState(GAME_STATE_PAUSED).post()

    def draw(self):
        display_surface = self._manager.get_display()
        camera = self._manager.get_camera()
        self.map_group.update(camera)
        self.player_group.update()

        display_surface.fill((0, 0, 0, 0))
        self.bg.fill((0, 0, 0, 0))

        for layer in self._map_object.get_layers():
            layer.draw(self._manager.get_display(), self._manager.get_camera())

        # self.player_group.draw(self.bg)

        # display_surface.blit(self.bg, (0, 0))

        self.group.update(display_surface)
        self.group.draw(display_surface)

    def update(self):
        pass