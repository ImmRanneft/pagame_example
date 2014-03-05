#!C:\Python33\python.exe
# -*- coding: utf-8 -*-

import os
import configparser

import pygame
from pygame.locals import *

import slg
import slg.scene.menuscene
import slg.scene.mapscene
import slg.scene.loadingscene
from slg.map.locals import *
from slg import Application, RUNNING, PAUSED, LOADING


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

    app = Application(display)

    clock = pygame.time.Clock()

    s_menu = slg.scene.menuscene.MenuScene(display_tup, app)

    s_map = slg.scene.mapscene.MapScene(display, app)
    l_map = os.path.realpath(os.path.join(os.getcwd(), "data", "maps", l_map))
    s_map.set_map(l_map)
    s_map.set_target(display)

    s_loading = slg.scene.loadingscene.LoadingScene(display_tup, app)
    s_loading.set_target(display)

    app.running(True)

    while app.running():
        if app.get_state() == LOADING:
            app.push_scene(s_loading)
        elif app.get_state() == RUNNING:
            display.fill(clr)
            app.push_scene(s_map)
        elif app.get_state() == PAUSED:
            app.push_scene(s_map)
            app.push_scene(s_menu)
        app.update()
        # exit()
        pygame.display.update()
        clock.tick(30)
        # running = False

if __name__ == "__main__":
    main()