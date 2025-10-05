from dataclasses import dataclass
from typing import List, Tuple, Optional
import pygame
from src.utils.constantes import *
from src.entities.enemigo import Enemigo
from src.entities.powerup import PowerUp
from src.entities.plataforma import Plataforma
from src.entities.moneda import Moneda
from src.entities.bandera import Bandera

@dataclass
class ColisionInfo:
    """Estructura de datos para información de colisiones."""
    arriba: bool = False
    abajo: bool = False
    izquierda: bool = False
    derecha: bool = False

class Mario(pygame.sprite.Sprite):
    """Clase que representa al personaje principal Mario."""
    
    # ...código existente de la clase Mario...

    def _detectar_colisiones(self, plataformas: List[pygame.sprite.Sprite]) -> ColisionInfo:
        """
        Detecta colisiones con plataformas y retorna la información de colisión.

        Args:
            plataformas: Lista de plataformas para verificar colisiones

        Returns:
            ColisionInfo: Estructura con información de colisiones en cada dirección
        """
        colisiones = ColisionInfo()
        
        # Movimiento horizontal
        self.rect.x += self.velocidad_x
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                if self.velocidad_x > 0:
                    self.rect.right = plataforma.rect.left
                    colisiones.derecha = True
                elif self.velocidad_x < 0:
                    self.rect.left = plataforma.rect.right
                    colisiones.izquierda = True
        
        # Movimiento vertical
        self.rect.y += self.velocidad_y
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                if self.velocidad_y > 0:
                    self.rect.bottom = plataforma.rect.top
                    colisiones.abajo = True
                    self.velocidad_y = 0
                    self.saltando = False
                elif self.velocidad_y < 0:
                    self.rect.top = plataforma.rect.bottom
                    colisiones.arriba = True
                    self.velocidad_y = 0
                    
                    # Golpear bloques
                    if plataforma.tipo == 'bloque' and not plataforma.golpeado:
                        plataforma.golpeado = True
        
        return colisiones

    def dibujar(self, superficie: pygame.Surface) -> None:
        """
        Dibuja a Mario en la superficie especificada.

        Args:
            superficie: Superficie de pygame donde se dibujará a Mario
        """
        if not self.vivo:
            return
            
        if self.invencible > 0 and self.invencible % 10 < 5:
            return
            
        self._dibujar_cuerpo(superficie)
        self._dibujar_detalles(superficie)
        
    def _dibujar_cuerpo(self, superficie: pygame.Surface) -> None:
        """
        Dibuja el cuerpo principal de Mario.

        Args:
            superficie: Superficie de pygame donde se dibujará
        """
        color_ropa = BLANCO if self.tiene_flor else ROJO
        
        # Cuerpo
        pygame.draw.rect(superficie, color_ropa, 
                        (self.rect.x + 8, self.rect.y + 10, 
                         16, self.alto - 10))
        
        # Cabeza
        pygame.draw.rect(superficie, color_ropa, 
                        (self.rect.x + 4, self.rect.y, 24, 10))
        
    def _dibujar_detalles(self, superficie: pygame.Surface) -> None:
        """
        Dibuja los detalles de Mario como ojos y ropa.

        Args:
            superficie: Superficie de pygame donde se dibujarán los detalles
        """
        # Ojos
        ojo_x = self.rect.x + (20 if self.direccion == 'derecha' else 8)
        pygame.draw.rect(superficie, NEGRO, 
                        (ojo_x, self.rect.y + 2, 4, 4))
        
        # Brazos
        brazo_x = self.rect.x + (24 if self.direccion == 'derecha' else 0)
        pygame.draw.rect(superficie, color_ropa, 
                        (brazo_x, self.rect.y + 12, 8, 8))
        
        # Animación de movimiento
        if self.velocidad_x != 0:
            self._animar_movimiento(superficie)
            
    def _animar_movimiento(self, superficie: pygame.Surface) -> None:
        """
        Aplica la animación de movimiento a Mario.

        Args:
            superficie: Superficie de pygame donde se dibujará la animación
        """
        pierna_x = self.rect.x + (8 if self.direccion == 'derecha' else 16)
        altura_pierna = abs(math.sin(self.animacion_frame * 0.5)) * 8
        
        pygame.draw.rect(superficie, AZUL, 
                        (pierna_x, self.rect.bottom - altura_pierna - 8, 
                         8, altura_pierna))

class Nivel:
    def __init__(self, numero):
        self.numero = numero
        self.plataformas = []
        self.enemigos = []
        self.monedas = []
        self.powerups = []
        self.bandera = None
        self.completado = False
        self.ancho_mapa = 3200
        self.crear_nivel()

    # ...resto del código de Nivel...
