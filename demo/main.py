from matlib.vec import Vec
from renderlib.animation import AnimationInstance
from renderlib.camera import OrthographicCamera
from renderlib.camera import PerspectiveCamera
from renderlib.core import renderer_init
from renderlib.core import renderer_present
from renderlib.core import renderer_shutdown
from renderlib.error import error_print_traceback
from renderlib.font import Font
from renderlib.image import Image
from renderlib.light import Light
from renderlib.material import Material
from renderlib.mesh import Mesh
from renderlib.mesh import MeshProps
from renderlib.quad import Quad
from renderlib.quad import QuadProps
from renderlib.scene import Scene
from renderlib.text import Text
from renderlib.text import TextProps
from renderlib.texture import Texture
from time import time
import sdl2 as sdl

#: Stats update interval in seconds
UPDATE_INTERVAL = 2.0


class Demo:
    def __init__(self, width, height):
        self.win = self.ctx = None

        # create a SDL window
        self.win = sdl.SDL_CreateWindow(
            b'Demo',
            sdl.SDL_WINDOWPOS_CENTERED,
            sdl.SDL_WINDOWPOS_CENTERED,
            width,
            height,
            sdl.SDL_WINDOW_OPENGL)
        if self.win is None:
            raise RuntimeError('failed to create SDL window')

        # create an OpenGL context
        sdl.SDL_GL_SetAttribute(
            sdl.SDL_GL_CONTEXT_PROFILE_MASK,
            sdl.SDL_GL_CONTEXT_PROFILE_CORE)
        sdl.SDL_GL_SetAttribute(sdl.SDL_GL_CONTEXT_MAJOR_VERSION, 3)
        sdl.SDL_GL_SetAttribute(sdl.SDL_GL_CONTEXT_MINOR_VERSION, 3)
        sdl.SDL_GL_SetAttribute(sdl.SDL_GL_DOUBLEBUFFER, 1)
        sdl.SDL_GL_SetAttribute(sdl.SDL_GL_DEPTH_SIZE, 24)
        self.ctx = sdl.SDL_GL_CreateContext(self.win)

        sdl.SDL_GL_SetSwapInterval(0)

        if self.ctx is None:
            raise RuntimeError('failed to initialize OpenGL context')

        # initialize renderer
        renderer_init()

        self.width = width
        self.height = height
        self.aspect = width / float(height)

        # initialize controls
        self.play_animation = False

        # initialize UI camera and scene
        self.ui_camera = OrthographicCamera(
            -self.width / 2,
            +self.width / 2,
            +self.height / 2,
            -self.height / 2,
            0,
            1)
        self.ui_scene = Scene()

        # initialize main camera and scene
        self.camera = PerspectiveCamera(
            30.0,
            self.aspect,
            1,
            50)
        self.camera.view.lookatv(
            Vec(5, 5, 5),
            Vec(0, 0, 0),
            Vec(0, 1, 0))
        self.scene = Scene()

        # initialize light
        self.light = Light()
        self.light.direction = Vec(0, -5, -5)
        self.light.direction.norm()
        self.light.color = Vec(1, 1, 1)
        self.light.ambient_intensity = 0.3
        self.light.diffuse_intensity = 1.0

        self.load_resources()
        self.setup_scene()

    def __del__(self):
        renderer_shutdown()
        sdl.SDL_GL_DeleteContext(self.ctx)
        sdl.SDL_DestroyWindow(self.win)
        sdl.SDL_Quit()

    def load_resources(self):
        self.mesh = Mesh.from_file('tests/data/zombie.mesh')
        self.animation = AnimationInstance(self.mesh.animations[0])
        self.image = Image.from_file('tests/data/zombie.jpg')
        self.texture = Texture.from_image(self.image, Texture.TextureType.texture_2d)

        self.terrain_mesh = Mesh.from_file('tests/data/plane.mesh')
        self.grass_img = Image.from_file('tests/data/grass.jpg')
        self.terrain_texture = Texture.from_image(self.grass_img, Texture.TextureType.texture_2d)

        self.font = Font.from_file('tests/data/courier.ttf', 16)
        self.text = Text(self.font)

        self.btn = Quad(38, 36)
        self.btn_img = Image.from_file('tests/data/close_btn.png')
        self.btn_texture = Texture.from_image(self.btn_img, Texture.TextureType.texture_rectangle)

        self.material = Material()
        self.material.texture = self.texture
        self.material.receive_light = True
        self.material.specular_intensity = 0.3
        self.material.specular_power = 4

        self.terrain_material = Material()
        self.terrain_material.texture = self.terrain_texture
        self.terrain_material.receive_light = True

    def setup_scene(self):
        self.mesh_props = MeshProps()
        self.mesh_props.cast_shadows = True
        self.mesh_props.receive_shadows = True
        self.mesh_props.animation = self.animation
        self.mesh_props.material = self.material
        self.scene.add_mesh(self.mesh, self.mesh_props)

        self.terrain_props = MeshProps()
        self.terrain_props.cast_shadows = False
        self.terrain_props.receive_shadows = True
        self.terrain_props.material = self.terrain_material
        terrain_obj = self.scene.add_mesh(self.terrain_mesh, self.terrain_props)
        terrain_obj.scale = Vec(2, 1, 2)

        self.text_props = TextProps()
        self.text_props.color = Vec(0.5, 1.0, 0.5, 1.0)
        self.text_props.opacity = 1.0
        text_obj = self.ui_scene.add_text(self.text, self.text_props)
        text_obj.position.x = -self.width / 2 + 10
        text_obj.position.y = self.height / 2 - 10

        self.btn_props = QuadProps()
        self.btn_props.texture = self.btn_texture
        btn_obj = self.ui_scene.add_quad(self.btn, self.btn_props)
        btn_obj.position.x = self.width / 2 - 40
        btn_obj.position.y = self.height / 2 - 2

    def update(self, dt):
        evt = sdl.SDL_Event()
        while sdl.SDL_PollEvent(evt):
            if evt.type == sdl.SDL_QUIT:
                return False
            elif evt.type == sdl.SDL_KEYUP:
                if evt.key.keysym.sym == sdl.SDLK_ESCAPE:
                    return False
                elif evt.key.keysym.sym == sdl.SDLK_SPACE:
                    self.play_animation = not self.play_animation
            elif evt.type == sdl.SDL_MOUSEBUTTONDOWN and \
                    evt.button.x >= self.width - 40 and \
                    evt.button.x <= self.width and \
                    evt.button.y >= 2 and \
                    evt.button.y <= 40:
                return False

        if self.play_animation:
            self.animation.play(dt)

        return True

    def update_stats(self, fps, render_time):
        self.text.string = 'FPS: {fps}, render time: {time:.2f}ms'.format(
            fps=int(fps),
            time=render_time * 1000)

    def render(self):
        self.scene.render(self.camera, self.light)
        self.ui_scene.render(self.ui_camera, None)
        renderer_present()
        sdl.SDL_GL_SwapWindow(self.win)

    def run(self):
        fps = render_time = time_acc = 0
        last_update = time()

        while True:
            # compute time delta
            now = time()
            dt = now - last_update
            last_update = now

            # update stats
            time_acc += dt
            if time_acc >= UPDATE_INTERVAL:
                time_acc -= UPDATE_INTERVAL
                self.update_stats(fps / UPDATE_INTERVAL, render_time)
                fps = 0
            else:
                fps += 1

            # update the scene
            if not self.update(dt):
                break

            # render and measure rendering time
            now = time()
            self.render()
            render_time = time() - now


if __name__ == '__main__':
    try:
        demo = Demo(800, 600)
        demo.run()
    except RuntimeError as err:
        print(err)
        error_print_traceback()
