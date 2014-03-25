__author__ = 'den'

import pygame.rect


class Orthogonal(object):

    def __init__(self):
        pass

    def map_to_screen(self, drawable):
        [x, y] = drawable.get_coordinates()
        [current_width, current_height] = drawable.get_dimensions()
        [regular_width, regular_height] = drawable.get_regular_tile_dimensions()
        [offset_x, offset_y] = drawable.get_offset()
        tile_x = regular_width * x
        tile_y = regular_width * y
        newrect = pygame.rect.Rect((tile_x, tile_y), (drawable.rect.width, drawable.rect.height))

        return newrect