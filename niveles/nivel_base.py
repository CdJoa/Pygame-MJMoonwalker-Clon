import pygame as py
from modo import *
py.init()
RELOJ = py.time.Clock()
import time
from Configuraciones import *
from constantes import*
from Clases.Class_Disparo import*
from Clases.Class_Personaje import*
from UI.GUI_form_opciones import *
from UI.GUI_form import*
from data_manager import dm

class Nivel(Form):
    def __init__(self,pantalla,plataformas_lista,estrella_lista,lista_monedas,lista_enemigos,lista_enemigos2,botiquin_lista,vida_lista,lista_portal,lista_sonido,lista_llave,jefe_final,imagen_fondo):
        
        if dm.niveles.get("medio", 0) == 1:
            dm.niveles["medio"] = 0

        self.sonido=lista_sonido

        self.jefe = jefe_final
        self._slave = pantalla
        self.plataformas = plataformas_lista
        self.estrella = estrella_lista
        self.monedas = lista_monedas
        self.enemigos = lista_enemigos
        self.enemigos2 = lista_enemigos2
        self.llave = lista_llave
        self.botiquin = botiquin_lista
        self.vidaUp = vida_lista
        self.img_fondo = imagen_fondo
        self.portal = lista_portal
        self.banderaTiempo = False

        self.jugador = Personaje(acciones,acciones_power_up,(TAMAÑO_MARIO), W/80,H-H/3 ,10) 
        self.jugador.nivelCompletado = 0
        self.jugador.salud = 100
        self.jugador.Puntaje = 0


        self.pausa_base_nivel = False  # Flag to pause the base level


    def update(self, lista_eventos):

        pygame.display.update()

        self.volumen_musica = dm.volumen.get("volumen_musica", 0)

        self.jugador.Tiempo -= 1
        if self.jugador.Tiempo ==-1:

            self.jugador.Tiempo= self.jugador.Tiempo+1

        if self.jugador.Tiempo == 0 and not self.banderaTiempo:
            self.banderaTiempo = True# Subtract one life from the player
            self.jugador.vidas -= 1
        
        if self.jugador.Tiempo == 350:

            sonido_nivel2 = py.mixer.Sound(r"Recursos/contrarreloj.mp3")
            sonido_nivel2.set_volume(0.25)  # Adjust the volume as needed (0.5 represents 50% volume)

            sonido_nivel2.play(0)

        
        if self.jugador.vidas != 0:
                for event in lista_eventos:
                    if event.type == py.KEYDOWN:
                        if event.key == py.K_TAB:
                            cambiar_modo()
                        if (event.key == py.K_SPACE and self.jugador.dobleSalto == True):
                            
                            self.jugador.desplazamiento_y = self.jugador.potencia_salto

                            self.jugador.dobleSalto = False
                    if event.type == py.KEYDOWN:
                        if event.key == py.K_ESCAPE:
                            dm.volumen["pausa"] = True
                            dm.save_volumen()

                           

                    elif event.type == py.KEYUP:
                        if event.key == py.K_x:
                                if self.jugador.que_hace != "golpeado":
                                        self.jugador.lanzar_proyectil()

                                        
                
                if self.jugador.que_hace != "muerte":
                        self.leer_inputs()

        for sound in self.sonido:
                sound.set_volume(self.volumen_musica)

        self.actualizar_pantalla()
        self.dibujar_rectangulos()
      
        self.ui()


        if self.jugador.llavero == True:
            self.plataformas.pop(0)
            self.jugador.llavero = False


            


            
    def actualizar_pantalla(self):

        self._slave.blit(self.img_fondo, (0, 0))

           
        for plataforma in self.plataformas:
            plataforma.update(self._slave)

        for llave in self.llave:
            llave.update(self._slave)


        for vida in self.vidaUp:
            imagen_actual = vida.animacion_actual[vida.contador_pasos]
            self._slave.blit(imagen_actual, vida.rectangulo_principal)


        for estrella in self.estrella:
            if estrella.contador_pasos >= len(estrella.animacion_actual):
                estrella.contador_pasos = 0  # Reset the counter to restart the animation

            imagen_actual = estrella.animacion_actual[estrella.contador_pasos]
            self._slave.blit(imagen_actual, estrella.rectangulo_principal)
            estrella.update(self._slave)
            if estrella.rectangulo_principal.y > H:
                self.estrella.remove(estrella)

                
        for moneda in self.monedas:
            moneda.update(self._slave)


        for portal in self.portal:
            portal.update(self._slave)


        for botiquin in self.botiquin:
            imagen_actual = botiquin.animacion_actual[botiquin.contador_pasos]
            self._slave.blit(imagen_actual, botiquin.rectangulo_principal)

        
        for jefe in self.jefe:
            if jefe.esta_muerto== True and jefe.bandera == False:
                    jefe.bandera=True
                    self.plataformas.pop(0)
                    self.jugador.llavero = False
                    self.jugador.Puntaje+=5000

            self.distancia = W/10
            jefe.update(self._slave,self.plataformas) 

            
            if self.jugador.rectangulo_principal.x <= jefe.rectangulo_principal.x:
                    jefe.direccion=1
            else:
                jefe.direccion =-1


            if jefe.rectangulo_principal.colliderect(self.jugador.rectangulo_principal):
                self.jugador.rectangulo_principal.x -= self.distancia/2

            for p in jefe.lista_Proyectiles:

                    if self.jugador.que_hace != "muerte" or self.jugador.que_hace != "golpeado":
                    
                        if self.jugador.rectangulo_principal.colliderect(p.rectangulo):
                                    self.jugador.salud = self.jugador.salud-20
                                    
                                    jefe.lista_Proyectiles.remove(p)
                                    self.jugador.que_hace = "golpeado"
                                    self.jugador.animacion_actual = self.jugador.animaciones["golpeado"]

                                    if self.jugador.power_up ==True:
                                        self.jugador.power_up = False


        for enemigo in self.enemigos:
            enemigo.update(self._slave,self.plataformas)  # Provide plataformas_lista argument

        for enemigo2 in self.enemigos2:
            enemigo2.update(self._slave,self.plataformas)  # Provide plataformas_lista argument

            if self.jugador.rectangulo_principal.x <= enemigo2.rectangulo_principal.x:
                    enemigo2.direccion=1
                    enemigo2.animacion_actual = enemigo2.animaciones["izquierda"]
            else:
                enemigo2.direccion =-1

                enemigo2.animacion_actual = rotar_imagen(enemigo2.animaciones["izquierda"])
                

            for p in enemigo2.lista_Proyectiles:

                if self.jugador.que_hace != "muerte" or self.jugador.que_hace != "golpeado":
                
                    if self.jugador.rectangulo_principal.colliderect(p.rectangulo):
                                self.jugador.salud = self.jugador.salud-20
                                
                                enemigo2.lista_Proyectiles.remove(p)
                                self.jugador.que_hace = "golpeado"
                                self.jugador.animacion_actual = self.jugador.animaciones["golpeado"]

                                if self.jugador.power_up ==True:
                                    self.jugador.power_up = False

        self.jugador.update(self._slave, self.plataformas,self.estrella,self.monedas,self.enemigos,self.enemigos2,self.botiquin,self.vidaUp,self.portal,self.llave,self.jefe)


    def leer_inputs(self):
        teclas = py.key.get_pressed()
        if self.jugador.vidas != 0:


                if teclas[py.K_RIGHT]:
                    self.jugador.que_hace = "Derecha"
                elif teclas[py.K_LEFT]:
                    self.jugador.que_hace = "Izquierda"
                elif teclas[py.K_SPACE]:
                    self.jugador.que_hace = "Salta"

                elif teclas[py.K_x]:
                    self.jugador.que_hace = "Dispara"
                            
                else:
                    self.jugador.que_hace = "Quieto"

    def dibujar_rectangulos(self):
        if obtener_modo()==True:

            for pl in self.plataformas:
                # Dibuja el rectángulo principal de la plataforma
                py.draw.rect(self._slave, "orange", pl.rectangulo, 3)

            for est in self.estrella:
                py.draw.rect(self._slave, "green", est.rectangulo_principal, 3)
            for bt in self.botiquin:
                py.draw.rect(self._slave, "green", bt.rectangulo_principal, 3)
            
            
            for mn in self.monedas:
                py.draw.rect(self._slave, "black", mn.rectangulo_principal, 3)

            
            for enemigo in self.enemigos:
                
                        py.draw.rect(self._slave, "red", enemigo.rectangulo_principal, 3)

            for enemigo in self.enemigos2:
                
                        py.draw.rect(self._slave, "red", enemigo.rectangulo_principal, 3)

            
            for enemigo in self.jefe:
                
                        py.draw.rect(self._slave, "red", enemigo.rectangulo_principal, 3)


            py.draw.rect(self._slave, "blue", self.jugador.rectangulo_principal, 3)

    
    def ui(self):
        imagen = py.image.load(r"Recursos/ui0.png").convert()
        imagen = py.transform.scale(imagen, (W // 10, H // 13))  # Assuming W and H are defined somewhere
        self._slave.blit(imagen, (0, H-H/9))
        font = py.font.Font(None, 45)  # You can adjust the font size as needed

        if self.jugador.vidas != 0:
            salud_texto = f"Salud: {self.jugador.salud}% "
            text_surface = font.render(salud_texto, True, (255, 255, 255))  # Assuming white text color
            self._slave.blit(text_surface, ( W/3, H - H / 16)) 


        vida_texto = f"x {self.jugador.vidas}"
        text_surface1 = font.render(vida_texto, True, (255, 255, 255))  # Assuming white text color
        self._slave.blit(text_surface1, ( W/6, H - H / 13)) 


        Puntaje_texto = f"Puntaje Nivel: {self.jugador.Puntaje}"
        text_surface1 = font.render(Puntaje_texto, True, (255, 255, 255))  # Assuming white text color
        self._slave.blit(text_surface1, ( W-W/4, H - H / 13)) 

        
        Tiempo_texto = f"Tiempo: {self.jugador.Tiempo}"
        text_surface1 = font.render(Tiempo_texto, True, (255, 255, 255))  # Assuming white text color
        self._slave.blit(text_surface1, ( W/2, H - H / 13)) 


        
        if self.jugador.vidas == 0:
                game_over = f"game over"
                text_surface2 = font.render(game_over, True, (255, 255, 255))  # Assuming white text color
                self._slave.blit(text_surface2, ( W/2, H/2))



