import pygame as py
import sys
from pygame.locals import *
from Configuraciones import *
from os import system
from niveles.nivel_uno import NivelUno
from niveles.nivel_dos import NivelDos
from niveles.nivel_tres import NivelTres




class ManejadorNiveles:
    def __init__(self,pantalla)->None:
        self._slave = pantalla
        self.niveles = {"nivel_uno":NivelUno,"nivel_dos":NivelDos,"nivel_tres":NivelTres}

    def get_level(self,nombre_nivel):

        return self.niveles[nombre_nivel](self._slave)
        


