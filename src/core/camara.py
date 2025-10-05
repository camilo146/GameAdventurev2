"""
Sistema de cámara para seguir al jugador.
"""

from src.utils.constantes import ANCHO

class Camara:
    """
    Sistema de cámara que sigue al jugador por el nivel.
    
    Attributes:
        x (int): Posición X de la cámara
        ancho_mapa (int): Ancho total del mapa del nivel
    """
    
    def __init__(self, ancho_mapa: int):
        self.x = 0
        self.ancho_mapa = ancho_mapa
        
    def actualizar(self, objetivo: object) -> None:
        """
        Actualiza la posición de la cámara para seguir al objetivo.
        
        Args:
            objetivo: Objeto a seguir (normalmente Mario)
        """
        # Mantener al objetivo en el tercio izquierdo de la pantalla
        self.x = objetivo.rect.x - ANCHO // 3
        
        # Limitar la cámara a los bordes del mapa
        if self.x < 0:
            self.x = 0
        if self.x > self.ancho_mapa - ANCHO:
            self.x = self.ancho_mapa - ANCHO
    
    def aplicar(self, objetivo: object) -> tuple:
        """
        Aplica el offset de la cámara a un objeto.
        
        Args:
            objetivo: Objeto al que aplicar el offset
            
        Returns:
            tuple: Posición ajustada (x, y)
        """
        return (objetivo.rect.x - self.x, objetivo.rect.y)
    
    def aplicar_rect(self, rect: object) -> object:
        """
        Aplica el offset de la cámara a un rectángulo.
        
        Args:
            rect: Rectángulo al que aplicar el offset
            
        Returns:
            pygame.Rect: Rectángulo ajustado
        """
        import pygame
        return pygame.Rect(rect.x - self.x, rect.y, rect.width, rect.height)