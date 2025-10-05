"""
Clase Plataforma para los elementos sólidos del juego.
"""

import pygame
from typing import Literal
from src.utils.constantes import (VERDE, MARRON, NARANJA, VERDE_TUBO, BLANCO, 
                                  MARRON_LADRILLO, VERDE_HIERBA, NARANJA_BLOQUE, 
                                  AMARILLO_BLOQUE)

class Plataforma(pygame.sprite.Sprite):
    """
    Clase que representa las plataformas del juego.
    
    Attributes:
        rect (pygame.Rect): Rectángulo de colisión
        tipo (str): Tipo de plataforma ('normal', 'suelo', 'bloque', 'tubo')
        golpeado (bool): Estado de si ha sido golpeado
    """
    
    def __init__(self, x: int, y: int, ancho: int, alto: int, 
                 tipo: Literal['normal', 'suelo', 'bloque', 'tubo', 'nube', 'metal'] = 'normal'):
        super().__init__()
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.tipo = tipo
        self.golpeado = False
        self.tiene_powerup = False
        self.tipo_powerup = None
        self.powerup_liberado = False
        self.brillo_timer = 0.0
        
        # Sistema de power-ups para bloques
        if tipo == 'bloque':
            # Algunos bloques tienen power-ups
            import random
            self.tiene_powerup = random.choice([True, False, False, False])  # 25% de probabilidad
            
    def actualizar(self, delta_time: float) -> None:
        """
        Actualiza los efectos visuales de la plataforma.
        
        Args:
            delta_time: Tiempo transcurrido desde la última actualización
        """
        self.brillo_timer += delta_time
        
        # Efecto de brillo para bloques con power-up
        if (self.tipo == 'bloque' and hasattr(self, 'tiene_powerup') and 
            self.tiene_powerup and not self.powerup_liberado):
            # Resetear el timer cada 2 segundos para el efecto de parpadeo
            if self.brillo_timer > 2.0:
                self.brillo_timer = 0.0
        
    def dibujar(self, superficie: pygame.Surface) -> None:
        """
        Dibuja la plataforma según su tipo.
        
        Args:
            superficie: Superficie donde dibujar la plataforma
        """
        if self.tipo == 'suelo':
            # Fondo marrón (tierra)
            pygame.draw.rect(superficie, MARRON_LADRILLO, self.rect)
            
            # Patrón de ladrillos como en Mario Bros clásico
            brick_width = 16
            brick_height = 16
            
            for y in range(self.rect.y, self.rect.y + self.rect.height, brick_height):
                for x in range(self.rect.x, self.rect.x + self.rect.width, brick_width):
                    # Offset para patrón de ladrillos
                    offset = brick_width // 2 if ((y - self.rect.y) // brick_height) % 2 else 0
                    brick_x = x + offset
                    
                    if brick_x < self.rect.x + self.rect.width:
                        # Dibujar ladrillo individual
                        pygame.draw.rect(superficie, MARRON_LADRILLO, 
                                       (brick_x, y, min(brick_width, self.rect.x + self.rect.width - brick_x), brick_height))
                        # Borde del ladrillo
                        pygame.draw.rect(superficie, (160, 100, 50), 
                                       (brick_x, y, min(brick_width, self.rect.x + self.rect.width - brick_x), brick_height), 1)
            
            # Hierba verde en la parte superior
            if self.rect.height > 20:
                for i in range(self.rect.x, self.rect.x + self.rect.width, 4):
                    # Pequeños tufts de hierba
                    pygame.draw.line(superficie, VERDE_HIERBA, 
                                   (i, self.rect.y - 2), (i, self.rect.y + 3), 2)
                    pygame.draw.line(superficie, VERDE_HIERBA, 
                                   (i + 2, self.rect.y - 1), (i + 2, self.rect.y + 2), 1)
                           
        elif self.tipo == 'bloque':
            if self.golpeado:
                # Bloque golpeado - color gris
                pygame.draw.rect(superficie, (160, 160, 160), self.rect)
                pygame.draw.rect(superficie, (100, 100, 100), self.rect, 2)
            elif hasattr(self, 'tiene_powerup') and self.tiene_powerup and not self.powerup_liberado:
                # Bloques con power-up - estilo Mario Bros clásico
                import math
                brillo_intensidad = (math.sin(self.brillo_timer * 3) + 1) / 2  # 0 a 1
                base_dorado = 200 + int(55 * brillo_intensidad)
                color = (base_dorado, base_dorado - 40, 0)  # Dorado animado
                
                # Fondo del bloque
                pygame.draw.rect(superficie, color, self.rect)
                
                # Patrón de puntos como en Mario Bros original
                for i in range(2):
                    for j in range(2):
                        x = self.rect.x + 4 + (i * 12)
                        y = self.rect.y + 4 + (j * 12)
                        pygame.draw.circle(superficie, AMARILLO_BLOQUE, (x, y), 2)
                
                # Borde del bloque
                pygame.draw.rect(superficie, (160, 120, 0), self.rect, 2)
                
                # Símbolo de interrogación más grande y visible
                centro_x = self.rect.centerx
                centro_y = self.rect.centery
                
                # Dibujar "?" estilo pixel art
                # Parte superior del ?
                pygame.draw.rect(superficie, BLANCO, (centro_x - 3, centro_y - 6, 6, 2))
                pygame.draw.rect(superficie, BLANCO, (centro_x + 1, centro_y - 4, 2, 4))
                pygame.draw.rect(superficie, BLANCO, (centro_x - 1, centro_y - 2, 2, 2))
                # Punto del ?
                pygame.draw.rect(superficie, BLANCO, (centro_x - 1, centro_y + 2, 2, 2))
            else:
                # Bloques normales - estilo ladrillo como Mario Bros
                pygame.draw.rect(superficie, NARANJA_BLOQUE, self.rect)
                
                # Patrón de ladrillos en el bloque
                pygame.draw.line(superficie, (160, 60, 20), 
                               (self.rect.x, self.rect.centery), 
                               (self.rect.x + self.rect.width, self.rect.centery), 1)
                pygame.draw.line(superficie, (160, 60, 20), 
                               (self.rect.centerx, self.rect.y), 
                               (self.rect.centerx, self.rect.y + self.rect.height), 1)
                
                # Borde del bloque
                pygame.draw.rect(superficie, (160, 60, 20), self.rect, 2)
                
                # Highlight superior para efecto 3D
                pygame.draw.line(superficie, (255, 150, 100), 
                               (self.rect.x + 1, self.rect.y + 1), 
                               (self.rect.x + self.rect.width - 2, self.rect.y + 1), 1)
                
        elif self.tipo == 'tubo':
            # Cuerpo del tubo
            pygame.draw.rect(superficie, VERDE_TUBO, self.rect)
            # Borde oscuro
            pygame.draw.rect(superficie, (0, 100, 0), self.rect, 3)
            # Borde superior (labio del tubo)
            pygame.draw.rect(superficie, VERDE_TUBO, 
                           (self.rect.x - 4, self.rect.y - 4, self.rect.width + 8, 8))
            pygame.draw.rect(superficie, (0, 100, 0), 
                           (self.rect.x - 4, self.rect.y - 4, self.rect.width + 8, 8), 2)
            # Highlight en el tubo
            pygame.draw.rect(superficie, (100, 255, 100), 
                           (self.rect.x + 5, self.rect.y, 8, self.rect.height), 0)
                           
        elif self.tipo == 'nube':
            # Plataforma de nube flotante
            color_nube = (255, 255, 255)
            color_sombra = (200, 200, 200)
            
            # Base de la nube
            pygame.draw.ellipse(superficie, color_nube, self.rect)
            pygame.draw.ellipse(superficie, color_sombra, self.rect, 2)
            
            # Círculos decorativos para simular esponjosidad
            for i in range(3):
                x_offset = (self.rect.width // 4) * (i + 1)
                y_offset = -5 if i % 2 == 0 else -3
                radio = 8 + (i * 2)
                pygame.draw.circle(superficie, color_nube, 
                                 (self.rect.x + x_offset, self.rect.y + y_offset), radio)
                pygame.draw.circle(superficie, color_sombra, 
                                 (self.rect.x + x_offset, self.rect.y + y_offset), radio, 1)
                                 
        elif self.tipo == 'metal':
            # Plataforma metálica
            color_metal = (150, 150, 150)
            color_brillante = (200, 200, 200)
            color_oscuro = (100, 100, 100)
            
            pygame.draw.rect(superficie, color_metal, self.rect)
            
            # Efecto metálico con gradiente
            for i in range(self.rect.height // 3):
                alpha = int(100 * (1 - i / (self.rect.height // 3)))
                color_gradiente = (*color_brillante, alpha)
                pygame.draw.line(superficie, color_gradiente,
                               (self.rect.x, self.rect.y + i),
                               (self.rect.x + self.rect.width, self.rect.y + i))
            
            # Remaches decorativos
            for i in range(0, self.rect.width, 25):
                pygame.draw.circle(superficie, color_oscuro,
                                 (self.rect.x + i + 10, self.rect.centery), 3)
                pygame.draw.circle(superficie, color_brillante,
                                 (self.rect.x + i + 10, self.rect.centery), 2)
            
            # Borde metálico
            pygame.draw.rect(superficie, color_oscuro, self.rect, 2)
            
        else:  # Plataformas normales
            # Plataforma con textura de ladrillos
            color_base = (139, 69, 19)  # Marrón ladrillo
            color_borde = (101, 67, 33)  # Marrón oscuro
            
            pygame.draw.rect(superficie, color_base, self.rect)
            pygame.draw.rect(superficie, color_borde, self.rect, 2)
            
            # Patrón de ladrillos
            for y in range(self.rect.y, self.rect.y + self.rect.height, 10):
                for x in range(self.rect.x, self.rect.x + self.rect.width, 20):
                    offset = 10 if ((y - self.rect.y) // 10) % 2 else 0
                    pygame.draw.line(superficie, color_borde, 
                                   (x + offset, y), (x + offset + 19, y), 1)
            
            # Highlight superior
            pygame.draw.line(superficie, (180, 140, 100), 
                           (self.rect.x, self.rect.y), 
                           (self.rect.x + self.rect.width, self.rect.y), 1)