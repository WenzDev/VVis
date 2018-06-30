import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy
from seperateenvpitch import *
import sys
from multiprocessing import Process

p = pyaubio()
current_color = p.getcc()


def main():
    # initialize glfw
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "vvis", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    triangle = [-0.5, -0.5, 0.0,
                0.5, -0.5, 0.0,
                0.0, 0.5, 0.0]

    triangle = numpy.array(triangle, dtype=numpy.float32)

    vertex_shader = """
    #version 330
    uniform vec3 current_color;
    out vec3 out_color
    
    void main()
    {
        gl_Position = position;
        out_color = current_color;
    }
    """

    fragment_shader = """
    #version 330
    in out_color;
    out frag_color;
    
    void main()
    {
        frag_color = out_color;
    }
    """
    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, 36, triangle, GL_DYNAMIC_DRAW)

    position = glGetAttribLocation(shader, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(position)

    glUseProgram(shader)

    glClearColor(0.2, 0.3, 0.2, 1.0)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        glfw.swap_buffers(window)
        glClear(GL_COLOR_BUFFER_BIT)

        glDrawArrays(GL_TRIANGLES, 0, 3)

    glfw.terminate()


if __name__ == '__main__':
    p2c = pyaubio()
    p1 = Process(target=main)
    p1.start()
    p2 = Process(target=p2c.main(sys.argv))
    p2.start()
    p1.join()
    p2.join()
