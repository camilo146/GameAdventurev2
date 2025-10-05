"""
Clase Mario actualizada con sistema de estados, partículas y sonidos.
"""

import pygame
import math
from dataclasses import dataclass
from typing import List, Tuple, Optional
from src.utils.constantes import *
from src.utils.particulas import SistemaParticulas
from src.utils.sonidos import gestor_sonidos

@dataclass
class ColisionInfo:
    """Estructura de datos para información de colisiones."""
    arriba: bool = False
    abajo: bool = False
    izquierda: bool = False
    derecha: bool = False

class Mario(pygame.sprite.Sprite):
    """
    Clase que representa al personaje principal Mario con sistema de estados avanzado.
    
    Attributes:
        estado (EstadoMario): Estado actual de Mario
        ancho (int): Ancho del sprite de Mario
        alto (int): Alto del sprite de Mario
        rect (pygame.Rect): Rectángulo de colisión
        velocidad_x (float): Velocidad horizontal
        velocidad_y (float): Velocidad vertical
        saltando (bool): Estado de salto
        direccion (str): Dirección actual ('izquierda' o 'derecha')
        vivo (bool): Estado de vida
        invencible (int): Contador de invencibilidad
        particulas (SistemaParticulas): Sistema de partículas para efectos
    """
    
    # Constantes específicas de Mario
    VELOCIDAD_BASE: float = 5.0
    VELOCIDAD_CORRIENDO: float = 8.0
    ALTO_NORMAL: int = 32
    ALTO_GRANDE: int = 48
    TIEMPO_INVENCIBLE: int = 120
    TIEMPO_TRANSFORMACION: int = 60
    
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.estado = EstadoMario.PEQUENO
        self.ancho = 32
        self.alto = self.ALTO_NORMAL
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)
        self.velocidad_x = 0.0
        self.velocidad_y = 0.0
        self.saltando = False
        self.direccion = 'derecha'
        self.vivo = True
        self.invencible = 0
        self.animacion_frame = 0
        self.animacion_contador = 0
        self.particulas = SistemaParticulas()
        self.tiempo_transformacion = 0
        self.corriendo = False
        
        # Estados anteriores para transiciones
        self.estado_anterior = EstadoMario.PEQUENO
        
    def update(self, plataformas: List[pygame.sprite.Sprite]) -> None:
        """
        Actualiza el estado de Mario.
        
        Args:
            plataformas: Lista de plataformas para colisiones
        """
        if not self.vivo:
            self._manejar_muerte()
            return
            
        self._actualizar_animacion()
        self._actualizar_invencibilidad()
        self._actualizar_transformacion()
        self._aplicar_gravedad()
        self._manejar_entrada()
        self._actualizar_posicion(plataformas)
        self.particulas.update()
    
    def _actualizar_animacion(self) -> None:
        """Actualiza los frames de animación."""
        self.animacion_contador += 1
        velocidad_animacion = 3 if self.corriendo else 5
        
        if self.animacion_contador > velocidad_animacion:
            self.animacion_frame = (self.animacion_frame + 1) % 4
            self.animacion_contador = 0
    
    def _actualizar_invencibilidad(self) -> None:
        """Actualiza el contador de invencibilidad."""
        if self.invencible > 0:
            self.invencible -= 1
            if self.invencible == 0 and self.estado == EstadoMario.INVENCIBLE:
                self._cambiar_estado(self.estado_anterior)
    
    def _actualizar_transformacion(self) -> None:
        """Actualiza el proceso de transformación."""
        if self.tiempo_transformacion > 0:
            self.tiempo_transformacion -= 1
            # Efecto de parpadeo durante transformación
            if self.tiempo_transformacion % 10 == 0:
                self.particulas.crear_efecto(self.rect.centerx, self.rect.centery, 'powerup')
    
    def _aplicar_gravedad(self) -> None:
        """Aplica la gravedad al movimiento vertical."""
        if self.estado != EstadoMario.MURIENDO:
            self.velocidad_y += GRAVEDAD
            self.velocidad_y = min(self.velocidad_y, 15)
    
    def _manejar_entrada(self) -> None:
        """Maneja la entrada del teclado para el movimiento."""
        if self.estado == EstadoMario.MURIENDO:
            return
            
        teclas = pygame.key.get_pressed()
        self.velocidad_x = 0
        self.corriendo = teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT]
        
        velocidad_actual = self.VELOCIDAD_CORRIENDO if self.corriendo else self.VELOCIDAD_BASE
        
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.velocidad_x = -velocidad_actual
            self.direccion = 'izquierda'
        elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.velocidad_x = velocidad_actual
            self.direccion = 'derecha'
    
    def _manejar_muerte(self) -> None:
        """Maneja la lógica cuando Mario está muriendo."""
        self.velocidad_y += GRAVEDAD * 0.5
        if self.rect.y > ALTO + 100:
            # Mario ha caído fuera de la pantalla
            pass
    
    def saltar(self) -> None:
        """Hace que Mario salte si está en el suelo."""
        if not self.saltando and self.vivo and self.estado != EstadoMario.MURIENDO:
            # Mario grande/fuego salta más alto
            multiplicador = 1.3 if self.estado in [EstadoMario.GRANDE, EstadoMario.FUEGO] else 1.0
            fuerza_base = FUERZA_SALTO * multiplicador
            fuerza = fuerza_base * 1.2 if self.corriendo else fuerza_base
            self.velocidad_y = -fuerza
            self.saltando = True
            
            # Efectos de salto
            gestor_sonidos.reproducir_efecto('salto')
            self.particulas.crear_efecto(self.rect.centerx, self.rect.bottom, 'salto')
    
    def _cambiar_estado(self, nuevo_estado: EstadoMario) -> None:
        """
        Cambia el estado de Mario.
        
        Args:
            nuevo_estado: El nuevo estado a establecer
        """
        if self.estado != nuevo_estado:
            self.estado_anterior = self.estado
            self.estado = nuevo_estado
            self._aplicar_cambio_estado()
    
    def _aplicar_cambio_estado(self) -> None:
        """Aplica los cambios necesarios según el nuevo estado."""
        if self.estado == EstadoMario.GRANDE or self.estado == EstadoMario.FUEGO:
            if self.alto == self.ALTO_NORMAL:
                self.alto = self.ALTO_GRANDE
                self.rect.height = self.ALTO_GRANDE
                self.rect.y -= 16
        elif self.estado == EstadoMario.PEQUENO:
            if self.alto == self.ALTO_GRANDE:
                self.alto = self.ALTO_NORMAL
                self.rect.height = self.ALTO_NORMAL
        elif self.estado == EstadoMario.INVENCIBLE:
            self.invencible = self.TIEMPO_INVENCIBLE
        elif self.estado == EstadoMario.MURIENDO:
            self.velocidad_x = 0
            self.velocidad_y = -8
            self.vivo = False
            gestor_sonidos.reproducir_efecto('muerte')
            self.particulas.crear_explosion(self.rect.centerx, self.rect.centery, ROJO)
    
    def recibir_dano(self) -> bool:
        """
        Procesa el daño recibido por Mario.
        
        Returns:
            bool: True si Mario muere, False si sobrevive
        """
        if self.invencible > 0 or self.estado == EstadoMario.INVENCIBLE:
            return False
            
        if self.estado == EstadoMario.FUEGO:
            self._cambiar_estado(EstadoMario.GRANDE)
            self.invencible = self.TIEMPO_INVENCIBLE
            self.tiempo_transformacion = self.TIEMPO_TRANSFORMACION
            return False
        elif self.estado == EstadoMario.GRANDE:
            self._cambiar_estado(EstadoMario.PEQUENO)
            self.invencible = self.TIEMPO_INVENCIBLE
            self.tiempo_transformacion = self.TIEMPO_TRANSFORMACION
            return False
        else:
            self._cambiar_estado(EstadoMario.MURIENDO)
            return True
    
    def obtener_powerup(self, tipo: TipoPowerUp) -> None:
        """
        Aplica un power-up a Mario.
        
        Args:
            tipo: Tipo de power-up obtenido
        """
        gestor_sonidos.reproducir_efecto('powerup')
        self.tiempo_transformacion = self.TIEMPO_TRANSFORMACION
        
        if tipo == TipoPowerUp.HONGO:
            if self.estado == EstadoMario.PEQUENO:
                self._cambiar_estado(EstadoMario.GRANDE)
        elif tipo == TipoPowerUp.FLOR:
            self._cambiar_estado(EstadoMario.FUEGO)
        elif tipo == TipoPowerUp.ESTRELLA:
            self.estado_anterior = self.estado
            self._cambiar_estado(EstadoMario.INVENCIBLE)
    
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
                    if hasattr(plataforma, 'tipo') and plataforma.tipo == 'bloque' and not plataforma.golpeado:
                        plataforma.golpeado = True
                        self.particulas.crear_efecto(plataforma.rect.centerx, plataforma.rect.centery, 'powerup')
                        # Notificar al juego que se golpeó un bloque (se manejará en la clase Juego)
                        if hasattr(plataforma, 'contiene_powerup'):
                            plataforma.contiene_powerup = True
        
        return colisiones
    
    def _actualizar_posicion(self, plataformas: List[pygame.sprite.Sprite]) -> None:
        """
        Actualiza la posición de Mario manejando colisiones.
        
        Args:
            plataformas: Lista de plataformas para verificar colisiones
        """
        self._detectar_colisiones(plataformas)
        
        # Límites de pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        # Eliminar límite derecho - permitir moverse por todo el mapa
            
        # Muerte por caída
        if self.rect.y > ALTO and self.vivo:
            self._cambiar_estado(EstadoMario.MURIENDO)

    def dibujar(self, superficie: pygame.Surface) -> None:
        """
        Dibuja a Mario en la superficie especificada.

        Args:
            superficie: Superficie de pygame donde se dibujará a Mario
        """
        # Dibujar partículas primero (detrás de Mario)
        self.particulas.dibujar(superficie)
        
        if not self.vivo and self.estado != EstadoMario.MURIENDO:
            return
            
        # Efecto de parpadeo para invencibilidad
        if (self.invencible > 0 or self.tiempo_transformacion > 0) and (self.invencible + self.tiempo_transformacion) % 10 < 5:
            return
            
        self._dibujar_cuerpo(superficie)
        self._dibujar_detalles(superficie)
        
    def _dibujar_cuerpo(self, superficie: pygame.Surface) -> None:
        """
        Dibuja el cuerpo principal de Mario.

        Args:
            superficie: Superficie de pygame donde se dibujará
        """
        # Determinar color según estado
        if self.estado == EstadoMario.FUEGO:
            color_ropa = BLANCO
            color_secundario = ROJO
        elif self.estado == EstadoMario.INVENCIBLE:
            # Efecto arcoíris para estado invencible
            frame_color = (self.animacion_frame * 60) % 360
            import colorsys
            rgb = colorsys.hsv_to_rgb(frame_color / 360.0, 1.0, 1.0)
            color_ropa = tuple(int(c * 255) for c in rgb)
            color_secundario = BLANCO
        else:
            color_ropa = ROJO
            color_secundario = AZUL
        
        # Dibujar Mario estilo pixel art más fiel al original
        x, y = self.rect.x, self.rect.y
        color_piel = (255, 220, 177)  # Color piel
        
        # Cabeza (círculo más grande y piel)
        pygame.draw.circle(superficie, color_piel, (x + 16, y + 8), 10)
        
        # Gorra roja (característica de Mario)
        pygame.draw.circle(superficie, color_ropa, (x + 16, y + 6), 8)
        
        # Visera de la gorra
        pygame.draw.rect(superficie, color_ropa, (x + 8, y + 8, 16, 4))
        
        # Cuerpo - Camisa
        pygame.draw.rect(superficie, color_ropa, (x + 10, y + 14, 12, 8))
        
        # Overol (pantalones azules con tirantes)
        pygame.draw.rect(superficie, color_secundario, (x + 10, y + 22, 12, 10))
        
        # Tirantes del overol
        pygame.draw.line(superficie, color_secundario, (x + 12, y + 16), (x + 12, y + 22), 2)
        pygame.draw.line(superficie, color_secundario, (x + 20, y + 16), (x + 20, y + 22), 2)
        
        # Botones dorados del overol
        pygame.draw.circle(superficie, AMARILLO, (x + 12, y + 18), 1)
        pygame.draw.circle(superficie, AMARILLO, (x + 20, y + 18), 1)
        
        # Brazos (color piel)
        if self.direccion == 'derecha':
            pygame.draw.rect(superficie, color_piel, (x + 22, y + 16, 4, 6))
            pygame.draw.rect(superficie, color_piel, (x + 6, y + 18, 4, 4))
        else:
            pygame.draw.rect(superficie, color_piel, (x + 6, y + 16, 4, 6))
            pygame.draw.rect(superficie, color_piel, (x + 22, y + 18, 4, 4))
        
        # Zapatos marrones (más grandes si es Mario grande)
        zapato_height = 4 if self.estado == EstadoMario.PEQUENO else 6
        pygame.draw.rect(superficie, MARRON, (x + 8, y + self.alto - zapato_height, 6, zapato_height))
        pygame.draw.rect(superficie, MARRON, (x + 18, y + self.alto - zapato_height, 6, zapato_height))
        
    def _dibujar_detalles(self, superficie: pygame.Surface) -> None:
        """
        Dibuja los detalles de Mario como ojos, bigote y extremidades.

        Args:
            superficie: Superficie de pygame donde se dibujarán los detalles
        """
        x, y = self.rect.x, self.rect.y
        
        # Ojos (dos puntos negros)
        if self.direccion == 'derecha':
            pygame.draw.circle(superficie, NEGRO, (x + 12, y + 8), 1)
            pygame.draw.circle(superficie, NEGRO, (x + 18, y + 8), 1)
        else:
            pygame.draw.circle(superficie, NEGRO, (x + 14, y + 8), 1)
            pygame.draw.circle(superficie, NEGRO, (x + 20, y + 8), 1)
        
        # Bigote (línea negra característica)
        pygame.draw.rect(superficie, NEGRO, (x + 14, y + 10, 4, 2))
        
        # Letra "M" en la gorra (detalle adicional)
        pygame.draw.circle(superficie, BLANCO, (x + 16, y + 6), 3)
        # Pequeña "M" pixelada
        pygame.draw.rect(superficie, ROJO, (x + 15, y + 5, 1, 2))
        pygame.draw.rect(superficie, ROJO, (x + 17, y + 5, 1, 2))
        pygame.draw.rect(superficie, ROJO, (x + 16, y + 5, 1, 1))
        
        # Bigote
        bigote_x = self.rect.x + (16 if self.direccion == 'derecha' else 12)
        pygame.draw.rect(superficie, NEGRO, (bigote_x, self.rect.y + 10, 8, 2))
        
        # Brazos
        brazo_x = self.rect.x + (26 if self.direccion == 'derecha' else 0)
        pygame.draw.rect(superficie, AMARILLO, (brazo_x, self.rect.y + 16, 6, 12))
        
        # Piernas con animación
        if abs(self.velocidad_x) > 0:
            self._animar_piernas(superficie)
        else:
            # Piernas estáticas
            pygame.draw.rect(superficie, AMARILLO, 
                           (self.rect.x + 10, self.rect.bottom - 12, 4, 12))
            pygame.draw.rect(superficie, AMARILLO, 
                           (self.rect.x + 18, self.rect.bottom - 12, 4, 12))
            
    def _animar_piernas(self, superficie: pygame.Surface) -> None:
        """
        Aplica la animación de movimiento a las piernas de Mario.

        Args:
            superficie: Superficie de pygame donde se dibujará la animación
        """
        # Animación más suave basada en seno
        offset_izq = int(math.sin(self.animacion_frame * 0.8) * 3)
        offset_der = int(math.sin(self.animacion_frame * 0.8 + math.pi) * 3)
        
        # Pierna izquierda
        pygame.draw.rect(superficie, AMARILLO, 
                        (self.rect.x + 10, self.rect.bottom - 12 + offset_izq, 4, 12 - abs(offset_izq)))
        
        # Pierna derecha
        pygame.draw.rect(superficie, AMARILLO, 
                        (self.rect.x + 18, self.rect.bottom - 12 + offset_der, 4, 12 - abs(offset_der)))
    
    def obtener_estado(self) -> EstadoMario:
        """
        Retorna el estado actual de Mario.
        
        Returns:
            EstadoMario: Estado actual
        """
        return self.estado
    
    def es_invencible(self) -> bool:
        """
        Verifica si Mario está en estado invencible.
        
        Returns:
            bool: True si está invencible
        """
        return self.estado == EstadoMario.INVENCIBLE or self.invencible > 0