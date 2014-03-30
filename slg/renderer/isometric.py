__author__ = 'den'

import pygame.rect
from slg.renderer.abstractrenderer import AbstractRenderer


class Isometric(AbstractRenderer):

    def map_to_screen(self, drawable):
        [x, y] = drawable.get_coordinates()
        [current_width, current_height] = drawable.get_dimensions()
        [regular_width, regular_height] = drawable.get_regular_tile_dimensions()
        [offset_x, offset_y] = drawable.get_offset()

        #this is additional offset for tiles that greater or lesser than regular tile
        dy = (current_height - 2 * offset_y - regular_height)
        dx = (current_width - 2 * offset_x) - regular_width

        tile_x = (x - y) * regular_width / 2 - offset_x - dx
        tile_y = (x + y) * regular_height / 2 - offset_y - dy

        new_rectangle = pygame.rect.Rect((tile_x, tile_y), (drawable.base_rect.width, drawable.base_rect.height))
        return new_rectangle

    def adjust_with_cam(self, drawable):
        [camera_offset_x,  camera_offset_y] = self.camera.get_dest()
        x = drawable.base_rect.x
        y = drawable.base_rect.y
        x -= camera_offset_x
        y -= camera_offset_y
        new_rectangle = pygame.rect.Rect((x, y), (drawable.base_rect.width, drawable.base_rect.height))
        return new_rectangle

    @staticmethod
    def screen_to_map(coordinates, tile_dimensions):
        twh = tile_dimensions[0]/2
        thh = tile_dimensions[1]/2
        x = (coordinates[0] / twh + coordinates[1] / thh) / 2
        y = (coordinates[1] / thh - (coordinates[0] / twh)) / 2
        return [x, y]

    def draw_map(self, layer, map_object):
        bounds = self.camera.get_bounds()
        dim = self.camera.get_dimensions()
        delta = layer._d_visible_area
        old_bounds = {}
        for key in bounds.keys():
            old_bounds[key] = bounds[key]-delta[key]
        layer._d_visible_area = {'left': 0, 'top': 0, 'right': 0, 'bottom': 0}

        # l = []
        for j in range(bounds['top'], bounds['bottom']):
            for i in range(bounds['left'], bounds['right']):
                try:
                    tile = layer.get([i, j])
                    if tile and tile.get_id() > 0:
                        tile.rect = self.adjust_with_cam(tile)
                        if - tile.rect.width < tile.rect.x < dim[0] \
                                and -tile.rect.height < tile.rect.y < dim[1] and tile.get_id() > 0:
                            map_object.add(tile)
                            # l.append(tile)
                except IndexError:
                    print(i, j)
                    exit()
        # l = sorted(l, key=lambda tile: tile.order)
        # map_object.add(*l)

        # if delta['bottom'] < 0:
        #     for j in range(bounds['bottom'], old_bounds['bottom']):
        #         for i in range(bounds['left'], bounds['right']):
        #             tile = layer.get([i, j])
        #             if tile:
        #                 map_object.remove(tile)
        # if delta['top'] > 0:
        #     for j in range(old_bounds['top'], bounds['top']):
        #         for i in range(bounds['left'], bounds['right']):
        #             tile = layer.get([i, j])
        #             if tile:
        #                 # if tile._coordinates[0] == 0:
        #                 print(tile)
        #                 map_object.remove(tile)
        # if delta['right'] < 0:
        #     for j in range(bounds['togp'], bounds['bottom']):
        #         for i in range(old_bounds['right'], bounds['right']):
        #             tile = layer.get([i, j])
        #             if tile:
        #                 map_object.remove(tile)
        # if delta['left'] > 0:
        #     for j in range(bounds['top'], bounds['bottom']):
        #         for i in range(bounds['left'], old_bounds['left']):
        #             tile = layer.get([i, j])
        #             if tile:
        #                 map_object.remove(tile)


        # if delta['left'] < 0:
            # print('moving left')
        # exit()
        # for j in range(old_bounds['top'], bounds['top']):
        #     for i in range(old_bounds['left'], bounds['left']):
        #         tile = layer.get([i, j])
        #         if tile and tile.get_id() > 0:
        #             tile.rect = self.map_to_screen(tile)
        #             if - tile.rect.width < tile.rect.x < dim[0] \
        #                     and -tile.rect.height < tile.rect.y < dim[1] and tile.get_id() > 0:
        #                 map_object.add(tile)
        #
        #

