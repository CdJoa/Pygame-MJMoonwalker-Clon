import pygame as py
from constantes import *
import time
from Clases.Class_Plataforma import*
from Clases.Class_Objetos import* 
from Clases.Class_Enemigo import*
from Clases.Class_Moneda import *
from Clases.Class_Disparo import *
from Clases.Class_Disparo2 import *
import math
import sys
from data_manager import dm

class Personaje:
    def __init__(self, animaciones,animaciones2,tamaño, pos_x, pos_y,velocidad) -> None:
        self.animaciones = animaciones
        self.animaciones2 = animaciones2
        self.datos_guardados = False
        self.nivel_actual = None
        self.power_up = False
        self.golpeado = False

        self.resta = False
        self.muerto = 0
        self.retirada = 0
        self.Tiempo = 3000

        reescalar_imagenes(self.animaciones2, *tamaño)
        if self.power_up == False:
            reescalar_imagenes(self.animaciones, *tamaño)

        
        self.rectangulo_principal = self.animaciones["Quieto"][0].get_rect()
        self.rectangulo_principal.x = pos_x
        self.rectangulo_principal.y = pos_y

        self.velocidad = velocidad

        self.que_hace = "Quieto"
        self.contador_pasos = 0
        self.animacion_actual = self.animaciones["Quieto"]
        
        self.gravedad = 2
        self.desplazamiento_y = 0
        self.potencia_salto = -15
        self.limite_velocidad_salto = 15
        self.esta_saltando = False
        self.direccion = 1
        self.new_rect = self.rectangulo_principal.copy()
        self.esta_disparando = False
        self.TiempoDisparo= 0
        self.lista_Proyectiles = []
        self.muriendo = False
        self.Puntaje = 0
        self.llavero = False
        self.nivelCompletado = 0
        self.salud = dm.jugador.get("salud", 100)
        self.vidas = dm.jugador.get("vida", 2)
        self.Puntaje = dm.jugador.get("puntaje", 0)
        self.dobleSalto = False
        
        self.contador_Muertes = 0

        self.PuntajeNivel = 0


        self.asombro_sound = py.mixer.Sound("Recursos/Aaow!.ogg")
        self.golpeado_sound = py.mixer.Sound("Recursos/Oh!.ogg")
        self.disparo_sound = py.mixer.Sound("Recursos/laser.ogg")
        self.muerto_sound=py.mixer.Sound("Recursos/muerteMJ.ogg") 
        self.muerte_enemigo =py.mixer.Sound("Recursos/muerte_enemigos.ogg")
        self.muerte_mj_sound=py.mixer.Sound( "Recursos/muerteMJ.ogg") 
        self.nivel_completado_sound = py.mixer.Sound("Recursos/HEE HEE.ogg")

        self.lista_sonidos = [self.asombro_sound,self.golpeado_sound,self.disparo_sound,self.muerto_sound,self.muerte_enemigo,self.muerte_mj_sound,self.nivel_completado_sound]

    def update(self, pantalla, plataformas_lista,flor_lista,lista_monedas,lista_enemigos,lista_enemigos2,botiquin_lista,vida_lista,lista_portal,lista_llave,jefe_final):
        
        self.PuntajeNivel = self.Puntaje+ self.vidas*100 + self.Tiempo -self.contador_Muertes*300 +self.salud*100

        self.manejar_efectos_sonido()

        self.guardar_datos_jugador()

        self.handle_collision("Moneda", lista_monedas, "Puntaje", 500, pantalla)

        self.handle_collision("Botiquin", botiquin_lista, "salud", 100, pantalla)

        self.handle_collision("flecha", lista_portal, "nivelCompletado", 1, pantalla)
        self.handle_collision("llave", lista_llave, "llavero", True, pantalla)

        self.handle_collision("Flor", flor_lista, "power_up", True, pantalla)
        self.handle_collision("vida", vida_lista, "vidas", 1, pantalla)


        self.actualizar_proyectiles(pantalla,plataformas_lista,lista_enemigos,lista_enemigos2,jefe_final)
        self.verificar_colision_enemigo(lista_enemigos,lista_enemigos2,jefe_final, pantalla)
        self.manejo_vidas_salud()
        

        H = pantalla.get_height()


        if self.salud == 0:
            self.que_hace = "muerte"
                
        teclas = py.key.get_pressed()

        if self.vidas != 0:

            if self.muriendo!=True:
                    if (teclas[py.K_LEFT] or teclas[py.K_RIGHT]) and teclas[py.K_SPACE] and not self.esta_saltando:
                                self.que_hace = "salto_en_movimiento"
            match self.que_hace:
                case "Dispara":
                    self.disparo_sound.play()
                    if self.power_up==True:
                            self.animacion_actual = self.animaciones2["dispara"]
                    else:
                        self.animacion_actual = self.animaciones["dispara"]
                    if self.direccion == -1:
                        self.animacion_actual = rotar_imagen(self.animacion_actual)
                    self.animar(pantalla)
                case "Derecha":
                    self.direccion = 1
                    if not self.esta_saltando:
                        if self.power_up==True:
                            self.animacion_actual = self.animaciones2["Derecha"]
                        else:
                            self.animacion_actual = self.animaciones["Derecha"]
                        self.animar(pantalla)
                    self.mover(pantalla, plataformas_lista, self.velocidad)  # Provide both pantalla, plataformas, and velocidad as arguments
    # Provide both pantalla and plataformas as arguments
                    
                case "Izquierda":
                    self.direccion = -1
                    if not self.esta_saltando:
                        if self.power_up==True:
                            self.animacion_actual = self.animaciones2["Izquierda"]

                        else:
                            self.animacion_actual = self.animaciones["Izquierda"]
                        self.animar(pantalla)
                    self.mover(pantalla, plataformas_lista, self.velocidad)  # Provide both pantalla, plataformas, and velocidad as arguments

                case "Quieto":

                        if self.power_up==True:
                            self.animacion_actual = self.animaciones2["Quieto"]

                        else:
                            self.animacion_actual = self.animaciones["Quieto"]
                        self.animar(pantalla)
                case "Salta":
                    if not self.esta_saltando:
                        self.esta_saltando = True
                        self.dobleSalto = True

                        self.desplazamiento_y = self.potencia_salto
                        if self.power_up==True:
                            self.animacion_actual = self.animaciones2["salta"]

                        else:
                            self.animacion_actual = self.animaciones["salta"]
                        
                case "golpeado":
                    self.golpeado_sound.play()
                    self.animacion_actual = self.animaciones["golpeado"]
                    self.rectangulo_principal.y -=  2
                    self.salud -= 1
                    self.golpeado = True

                    self.animar(pantalla)

                case "muerte":
                    self.muerto_sound.play()
                    self.rectangulo_principal.x = W/100
                    self.rectangulo_principal.y =  H-H/4
                    self.animacion_actual = self.animaciones["muerte"]
                    self.animar(pantalla)
                    self.salud =100
                   

                case "salto_en_movimiento":

                    self.esta_saltando = True
                    self.desplazamiento_y = self.potencia_salto
                    self.dobleSalto = True
                    if self.power_up== True:
                        if teclas[py.K_LEFT]:
                            self.animacion_actual = rotar_imagen(self.animaciones2["salta"])
                            self.direccion = -1
                        else:
                            self.animacion_actual = self.animaciones2["salta"]

                    else:
                        if teclas[py.K_LEFT]:
                                        
                            self.animacion_actual = rotar_imagen(self.animaciones["salta"])
                            self.direccion = -1
                        else:
                            self.animacion_actual = self.animaciones["salta"]
                            
        
        self.aplicar_gravedad(pantalla, plataformas_lista)
        

        
    def animar(self, pantalla):
        largo = len(self.animacion_actual)

        if self.contador_pasos >= largo:
            self.contador_pasos = 0

        pantalla.blit(self.animacion_actual[self.contador_pasos],self.rectangulo_principal)
        self.contador_pasos += 1
    

    def mover(self, pantalla, plataformas_lista: list["Plataforma"], velocidad):
        
        if self.que_hace == "Izquierda":
            nueva_x = self.rectangulo_principal.x - velocidad
 
        elif self.que_hace == "Derecha":
            nueva_x = self.rectangulo_principal.x + velocidad
        
        elif self.que_hace == "dispara":
            if self.direccion == 1:
                nueva_x = self.rectangulo_principal.x + velocidad
            else:
                nueva_x = self.rectangulo_principal.x - velocidad
                
        self.new_rect = self.rectangulo_principal.copy()
        self.new_rect.x = nueva_x

        for plataforma in plataformas_lista:
            if self.new_rect.colliderect(plataforma.rectangulo):
                return


        self.rectangulo_principal.x = max(0, min(nueva_x, pantalla.get_width() - self.rectangulo_principal.width))


    def aplicar_gravedad(self, pantalla, plataformas_lista: list["Plataforma"]):
        self.animar(pantalla)

        if self.esta_saltando:
            
            self.rectangulo_principal.y += self.desplazamiento_y
            if self.desplazamiento_y + self.gravedad < self.limite_velocidad_salto:
                self.desplazamiento_y += self.gravedad
                
    
        for plataforma in plataformas_lista:
            if plataforma.banderaDaño==True:
                if self.rectangulo_principal.colliderect(plataforma.rectangulo):
                    self.golpeado_sound.play(1)

      
                    self.salud-=2
                    self.golpeado= True    
                    self.que_hace = "golpeado"
                    self.animar(pantalla)
                    if self.power_up ==True:
                        self.power_up = False


            if self.rectangulo_principal.colliderect(plataforma.borde_abajo):
                self.desplazamiento_y = 0
                self.esta_saltando = True
                self.rectangulo_principal.bottom = plataforma.borde_abajo.bottom + (TAMAÑO_MARIO_Y)
                plataforma.golpeado = True

                break
            elif self.rectangulo_principal.colliderect(plataforma.borde_arriba):
                self.desplazamiento_y = 0
                self.esta_saltando = False
                self.rectangulo_principal.bottom = plataforma.borde_arriba.top
                break
            else:
                self.esta_saltando = True

    def verificar_colision_enemigo(self,lista_enemigos:list["Enemigo"],lista_enemigos2,jefe_final, pantalla):
        for enemigo in lista_enemigos or lista_enemigos2 or jefe_final:
            if self.vidas != 0:
                
                    if self.rectangulo_principal.colliderect(enemigo.rectangulo_principal):


      
                        self.golpeado= True    
                        self.que_hace = "golpeado"
                        

                        if self.power_up ==True:
                            self.power_up = False



                        self.tiempo_Golpeado = time.time()

                        if self.tiempo_Golpeado == 0:
                                
                                

                                if self.tiempo_Golpeado== 3:
                                    self.que_hace= "derecha"
                                    self.tiempo_Golpeado== 0

                    
            
    def handle_collision(self, obj, lista, nombre_categoria, suma, pantalla):

        for item in lista:
            if self.rectangulo_principal.colliderect(item.rectangulo_principal):
                print(f"Choco {obj}")
                item.muriendo = True
                lista.remove(item)
                
                # Special sound for level completion (portal collision)
                if obj == "flecha" and nombre_categoria == "nivelCompletado":
                    self.nivel_completado_sound.play(1)
                else:
                    self.asombro_sound.play(1)
                
                # If the attribute exists, update it
                if hasattr(self, nombre_categoria):
                    setattr(self, nombre_categoria, getattr(self, nombre_categoria) + suma)

                # If there's a specific animation, use it
                if hasattr(item, "animacion_actual"):
                    item.animacion_actual = item.animaciones.get("aplastado", item.animacion_actual)
                    item.animar(pantalla)




    def lanzar_proyectil(self):
        if self.que_hace != "muerte":
            if self.power_up == True:
                self.lista_Proyectiles.append(Disparo(self.rectangulo_principal.centerx,((self.rectangulo_principal.y)+(TAMAÑO_MARIO_Y/5)),self.direccion,5*self.direccion))
            else:
                self.lista_Proyectiles.append(Disparo2(self.rectangulo_principal.centerx,((self.rectangulo_principal.y)+(TAMAÑO_MARIO_Y/5)),self.direccion,self.direccion))


            print(len(self.lista_Proyectiles))
        
    def actualizar_proyectiles(self, pantalla, plataformas_lista, lista_enemigos,lista_enemigos2,jefe_final):
        i = len(self.lista_Proyectiles) - 1
        while i >= 0:
            try:
                p = self.lista_Proyectiles[i]
                pantalla.blit(p.superficie, p.rectangulo)
                p.update()

                for plataforma in plataformas_lista:
                    if p.rectangulo.colliderect(plataforma.rectangulo):
                        self.lista_Proyectiles.pop(i)
                        break

                for enemigo in lista_enemigos:
                    if p.rectangulo.colliderect(enemigo.rectangulo_principal):
                        self.lista_Proyectiles.pop(i)
                        enemigo.muriendo = True
                        lista_enemigos.remove(enemigo)
                        enemigo.animacion_actual = enemigo.animaciones["aplastado"]
                        enemigo.animar(pantalla)
                        self.muerte_enemigo.play(1)
                        self.Puntaje += 100
                        break
                
                
                for enemigo in lista_enemigos2:
                    if p.rectangulo.colliderect(enemigo.rectangulo_principal):
                        self.lista_Proyectiles.pop(i)
                        enemigo.muriendo = True
                        lista_enemigos2.remove(enemigo)
                        enemigo.animacion_actual = enemigo.animaciones["aplastado"]
                        enemigo.animar(pantalla)
                        self.muerte_enemigo.play(1)

                        self.Puntaje += 100
                        break

                for enemigo in jefe_final:
                    if p.rectangulo.colliderect(enemigo.rectangulo_principal):
                        
                        if not self.power_up:
                                enemigo.salud -= 5
                        else:
                            enemigo.salud -= 10
                        enemigo.contador+=1
                        self.lista_Proyectiles.pop(i)

                        enemigo.animacion_actual = enemigo.animaciones["aplastado"]
                        if enemigo.direccion ==1:
                            enemigo.animacion_actual = rotar_imagen(enemigo.animaciones["aplastado"])

                              
                        enemigo.animar(pantalla)
                        self.muerte_enemigo.play(1)

                        self.Puntaje += 100
                        break


                if p.rectangulo.centerx < 0 or p.rectangulo.centerx > W:
                    self.lista_Proyectiles.pop(i)

                if not self.power_up:
                    distance = math.sqrt((self.new_rect.centerx - p.rectangulo.centerx) ** 2)
                    if distance > 250:
                        self.lista_Proyectiles.pop(i)

            except IndexError:
                print("error disparo")

            i -= 1



        if obtener_modo()==True:

            for p in self.lista_Proyectiles:
                # Dibuja el rectángulo principal de la plataforma
                py.draw.rect(pantalla, "white", p.rectangulo, 3)
        
    def manejo_vidas_salud(self):

            if self.salud <= 0:
                self.tiempo_muerto = time.time()
                self.que_hace = "muerte" 
                self.contador_Muertes +=1

                if self.vidas != 0:
                    self.salud = 100
                else: 
                    self.salud = 0
                self.rectangulo_principal.y =  self.rectangulo_principal.y - 10

                self.animacion_actual = self.animaciones["muerte"]
                self.vidas -= 1
                self.muerte_mj_sound.play(1)
            
            if self.salud > 100:
                self.salud = 100

            if self.vidas == 0:
                self.muerto=1

            if self.rectangulo_principal.y>= H:
                self.vidas -= 1
                self.contador_Muertes +=1

                self.tiempo_muerto = 0
                self.rectangulo_principal.y= H-H/3
                self.rectangulo_principal.x = W/80

    def guardar_datos_jugador(self):
        dm.jugador["salud"] = self.salud
        dm.jugador["vida"] = self.vidas
        dm.jugador["puntaje"] = self.Puntaje
        dm.jugador["nivel completado"] = self.nivelCompletado
        dm.jugador["nivel actual"] = self.nivel_actual
        dm.jugador["muerto"] = self.muerto
        dm.jugador["Muertes"] = self.contador_Muertes
        dm.jugador["Tiempo"] = self.Tiempo
        dm.jugador["Puntaje Nivel"] = self.PuntajeNivel

        
    def manejar_efectos_sonido(self):
        self.volumen_efectos = dm.volumen.get("volumen_efectos", 0)
        for sound in self.lista_sonidos:
            sound.set_volume(self.volumen_efectos)
