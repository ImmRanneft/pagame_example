__author__ = 'Den'

import pygame
import os
from slg.map.locals import *

class Tileset(object):

    __firstgid = 0
    """
    @param __image - loaded by pygame image surface
    """
    __image = None

    def __init__(self):
        self.__firstgid = 1
        self.__image = pygame.image.load(os.path.join(os.path.join(DATA_DIR, 'tiles'), 'isometric_grass_and_water.png')).convert_alpha()

    def get_image(self):
        return self.__image