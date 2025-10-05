import pygame
from typing import Literal
from src.utils.constantes import VERDE, MARRON, NARANJA, VERDE_TUBO

class Plataforma(pygame.sprite.Sprite):
    """Clase que representa las plataformas del juego."""
    
    def __init__(self, x: int, y: int, ancho: int, alto: int, 
                 tipo: Literal['normal', 'suelo', 'bloque', 'tubo'] = 'normal'):
        super().__init__()
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.tipo = tipo
        self.golpeado = False
        
    def dibujar(self, superficie: pygame.Surface) -> None:
        """Dibuja la plataforma según su tipo."""
        if self.tipo == 'suelo':
            pygame.draw.rect(superficie, VERDE, self.rect)
            pygame.draw.rect(superficie, MARRON, 
                           (self.rect.x, self.rect.y + 10, self.rect.width, self.rect.height - 10))
        elif self.tipo == 'bloque':
            color = NARANJA if not self.golpeado else (150, 150, 150)
            pygame.draw.rect(superficie, color, self.rect)
            for i in range(0, self.rect.width, 20):
                for j in range(0, self.rect.height, 20):
                    pygame.draw.rect(superficie, MARRON, 
                                   (self.rect.x + i, self.rect.y + j, 20, 20), 1)
        elif self.tipo == 'tubo':
            pygame.draw.rect(superficie, VERDE_TUBO, self.rect)
            pygame.draw.rect(superficie, (0, 100, 0), self.rect, 3)
            pygame.draw.rect(superficie, VERDE_TUBO, 
                           (self.rect.x - 4, self.rect.y - 4, self.rect.width + 8, 8))
        else:
            pygame.draw.rect(superficie, MARRON, self.rect)
            pygame.draw.rect(superficie, (101, 67, 33), self.rect, 2)
