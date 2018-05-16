import pyglet
from typing import List
from functools import reduce
from operator import add
from game.primitives import Quad, Triangle, Point, ColorRGB


VERTEX_2INT = 'v2i'
VERTEX_4INT = 'v4i'
COLOR_RGB = 'c3B'
COLOR_RGBA = 'c4B'


class Graphics(object):
    def __init__(self, window: pyglet.window.Window):
        self.window = window

    @staticmethod
    def batch_quads(quads: List[Quad],
                    color: ColorRGB) -> list:
        vertices = list(reduce(add, [q.vertices for q in quads]))
        args = [
            int(len(vertices) / 2),
            pyglet.gl.GL_QUADS,
            None,
            (VERTEX_2INT, vertices),
            (COLOR_RGB, color.values * 4)
        ]
        # print(args)
        return args
        # pyglet.graphics.draw(*args)

    @staticmethod
    def batch_triangles(triads: List[Triangle], color: ColorRGB) -> list:
        vertices = list(reduce(add, [t.vertices for t in triads]))
        args = [
            int(len(vertices) / 2),
            pyglet.gl.GL_TRIANGLES,
            None,
            (VERTEX_2INT, vertices),
            (COLOR_RGB, color.values * 3 * len(triads))
        ]
        # print(args)
        return args
        # pyglet.graphics.draw(*args)

    @staticmethod
    def batch_points(points: List[Point], color: ColorRGB) -> list:
        vertices = list(reduce(add, [p.values for p in points]))
        args = [
            int(len(vertices) / 2),
            pyglet.gl.GL_POINTS,
            None,
            (VERTEX_2INT, vertices),
            (COLOR_RGB, color.values)
        ]
        # print(args)
        return args
        # pyglet.graphics.draw(*args)

# pyglet.gl.GL_LINES
# pyglet.gl.GL_LINE_LOOP
# pyglet.gl.GL_LINE_STRIP
# pyglet.gl.GL_TRIANGLE_STRIP
# pyglet.gl.GL_TRIANGLE_FAN
# pyglet.gl.GL_QUAD_STRIP
# pyglet.gl.GL_POLYGON
