"""Quad wrappers"""
from _renderlib import ffi
from matlib.vec import Vec


class Quad:
    def __init__(self, width, height, ptr=None):
        self._ptr = ptr or ffi.new('struct Quad*')
        self.width = width
        self.height = height

    @property
    def width(self):
        return self._ptr.width

    @width.setter
    def width(self, w):
        self._ptr.width = w

    @property
    def height(self):
        return self._ptr.height

    @height.setter
    def height(self, h):
        self._ptr.height = h


class QuadProps:
    class Borders:
        def __init__(self, container):
            self._borders = container._ptr.borders
            self.left = self.right = self.top = self.bottom = 0

        @property
        def left(self):
            return self._borders.left

        @left.setter
        def left(self, value):
            self._borders.left = value

        @property
        def top(self):
            return self._borders.top

        @top.setter
        def top(self, value):
            self._borders.top = value

        @property
        def right(self):
            return self._borders.right

        @right.setter
        def right(self, value):
            self._borders.right = value

        @property
        def bottom(self):
            return self._borders.bottom

        @bottom.setter
        def bottom(self, value):
            self._borders.bottom = value

    def __init__(self):
        self._ptr = ffi.new('struct QuadProps*')
        self._color = Vec(ptr=ffi.addressof(self._ptr, 'color'))
        self._texture = None
        self.borders = QuadProps.Borders(self)
        self.color = Vec(1, 1, 1, 1)
        self.opacity = 1.0

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, c):
        ffi.memmove(self._color._ptr, c._ptr, ffi.sizeof('Vec'))

    @property
    def opacity(self):
        return self._ptr.opacity

    @opacity.setter
    def opacity(self, value):
        self._ptr.opacity = value

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, t):
        self._texture = t
        self._ptr.texture = t._ptr
