import pygame
from pygame.locals import *
from niveles.nivel_uno import *
from niveles.nivel_base import*
from UI.GUI_button_image import *
from UI.GUI_form import *
from UI.GUI_label import *
from manejador_niveles import*
from UI.GUI_form_contenedor_de_niveles import *
import pygame as py
from data_manager import dm


class FormGameOVer(Form):
    def __init__(self, screen, x, y, w, h, color_background, color_border, active,path_image):
        super().__init__(screen, x,y,w,h,color_background,color_border,active)


        
        aux_image = pygame.image.load(path_image)
        aux_image = pygame.transform.scale(aux_image,(w,h))
        self._slave = aux_image
        self.lista_widgets = []

        
                
        self.back = Button_Image(screen = self._slave,
                                       master_x = x,
                                       master_y = y, 
                                       x = w /2 ,
                                       y = h-h /6,
                                       w= w/10,
                                       h = h/10,
                                       path_image = "Recursos/eatras.png",
                                       onclick = self.btn_home_click,
                                       onclick_param= ""
                                       )


        self.lista_widgets.append(self.back)


    def btn_home_click(self, parametro):
        dm.reset_jugador()
        dm.reset_niveles()
        self.end_dialog()

    

    def update(self, lista_eventos):
        if self.verificar_dialog_result():
            for widget in self.lista_widgets:
                widget.update(lista_eventos)



        self.draw()
