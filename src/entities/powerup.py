import pygame
from src.utils.constantes import *

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo='hongo'):
        super().__init__()
        self.tipo = tipo
        self.rect = pygame.Rect(x, y, 24, 24)
        self.velocidad_x = 2
        self.velocidad_y = 0
        self.activo = False

    # ...resto del código de PowerUp...
