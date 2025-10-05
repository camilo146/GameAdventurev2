"""
Clase Bandera para la meta del nivel.
"""

import pygame
from typing import List, Tuple
from src.utils.constantes import BLANCO, ROJO, AMARILLO

class Bandera(pygame.sprite.Sprite):
    """
    Clase que representa la bandera de meta al final del nivel.
    
    Attributes:
        rect (pygame.Rect): Rectángulo de colisión
        animacion_frame (int): Frame de animación de la bandera
        animacion_contador (int): Contador para controlar la animación
    """
    
    def __init__(self, x: int, y: int):
        super().__init__()
        self.rect = pygame.Rect(x, y, 40, 200)
        self.animacion_frame = 0
        self.animacion_contador = 0
        
    def update(self) -> None:
        """Actualiza la animación de la bandera."""
        self.animacion_contador += 1
        if self.animacion_contador > 8:
            self.animacion_frame = (self.animacion_frame + 1) % 3
            self.animacion_contador = 0
        
    def dibujar(self, superficie: pygame.Surface) -> None:
        """
        Dibuja la bandera con su asta y decoraciones.
        
        Args:
            superficie: Superficie donde dibujar la bandera
        """
        # Asta de la bandera
        pygame.draw.rect(superficie, BLANCO, 
                        (self.rect.x + 18, self.rect.y, 4, 200))
        
        # Bandera ondeando
        offset = self.animacion_frame * 2
        puntos: List[Tuple[int, int]] = [
            (self.rect.x + 22, self.rect.y + 10),
            (self.rect.x + 50 + offset, self.rect.y + 20),
            (self.rect.x + 45 + offset, self.rect.y + 30),
            (self.rect.x + 22, self.rect.y + 40)
        ]
        pygame.draw.polygon(superficie, ROJO, puntos)
        pygame.draw.polygon(superficie, (150, 0, 0), puntos, 2)
        
        # Punta dorada de la bandera
        pygame.draw.circle(superficie, AMARILLO, 
                         (self.rect.x + 20, self.rect.y), 6)
        pygame.draw.circle(superficie, (200, 180, 0), 
                         (self.rect.x + 20, self.rect.y), 6, 2)
        
        # Base del asta
        pygame.draw.rect(superficie, (139, 69, 19), 
                        (self.rect.x + 15, self.rect.bottom - 10, 10, 10))