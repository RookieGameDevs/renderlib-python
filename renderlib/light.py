"""Light API."""
from _renderlib import ffi
from matlib.vec import Vec


class Light:
    def __init__(self):
        self._ptr = ffi.new('struct Light*')
        self._direction = Vec(ptr=ffi.addressof(self._ptr, 'direction'))
        self._color = Vec(ptr=ffi.addressof(self._ptr, 'color'))

        # initialize defaults
        self.direction = Vec(0, -1, 0)
        self.color = Vec(1, 1, 1)
        self.ambient_intensity = 0.3
        self.diffuse_intensity = 0.8

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, d):
        ffi.memmove(self._direction._ptr, d._ptr, ffi.sizeof('Vec'))

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, c):
        ffi.memmove(self._color._ptr, c._ptr, ffi.sizeof('Vec'))

    @property
    def ambient_intensity(self):
        return self._ptr.ambient_intensity

    @ambient_intensity.setter
    def ambient_intensity(self, ai):
        self._ptr.ambient_intensity = ai

    @property
    def diffuse_intensity(self):
        return self._ptr.diffuse_intensity

    @diffuse_intensity.setter
    def diffuse_intensity(self, di):
        self._ptr.diffuse_intensity = di
