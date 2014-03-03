__author__ = 'Den'

import math

class Camera(object):

    __current_x = __current_y = 0
    __width = __height = 0
    moving_x = moving_y = 0
    __left = __right = __top = __bottom = 0
    __tile_width = __tile_height = 0
    __map_width = __map_height = 0

    __edges = {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}

    MOVEMENT_SPEED = 40
    MOVEMENT_POSITIVE = 1
    MOVEMENT_NEGATIVE = -1
    MOVEMENT_STOP = 0

    def __init__(self, display):
        self.__width = display[0]
        self.__height = display[1]

    def set_dimensions(self, tile_dimensions, map_dimensions):
        self.__tile_width = tile_dimensions[0]
        self.__tile_height = tile_dimensions[1]
        self.__map_width = map_dimensions[0]
        self.__map_height = map_dimensions[1]

        self.__edges['left'] = tile_dimensions[0]/2
        self.__edges['top'] = tile_dimensions[1]/2
        self.__edges['right'] = map_dimensions[0] * tile_dimensions[0] - tile_dimensions[0]/2
        self.__edges['bottom'] = map_dimensions[1] * tile_dimensions[1] / 2 - tile_dimensions[1]/2

    def set_moving_x(self, movement):
        self.moving_x = movement

    def set_moving_y(self, movement):
        self.moving_y = movement

    def reset_camera_to(self, coordinates):
        if coordinates[0] is not False:
            self.__current_x = coordinates[0] * self.__tile_width - self.__width / 2
        if coordinates[1] is not False:
            self.__current_y = coordinates[1] * self.__tile_height / 2  - 3 / 2 * self.__height

    def get_dest(self):
        return self.__current_x, self.__current_y

    def get_dimensions(self):
        return self.__width, self.__height

    def update(self):
        self.__current_x += self.moving_x * self.MOVEMENT_SPEED
        if self.__current_x < self.__edges['left'] -500:
            self.__current_x = self.__tile_width - 500
        if self.__current_x + self.__width > self.__edges['right']:
            self.__current_x = self.__edges['right'] - self.__width - self.__tile_width / 2
        self.__current_y += self.moving_y * self.MOVEMENT_SPEED
        if self.__current_y < self.__edges['top']-500:
            self.__current_y = self.__tile_height-500
        if self.__current_y + self.__height > self.__edges['bottom']:
            self.__current_y = self.__edges['bottom'] - self.__height - self.__tile_height / 2

    def get_bounds(self):
        left = math.floor(self.__current_x / self.__tile_width - 1)
        left = left if 0 < left else 0
        right = math.ceil((self.__current_x + self.__width) / self.__tile_width + 1)
        right = right if right < self.__map_width else self.__map_width
        top = math.floor(self.__current_y / self.__tile_height - 1)
        top = top if 0 < top else 0
        bottom = math.ceil((self.__current_y + self.__height) / (self.__tile_height / 2) + 1)
        bottom = bottom if bottom < self.__map_height else self.__map_height

        return left, right, top, bottom
