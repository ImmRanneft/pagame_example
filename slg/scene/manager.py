__author__ = "Den"

import slg
from slg.scene.loadingscene import LoadingScene
from slg.scene.menuscene import MenuScene
from slg.scene.mapscene import MapScene
from slg import RUNNING, LOADING, PAUSED

class Manager(object):

    _container = dict()
    _names = {'loading': 'LoadingScene', 'map': 'MapScene', 'menu': "MenuScene"}
    _app = None

    def __init__(self, app: slg.Application):
        self.set_app(app)

    def set_app(self, app):
        self._app = app

    def get(self, scene_name):
        scene = self._container.get(scene_name, False)
        if not scene:
            self._container[scene_name] = self._names[scene_name](self._app.display, self._app)

    def update(self):
        state = self._app.get_state()
        if state == LOADING:
            self._app.push_scene(self.get('loading'))
        elif state == RUNNING:
            self._app.push_scene(self.get('map'))
        elif state == PAUSED:
            self._app.push_scene(self.get('map'))
            self._app.push_scene(self.get('menu'))
