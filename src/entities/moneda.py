import pygame
from typing import Tuple
from src.utils.constantes import AMARILLO, NARANJA

class Moneda(pygame.sprite.Sprite):
    """Clase que representa una moneda coleccionable en el juego."""
    
    def __init__(self, x: int, y: int):
        super().__init__()
        self.rect = pygame.Rect(x, y, 20, 20)
        self.animacion_frame = 0
        self.animacion_contador = 0
        
    def update(self) -> None:
        """Actualiza el estado de la moneda y su animación."""
        self.animacion_contador += 1
        if self.animacion_contador > 5:
            self.animacion_frame = (self.animacion_frame + 1) % 4
            self.animacion_contador = 0
    
    def dibujar(self, superficie: pygame.Surface) -> None:
        """Dibuja la moneda con efecto de rotación."""
        ancho = 20 - abs(self.animacion_frame - 2) * 5
        pygame.draw.ellipse(superficie, AMARILLO, 
                          (self.rect.x + (20 - ancho) // 2, self.rect.y, ancho, 20))
        pygame.draw.ellipse(superficie, NARANJA, 
                          (self.rect.x + (20 - ancho) // 2, self.rect.y, ancho, 20), 2)
