__author__ = 'Den'

import slg.ui.text
import slg.scene.gamescene

from slg.locals import *
from slg.event.changestate import ChangeState
from slg.event.mainmenu import MainMenu


class GameMenu(slg.ui.text.Text):
    def __init__(self, surface, manager, *groups):
        self.manager = manager
        string_to_render = "Нажми меня, если хочешь в главное меню!"
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
