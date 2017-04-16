"""Core API."""
from _renderlib import lib
from enum import IntEnum
from enum import unique


@unique
class RenderTarget(IntEnum):

    framebuffer = lib.RENDER_TARGET_FRAMEBUFFER
    overlay = lib.RENDER_TARGET_OVERLAY


def renderer_init():
    """Initializes renderlib library."""
    if not lib.renderer_init():
        raise RuntimeError('renderer initialization failed')


def renderer_clear():
    """Clear render buffers."""
    lib.renderer_clear()


def renderer_present():
    """Presents rendering results (a frame)."""
    if not lib.renderer_present():
        raise RuntimeError('rendering failed')


def renderer_shutdown():
    """Shuts down the library."""
    lib.renderer_shutdown()
