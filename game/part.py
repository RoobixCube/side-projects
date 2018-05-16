"""
Constructor objects, which wrap a single seed-generation function
"""
from game.abstract import DrawablePart
from game.graphics import Graphics
from game.primitives import Point, Triangle, Quad, ColorRGB
from random import Random, randint
from pyglet import clock


class Trunk(DrawablePart):

    def set_x(self, dt: int):
        if self.sway_right:
            if self.x < self._x + self.jitter:
                self.x += 1
            if self.x == self._x + self.jitter:
                self.sway_right = False
        elif self.x > self._x - self.jitter:
            self.x -= 1
            if self.x == self._x - self.jitter:
                self.sway_right = True

    def __init__(self, parent_x: int, parent_y: int, parent_w: int, parent_h: int):
        super().__init__(parent_x, parent_y, parent_w, parent_h)
        self.jitter = 2
        self._x = int(parent_x + (parent_w / 2))
        self.sway_right = True
        self._y = parent_y

        self.x = randint(self._x - self.jitter, self._x + self.jitter)
        self.y = self._y

        clock.schedule_interval(self.set_x, 0.25)

    def construct(self, gen: Random):
        super().construct(gen)
        self._height = gen.randint(int(self.parent_h / 3), int(self.parent_h * 2 / 3))
        self._width = min(gen.randint(self.parent_w/4, self.parent_w/2), int(self.get_height() * 3 / 8))
        self.color = ColorRGB(
            r=gen.randint(40, 100),
            g=gen.randint(20, 65),
            b=gen.randint(0, 20)
        )
        return self

    def get_graphics(self):
        half_w = int(self.get_width() / 2)
        quad = Quad(
            ll=Point(self._x - half_w, self.y),
            lr=Point(self._x + half_w, self.y),
            tr=Point(self.x + half_w, self.y + self.get_height()),
            tl=Point(self.x - half_w, self.y + self.get_height()),
        )
        return Graphics.batch_quads(
            quads=[quad],
            color=self.color,
        )


class Leaves(DrawablePart):

    def set_x(self, dt):
        def jitter():
            return randint(-self.x_jitter, self.x_jitter)
        self.x = self._x + jitter()

    def set_y(self, dt):
        def jitter():
            return randint(-self.y_jitter, self.y_jitter)
        self.y = self._y + jitter()

    def __init__(self, parent_x: int, parent_y: int, parent_w: int, parent_h: int,
                 get_trunk_y: classmethod, get_trunk_w: classmethod):
        super().__init__(parent_x, parent_y, parent_w, parent_h)
        self.get_trunk_y = get_trunk_y
        self.get_trunk_w = get_trunk_w
        self.x_jitter = 1
        self.y_jitter = 3
        self.t_num = 1
        self.t_variance = 1

        clock.schedule_interval(self.set_x, 0.50)
        clock.schedule_interval(self.set_y, 0.12)

    def construct(self, gen: Random):
        self._x = int(self.parent_x + (self.parent_w / 2))
        self._y = self.parent_y + self.get_trunk_y()

        self.set_x(0)
        self.set_y(0)

        self.t_num = gen.randint(1, 4)
        self.t_variance = int(self.t_num / gen.randint(1, self.t_num))

        self._height = self.parent_h - self.get_trunk_y()
        self._width = gen.randint(max(self.parent_w / 4, self.get_trunk_w()) + (2 * self.x_jitter), self.parent_w)
        self.color = ColorRGB(
            r=gen.randint(0, 50),
            g=gen.randint(50, 255),
            b=gen.randint(0, 50)
        )
        return self

    def get_graphics(self):
        half_w = int(self.get_width() / 2)

        def get_triangle(__x, __y, __half_w):
            return Triangle(
                one=Point(__x - __half_w, __y),
                two=Point(__x + __half_w, __y),
                three=Point(__x, __y + self.get_height())
            )
        triads = list()
        y_diff = int(self._height / self.t_num)
        for n in range(self.t_num):
            __y = self._y + (n * y_diff)
            __half_w = half_w - (n * self.t_variance)
            triads.append(get_triangle(self.x, __y, __half_w))

        # triad = Triangle(
        #     one=Point(self.x - half_w, self._y),
        #     two=Point(self.x + half_w, self._y),
        #     three=Point(self.x, self.y + self.get_height())
        # )
        return Graphics.batch_triangles(
            triads=triads,
            color=self.color,
        )
