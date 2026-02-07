import pygame as py
from modo import *
from constantes import*
from Configuraciones import*

class Disparo2:
    def __init__(self, x, y, direccion,velocidad):
        self.superficie = py.image.load(r"Recursos/disparoCorto.png")
        self.superficie = py.transform.scale(self.superficie, (TAMAÑO_MARIO_X/3, TAMAÑO_MARIO_Y/6))
        self.rectangulo = self.superficie.get_rect()
        self.rectangulo.x = x
        self.rectangulo.centery = y
        self.direccion = direccion
        self.velocidad = velocidad
        self.inicial_x = x  # Store the initial x position


    def update(self):
        if self.direccion == 1:
            self.rectangulo.right+= 10
        elif self.direccion == -1:
            self.rectangulo.left-= 10
        self.avanzar()

  

    def avanzar (self):
       
        self.rectangulo.x += self.velocidad
    