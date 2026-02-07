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
from UI.GUI_form_game_over import *
from UI.GUI_form_guardar_record import*
from data_manager import dm

class EntreNiveles(Form):
    def __init__(self, screen, x, y, w, h, color_background, color_border, active,path_image):
        super().__init__(screen, x,y,w,h,color_background,color_border,active)
        py.mixer.stop() 
        
        self.nivel1=0
        self.nivel2=0
        self.nivel3=0

    
        self.gameOver=0
        
        self.Puntaje_Nivel1=0
        self.Puntaje_Nivel2=0
        self.Puntaje_Nivel3=0

        self.manejador_de_niveles = ManejadorNiveles(self._master)
        self.lista_widgets = []
        
        self.aux_image = pygame.image.load(path_image)
        self.aux_image = pygame.transform.scale(self.aux_image,(w,h))
        





        self.back = Button_Image(screen = self._slave,
                                       master_x = x,
                                       master_y = y, 
                                       x = w /6 ,
                                       y = h-h /6,
                                       w= w/10,
                                       h = h/10,
                                       path_image = "Recursos/eatras.png",
                                       onclick = self.btn_home_click,
                                       onclick_param= ""
                                       )
        self.lvl2 = Button_Image(screen = self._slave,
                                       master_x = x,
                                       master_y = y, 
                                       x = w/2+ w/3,
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
        self._slave.fill((0, 0, 0))
        self.lista_widgets.append(self.back)

    def guardar_record(self, parametro):
        frm_guardar_record = records(
            screen=self._master,
            x=0,
            y=0,
            w=W/ 2,
            h=H / 2,
            color_background="green",
            color_border="blue",
            active=True,
            path_image="Recursos/ui5.png"
        )
        self.show_dialog(frm_guardar_record)

    def entrar_nivel(self,nombre_nivel):
        nivel = self.manejador_de_niveles.get_level(nombre_nivel)
        frm_contenedor_nivel = FormContenedorDeNivel(self._master,nivel)

        self.show_dialog(frm_contenedor_nivel)

    def btn_home_click(self, parametro):
        if dm.niveles.get("medio", 0) == 1:
            dm.niveles["medio"] = 0
        dm.save_niveles()
        self.end_dialog()


    def cargar_datos_jugador(self):
        nivel_actual = dm.jugador.get("nivel actual", "")
        if nivel_actual == "niveles.uno":
            self.lista_widgets.append(self.lvl2)
        elif nivel_actual == "niveles.dos":
            self.lista_widgets.clear()
            self.lista_widgets.append(self.lvl3)
            self.lista_widgets.append(self.back)
        elif nivel_actual == "niveles.tres":
            self.lista_widgets.clear()
            self.lista_widgets.append(self.back)

        if dm.jugador.get("muerto", 0) == 1:
            self.gameOver = 1


    
    
    def ui(self):
         
        widget_surface = pygame.Surface((W, H))
        widget_surface.fill((0, 0, 0))  # Fill background color

        # Draw widgets on the widget surface
        for widget in self.lista_widgets:
            widget.draw()
            widget.render()

    # Draw the background image on the main surface
        self._slave.blit(self.aux_image, (0, 0))
         
        posicion_inicial = (W/10 , H/2)
        posicion_final = (W/2,  H/2)
        py.draw.line(self._slave, "White", posicion_inicial, posicion_final, 2)

        datos_jugador = dm.jugador

        font = py.font.Font(None, 45)

        puntaje = str(datos_jugador.get("puntaje", 0))
        muertes_texto = f"Puntaje Inicial: {puntaje}            x 1"
        text_surface1 = font.render(muertes_texto, True, ("white"))
        self._slave.blit(text_surface1, (W/8, H/16))

        vidas = str(datos_jugador.get("vida", 0))
        vidas_texto = f" Vidas: {vidas}                 x 100 "
        text_surface1 = font.render(vidas_texto, True, ("white"))
        self._slave.blit(text_surface1, (W/8, H/8))

        tiempo = str(datos_jugador.get("Tiempo", 0))
        tiempo_texto = f"+    Tiempo: {tiempo}                 x 1"
        text_surface1 = font.render(tiempo_texto, True, ("white"))
        self._slave.blit(text_surface1, (W/10, H/5))

        muertes = str(datos_jugador.get("Muertes", 0))
        muertes_texto = f"Muertes: {muertes}                 x- 100"
        text_surface1 = font.render(muertes_texto, True, ("white"))
        self._slave.blit(text_surface1, (W/8, H/3))

        salud = str(datos_jugador.get("salud", 0))
        salud_texto = f"Salud: {salud}%                 x 10  "
        text_surface = font.render(salud_texto, True, ("white"))
        self._slave.blit(text_surface, (W/8, H/2.5))

        PuntajeFinal = str(datos_jugador.get("Puntaje Nivel", 0))
        PuntajeFinal_texto = f"Puntaje Final     {PuntajeFinal}"
        text_surface = font.render(PuntajeFinal_texto, True, ("white"))
        self._slave.blit(text_surface, (W/8, H/2+H/5))

        

    def update(self, lista_eventos):
        py.display.update()

        self.cargar_datos_jugador()
        self.ui()

        if self.verificar_dialog_result():
            if self.active:
                for widget in self.lista_widgets:
                    widget.update(lista_eventos)  # POLIMORFISMO (CADA WIDGET SE ACTUALIZA DE MANERA DIFERENTE)
                    widget.draw()

                self.draw()
                self.render()
        else:
            self.hijo.update(lista_eventos)



