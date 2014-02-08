#!C:\Python33\python.exe
# -*- coding: utf-8 -*-

from slg import *
from pygame.locals import *
import pygame

WIN_WIDTH = 640
WIN_HEIGHT = 480
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#004400"


PLATFORM_COLOR = "#FF6262"


class Camera(object):

    __current_x = __current_y = 0
    __width = __height = 0
    moving_x = moving_y = 0
    __left = __right = __top = __bottom = 0

    MOVEMENT_SPEED = 50
    MOVEMENT_POSITIVE = 1
    MOVEMENT_NEGATIVE = -1
    MOVEMENT_STOP = 0

    def __init__(self, display):
        self.__width = display[0]
        self.__height = display[1]

    def set_moving_x(self, movement):
        self.moving_x = movement

    def set_moving_y(self, movement):
        self.moving_y = movement

    def reset_camera_to(self, coordinates):
        if coordinates[0] is not False:
            self.__current_x = coordinates[0] - self.__width / 2
        if coordinates[1] is not False:
            self.__current_y = coordinates[1] - self.__height / 2

    def get_dest(self):
        return self.__current_x, self.__current_y

    def get_dimensions(self):
        return self.__width, self.__height

    def set_limits(self, left, right, top, bottom):
        self.__left, self.__right, self.__top, self.__bottom = left, right, top, bottom

    def update(self):
        if self.__current_x + self.__width / 2 < self.__right or self.__current_x - self.__width / 2 > self.__left:
            self.__current_x += self.moving_x * self.MOVEMENT_SPEED
        ''' we have to check another situation cause y coordinate on screen grows in direction of bottom '''
        new_y = self.__current_y + self.moving_y * self.MOVEMENT_SPEED
        # print(self.moving_y)
        if (self.moving_y < 1 and new_y < self.__top) or (self.moving_y > 1 and new_y + self.__height > self.__bottom):
            self.__current_y += self.moving_y * self.MOVEMENT_SPEED
        # print(self.__current_y, new_y, self.__top)


def main():

    pygame.init()

    display = pygame.display.set_mode(DISPLAY, DOUBLEBUF)
    color = (0, 0, 0)
    clock = pygame.time.Clock()

    camera = Camera(DISPLAY)
    renderer = Renderer(display, camera)
    tile_group = TileGroup()
    worldmap = Map(tile_group, renderer)
    worldmap.generate()
    left, right, top, bottom = worldmap.get_world_bounding_box()
    camera.set_limits(left, right, top, bottom)
    camera.reset_camera_to(worldmap.get_world_center())
    # camera.reset_camera_to(tile_group.get(1).get_x(), tile_group.get(1).get_y())

    running = True
    for t in tile_group.get():
        print(t.get_coordinates())
    while running:
        for e in pygame.event.get():
            if e.type == KEYDOWN:
                if (e.key == K_F4 and pygame.key.get_mods() and pygame.KMOD_ALT) or e.key == K_ESCAPE:
                    running = False
                if e.key == K_DOWN:
                    camera.set_moving_y(camera.MOVEMENT_POSITIVE)
                if e.key == K_UP:
                    camera.set_moving_y(camera.MOVEMENT_NEGATIVE)
                if e.key == K_RIGHT:
                    camera.set_moving_x(camera.MOVEMENT_POSITIVE)
                if e.key == K_LEFT:
                    camera.set_moving_x(camera.MOVEMENT_NEGATIVE)
            if e.type == KEYUP:
                if e.key == K_UP or e.key == K_DOWN:
                    camera.set_moving_y(camera.MOVEMENT_STOP)
                if e.key == K_LEFT or e.key == K_RIGHT:
                    camera.set_moving_x(camera.MOVEMENT_STOP)
                if e.key == K_c:

                    camera.reset_camera_to(worldmap.get_world_center())
        camera.update()
        display.fill(color)
        tile_group.draw()
        pygame.display.update()
        clock.tick(16)

if __name__ == "__main__":
    main()