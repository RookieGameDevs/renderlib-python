from matlib.vec import Vec
from renderlib.animation import AnimationInstance
from renderlib.camera import OrthographicCamera
from renderlib.camera import PerspectiveCamera
from renderlib.core import renderer_present
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


def test_render_mesh(context):
    # load the mesh and create an animation instance
    mesh = Mesh.from_file('tests/data/zombie.mesh')
    anim = AnimationInstance(mesh.animations[0])

    # create a textured material
    img = Image.from_file('tests/data/zombie.jpg')
    texture = Texture.from_image(img, Texture.TextureType.texture_2d)
    material = Material()
    material.texture = texture
    material.color = Vec(0.3, 0.8, 0.4)  # unnecessary with textures, just test
    material.receive_light = True
    material.specular_intensity = 0.8
    material.specular_power = 4

    # create a light
    light = Light()
    light.direction = Vec(0, -5, -5)
    light.direction.norm()
    light.color = Vec(0.8, 0.8, 0.8, 1.0)
    light.ambient_intensity = 0.3
    light.diffuse_intensity = 0.8

    # configure mesh rendering properties
    props = MeshProps()
    props.cast_shadows = True
    props.receive_shadows = True
    props.animation = anim
    props.material = material

    # create a scene and add the mesh to it
    scene = Scene()
    scene.add_mesh(mesh, props)

    # create a camera
    camera = PerspectiveCamera(60.0, 4 / 3, 1, 100)

    # do actual rendering
    scene.render(camera, light)
    renderer_present()


def test_render_text(context):
    # load a font and create a text from it
    font = Font.from_file('tests/data/courier.ttf', 21)
    text = Text(font, 'hello world')

    # create and initialize instance of text render properties container
    props = TextProps()
    props.color = Vec(0.8, 0.8, 1.0, 1.0)
    props.opacity = 0.8

    # create a scene and add the text to it
    scene = Scene()
    scene.add_text(text, props)

    # create an orthographic camera
    camera = OrthographicCamera(-400, 400, 300, -300, 0, 1)

    # do actual rendering
    scene.render(camera, None)
    renderer_present()


def test_render_colored_quad(context):
    # create a simple rectangle
    quad = Quad(120, 70)

    # initialize simple quad props container
    props = QuadProps()
    props.color = Vec(0.3, 0.9, 0.3, 1.0)
    props.opacity = 0.8

    # create a scene and add the quad to it
    scene = Scene()
    scene.add_quad(quad, props)

    # create an orthographic camera
    camera = OrthographicCamera(-400, 400, 300, -300, 0, 1)

    # do actual rendering
    scene.render(camera, None)
    renderer_present()


def test_render_textured_quad(context):
    # load an image and make a *rectangular* texture from it
    img = Image.from_file('tests/data/star.png')
    texture = Texture.from_image(img, Texture.TextureType.texture_rectangle)

    # create a simple rectangle
    quad = Quad(120, 70)

    # initialize quad props container
    props = QuadProps()
    props.texture = texture
    props.opacity = 0.8

    # create a scene and add the quad to it
    scene = Scene()
    scene.add_quad(quad, props)

    # create an orthographic camera
    camera = OrthographicCamera(-400, 400, 300, -300, 0, 1)

    # do actual rendering
    scene.render(camera, None)
    renderer_present()