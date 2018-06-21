import numpy as np
from PyQt5 import QtGui, QtCore
import pyqtgraph.opengl as gl
import sys
from opensimplex import OpenSimplex


class Terrain(object):
    def __init__(self):
        """
        Initialize the graphics window and mesh
        """

        # setup the view window
        self.app = QtGui.QApplication(sys.argv)
        self.w = gl.GLViewWidget()
        self.w.setGeometry(0, 110, 1920, 1080)
        self.w.show()
        self.w.setWindowTitle('Terrain')
        self.w.setCameraPosition(distance=30, elevation=8)

        grid = gl.GLGridItem()
        grid.scale(2, 2, 2)
        self.w.addItem(grid)

        self.nsteps = 1
        self.ypoints = range(-20, 22, self.nsteps)
        self.xpoints = range(-20, 22, self.nsteps)
        self.nfaces = len(self.ypoints)

        verts = np.array([
            [
                x, y, 0
            ] for n, x in enumerate(self.xpoints) for m, y in enumerate(self.ypoints)
        ], dtype=np.float32)

        faces = []
        colors = []
        for m in range(self.nfaces - 1):
            yoff = m * self.nfaces
            for n in range(self.nfaces - 1):
                faces.append([n + yoff + n + self.nfaces, yoff + n + self.nfaces + 1])
                faces.append([n + yoff, yoff + n + 1, yoff + n + self.nfaces + 1])
                colors.append([0, 0, 0, 0])

        faces = np.array(faces)
        colors = np.array(colors)
        self.m1 = gl.GLMeshItem(
            vertexes=verts,
            faces=faces,  # faceColors=colors,
            smooth=False, drawEdges=True
        )

        self.m1.setGLOptions('additive')
        self.w.addItem(self.m1)




    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()


if __name__ == '__main__':
    t = Terrain()
    t.start()
