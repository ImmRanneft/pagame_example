__author__ = 'Den'

import pygame

class Tile(object):

    __coorinates = [0, 0]
    __display_coordinates = [0, 0]
    __rectangle = [0, 0, 0, 0]
    __dimensions = [0, 0]
    __offset = [0, 0]

    def __init__(self, coordinates, offset, dimensions):
        self.__coordinates = coordinates
        self.__offset = offset
        self.__dimensions = dimensions

