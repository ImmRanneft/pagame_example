#!C:\Python33\python.exe
# -*- coding: utf-8 -*-

from configparser import ConfigParser

import slg.event.loadmap
from slg.application import Application
from slg.locals import *


def main():
    config = ConfigParser()
    config.sections()
    config.read(MAIN_CONFIG)
    app = Application(config)
    app.init()
    app.run(True)

if __name__ == "__main__":
    main()