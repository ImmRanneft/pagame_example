__author__ = "Den"

import pygame
from slg.scene import Scene
import slg.ui as ui


class MenuScene(Scene):

    def __init__(self, display: pygame.display, app):

        super().__init__(display, app)
        transparent_surface = pygame.Surface(display.get_size())
        transparent_surface.set_alpha(128)
        transparent_surface.fill((0, 0, 0))
        self.image = transparent_surface
        self.rect = self.image.get_rect()
        str = "Game Paused\n" \
              "mini-help\n" \
              "use arrow keys to move camera\n" \
              "use \"c\" key to center the map\n" \
              "use \"p\" to pause/run game"
        self.label = ui.TextWidget((200, 200, 200))
        self.label.set_text(str)

    def update(self, surface=None):
        if surface is not None:
            self.set_target(surface)
        if self._target is not None:
            self._target.blit(self.image, (0, 0))
            self.label.set_target(self._target)
            self.label.draw()