import pygame
from pygame.locals import *
from niveles.nivel_uno import *
from niveles.nivel_base import*
from UI.GUI_button_image import *
from UI.GUI_form import *
from UI.GUI_label import *
from manejador_niveles import*
from UI.GUI_form_contenedor_de_niveles import *
from UI.GUI_form_guardar_record import *
import pygame as py
import sys
import os
from UI.GUI_form_game_over import *
from UI.GUI_form_EntreNiveles import*
from UI.GUI_form_opciones import *

class FormNiveles(Form):
    def __init__(self, screen, x, y, w, h, color_background, color_border, active,path_image):
        super().__init__(screen, x,y,w,h,color_background,color_border,active)

        self._slave.fill((0, 0, 0))


        if os.path.exists("datos_jugador.json") :
            with open("datos_jugador.json", "r+") as json_file:
                    datos_jugador = json.load(json_file)

                    if datos_jugador.get("nivel completado", 0) == 1:
                        datos_jugador["nivel completado"] = 0
                    
                    json_file.seek(0)   
                    json.dump(datos_jugador, json_file, indent=2)
                    json_file.truncate()


        if not os.path.exists("datos_niveles.json"):
            self.nivel1=0
            self.nivel2=0
            self.nivel3=0        
            self.Record_Final = 0

        else:
            with open("datos_niveles.json") as json_file:
                datos_niveles = json.load(json_file)

                self.nivel1=datos_niveles["nivel1"]
                self.nivel2=datos_niveles["nivel2"]
                self.nivel3=datos_niveles["nivel3"]
        self.gameOver=0
        
        self.Medio1 = 0

        self.Record_Nivel1 =0

        self.Record_Nivel2 =0
        
        self.Record_Nivel3 =0

        self.manejador_de_niveles = ManejadorNiveles(self._master)
        self.lista_widgets = []
        aux_image = pygame.image.load(path_image)
        aux_image = pygame.transform.scale(aux_image,(w,h))
        self._slave = aux_image

        self.lvl1 = Button_Image(screen = self._slave,
                                       master_x = x,
                                       master_y = y, 
                                       x = w/2-w /3 ,
                                       y =  h/3,
                                       w= w/10,
                                       h = h/10,
                                       path_image = "Recursos\level1.png",
                                       onclick = self.entrar_nivel,
                                       onclick_param= "nivel_uno",
        
                                       )
        self.lvl2 = Button_Image(screen = self._slave,
                                       master_x = x,
                                       master_y = y, 
                                       x =  w /2 ,
                                       y =h /3,
                                       w= w/10,
                                       h = h/10,
                                       path_image = "Recursos\level2.png",
                                       onclick = self.entrar_nivel,
                                       onclick_param= "nivel_dos"
                                       )
        
        self.lvl3 = Button_Image(screen = self._slave,
                                       master_x = x,
                                       master_y = y, 
                                       x = w/2+ w/3,
                                       y = h/3,
                                       w= w/10,
                                       h = h/10,
                                       path_image = "Recursos\level3.png",
                                       onclick = self.entrar_nivel,
                                       onclick_param= "nivel_tres"

                                       )
                
        self.back = Button_Image(screen = self._slave,
                                       master_x = x,
                                       master_y = y, 
                                       x = w /7 ,
                                       y = h-h /6,
                                       w= w/10,
                                       h = h/10,
                                       path_image = "Recursos\eatras.png",
                                       onclick = self.btn_home_click,
                                       onclick_param= ""

                                       )

        self.formEntre1 = EntreNiveles(screen = self._master,
                                                x = 0,
                                                y = 0,
                                                w = 1200,
                                                h = 700,
                                                color_background = "green",
                                                color_border = "blue",
                                                active = True,
                                                path_image = "Recursos\puntajes.png", 
                                                )

        self.back = Button_Image(screen = self._slave,
                                       master_x = x,
                                       master_y = y, 
                                       x = W/10 ,
                                       y = h-h /6,
                                       w= w/10,
                                       h = h/10,
                                       path_image = "Recursos\eatras.png",
                                       onclick = self.btn_home_click,
                                       onclick_param= ""

                                       )

        self.records= Button_Image(screen = self._slave,
                                       master_x = x,
                                       master_y = y, 
                                       x = W-W/10 ,
                                       y = h-h /6,
                                       w= w/10,
                                       h = h/10,
                                       path_image = "Recursos\erecord.png",
                                       onclick = self.guardar_record,
                                       onclick_param= ""

                                       )

        self.lista_widgets.append(self.lvl1)
        self.lista_widgets.append(self.back)
        
    def entrar_nivel(self,nombre_nivel):
        nivel = self.manejador_de_niveles.get_level(nombre_nivel)
        frm_contenedor_nivel = FormContenedorDeNivel(self._master,nivel)

        self.show_dialog(frm_contenedor_nivel)


    

    def guardar_record(self, parametro):
        frm_guardar_record = records(
            screen=self._master,
            x=W/3,
            y=H /3,
            w=W/ 3,
            h=H / 3,
            color_background="green",
            color_border="blue",
            active=True,
            path_image="Recursos\\ui5.png"
        )
        self.show_dialog(frm_guardar_record)


    def btn_home_click(self,parametro):
        self.end_dialog()

                    

    def guardar_datos_niveles(self):
        

        datos_niveles = {"nivel1": self.nivel1,"recordlvl1": self.Record_Nivel1,"nivel2": self.nivel2,"recordlvl2": self.Record_Nivel2,"nivel3": self.nivel3, "recordlvl3": self.Record_Nivel3, "game_over": self.gameOver, "medio": self.Medio1,"record final": self.Record_Final}
        with open("datos_niveles.json", "w") as json_file:
            json.dump(datos_niveles, json_file)


    def manejar_niveles(self):
            font = py.font.Font(None, 45)  # You can adjust the font size as needed
            if self.nivel1 == 1:
                with open("datos_nivel1.json", "r") as nivel1_file:
                    content = json.load(nivel1_file)
                    nivel1_puntaje = content.get("Puntaje Nivel", 0)
                    
                    if nivel1_puntaje > self.Record_Nivel1:
                        self.Record_Nivel1 = nivel1_puntaje
                        print(f"Updated Record_Nivel1: {self.Record_Nivel1}")
                Record = str(self.Record_Nivel1)
                Record_texto = f" Record lvl1 : {Record}" 
                self.record1 = font.render(Record_texto, True, ("white"))  # Assuming white text color

            if self.nivel2 == 1:
                with open("datos_nivel2.json", "r") as nivel2_file:
                    content = json.load(nivel2_file)
                    nivel2_puntaje = content.get("Puntaje Nivel", 0)
                    
                    if nivel2_puntaje > self.Record_Nivel2:
                        self.Record_Nivel2 = nivel2_puntaje

                Record2 = str(self.Record_Nivel2)
                Record2_texto = f" Record lvl2 : {Record2}" 
                self.record2 = font.render(Record2_texto, True, ("white"))  # Assuming white text color

            if self.nivel3 == 1:

                with open("datos_nivel3.json", "r") as nivel3_file:
                    content = json.load(nivel3_file)
                    nivel3_puntaje = content.get("Puntaje Nivel", 0)
                    
                    if nivel3_puntaje > self.Record_Nivel3:
                        self.Record_Nivel3 = nivel3_puntaje

                Record3 = str(self.Record_Nivel3)
                Record3_texto = f" Record lvl3 : {Record3}" 
                self.record3 = font.render(Record3_texto, True, ("white"))  # Assuming white text color

                Record4 = str(self.Record_Final)
                Record4_texto = f" Record Final: {Record4}" 
                self.record4 = font.render(Record4_texto, True, ("white"))  # Assuming white text color


    
    def cargar_datos_jugador(self):
        with open("datos_jugador.json", "r") as json_file:
            datos_jugador = json.load(json_file)
            if datos_jugador["nivel completado"] == 1:

                if datos_jugador["nivel actual"] == "niveles.uno":
                    self.nivel1 = 1

                    with open("datos_nivel1.json", "w+") as nivel1_file:
                        json.dump(datos_jugador, nivel1_file)

                elif datos_jugador["nivel actual"] == "niveles.dos":
                    self.nivel1 = self.nivel2 = 1
                    self.Medio1 = 1

                    with open("datos_nivel2.json", "w+") as nivel2_file:
                        json.dump(datos_jugador, nivel2_file)

                elif datos_jugador["nivel actual"] == "niveles.tres":
                    self.nivel1 = self.nivel2 = self.nivel3 = 1

                    self.Medio1 = 1
                    with open("datos_nivel3.json", "w+") as nivel3_file:
                        json.dump(datos_jugador, nivel3_file)
                self.Medio1 = 1

            else:
                self.Medio1 = 0
                
            if datos_jugador["muerto"] == 1:
                self.gameOver = 1

    def update(self, lista_eventos):
        self.Record_Final = self.Record_Nivel1 +self.Record_Nivel2 + self.Record_Nivel3


        if os.path.exists("datos_jugador.json"):
            self.cargar_datos_jugador()


        self.guardar_datos_niveles()
        self.manejar_niveles()
        if self.nivel1 == 1:
            self.lista_widgets.append(self.lvl2)
            
            self._slave.blit(self.record1, (W/10, H/2)) 


        if self.nivel2 == 1:
            self.lista_widgets.append(self.lvl3)
            self._slave.blit(self.record2, (W/2-W/10, H/2)) 


        
        if self.nivel3 == 1:
            self._slave.blit(self.record3, (W/2+ W/6, H/2)) 
            self._slave.blit(self.record4, (W/4, H-H/6))
            self.lista_widgets.append(self.records)


        if self.gameOver==1:
                        
            self.formGameOver = FormGameOVer(screen = self._master,
                                                    x = 0,
                                                    y = 0,
                                                    w = 1200,
                                                    h = 700,
                                                    color_background = "green",
                                                    color_border = "blue",
                                                    active = True,
                                                    path_image = "Recursos\game_over.png", 
                                                    )
        
          


        if self.verificar_dialog_result():
            if self.active:
                self.draw()
                self.render()
                if self.Medio1 == 1:
                    self.show_dialog(self.formEntre1)

                if self.gameOver == 1:
                    self.show_dialog(self.formGameOver)#modal se llama buscar
                    self.gameOver = 0

                for widget in self.lista_widgets:
                    widget.update(lista_eventos)
        else:
            self.hijo.update(lista_eventos)