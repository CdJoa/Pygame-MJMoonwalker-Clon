import pygame
from pygame.locals import *
import os
from UI.GUI_button_image import *
from UI.GUI_form import *
from UI.GUI_label import *
from UI.GUI_form_niveles import *
from UI.GUI_form_menu_score import *
from UI.GUI_textbox import *
import pygame as py
import sys
import sqlite3 as sql
import csv
import pandas as pd
import json

class records(Form):
    def __init__(self, screen, x, y, w, h, color_background, color_border, active, path_image):
        super().__init__(screen, x, y, w, h, color_background, color_border, active)
        aux_image = pygame.image.load(path_image)
        aux_image = pygame.transform.scale(aux_image, (w, h))
        self._slave = aux_image

        self.Record_Final = 0

        self.txt_nombre = TextBox(self._slave, x, y,
                                  50, 50, 150, 30,
                                  "gray", "white", "red", "blue", 2,
                                  "Comic Sans Ms", 15, "black")

        self.contenido = (self.txt_nombre._text)

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

        self.boton_guardar = Button_Image(screen=self._slave,
                                          master_x=x,
                                          master_y=y,
                                          x=w / 8,
                                          y=h - h / 6,
                                          w=w / 10,
                                          h=h / 10,
                                          path_image="Recursos\disket.png",
                                          onclick=self.btn_guardar_click,
                                          onclick_param=""
                                          )
        
        self.lista_widgets.append(self.txt_nombre)
        self.lista_widgets.append(self.boton_exit)

    def btn_home_click(self, parametro):
        self.end_dialog()


    def btn_guardar_click(self, parametro):
        if os.path.exists("datos_niveles.json"):
            with open("datos_niveles.json", "r") as json_file:
                datos_niveles = json.load(json_file)
                self.Record_Final = datos_niveles.get("record final", "0")

        self.nombre_jugador = self.txt_nombre._text

        with sql.connect("leaderboard1.db") as conexion:
            cursor = conexion.cursor()

            cursor.execute("UPDATE mi_tabla SET nombre = ? WHERE score = ?", (self.nombre_jugador, int(self.Record_Final)))

            if cursor.rowcount == 0:
                cursor.execute("INSERT INTO mi_tabla (score, nombre) VALUES (?, ?)", (int(self.Record_Final), self.nombre_jugador))

            conexion.commit()

        self.end_dialog()




    def update(self, lista_eventos):


        self.lista_widgets.append(self.boton_guardar)

        if self.verificar_dialog_result():
            if self.active:
                self.draw()
                self.render()
                for widget in self.lista_widgets:
                    widget.update(lista_eventos)  # POLIMORFISMO (CADA WIDGET SE ACTUALIZA DE MANERA DIFERENTE)
        else:
            self.hijo.update(lista_eventos)
