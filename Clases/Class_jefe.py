import pygame as py
from Configuraciones import *
from Clases.Class_Disparo3 import*
from Clases.Class_Plataforma import*
import time
import random
class jefe:
    def __init__(self, animaciones, x, y,velocidad):
        self.animaciones = animaciones
        reescalar_imagenes(self.animaciones, 100, 100)
        self.salud = 100
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
        self.bandera=False

        self.imagen = py.image.load(r"Recursos/icono_huevo.png").convert()
        self.imagen = py.transform.scale( self.imagen, (W // 10, H // 13))  # Assuming W and H are defined somewhere

        self.velocidad = velocidad

        self.contador = 0
        self.fase2= False
            
    def animar(self, pantalla):


        pantalla.blit(self.animacion_actual[0], self.rectangulo_principal)

        if self.muriendo:
            self.esta_muerto = True


    def alternar_posicion(self):
        if self.contador == 2:

            posicion = random.randint(0, 3)

            if posicion == 0:
                self.rectangulo_principal.y = H/2.5
                self.rectangulo_principal.x = W-W/6
                self.contador = 0
            elif posicion == 1:
                self.rectangulo_principal.y = H/2.5
                self.rectangulo_principal.x = W/10
                self.contador = 0
            elif posicion == 2:
                self.rectangulo_principal.y =  H-H/6
                self.rectangulo_principal.x = W-W/6
                self.contador = 0
            else:
                self.rectangulo_principal.y = H-H/6
                self.rectangulo_principal.x = W/10
                self.contador = 0

    def alternar_posicion2(self):
        if self.contador == 2:

            posicion = random.randint(0, 1)

            if posicion == 0:
                self.rectangulo_principal.y = H/2.5
                self.contador = 0

            else:
                self.rectangulo_principal.y = H-H/6
                self.contador = 0



    def explosion(self, pantalla):
        self.animacion_actual = self.animaciones["bomba"]
        
        pantalla.blit(self.animacion_actual[self.contador_pasos], self.rectangulo_principal)
        self.contador_pasos += 1
        
        if self.contador_pasos >= len(self.animacion_actual):
            self.esta_muerto = True  # Set to True after the animation is complete
            self.contador_pasos = 0  # Reset the counter to restart the animation

        py.display.flip()


    def aplicar_gravedad(self, plataformas_lista: list["Plataforma"]):

                
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
        if tiempo_actual - self.tiempo_disparo > 2:
            self.tiempo_disparo = tiempo_actual

            self.animacion_actual = self.animaciones["izquierda"]

            self.lista_Proyectiles.append(Disparo3(self.rectangulo_principal.centerx,
                                                self.rectangulo_principal.centery,-self.direccion,
                                                1 * -self.direccion))

            print(len(self.lista_Proyectiles))

            if self.direccion !=1:
                self.animacion_actual = self.animaciones["derecha"]
                

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
            
                            

    def avanzar(self):
            self.rectangulo_principal.x += self.velocidad* self.direccion
            if self.rectangulo_principal.x >=W: 
                    self.velocidad *= -1  # Reverse the direction of movement
                    self.rectangulo_principal.x -= 15

            elif  self.rectangulo_principal.x <=0:
                    self.velocidad *= -1  # Reverse the direction of movement
                    self.rectangulo_principal.x += 15




    def update(self, pantalla,plataformas_lista):
        if self.esta_muerto == False:
            if self.salud >=49:
                self.alternar_posicion()
            if self.salud >0 and self.salud <50:
                self.fase2= True
                self.alternar_posicion2()
                self.avanzar()

            if self.salud <=0:
                 self.explosion(pantalla)
            
            self.lanzar_proyectil()
            self.animar(pantalla)
            self.aplicar_gravedad(plataformas_lista)
            self.actualizar_proyectiles( pantalla, plataformas_lista)

            pantalla.blit(self.imagen, (0, 0))

            font = py.font.Font(None, 45)  # You can adjust the font size as needed

            self.Tiempo_texto = f"Vida Dr. Huevo: {self.salud}"
            self.text_surface1 = font.render(  self.Tiempo_texto, True, (255, 255, 255)) 
            pantalla.blit(self.text_surface1,  (W/6, 0)) 
                
            
            if self.direccion==1:
                    self.animacion_actual = self.animaciones["izquierda"]
            else:
                self.animacion_actual = self.animaciones["derecha"]


        else: 
            self.rectangulo_principal.x = 0
            self.rectangulo_principal.y = 0