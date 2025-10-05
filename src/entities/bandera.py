import pygame
from typing import List, Tuple
from src.utils.constantes import BLANCO, ROJO, AMARILLO

class Bandera(pygame.sprite.Sprite):
    """Clase que representa la bandera de meta al final del nivel."""
    
    def __init__(self, x: int, y: int):
        super().__init__()
        self.rect = pygame.Rect(x, y, 40, 200)
        
    def dibujar(self, superficie: pygame.Surface) -> None:
        """Dibuja la bandera con su asta y decoraciones."""
        # Asta
        pygame.draw.rect(superficie, BLANCO, 
                        (self.rect.x + 18, self.rect.y, 4, 200))
        # Bandera
        puntos: List[Tuple[int, int]] = [
            (self.rect.x + 22, self.rect.y + 10),
            (self.rect.x + 50, self.rect.y + 25),
            (self.rect.x + 22, self.rect.y + 40)
        ]
        pygame.draw.polygon(superficie, ROJO, puntos)
        # Punta
        pygame.draw.circle(superficie, AMARILLO, 
                         (self.rect.x + 20, self.rect.y), 6)
