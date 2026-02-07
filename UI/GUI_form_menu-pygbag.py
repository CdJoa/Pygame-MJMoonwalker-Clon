import pygame
from pygame.locals import *
from UI.GUI_button_image import *
from UI.GUI_form import *
from UI.GUI_label import *
from UI.GUI_form_niveles import*
from UI.GUI_form_menu_score import*
from UI.GUI_textbox import*
from UI.GUI_form_opciones import *

import pygame as py
from data_manager import dm


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
        dm.save_volumen()
        dm.leaderboard_seed([
            (123, "joaquin"), (333, "jean"),
            (555, "michael"), (14456, "billie"),
        ])




        py.mixer.init()
        self.sonido_nivel = py.mixer.Sound("Recursos/Bad.ogg")
        self.sonido_nivel.play()
   

        self.boton_opciones = Button_Image(screen = self._slave,
                                       master_x = x,
                                       master_y = y, 
                                       x = w/2.2 ,
                                       y =  h- h /3,
                                       w= w/10,
                                       h = h/10,
                                       path_image = "Recursos/opciones.png",
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
                                       path_image = "Recursos/jugar.png",
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
                                       path_image = "Recursos/exit.png",
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
                                       path_image = "Recursos/erecord.png",
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

    
    def btn_niveles_click(self,parametro):
            formNiveles = FormNiveles(screen = self._master,
                                x = 0,
                                y = 0,
                                w = 1200,
                                h = 700,
                                color_background = "green",
                                color_border = "blue",
                                active = True,
                                path_image = "Recursos/pantalla_niveles.png",
 )
            self.show_dialog(formNiveles)#modal se llama buscar


    def btn_tabla_click(self, param):
        datos = dm.leaderboard_get_top(4)

            
        nuevo_form = FormMenuScore(
                screen=self._master,
                x=0,
                y=0,
                w=W,
                h=H,
                color_background="green",
                color_border="gold",
                active=True,
                path_image="Recursos/Window.png",
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
            path_image="Recursos/test1.jpg"
        )
        self.show_dialog(opciones)


    def update(self, lista_eventos):
        if self.verificar_dialog_result():
            if self.active:
                self.draw()
                self.render()
                for widget in self.lista_widgets:
                    widget.update(lista_eventos)
                self.volumen_musica = dm.volumen.get("volumen_musica", 0)
                self.sonido_nivel.set_volume(self.volumen_musica)
        else:
            self.hijo.update(lista_eventos)





