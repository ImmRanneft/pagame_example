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
        dy = current_height - 2 * offset_y - regular_height
        dx = current_width - 2 * offset_x - regular_width

        tile_x, tile_y = self.mts(x, y, regular_width, regular_height)

        tile_x -= offset_x + dx
        tile_y -= offset_y + dy

        new_rectangle = pygame.rect.Rect((tile_x, tile_y), (drawable.base_rect.width, drawable.base_rect.height))
        return new_rectangle

    @staticmethod
    def mts(x, y, tw, th):
        screen_x = (x - y) * tw / 2
        screen_y = (x + y) * th / 2
        return screen_x, screen_y

    def adjust_with_cam(self, rect):
        [camera_offset_x,  camera_offset_y] = self.camera.get_dest()
        x = rect.x
        y = rect.y
        x -= camera_offset_x
        y -= camera_offset_y
        new_rectangle = pygame.rect.Rect((x, y), (rect.width, rect.height))
        return new_rectangle

    @staticmethod
    def screen_to_map(x, y, tw, th):
        twh = tw/2
        thh = th/2
        map_x = (x / twh + y / thh) / 2
        map_y = (y / thh - x / twh) / 2
        return [map_x, map_y]

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
                        tile.rect = self.adjust_with_cam(tile.base_rect)
                        if - tile.rect.width < tile.rect.x < dim[0] \
                                and -tile.rect.height < tile.rect.y < dim[1] and tile.get_id() > 0:
                            map_object.add(tile)
                            # l.append(tile)
                except IndexError:
                    print(i, j)
                    exit()

        # here we have strange logic:
        # if we are moving left to right, then it`s obvious that delta left have to be positive
        # so we kill tiles that left outside left edge of camera
        # we have our loop like this from top to bottom and from left to right,
        # old_bounds['left'] becomes left, and bounds['left'] becomes right

        # just collect the sprites, and then kill them in one shot... i mean method call
        sprites_to_kill = list()

        # ok, we`re going left to right
        if delta['left'] > 0:
            for j in range(bounds['top'], bounds['bottom']):
                for i in range(old_bounds['left'], bounds['left']):
                    tile = layer.get([i, j])
                    if tile:
                        sprites_to_kill.append(tile)
        # going right to left
        # so bounds['right'] becomes left and old_bounds['right'] becomes right
        if delta['left'] < 0:
            for j in range(bounds['top'], bounds['bottom']):
                for i in range(bounds['right'], old_bounds['right']):
                    tile = layer.get([i, j])
                    if tile:
                        sprites_to_kill.append(tile)
        # now we`re going top to bottom, this means top row have to be removed
        # and bounds['top'] becomes bottom and old_bounds['top'] becomes top
        if delta['top'] > 0:
            for j in range(old_bounds['top'], bounds['top']):
                for i in range(bounds['left'], bounds['right']):
                    tile = layer.get([i, j])
                    if tile:
                        sprites_to_kill.append(tile)
        # versa
        if delta['top'] < 0:
            for j in range(bounds['bottom'], old_bounds['bottom']):
                for i in range(bounds['left'], bounds['right']):
                    tile = layer.get([i, j])
                    if tile:
                        sprites_to_kill.append(tile)
        if len(sprites_to_kill) > 0:
            # print(map_object)
            # print(len(sprites_to_kill), ' was removed')
            map_object.remove(sprites_to_kill)
            # print(map_object)
