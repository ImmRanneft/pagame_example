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

    app = Application(config)
    app.init()
    app.running(True)
    app.set_state(LOADING)

    app.run()

if __name__ == "__main__":
    main()