__author__ = "Den"

import pygame
from slg.scene.scene import Scene
import slg.ui as ui

class MenuScene(Scene):

    def __init__(self, vp):
        super().__init__(vp)
        transparent_surface = pygame.Surface(vp)
        transparent_surface.set_alpha(128)
        transparent_surface.fill((0, 0, 0))
        self.overlay = transparent_surface
        str = "Game Paused\n" \
              "mini-help\n" \
              "use arrow keys to move camera\n" \
              "use \"c\" key to center the map\n" \
              "use \"p\" to pause/run game"
        self.label = ui.TextWidget((200, 200, 200))
        self.label.set_text(str)

    def draw(self, surface = None):
        if surface is not None:
            self.set_target(surface)

        self._target.blit(self.overlay, (0, 0))
        self.label.set_target(self._target)
        self.label.draw()