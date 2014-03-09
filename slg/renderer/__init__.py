__author__ = 'Den'

import slg

class Renderer(object):

    __camera = None
    __surface = None

    def __init__(self, surface, camera):
        self.__surface = surface
        self.__camera = camera

    def translate(self, drawable: slg.map.tile.Tile):
        [x, y] = drawable.get_coordinates()
        [current_width, current_height] = drawable.get_dimensions()
        [regular_width, regular_height] = drawable.get_regular_tile_dimensions()
        [offset_x, offset_y] = drawable.get_offset()
        camera_x, camera_y = self.__camera.get_dest()

        tile_x = current_width * x + \
                 int(y) % 2 * current_width/2

        divider = (current_height - 2 * offset_y) / regular_height * 2
        tile_y = current_height / divider * y
        dy = current_height - regular_height - offset_y + offset_y * y
        tile_y -= dy

        return [tile_x - camera_x, tile_y - camera_y]

    def draw(self, drawable):
        camera_x, camera_y = self.__camera.get_dest()
        try:
            get_x, get_y = drawable.get_x() - camera_x, drawable.get_y() - camera_y
            # print(get_x, get_y)
            self.__surface.blit(drawable.get_image(), self.translate(drawable), drawable.get_rect())
        except AttributeError:
            drawable
            # print(drawable)

    def get_camera_dimensions(self):
        return self.__camera.get_dimensions()
