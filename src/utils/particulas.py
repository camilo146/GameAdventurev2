"""
Sistema de partículas para efectos visuales del juego.
"""

import pygame
import random
import math
from typing import List, Tuple
from src.utils.constantes import *

class Particula:
    """
    Clase individual que representa una partícula visual.
    
    Attributes:
        x (float): Posición X de la partícula
        y (float): Posición Y de la partícula
        velocidad_x (float): Velocidad horizontal
        velocidad_y (float): Velocidad vertical
        color (Tuple[int, int, int]): Color RGB de la partícula
        vida (int): Tiempo de vida restante
        vida_inicial (int): Tiempo de vida inicial
        tamaño (int): Tamaño de la partícula
    """
    
    def __init__(self, x: float, y: float, velocidad_x: float, velocidad_y: float, 
                 color: Tuple[int, int, int], vida: int = 60, tamaño: int = 3):
        self.x = x
        self.y = y
        self.velocidad_x = velocidad_x
        self.velocidad_y = velocidad_y
        self.color = color
        self.vida = vida
        self.vida_inicial = vida
        self.tamaño = tamaño
        
    def update(self) -> bool:
        """
        Actualiza la posición y estado de la partícula.
        
        Returns:
            bool: True si la partícula sigue viva, False si debe eliminarse
        """
        self.x += self.velocidad_x
        self.y += self.velocidad_y
        self.velocidad_y += 0.2  # Gravedad ligera
        self.velocidad_x *= 0.98  # Fricción
        self.vida -= 1
        
        return self.vida > 0
    
    def dibujar(self, superficie: pygame.Surface) -> None:
        """
        Dibuja la partícula en la superficie.
        
        Args:
            superficie: Superficie donde dibujar la partícula
        """
        # Calcular transparencia basada en vida restante
        alpha = int(255 * (self.vida / self.vida_inicial))
        color_con_alpha = (*self.color, alpha)
        
        # Crear superficie temporal con alpha
        temp_surf = pygame.Surface((self.tamaño * 2, self.tamaño * 2), pygame.SRCALPHA)
        pygame.draw.circle(temp_surf, color_con_alpha, 
                          (self.tamaño, self.tamaño), self.tamaño)
        
        superficie.blit(temp_surf, (int(self.x - self.tamaño), int(self.y - self.tamaño)))

class SistemaParticulas:
    """
    Sistema que maneja múltiples partículas para efectos visuales.
    
    Attributes:
        particulas (List[Particula]): Lista de partículas activas
    """
    
    def __init__(self):
        self.particulas: List[Particula] = []
    
    def crear_efecto(self, x: float, y: float, tipo: str) -> None:
        """
        Crea un efecto de partículas en la posición especificada.
        
        Args:
            x: Posición X del efecto
            y: Posición Y del efecto
            tipo: Tipo de efecto ('salto', 'moneda', 'enemigo', 'powerup')
        """
        config = PARTICULAS_CONFIG.get(tipo, PARTICULAS_CONFIG['salto'])
        
        for _ in range(config['cantidad']):
            velocidad_x = random.uniform(-config['velocidad'], config['velocidad'])
            velocidad_y = random.uniform(-config['velocidad'], -1)
            vida = random.randint(30, 90)
            tamaño = random.randint(2, 5)
            
            particula = Particula(x, y, velocidad_x, velocidad_y, 
                                config['color'], vida, tamaño)
            self.particulas.append(particula)
    
    def crear_explosion(self, x: float, y: float, color: Tuple[int, int, int], 
                       cantidad: int = 15) -> None:
        """
        Crea una explosión de partículas.
        
        Args:
            x: Posición X de la explosión
            y: Posición Y de la explosión
            color: Color de las partículas
            cantidad: Número de partículas a crear
        """
        for _ in range(cantidad):
            angulo = random.uniform(0, 2 * math.pi)
            velocidad = random.uniform(2, 8)
            velocidad_x = math.cos(angulo) * velocidad
            velocidad_y = math.sin(angulo) * velocidad
            vida = random.randint(40, 80)
            tamaño = random.randint(3, 6)
            
            particula = Particula(x, y, velocidad_x, velocidad_y, color, vida, tamaño)
            self.particulas.append(particula)
    
    def update(self) -> None:
        """Actualiza todas las partículas y elimina las que han expirado."""
        self.particulas = [p for p in self.particulas if p.update()]
    
    def dibujar(self, superficie: pygame.Surface) -> None:
        """
        Dibuja todas las partículas activas.
        
        Args:
            superficie: Superficie donde dibujar las partículas
        """
        for particula in self.particulas:
            particula.dibujar(superficie)
    
    def limpiar(self) -> None:
        """Elimina todas las partículas."""
        self.particulas.clear()
    
    def cantidad_particulas(self) -> int:
        """
        Retorna la cantidad de partículas activas.
        
        Returns:
            int: Número de partículas activas
        """
        return len(self.particulas)