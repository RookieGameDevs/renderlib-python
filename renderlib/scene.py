"""Scene API."""
from _renderlib import ffi
from _renderlib import lib
from matlib.qtr import Qtr
from matlib.vec import Vec


class Object:
    def __init__(self, scene, ptr, refs):
        self._scene = scene
        self._ptr = ptr
        self._refs = refs
        self._position = Vec(ptr=ffi.addressof(self._ptr, 'position'))
        self._rotation = Qtr(ptr=ffi.addressof(self._ptr, 'rotation'))
        self._scale = Vec(ptr=ffi.addressof(self._ptr, 'scale'))

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, p):
        ffi.memmove(self._position._ptr, p._ptr, ffi.sizeof('Vec'))

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, r):
        ffi.memmove(self._rotation._ptr, r._ptr, ffi.sizeof('Qtr'))

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, s):
        ffi.memmove(self._scale._ptr, s._ptr, ffi.sizeof('Vec'))

    def remove(self):
        self._scene.remove_object(self)


class Scene:
    def __init__(self):
        self._ptr = ffi.gc(lib.scene_new(), lib.scene_free)

    @property
    def object_count(self):
        return lib.scene_object_count(self._ptr)

    def add_mesh(self, mesh, props):
        return Object(
            self,
            lib.scene_add_mesh(self._ptr, mesh._ptr, props._ptr),
            (mesh, props))

    def add_text(self, text, props):
        return Object(
            self,
            lib.scene_add_text(self._ptr, text._ptr, props._ptr),
            (text, props))

    def add_quad(self, quad, props):
        return Object(
            self,
            lib.scene_add_quad(self._ptr, quad._ptr, props._ptr),
            (quad, props))

    def remove_object(self, obj):
        lib.scene_remove_object(self._ptr, obj._ptr)

    def render(self, render_target, camera, light=None):
        lib.scene_render(
            self._ptr,
            render_target.value,
            camera._ptr,
            light._ptr if light else ffi.NULL)
