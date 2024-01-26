import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math
import numpy as np


class Cubo:

    def __init__(self, dim, vel, scale, basura, basurero):
        self.points = np.array([[-1.0, -0.5, 1.5], [1.0, -0.5, 1.5], [1.0, -0.5, -1.5], [-1.0, -0.5, -1.5],
            [-1.0, 0.5, 1.5], [1.0, 0.5, 1.5], [1.0, 0.5, -1.5], [-1.0, 0.5, -1.5]])

        self.basuraCargada = 0
        self.basuraHeight = 0.3
        self.brazoHeight = 0.5
        self.currentHeight = 0
        self.minHeight = -0.5
        self.maxHeight = 2.0
        self.collision = 0
        self.scale = scale
        self.radio = math.sqrt(self.scale * self.scale + self.scale * self.scale)
        self.basura = basura
        self.basurero = basurero
        self.DimBoard = dim
        self.rotationAngle = 0.0
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
        self.rotationAngle = (math.acos(self.Direction[0]) * 180 / math.pi) + 90
        

    def update(self):
        self.collisionDetection()
        if self.collision == 0:
            new_x = self.Position[0] + self.Direction[0]
            new_z = self.Position[2] + self.Direction[2]

            # detecc de que el objeto no se salga del area de navegacion
            if (abs(new_x) <= self.DimBoard):
                self.Position[0] = new_x
            else:
                self.Direction[0] *= -1.0
                self.Position[0] += self.Direction[0]
            self.rotationAngle = (math.acos(self.Direction[0]) * 180 / math.pi) + 90
            if (abs(new_z) <= self.DimBoard):
                self.Position[2] = new_z
            else:
                self.Direction[2] *= -1.0
                self.Position[2] += self.Direction[2]
                self.rotationAngle = (math.acos(self.Direction[0]) * 180 / math.pi) + 90
        elif self.collision == 1:
            #Animación de subir brazos con la basura
            if self.currentHeight >= self.maxHeight:
                self.collision = 2
        elif self.collision == 2:
            #Animación de vuelta
            self.collision = 3
            #Una vez terminada la vuelta darle el mismo vector de direccion del carro a la basura
            self.basura[self.basuraCargada].Direction = [self.Direction[0], self.Direction[1], self.Direction[2]]
        elif self.collision == 3:
            #Movimiento hacia el basurero
            new_x = self.Position[0] + self.Direction[0]
            new_z = self.Position[2] + self.Direction[2]

            if (abs(new_x) <= self.DimBoard):
                self.Position[0] = new_x
            else:
                self.Direction[0] *= -1.0
                self.Position[0] += self.Direction[0]
                self.rotationAngle = (math.acos(self.Direction[0]) * 180 / math.pi) + 90

            if (abs(new_z) <= self.DimBoard):
                self.Position[2] = new_z
            else:
                self.Direction[2] *= -1.0
                self.Position[2] += self.Direction[2]
                self.rotationAngle = (math.acos(self.Direction[0]) * 180 / math.pi) + 90
        elif self.collision == 4:
            #Animación de bajar brazos, dejar basura en el basurero y vuelta
            if self.currentHeight <= self.minHeight:
                self.collision = 0
                self.basura[self.basuraCargada].Direction = [0.0,0.0,0.0]
            print("Collision detected")


    def drawPrisma(self):
        # Dimensiones del prisma rectangular
        prisma_width = 1.5
        prisma_height = 3.0
        prisma_depth = 1.0

        # Puntos del prisma (en la cara frontal del cubo)
        prisma_points = np.array([
            [-prisma_width / 2, -prisma_height / 2, 1.0],
            [prisma_width / 2, -prisma_height / 2, 1.0],
            [prisma_width / 2, prisma_height / 2, 1.0],
            [-prisma_width / 2, prisma_height / 2, 1.0],
            [-prisma_width / 2, -prisma_height / 2, 2.0],
            [prisma_width / 2, -prisma_height / 2, 2.0],
            [prisma_width / 2, prisma_height / 2, 2.0],
            [-prisma_width / 2, prisma_height / 2, 2.0],
        ])

        # glColor3f(0.0, 1.0, 0.0)  # Color del prisma (verde en este caso)
        glColor3f(0.0, 0.0, 0.0)

        glBegin(GL_QUADS)
        for face in [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]:
            for vertex in face:
                glVertex3fv(prisma_points[vertex])
        glEnd()
        
    
    
    
    def drawBrazos(self):
        # Dimensiones de los brazos rectangulares
        brazo_width = 0.2
        brazo_height = 0.5
        brazo_depth = 2.0

        if self.collision == 1 and self.currentHeight < self.maxHeight:
            self.brazoHeight += 0.05
            self.currentHeight = -1 + self.brazoHeight
            self.basura[self.basuraCargada].Position[1] += self.basuraHeight
        elif self.collision == 4 and self.currentHeight > self.minHeight:
            self.brazoHeight -= 0.05
            self.currentHeight = -1 + self.brazoHeight
            self.basura[self.basuraCargada].Position[1] -= self.basuraHeight
        # Puntos de los brazos (frente del prisma verde)
        brazo_points1 = np.array([
            [0.0, -1.5 + self.brazoHeight, 1.5],  # Punto inferior izquierdo
            [brazo_width, -1.5 + self.brazoHeight, 1.5],  # Punto inferior derecho
            [brazo_width, -1.0 + self.brazoHeight, 1.5],  # Punto superior derecho
            [0.0, -1.0 + self.brazoHeight, 1.5],  # Punto superior izquierdo
            [0.0, -1.5 + self.brazoHeight, 1.5 + brazo_depth],  # Punto inferior izquierdo trasero
            [brazo_width, -1.5 + self.brazoHeight, 1.5 + brazo_depth],  # Punto inferior derecho trasero
            [brazo_width, -1.0 + self.brazoHeight, 1.5 + brazo_depth],  # Punto superior derecho trasero
            [0.0, -1.0 + self.brazoHeight, 1.5 + brazo_depth],  # Punto superior izquierdo trasero
        ])

        brazo_points2 = np.array([
            [1.0 - brazo_width,-1.5 + self.brazoHeight, 1.5],  # Punto inferior izquierdo
            [1.0, -1.5 + self.brazoHeight, 1.5],  # Punto inferior derecho
            [1.0, -1.0 + self.brazoHeight, 1.5],  # Punto superior derecho
            [1.0 - brazo_width, -1.0 + self.brazoHeight, 1.5],  # Punto superior izquierdo
            [1.0 - brazo_width, -1.5 + self.brazoHeight, 1.5 + brazo_depth],  # Punto inferior izquierdo trasero
            [1.0, -1.5 + self.brazoHeight, 1.5 + brazo_depth],  # Punto inferior derecho trasero
            [1.0, -1.0 + self.brazoHeight, 1.5 + brazo_depth],  # Punto superior derecho trasero
            [1.0 - brazo_width, -1.0 + self.brazoHeight, 1.5 + brazo_depth],  # Punto superior izquierdo trasero
        ])

        glColor3f(1.0, 0.0, 0.0)  # Color de los brazos (rojo en este caso)

        glBegin(GL_QUADS)
        for face in [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]:
            for vertex in face:
                glVertex3fv(brazo_points1[vertex])
        glEnd()

        glBegin(GL_QUADS)
        for face in [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]:
            for vertex in face:
                glVertex3fv(brazo_points2[vertex])
        glEnd()
    
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

    def drawTecho(self):
        # Dimensiones del prisma rectangular para el techo
        techo_width = 1.6
        techo_height = 0.2
        techo_depth = -1.6

        # Puntos del prisma (en la cara frontal del cubo)
        techo_points = np.array([
            [-techo_width / 2, 0.5 + 1.5, 1.5],            # Punto A
            [techo_width / 2, 0.5 + 1.5, 1.5],             # Punto B
            [techo_width / 2, 0.5 + techo_height + 1.5, 1.5],  # Punto C
            [-techo_width / 2, 0.5 + techo_height + 1.5, 1.5], # Punto D
            [-techo_width / 2, 0.5 + 1.5, 1.5 + techo_depth],  # Punto E
            [techo_width / 2, 0.5 + 1.5, 1.5 + techo_depth],   # Punto F
            [techo_width / 2, 0.5 + techo_height + 1.5, 1.5 + techo_depth],  # Punto G
            [-techo_width / 2, 0.5 + techo_height + 1.5, 1.5 + techo_depth], # Punto H
        ])

        glBegin(GL_QUADS)
        glColor3f(0.0, 0.0, 0.0)  # Cambiar a color negro
        # Caras frontales
        for face in [(0, 1, 2, 3)]:
            for vertex in face:
                glVertex3fv(techo_points[vertex])
        # Caras laterales
        for face in [(0, 3, 7, 4), (1, 2, 6, 5), (0, 1, 5, 4), (2, 3, 7, 6)]:
            for vertex in face:
                glVertex3fv(techo_points[vertex])
        glEnd()
        
        
        # Extensión hacia atrás
        glBegin(GL_QUADS)
        # Caras laterales hacia atrás
        for face in [(4, 5, 6, 7)]:
            for vertex in face:
                glVertex3fv(techo_points[vertex])
        glEnd()
        
    def drawPrismaCabina(self):
        # Dimensiones originales del prisma rectangular gris
        # prisma_gris_width = 1.5
        # prisma_gris_height = 4.0
        # prisma_gris_depth = 1.0

        prisma_gris_width = 1.9
        prisma_gris_height = 4.0
        prisma_gris_depth = 1.3

        # Puntos del prisma (en la cara frontal del cubo)
        prisma_gris_points = np.array([
            [-prisma_gris_width / 2, -prisma_gris_height / 2, 0.0],
            [prisma_gris_width / 2, -prisma_gris_height / 2, 0.0],
            [prisma_gris_width / 2, prisma_gris_height / 2, 0.0],
            [-prisma_gris_width / 2, prisma_gris_height / 2, 0.0],
            [-prisma_gris_width / 2, -prisma_gris_height / 2, prisma_gris_depth],
            [prisma_gris_width / 2, -prisma_gris_height / 2, prisma_gris_depth],
            [prisma_gris_width / 2, prisma_gris_height / 2, prisma_gris_depth],
            [-prisma_gris_width / 2, prisma_gris_height / 2, prisma_gris_depth],
        ])

        glBegin(GL_QUADS)
        glColor3f(0.5, 0.5, 0.5)  # Color del prisma gris
        for face in [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]:
            for vertex in face:
                glVertex3fv(prisma_gris_points[vertex])
        glEnd()


    def draw(self):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(self.scale, self.scale, self.scale)
        glColor3f(0.0, 0.9, 0.0)
        glRotatef(self.rotationAngle, 0.0, 1.0, 0.0)
        self.drawFaces()
        self.drawPrisma()
        self.drawBrazos()
        
        # Agregar prisma gris
        self.drawPrismaCabina()
        
        # Agregar prisma negro como techo
        glColor3f(0.0, 0.0, 0.0)  # Color del techo negro
        self.drawTecho()
        glPopMatrix()

    def collisionDetection(self):
    #Revisar por colision contra basura mientras no se este cargando nada
        if self.collision == 0:
            i = 0
            for obj in self.basura:
                d_x = self.Position[0] - obj.Position[0]
                d_z = self.Position[2] - obj.Position[2]
                d_c = math.sqrt(d_x * d_x + d_z * d_z)
                if d_c - (self.radio + obj.radio) < 0.0 and obj.collision != 1:
                    self.collision = 1
                    obj.collision = 1
                    self.basuraCargada = i
                    obj.Position[0] = self.Position[0] + 8.0
                    obj.Position[2] = self.Position[2] + 18.0
                    # Cambia la dirección hacia el centro del mapa (asumiendo que el centro del mapa es (0,0))
                    newdir_x = -self.Position[0]
                    newdir_z = -self.Position[2]
                    m = math.sqrt(newdir_x ** 2 + newdir_z  ** 2)
                    new_direction = [(newdir_x / m), 0, (newdir_z / m)]
                    self.Direction = new_direction
                    self.rotationAngle = (math.acos(self.Direction[0]) * 180 / math.pi) + 90
                i += 1
        for obj in self.basurero:
            d_x = self.Position[0] - obj.Position[0]
            d_z = self.Position[2] - obj.Position[2]
            d_c = math.sqrt(d_x * d_x + d_z * d_z)
            if d_c - (self.radio + obj.radio) < 0.0:
                #Revisar si esta llevando basura
                if self.collision == 3:
                    self.collision = 4
                self.Direction[0] *= -1.0
                self.Direction[2] *= -1.0
                self.rotationAngle = (math.acos(self.Direction[0]) * 180 / math.pi) + 90


# la direccion actual, la comparamos con la nueva, y hacemos 
# lo de pitagoras para sacar el angulo en el que rota

