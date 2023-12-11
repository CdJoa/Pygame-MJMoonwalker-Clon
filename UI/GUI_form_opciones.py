import pygame
from pygame.locals import *
import os
from UI.GUI_button_image import *
from UI.GUI_form import *
from UI.GUI_label import *
from UI.GUI_form_niveles import *
from UI.GUI_form_menu_score import *
from UI.GUI_textbox import *
from UI.GUI_slider import *
import pygame as py
import sys
import sqlite3 as sql
import csv
import pandas as pd
import json

W,H = 1200, 700
class menu_opciones(Form):
    def __init__(self, screen, x, y, w, h, color_background, color_border, active, path_image):
        super().__init__(screen, x, y, w, h, color_background, color_border, active)
        aux_image = pygame.image.load(path_image)
        self.aux_image = pygame.transform.scale(aux_image, (w, h))

        self.bandera = 0

        py.mixer.init()

        with open("datos_volumen.json", "r") as nivel2_file:
            content = json.load(nivel2_file)
            self.volumen_musica = content.get("volumen_musica", 0)
            self.volumenEfectos = content.get("volumen_efectos", 1)

        self.boton_exit = Button_Image(screen=self._slave,
                                       master_x=x,
                                       master_y=y,
                                       x=w - w / 8,
                                       y=h - h / 6,
                                       w=w / 10,
                                       h=h / 10,
                                       path_image="Recursos\exit.png",
                                       onclick=self.btn_home_click,
                                       onclick_param=""
                                       )
        
        self.slider_volumen_musica = Slider(self._slave, x, y, 
                                    W/12, W/6, W/3, H/35, 
                                    self.volumen_musica, 
                                    "blue", "white")
        
        porcentaje_volumen_musica= f"{self.volumen_musica * 100}%"  # Display two decimal places
        self.label_volumen_musica = Label(self._slave, W/2, H/3, W/12, H/12, porcentaje_volumen_musica, 
                                "Comic Sans MS", 15, "white", "Recursos\Table.png")



        
        self.Musica_on = Button_Image(screen=self._slave,
                                       master_x=x,
                                       master_y=y,
                                       x=w /4,
                                       y=h / 2,
                                       w=w / 10,
                                       h=h / 10,
                                       path_image="Recursos\sonidoOnn.png",
                                       onclick=self.musica_onn,
                                       onclick_param=""
                                       )

        self.Musica_off = Button_Image(screen=self._slave,
                                       master_x=x,
                                       master_y=y,
                                       x=w/4,
                                       y=h/ 2,
                                       w=w / 10,
                                       h=h / 10,
                                       path_image="Recursos\sonidoOff.png",
                                       onclick=self.musica_off,
                                       onclick_param=""
                                       )


        font = py.font.Font(None, 45)  # You can adjust the font size as needed
        textoa = f" Volumen Musica" 
        self.Texto1 = font.render(textoa, True, ("white"))  # Assuming white text color


        font = py.font.Font(None, 45)  # You can adjust the font size as needed
        textob = f" Volumen efectos" 
        self.Texto2 = font.render(textob, True, ("white"))  # Assuming white text color


    def musica_onn(self, parametro):
        with open("datos_volumen.json", "r") as nivel2_file:
            content = json.load(nivel2_file)
            content["bandera"] = self.bandera
            self.bandera = False
            content["volumen_efectos"] = 100 if self.bandera else 0  # Set volumen_efectos based on bandera value

        with open("datos_volumen.json", "w") as nivel2_file:
            json.dump(content, nivel2_file)

    def musica_off(self, parametro):
        with open("datos_volumen.json", "r") as nivel2_file:
            content = json.load(nivel2_file)
            content["bandera"] = self.bandera
            self.bandera = True
            content["volumen_efectos"] = 100 if self.bandera else 0  # Set volumen_efectos based on bandera value

        with open("datos_volumen.json", "w") as nivel2_file:
            json.dump(content, nivel2_file)


    def btn_home_click(self, parametro):
        with open("datos_volumen.json", "r") as nivel2_file:
            content = json.load(nivel2_file)

        # Modify the content
        content["pausa"] = False
    
        # Open the file in write mode and dump the modified content
        with open("datos_volumen.json", "w") as nivel2_file:
            json.dump(content, nivel2_file)

        self.end_dialog()

    def update(self, lista_eventos):
        

        self._slave.blit(self.Texto1, (W/2, H/6)) 
        self._slave.blit(self.Texto2, (W/2.5, H/2)) 

        self.slider_volumen_musica.value = self.volumen_musica

        with open("datos_volumen.json", "r") as nivel2_file:
            content = json.load(nivel2_file)
            self.bandera = content.get("bandera", True)

            if self.bandera == False:  # If bandera is False, add Musica_off to the widget list
                self.lista_widgets.append(self.Musica_off)
            elif self.bandera == True:  # If bandera is True, add Musica_on to the widget list
                self.lista_widgets.append(self.Musica_on)

        if self.verificar_dialog_result():
            if self.active:
                self.draw()
                self.render()
                for widget in self.lista_widgets:
                    widget.update(lista_eventos)
                        
                self.update_volumen(lista_eventos)
        else:
            self.hijo.update(lista_eventos)

    def update_volumen(self, lista_eventos):
        self._slave.blit(self.aux_image, (0, 0))  # Blit the background image

        self.volumen_musica = self.slider_volumen_musica.value
        self.label_volumen_musica.update(lista_eventos)
        porcentaje_volumen_musica = f"{self.volumen_musica * 100:.2f}%"  # Update the label with two decimal places
        self.label_volumen_musica.set_text(porcentaje_volumen_musica)
        pygame.mixer.music.set_volume(self.volumen_musica)

        self.lista_widgets.append(self.slider_volumen_musica)
        self.lista_widgets.append(self.boton_exit)

        


        for widget in self.lista_widgets:
            widget.update(lista_eventos)


        with open("datos_volumen.json", "r") as nivel2_file:
            content = json.load(nivel2_file)

        # Update specific fields
            content["volumen_musica"] = self.volumen_musica

            # Write the updated content back to the JSON file
            with open("datos_volumen.json", "w") as nivel2_file:
                json.dump(content, nivel2_file)

            for widget in self.lista_widgets:
                widget.update(lista_eventos)

            # Render the changes
            self.render()