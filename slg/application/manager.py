__author__ = 'Den'

from slg.locals import *
from slg.scene.loadingscene import LoadingScene
from slg.scene.gamescene import GameScene
from slg.scene.mainmenuscene import MainMenuScene
from slg.event import *


class Manager(object):
    """
    @type _application: slg.application.Application
    """
    _application = None
    _scenes = dict()

    def __init__(self, application):
        self._application = application

    def get_display(self):
        return self._application.get_display()

    def get_camera(self):
        """
        @rtype: slg.application.camera.Camera
        """
        return self._application.get_camera()

    def get_scene(self, key):
        instance = self._scenes.get(key, None)
        if not instance:
            instance = key(self)
            self._scenes[key] = instance
        return instance

    def del_scene(self, key):
        self._scenes[key] = None

    def get_time(self):
        return self._application.get_time()

    def handle(self, events):
        for e in events:
            if e.type == EVENT_CHANGE_STATE:
                self._application.set_state(e.state)
            if e.type == EVENT_LOAD_MAP:
                self._application.set_scene(self.get_scene(LoadingScene))
            if e.type == EVENT_MAIN_MENU:
                self._application.set_scene(self.get_scene(MainMenuScene))
            if e.type == EVENT_MAP_LOADED:
                ChangeState(GAME_STATE_RUNNING).post()
                game_scene = self.get_scene(GameScene)
                game_scene.set_map(e.map_object)
                self.del_scene(MainMenuScene)
                self._application.set_scene(game_scene)

    state = property(lambda self: self._application.get_state())