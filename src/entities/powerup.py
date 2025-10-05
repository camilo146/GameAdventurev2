"""
Clase PowerUp para los objetos que mejoran a Mario.
"""

import pygame
from typing import List
from src.utils.constantes import *
from src.utils.particulas import SistemaParticulas

class PowerUp(pygame.sprite.Sprite):
    """
    Clase que representa los power-ups del juego.
    
    Attributes:
        tipo (TipoPowerUp): Tipo de power-up
        rect (pygame.Rect): Rectángulo de colisión
        velocidad_x (float): Velocidad horizontal
        velocidad_y (float): Velocidad vertical
        activo (bool): Si el power-up está activo
        particulas (SistemaParticulas): Sistema de efectos visuales
    """
    
    def __init__(self, x: int, y: int, tipo: TipoPowerUp = TipoPowerUp.HONGO, desde_bloque: bool = False):
        super().__init__()
        self.tipo = tipo
        self.rect = pygame.Rect(x, y, 24, 24)
        self.velocidad_x = 2
        self.velocidad_y = 0
        self.activo = not desde_bloque  # Los del suelo empiezan activos, los de bloques no
        self.animacion_frame = 0
        self.animacion_contador = 0
        self.particulas = SistemaParticulas()
        self.tiempo_aparicion = 0
        self.desde_bloque = desde_bloque
        
    def activar(self) -> None:
        """Activa el power-up para que comience a moverse."""
        self.activo = True
        self.particulas.crear_efecto(self.rect.centerx, self.rect.centery, 'powerup')
        
    def update(self, plataformas: List[pygame.sprite.Sprite]) -> None:
        """
        Actualiza el estado del power-up.
        
        Args:
            plataformas: Lista de plataformas para colisiones
        """
        if not self.activo:
            self.tiempo_aparicion += 1
            # Animación de aparición
            if self.tiempo_aparicion < 30:
                self.rect.y -= 1
            elif self.tiempo_aparicion == 30:
                self.activar()
            return
            
        self._actualizar_animacion()
        self._aplicar_gravedad()
        self._actualizar_posicion(plataformas)
        self.particulas.update()
        
    def _actualizar_animacion(self) -> None:
        """Actualiza los frames de animación."""
        self.animacion_contador += 1
        if self.animacion_contador > 6:
            self.animacion_frame = (self.animacion_frame + 1) % 4
            self.animacion_contador = 0
    
    def _aplicar_gravedad(self) -> None:
        """Aplica la gravedad al power-up."""
        if self.tipo != TipoPowerUp.ESTRELLA:  # Las estrellas rebotan
            self.velocidad_y += GRAVEDAD
            self.velocidad_y = min(self.velocidad_y, 15)
    
    def _actualizar_posicion(self, plataformas: List[pygame.sprite.Sprite]) -> None:
        """
        Actualiza la posición del power-up con colisiones.
        
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
                    
                    # Las estrellas rebotan
                    if self.tipo == TipoPowerUp.ESTRELLA:
                        self.velocidad_y = -8
                        
                elif self.velocidad_y < 0:
                    self.rect.top = plataforma.rect.bottom
                    self.velocidad_y = 0
    
    def dibujar(self, superficie: pygame.Surface) -> None:
        """
        Dibuja el power-up en la superficie.
        
        Args:
            superficie: Superficie donde dibujar el power-up
        """
        # Dibujar partículas
        self.particulas.dibujar(superficie)
        
        # Efecto de aparición
        if not self.activo and self.tiempo_aparicion % 6 < 3:
            return  # Parpadeo durante aparición
            
        if self.tipo == TipoPowerUp.HONGO:
            self._dibujar_hongo(superficie)
        elif self.tipo == TipoPowerUp.FLOR:
            self._dibujar_flor(superficie)
        elif self.tipo == TipoPowerUp.ESTRELLA:
            self._dibujar_estrella(superficie)
    
    def _dibujar_hongo(self, superficie: pygame.Surface) -> None:
        """
        Dibuja un hongo power-up.
        
        Args:
            superficie: Superficie donde dibujar
        """
        # Tallo
        pygame.draw.rect(superficie, (255, 248, 220), 
                        (self.rect.x + 8, self.rect.y + 12, 8, 12))
        
        # Cabeza del hongo
        pygame.draw.ellipse(superficie, ROJO, 
                          (self.rect.x, self.rect.y, 24, 16))
        
        # Puntos blancos en la cabeza
        pygame.draw.circle(superficie, BLANCO, 
                         (self.rect.x + 6, self.rect.y + 6), 3)
        pygame.draw.circle(superficie, BLANCO, 
                         (self.rect.x + 18, self.rect.y + 6), 3)
        pygame.draw.circle(superficie, BLANCO, 
                         (self.rect.x + 12, self.rect.y + 10), 2)
    
    def _dibujar_flor(self, superficie: pygame.Surface) -> None:
        """
        Dibuja una flor de fuego power-up.
        
        Args:
            superficie: Superficie donde dibujar
        """
        # Tallo
        pygame.draw.rect(superficie, VERDE, 
                        (self.rect.x + 10, self.rect.y + 16, 4, 8))
        
        # Pétalos con animación
        colores_petalos = [ROJO, NARANJA, AMARILLO, BLANCO]
        color_actual = colores_petalos[self.animacion_frame % len(colores_petalos)]
        
        # Pétalos superiores
        pygame.draw.circle(superficie, color_actual, 
                         (self.rect.x + 8, self.rect.y + 8), 6)
        pygame.draw.circle(superficie, color_actual, 
                         (self.rect.x + 16, self.rect.y + 8), 6)
        
        # Pétalos laterales
        pygame.draw.circle(superficie, color_actual, 
                         (self.rect.x + 4, self.rect.y + 12), 6)
        pygame.draw.circle(superficie, color_actual, 
                         (self.rect.x + 20, self.rect.y + 12), 6)
        
        # Centro
        pygame.draw.circle(superficie, AMARILLO, 
                         (self.rect.x + 12, self.rect.y + 10), 4)
    
    def _dibujar_estrella(self, superficie: pygame.Surface) -> None:
        """
        Dibuja una estrella power-up.
        
        Args:
            superficie: Superficie donde dibujar
        """
        import math
        
        # Estrella con efecto arcoíris
        if self.tipo == TipoPowerUp.ESTRELLA:
            import colorsys
            hue = (self.animacion_frame * 15) % 360
            rgb = colorsys.hsv_to_rgb(hue / 360.0, 1.0, 1.0)
            color_estrella = tuple(int(c * 255) for c in rgb)
        else:
            color_estrella = AMARILLO
        
        # Puntos de la estrella
        centro_x = self.rect.centerx
        centro_y = self.rect.centery
        radio_exterior = 12
        radio_interior = 6
        puntos = []
        
        for i in range(10):  # 5 puntas, 2 puntos por punta
            angulo = i * math.pi / 5
            if i % 2 == 0:
                x = centro_x + radio_exterior * math.cos(angulo - math.pi / 2)
                y = centro_y + radio_exterior * math.sin(angulo - math.pi / 2)
            else:
                x = centro_x + radio_interior * math.cos(angulo - math.pi / 2)
                y = centro_y + radio_interior * math.sin(angulo - math.pi / 2)
            puntos.append((int(x), int(y)))
        
        # Dibujar la estrella
        pygame.draw.polygon(superficie, color_estrella, puntos)
        pygame.draw.polygon(superficie, BLANCO, puntos, 2)