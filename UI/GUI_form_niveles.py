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
from UI.GUI_form_game_over import *
from UI.GUI_form_EntreNiveles import*
from UI.GUI_form_opciones import *
from data_manager import dm

class FormNiveles(Form):
    def __init__(self, screen, x, y, w, h, color_background, color_border, active,path_image):
        super().__init__(screen, x,y,w,h,color_background,color_border,active)

        self._slave.fill((0, 0, 0))


        if dm.jugador.get("nivel completado", 0) == 1:
            dm.jugador["nivel completado"] = 0
            dm.save_jugador()

        self.nivel1 = dm.niveles.get("nivel1", 0)
        self.nivel2 = dm.niveles.get("nivel2", 0)
        self.nivel3 = dm.niveles.get("nivel3", 0)
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
                                       path_image = "Recursos/level1.png",
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
                                       path_image = "Recursos/level2.png",
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
                                       path_image = "Recursos/level3.png",
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
                                       path_image = "Recursos/eatras.png",
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
                                                path_image = "Recursos/puntajes.png", 
                                                )

        self.back = Button_Image(screen = self._slave,
                                       master_x = x,
                                       master_y = y, 
                                       x = W/10 ,
                                       y = h-h /6,
                                       w= w/10,
                                       h = h/10,
                                       path_image = "Recursos/eatras.png",
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
                                       path_image = "Recursos/erecord.png",
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
            path_image="Recursos/ui5.png"
        )
        self.show_dialog(frm_guardar_record)


    def btn_home_click(self,parametro):
        self.end_dialog()

                    

    def guardar_datos_niveles(self):
        dm.niveles["nivel1"] = self.nivel1
        dm.niveles["recordlvl1"] = self.Record_Nivel1
        dm.niveles["nivel2"] = self.nivel2
        dm.niveles["recordlvl2"] = self.Record_Nivel2
        dm.niveles["nivel3"] = self.nivel3
        dm.niveles["recordlvl3"] = self.Record_Nivel3
        dm.niveles["game_over"] = self.gameOver
        dm.niveles["medio"] = self.Medio1
        dm.niveles["record final"] = self.Record_Final
        dm.save_niveles()


    def manejar_niveles(self):
            font = py.font.Font(None, 45)
            if self.nivel1 == 1:
                nivel1_puntaje = dm.nivel1.get("Puntaje Nivel", 0)
                if nivel1_puntaje > self.Record_Nivel1:
                    self.Record_Nivel1 = nivel1_puntaje
                Record = str(self.Record_Nivel1)
                Record_texto = f" Record lvl1 : {Record}"
                self.record1 = font.render(Record_texto, True, ("white"))

            if self.nivel2 == 1:
                nivel2_puntaje = dm.nivel2.get("Puntaje Nivel", 0)
                if nivel2_puntaje > self.Record_Nivel2:
                    self.Record_Nivel2 = nivel2_puntaje
                Record2 = str(self.Record_Nivel2)
                Record2_texto = f" Record lvl2 : {Record2}"
                self.record2 = font.render(Record2_texto, True, ("white"))

            if self.nivel3 == 1:
                nivel3_puntaje = dm.nivel3.get("Puntaje Nivel", 0)
                if nivel3_puntaje > self.Record_Nivel3:
                    self.Record_Nivel3 = nivel3_puntaje
                Record3 = str(self.Record_Nivel3)
                Record3_texto = f" Record lvl3 : {Record3}"
                self.record3 = font.render(Record3_texto, True, ("white"))

                Record4 = str(self.Record_Final)
                Record4_texto = f" Record Final: {Record4}"
                self.record4 = font.render(Record4_texto, True, ("white"))


    
    def cargar_datos_jugador(self):
        datos = dm.jugador
        if datos.get("nivel completado", 0) == 1:
            if datos.get("nivel actual") == "niveles.uno":
                self.nivel1 = 1
                dm.nivel1 = dict(datos)
                dm.save_nivel1()
            elif datos.get("nivel actual") == "niveles.dos":
                self.nivel1 = self.nivel2 = 1
                self.Medio1 = 1
                dm.nivel2 = dict(datos)
                dm.save_nivel2()
            elif datos.get("nivel actual") == "niveles.tres":
                self.nivel1 = self.nivel2 = self.nivel3 = 1
                self.Medio1 = 1
                dm.nivel3 = dict(datos)
                dm.save_nivel3()
            self.Medio1 = 1
        else:
            self.Medio1 = 0

        if datos.get("muerto", 0) == 1:
            self.gameOver = 1

    def update(self, lista_eventos):
        self.Record_Final = self.Record_Nivel1 +self.Record_Nivel2 + self.Record_Nivel3


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
                                                    path_image = "Recursos/game_over.png", 
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