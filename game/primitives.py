from abc import ABC, abstractmethod
from functools import reduce
from operator import add


class Primitive(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @property
    def values(self):
        return list(self.__dict__.values())

    @property
    def vertices(self):
        return list(reduce(add, [q.values for q in self.values]))


class ColorRGB(Primitive):
    def __init__(self, r: int, g: int, b: int):
        super().__init__()
        self.r = r
        self.g = g
        self.b = b


class Point(Primitive):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.x = x
        self.y = y


class Quad(Primitive):
    def __init__(self, ll: Point, lr: Point, tr: Point, tl: Point):
        super().__init__()
        self.ll = ll
        self.lr = lr
        self.tr = tr
        self.tl = tl


class Triangle(Primitive):
    def __init__(self, one: Point, two: Point, three: Point):
        super().__init__()
        self.one = one
        self.two = two
        self.three = three

