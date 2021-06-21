__author__ = 'Den'

from slg.ui.text import Text
import slg.scene.gamescene

from slg.locals import *
from slg.event.changestate import ChangeState
from slg.event.mainmenu import MainMenu


class DebugInfo(Text):
    def __init__(self, surface, manager, *groups):
        self.manager = manager
        strings = list()
        strings.append(str(manager.get_camera().get_dest()))
        strings.append(str(manager.get_scene(slg.scene.gamescene.GameScene).player))
        string_to_render = "\n".join(strings)
        styles = {'font_size': 18, 'font': 'calibrii', 'text_color': (255, 255, 255), 'border': (5, 5),
                  'align': (ALIGN_LEFT, ALIGN_TOP), 'bgcolor': (100, 100, 100)}
        super().__init__(string_to_render, surface, *groups, **styles)

    def _click(self, *args, **kwargs):
        self.manager.del_scene(slg.scene.gamescene.GameScene)
        self.kill()
        rect = self.get_close_button()
        if rect.collidepoint(*kwargs['mouse_pos']):
            self.visible = 0
            self.dirty = 1
            ChangeState(GAME_STATE_RUNNING).post()
        elif self.rect.collidepoint(*kwargs['mouse_pos']):
            ChangeState(GAME_STATE_PAUSED).post()
            MainMenu().post()
