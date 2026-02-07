import pygame as py
from pygame.locals import *
from UI.GUI_form import *
from UI.GUI_button import *
from data_manager import dm
import re

class FormContenedorDeNivel(Form):
    def __init__(self, pantalla:py.Surface,nivel):
        super().__init__(pantalla,0,0,pantalla.get_width(),pantalla.get_height(),"blue")
        nivel._slave = self._slave
        self.nivel = nivel

    def leer_datos_jugador(self):
        return dm.jugador

    def update(self, lista_eventos):
        self.nivel.update(lista_eventos)
        self.draw()
        datos_jugador = self.leer_datos_jugador()

        nivel_completado = datos_jugador.get("nivel completado", 0)
        game_over = datos_jugador.get("muerto", 0)

        if nivel_completado == 1 or game_over == 1:
            dm.save_jugador()
            self.end_dialog()

        nivel_nombre = re.sub(r'Nivel', '', self.nivel.__class__.__name__, flags=re.IGNORECASE).lower()
        self.nivel_actual = f"niveles.{nivel_nombre}"
        dm.jugador["nivel actual"] = self.nivel_actual

        if self.verificar_dialog_result():
            for widget in self.lista_widgets:
                widget.update(lista_eventos)
                self.draw()
        else:
            self.hijo.update(lista_eventos)