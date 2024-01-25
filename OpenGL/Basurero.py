import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math
import numpy as np



class Basurero:

    def __init__(self, dim, scale):
        # vertices del cubo
        self.points = np.array([[-1.0, -1.0, 1.0], [1.0, -1.0, 1.0], [1.0, -1.0, -1.0], [-1.0, -1.0, -1.0],
                                [-1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0, -1.0], [-1.0, 1.0, -1.0]])
        self.scale = scale
        self.radio = math.sqrt(self.scale*self.scale + self.scale*self.scale)
        self.DimBoard = dim
        # Se inicializa una posicion aleatoria en el tablero
        self.Position = []
        self.Position.append(0.0)
        self.Position.append(5.0)
        self.Position.append(0.0)


    def update(self):
        d = 1
        # # detecc de que el objeto no se salga del area de navegacion
        # if (abs(new_x) <= self.DimBoard):
        #     self.Position[0] = new_x
        # else:
        #     self.Direction[0] *= -1.0
        #     self.Position[0] += self.Direction[0]
        #
        # if (abs(new_z) <= self.DimBoard):
        #     self.Position[2] = new_z
        # else:
        #     self.Direction[2] *= -1.0
        #     self.Position[2] += self.Direction[2]

    def drawFaces(self):
        glBegin(GL_QUADS)
        glVertex3fv(self.points[0])
        glVertex3fv(self.points[1])
        glVertex3fv(self.points[2])
        glVertex3fv(self.points[3])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[4])
        glVertex3fv(self.points[5])
        glVertex3fv(self.points[6])
        glVertex3fv(self.points[7])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[0])
        glVertex3fv(self.points[1])
        glVertex3fv(self.points[5])
        glVertex3fv(self.points[4])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[1])
        glVertex3fv(self.points[2])
        glVertex3fv(self.points[6])
        glVertex3fv(self.points[5])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[2])
        glVertex3fv(self.points[3])
        glVertex3fv(self.points[7])
        glVertex3fv(self.points[6])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3fv(self.points[3])
        glVertex3fv(self.points[0])
        glVertex3fv(self.points[4])
        glVertex3fv(self.points[7])
        glEnd()

    def draw(self):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(self.scale, self.scale, self.scale)
        glColor3f(0.0, 0.0, 1.0)
        self.drawFaces()
        glPopMatrix()