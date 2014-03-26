__author__ = 'den'

import pygame.rect


class Isometric(object):

    def __init__(self):
        pass

    @staticmethod
    def map_to_screen(drawable):
        [x, y] = drawable.get_coordinates()
        [current_width, current_height] = drawable.get_dimensions()
        [regular_width, regular_height] = drawable.get_regular_tile_dimensions()

        [offset_x, offset_y] = drawable.get_offset()

        #this is additional offset for tiles that greater or lesser than regular tile
        dy = (current_height - 2 * offset_y - regular_height)
        dx = (current_width - 2 * offset_x) - regular_width

        tile_x = (x - y) * regular_width / 2 - offset_x - dx
        tile_y = (x + y) * regular_height / 2 - offset_y - dy
        if drawable.get_id() == 999999:
            pass # print(x, y, tile_x, tile_y, [current_width, current_height], [regular_width, regular_height])

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
        img_size = image.get_size()
        for j in range(0, dimensions[1]):
            for i in range(0, dimensions[0]):
                try:
                    tile = container[i][j]
                    if tile and tile.get_id() > 0:
                        tile_rect = self.map_to_screen(tile)
                        tile_rect.x += img_size[0]/2
                        image.blit(tile.image, tile_rect)
                except IndexError:
                    print(i, j)
                    exit()