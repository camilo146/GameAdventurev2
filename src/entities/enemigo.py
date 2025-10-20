"""
Clase Enemigo para los antagonistas del juego.
"""

import pygame
from typing import List
from src.utils.constantes import *
from src.utils.particulas import SistemaParticulas
from src.utils.sonidos import gestor_sonidos

class Enemigo(pygame.sprite.Sprite):
    """
    Clase que representa los enemigos del juego.
    
    Attributes:
        tipo (str): Tipo de enemigo ('goomba' o 'koopa')
        rect (pygame.Rect): Rectángulo de colisión
        velocidad_x (float): Velocidad horizontal
        vivo (bool): Estado de vida
        aplastado (bool): Si ha sido aplastado
        particulas (SistemaParticulas): Sistema de efectos visuales
    """
    
    def __init__(self, x: int, y: int, tipo: str = 'goomba'):
        super().__init__()
        self.tipo = tipo
        self.ancho = 30 if tipo == 'goomba' else 32
        self.alto = 30 if tipo == 'goomba' else 40
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)
        self.velocidad_x = -2 if tipo == 'goomba' else -1
        self.velocidad_y = 0
        self.vivo = True
        self.aplastado = False
        self.animacion_frame = 0
        self.animacion_contador = 0
        self.particulas = SistemaParticulas()
        self.tiempo_aplastado = 0
        
    def update(self, plataformas: List[pygame.sprite.Sprite]) -> None:
        """
        Actualiza el estado del enemigo.
        
        Args:
            plataformas: Lista de plataformas para colisiones
        """
        if not self.vivo:
            return
        
        # Eliminar enemigo si cae fuera del mapa
        if self.rect.y > ALTO + 100:
            self.vivo = False
            return
            
        if self.aplastado:
            self.tiempo_aplastado += 1
            if self.tiempo_aplastado > 60:  # 1 segundo a 60 FPS
                self.vivo = False
            return
            
        self._actualizar_animacion()
        self._aplicar_gravedad()
        self._actualizar_posicion(plataformas)
        self.particulas.update()
        
    def _actualizar_animacion(self) -> None:
        """Actualiza los frames de animación."""
        self.animacion_contador += 1
        if self.animacion_contador > 8:
            self.animacion_frame = (self.animacion_frame + 1) % 2
            self.animacion_contador = 0
    
    def _aplicar_gravedad(self) -> None:
        """Aplica la gravedad al enemigo."""
        self.velocidad_y += GRAVEDAD
        self.velocidad_y = min(self.velocidad_y, 15)
    
    def _actualizar_posicion(self, plataformas: List[pygame.sprite.Sprite]) -> None:
        """
        Actualiza la posición del enemigo con colisiones.
        
        Args:
            plataformas: Lista de plataformas para verificar colisiones
        """
        # Movimiento horizontal
        self.rect.x += self.velocidad_x
        
        # Cambiar dirección al tocar plataformas lateralmente
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                if self.velocidad_x > 0:
                    self.rect.right = plataforma.rect.left
                    self.velocidad_x = -abs(self.velocidad_x)
                elif self.velocidad_x < 0:
                    self.rect.left = plataforma.rect.right
                    self.velocidad_x = abs(self.velocidad_x)
        
        # Movimiento vertical
        self.rect.y += self.velocidad_y
        
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                if self.velocidad_y > 0:
                    self.rect.bottom = plataforma.rect.top
                    self.velocidad_y = 0
                elif self.velocidad_y < 0:
                    self.rect.top = plataforma.rect.bottom
                    self.velocidad_y = 0
    
    def aplastar(self) -> int:
        """
        Aplasta al enemigo.
        
        Returns:
            int: Puntos obtenidos por aplastar al enemigo
        """
        if self.aplastado or not self.vivo:
            return 0
            
        self.aplastado = True
        self.velocidad_x = 0
        self.alto = 15
        self.rect.height = 15
        
        # Efectos
        gestor_sonidos.reproducir_efecto('enemigo')
        self.particulas.crear_efecto(self.rect.centerx, self.rect.centery, 'enemigo')
        
        return 100 if self.tipo == 'goomba' else 200
    
    def eliminar(self) -> int:
        """
        Elimina al enemigo (por ejemplo, con bola de fuego).
        
        Returns:
            int: Puntos obtenidos
        """
        if not self.vivo:
            return 0
            
        self.vivo = False
        
        # Efectos
        gestor_sonidos.reproducir_efecto('enemigo')
        self.particulas.crear_explosion(self.rect.centerx, self.rect.centery, ROJO)
        
        return 200 if self.tipo == 'goomba' else 400
    
    def dibujar(self, superficie: pygame.Surface) -> None:
        """
        Dibuja al enemigo en la superficie.
        
        Args:
            superficie: Superficie donde dibujar al enemigo
        """
        # Dibujar partículas primero
        self.particulas.dibujar(superficie)
        
        if not self.vivo:
            return
            
        if self.tipo == 'goomba':
            self._dibujar_goomba(superficie)
        elif self.tipo == 'koopa':
            self._dibujar_koopa(superficie)
    
    def _dibujar_goomba(self, superficie: pygame.Surface) -> None:
        """
        Dibuja un Goomba.
        
        Args:
            superficie: Superficie donde dibujar
        """
        color = (101, 67, 33) if not self.aplastado else (80, 50, 20)
        
        if self.aplastado:
            # Goomba aplastado
            pygame.draw.ellipse(superficie, color, self.rect)
        else:
            # Cuerpo
            pygame.draw.ellipse(superficie, color, 
                              (self.rect.x + 2, self.rect.y + 8, self.ancho - 4, self.alto - 8))
            
            # Cabeza
            pygame.draw.ellipse(superficie, color, 
                              (self.rect.x, self.rect.y, self.ancho, 20))
            
            # Ojos
            ojo_offset = 2 if self.animacion_frame == 0 else -2
            pygame.draw.circle(superficie, NEGRO, 
                             (self.rect.x + 8 + ojo_offset, self.rect.y + 8), 3)
            pygame.draw.circle(superficie, NEGRO, 
                             (self.rect.x + 22 + ojo_offset, self.rect.y + 8), 3)
            
            # Cejas
            pygame.draw.rect(superficie, NEGRO, 
                           (self.rect.x + 5, self.rect.y + 4, 8, 2))
            pygame.draw.rect(superficie, NEGRO, 
                           (self.rect.x + 17, self.rect.y + 4, 8, 2))
    
    def _dibujar_koopa(self, superficie: pygame.Surface) -> None:
        """
        Dibuja un Koopa.
        
        Args:
            superficie: Superficie donde dibujar
        """
        if self.aplastado:
            # Caparazón
            pygame.draw.ellipse(superficie, VERDE, self.rect)
            pygame.draw.ellipse(superficie, (0, 150, 0), self.rect, 3)
        else:
            # Cuerpo
            pygame.draw.rect(superficie, AMARILLO, 
                           (self.rect.x + 8, self.rect.y + 20, 16, 20))
            
            # Caparazón
            pygame.draw.ellipse(superficie, VERDE, 
                              (self.rect.x, self.rect.y, self.ancho, 25))
            pygame.draw.ellipse(superficie, (0, 150, 0), 
                              (self.rect.x, self.rect.y, self.ancho, 25), 3)
            
            # Cabeza
            pygame.draw.circle(superficie, AMARILLO, 
                             (self.rect.x + 16, self.rect.y + 30), 8)
            
            # Ojos
            pygame.draw.circle(superficie, NEGRO, 
                             (self.rect.x + 13, self.rect.y + 28), 2)
            pygame.draw.circle(superficie, NEGRO, 
                             (self.rect.x + 19, self.rect.y + 28), 2)
            
            # Patas con animación
            pata_offset = 2 if self.animacion_frame == 0 else -2
            pygame.draw.rect(superficie, AMARILLO, 
                           (self.rect.x + 4, self.rect.bottom - 5 + pata_offset, 6, 5))
            pygame.draw.rect(superficie, AMARILLO, 
                           (self.rect.x + 22, self.rect.bottom - 5 - pata_offset, 6, 5))