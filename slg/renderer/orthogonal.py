__author__ = 'den'

import pygame.rect


class Orthogonal(object):

    def __init__(self):
        pass

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

    @staticmethod
    def get_layer_surface_dimensions(dimensions, tile_dimensions):
        return [int(dimensions[0]*tile_dimensions[0]),
                int(dimensions[1]*tile_dimensions[1])]

    @staticmethod
    def calculate_tile_dimensions(tile_dimensions):
        return [tile_dimensions[0], tile_dimensions[1]]

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