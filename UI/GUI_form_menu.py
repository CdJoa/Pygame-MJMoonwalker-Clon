import pygame
from pygame.locals import *
import os
from UI.GUI_button_image import *
from UI.GUI_form import *
from UI.GUI_label import *
from UI.GUI_form_niveles import*
from UI.GUI_form_menu_score import*
from UI.GUI_textbox import*
from UI.GUI_form_opciones import *

import pygame as py
import sys
import sqlite3 as sql


class FormMenu(Form):
    def __init__(self, screen, x, y, w, h, color_background, color_border, active, path_image):
        super().__init__(screen, x,y,w,h,color_background,color_border,active)
        aux_image = pygame.image.load(path_image)
        aux_image = pygame.transform.scale(aux_image,(w,h))
        self._slave = aux_image
        self.lista_widgets = []
        self.volumen_musica = 1
        self.volumen_efectos = 100
        self.bandera= True
        self.pausa = False
        if not os.path.exists("leaderboard1.db"):
            self.crear_base_de_datos()

        datos = {"volumen_musica": self.volumen_musica,"volumen_efectos": self.volumen_efectos,"bandera":self.bandera,"pausa":self.pausa}

        if not os.path.exists("volumen.json") :
            with open("datos_volumen.json", "w") as json_file:
                json.dump(datos, json_file)




        py.mixer.init()
        self.sonido_nivel = py.mixer.Sound("Recursos\Bad.mp3")
        self.sonido_nivel.play()
   

        self.boton_opciones = Button_Image(screen = self._slave,
                                       master_x = x,
                                       master_y = y, 
                                       x = w/2.2 ,
                                       y =  h- h /3,
                                       w= w/10,
                                       h = h/10,
                                       path_image = "Recursos\opciones.png",
                                       onclick = self.menu_opciones,
                                       onclick_param= ""
                                       )
        self.boton_jugar = Button_Image(screen = self._slave,
                                       master_x = x,
                                       master_y = y, 
                                       x =  w/2.2 ,
                                       y =h /2,
                                       w= w/10,
                                       h = h/10,
                                       path_image = "Recursos\jugar.png",
                                       onclick = self.btn_niveles_click,
                                       onclick_param= ""
                                       )
        
        self.boton_exit = Button_Image(screen = self._slave,
                                       master_x = x,
                                       master_y = y, 
                                       x = w- w /8 ,
                                       y = h-h /6,
                                       w= w/10,
                                       h = h/10,
                                       path_image = "Recursos\exit.png",
                                       onclick = self.btn_home_click,
                                       onclick_param= ""

                                       )
        
                
        self.boton_record = Button_Image(screen = self._slave,
                                       master_x = x,
                                       master_y = y, 
                                       x = w /8 ,
                                       y = h-h /6,
                                       w= w/10,
                                       h = h/10,
                                       path_image = "Recursos\erecord.png",
                                       onclick = self.btn_tabla_click,
                                       onclick_param= ""

                                       )
        self.lista_widgets.append(self.boton_jugar)
        self.lista_widgets.append(self.boton_exit)
        self.lista_widgets.append(self.boton_opciones)
        self.lista_widgets.append(self.boton_record)
    def btn_home_click(self,parametro):
        self.end_dialog()
        py.quit()
        sys.exit()

    
    def btn_niveles_click(self,parametro):
            formNiveles = FormNiveles(screen = self._master,
                                x = 0,
                                y = 0,
                                w = 1200,
                                h = 700,
                                color_background = "green",
                                color_border = "blue",
                                active = True,
                                path_image = "Recursos\pantalla_niveles.png",
 )
            self.show_dialog(formNiveles)#modal se llama buscar


    def crear_base_de_datos(self):
        with sql.connect("leaderboard1.db") as conexion:
            try:
                sentencia = '''
                            CREATE TABLE mi_tabla (
                                score INTEGER PRIMARY KEY,
                                nombre TEXT
                            );
                            '''
                conexion.execute(sentencia)

                # Ahora puedes insertar datos con valores enteros
                conexion.execute("INSERT INTO mi_tabla (score, nombre) VALUES (?, ?)", (123, "joaquin"))
                conexion.execute("INSERT INTO mi_tabla (score, nombre) VALUES (?, ?)", (333, "jean"))
                conexion.execute("INSERT INTO mi_tabla (score, nombre) VALUES (?, ?)", (555, "michael"))
                conexion.execute("INSERT INTO mi_tabla (score, nombre) VALUES (?, ?)", (14456, "billie"))

                print("bien")
            except Exception as e:
                print("error:", e)


    def btn_tabla_click(self, param):
        datos = []  
           
        with sql.connect("leaderboard1.db") as conexion:
                cursor = conexion.cursor()
                cursor.execute("SELECT score, nombre FROM mi_tabla")
                filas = cursor.fetchall()

                for fila in filas:
                    score, nombre = fila
                    datos.append({"score": score, "nombre": nombre})

        datos.sort(key=lambda x: x["score"], reverse=True)
        if len(datos) >= 5:
            del datos[4]

            
        nuevo_form = FormMenuScore(
                screen=self._master,
                x=0,
                y=0,
                w=W,
                h=H,
                color_background="green",
                color_border="gold",
                active=True,
                path_image="Recursos\Window.png",
                scoreboard=datos,
                margen_x=10,
                margen_y=100,
                espacio=10
            )


        self.show_dialog(nuevo_form)


    def menu_opciones(self, parametro):
        opciones = menu_opciones(
            screen=self._master,
            x=0,
            y=0,
            w=W,
            h=H,
            color_background="green",
            color_border="blue",
            active=True,
            path_image="Recursos\\test1.jpg"
        )
        self.show_dialog(opciones)


    def update(self, lista_eventos):
        if self.verificar_dialog_result():
            if self.active:
                self.draw()
                self.render()
                for widget in self.lista_widgets:
                    widget.update(lista_eventos)
                # Read the volumen value from the JSON file
                with open("datos_volumen.json", "r") as nivel2_file:
                    content = json.load(nivel2_file)
                    self.volumen_musica = content.get("volumen_musica", 0)
                self.sonido_nivel.set_volume(self.volumen_musica)
        else:
            self.hijo.update(lista_eventos)





