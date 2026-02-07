import pygame as py
from Configuraciones import *




class Flor:
    def __init__(self, animaciones, velocidad, x, y):
        self.animaciones = animaciones
        reescalar_imagenes(self.animaciones, 50, 50)

        self.rectangulo_principal = self.animaciones["izquierda"][0].get_rect()
        self.rectangulo_principal.x = x
        self.rectangulo_principal.y = y

        self.velocidad = velocidad

        self.esta_muerto = False
        self.contador_pasos = 0
        self.animacion_actual = self.animaciones["izquierda"]

        self.muriendo = False



    def animar(self, pantalla):


        pantalla.blit(self.animacion_actual[self.contador_pasos], self.rectangulo_principal)
        self.contador_pasos += 1

    def update(self, pantalla):
        if self.esta_muerto == False:
            self.animar(pantalla)
