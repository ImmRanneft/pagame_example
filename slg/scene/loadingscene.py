__author__ = 'Den'

import os

import pygame
import pygame.rect
from pygame.surface import Surface

from slg.scene.abstractscene import AbstractScene
from slg.event.changestate import ChangeState
from slg.event.loadmap import LoadMap
from slg.scene.group.gamescenegroup import GameSceneGroup
from slg.map.selector import Selector
from slg.locals import *
from slg.ui.textwidget import TextWidget


class LoadingScene(AbstractScene):
    """
    @type image: SurfaceType
    @type rect: pygame.rect.RectType
    """

    image = None
    rect = None

    def __init__(self, manager):
        """
        @type manager: slg.application.manager.Manager
        """
        super().__init__(manager)
        self.group = GameSceneGroup(self)
        image = pygame.image.load(os.path.join(GUI_DIR, 'loading_screen.jpg'))
        self.image = Surface(self._manager.get_display().get_size())
        self.rect = pygame.rect.Rect(self.image.get_rect())
        image_size = image.get_size()
        surface_size = self.image.get_size()
        x = int((image_size[0] - surface_size[0]) / 2)
        y = int((image_size[1] - surface_size[1]) / 2)
        if x < 0 and y < 0:
            image = pygame.transform.scale(image, surface_size)
            x, y = 0, 0
        elif x <= 0 <= y:
            image = pygame.transform.scale(image, (surface_size[0], image_size[1]))
            x = 0
        elif y <= 0 <= x:
            image = pygame.transform.scale(image, (image_size[0], surface_size[1]))
            y = 0
        styles = {'font': 'alger', 'font_size': 40, 'align': [TextWidget.CENTER, TextWidget.CENTER]}
        text = TextWidget(**styles)
        text.set_text("""Loading...
Please wait""")
        self.image.blit(image, (-x, -y))
        text.draw(self.image)

    def handle_events(self, events):
        self.group.handle_events(events)
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
        display_surface.blit(self.image, (0, 0))
        self.group.update(display_surface)
        self.group.draw(display_surface)




