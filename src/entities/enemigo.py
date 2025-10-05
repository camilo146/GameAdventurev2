import pygame
from src.utils.constantes import *

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo='goomba'):
        super().__init__()
        self.tipo = tipo
        self.ancho = 30 if tipo == 'goomba' else 32
        self.alto = 30 if tipo == 'goomba' else 40
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)
        self.velocidad_x = -2 if tipo == 'goomba' else -1
        self.vivo = True
        self.aplastado = False
        self.animacion_frame = 0
        self.animacion_contador = 0

    # ...resto del código de Enemigo...
