import pygame as py
from Configuraciones import *
from Clases.Class_Disparo import*
from Clases.Class_Plataforma import*


class Enemigo:
    def __init__(self, animaciones, velocidad, x, y):
        self.animaciones = animaciones
        reescalar_imagenes(self.animaciones, 100, 100)

        self.rectangulo_principal = self.animaciones["izquierda"][0].get_rect()
        self.rectangulo_principal.x = x
        self.rectangulo_principal.y = y

        self.velocidad = velocidad

        self.esta_muerto = False
        self.contador_pasos = 0
        self.animacion_actual = self.animaciones["izquierda"]

        self.gravedad = 1 
        self.desplazamiento_y = 0
        self.muriendo = False


    def avanzar(self, plataformas_lista):
        self.rectangulo_principal.x += self.velocidad
        for plataforma in plataformas_lista:
            if self.rectangulo_principal.colliderect(plataforma.borde_izquierda)or self.rectangulo_principal.x >=W: 
                self.velocidad *= -1  # Reverse the direction of movement
                self.rectangulo_principal.x -= 15

            elif self.rectangulo_principal.colliderect(plataforma.borde_derecha) or self.rectangulo_principal.x <=0:
                self.velocidad *= -1  # Reverse the direction of movement
                self.rectangulo_principal.x += 15

            if self.velocidad >=0:
                self.animacion_actual = self.animaciones["derecha"]

            else:
                self.animacion_actual = self.animaciones["izquierda"]

            
            
    def animar(self, pantalla):
        largo = len(self.animacion_actual)

        if self.contador_pasos >= largo:
            self.contador_pasos = 0

        

        pantalla.blit(self.animacion_actual[self.contador_pasos], self.rectangulo_principal)
        self.contador_pasos += 1

        if self.muriendo and self.contador_pasos == 2:
            self.esta_muerto = True


        if self.velocidad >=0:
                 self.animacion_actual = rotar_imagen(self.animacion_actual)

        
    def aplicar_gravedad(self, plataformas_lista: list["Plataforma"]):
            self.rectangulo_principal.y += self.desplazamiento_y
            self.desplazamiento_y += self.gravedad
                
            for plataforma in plataformas_lista:
                if self.rectangulo_principal.colliderect(plataforma.borde_abajo):
                    self.desplazamiento_y = 0
                    self.rectangulo_principal.bottom = plataforma.borde_abajo.bottom + (TAMAÑO_MARIO_Y)
                    break
                elif self.rectangulo_principal.colliderect(plataforma.borde_arriba):
                    self.desplazamiento_y = 0
                    self.rectangulo_principal.bottom = plataforma.borde_arriba.top
                    break
                


    def update(self, pantalla,plataformas_lista):
        if self.esta_muerto == False:
            self.animar(pantalla)
            self.avanzar(plataformas_lista)
            self.aplicar_gravedad(plataformas_lista)



