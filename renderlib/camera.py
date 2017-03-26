"""Camera API."""
from _renderlib import ffi
from _renderlib import lib
from abc import ABC
from matlib.mat import Mat
from matlib.qtr import Qtr
from matlib.vec import Vec


class Camera(ABC):
    def __init__(self):
        self._ptr = ffi.new('struct Camera*')
        self._position = Vec(ptr=ffi.addressof(self._ptr, 'position'))
        self._orientation = Qtr(ptr=ffi.addressof(self._ptr, 'orientation'))
        self._view = Mat(ptr=ffi.addressof(self._ptr, 'view'))
        self._view.ident()
        self._projection = Mat(ptr=ffi.addressof(self._ptr, 'projection'))
        self._projection.ident()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, p):
        lib.camera_set_position(self._ptr, p._ptr)

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, o):
        lib.camera_set_orientation(self._ptr, o._ptr)

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

    def look_at(self, eye, target, up=None):
        """Sets up camera look transformation.

        :param eye: Eye position.
        :type eye: :class:`matlib.Vec`

        :param target: Target point to look at.
        :type target: :class:`matlib.Vec`

        :param up: Up vector.
        :type up: :class:`matlib.Vec`
        """
        if up is None:
            up = Vec(0, 1, 0)
        lib.camera_look_at(self._ptr, eye._ptr, target._ptr, up._ptr)

    def unproject(self, vx, vy, vz, vw, vh):
        """Unprojects a point in viewport coordinates into world coordinates.

        :param vx: Viewport X coordinate.
        :type vx: float

        :param vy: Viewport Y coordinate.
        :type vy: float

        :param vz: Viewport Z coordinate in range [0, 1].
        :type vz: float

        :param vw: Viewport width.
        :type vw: float

        :param vh: Viewport height.
        :type vh: float

        :returns: Unprojected point in world coordinates.
        :rtype: :class:`matlib.Vec`
        """
        x_ndc = 2.0 * vx / vw - 1.0
        y_ndc = 1.0 - (2.0 * vy) / vh
        z_ndc = 2 * vz - 1
        w_ndc = 1.0
        v_clip = Vec(x_ndc, y_ndc, z_ndc, w_ndc)

        m = (self.projection * self.view).inverse()

        out = m * v_clip
        out.w = 1.0 / out.w
        out.x *= out.w
        out.y *= out.w
        out.z *= out.w
        return out

    def trace_ray(self, vx, vy, vw, vh):
        """Traces a ray from viewport point "into the screen" and returns the
        ray origin and direction vector.

        :param vx: Viewport X coordinate.
        :type vx: float

        :param vy: Viewport Y coordinate.
        :type vy: float

        :param vw: Viewport width.
        :type vw: float

        :param vh: Viewport height.
        :type vh: float

        :returns: A tuple with the origin being first element and normalized
            direction vector the second.
        :rtype: (:class:`matlib.Vec`, :class:`matlib.Vec`)
        """
        p1 = self.unproject(vx, vy, 0, vw, vh)
        p2 = self.unproject(vx, vy, 1, vw, vh)
        ray = p2 - p1
        ray.norm()
        return p1, ray


class OrthographicCamera(Camera):
    def __init__(self, left, right, top, bottom, near, far):
        super().__init__()
        lib.camera_init_orthographic(self._ptr, left, right, top, bottom, near, far)


class PerspectiveCamera(Camera):
    def __init__(self, fovy, aspect, near, far):
        super().__init__()
        lib.camera_init_perspective(self._ptr, fovy, aspect, near, far)
