"""
Entidad Puerta para el sistema de quiz de inglés.
Incluye puertas obligatorias, opcionales y especiales.
"""

import pygame
from typing import Optional
from src.utils.preguntas import TipoPuerta

class Puerta:
    def __init__(self, x: int, y: int, tipo: TipoPuerta, llaves_requeridas: int = 0):
        """
        Inicializa una puerta.
        
        Args:
            x, y: Posición de la puerta
            tipo: Tipo de puerta (obligatoria, opcional, etc.)
            llaves_requeridas: Número de llaves necesarias para intentar abrirla
        """
        self.rect = pygame.Rect(x, y, 60, 80)  # Puerta de 60x80 píxeles
        self.tipo = tipo
        self.llaves_requeridas = llaves_requeridas
        self.abierta = False
        self.bloqueada = True  # Inicialmente bloqueada
        
        # Animación
        self.frame_animacion = 0
        self.animando_apertura = False
        self.tiempo_animacion = 0
        
        # Efectos visuales
        self.brillo_activo = False
        self.tiempo_brillo = 0
        
        # Colores según tipo
        self._definir_colores()
        
    def _definir_colores(self):
        """Define los colores según el tipo de puerta."""
        if self.tipo == TipoPuerta.OBLIGATORIA:
            self.color_puerta = (139, 69, 19)      # Marrón oscuro
            self.color_marco = (101, 67, 33)       # Marrón más oscuro
            self.color_candado = (255, 215, 0)     # Dorado
            self.color_brillo = (255, 255, 255)    # Blanco
            
        elif self.tipo == TipoPuerta.OPCIONAL_SECRETA:
            self.color_puerta = (75, 0, 130)       # Púrpura oscuro
            self.color_marco = (50, 0, 80)         # Púrpura más oscuro
            self.color_candado = (255, 20, 147)    # Rosa fuerte
            self.color_brillo = (255, 0, 255)      # Magenta
            
        elif self.tipo == TipoPuerta.OPCIONAL_BONUS:
            self.color_puerta = (0, 100, 0)        # Verde oscuro
            self.color_marco = (0, 80, 0)          # Verde más oscuro
            self.color_candado = (50, 205, 50)     # Verde lima
            self.color_brillo = (0, 255, 0)        # Verde brillante
            
        elif self.tipo == TipoPuerta.LLAVE_ESPECIAL:
            self.color_puerta = (255, 140, 0)      # Naranja oscuro
            self.color_marco = (255, 69, 0)        # Rojo naranja
            self.color_candado = (255, 215, 0)     # Dorado
            self.color_brillo = (255, 255, 0)      # Amarillo brillante
            
    def update(self):
        """Actualiza la animación de la puerta."""
        self.frame_animacion += 1
        
        # Animación de apertura
        if self.animando_apertura:
            self.tiempo_animacion += 1
            if self.tiempo_animacion >= 60:  # 1 segundo a 60 FPS
                self.animando_apertura = False  # Solo termina la animación
                
        # Efecto de brillo cuando está activa
        if self.brillo_activo:
            self.tiempo_brillo = (self.tiempo_brillo + 1) % 120  # Ciclo de 2 segundos
            
    def activar_brillo(self):
        """Activa el efecto de brillo cuando Mario está cerca."""
        self.brillo_activo = True
        
    def desactivar_brillo(self):
        """Desactiva el efecto de brillo."""
        self.brillo_activo = False
        self.tiempo_brillo = 0
        
    def abrir(self):
        """Inicia la animación de apertura de la puerta."""
        if not self.abierta and not self.animando_apertura:
            self.abierta = True  # Marcar como abierta inmediatamente
            self.animando_apertura = True
            self.tiempo_animacion = 0
            self.bloqueada = False
            
    def puede_intentar_abrir(self, llaves_jugador: int) -> bool:
        """
        Verifica si el jugador puede intentar abrir la puerta.
        
        Args:
            llaves_jugador: Número de llaves que tiene el jugador
            
        Returns:
            True si puede intentar abrirla, False si no
        """
        if self.abierta:
            return False
        return llaves_jugador >= self.llaves_requeridas
        
    def get_rect(self) -> pygame.Rect:
        """Obtiene el rectángulo de colisión de la puerta."""
        return self.rect
        
    def bloquea_paso(self) -> bool:
        """
        Verifica si la puerta bloquea físicamente el paso.
        
        Returns:
            True si la puerta está cerrada y bloquea el paso
        """
        return not self.abierta and self.bloqueada
        
    def get_rect_colision(self) -> pygame.Rect:
        """
        Obtiene el rectángulo de colisión para bloqueo físico.
        Solo existe si la puerta está cerrada.
        
        Returns:
            pygame.Rect si bloquea el paso, None si está abierta
        """
        if self.bloquea_paso():
            return self.rect
        return None
        
    def dibujar(self, superficie: pygame.Surface, camara_x: int):
        """
        Dibuja la puerta en la superficie.
        
        Args:
            superficie: Superficie donde dibujar
            camara_x: Posición X de la cámara para el scroll
        """
        if self.abierta:
            return  # No dibujar si está abierta
            
        # Posición ajustada por la cámara
        x = self.rect.x - camara_x
        y = self.rect.y
        
        # No dibujar si está fuera de la pantalla
        if x < -self.rect.width or x > 800:
            return
            
        # Calcular efecto de brillo
        intensidad_brillo = 0
        if self.brillo_activo:
            intensidad_brillo = abs(60 - self.tiempo_brillo) / 60.0 * 0.3
            
        # Colores ajustados por brillo
        color_puerta = self._ajustar_color_brillo(self.color_puerta, intensidad_brillo)
        color_marco = self._ajustar_color_brillo(self.color_marco, intensidad_brillo)
        color_candado = self._ajustar_color_brillo(self.color_candado, intensidad_brillo)
        
        # Si está animando la apertura, aplicar efecto
        if self.animando_apertura:
            apertura_progreso = self.tiempo_animacion / 60.0
            # La puerta se "desvanece" gradualmente
            alpha = int(255 * (1 - apertura_progreso))
            # Crear superficie temporal para transparencia
            temp_surface = pygame.Surface((self.rect.width, self.rect.height))
            temp_surface.set_alpha(alpha)
            self._dibujar_puerta_completa(temp_surface, 0, 0, color_puerta, color_marco, color_candado)
            superficie.blit(temp_surface, (x, y))
        else:
            self._dibujar_puerta_completa(superficie, x, y, color_puerta, color_marco, color_candado)
            
    def _ajustar_color_brillo(self, color, intensidad):
        """Ajusta un color aplicando brillo."""
        if intensidad <= 0:
            return color
            
        r, g, b = color
        brillo_r, brillo_g, brillo_b = self.color_brillo
        
        # Mezclar con el color de brillo
        r = min(255, int(r + (brillo_r - r) * intensidad))
        g = min(255, int(g + (brillo_g - g) * intensidad))
        b = min(255, int(b + (brillo_b - b) * intensidad))
        
        return (r, g, b)
        
    def _dibujar_puerta_completa(self, superficie, x, y, color_puerta, color_marco, color_candado):
        """Dibuja la puerta completa en las coordenadas especificadas."""
        # Marco exterior
        pygame.draw.rect(superficie, color_marco, (x, y, self.rect.width, self.rect.height))
        
        # Puerta interior
        margen = 4
        pygame.draw.rect(superficie, color_puerta, 
                        (x + margen, y + margen, 
                         self.rect.width - 2*margen, self.rect.height - 2*margen))
        
        # Paneles decorativos de la puerta
        panel_w = (self.rect.width - 3*margen) // 2
        panel_h = (self.rect.height - 4*margen) // 3
        
        # Panel superior izquierdo
        pygame.draw.rect(superficie, self._oscurecer_color(color_puerta, 0.2),
                        (x + margen*2, y + margen*2, panel_w, panel_h), 2)
        
        # Panel superior derecho
        pygame.draw.rect(superficie, self._oscurecer_color(color_puerta, 0.2),
                        (x + margen*2 + panel_w + margen, y + margen*2, panel_w, panel_h), 2)
        
        # Panel inferior (más grande)
        pygame.draw.rect(superficie, self._oscurecer_color(color_puerta, 0.2),
                        (x + margen*2, y + margen*3 + panel_h, 
                         self.rect.width - 4*margen, panel_h*2 - margen), 2)
        
        # Manija de la puerta
        manija_x = x + self.rect.width - margen*3
        manija_y = y + self.rect.height // 2
        pygame.draw.circle(superficie, self._oscurecer_color(color_candado, 0.3), 
                          (manija_x, manija_y), 4)
        pygame.draw.circle(superficie, color_candado, (manija_x, manija_y), 3)
        
        # Candado (si está bloqueada)
        if self.bloqueada:
            self._dibujar_candado(superficie, x + self.rect.width//2, y + self.rect.height//2, color_candado)
            
        # Indicador del tipo de puerta
        self._dibujar_indicador_tipo(superficie, x, y)
        
        # Indicador de llaves requeridas
        if self.llaves_requeridas > 0:
            self._dibujar_indicador_llaves(superficie, x, y + self.rect.height - 20)
            
    def _dibujar_candado(self, superficie, centro_x, centro_y, color):
        """Dibuja un candado en el centro de la puerta."""
        # Cuerpo del candado
        candado_w, candado_h = 16, 12
        pygame.draw.rect(superficie, color,
                        (centro_x - candado_w//2, centro_y - candado_h//2, candado_w, candado_h))
        pygame.draw.rect(superficie, self._oscurecer_color(color, 0.4),
                        (centro_x - candado_w//2, centro_y - candado_h//2, candado_w, candado_h), 2)
        
        # Arco del candado
        pygame.draw.arc(superficie, color,
                       (centro_x - 8, centro_y - 15, 16, 12), 0, 3.14159, 3)
        
        # Agujero de la llave
        pygame.draw.circle(superficie, self._oscurecer_color(color, 0.6),
                          (centro_x, centro_y - 2), 2)
                          
    def _dibujar_indicador_tipo(self, superficie, x, y):
        """Dibuja un pequeño indicador del tipo de puerta."""
        if self.tipo == TipoPuerta.OBLIGATORIA:
            # Triángulo rojo (obligatoria)
            points = [(x + 5, y + 15), (x + 15, y + 5), (x + 15, y + 15)]
            pygame.draw.polygon(superficie, (255, 0, 0), points)
            
        elif self.tipo == TipoPuerta.OPCIONAL_SECRETA:
            # Estrella púrpura (secreta)
            self._dibujar_estrella(superficie, x + 10, y + 10, 5, (255, 0, 255))
            
        elif self.tipo == TipoPuerta.OPCIONAL_BONUS:
            # Círculo verde (bonus)
            pygame.draw.circle(superficie, (0, 255, 0), (x + 10, y + 10), 5)
            pygame.draw.circle(superficie, (0, 200, 0), (x + 10, y + 10), 5, 2)
            
        elif self.tipo == TipoPuerta.LLAVE_ESPECIAL:
            # Rombo dorado (llave especial)
            points = [(x + 10, y + 5), (x + 15, y + 10), (x + 10, y + 15), (x + 5, y + 10)]
            pygame.draw.polygon(superficie, (255, 215, 0), points)
            
    def _dibujar_indicador_llaves(self, superficie, x, y):
        """Dibuja el indicador de llaves requeridas."""
        # Fondo del indicador
        pygame.draw.rect(superficie, (0, 0, 0, 128), (x, y, 25, 15))
        
        # Dibujar pequeñas llaves
        for i in range(min(self.llaves_requeridas, 3)):  # Máximo 3 llaves visibles
            llave_x = x + 3 + i * 6
            llave_y = y + 7
            
            # Cuerpo de la llave
            pygame.draw.circle(superficie, (255, 215, 0), (llave_x, llave_y), 2)
            # Mango de la llave
            pygame.draw.line(superficie, (255, 215, 0), (llave_x + 2, llave_y), (llave_x + 5, llave_y), 1)
            
        # Si necesita más de 3 llaves, mostrar "+"
        if self.llaves_requeridas > 3:
            font = pygame.font.Font(None, 12)
            texto = font.render("+", True, (255, 255, 255))
            superficie.blit(texto, (x + 20, y + 3))
            
    def _dibujar_estrella(self, superficie, centro_x, centro_y, radio, color):
        """Dibuja una estrella de 5 puntas."""
        import math
        points = []
        for i in range(10):
            angle = i * math.pi / 5
            if i % 2 == 0:
                r = radio
            else:
                r = radio // 2
            px = centro_x + r * math.cos(angle - math.pi/2)
            py = centro_y + r * math.sin(angle - math.pi/2)
            points.append((px, py))
        pygame.draw.polygon(superficie, color, points)
        
    def _oscurecer_color(self, color, factor):
        """Oscurece un color por el factor dado (0.0-1.0)."""
        r, g, b = color
        return (max(0, int(r * (1 - factor))), 
                max(0, int(g * (1 - factor))), 
                max(0, int(b * (1 - factor))))