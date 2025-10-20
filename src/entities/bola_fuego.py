"""
Módulo que contiene la clase BolaFuego para los proyectiles de Mario.
"""
import pygame
from typing import List
from src.utils.constantes import ROJO, NARANJA, AMARILLO, BLANCO


class BolaFuego(pygame.sprite.Sprite):
    """Representa una bola de fuego lanzada por Mario."""
    
    def __init__(self, x: int, y: int, direccion: str):
        """
        Inicializa una bola de fuego.
        
        Args:
            x: Posición X inicial
            y: Posición Y inicial
            direccion: Dirección del lanzamiento ('izquierda' o 'derecha')
        """
        super().__init__()
        self.ancho = 12
        self.alto = 12
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)
        self.direccion = direccion
        self.velocidad_x = 10 if direccion == 'derecha' else -10
        self.velocidad_y = -2  # Pequeño arco hacia arriba
        self.gravedad = 0.3
        self.animacion_frame = 0
        self.viva = True
        
    def update(self, plataformas: List[pygame.sprite.Sprite]) -> None:
        """
        Actualiza la posición y estado de la bola de fuego.
        
        Args:
            plataformas: Lista de plataformas para detectar colisiones
        """
        if not self.viva:
            return
            
        # Movimiento
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        
        # Aplicar gravedad
        self.velocidad_y += self.gravedad
        
        # Animación
        self.animacion_frame += 1
        
        # Rebotar en plataformas
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                if self.velocidad_y > 0:  # Cayendo
                    self.rect.bottom = plataforma.rect.top
                    self.velocidad_y = -5  # Rebote
        
        # Destruir si sale de la pantalla o lleva mucho tiempo
        if self.rect.x < -50 or self.rect.x > 1000 or self.animacion_frame > 300:
            self.viva = False
    
    def dibujar(self, superficie: pygame.Surface, offset_x: int = 0) -> None:
        """
        Dibuja la bola de fuego en la superficie.
        
        Args:
            superficie: Superficie donde dibujar
            offset_x: Desplazamiento horizontal de la cámara
        """
        if not self.viva:
            return
            
        x = self.rect.x - offset_x
        y = self.rect.y
        
        # Animación de rotación (4 frames)
        frame = (self.animacion_frame // 5) % 4
        
        # Centro de la bola
        centro_x = x + self.ancho // 2
        centro_y = y + self.alto // 2
        
        # Núcleo blanco brillante
        pygame.draw.circle(superficie, BLANCO, (centro_x, centro_y), 3)
        
        if frame == 0 or frame == 2:
            # Forma circular con llamas
            pygame.draw.circle(superficie, AMARILLO, (centro_x, centro_y), 5)
            pygame.draw.circle(superficie, NARANJA, (centro_x, centro_y), 6)
            pygame.draw.circle(superficie, ROJO, (centro_x, centro_y), 7)
        else:
            # Forma con picos (llamas)
            puntos = [
                (centro_x, centro_y - 7),  # Arriba
                (centro_x + 5, centro_y - 4),  # Derecha arriba
                (centro_x + 7, centro_y),  # Derecha
                (centro_x + 5, centro_y + 4),  # Derecha abajo
                (centro_x, centro_y + 7),  # Abajo
                (centro_x - 5, centro_y + 4),  # Izquierda abajo
                (centro_x - 7, centro_y),  # Izquierda
                (centro_x - 5, centro_y - 4),  # Izquierda arriba
            ]
            pygame.draw.polygon(superficie, ROJO, puntos)
            
            # Capa naranja interior
            puntos_naranja = [
                (centro_x, centro_y - 5),
                (centro_x + 4, centro_y - 3),
                (centro_x + 5, centro_y),
                (centro_x + 4, centro_y + 3),
                (centro_x, centro_y + 5),
                (centro_x - 4, centro_y + 3),
                (centro_x - 5, centro_y),
                (centro_x - 4, centro_y - 3),
            ]
            pygame.draw.polygon(superficie, NARANJA, puntos_naranja)
            
            # Capa amarilla interior
            pygame.draw.circle(superficie, AMARILLO, (centro_x, centro_y), 4)
    
    def eliminar(self) -> None:
        """Marca la bola de fuego para eliminación."""
        self.viva = False
