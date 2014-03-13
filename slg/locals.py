__author__ = 'den'

import os

from pygame.locals import *

CONFIG_DIR = os.path.join(os.path.realpath(os.getcwd()), 'config')
MAIN_CONFIG = os.path.join(CONFIG_DIR, 'main.ini')
DATA_DIR = os.path.join(os.path.realpath(os.getcwd()), 'data')
MAP_DIR = os.path.join(DATA_DIR, 'maps')
SOUND_DIR = os.path.join(DATA_DIR, 'sound')
TILE_DIR = os.path.join(DATA_DIR, 'tiles')
MODELS_DIR = os.path.join(DATA_DIR, 'monsters')
GUI_DIR = os.path.join(DATA_DIR, 'gui')

GAME_STATE_PAUSED = 0
GAME_STATE_RUNNING = 1
GAME_STATE_LOADING = 2

EVENT_CHANGE_STATE = USEREVENT + 1
EVENT_LOAD_MAP = USEREVENT + 2
