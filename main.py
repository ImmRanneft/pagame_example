#!C:\Python33\python.exe
# -*- coding: utf-8 -*-

from slg import *
from pygame.locals import *
import pygame
import math

BACKGROUND_COLOR = "#004400"


class Camera(object):

    __current_x = __current_y = 0
    __width = __height = 0
    moving_x = moving_y = 0
    __left = __right = __top = __bottom = 0

    MOVEMENT_SPEED = 40
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

    def update(self):
        self.__current_x += self.moving_x * self.MOVEMENT_SPEED
        self.__current_y += self.moving_y * self.MOVEMENT_SPEED

    def get_bounds(self):
        left = math.floor(self.__current_x / TILE_WIDTH - 1)
        right = math.ceil((self.__current_x + self.__width) / TILE_WIDTH + 1)

        top = math.floor(self.__current_y / TILE_HEIGHT * 4 - 2)
        bottom = math.ceil((self.__current_y + self.__height) / TILE_HEIGHT * 4 + 2)

        return left, right, top, bottom


def main():

    pygame.init()

    videoinfo = pygame.display.Info()
    DISPLAY = (videoinfo.current_w, videoinfo.current_h)

    display = pygame.display.set_mode(DISPLAY, FULLSCREEN)

    clr = (0, 0, 0)
    clock = pygame.time.Clock()

    camera = Camera(DISPLAY)
    renderer = Renderer(display, camera)
    tile_group = TileGroup(MAP_WIDTH_IN_TILES, MAP_HEIGHT_IN_TILES)
    worldmap = Map(tile_group, renderer)
    worldmap.generate()
    camera.reset_camera_to((0, 0))
    tile_group.draw()
    # camera.reset_camera_to(tile_group.get(1).get_x(), tile_group.get(1).get_y())

    running = True

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
                    camera.reset_camera_to((0, 0))
        camera.update()
        display.fill(clr)
        left, right, top, bottom = camera.get_bounds()
        tile_group.set_area(left, right, top, bottom)
        tile_group.draw()

        pygame.display.update()
        clock.tick(30)
        # running = False

if __name__ == "__main__":
    main()