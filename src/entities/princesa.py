"""
Clase para la Princesa Peach.
"""

import pygame
from src.utils.constantes import ROSA, AMARILLO, BLANCO, NEGRO, ROJO

class Princesa:
    """
    Clase que representa a la Princesa Peach al final del juego.
    
    Attributes:
        x (int): Posición X de la princesa
        y (int): Posición Y de la princesa
        ancho (int): Ancho de la princesa
        alto (int): Alto de la princesa
        rescatada (bool): Si Mario ha llegado hasta ella
    """
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.ancho = 30
        self.alto = 40
        self.rescatada = False
        self.frame_animacion = 0
        
        # Animación de balanceo suave
        self.tiempo_balanceo = 0
        self.offset_balanceo = 0
    
    def get_rect(self) -> pygame.Rect:
        """Retorna el rectángulo de colisión de la princesa."""
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)
    
    def rescatar(self) -> None:
        """Marca a la princesa como rescatada."""
        self.rescatada = True
    
    def update(self) -> None:
        """Actualiza la animación de la princesa."""
        self.frame_animacion = (self.frame_animacion + 1) % 60
        
        # Animación de balanceo suave
        import math
        self.tiempo_balanceo += 0.1
        self.offset_balanceo = int(math.sin(self.tiempo_balanceo) * 2)
    
    def dibujar(self, pantalla: pygame.Surface, camara_x: int) -> None:
        """
        Dibuja a la princesa Peach en la pantalla con estilo mejorado de NES.
        
        Args:
            pantalla: Superficie de pygame donde dibujar
            camara_x: Posición X de la cámara para el desplazamiento
        """
        x_pantalla = self.x - camara_x + self.offset_balanceo
        y_base = self.y
        
        # Colores de la Princesa Peach clásica (mejorados)
        color_piel = (255, 206, 177)
        color_piel_sombra = (235, 186, 157)
        color_rosa_vestido = (255, 153, 204)
        color_rosa_oscuro = (230, 120, 180)
        color_rosa_claro = (255, 204, 229)
        color_amarillo_cabello = (255, 204, 0)
        color_amarillo_oscuro = (230, 180, 0)
        color_azul_ojos = (51, 153, 255)
        
        # Animación de brillo del vestido
        brillo_vestido = abs((self.frame_animacion - 30)) / 60
        
        # Animación de brillo para la corona (más intensa)
        brillo = abs((self.frame_animacion - 30)) / 30
        color_corona = (
            int(255 * (0.85 + 0.15 * brillo)),
            int(215 * (0.85 + 0.15 * brillo)),
            int(0)
        )
        color_corona_oscuro = (200, 165, 0)
        
        # ===== CABELLO TRASERO (detrás de la cabeza) =====
        # Cabello largo detrás con volumen
        pygame.draw.ellipse(pantalla, color_amarillo_cabello, (x_pantalla + 5, y_base + 10, 8, 16))
        pygame.draw.ellipse(pantalla, color_amarillo_cabello, (x_pantalla + 17, y_base + 10, 8, 16))
        # Sombras del cabello
        pygame.draw.ellipse(pantalla, color_amarillo_oscuro, (x_pantalla + 6, y_base + 18, 6, 6))
        pygame.draw.ellipse(pantalla, color_amarillo_oscuro, (x_pantalla + 18, y_base + 18, 6, 6))
        
        # ===== CORONA =====
        # Base de la corona (3 puntas principales con bordes)
        # Punta izquierda
        pygame.draw.polygon(pantalla, color_corona, [
            (x_pantalla + 9, y_base + 1),
            (x_pantalla + 7, y_base + 7),
            (x_pantalla + 15, y_base + 7),
            (x_pantalla + 13, y_base + 1)
        ])
        pygame.draw.polygon(pantalla, color_corona_oscuro, [
            (x_pantalla + 9, y_base + 1),
            (x_pantalla + 7, y_base + 7),
            (x_pantalla + 15, y_base + 7),
            (x_pantalla + 13, y_base + 1)
        ], 1)
        
        # Punta central
        pygame.draw.polygon(pantalla, color_corona, [
            (x_pantalla + 13, y_base + 1),
            (x_pantalla + 11, y_base + 7),
            (x_pantalla + 19, y_base + 7),
            (x_pantalla + 17, y_base + 1)
        ])
        pygame.draw.polygon(pantalla, color_corona_oscuro, [
            (x_pantalla + 13, y_base + 1),
            (x_pantalla + 11, y_base + 7),
            (x_pantalla + 19, y_base + 7),
            (x_pantalla + 17, y_base + 1)
        ], 1)
        
        # Punta derecha
        pygame.draw.polygon(pantalla, color_corona, [
            (x_pantalla + 17, y_base + 1),
            (x_pantalla + 15, y_base + 7),
            (x_pantalla + 23, y_base + 7),
            (x_pantalla + 21, y_base + 1)
        ])
        pygame.draw.polygon(pantalla, color_corona_oscuro, [
            (x_pantalla + 17, y_base + 1),
            (x_pantalla + 15, y_base + 7),
            (x_pantalla + 23, y_base + 7),
            (x_pantalla + 21, y_base + 1)
        ], 1)
        
        # Banda dorada de la corona con sombra
        pygame.draw.rect(pantalla, color_corona, (x_pantalla + 7, y_base + 7, 16, 3))
        pygame.draw.rect(pantalla, color_corona_oscuro, (x_pantalla + 7, y_base + 9, 16, 1))
        
        # Gemas en la corona (rojas y azules alternadas)
        pygame.draw.circle(pantalla, ROJO, (x_pantalla + 11, self.y + 3), 2)
        pygame.draw.circle(pantalla, (0, 100, 255), (x_pantalla + 15, self.y + 2), 2)
        pygame.draw.circle(pantalla, ROJO, (x_pantalla + 19, self.y + 3), 2)
        
        # Brillo en la gema central
        if self.frame_animacion < 30:
            pygame.draw.circle(pantalla, BLANCO, (x_pantalla + 16, self.y + 1), 1)
        
        # ===== CABELLO FRONTAL =====
        # Cabello rubio sobre la frente
        pygame.draw.rect(pantalla, color_amarillo_cabello, (x_pantalla + 7, self.y + 9, 16, 6))
        
        # Flequillo (mechones)
        pygame.draw.polygon(pantalla, color_amarillo_cabello, [
            (x_pantalla + 10, self.y + 9),
            (x_pantalla + 8, self.y + 13),
            (x_pantalla + 12, self.y + 13)
        ])
        pygame.draw.polygon(pantalla, color_amarillo_cabello, [
            (x_pantalla + 15, self.y + 9),
            (x_pantalla + 13, self.y + 13),
            (x_pantalla + 17, self.y + 13)
        ])
        pygame.draw.polygon(pantalla, color_amarillo_cabello, [
            (x_pantalla + 20, self.y + 9),
            (x_pantalla + 18, self.y + 13),
            (x_pantalla + 22, self.y + 13)
        ])
        
        # ===== CABEZA Y CARA =====
        # Cabeza (forma ovalada)
        pygame.draw.ellipse(pantalla, color_piel, (x_pantalla + 9, self.y + 12, 12, 14))
        
        # Orejas
        pygame.draw.circle(pantalla, color_piel, (x_pantalla + 8, self.y + 16), 3)
        pygame.draw.circle(pantalla, color_piel, (x_pantalla + 22, self.y + 16), 3)
        
        # Aretes (pendientes dorados)
        pygame.draw.circle(pantalla, color_corona, (x_pantalla + 7, self.y + 17), 2)
        pygame.draw.circle(pantalla, color_corona, (x_pantalla + 23, self.y + 17), 2)
        
        # ===== OJOS =====
        # Ojos grandes (estilo anime de NES)
        pygame.draw.ellipse(pantalla, BLANCO, (x_pantalla + 10, self.y + 16, 4, 5))
        pygame.draw.ellipse(pantalla, BLANCO, (x_pantalla + 16, self.y + 16, 4, 5))
        
        # Pupilas azules
        pygame.draw.ellipse(pantalla, color_azul_ojos, (x_pantalla + 11, self.y + 17, 3, 3))
        pygame.draw.ellipse(pantalla, color_azul_ojos, (x_pantalla + 17, self.y + 17, 3, 3))
        
        # Brillos en los ojos
        pygame.draw.circle(pantalla, BLANCO, (x_pantalla + 12, self.y + 17), 1)
        pygame.draw.circle(pantalla, BLANCO, (x_pantalla + 18, self.y + 17), 1)
        
        # Pestañas
        pygame.draw.line(pantalla, NEGRO, (x_pantalla + 10, self.y + 15), (x_pantalla + 9, self.y + 14), 1)
        pygame.draw.line(pantalla, NEGRO, (x_pantalla + 19, self.y + 15), (x_pantalla + 20, self.y + 14), 1)
        
        # ===== NARIZ Y BOCA =====
        # Pequeña nariz
        pygame.draw.circle(pantalla, (255, 180, 150), (x_pantalla + 15, self.y + 21), 1)
        
        # Sonrisa dulce
        pygame.draw.arc(pantalla, (200, 80, 80), (x_pantalla + 12, self.y + 21, 6, 4), 3.14, 0, 2)
        
        # ===== CUELLO =====
        pygame.draw.rect(pantalla, color_piel, (x_pantalla + 12, self.y + 25, 6, 3))
        
        # ===== VESTIDO =====
        # Parte superior del vestido (corsé)
        pygame.draw.rect(pantalla, color_rosa_vestido, (x_pantalla + 9, self.y + 28, 12, 10))
        
        # Escote y detalles blancos
        pygame.draw.arc(pantalla, BLANCO, (x_pantalla + 10, self.y + 28, 10, 6), 3.14, 0, 2)
        
        # Broche/joya del vestido
        pygame.draw.circle(pantalla, (0, 150, 255), (x_pantalla + 15, self.y + 32), 2)
        pygame.draw.circle(pantalla, BLANCO, (x_pantalla + 16, self.y + 31), 1)
        
        # Falda del vestido (forma de campana más amplia)
        pygame.draw.polygon(pantalla, color_rosa_vestido, [
            (x_pantalla + 9, self.y + 38),
            (x_pantalla + 4, self.y + 42),
            (x_pantalla + 26, self.y + 42),
            (x_pantalla + 21, self.y + 38)
        ])
        
        # Capa de tul (más clara)
        pygame.draw.polygon(pantalla, color_rosa_claro, [
            (x_pantalla + 10, self.y + 38),
            (x_pantalla + 6, self.y + 41),
            (x_pantalla + 24, self.y + 41),
            (x_pantalla + 20, self.y + 38)
        ])
        
        # Decoraciones del vestido (bordado)
        for i in range(4):
            pygame.draw.circle(pantalla, BLANCO, (x_pantalla + 9 + i * 4, self.y + 40), 1)
        
        # ===== BRAZOS =====
        # Hombros abultados (manga globo)
        pygame.draw.circle(pantalla, color_rosa_vestido, (x_pantalla + 7, self.y + 30), 3)
        pygame.draw.circle(pantalla, color_rosa_vestido, (x_pantalla + 23, self.y + 30), 3)
        
        # Brazos (piel)
        pygame.draw.rect(pantalla, color_piel, (x_pantalla + 3, self.y + 32, 4, 6))
        pygame.draw.rect(pantalla, color_piel, (x_pantalla + 23, self.y + 32, 4, 6))
        
        # ===== GUANTES BLANCOS =====
        # Guante izquierdo
        pygame.draw.ellipse(pantalla, BLANCO, (x_pantalla + 2, self.y + 37, 6, 5))
        # Guante derecho
        pygame.draw.ellipse(pantalla, BLANCO, (x_pantalla + 22, self.y + 37, 6, 5))
        
        # Dedos (líneas simples)
        pygame.draw.line(pantalla, (220, 220, 220), (x_pantalla + 4, self.y + 39), (x_pantalla + 6, self.y + 39), 1)
        pygame.draw.line(pantalla, (220, 220, 220), (x_pantalla + 24, self.y + 39), (x_pantalla + 26, self.y + 39), 1)
        
        # ===== ZAPATOS =====
        # Zapatos rosas (estilo clásico)
        pygame.draw.ellipse(pantalla, color_rosa_vestido, (x_pantalla + 8, self.y + 40, 7, 4))
        pygame.draw.ellipse(pantalla, color_rosa_vestido, (x_pantalla + 15, self.y + 40, 7, 4))
        
        # Hebillas doradas
        pygame.draw.rect(pantalla, color_corona, (x_pantalla + 10, self.y + 41, 2, 2))
        pygame.draw.rect(pantalla, color_corona, (x_pantalla + 17, self.y + 41, 2, 2))
