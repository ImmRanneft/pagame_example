__author__ = 'den'

import pygame
import pygame.sprite
import pygame.rect


class Layer(pygame.sprite.DirtySprite):
    """
    Simple layer, that holds all this tiles and determinates which of them have to be drawn depending in visible_area
    @type _name: str
    @type _order: int
    @type image: pygame.SurfaceType
    @type rect: pygame.rect.Rect
    """

    _name = ''

    _order = 0

    _visible_area = {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}

    _container = [[]]

    image = None
    rect = None

    def __init__(self, *groups):
        super().__init__(*groups)

    # setters and getters
    def get_name(self):
        return self._name

    def set_name(self, name: str):
        self._name = name

    name = property(get_name, set_name)

    def get_order(self):
        return self._order

    def set_order(self, order: int):
        self._order = order

    def update(self, camera):
        camera_bounds = camera.get_bounds()

        for key, bound in camera_bounds:
            if self._visible_area[key] != bound:
                self._visible_area[key] = bound
                self.dirty = 1
        if self.dirty > 0:
            self._render(camera)

    def _render(self, camera):

        self.rect = pygame.rect.Rect((camera.get_dest()), self.image.get_size())

    order = property(get_order, set_order)
