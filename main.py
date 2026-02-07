import pygame
from pygame.locals import *
from UI.GUI_form_menu import FormMenu
from UI.GUI_form_opciones import *
import asyncio
from data_manager import dm


pygame.init()

WIDTH = 1200
HEIGHT = 700
FPS = 27

reloj = pygame.time.Clock()
PANTALLA = pygame.display.set_mode((WIDTH, HEIGHT))

icono = pygame.image.load("Recursos/icono1.png")
pygame.display.set_icon(icono)

pygame.display.set_caption("Michael Jackson Moonwalker Utn")  # nombre ventana

COUNT_DOWN = 3

# Initialize pausa variable
pausa = False

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
    w=WIDTH,
    h=HEIGHT,
    color_background="green",
    color_border="blue",
    active=True,
    path_image="Recursos/test1.jpg",
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
            if event.type == pygame.QUIT:
                dm.save_jugador()
                dm.save_all()
                pygame.quit()
                return

        pausa = dm.volumen.get("pausa", False)

        if not pausa:
            reloj.tick(FPS)
            nuevo_form.update(eventos)
        else:
            reloj.tick(0)        
            opciones.draw()

            reloj_opciones.tick(30)
            opciones.active = True  # Activate opciones when in pause mode
            opciones.update(eventos)

            pausa = dm.volumen.get("pausa", False)

        pygame.display.update()
        await asyncio.sleep(0)  # Very important, and keep it 0



asyncio.run(main())