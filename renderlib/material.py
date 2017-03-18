"""Material wrappers."""
from _renderlib import ffi
from matlib.vec import Vec


class Material:
    def __init__(self):
        self._ptr = ffi.new('struct Material*')
        self._texture = None
        self._color = Vec(ptr=ffi.addressof(self._ptr, 'color'))

        # defaults
        self.receive_light = False
        self.specular_intensity = 0.8
        self.specular_power = 4

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, t):
        self._texture = t
        self._ptr.texture = t._ptr

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, c):
        ffi.memmove(self._color._ptr, c._ptr, ffi.sizeof('Vec'))

    @property
    def receive_light(self):
        return bool(self._ptr.receive_light)

    @receive_light.setter
    def receive_light(self, flag):
        self._ptr.receive_light = int(bool(flag))

    @property
    def specular_intensity(self):
        return self._ptr.specular_intensity

    @specular_intensity.setter
    def specular_intensity(self, si):
        self._ptr.specular_intensity = si

    @property
    def specular_power(self):
        return self._ptr.specular_power

    @specular_power.setter
    def specular_power(self, sp):
        self._ptr.specular_power = sp
