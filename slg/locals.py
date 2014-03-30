__author__ = 'den'

import os

from pygame.locals import *

TPS = 0.25  # this is Tile Per Second Constant
FPS = 60  # Frames per second

CONFIG_DIR = os.path.join(os.path.realpath(os.getcwd()), 'config')
MAIN_CONFIG = os.path.join(CONFIG_DIR, 'main.ini')
DATA_DIR = os.path.join(os.path.realpath(os.getcwd()), 'data')
MAP_DIR = os.path.join(DATA_DIR, 'maps')
SOUND_DIR = os.path.join(DATA_DIR, 'sound')
TEXTS_DIR = os.path.join(DATA_DIR, 'text')
TILE_DIR = os.path.join(DATA_DIR, 'tiles')
MODELS_DIR = os.path.join(DATA_DIR, 'monsters')
GUI_DIR = os.path.join(DATA_DIR, 'gui')
FONTS_DIR = os.path.join(GUI_DIR, 'fonts')

GAME_STATE_PAUSED = 0
GAME_STATE_RUNNING = 1
GAME_STATE_LOADING = 2

ALIGN_CENTER = 0
ALIGN_TOP = 1
ALIGN_BOTTOM = 2
ALIGN_LEFT = 3
ALIGN_RIGHT = 4

EVENT_CHANGE_STATE = USEREVENT + 1
EVENT_LOAD_MAP = USEREVENT + 2
EVENT_MAP_LOADED = USEREVENT + 3
EVENT_MAIN_MENU = USEREVENT + 4
EVENT_MAP_UPDATED = USEREVENT + 5
