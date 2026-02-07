import pygame as py
from Configuraciones import *
from Clases.Class_Disparo3 import*
from Clases.Class_Plataforma import*
import time

class Enemigo2:
    def __init__(self, animaciones, x, y):
        self.animaciones = animaciones
        reescalar_imagenes(self.animaciones, 50, 100)

        self.direccion = 1
        self.rectangulo_principal = self.animaciones["izquierda"][0].get_rect()
        self.animacion_actual = self.animaciones["izquierda"]

        self.rectangulo_principal.x = x
        self.rectangulo_principal.y = y

        self.banderaDisparo = False

        self.esta_muerto = False
        self.contador_pasos = 0

        self.banderaDisparo = False

        self.gravedad = 1 
        self.desplazamiento_y = 0
        self.muriendo = False

        self.lista_Proyectiles = []
        self.tiempo_disparo = 0  # Added to track the last time a shot was fired


            
    def animar(self, pantalla):


        pantalla.blit(self.animacion_actual[0], self.rectangulo_principal)

        if self.muriendo:
            self.esta_muerto = True


        
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
    

    def lanzar_proyectil(self):

        tiempo_actual = time.time()
        if tiempo_actual - self.tiempo_disparo > 1:
            self.tiempo_disparo = tiempo_actual

            self.animacion_actual = self.animaciones["dispara"]

            self.lista_Proyectiles.append(Disparo3(self.rectangulo_principal.centerx,
                                                self.rectangulo_principal.centery,-self.direccion,
                                                2 * -self.direccion))
            




    def actualizar_proyectiles(self, pantalla, plataformas_lista):
        i = 0
        while i < len(self.lista_Proyectiles):
            p = self.lista_Proyectiles[i]
            pantalla.blit(p.superficie, p.rectangulo)
            p.update()

            for plataforma in plataformas_lista:
                if p.rectangulo.colliderect(plataforma.rectangulo):
                    self.lista_Proyectiles.remove(p)
                    i -= 1
                    break

            if p.rectangulo.centerx < 0 or p.rectangulo.centerx > W:
                self.lista_Proyectiles.remove(p)
                i -= 1

            


            i += 1
            
                            



    def update(self, pantalla,plataformas_lista):
        if self.esta_muerto == False:
            self.lanzar_proyectil()
            self.animar(pantalla)
            self.aplicar_gravedad(plataformas_lista)
            self.actualizar_proyectiles( pantalla, plataformas_lista)







    

    