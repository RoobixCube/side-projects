"""
Abstract classes, which may not be implemented on their own, but from which other useful classes are derived
"""
from abc import ABC, abstractmethod
from typing import Dict, List
from random import Random
from game.graphics import Graphics
from game.primitives import ColorRGB, Point


class Part(ABC):
    """
    A member of a Constructable, which is constructed according to a manifest
    Has individual attributes which are determined by the construct method
    """
    def __repr__(self):
        return self.__class__.__name__ + str(self.__dict__)

    def __init__(self, parent_x: int, parent_y: int, parent_w: int, parent_h: int):
        self.parent_x = parent_x
        self.parent_y = parent_y
        self.parent_w = parent_w
        self.parent_h = parent_h
        self._x = None
        self._y = None
        self.x = None
        self.y = None
        self._height = None
        self._width = None

    @abstractmethod
    def construct(self, gen: Random) -> object:
        pass


class DrawablePart(Part):
    """
    A Part that can be drawn on the screen
    """
    def __init__(self, parent_x: int, parent_y: int, parent_w: int, parent_h: int):
        super().__init__(parent_x, parent_y, parent_w, parent_h)
        self.color = ColorRGB(200, 0, 200)

    def set_x(self, dt: int):
        self.x = self._x

    def set_y(self, dt: int):
        self.y = self._y

    # @property
    def get_height(self) -> int:
        return self._height

    # @property
    def get_width(self) -> int:
        return self._width

    def get_graphics(self) -> list:
        return Graphics.batch_points(points=[Point(self._x, self._y)], color=self.color)

    @abstractmethod
    def construct(self, gen: Random) -> object:
        pass


class Interaction(ABC):
    """
    A wrapper class for a function with signature accepting an actor and a reactor.
    """
    @abstractmethod
    def act(self, actor: object, reactor: object) -> dict:
        pass


class Constructable(ABC):
    """
    An object whose essential properties and/or interactions are not known until build time
    """
    def __repr__(self):
        return self.__class__.__name__ + str(self.parts)

    @staticmethod
    def __construct(gen: Random, manifest: List[Part]):
        for p in manifest:
            yield (p.construct(gen))

    def construct(self, gen: Random):
        """
        A construction method must be a method that accepts nothing but a seed as an argument
        """
        self.parts = list(self.__construct(gen=gen, manifest=self.manifest))

    def __init__(self):
        """

        """
        self.parts = []

    @property
    @abstractmethod
    def manifest(self) -> List[Part]:
        """
        The manifest contains initialized, but not constructed, parts.
        :return:
        """
        return []


class Interactable(ABC):
    """
    An object with a dictionary of interactions, mapping from object types to functions that execute on collision
    """
    def __init__(self, interactions: Dict[Constructable, Interaction]=None):
        """

        :param interactions:
        """
        self.interactions = interactions


class Drawable(ABC):
    """
    An object that has the ability to be drawn on the screen
    """
    @abstractmethod
    def get_graphics(self) -> list:
        """
        return the set of graphics to be drawn by a draw method
        :return:
        """
        raise NotImplementedError


#
# class BaseInteraction(object):
#     """
#     An object which is really just a function wrapper, defining interactions between one class and another
#     """
#     def __init__(self,
#                  allowed_f: List[AbstractConstruct],
#                  allowed_t: List[AbstractConstruct],
#                  interaction: function,
#                  ):
#         self.allowed_f = allowed_f
#         self.allowed_t = allowed_t
#         self.do = interaction
#
#     @abstractmethod
#     def __do(self, f: AbstractConstruct, t: AbstractConstruct):
#         """
#         Make f do a thing to t
#         :param f:
#         :param t:
#         :return:
#         """
