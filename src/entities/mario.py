import pygame
from typing import List, Optional
from src.utils.constantes import *

class Mario(pygame.sprite.Sprite):
    """
    Clase que representa al personaje principal Mario.
    
    Attributes:
        ancho (int): Ancho del sprite de Mario
        alto (int): Alto del sprite de Mario
        rect (pygame.Rect): Rectángulo de colisión
        velocidad_x (float): Velocidad horizontal
        velocidad_y (float): Velocidad vertical
        saltando (bool): Estado de salto
        direccion (str): Dirección actual ('izquierda' o 'derecha')
        vivo (bool): Estado de vida
        invencible (int): Contador de invencibilidad
        grande (bool): Estado de super mario
        tiene_flor (bool): Estado de fire mario
    """
    
    # Constantes específicas de Mario
    VELOCIDAD_BASE: float = 5.0
    ALTO_NORMAL: int = 32
    ALTO_GRANDE: int = 48
    TIEMPO_INVENCIBLE: int = 120
    
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.ancho = 32
        self.alto = self.ALTO_NORMAL
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)
        self.velocidad_x = 0.0
        self.velocidad_y = 0.0
        self.saltando = False
        self.direccion = 'derecha'
        self.vivo = True
        self.invencible = 0
        self.grande = False
        self.tiene_flor = False
        self.animacion_frame = 0
        self.animacion_contador = 0
    
    def update(self, plataformas: List[pygame.sprite.Sprite]) -> None:
        """
        Actualiza el estado de Mario.
        
        Args:
            plataformas: Lista de plataformas para colisiones
        """
        if not self.vivo:
            return
            
        self._actualizar_animacion()
        self._actualizar_invencibilidad()
        self._aplicar_gravedad()
        self._manejar_entrada()
        self._actualizar_posicion(plataformas)
    
    def _actualizar_animacion(self) -> None:
        """Actualiza los frames de animación."""
        self.animacion_contador += 1
        if self.animacion_contador > 5:
            self.animacion_frame = (self.animacion_frame + 1) % 3
            self.animacion_contador = 0
    
    def _actualizar_invencibilidad(self) -> None:
        """Actualiza el contador de invencibilidad."""
        if self.invencible > 0:
            self.invencible -= 1
    
    def _aplicar_gravedad(self) -> None:
        """Aplica la gravedad al movimiento vertical."""
        self.velocidad_y += GRAVEDAD
        self.velocidad_y = min(self.velocidad_y, 15)
    
    def _manejar_entrada(self) -> None:
        """Maneja la entrada del teclado para el movimiento."""
        teclas = pygame.key.get_pressed()
        self.velocidad_x = 0
        
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.velocidad_x = -self.VELOCIDAD_BASE
            self.direccion = 'izquierda'
        elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.velocidad_x = self.VELOCIDAD_BASE
            self.direccion = 'derecha'
    
    def saltar(self) -> None:
        """Hace que Mario salte si está en el suelo."""
        if not self.saltando and self.vivo:
            self.velocidad_y = -FUERZA_SALTO
            self.saltando = True
    
    def recibir_dano(self) -> bool:
        """
        Procesa el daño recibido por Mario.
        
        Returns:
            bool: True si Mario muere, False si sobrevive
        """
        if self.invencible > 0:
            return False
            
        if self.tiene_flor:
            self.tiene_flor = False
            self.invencible = self.TIEMPO_INVENCIBLE
            return False
        elif self.grande:
            self.grande = False
            self.alto = self.ALTO_NORMAL
            self.rect.height = self.ALTO_NORMAL
            self.invencible = self.TIEMPO_INVENCIBLE
            return False
        else:
            self.vivo = False
            return True
    
    def crecer(self) -> None:
        """Transforma a Mario en Super Mario."""
        if not self.grande:
            self.grande = True
            self.alto = self.ALTO_GRANDE
            self.rect.height = self.ALTO_GRANDE
            self.rect.y -= 16
    
    def obtener_flor(self) -> None:
        """Transforma a Mario en Fire Mario."""
        self.crecer()
        self.tiene_flor = True

    def dibujar(self, superficie):
        # ...código existente...
        pass
