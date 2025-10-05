import pygame
from src.utils.constantes import *
from src.entities.mario import Mario
from src.core.nivel import Nivel
from src.core.camara import Camara

class Juego:
    def __init__(self, pantalla, reloj):
        self.pantalla = pantalla
        self.reloj = reloj
        self.mario = Mario(50, 400)
        # ...resto de la inicialización...

    def ejecutar(self):
        # ...código existente...
        pass
