__author__ = 'den'

import pygame.rect
from slg.renderer.abstractrenderer import AbstractRenderer


class Orthogonal(AbstractRenderer):

    @staticmethod
    def map_to_screen(drawable):
        [x, y] = drawable.get_coordinates()
        [current_width, current_height] = drawable.get_dimensions()
        [regular_width, regular_height] = drawable.get_regular_tile_dimensions()
        [offset_x, offset_y] = drawable.get_offset()
        tile_x = regular_width * x
        tile_y = regular_width * y
        newrect = pygame.rect.Rect((tile_x, tile_y), (drawable.rect.width, drawable.rect.height))

        return newrect

    def draw_map(self, dimensions, container, image):
        for i in range(0, dimensions[0]):
            for j in range(0, dimensions[1]):
                try:
                    tile = container[i][j]
                    if tile and tile.get_id() > 0:
                        tile_rect = self.map_to_screen(tile)
                        image.blit(tile.image, tile_rect)
                except IndexError:
                    print(i, j)
                    exit()