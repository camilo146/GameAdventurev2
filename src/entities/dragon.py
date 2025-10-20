"""
Sistema del Jefe Final - Dragón Bowser.
El dragón aparece en el nivel 5 antes de rescatar a la princesa.
Se derrota respondiendo preguntas de quiz correctamente.
"""

import pygame
from src.utils.constantes import *

class Dragon:
    """
    Jefe final del juego - Dragón que protege a la princesa.
    
    Mecánica:
    - Aparece cuando Mario llega a la zona final del nivel 5
    - Tiene vida que se reduce al responder preguntas correctamente
    - Si Mario responde mal, pierde una vida
    - Cuando la vida del dragón llega a 0, se puede rescatar a la princesa
    """
    
    def __init__(self, x: int, y: int):
        """
        Inicializa el dragón.
        
        Args:
            x: Posición X inicial
            y: Posición Y inicial
        """
        self.rect = pygame.Rect(x, y, 100, 120)  # Dragón más grande
        self.vida_maxima = 5  # 5 preguntas correctas para derrotarlo
        self.vida_actual = 5
        self.activo = False  # Se activa cuando Mario se acerca
        self.derrotado = False
        self.animacion_frame = 0
        self.tiempo_animacion = 0
        self.disparando_fuego = False
        self.tiempo_disparo = 0
        
        # Colores del dragón (estilo Bowser mejorado)
        self.color_cuerpo = (34, 139, 34)  # Verde oscuro
        self.color_caparazon = (218, 85, 34)  # Naranja/rojo
        self.color_caparazon_oscuro = (139, 69, 19)  # Marrón oscuro para bordes
        self.color_picos = (255, 255, 255)  # Blanco
        self.color_picos_sombra = (139, 0, 0)  # Rojo oscuro para bordes
        self.color_ojos = (255, 0, 0)  # Rojo
        self.color_fuego = (255, 140, 0)  # Naranja fuego
        self.color_vientre = (50, 180, 50)  # Verde claro para vientre
        
        # Animación de parpadeo
        self.tiempo_parpadeo = 0
        self.parpadeando = False
        
    def activar(self):
        """Activa al dragón cuando Mario se acerca."""
        if not self.derrotado:
            self.activo = True
    
    def recibir_danio(self) -> bool:
        """
        El dragón recibe daño cuando Mario responde correctamente.
        
        Returns:
            True si el dragón fue derrotado, False si no
        """
        if self.vida_actual > 0:
            self.vida_actual -= 1
            if self.vida_actual <= 0:
                self.derrotado = True
                self.activo = False
                return True
        return False
    
    def disparar_fuego(self):
        """
        Activa la animación de disparar fuego del dragón.
        Se usa cuando Mario responde incorrectamente.
        """
        self.disparando_fuego = True
        self.tiempo_disparo = 0
    
    def update(self, dt: float):
        """
        Actualiza el estado del dragón.
        
        Args:
            dt: Delta time en segundos
        """
        if not self.activo or self.derrotado:
            return
        
        # Animación de respiración/movimiento
        self.tiempo_animacion += dt
        if self.tiempo_animacion >= 0.2:  # Cambiar frame cada 0.2s
            self.tiempo_animacion = 0
            self.animacion_frame = (self.animacion_frame + 1) % 4
            
        # Animación de lanzar fuego periódicamente
        self.tiempo_disparo += dt
        if self.tiempo_disparo >= 2.0:  # Cada 2 segundos
            self.disparando_fuego = True
            self.tiempo_disparo = 0
        elif self.tiempo_disparo >= 0.5:
            self.disparando_fuego = False
            
        # Animación de parpadeo
        self.tiempo_parpadeo += dt
        if self.tiempo_parpadeo >= 3.0:  # Parpadeo cada 3 segundos
            self.parpadeando = True
            self.tiempo_parpadeo = 0
        elif self.tiempo_parpadeo >= 0.1:  # Parpadeo dura 0.1s
            self.parpadeando = False
    
    def dibujar(self, pantalla: pygame.Surface, camara_x: int):
        """
        Dibuja al dragón Bowser en la pantalla con estilo mejorado de NES.
        
        Args:
            pantalla: Surface donde dibujar
            camara_x: Offset de la cámara
        """
        if self.derrotado:
            return
        
        x = self.rect.x - camara_x
        y = self.rect.y
        
        # Movimiento de respiración más pronunciado
        offset_y = 0
        if self.activo:
            offset_y = [0, -3, -2, 2][self.animacion_frame]
        
        # Color de piel (verde más oscuro para mejor definición)
        color_piel = (34, 139, 34)
        color_piel_claro = (50, 180, 50)
        
        # ===== CAPARAZÓN TRASERO (más detallado) =====
        # Caparazón principal (forma más redondeada)
        caparazon_rect = pygame.Rect(x + 5, y + 25 + offset_y, 85, 65)
        pygame.draw.ellipse(pantalla, self.color_caparazon, caparazon_rect)
        
        # Borde oscuro del caparazón
        pygame.draw.ellipse(pantalla, (139, 69, 19), caparazon_rect, 3)
        
        # Picos del caparazón (6 picos más grandes y puntiagudos)
        for i in range(6):
            punto_x = x + 12 + (i * 13)
            punto_y = y + 25 + offset_y
            # Pico principal
            pygame.draw.polygon(pantalla, self.color_picos, [
                (punto_x, punto_y),
                (punto_x + 6, punto_y - 12),
                (punto_x + 12, punto_y)
            ])
            # Borde oscuro del pico
            pygame.draw.polygon(pantalla, (139, 0, 0), [
                (punto_x, punto_y),
                (punto_x + 6, punto_y - 12),
                (punto_x + 12, punto_y)
            ], 2)
        
        # ===== CUERPO =====
        # Cuerpo principal (más ancho en el medio)
        cuerpo_rect = pygame.Rect(x + 25, y + 45 + offset_y, 55, 55)
        pygame.draw.ellipse(pantalla, color_piel, cuerpo_rect)
        
        # Vientre (parte frontal más clara)
        vientre_rect = pygame.Rect(x + 35, y + 50 + offset_y, 35, 45)
        pygame.draw.ellipse(pantalla, color_piel_claro, vientre_rect)
        
        # ===== CABEZA =====
        # Cabeza principal (más grande y prominente)
        cabeza_rect = pygame.Rect(x + 42, y + 5 + offset_y, 52, 48)
        pygame.draw.ellipse(pantalla, color_piel, cabeza_rect)
        
        # ===== CUERNOS (más grandes y curvados) =====
        # Cuerno izquierdo
        pygame.draw.polygon(pantalla, self.color_caparazon, [
            (x + 45, y + 12 + offset_y),
            (x + 38, y + 2 + offset_y),
            (x + 42, y + 8 + offset_y),
            (x + 50, y + 18 + offset_y)
        ])
        # Cuerno derecho
        pygame.draw.polygon(pantalla, self.color_caparazon, [
            (x + 88, y + 12 + offset_y),
            (x + 95, y + 2 + offset_y),
            (x + 91, y + 8 + offset_y),
            (x + 83, y + 18 + offset_y)
        ])
        
        # Detalles de cuernos (brillo)
        pygame.draw.polygon(pantalla, AMARILLO, [
            (x + 42, y + 6 + offset_y),
            (x + 40, y + 4 + offset_y),
            (x + 44, y + 10 + offset_y)
        ])
        pygame.draw.polygon(pantalla, AMARILLO, [
            (x + 91, y + 6 + offset_y),
            (x + 93, y + 4 + offset_y),
            (x + 89, y + 10 + offset_y)
        ])
        
        # ===== CEJAS (expresión amenazante) =====
        pygame.draw.polygon(pantalla, color_piel, [
            (x + 52, y + 20 + offset_y),
            (x + 58, y + 18 + offset_y),
            (x + 60, y + 22 + offset_y)
        ])
        pygame.draw.polygon(pantalla, color_piel, [
            (x + 80, y + 20 + offset_y),
            (x + 74, y + 18 + offset_y),
            (x + 72, y + 22 + offset_y)
        ])
        
        # ===== OJOS (más grandes y expresivos) =====
        if not self.parpadeando:
            # Ojos blancos
            pygame.draw.ellipse(pantalla, BLANCO, (x + 52, y + 22 + offset_y, 14, 12))
            pygame.draw.ellipse(pantalla, BLANCO, (x + 68, y + 22 + offset_y, 14, 12))
            
            # Pupilas rojas malvadas (más intensas cuando ataca)
            color_pupila = (255, 50, 0) if self.disparando_fuego else self.color_ojos
            pygame.draw.circle(pantalla, color_pupila, (x + 57, y + 28 + offset_y), 5)
            pygame.draw.circle(pantalla, color_pupila, (x + 73, y + 28 + offset_y), 5)
            
            # Brillo en los ojos (más brillante cuando ataca)
            brillo_size = 3 if self.disparando_fuego else 2
            pygame.draw.circle(pantalla, BLANCO, (x + 59, y + 26 + offset_y), brillo_size)
            pygame.draw.circle(pantalla, BLANCO, (x + 75, y + 26 + offset_y), brillo_size)
        else:
            # Parpadeo - líneas cerradas
            pygame.draw.line(pantalla, NEGRO, (x + 52, y + 28 + offset_y), (x + 66, y + 28 + offset_y), 2)
            pygame.draw.line(pantalla, NEGRO, (x + 68, y + 28 + offset_y), (x + 82, y + 28 + offset_y), 2)
        
        # ===== HOCICO/BOCA =====
        # Hocico prominente (como Bowser original)
        hocico_rect = pygame.Rect(x + 78, y + 30 + offset_y, 22, 20)
        pygame.draw.ellipse(pantalla, color_piel_claro, hocico_rect)
        
        # Contorno del hocico
        pygame.draw.ellipse(pantalla, color_piel, hocico_rect, 2)
        
        # Fosas nasales grandes
        pygame.draw.ellipse(pantalla, NEGRO, (x + 84, y + 35 + offset_y, 5, 6))
        pygame.draw.ellipse(pantalla, NEGRO, (x + 84, y + 42 + offset_y, 5, 6))
        
        # Boca abierta (amenazante)
        pygame.draw.arc(pantalla, NEGRO, (x + 70, y + 42 + offset_y, 20, 10), 3.14, 6.28, 3)
        
        # Dientes/colmillos
        for i in range(3):
            pygame.draw.polygon(pantalla, BLANCO, [
                (x + 72 + i * 6, y + 48 + offset_y),
                (x + 74 + i * 6, y + 52 + offset_y),
                (x + 76 + i * 6, y + 48 + offset_y)
            ])
        
        # ===== FUEGO (cuando dispara) =====
        if self.disparando_fuego and self.activo:
            # Llamas más grandes y detalladas
            for i in range(4):
                fuego_x = x + 100 + (i * 18)
                fuego_y = y + 40 + offset_y + (i * 3)
                # Llama naranja exterior
                pygame.draw.circle(pantalla, self.color_fuego, (fuego_x, fuego_y), 10 - i * 2)
                # Llama amarilla interior
                pygame.draw.circle(pantalla, AMARILLO, (fuego_x + 2, fuego_y), 6 - i * 1.5)
                # Centro blanco brillante
                if i < 2:
                    pygame.draw.circle(pantalla, BLANCO, (fuego_x + 3, fuego_y), 2)
        
        # ===== BRAZOS/GARRAS =====
        # Brazo izquierdo (más musculoso)
        pygame.draw.ellipse(pantalla, color_piel, (x + 20, y + 55 + offset_y, 18, 35))
        pygame.draw.circle(pantalla, color_piel, (x + 29, y + 88 + offset_y), 7)
        
        # Brazo derecho
        pygame.draw.ellipse(pantalla, color_piel, (x + 67, y + 55 + offset_y, 18, 35))
        pygame.draw.circle(pantalla, color_piel, (x + 76, y + 88 + offset_y), 7)
        
        # Garras blancas (3 en cada mano)
        for i in range(3):
            # Garra izquierda
            pygame.draw.polygon(pantalla, BLANCO, [
                (x + 24 + i * 5, y + 88 + offset_y),
                (x + 25 + i * 5, y + 96 + offset_y),
                (x + 27 + i * 5, y + 88 + offset_y)
            ])
            # Garra derecha
            pygame.draw.polygon(pantalla, BLANCO, [
                (x + 71 + i * 5, y + 88 + offset_y),
                (x + 72 + i * 5, y + 96 + offset_y),
                (x + 74 + i * 5, y + 88 + offset_y)
            ])
        
        # ===== COLA (más gruesa y con punta de flecha) =====
        # Cola principal
        cola_puntos = [
            (x + 8, y + 65 + offset_y),
            (x - 2, y + 75 + offset_y),
            (x + 2, y + 92 + offset_y),
            (x + 18, y + 82 + offset_y)
        ]
        pygame.draw.polygon(pantalla, color_piel, cola_puntos)
        
        # Punta de flecha en la cola (pico rojo)
        pygame.draw.polygon(pantalla, self.color_picos, [
            (x + 0, y + 92 + offset_y),
            (x - 4, y + 80 + offset_y),
            (x + 8, y + 88 + offset_y)
        ])
        # Borde del pico
        pygame.draw.polygon(pantalla, (139, 0, 0), [
            (x + 0, y + 92 + offset_y),
            (x - 4, y + 80 + offset_y),
            (x + 8, y + 88 + offset_y)
        ], 2)
        
        # ===== PIES (añadidos para completar el diseño) =====
        # Pie izquierdo
        pygame.draw.ellipse(pantalla, color_piel, (x + 28, y + 95 + offset_y, 20, 12))
        # Pie derecho
        pygame.draw.ellipse(pantalla, color_piel, (x + 57, y + 95 + offset_y, 20, 12))
        
        # Barra de vida del dragón (encima)
        self._dibujar_barra_vida(pantalla, x, y - 20)
    
    def _dibujar_barra_vida(self, pantalla: pygame.Surface, x: int, y: int):
        """
        Dibuja la barra de vida del dragón.
        
        Args:
            pantalla: Surface donde dibujar
            x: Posición X
            y: Posición Y
        """
        # Fondo de la barra
        barra_ancho = 100
        barra_alto = 12
        pygame.draw.rect(pantalla, NEGRO, (x, y, barra_ancho, barra_alto))
        pygame.draw.rect(pantalla, GRIS, (x + 2, y + 2, barra_ancho - 4, barra_alto - 4))
        
        # Vida actual
        porcentaje_vida = self.vida_actual / self.vida_maxima
        ancho_vida = int((barra_ancho - 4) * porcentaje_vida)
        
        # Color según la vida
        if porcentaje_vida > 0.6:
            color_vida = VERDE
        elif porcentaje_vida > 0.3:
            color_vida = AMARILLO
        else:
            color_vida = ROJO
        
        pygame.draw.rect(pantalla, color_vida, (x + 2, y + 2, ancho_vida, barra_alto - 4))
        
        # Texto "BOWSER"
        fuente = pygame.font.Font(None, 16)
        texto = fuente.render("BOWSER", True, BLANCO)
        pantalla.blit(texto, (x + 20, y - 15))
        
        # Contador de vida
        texto_vida = fuente.render(f"{self.vida_actual}/{self.vida_maxima}", True, BLANCO)
        pantalla.blit(texto_vida, (x + 35, y + 1))
    
    def esta_cerca_de_mario(self, mario_x: int) -> bool:
        """
        Verifica si Mario está cerca del dragón para activarlo.
        
        Args:
            mario_x: Posición X de Mario
            
        Returns:
            True si Mario está cerca
        """
        distancia = abs(mario_x - self.rect.x)
        return distancia < 400  # Se activa a 400 píxeles
    
    def get_rect(self) -> pygame.Rect:
        """Retorna el rectángulo de colisión del dragón."""
        return self.rect
