#!C:\Python33\python.exe
# -*- coding: utf-8 -*-

from configparser import ConfigParser

import pygame
import pygame.sprite
import pygame.rect
from pygame import gfxdraw

from slg.application.application import Application
from slg.locals import *


class Test(pygame.sprite.Sprite):

    def __init__(self):
        self.image = pygame.Surface((64, 64))
        self.image.fill((255, 0, 0))
        self.rect = pygame.rect.Rect(self.image.get_rect())

    def update(self, move):
        print(move)
        print(self.rect.centerx, self.rect.topleft)
        self.rect.move(move, move)


def main():
    pygame.init()
    display = pygame.display.set_mode((400, 300))
    display.fill((0, 0, 0))
    rect = pygame.rect.Rect((20, 20), (100, 40))
    gfxdraw.box(display, rect, (139, 69, 20))
    run = True
    while(run):
        for e in pygame.event.get():
            if e.type == QUIT:
                run = False
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    run = False
        pygame.display.update()
    exit()
    config = ConfigParser()
    config.sections()
    config.read(MAIN_CONFIG)
    app = Application(config)
    app.init()
    app.run(True)

if __name__ == "__main__":
    main()