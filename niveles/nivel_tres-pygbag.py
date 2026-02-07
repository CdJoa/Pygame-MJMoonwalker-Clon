import pygame as py
from niveles.nivel_base import *
from Clases.Class_Plataforma import* 

from Clases.Class_Objetos import* 
from Clases.Class_Moneda import* 
from Clases.Class_Personaje import* 
from Clases.Class_Enemigo import* 
from Clases.Class_Enemigo2 import* 
from Clases.Class_Flecha import* 
from Clases.Class_jefe import* 

import random
from constantes import *





class NivelTres(Nivel):
      
      def __init__(self,pantalla:py.Surface):
            self.lista_enemigos = lista_enemigos

            py.mixer.stop()  
            sonido_nivel = py.mixer.Sound(r"Recursos/Smooth Criminal.ogg")
            sonido_nivel.play()

            lista_sonido = [sonido_nivel]

            pared = Plataforma((W/25,H), W-W/10, 0,0,0,0,r"Recursos/paredVioleta.png")

            Piso = Plataforma((W, H/10), 0, H-H/8,0,0,0, r"Recursos/piso.png")   # Cambia "Recursos/caño.png" al archivo correcto
            Piso2 = Plataforma((W/2.5, H/15), W/4, H/2+H/15,0,0,0, r"Recursos/piso.png")   # Cambia "Recursos/caño.png" al archivo correcto

            Pisob = Plataforma((W/15, H/25), W/12, H-H/3.5,0,0,0, r"Recursos/piso.png")   # Cambia "Recursos/caño.png" al archivo correcto

            Pisoc = Plataforma((W/15, H/25), W/2+W/4, H-H/3.5,0,0,0, r"Recursos/piso.png")  


            plataformas_lista = [pared,Piso,Piso2,Pisob,Pisoc]


            estrella2 = Objetos(diccionario_estrella,1,W-W/6,-H)


            estrella1 = Objetos(diccionario_estrella,2,W/6,H/8)
            estrella_lista = [estrella1,estrella2]
            
            botiquin2 = Objetos(diccionario_botiquin,0,W/2,H/3)

            botiquin_lista = [botiquin2]

                        
            vida1 = Objetos(diccionario_vida,0,W/2,H-H/6)
            vida_lista = [vida1]
            
            moneda = Moneda(diccionario_moneda,0,W/10,H-H/6)
            lista_monedas = [moneda]

            fondo = py.image.load(r"Recursos/fondo3.png").convert()
            fondo = py.transform.scale(fondo, (W,H))
            lista_enemigos2=[]
            huevo = jefe(diccionario_drHuevo,W-W/6,H-H/6,4)
            
            lista_llave = []

            flecha = Flecha(diccionario_flecha,0,W-W/20,H-H/4)

            lista_portal = [flecha]
            jefe_final = [huevo]

            super().__init__(pantalla, plataformas_lista, estrella_lista, lista_monedas, lista_enemigos,lista_enemigos2,botiquin_lista,vida_lista,lista_portal,lista_sonido,lista_llave,jefe_final, fondo)
 
