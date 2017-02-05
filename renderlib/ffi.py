"""CFFI wrapper entry point."""

from cffi import FFI
from matlib.ffi import ffi as matlib_ffi

ffi = FFI()

# matlib FFI dependency
ffi.include(matlib_ffi)

ffi.set_source(
    '_renderlib',
    """
    #include "renderlib.h"
    #include <GL/glew.h>
    """,
    libraries=['render'])

# OpenGL types
ffi.cdef(
    """
    typedef int... GLenum;
    typedef unsigned int... GLuint;
    enum {
        GL_TEXTURE_2D,
        GL_TEXTURE_RECTANGLE,
        ...
    };
    """)

# Core API
ffi.cdef(
    """
    struct Light {
        struct Mat transform;
        struct Vec direction;
        struct Vec color;
        float ambient_intensity;
        float diffuse_intensity;
    };

    struct Material {
        struct Texture *texture;
        struct Vec color;
        int receive_light;
        float specular_intensity;
        float specular_power;
    };

    struct MeshRenderProps {
        struct Vec eye;
        struct Mat model, view, projection;
        int cast_shadows;
        int receive_shadows;
        struct Light *light;
        struct AnimationInstance *animation;
        struct Material *material;
    };

    struct TextRenderProps {
        Mat model, view, projection;
        Vec color;
        float opacity;
    };

    struct QuadRenderProps {
        Mat model, view, projection;
        Vec color;
        struct Texture *texture;
        struct {
            float left, top;
            float right, bottom;
        } borders;
        float opacity;
    };

    int
    renderer_init(void);

    void
    renderer_clear(void);

    int
    renderer_present(void);

    void
    renderer_shutdown(void);

    int
    render_mesh(struct Mesh *mesh, struct MeshRenderProps *props);

    int
    render_text(struct Text *text, struct TextRenderProps *props);

    int
    render_quad(float w, float h, struct QuadRenderProps *props);
    """)

# Error API
ffi.cdef(
    """
    void
    error_print_traceback(void);
    """)

# Mesh API
ffi.cdef(
    """
    struct Mesh {
        Mat transform;
        size_t vertex_count;
        size_t index_count;
        struct Animation *animations;
        size_t anim_count;
        ...;
    };

    struct Mesh*
    mesh_from_file(const char *filename);

    struct Mesh*
    mesh_from_buffer(const void *data, size_t data_size);

    struct Mesh*
    mesh_new(
        float vertices[][3],
        float normals[][3],
        float uvs[][2],
        uint8_t joint_ids[][4],
        uint8_t joint_weights[][4],
        size_t vertex_count,
        uint32_t *indices,
        size_t index_count
    );

    void
    mesh_free(struct Mesh *mesh);
    """)

# Font API
ffi.cdef(
    """
    struct Font;

    struct Font*
    font_from_buffer(const void *data, size_t size, unsigned pt);

    struct Font*
    font_from_file(const char *filename, unsigned pt);

    void
    font_free(struct Font *font);
    """)

# Image API
ffi.cdef(
    """
    enum {
        IMAGE_FORMAT_RGBA,
        IMAGE_FORMAT_RGB,
        IMAGE_CODEC_PNG,
        IMAGE_CODEC_JPEG,
        ...
    };

    struct Image {
        unsigned width, height;
        int format;
        ...;
    };

    struct Image*
    image_from_buffer(const void *data, size_t size, int codec);

    struct Image*
    image_from_file(const char *filename);

    void
    image_free(struct Image *image);
    """)

# Texture API
ffi.cdef(
    """
    struct Texture {
        ...;
    };

    struct Texture*
    texture_from_image(struct Image *image, GLenum type);

    void
    texture_free(struct Texture *tex);
    """)

# Animation API
ffi.cdef(
    """
    struct Animation {
        ...;
    };

    struct AnimationInstance;

    struct AnimationInstance*
    animation_instance_new(struct Animation *anim);

    void
    animation_instance_free(struct AnimationInstance *inst);

    int
    animation_instance_play(struct AnimationInstance *inst, float dt);
    """)

# Text API
ffi.cdef(
    """
    struct Text {
        unsigned width;
        unsigned height;
        ...;
    };

    struct Text*
    text_new(struct Font *font);

    int
    text_set_string(struct Text *text, const char *str);

    void
    text_free(struct Text *text);
    """)
