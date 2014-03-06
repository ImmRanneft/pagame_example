__author__ = "Den"

import slg
from slg.scene.loadingscene import LoadingScene
from slg.scene.menuscene import MenuScene
from slg.scene.mapscene import MapScene
import os


class Manager(object):

    _container = dict()
    _app = None

    def __init__(self, app):
        self.set_app(app)
        s_menu = slg.scene.menuscene.MenuScene(app.display, app)
        s_menu.set_target(app.display)

        s_map = slg.scene.mapscene.MapScene(app.display, app)
        # map_config
        l_map = app.config['MAIN']['map']
        l_map = os.path.realpath(os.path.join(os.getcwd(), "data", "maps", l_map))
        s_map.set_map(l_map)
        s_map.set_target(app.display)

        s_loading = slg.scene.loadingscene.LoadingScene(app.display, app)
        s_loading.set_target(app.display)
        self._container['loading'] = s_loading
        self._container['menu'] = s_menu
        self._container['map'] = s_map

    def set_app(self, app):
        self._app = app

    def get(self, scene_name):
        scene = self._container.get(scene_name, False)
        return scene

    def update(self):
        state = self._app.get_state()
        if state == slg.LOADING:
            self._app.push_scene(self.get('loading'))
        elif state == slg.RUNNING:
            self._app.push_scene(self.get('map'))
        elif state == slg.PAUSED:
            self._app.push_scene(self.get('map'))
            self._app.push_scene(self.get('menu'))
