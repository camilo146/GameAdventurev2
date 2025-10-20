"""
Clase Mario actualizada con sistema de estados, partículas y sonidos.
"""

import pygame
import math
from dataclasses import dataclass
from typing import List, Tuple, Optional, TYPE_CHECKING
from src.utils.constantes import *
from src.utils.particulas import SistemaParticulas
from src.utils.sonidos import gestor_sonidos

if TYPE_CHECKING:
    from src.entities.bola_fuego import BolaFuego

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
    TIEMPO_INVENCIBLE: int = 480  # 8 segundos de invencibilidad (60 FPS * 8)
    TIEMPO_TRANSFORMACION: int = 60
    TIEMPO_POWER_UP_GRANDE: int = 480  # 8 segundos de estado GRANDE (60 FPS * 8)
    TIEMPO_POWER_UP_FUEGO: int = 600  # 10 segundos de estado FUEGO (60 FPS * 10)
    
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
        self.tiempo_power_up_grande = 0  # Temporizador para estado GRANDE temporal
        self.tiempo_power_up_fuego = 0  # Temporizador para estado FUEGO temporal
        
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
        self._actualizar_power_up_grande()  # Nuevo: actualizar temporizador de estado GRANDE
        self._actualizar_power_up_fuego()  # Nuevo: actualizar temporizador de estado FUEGO
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
    
    def _actualizar_power_up_grande(self) -> None:
        """Actualiza el temporizador del estado GRANDE temporal."""
        # Solo aplicar si Mario está en estado GRANDE (no FUEGO ni INVENCIBLE)
        if self.estado == EstadoMario.GRANDE and self.tiempo_power_up_grande > 0:
            self.tiempo_power_up_grande -= 1
            
            # Advertencia visual cuando quedan 2 segundos (120 frames)
            if self.tiempo_power_up_grande <= 120 and self.tiempo_power_up_grande % 20 == 0:
                self.particulas.crear_efecto(self.rect.centerx, self.rect.centery, 'advertencia')
            
            # Cuando se acaba el tiempo, volver a PEQUEÑO
            if self.tiempo_power_up_grande == 0:
                self._cambiar_estado(EstadoMario.PEQUENO)
                self.tiempo_transformacion = self.TIEMPO_TRANSFORMACION
                gestor_sonidos.reproducir_efecto('powerup')  # Sonido de transformación
    
    def _actualizar_power_up_fuego(self) -> None:
        """Actualiza el temporizador del estado FUEGO temporal."""
        # Solo aplicar si Mario está en estado FUEGO
        if self.estado == EstadoMario.FUEGO and self.tiempo_power_up_fuego > 0:
            self.tiempo_power_up_fuego -= 1
            
            # Advertencia visual cuando quedan 3 segundos (180 frames)
            if self.tiempo_power_up_fuego <= 180 and self.tiempo_power_up_fuego % 20 == 0:
                self.particulas.crear_efecto(self.rect.centerx, self.rect.centery, 'advertencia')
            
            # Cuando se acaba el tiempo, volver al estado anterior (PEQUEÑO)
            if self.tiempo_power_up_fuego == 0:
                self._cambiar_estado(EstadoMario.PEQUENO)
                self.tiempo_transformacion = self.TIEMPO_TRANSFORMACION
                gestor_sonidos.reproducir_efecto('powerup')  # Sonido de transformación
    
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
        # Aplicar gravedad reducida durante muerte
        self.velocidad_y += GRAVEDAD * 0.5
        # LIMITAR la velocidad de caída para evitar valores extremos
        self.velocidad_y = min(self.velocidad_y, 15)
        # Actualizar posición vertical
        self.rect.y += int(self.velocidad_y)
        
        if self.rect.y > ALTO + 100:
            # Mario ha caído fuera de la pantalla, marcar como completamente muerto
            self.vivo = False
    
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
    
    def lanzar_fuego(self) -> Optional['BolaFuego']:
        """
        Lanza una bola de fuego si Mario tiene el poder de fuego.
        
        Returns:
            BolaFuego si se puede lanzar, None si no
        """
        if self.estado == EstadoMario.FUEGO and self.vivo and self.estado != EstadoMario.MURIENDO:
            from src.entities.bola_fuego import BolaFuego
            
            # Posición de lanzamiento
            offset_x = 20 if self.direccion == 'derecha' else -20
            x = self.rect.centerx + offset_x
            y = self.rect.centery
            
            # Crear bola de fuego
            bola = BolaFuego(x, y, self.direccion)
            
            # Efectos visuales y sonoros
            self.particulas.crear_efecto(x, y, 'fuego')
            gestor_sonidos.reproducir_efecto('powerup')
            
            return bola
        
        return None
    
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
        if self.estado == EstadoMario.GRANDE:
            # Solo el estado GRANDE cambia el tamaño
            if self.alto == self.ALTO_NORMAL:
                self.alto = self.ALTO_GRANDE
                self.rect.height = self.ALTO_GRANDE
                self.rect.y -= 16
        elif self.estado == EstadoMario.FUEGO:
            # El estado FUEGO NO cambia el tamaño, solo da habilidad de lanzar fuego
            # Mario mantiene su tamaño actual (PEQUENO o GRANDE)
            pass
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
        # No recibir daño si ya está muriendo o muerto
        if not self.vivo or self.estado == EstadoMario.MURIENDO:
            return False
            
        if self.invencible > 0 or self.estado == EstadoMario.INVENCIBLE:
            return False
            
        if self.estado == EstadoMario.FUEGO:
            # Al recibir daño con fuego, solo pierde el poder (vuelve a PEQUEÑO)
            self._cambiar_estado(EstadoMario.PEQUENO)
            self.invencible = self.TIEMPO_INVENCIBLE
            self.tiempo_transformacion = self.TIEMPO_TRANSFORMACION
            self.tiempo_power_up_fuego = 0  # Cancelar temporizador de fuego
            # Efecto visual de daño
            self.particulas.crear_efecto(self.rect.centerx, self.rect.centery, 'enemigo')
            gestor_sonidos.reproducir_efecto('powerup')  # Sonido de transformación
            return False
        elif self.estado == EstadoMario.GRANDE:
            self._cambiar_estado(EstadoMario.PEQUENO)
            self.invencible = self.TIEMPO_INVENCIBLE
            self.tiempo_transformacion = self.TIEMPO_TRANSFORMACION
            self.tiempo_power_up_grande = 0  # Cancelar temporizador de estado GRANDE
            # Efecto visual de daño
            self.particulas.crear_efecto(self.rect.centerx, self.rect.centery, 'enemigo')
            gestor_sonidos.reproducir_efecto('powerup')  # Sonido de transformación
            return False
        else:
            # Mario pequeño muere
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
                self.tiempo_power_up_grande = self.TIEMPO_POWER_UP_GRANDE  # 8 segundos temporales
            elif self.estado == EstadoMario.GRANDE:
                # Si ya es grande, renovar el tiempo
                self.tiempo_power_up_grande = self.TIEMPO_POWER_UP_GRANDE
        elif tipo == TipoPowerUp.FLOR:
            # La flor NO hace crecer a Mario, solo le da poder de fuego temporal
            self._cambiar_estado(EstadoMario.FUEGO)
            self.tiempo_power_up_fuego = self.TIEMPO_POWER_UP_FUEGO  # 10 segundos temporales
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
        # Nota: La muerte por caída se maneja en la clase Juego

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
        Dibuja el cuerpo principal de Mario - Estilo clásico NES mejorado.

        Args:
            superficie: Superficie de pygame donde se dibujará
        """
        # Determinar colores según estado
        if self.estado == EstadoMario.FUEGO:
            color_camisa = BLANCO
            color_overol = ROJO
        elif self.estado == EstadoMario.INVENCIBLE:
            # Efecto arcoíris para estado invencible
            frame_color = (self.animacion_frame * 60) % 360
            import colorsys
            rgb = colorsys.hsv_to_rgb(frame_color / 360.0, 1.0, 1.0)
            color_camisa = tuple(int(c * 255) for c in rgb)
            color_overol = BLANCO
        else:
            color_camisa = ROJO
            color_overol = (0, 0, 200)  # Azul overol más oscuro
        
        x, y = self.rect.x, self.rect.y
        color_piel = (255, 206, 165)  # Color piel más fiel al original
        color_gorra = color_camisa
        
        # === GORRA ROJA ===
        # Base de la gorra (más grande y prominente)
        pygame.draw.rect(superficie, color_gorra, (x + 8, y + 2, 16, 6))
        # Visera de la gorra (saliente)
        pygame.draw.rect(superficie, color_gorra, (x + 6, y + 7, 20, 3))
        # Sombra de la visera
        pygame.draw.rect(superficie, (150, 0, 0), (x + 6, y + 9, 20, 1))
        
        # Símbolo "M" en la gorra (círculo blanco)
        pygame.draw.circle(superficie, BLANCO, (x + 16, y + 5), 3)
        # Letra "M" roja dentro
        pygame.draw.rect(superficie, color_gorra, (x + 14, y + 4, 1, 3))
        pygame.draw.rect(superficie, color_gorra, (x + 16, y + 4, 1, 2))
        pygame.draw.rect(superficie, color_gorra, (x + 18, y + 4, 1, 3))
        
        # === CARA Y CABELLO ===
        # Cabello marrón oscuro (asoma por los lados)
        pygame.draw.rect(superficie, (101, 67, 33), (x + 7, y + 8, 2, 3))
        pygame.draw.rect(superficie, (101, 67, 33), (x + 23, y + 8, 2, 3))
        
        # Cara (piel)
        pygame.draw.rect(superficie, color_piel, (x + 9, y + 10, 14, 8))
        
        # Ojos (dos puntos negros)
        ojo_offset = 2 if self.direccion == 'derecha' else -2
        pygame.draw.rect(superficie, NEGRO, (x + 12 + ojo_offset, y + 12, 2, 2))
        pygame.draw.rect(superficie, NEGRO, (x + 17 + ojo_offset, y + 12, 2, 2))
        
        # Nariz (pequeño rectángulo)
        pygame.draw.rect(superficie, (220, 150, 100), (x + 15, y + 14, 2, 3))
        
        # BIGOTE NEGRO PROMINENTE (característica icónica)
        pygame.draw.rect(superficie, NEGRO, (x + 11, y + 16, 3, 2))
        pygame.draw.rect(superficie, NEGRO, (x + 18, y + 16, 3, 2))
        pygame.draw.rect(superficie, NEGRO, (x + 14, y + 17, 4, 1))
        
        # === CUERPO - CAMISA ROJA ===
        pygame.draw.rect(superficie, color_camisa, (x + 10, y + 18, 12, 6))
        
        # === OVEROL AZUL ===
        # Pantalones
        pygame.draw.rect(superficie, color_overol, (x + 9, y + 24, 14, 4))
        
        # Tirantes del overol (característicos)
        pygame.draw.rect(superficie, color_overol, (x + 11, y + 18, 2, 6))
        pygame.draw.rect(superficie, color_overol, (x + 19, y + 18, 2, 6))
        
        # Botones dorados grandes (más visibles)
        pygame.draw.circle(superficie, AMARILLO, (x + 12, y + 20), 2)
        pygame.draw.circle(superficie, AMARILLO, (x + 20, y + 20), 2)
        pygame.draw.rect(superficie, (200, 180, 0), (x + 11, y + 20, 2, 1))  # Brillo
        pygame.draw.rect(superficie, (200, 180, 0), (x + 19, y + 20, 2, 1))
        
        # === GUANTES BLANCOS (brazos) ===
        if self.direccion == 'derecha':
            # Brazo derecho adelante
            pygame.draw.rect(superficie, color_piel, (x + 23, y + 20, 3, 4))
            pygame.draw.rect(superficie, BLANCO, (x + 23, y + 24, 4, 3))  # Guante
            # Brazo izquierdo atrás
            pygame.draw.rect(superficie, color_piel, (x + 5, y + 21, 3, 3))
            pygame.draw.rect(superficie, BLANCO, (x + 4, y + 24, 4, 2))  # Guante
        else:
            # Brazo izquierdo adelante
            pygame.draw.rect(superficie, color_piel, (x + 6, y + 20, 3, 4))
            pygame.draw.rect(superficie, BLANCO, (x + 5, y + 24, 4, 3))  # Guante
            # Brazo derecho atrás
            pygame.draw.rect(superficie, color_piel, (x + 24, y + 21, 3, 3))
            pygame.draw.rect(superficie, BLANCO, (x + 24, y + 24, 4, 2))  # Guante
        
        # === ZAPATOS MARRONES GRANDES ===
        zapato_y = y + self.alto - 4
        # Zapato izquierdo
        pygame.draw.rect(superficie, (101, 67, 33), (x + 8, zapato_y, 7, 4))
        pygame.draw.rect(superficie, (70, 45, 20), (x + 8, zapato_y + 3, 7, 1))  # Suela
        # Zapato derecho
        pygame.draw.rect(superficie, (101, 67, 33), (x + 17, zapato_y, 7, 4))
        pygame.draw.rect(superficie, (70, 45, 20), (x + 17, zapato_y + 3, 7, 1))  # Suela
        
    def _dibujar_detalles(self, superficie: pygame.Surface) -> None:
        """
        Dibuja detalles adicionales y animaciones de piernas.

        Args:
            superficie: Superficie de pygame donde se dibujarán los detalles
        """
        # Animación de piernas al caminar
        if abs(self.velocidad_x) > 0.5:
            self._animar_piernas(superficie)
            
    def _animar_piernas(self, superficie: pygame.Surface) -> None:
        """
        Aplica la animación de movimiento a las piernas/zapatos de Mario.

        Args:
            superficie: Superficie de pygame donde se dibujará la animación
        """
        # Animación de caminar - alternancia de piernas
        x, y = self.rect.x, self.rect.y
        
        # Determinar fase de animación (0-3)
        fase = self.animacion_frame % 4
        
        # Color overol
        color_overol = (0, 0, 200) if self.estado != EstadoMario.FUEGO else ROJO
        
        if fase == 0 or fase == 2:
            # Posición neutra
            # Piernas (overol azul)
            pygame.draw.rect(superficie, color_overol, (x + 10, y + 28, 4, 2))
            pygame.draw.rect(superficie, color_overol, (x + 18, y + 28, 4, 2))
            
        elif fase == 1:
            # Pierna izquierda adelante, derecha atrás
            pygame.draw.rect(superficie, color_overol, (x + 10, y + 27, 4, 3))
            pygame.draw.rect(superficie, color_overol, (x + 18, y + 29, 4, 1))
            
        else:  # fase == 3
            # Pierna derecha adelante, izquierda atrás  
            pygame.draw.rect(superficie, color_overol, (x + 10, y + 29, 4, 1))
            pygame.draw.rect(superficie, color_overol, (x + 18, y + 27, 4, 3))
    
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