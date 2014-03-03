#!C:\Python33\python.exe
# -*- coding: utf-8 -*-

import slg
import pygame
import os
import configparser
from slg.camera import Camera
from slg.map.locals import *
from pygame.locals import *
from slg.map.map import Map
from slg.renderer import Renderer
from slg.map.layer import Layer

BACKGROUND_COLOR = "#004400"


def main():
    config = configparser.ConfigParser()
    config.sections()
    config.read(os.path.join(os.getcwd(), "config", "main.ini"))
    l_map = config['MAIN']['map']
    config_display = config['DISPLAY']
    display_width = int(config_display.get('width', 800))
    display_height = int(config_display.get('height', 600))
    fullscreen = int(config_display.get('fullscreen', 0))
    pygame.init()

    display_tup = (display_width, display_height)
    display_flags = 0
    if fullscreen == 1:
        display_flags |= FULLSCREEN
        videoinfo = pygame.display.Info()
        display_tup = (videoinfo.current_w, videoinfo.current_h)

    display = pygame.display.set_mode(display_tup, display_flags)

    clr = (0, 0, 0)
    clock = pygame.time.Clock()

    camera = Camera(display_tup)
    renderer = Renderer(display, camera)

    loader = slg.map.loader.tmx.TmxLoader()

    l_map = os.path.realpath(os.path.join(os.getcwd(), "data", "maps", l_map))
    world_map = Map(l_map, renderer, loader)

    camera.set_dimensions(world_map.get_tile_dimensions(), world_map.get_map_dimensions())
    camera.reset_camera_to((0, 0))

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
                # if e.key == K_c:
                #     zz = layer.get([0, 0])
                #     camera.reset_camera_to((zz.get_x(), zz.get_y()))

        camera.update()
        display.fill(clr)
        visible_area = camera.get_bounds()
        world_map.draw(visible_area)

        pygame.display.update()
        clock.tick(30)
        # running = False

if __name__ == "__main__":
    main()