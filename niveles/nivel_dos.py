import pygame as py
from niveles.nivel_base import *
from Clases.Class_Plataforma import* 
from Clases.Class_Flecha import*
from Clases.Class_Objetos import* 
from Clases.Class_Moneda import* 
from Clases.Class_Personaje import* 
from Clases.Class_Enemigo import* 
from Clases.Class_Enemigo2 import* 

import random
from constantes import *

from data_manager import dm


class NivelDos(Nivel):
      
      def __init__(self,pantalla:py.Surface):
            self.lista_enemigos = lista_enemigos

            py.mixer.stop()  
            sonido_nivel = py.mixer.Sound("Recursos/Beat It.mp3")
            sonido_nivel.play()
            lista_sonido = [sonido_nivel]

            dm.jugador = dict(dm.nivel1)

            W = pantalla.get_width()
            H = pantalla.get_height()
                                
            moneda = Moneda(diccionario_moneda,0,W/4,H/4)
            lista_monedas = [moneda]

            pared = Plataforma((W/15,H/2), W-W/4, H/3,0,0,0,r"Recursos/paredVioleta.png")
            Piso = Plataforma((W/8, H/15), 0, H-H/8,0,0,0,r"Recursos/piso.png")   # Cambia "Recursos/caño.png" al archivo correcto
            Pisob = Plataforma((W/8, H/15), W/3, H-H/8,0,0,0, r"Recursos/piso.png")   # Cambia "Recursos/caño.png" al archivo correcto

            Pisoc = Plataforma((W/8, H/15), W/2, H-H/8,0,0,0, r"Recursos/piso.png")   # Cambia "Recursos/caño.png" al archivo correcto


            Piso2 = Plataforma((W/2, H/15), 0, H/2+H/8,0,0,0, r"Recursos/piso.png")   # Cambia "Recursos/caño.png" al archivo correcto
            Piso3 = Plataforma((W/8, H/15), W-W/2.5, H-H/4,0,0,0, r"Recursos/piso.png")   # Cambia "Recursos/caño.png" al archivo correcto
            Piso4 = Plataforma((W/8, H/15), 0, H/2,0,0,0, r"Recursos/piso.png")   # Cambia "Recursos/caño.png" al archivo correcto
            Piso5 = Plataforma((W/12, H/15), 0, H/3,1,0,0, r"Recursos/piso.png")   # Cambia "Recursos/caño.png" al archivo correcto
            
            Piso6 = Plataforma((W/8, H/12),W/3, H/5,0,0,0, r"Recursos/piso.png")   # Cambia "Recursos/caño.png" al archivo correcto
            Piso7 = Plataforma((W/2, H/20), W/2, H/4,0,0,1, r"Recursos/lava2.png")   # Cambia "Recursos/caño.png" al archivo correcto


            llave1= Objetos(diccionario_llave,0,W-W/15,H/8)

            lista_llave = [llave1]



            plataformas_lista = [pared,Piso,Pisob,Pisoc,Piso2,Piso3,Piso4,Piso5,Piso6,Piso7]

            estrella1 = Objetos(diccionario_estrella,4,W/6,H/8)

            estrella_lista = [estrella1]
            
            botiquin1 = Objetos(diccionario_botiquin,0,W/2,H-H/3)
            botiquin_lista = [botiquin1]

            self.generar_enemigos(lista_enemigos)

                        
            vida1 = Objetos(diccionario_vida,0,W/2, H/2)
            vida_lista = [vida1]
    

            fondo = py.image.load(r"Recursos/fondo2.png").convert()
            fondo = py.transform.scale(fondo, (W,H))
            
            un_enemigo3 = Enemigo2(diccionario_enemigoQuieto,W/3,H/2)

            un_enemigo4= Enemigo2(diccionario_enemigoQuieto,W/20,H/6)

            lista_enemigos2 = [un_enemigo3,un_enemigo4]
            

            flecha = Flecha(diccionario_flecha,0,W-W/20,H/2)

            lista_portal = [flecha]

            jefe_final = []

            super().__init__(pantalla, plataformas_lista, estrella_lista, lista_monedas, lista_enemigos,lista_enemigos2,botiquin_lista,vida_lista,lista_portal,lista_sonido,lista_llave,jefe_final,fondo)

      
      def generar_enemigos(self, lista_enemigos):
            self.lista_enemigos.clear()

            cantidad = random.randint(2, 5)  # Puedes ajustar el rango según tus necesidades

            velocidades_unicas = (set(random.uniform(5, 10) for _ in range(cantidad)))

            # Crear enemigos con las velocidades únicas
            for velocidad in velocidades_unicas:

                  nuevo_enemigo = Enemigo(diccionario_enemigo, velocidad, W / 2 + W/4, 0)
                  lista_enemigos.append(nuevo_enemigo)
      

