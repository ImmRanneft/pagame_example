__author__ = 'den'

import pygame.rect


class AbstractRenderer(object):

    camera = None

    def __init__(self):
        pass

    @staticmethod
    def calculate_surface_dimensions(dimensions, tile_dimensions):
        return [int(dimensions[0]*tile_dimensions[0]),
                int(dimensions[1]*tile_dimensions[1])]

    @staticmethod
    def calculate_tile_dimensions(tile_dimensions):
        return [tile_dimensions[0], tile_dimensions[1]]

    def set_camera(self, camera):
        self.camera = camera

    def get_camera_bounds(self):
        return self.camera.get_bounds()
