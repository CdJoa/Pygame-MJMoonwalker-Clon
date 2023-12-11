import pygame as py
from Configuraciones import*



# Obtiene el ancho y el alto de la pantalla
H = PANTALLA.get_height()
class Plataforma:
    def __init__(self, tamaño, x, y,direccion,direccionY,danio, path=""):
        self.contador_pasos = 0
        self.muriendo = False
        self.direccion = direccion
        self.direccionY = direccionY
        self.danio = danio
        self.banderaDaño = False
        self.banderaPortal = False

                # Dentro de __init__
        self.superficie = py.image.load(path)
        self.superficie = py.transform.scale(self.superficie, tamaño)

        self.rectangulo = self.superficie.get_rect()
        self.rectangulo.x = x
        self.rectangulo.y = y




    def mover(self):
        self.velocidad = self.direccion * 7
        self.velocidadY = self.direccionY * 7

        self.rectangulo.x += self.velocidad
        self.rectangulo.y += self.velocidadY


        if self.direccion!=0:
            if self.rectangulo.left <= 0:
                self.direccion = 1  # Change direction when hitting the left edge
                self.rectangulo.left = 0  # Set the left edge to 0

            elif self.rectangulo.right >= W:
                self.direccion = -1  # Change direction when hitting the right edge
                self.rectangulo.right = W  # Set the right edge to the screen width






        if self.direccionY!=0:
            if self.rectangulo.bottom>= H:
                self.direccionY *= -1  # Change direction when hitting the left edge

            elif self.rectangulo.top <= 0:
                self.direccionY *= -1  # Change direction when hitting the right edge


             # Recompute the collision borders
        self.borde_arriba = py.Rect(self.rectangulo.x, self.rectangulo.y, self.rectangulo.width, 1)
        self.borde_abajo = py.Rect(self.rectangulo.x, self.rectangulo.y + self.rectangulo.height, self.rectangulo.width, 1)
        self.borde_izquierda = py.Rect(self.rectangulo.x, self.rectangulo.y, 1, self.rectangulo.height)
        self.borde_derecha = py.Rect(self.rectangulo.x + self.rectangulo.width, self.rectangulo.y, 1, self.rectangulo.height)


    def update(self, pantalla):
        self.mover()
        pantalla.blit(self.superficie, self.rectangulo.topleft)
        if self.danio!=0:
            self.banderaDaño = True

        