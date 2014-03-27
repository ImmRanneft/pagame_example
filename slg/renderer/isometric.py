__author__ = 'den'

import pygame.rect
from slg.renderer.abstractrenderer import AbstractRenderer


class Isometric(AbstractRenderer):

    def map_to_screen(self, drawable):
        [x, y] = drawable.get_coordinates()
        [current_width, current_height] = drawable.get_dimensions()
        [regular_width, regular_height] = drawable.get_regular_tile_dimensions()
        [offset_x, offset_y] = drawable.get_offset()
        [camera_offset_x,  camera_offset_y] = [-x for x in self.camera.get_dest()]

        #this is additional offset for tiles that greater or lesser than regular tile
        dy = (current_height - 2 * offset_y - regular_height)
        dx = (current_width - 2 * offset_x) - regular_width

        tile_x = (x - y) * regular_width / 2 - offset_x - dx
        tile_y = (x + y) * regular_height / 2 - offset_y - dy

        tile_x -= camera_offset_x
        tile_y -= camera_offset_y

        new_rectangle = pygame.rect.Rect((tile_x, tile_y), (drawable.rect.width, drawable.rect.height))
        return new_rectangle

    def draw_map(self, layer, map_object):
        print(layer, map_object)
        for j in range(0, layer.get_dimensions()[1]):
            for i in range(0, layer.get_dimensions()[0]):
                try:
                    tile = layer.get([i, j])
                    if tile and tile.get_id() > 0:
                        tile_rect = self.map_to_screen(tile)
                        # tile_rect.x += img_size[0]/2
                        # image.blit(tile.image, tile_rect)
                except IndexError:
                    print(i, j)
                    exit()