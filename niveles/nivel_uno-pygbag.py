import pygame as py
from niveles.nivel_base import *
from Clases.Class_Plataforma import* 

from Clases.Class_Objetos import* 
from Clases.Class_Moneda import* 
from Clases.Class_Personaje import* 
from Clases.Class_Enemigo import* 
from Clases.Class_Enemigo2 import* 
from Clases.Class_Flecha import* 
import shutil

import random
from constantes import *





class NivelUno(Nivel):
      
      def __init__(self,pantalla:py.Surface):

            py.mixer.init()
            sonido_nivel = py.mixer.Sound(r"Recursos/Billie Jean.ogg")
            sonido_nivel.play()

            lista_sonido = [sonido_nivel]


            pisob1 = Plataforma((W/10,  H/15), W-W/5, H-H/3,0,0,0, r"Recursos/piso.png")  
            pisoc = Plataforma((W/15, H/15),W/6, H/4.5,0,0,0, r"Recursos/piso.png")  
            pisoE = Plataforma((W-W/5, H/15),W/5, H/4,0,0,0, r"Recursos/piso.png")  
            



            piso4 = Plataforma((W/10, H/15), 0, H/2 - H/8,0,0,0, r"Recursos/piso.png")  
            


            lava = Plataforma((W, H/10), 0, H-H/8,0,0,1, r"Recursos/lava.png")   # Cambia "Recursos/caño.png" al archivo correcto
            piso3 = Plataforma((W/10, H/15), W/9, H-H/6,-1,0,0, r"Recursos/piso.png")   # Cambia "Recursos/caño.png" al archivo correcto
           
            piso2 = Plataforma((W/10, H/15), W/2, H/2,1,0,0,r"Recursos/piso.png")   # Cambia "Recursos/caño.png" al archivo correcto



            plataformas_lista = [lava,piso2,piso3,pisob1,piso4,pisoc,pisoE]



            estrella1 = Objetos(diccionario_estrella,2,W-W/6,H/8)
            estrella_lista = [estrella1]
            
            botiquin1 = Objetos(diccionario_botiquin,0,W-W/8,H/3)
            botiquin_lista = [botiquin1]

                        
            vida1 = Objetos(diccionario_vida,0,W-W/10,H/2+H/4)
            vida_lista = [vida1]
            
            moneda = Moneda(diccionario_moneda,0,W/2,H/3)
            moneda2 = Moneda(diccionario_moneda,0,W/3,H/3)
            moneda3 = Moneda(diccionario_moneda,0,W/3,H/3)

            lista_monedas = [moneda,moneda2,moneda3]

            fondo = py.image.load(r"Recursos/fondo1.png").convert()
            fondo = py.transform.scale(fondo, (W,H))
            
            un_enemigo3 = Enemigo2(diccionario_enemigoQuieto,0,H/7)

            lista_enemigos2 = [un_enemigo3]
            

            self.generar_enemigos(lista_enemigos)


            flecha = Flecha(diccionario_flecha,0,W-W/20,H/8)

            lista_portal = [flecha]
            lista_llave = []

            jefe_final = []

            super().__init__(pantalla, plataformas_lista, estrella_lista, lista_monedas, lista_enemigos,lista_enemigos2,botiquin_lista,vida_lista,lista_portal,lista_sonido,lista_llave,jefe_final, fondo)

      def generar_enemigos(self, lista_enemigos):

            cantidad = random.randint(2, 5)  # Puedes ajustar el rango según tus necesidades

            velocidades_unicas = (set(random.uniform(5, 10) for _ in range(cantidad)))

            # Crear enemigos con las velocidades únicas
            for velocidad in velocidades_unicas:

                  nuevo_enemigo = Enemigo(diccionario_enemigo, velocidad, W / 2, 0)
                  lista_enemigos.append(nuevo_enemigo)
      