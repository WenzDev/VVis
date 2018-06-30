from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from seperateenvpitch import *
import sys
from multiprocessing import Process
p = pyaubio()
current_color = p.getcc()

window = 0
width, height = (500, 400)


def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    refresh2d(width, height)
    glColor3f(current_color[0] / 255.0, current_color[1] / 255.0, current_color[2] / 255.0)
    draw_rect(10, 10, 200, 100)

    glutSwapBuffers()


def draw_rect(x, y, width, height):
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()


def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("vvis")
    draw()
    glutDisplayFunc(draw)
    glutIdleFunc(draw)
    glutMainLoop()


if __name__ == "__main__":
    p2c = pyaubio()
    p1 = Process(target=main)
    p1.start()
    p2 = Process(target=p2c.main(sys.argv))
    p2.start()
    p1.join()
    p2.join()



