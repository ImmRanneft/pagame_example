__author__ = 'Den'

import pygame


class Renderer(object):

    __camera = None
    __surface = None

    def __init__(self, surface, camera):
        self.__surface = surface
        self.__camera = camera

    def draw(self, drawable):
        camera_x, camera_y = self.__camera.get_dest()
        cam_width, cam_height = self.__camera.get_dimensions()
        # if camera_y < drawable.get_y() < camera_y + drawable.get_height()*2 + cam_height * 3/2  \
        #    and camera_x -cam_width * 3/2 < drawable.get_x() < camera_x + cam_width * 3/2:
        self.__surface.blit(drawable.get_image(), (drawable.get_x() - camera_x, drawable.get_y() - camera_y), drawable.get_rect())
        # print(camera_x, drawable.get_x())

    def get_camera_dimensions(self):
        return self.__camera.get_dimensions()
