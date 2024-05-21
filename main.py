import pygame
import sys
from pygame.locals import *
from interfaz.GUI_form_menu import FormMenu
from interfaz.GUI_form_opciones import *
import json
import os
import pygbag
import asyncio


pygame.init()

WIDTH = 1200
HEIGHT = 700
FPS = 27

reloj = pygame.time.Clock()
PANTALLA = pygame.display.set_mode((WIDTH, HEIGHT))

icono = pygame.image.load("assets\\icono1.png")
pygame.display.set_icon(icono)

pygame.display.set_caption("Michael Jackson Moonwalker Utn")  # nombre ventana

COUNT_DOWN = 3

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
    path_image="assets\\efondo.png",
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
    path_image="assets\\test1.jpg",
)

reloj_opciones = pygame.time.Clock()  # Create a separate clock for opciones

async def main():
    global pausa
    global COUNT_DOWN

    # avoid this kind declaration, prefer the way above
    COUNT_DOWN = 3
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
        await asyncio.sleep(0)  # Very important, and keep it 0



asyncio.run(main())