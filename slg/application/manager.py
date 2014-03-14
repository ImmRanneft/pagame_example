__author__ = 'Den'

from slg.locals import *
from slg.scene.loadingscene import LoadingScene
from slg.scene.gamescene import GameScene
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

    def _get_scene(self, key):
        instance = self._scenes.get(key, None)
        if not instance:
            instance = key(self)
            self._scenes[key] = instance
        return instance

    def handle(self, events):
        for e in events:
            if e.type == EVENT_CHANGE_STATE:
                self._application.set_state(e.state)
            if e.type == EVENT_LOAD_MAP:
                ChangeState().post()
                self._application.set_scene(self._get_scene(LoadingScene))
            if e.type == EVENT_MAP_LOADED:
                ChangeState(GAME_STATE_RUNNING).post()
                self._application.set_scene(self._get_scene(GameScene))

    state = property(lambda self: self._application.get_state())