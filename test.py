import pygame
import sys
from pygame.locals import *
from UI.GUI_form_menu import FormMenu
from UI.GUI_form_opciones import *
import json
import os

pygame.init()

WIDTH = 1200
HEIGHT = 700
FPS = 27

reloj = pygame.time.Clock()
PANTALLA = pygame.display.set_mode((WIDTH, HEIGHT))

icono = pygame.image.load("Recursos/icono1.png")
pygame.display.set_icon(icono)

pygame.display.set_caption("Michael Jackson Moonwalker Utn") #nombre ventana




# CREAR FORMULARIO
nuevo_form = FormMenu(
    PANTALLA,
    x=0,
    y=0,
    w=WIDTH,
    h=HEIGHT,
    color_background="green",
    color_border="blue",
    active=True,
    path_image="Recursos/efondo.png",
)  # formulario activo es que se muestre en pantalla

opciones = menu_opciones(
    screen=PANTALLA,
    x=0,
    y=0,
    w=W,
    h=H,
    color_background="green",
    color_border="blue",
    active=True,
    path_image="Recursos/test1.jpg",
)

reloj_opciones = pygame.time.Clock()  # Create a separate clock for opciones
while True:
    eventos = pygame.event.get()
    for event in eventos:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if os.path.exists("datos_volumen.json"):
        with open("datos_volumen.json", "r") as nivel2_file:
            content = json.load(nivel2_file)
            pausa = content.get("pausa", False)

    if not pausa:
        reloj.tick(FPS)
        nuevo_form.update(eventos)
    else:
        reloj.tick(0)        
        opciones.draw()

        reloj_opciones.tick(30)
        opciones.active = True  # Activate opciones when in pause mode
        opciones.update(eventos)

        with open("datos_volumen.json", "r") as nivel2_file:
            content = json.load(nivel2_file)
            pausa = content.get("pausa", False)

    pygame.display.update()
