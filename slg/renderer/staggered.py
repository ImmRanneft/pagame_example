__author__ = 'den'

import pygame.rect


class Staggered(object):

    def __init__(self):
        pass

    def map_to_screen(self, drawable):
        [x, y] = drawable.get_coordinates()
        [current_width, current_height] = drawable.get_dimensions()
        [regular_width, regular_height] = drawable.get_regular_tile_dimensions()
        [offset_x, offset_y] = drawable.get_offset()

        tile_x = current_width * x + \
                 int(y) % 2 * current_width/2

        divider = (current_height - 2 * offset_y) / regular_height * 2
        tile_y = current_height / divider * y
        dy = current_height - regular_height - offset_y + offset_y * y
        tile_y -= dy

        return drawable.rect.move(tile_x, tile_y)