#!C:\Python33\python.exe
# -*- coding: utf-8 -*-

import os
import configparser

import pygame
from pygame.locals import *

import slg
from slg.camera import Camera
from slg.map.locals import *
from slg.map.map import Map
from slg.renderer import Renderer
import slg.ui as ui

PAUSED = 0
RUNNING = 1


class Scene(object):

    _surface = _target = None

    def __init__(self, vp):
        self._surface = pygame.Surface(vp)

    def set_target(self, surface):
        self._target = surface

    def draw(self, surface=None):
        if surface:
            self.set_target(surface)
        if self._target is not None:
            self._target.blit(self._surface, (0, 0))

    def append(self, surface, dest):
        self._surface.blit(surface, dest)

    def get_surface(self):
        return self._surface


class MenuScene(Scene):

    def __init__(self, vp):
        super().__init__(vp)
        transparent_surface = pygame.Surface(vp)
        transparent_surface.set_alpha(128)
        transparent_surface.fill((0, 0, 0))
        self.overlay = transparent_surface

    def draw(self, surface = None):
        if surface is not None:
            self.set_target(surface)
        self._target.blit(self.overlay, (0, 0))
        str = "Game Paused\n" \
              "mini-help\n" \
              "use arrow keys to move camera\n" \
              "use \"c\" key to center the map\n" \
              "use \"p\" to pause/run game"
        label = ui.TextWidget(str, (200, 0, 50))
        label.draw_to(self._target)


def main():

    config = configparser.ConfigParser()
    config.sections()
    config.read(os.path.join(os.getcwd(), "config", "main.ini"))

    # map_config
    l_map = config['MAIN']['map']

    # display config
    config_display = config['DISPLAY']
    display_width = int(config_display.get('width', 800))
    display_height = int(config_display.get('height', 600))
    display_tup = (display_width, display_height)

    fullscreen = int(config_display.get('fullscreen', 0))
    display_flags = 0
    if fullscreen == 1:
        display_flags |= FULLSCREEN
        videoinfo = pygame.display.Info()
        display_tup = (videoinfo.current_w, videoinfo.current_h)

    clr = (0, 0, 0)

    pygame.init()
    display = pygame.display.set_mode(display_tup, display_flags)

    map_surface = pygame.Surface(display_tup)


    menu = MenuScene(display_tup)

    clock = pygame.time.Clock()

    camera = Camera(display_tup)
    renderer = Renderer(map_surface, camera)

    loader = slg.map.loader.tmx.TmxLoader()

    l_map = os.path.realpath(os.path.join(os.getcwd(), "data", "maps", l_map))
    world_map = Map(l_map, renderer, loader)

    camera.set_dimensions(world_map.get_tile_dimensions(), world_map.get_map_dimensions())
    camera.reset_camera_to((0, 0))

    running = True
    state = RUNNING
    while running:
        previous_state = state
        for e in pygame.event.get():
            if state != PAUSED:
                if e.type == KEYDOWN:
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
                        camera.reset_camera_to((world_map.get_world_center()))
            if e.type == KEYDOWN:
                if (e.key == K_F4 and pygame.key.get_mods() and pygame.KMOD_ALT) or e.key == K_ESCAPE:
                    running = False
            if e.type == KEYUP:
                if e.key == K_p:
                    if state == PAUSED:
                        state = RUNNING
                        print('running')
                    else:
                        state = PAUSED
                        print('paused')

        if state == RUNNING:
            display.fill(clr)
            visible_area = camera.get_bounds()
            world_map.draw(visible_area)
            display.blit(map_surface, (0, 0))
            camera.update()
        elif state == PAUSED:
            if previous_state != state:
                menu.draw(display)
        pygame.display.update()
        clock.tick(30)
        # running = False

if __name__ == "__main__":
    main()