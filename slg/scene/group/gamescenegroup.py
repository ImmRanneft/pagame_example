__author__ = 'Den'

import pygame.sprite
import pygame.rect
from pygame.locals import *

from slg.event.changestate import ChangeState
from slg.locals import *


class GameSceneGroup(pygame.sprite.OrderedUpdates):

    """
    @type _scene: slg.scene.abstractscene.AbstractScene
    """
    _scene = None

    def __init__(self, scene, *sprites, **kwargs):
        self._scene = scene
        super().__init__(*sprites, **kwargs)

    # def draw(self, surface):
    #     _sprites = self._spritelist
    #     print(_sprites)
    #     super().draw(surface)

    def handle_events(self, events):
        for e in events:
            if e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for sprite in self.sprites():
                    if sprite.rect.collidepoint(*mouse_pos):
                        sprite.events['click'](e, mouse_pos = mouse_pos)