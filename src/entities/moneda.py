"""
Clase Moneda para los objetos coleccionables.
"""

import pygame
from src.utils.constantes import AMARILLO, NARANJA
from src.utils.sonidos import gestor_sonidos

class Moneda(pygame.sprite.Sprite):
    """
    Clase que representa una moneda coleccionable en el juego.
    
    Attributes:
        rect (pygame.Rect): Rectángulo de colisión
        animacion_frame (int): Frame actual de animación
        animacion_contador (int): Contador para controlar velocidad de animación
        valor (int): Valor en puntos de la moneda
    """
    
    def __init__(self, x: int, y: int, valor: int = 200):
        super().__init__()
        self.rect = pygame.Rect(x, y, 20, 20)
        self.animacion_frame = 0
        self.animacion_contador = 0
        self.valor = valor
        
    def update(self) -> None:
        """Actualiza el estado de la moneda y su animación."""
        self.animacion_contador += 1
        if self.animacion_contador > 5:
            self.animacion_frame = (self.animacion_frame + 1) % 4
            self.animacion_contador = 0
    
    def recoger(self) -> int:
        """
        Recoge la moneda y reproduce el sonido correspondiente.
        
        Returns:
            int: Valor de la moneda en puntos
        """
        gestor_sonidos.reproducir_efecto('moneda')
        return self.valor
    
    def dibujar(self, superficie: pygame.Surface) -> None:
        """
        Dibuja la moneda con efecto de rotación.
        
        Args:
            superficie: Superficie donde dibujar la moneda
        """
        # Efecto de rotación cambiando el ancho
        ancho = 20 - abs(self.animacion_frame - 2) * 5
        
        # Moneda principal
        pygame.draw.ellipse(superficie, AMARILLO, 
                          (self.rect.x + (20 - ancho) // 2, self.rect.y, ancho, 20))
        
        # Borde de la moneda
        pygame.draw.ellipse(superficie, NARANJA, 
                          (self.rect.x + (20 - ancho) // 2, self.rect.y, ancho, 20), 2)
        
        # Símbolo en el centro (cuando está de frente)
        if ancho > 15:
            centro_x = self.rect.x + 10
            centro_y = self.rect.y + 10
            
            # Dibujar símbolo de moneda
            pygame.draw.circle(superficie, NARANJA, (centro_x, centro_y), 6, 2)
            pygame.draw.rect(superficie, NARANJA, (centro_x - 1, centro_y - 6, 2, 12))
            pygame.draw.rect(superficie, NARANJA, (centro_x - 4, centro_y - 2, 8, 2))
            pygame.draw.rect(superficie, NARANJA, (centro_x - 4, centro_y + 1, 8, 2))