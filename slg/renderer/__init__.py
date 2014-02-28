__author__ = 'Den'

import pygame


class Renderer(object):

    __camera = None
    __surface = None

    def __init__(self, surface, camera):
        self.__surface = surface
        self.__camera = camera

    def translate(self, drawable):
        x, y = drawable.get_coordinates()
        width, height = drawable.get_dimensions
        offset_x, offset_y = drawable.get_offsets
        drawable.set_coordinates(x, y)

    def draw(self, drawable):
        camera_x, camera_y = self.__camera.get_dest()
        get_x, get_y = drawable.get_x() - camera_x, drawable.get_y() - camera_y
        # print(get_x, get_y)
        self.__surface.blit(drawable.get_image(), (get_x, get_y), drawable.get_rect())

    def get_camera_dimensions(self):
        return self.__camera.get_dimensions()
