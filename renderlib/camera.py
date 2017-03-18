"""Camera API."""
from _renderlib import ffi
from _renderlib import lib
from matlib.mat import Mat
from matlib.vec import Vec


class Camera:
    def __init__(self):
        self._ptr = ffi.new('struct Camera*')
        self._position = Vec(ptr=ffi.addressof(self._ptr, 'position'))
        self._view = Mat(ptr=ffi.addressof(self._ptr, 'view'))
        self._projection = Mat(ptr=ffi.addressof(self._ptr, 'projection'))

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, p):
        ffi.memmove(self._position._ptr, p._ptr, ffi.sizeof('Vec'))

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, v):
        ffi.memmove(self._view._ptr, v._ptr, ffi.sizeof('Mat'))

    @property
    def projection(self):
        return self._projection

    @projection.setter
    def projection(self, p):
        ffi.memmove(self._projection._ptr, p._ptr, ffi.sizeof('Mat'))


class OrthographicCamera(Camera):
    def __init__(self, left, right, top, bottom, near, far):
        super().__init__()
        lib.camera_init_orthographic(self._ptr, left, right, top, bottom, near, far)


class PerspectiveCamera(Camera):
    def __init__(self, fovy, aspect, near, far):
        super().__init__()
        lib.camera_init_perspective(self._ptr, fovy, aspect, near, far)
