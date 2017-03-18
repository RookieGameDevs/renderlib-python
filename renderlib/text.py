"""Text wrappers."""
from _renderlib import ffi
from _renderlib import lib
from matlib.vec import Vec


class Text:
    def __init__(self, font, string=''):
        self._ptr = lib.text_new(font._ptr)
        if not self._ptr:
            raise RuntimeError('failed to create text')
        self._string = None
        self.string = string

    def __del__(self):
        lib.text_free(self._ptr)

    @property
    def string(self):
        return self._string

    @string.setter
    def string(self, s):
        if self._string != s:
            self._string = s
            if not lib.text_set_string(self._ptr, s.encode('utf8')):
                raise RuntimeError('failed to set text string')

    @property
    def width(self):
        return self._ptr.width

    @property
    def height(self):
        return self._ptr.height


class TextProps:
    def __init__(self):
        self._ptr = ffi.new('struct TextProps*')
        self._color = Vec(ptr=ffi.addressof(self._ptr, 'color'))
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
