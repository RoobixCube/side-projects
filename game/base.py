"""
Base classes, which may be implemented on their own, or from which other useful classes are derived
"""
from game.abstract import *
from game.part import *
from uuid import uuid4, UUID
import pyglet
from typing import List


class BaseGame(object):
    """
    Overarching construct container
    """
    assets = {}

    @property
    def drawables(self) -> List[Drawable]:
        """
        Generate set of drawable assets
        :return:
        """
        for a in self.assets:
            if hasattr(a, "get_graphics"):
                yield a

    def __init__(self, constructables: List[Constructable], screen: pyglet.window.Window, local_seed: UUID=None):
        self.assets = constructables

        local_seed = local_seed or uuid4()
        self.gen = Random(x=local_seed.bytes)

        self.screen = screen

        @screen.event
        def on_draw():
            screen.clear()
            self.__draw_all()

        def update(dt):
            if dt:
                pass

        pyglet.clock.schedule_interval(update, 1 / 12.0)

    def __draw_all(self):
        batch = pyglet.graphics.Batch()
        for d in self.drawables:
            for a in d.get_graphics():
                batch.add(*a)
        # list(batch.add(*d.get_graphics()) for d in self.assets if hasattr(d, "draw"))

        batch.draw()

    def build(self):
        for a in self.assets:
            print("Building ", a)
            a.construct(gen=self.gen)

    def start(self, window_title: str=None):
        self.screen.set_caption(window_title)
        self.__draw_all()
        self.screen.activate()
        pyglet.app.run()


class TreeAsset(Constructable, Drawable):  # , Interactable):
    """
    A dynamically generated game asset which can interact with other similar assets
    """

    def __init__(self, x: int, y: int, w: int, h: int):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.trunk = Trunk(self.x, self.y, self.w, self.h)
        self.leaves = Leaves(self.x, self.y, self.w, self.h,
                             get_trunk_y=self.trunk.get_height, get_trunk_w=self.trunk.get_width)

    def construct(self, gen: Random):
        super().construct(gen)

    @property
    def manifest(self) -> List[Part]:
        return [
            self.trunk,
            self.leaves
        ]

    def get_graphics(self):
        """
        Draw on the screen
        :return:
        """
        for p in self.parts:
            if hasattr(p, "get_graphics"):
                yield p.get_graphics()
