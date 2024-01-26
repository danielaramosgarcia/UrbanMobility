import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math
import numpy as np



class Basura:

    def __init__(self, dim, vel, scale, cubo, basurero):
        # vertices del cubo
        self.points = np.array([[-1.0, -1.0, 1.0], [1.0, -1.0, 1.0], [1.0, -1.0, -1.0], [-1.0, -1.0, -1.0],
                                [-1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0, -1.0], [-1.0, 1.0, -1.0]])
        self.cubo = cubo
        self.basurero = basurero
        self.collision = 0
        self.scale = scale
        self.firstCollision = False
        self.radio = math.sqrt(self.scale*self.scale + self.scale*self.scale)
        self.DimBoard = dim
        # Se inicializa una posicion aleatoria en el tablero
        self.Position = []
        self.Position.append(random.randint(-1 * self.DimBoard, self.DimBoard))
        self.Position.append(5.0)
        self.Position.append(random.randint(-1 * self.DimBoard, self.DimBoard))
        # Se inicializa un vector de direccion aleatorio
        self.Direction = []
        self.Direction.append(random.random())
        self.Direction.append(5.0)
        self.Direction.append(random.random())
        # Se normaliza el vector de direccion
        m = math.sqrt(self.Direction[0] * self.Direction[0] + self.Direction[2] * self.Direction[2])
        self.Direction[0] /= m
        self.Direction[2] /= m
        # Se cambia la maginitud del vector direccion
        self.Direction[0] *= vel
        self.Direction[2] *= vel

    def update(self):
        hola = 0
        # self.collisionDetection()
        # if not self.firstCollision:
        #     return
        # if self.collision:
        #     self.Position[0] = 0.0
        #     self.Position[2] = 0.0
        # else:
        #     d = 1
        #     # detecc de que el objeto no se salga del area de navegacion
        #     new_x = self.Position[0] + self.Direction[0]
        #     new_z = self.Position[2] + self.Direction[2]
        #     if (abs(new_x) <= self.DimBoard):
        #         self.Position[0] = new_x
        #     else:
        #         self.Direction[0] *= -1.0
        #         self.Position[0] += self.Direction[0]

        #     if (abs(new_z) <= self.DimBoard):
        #         self.Position[2] = new_z
        #     else:
        #         self.Direction[2] *= -1.0
        #         self.Position[2] += self.Direction[2]

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
        glColor3f(0.644, 0.164, 0.164)
        self.drawFaces()
        glPopMatrix()
        
    # def collisionDetection(self):
    #     # Revisar por colision contra cubo
    #     for obj in self.cubo:
    #         self.hasCollided = True
    #         self.Position[1] = 10.0
    #         d_x = self.Position[0] - obj.Position[0]
    #         d_z = self.Position[2] - obj.Position[2]
    #         d = math.sqrt(d_x * d_x + d_z * d_z)
    #         if d - (self.radio + obj.radio) < 0.0:
    #             # Cambia la dirección hacia el centro del mapa (asumiendo que el centro del mapa es (0,0))
    #             self.firstCollision = True 
    #             newdir_x = -self.Position[0]
    #             newdir_z = -self.Position[2]
    #             m = math.sqrt(newdir_x ** 2 + newdir_z ** 2)
    #             self.Direction = [(newdir_x / m), 0, (newdir_z / m)]
    #     for obj in self.basurero:
    #         d_x = self.Position[0] - obj.Position[0]
    #         d_z = self.Position[2] - obj.Position[2]
    #         d = math.sqrt(d_x * d_x + d_z * d_z)
    #         if d - (self.radio + obj.radio) < 0.0:
    #             self.Position = [0.0, 15.0, 0.0]
                