import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Constantes
ANCHO = 800
ALTO = 600
FPS = 60
GRAVEDAD = 0.8
VELOCIDAD_JUGADOR = 5
FUERZA_SALTO = 15

# Colores
AZUL_CIELO = (107, 140, 255)
MARRON = (139, 69, 19)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 215, 0)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 200, 0)
NARANJA = (255, 140, 0)
VERDE_TUBO = (0, 168, 0)

# Configurar ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Super Mario Bros 2005")
reloj = pygame.time.Clock()

class Camara:
    def __init__(self, ancho_mapa):
        self.x = 0
        self.ancho_mapa = ancho_mapa
        
    def actualizar(self, objetivo):
        # La cámara sigue al jugador cuando pasa la mitad de la pantalla
        self.x = objetivo.rect.x - ANCHO // 3
        
        # Límites de la cámara
        if self.x < 0:
            self.x = 0
        if self.x > self.ancho_mapa - ANCHO:
            self.x = self.ancho_mapa - ANCHO

class Mario(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.ancho = 32
        self.alto = 32
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.saltando = False
        self.direccion = 'derecha'
        self.vivo = True
        self.invencible = 0
        self.grande = False
        self.tiene_flor = False
        self.animacion_frame = 0
        self.animacion_contador = 0
        
    def update(self, plataformas):
        if not self.vivo:
            return
            
        # Animación
        self.animacion_contador += 1
        if self.animacion_contador > 5:
            self.animacion_frame = (self.animacion_frame + 1) % 3
            self.animacion_contador = 0
        
        # Invencibilidad
        if self.invencible > 0:
            self.invencible -= 1
            
        # Gravedad
        self.velocidad_y += GRAVEDAD
        if self.velocidad_y > 15:
            self.velocidad_y = 15
            
        # Movimiento horizontal
        teclas = pygame.key.get_pressed()
        self.velocidad_x = 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.velocidad_x = -VELOCIDAD_JUGADOR
            self.direccion = 'izquierda'
        elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.velocidad_x = VELOCIDAD_JUGADOR
            self.direccion = 'derecha'
            
        # Actualizar posición
        self.rect.x += self.velocidad_x
        self.colision_horizontal(plataformas)
        
        self.rect.y += self.velocidad_y
        self.saltando = True
        self.colision_vertical(plataformas)
            
    def colision_horizontal(self, plataformas):
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                if self.velocidad_x > 0:
                    self.rect.right = plataforma.rect.left
                elif self.velocidad_x < 0:
                    self.rect.left = plataforma.rect.right
                    
    def colision_vertical(self, plataformas):
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                if self.velocidad_y > 0:
                    self.rect.bottom = plataforma.rect.top
                    self.velocidad_y = 0
                    self.saltando = False
                elif self.velocidad_y < 0:
                    self.rect.top = plataforma.rect.bottom
                    self.velocidad_y = 0
                    if hasattr(plataforma, 'tipo') and plataforma.tipo == 'bloque':
                        plataforma.golpeado = True
                        
    def saltar(self):
        if not self.saltando and self.vivo:
            self.velocidad_y = -FUERZA_SALTO
            self.saltando = True
            
    def crecer(self):
        if not self.grande:
            self.grande = True
            self.alto = 48
            self.rect.height = 48
            self.rect.y -= 16
            
    def obtener_flor(self):
        self.crecer()
        self.tiene_flor = True
        
    def recibir_dano(self):
        if self.invencible > 0:
            return False
            
        if self.tiene_flor:
            self.tiene_flor = False
            self.invencible = 120
            return False
        elif self.grande:
            self.grande = False
            self.alto = 32
            self.rect.height = 32
            self.invencible = 120
            return False
        else:
            self.vivo = False
            return True
            
    def dibujar(self, superficie):
        if not self.vivo:
            return
            
        # Efecto de parpadeo cuando está invencible
        if self.invencible > 0 and self.invencible % 10 < 5:
            return
            
        alto_actual = self.alto
        
        # Color base
        color_ropa = ROJO
        if self.tiene_flor:
            color_ropa = BLANCO
            
        # Gorra
        pygame.draw.rect(superficie, color_ropa, 
                        (self.rect.x + 4, self.rect.y, 24, 10))
        # Logo M
        pygame.draw.circle(superficie, BLANCO, 
                          (self.rect.x + 16, self.rect.y + 5), 4)
        
        # Cabello
        pygame.draw.rect(superficie, MARRON, 
                        (self.rect.x + 2, self.rect.y + 8, 28, 4))
        
        # Cara
        cara_y = self.rect.y + 12
        pygame.draw.rect(superficie, (255, 220, 177), 
                        (self.rect.x + 4, cara_y, 24, 16))
        
        # Ojos
        if self.direccion == 'derecha':
            pygame.draw.circle(superficie, NEGRO, 
                             (self.rect.x + 18, cara_y + 6), 2)
        else:
            pygame.draw.circle(superficie, NEGRO, 
                             (self.rect.x + 14, cara_y + 6), 2)
        
        # Bigote
        pygame.draw.rect(superficie, MARRON, 
                        (self.rect.x + 8, cara_y + 10, 16, 4))
        
        # Camisa
        cuerpo_y = self.rect.y + 28
        pygame.draw.rect(superficie, color_ropa, 
                        (self.rect.x + 4, cuerpo_y, 24, 12 if not self.grande else 20))
        
        # Botones
        for i in range(2 if not self.grande else 3):
            pygame.draw.circle(superficie, AMARILLO, 
                             (self.rect.x + 16, cuerpo_y + 4 + i * 6), 2)
        
        # Overol
        overol_y = cuerpo_y + 8
        pygame.draw.rect(superficie, AZUL, 
                        (self.rect.x + 8, overol_y, 16, 12 if not self.grande else 20))
        
        # Brazos (animación de caminar)
        if abs(self.velocidad_x) > 0:
            offset = 2 if self.animacion_frame % 2 == 0 else -2
            pygame.draw.rect(superficie, (255, 220, 177), 
                           (self.rect.x + 2, cuerpo_y + offset, 6, 12))
            pygame.draw.rect(superficie, (255, 220, 177), 
                           (self.rect.x + 24, cuerpo_y - offset, 6, 12))
        else:
            pygame.draw.rect(superficie, (255, 220, 177), 
                           (self.rect.x + 2, cuerpo_y, 6, 12))
            pygame.draw.rect(superficie, (255, 220, 177), 
                           (self.rect.x + 24, cuerpo_y, 6, 12))
        
        # Piernas
        piernas_y = self.rect.bottom - 12
        if abs(self.velocidad_x) > 0 and not self.saltando:
            # Animación de caminar
            if self.animacion_frame % 2 == 0:
                pygame.draw.rect(superficie, AZUL, 
                               (self.rect.x + 8, piernas_y, 6, 12))
                pygame.draw.rect(superficie, AZUL, 
                               (self.rect.x + 18, piernas_y - 2, 6, 12))
            else:
                pygame.draw.rect(superficie, AZUL, 
                               (self.rect.x + 8, piernas_y - 2, 6, 12))
                pygame.draw.rect(superficie, AZUL, 
                               (self.rect.x + 18, piernas_y, 6, 12))
        else:
            pygame.draw.rect(superficie, AZUL, 
                           (self.rect.x + 8, piernas_y, 6, 12))
            pygame.draw.rect(superficie, AZUL, 
                           (self.rect.x + 18, piernas_y, 6, 12))
        
        # Zapatos
        pygame.draw.rect(superficie, MARRON, 
                        (self.rect.x + 4, self.rect.bottom - 4, 10, 4))
        pygame.draw.rect(superficie, MARRON, 
                        (self.rect.x + 18, self.rect.bottom - 4, 10, 4))

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto, tipo='normal'):
        super().__init__()
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.tipo = tipo
        self.golpeado = False
        
    def dibujar(self, superficie):
        if self.tipo == 'suelo':
            # Césped
            pygame.draw.rect(superficie, VERDE, self.rect)
            pygame.draw.rect(superficie, MARRON, 
                           (self.rect.x, self.rect.y + 10, self.rect.width, self.rect.height - 10))
        elif self.tipo == 'bloque':
            # Bloque de ladrillos
            color = NARANJA if not self.golpeado else (150, 150, 150)
            pygame.draw.rect(superficie, color, self.rect)
            for i in range(0, self.rect.width, 20):
                for j in range(0, self.rect.height, 20):
                    pygame.draw.rect(superficie, MARRON, 
                                   (self.rect.x + i, self.rect.y + j, 20, 20), 1)
        elif self.tipo == 'tubo':
            # Tubo
            pygame.draw.rect(superficie, VERDE_TUBO, self.rect)
            pygame.draw.rect(superficie, (0, 100, 0), self.rect, 3)
            # Borde superior
            pygame.draw.rect(superficie, VERDE_TUBO, 
                           (self.rect.x - 4, self.rect.y - 4, self.rect.width + 8, 8))
        else:
            pygame.draw.rect(superficie, MARRON, self.rect)
            pygame.draw.rect(superficie, (101, 67, 33), self.rect, 2)

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo='goomba'):
        super().__init__()
        self.tipo = tipo
        self.ancho = 30 if tipo == 'goomba' else 32
        self.alto = 30 if tipo == 'goomba' else 40
        self.rect = pygame.Rect(x, y, self.ancho, self.alto)
        self.velocidad_x = -2 if tipo == 'goomba' else -1
        self.vivo = True
        self.aplastado = False
        self.animacion_frame = 0
        self.animacion_contador = 0
        
    def update(self, plataformas):
        if not self.vivo:
            return
            
        if self.aplastado:
            return
            
        self.animacion_contador += 1
        if self.animacion_contador > 10:
            self.animacion_frame = (self.animacion_frame + 1) % 2
            self.animacion_contador = 0
            
        self.rect.x += self.velocidad_x
        
        # Colisión con plataformas
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                if self.velocidad_x > 0:
                    self.rect.right = plataforma.rect.left
                    self.velocidad_x *= -1
                elif self.velocidad_x < 0:
                    self.rect.left = plataforma.rect.right
                    self.velocidad_x *= -1
                    
    def aplastar(self):
        self.aplastado = True
        self.alto = 10
        self.rect.height = 10
        
    def dibujar(self, superficie):
        if not self.vivo:
            return
            
        if self.tipo == 'goomba':
            if self.aplastado:
                pygame.draw.ellipse(superficie, MARRON, self.rect)
            else:
                # Cuerpo
                pygame.draw.rect(superficie, MARRON, 
                               (self.rect.x, self.rect.y + 5, self.ancho, self.alto - 10))
                # Cabeza
                pygame.draw.ellipse(superficie, MARRON, 
                                  (self.rect.x, self.rect.y, self.ancho, 15))
                # Ojos
                pygame.draw.circle(superficie, BLANCO, 
                                 (self.rect.x + 10, self.rect.y + 6), 4)
                pygame.draw.circle(superficie, BLANCO, 
                                 (self.rect.x + 20, self.rect.y + 6), 4)
                pygame.draw.circle(superficie, NEGRO, 
                                 (self.rect.x + 10, self.rect.y + 6), 2)
                pygame.draw.circle(superficie, NEGRO, 
                                 (self.rect.x + 20, self.rect.y + 6), 2)
                # Ceño
                pygame.draw.line(superficie, NEGRO, 
                               (self.rect.x + 5, self.rect.y + 3),
                               (self.rect.x + 25, self.rect.y + 3), 2)
                # Pies
                offset = 2 if self.animacion_frame == 0 else -2
                pygame.draw.ellipse(superficie, MARRON, 
                                  (self.rect.x - 5 + offset, self.rect.bottom - 5, 12, 8))
                pygame.draw.ellipse(superficie, MARRON, 
                                  (self.rect.x + 23 - offset, self.rect.bottom - 5, 12, 8))
        
        elif self.tipo == 'koopa':
            # Caparazón
            pygame.draw.ellipse(superficie, VERDE, 
                              (self.rect.x, self.rect.y + 15, self.ancho, 25))
            # Patrón del caparazón
            for i in range(3):
                pygame.draw.circle(superficie, AMARILLO, 
                                 (self.rect.x + 8 + i * 8, self.rect.y + 27), 3)
            # Cabeza
            pygame.draw.ellipse(superficie, AMARILLO, 
                              (self.rect.x + 6, self.rect.y, 20, 20))
            # Ojos
            pygame.draw.circle(superficie, BLANCO, 
                             (self.rect.x + 12, self.rect.y + 8), 3)
            pygame.draw.circle(superficie, BLANCO, 
                             (self.rect.x + 20, self.rect.y + 8), 3)
            pygame.draw.circle(superficie, NEGRO, 
                             (self.rect.x + 12, self.rect.y + 8), 1)
            pygame.draw.circle(superficie, NEGRO, 
                             (self.rect.x + 20, self.rect.y + 8), 1)
            # Pies
            offset = 2 if self.animacion_frame == 0 else -2
            pygame.draw.rect(superficie, AMARILLO, 
                           (self.rect.x + 4 + offset, self.rect.bottom - 8, 8, 8))
            pygame.draw.rect(superficie, AMARILLO, 
                           (self.rect.x + 20 - offset, self.rect.bottom - 8, 8, 8))

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo='hongo'):
        super().__init__()
        self.tipo = tipo
        self.rect = pygame.Rect(x, y, 24, 24)
        self.velocidad_x = 2
        self.velocidad_y = 0
        self.activo = False
        
    def update(self, plataformas):
        if not self.activo:
            return
            
        self.velocidad_y += GRAVEDAD
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y
        
        # Colisión con plataformas
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                if self.velocidad_y > 0:
                    self.rect.bottom = plataforma.rect.top
                    self.velocidad_y = 0
                if self.velocidad_x > 0:
                    self.rect.right = plataforma.rect.left
                    self.velocidad_x *= -1
                elif self.velocidad_x < 0:
                    self.rect.left = plataforma.rect.right
                    self.velocidad_x *= -1
                    
    def activar(self):
        self.activo = True
        self.velocidad_y = -5
        
    def dibujar(self, superficie):
        if not self.activo:
            return
            
        if self.tipo == 'hongo':
            # Tallo
            pygame.draw.rect(superficie, BLANCO, 
                           (self.rect.x + 8, self.rect.y + 12, 8, 12))
            # Cabeza
            pygame.draw.ellipse(superficie, ROJO, 
                              (self.rect.x, self.rect.y, 24, 16))
            # Puntos blancos
            pygame.draw.circle(superficie, BLANCO, 
                             (self.rect.x + 6, self.rect.y + 6), 3)
            pygame.draw.circle(superficie, BLANCO, 
                             (self.rect.x + 18, self.rect.y + 6), 3)
            pygame.draw.circle(superficie, BLANCO, 
                             (self.rect.x + 12, self.rect.y + 10), 2)
        
        elif self.tipo == 'flor':
            # Tallo
            pygame.draw.rect(superficie, VERDE, 
                           (self.rect.x + 10, self.rect.y + 8, 4, 16))
            # Pétalos
            colores = [ROJO, AMARILLO, ROJO, AMARILLO]
            for i, color in enumerate(colores):
                offset_x = [8, 0, -8, 0][i]
                offset_y = [0, -8, 0, 8][i]
                pygame.draw.circle(superficie, color, 
                                 (self.rect.x + 12 + offset_x, 
                                  self.rect.y + 8 + offset_y), 5)
            # Centro
            pygame.draw.circle(superficie, NARANJA, 
                             (self.rect.x + 12, self.rect.y + 8), 4)

class Moneda(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 20, 20)
        self.animacion_frame = 0
        self.animacion_contador = 0
        
    def update(self):
        self.animacion_contador += 1
        if self.animacion_contador > 5:
            self.animacion_frame = (self.animacion_frame + 1) % 4
            self.animacion_contador = 0
        
    def dibujar(self, superficie):
        # Efecto de rotación
        ancho = 20 - abs(self.animacion_frame - 2) * 5
        pygame.draw.ellipse(superficie, AMARILLO, 
                          (self.rect.x + (20 - ancho) // 2, self.rect.y, ancho, 20))
        pygame.draw.ellipse(superficie, NARANJA, 
                          (self.rect.x + (20 - ancho) // 2, self.rect.y, ancho, 20), 2)

class Bandera(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 40, 200)
        
    def dibujar(self, superficie):
        # Asta
        pygame.draw.rect(superficie, BLANCO, 
                        (self.rect.x + 18, self.rect.y, 4, 200))
        # Bandera
        puntos = [
            (self.rect.x + 22, self.rect.y + 10),
            (self.rect.x + 50, self.rect.y + 25),
            (self.rect.x + 22, self.rect.y + 40)
        ]
        pygame.draw.polygon(superficie, ROJO, puntos)
        # Punta
        pygame.draw.circle(superficie, AMARILLO, 
                         (self.rect.x + 20, self.rect.y), 6)

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
        
    def crear_nivel(self):
        if self.numero == 1:
            # Nivel 1: Tutorial extendido
            self.ancho_mapa = 3200
            
            # Suelo base continuo
            self.plataformas = [
                Plataforma(0, 550, 3200, 50, 'suelo'),
            ]
            
            # Primera sección
            self.plataformas.extend([
                Plataforma(200, 450, 100, 20, 'bloque'),
                Plataforma(350, 400, 80, 20, 'bloque'),
                Plataforma(150, 350, 60, 120, 'tubo'),
            ])
            
            self.enemigos.extend([
                Enemigo(250, 520, 'goomba'),
                Enemigo(400, 370, 'goomba'),
            ])
            
            self.monedas.extend([
                Moneda(220, 430),
                Moneda(250, 430),
                Moneda(280, 430),
                Moneda(370, 380),
            ])
            
            self.powerups.append(PowerUp(240, 430, 'hongo'))
            
            # Segunda sección
            self.plataformas.extend([
                Plataforma(550, 450, 80, 20, 'bloque'),
                Plataforma(680, 380, 80, 20, 'bloque'),
                Plataforma(810, 310, 80, 20, 'bloque'),
                Plataforma(500, 300, 60, 120, 'tubo'),
            ])
            
            self.enemigos.extend([
                Enemigo(600, 420, 'goomba'),
                Enemigo(730, 350, 'goomba'),
                Enemigo(860, 280, 'goomba'),
            ])
            
            self.monedas.extend([
                Moneda(580, 430),
                Moneda(710, 360),
                Moneda(840, 290),
            ])
            
            # Tercera sección
            self.plataformas.extend([
                Plataforma(1000, 450, 60, 120, 'tubo'),
                Plataforma(1150, 400, 60, 170, 'tubo'),
                Plataforma(1300, 450, 60, 120, 'tubo'),
                Plataforma(1100, 300, 100, 20, 'bloque'),
            ])
            
            self.enemigos.extend([
                Enemigo(1050, 520, 'goomba'),
                Enemigo(1200, 520, 'koopa'),
                Enemigo(1350, 520, 'goomba'),
            ])
            
            self.monedas.extend([
                Moneda(1130, 280),
                Moneda(1160, 280),
            ])
            
            self.powerups.append(PowerUp(1140, 280, 'flor'))
            
            # Cuarta sección
            self.plataformas.extend([
                Plataforma(1500, 480, 80, 20, 'bloque'),
                Plataforma(1630, 420, 80, 20, 'bloque'),
                Plataforma(1760, 360, 80, 20, 'bloque'),
                Plataforma(1890, 300, 80, 20, 'bloque'),
                Plataforma(2020, 240, 100, 20, 'bloque'),
            ])
            
            self.enemigos.extend([
                Enemigo(1550, 450, 'goomba'),
                Enemigo(1680, 390, 'goomba'),
                Enemigo(1810, 330, 'koopa'),
            ])
            
            self.monedas.extend([
                Moneda(1540, 460),
                Moneda(1670, 400),
                Moneda(1800, 340),
                Moneda(1930, 280),
                Moneda(2060, 220),
            ])
            
            # Quinta sección
            self.plataformas.extend([
                Plataforma(2200, 450, 120, 20, 'bloque'),
                Plataforma(2380, 380, 100, 20, 'bloque'),
                Plataforma(2500, 450, 60, 120, 'tubo'),
            ])
            
            self.enemigos.extend([
                Enemigo(2250, 420, 'koopa'),
                Enemigo(2420, 350, 'goomba'),
            ])
            
            self.monedas.extend([
                Moneda(2240, 430),
                Moneda(2270, 430),
                Moneda(2420, 360),
            ])
            
            # Zona final
            self.plataformas.extend([
                Plataforma(2700, 480, 60, 20, 'bloque'),
                Plataforma(2800, 420, 60, 20, 'bloque'),
                Plataforma(2900, 360, 60, 20, 'bloque'),
            ])
            
            self.enemigos.extend([
                Enemigo(2750, 450, 'goomba'),
                Enemigo(2850, 390, 'koopa'),
            ])
            
            self.monedas.extend([
                Moneda(2730, 460),
                Moneda(2830, 400),
                Moneda(2930, 340),
            ])
            
            self.bandera = Bandera(3100, 350)
            
        elif self.numero == 2:
            # Nivel 2
            self.ancho_mapa = 4000
            
            self.plataformas = [
                Plataforma(0, 550, 4000, 50, 'suelo'),
            ]
            
            # Sección 1
            self.plataformas.extend([
                Plataforma(150, 450, 60, 120, 'tubo'),
                Plataforma(300, 400, 60, 170, 'tubo'),
                Plataforma(450, 450, 60, 120, 'tubo'),
                Plataforma(250, 320, 80, 20, 'bloque'),
            ])
            
            self.enemigos.extend([
                Enemigo(200, 520, 'goomba'),
                Enemigo(350, 520, 'koopa'),
                Enemigo(500, 520, 'goomba'),
            ])
            
            self.monedas.extend([
                Moneda(270, 300),
                Moneda(300, 300),
            ])
            
            self.powerups.append(PowerUp(285, 300, 'hongo'))
            
            # Sección 2
            for i in range(8):
                x = 600 + i * 120
                y = 450 - (i % 4) * 70
                self.plataformas.append(Plataforma(x, y, 80, 20, 'bloque'))
                
                if i % 2 == 0:
                    self.enemigos.append(Enemigo(x + 20, y - 30, 'goomba'))
                    self.monedas.append(Moneda(x + 30, y - 30))
                else:
                    self.monedas.append(Moneda(x + 30, y - 30))
            
            # Sección 3
            self.plataformas.extend([
                Plataforma(1600, 400, 80, 170, 'tubo'),
                Plataforma(1750, 350, 80, 220, 'tubo'),
                Plataforma(1900, 400, 80, 170, 'tubo'),
                Plataforma(1700, 250, 120, 20, 'bloque'),
            ])
            
            self.enemigos.extend([
                Enemigo(1650, 520, 'koopa'),
                Enemigo(1800, 520, 'koopa'),
                Enemigo(1950, 520, 'goomba'),
            ])
            
            self.monedas.extend([
                Moneda(1730, 230),
                Moneda(1760, 230),
            ])
            
            self.powerups.append(PowerUp(1760, 230, 'flor'))
            
            # Sección 4
            for i in range(10):
                x = 2100 + i * 100
                y = 450 - (i % 5) * 60
                self.plataformas.append(Plataforma(x, y, 70, 20, 'bloque'))
                
                if i % 3 == 0:
                    self.enemigos.append(Enemigo(x + 10, y - 30, 'goomba'))
                if i % 2 == 0:
                    self.monedas.append(Moneda(x + 20, y - 30))
            
            # Sección 5
            self.plataformas.extend([
                Plataforma(3000, 450, 60, 120, 'tubo'),
                Plataforma(3120, 380, 60, 190, 'tubo'),
                Plataforma(3240, 320, 60, 250, 'tubo'),
                Plataforma(3360, 380, 60, 190, 'tubo'),
                Plataforma(3480, 450, 60, 120, 'tubo'),
            ])
            
            self.enemigos.extend([
                Enemigo(3050, 520, 'goomba'),
                Enemigo(3170, 520, 'koopa'),
                Enemigo(3290, 520, 'goomba'),
            ])
            
            for i, x in enumerate([3030, 3150, 3270]):
                altura = [420, 350, 290][i]
                self.monedas.append(Moneda(x, altura))
            
            # Zona final
            self.plataformas.extend([
                Plataforma(3650, 450, 80, 20, 'bloque'),
                Plataforma(3750, 380, 80, 20, 'bloque'),
            ])
            
            self.enemigos.extend([
                Enemigo(3700, 420, 'koopa'),
            ])
            
            self.monedas.extend([
                Moneda(3690, 430),
                Moneda(3790, 360),
            ])
            
            self.bandera = Bandera(3920, 350)
            
        elif self.numero == 3:
            # Nivel 3
            self.ancho_mapa = 5000
            
            self.plataformas = [
                Plataforma(0, 550, 5000, 50, 'suelo'),
            ]
            
            # Sección 1
            self.plataformas.extend([
                Plataforma(100, 450, 60, 120, 'tubo'),
                Plataforma(220, 380, 60, 190, 'tubo'),
                Plataforma(340, 320, 60, 250, 'tubo'),
                Plataforma(460, 380, 60, 190, 'tubo'),
                Plataforma(580, 450, 60, 120, 'tubo'),
                Plataforma(300, 240, 100, 20, 'bloque'),
            ])
            
            self.enemigos.extend([
                Enemigo(150, 520, 'goomba'),
                Enemigo(270, 520, 'koopa'),
                Enemigo(390, 520, 'goomba'),
                Enemigo(510, 520, 'koopa'),
            ])
            
            self.monedas.extend([
                Moneda(330, 220),
                Moneda(360, 220),
            ])
            
            self.powerups.append(PowerUp(345, 220, 'hongo'))
            
            # Sección 2
            for i in range(12):
                x = 750 + i * 100
                y = 480 - (i % 5) * 60
                self.plataformas.append(Plataforma(x, y, 70, 20, 'bloque'))
                
                if i % 2 == 0:
                    self.enemigos.append(Enemigo(x + 15, y - 30, 'goomba'))
                
                if i % 3 == 0:
                    self.monedas.append(Moneda(x + 20, y - 30))
            
            # Sección 3
            tubos_x = [2000, 2140, 2280, 2420, 2560]
            tubos_altura = [450, 350, 280, 350, 450]
            
            for x, altura_base in zip(tubos_x, tubos_altura):
                altura_tubo = 550 - altura_base + 20
                self.plataformas.append(Plataforma(x, altura_base, 70, altura_tubo, 'tubo'))
                self.enemigos.append(Enemigo(x + 20, 520, 'goomba'))
                
                if random.random() < 0.6:
                    self.monedas.append(Moneda(x + 20, altura_base - 30))
            
            self.plataformas.extend([
                Plataforma(2100, 280, 80, 20, 'bloque'),
                Plataforma(2240, 200, 80, 20, 'bloque'),
                Plataforma(2380, 280, 80, 20, 'bloque'),
            ])
            
            self.enemigos.extend([
                Enemigo(2140, 250, 'goomba'),
                Enemigo(2280, 170, 'koopa'),
            ])
            
            self.powerups.append(PowerUp(2280, 180, 'flor'))
            
            # Sección 4
            for i in range(14):
                x = 2800 + i * 80
                y = 450 - abs(i % 8 - 4) * 50
                self.plataformas.append(Plataforma(x, y, 60, 20, 'bloque'))
                
                if i % 3 == 0:
                    self.enemigos.append(Enemigo(x + 10, y - 30, 'goomba'))
                
                if i % 2 == 0:
                    self.monedas.append(Moneda(x + 20, y - 30))
            
            # Sección 5
            torres = [
                (4000, 400, 170),
                (4140, 320, 250),
                (4280, 250, 320),
                (4420, 320, 250),
                (4560, 400, 170),
            ]
            
            for x, y, altura in torres:
                self.plataformas.append(Plataforma(x, y, 70, altura, 'tubo'))
                self.enemigos.append(Enemigo(x + 15, 520, 'goomba'))
                
                for j in range(2):
                    self.monedas.append(Moneda(x + 25, y - 30 - j * 30))
            
            self.plataformas.extend([
                Plataforma(4100, 220, 80, 20, 'bloque'),
                Plataforma(4240, 150, 120, 20, 'bloque'),
                Plataforma(4380, 220, 80, 20, 'bloque'),
            ])
            
            self.enemigos.extend([
                Enemigo(4140, 190, 'koopa'),
                Enemigo(4280, 120, 'goomba'),
            ])
            
            self.monedas.extend([
                Moneda(4270, 130),
                Moneda(4300, 130),
            ])
            
            self.powerups.append(PowerUp(4300, 130, 'flor'))
            
            # Zona final
            self.plataformas.extend([
                Plataforma(4700, 480, 60, 20, 'bloque'),
                Plataforma(4780, 420, 60, 20, 'bloque'),
                Plataforma(4860, 360, 60, 20, 'bloque'),
            ])
            
            self.enemigos.extend([
                Enemigo(4730, 450, 'koopa'),
                Enemigo(4810, 390, 'koopa'),
            ])
            
            self.monedas.extend([
                Moneda(4730, 460),
                Moneda(4810, 400),
            ])
            
            self.bandera = Bandera(4920, 350)

class Juego:
    def __init__(self):
        self.mario = Mario(50, 400)
        self.nivel_actual = 1
        self.nivel = Nivel(self.nivel_actual)
        self.camara = Camara(self.nivel.ancho_mapa)
        self.puntuacion = 0
        self.vidas = 3
        self.monedas_totales = 0
        self.tiempo = 400
        self.tiempo_contador = 0
        self.fuente = pygame.font.Font(None, 36)
        self.fuente_pequena = pygame.font.Font(None, 24)
        self.fuente_grande = pygame.font.Font(None, 72)
        self.game_over = False
        self.pausa = False
        self.mensaje = ""
        self.mensaje_tiempo = 0
        
    def reiniciar_nivel(self):
        self.mario = Mario(50, 400)
        self.nivel = Nivel(self.nivel_actual)
        self.camara = Camara(self.nivel.ancho_mapa)
        self.tiempo = 400
        self.tiempo_contador = 0
        self.mensaje = ""
        
    def siguiente_nivel(self):
        self.nivel_actual += 1
        if self.nivel_actual > 3:
            self.mensaje = "¡FELICIDADES! ¡JUEGO COMPLETADO!"
            self.mensaje_tiempo = 180
            self.nivel_actual = 1
        self.reiniciar_nivel()
        
    def reiniciar_juego(self):
        self.mario = Mario(50, 400)
        self.nivel_actual = 1
        self.nivel = Nivel(self.nivel_actual)
        self.camara = Camara(self.nivel.ancho_mapa)
        self.puntuacion = 0
        self.vidas = 3
        self.monedas_totales = 0
        self.tiempo = 400
        self.tiempo_contador = 0
        self.game_over = False
        self.mensaje = ""
        self.mensaje_tiempo = 0
        
    def verificar_colisiones(self):
        # Colisión con enemigos
        for enemigo in self.nivel.enemigos[:]:
            if not enemigo.vivo:
                continue
                
            if self.mario.rect.colliderect(enemigo.rect):
                if self.mario.velocidad_y > 0 and self.mario.rect.bottom < enemigo.rect.centery + 5:
                    enemigo.aplastar()
                    enemigo.vivo = False
                    self.puntuacion += 100
                    self.mario.velocidad_y = -8
                    self.mensaje = "+100"
                    self.mensaje_tiempo = 30
                else:
                    if self.mario.recibir_dano():
                        self.vidas -= 1
                        if self.vidas <= 0:
                            self.game_over = True
                        else:
                            self.reiniciar_nivel()
                            
        # Colisión con monedas
        for moneda in self.nivel.monedas[:]:
            if self.mario.rect.colliderect(moneda.rect):
                self.nivel.monedas.remove(moneda)
                self.puntuacion += 50
                self.monedas_totales += 1
                self.mensaje = "+50"
                self.mensaje_tiempo = 30
                
                if self.monedas_totales % 100 == 0:
                    self.vidas += 1
                    self.mensaje = "¡VIDA EXTRA!"
                    self.mensaje_tiempo = 60
                    
        # Colisión con power-ups
        for powerup in self.nivel.powerups[:]:
            if not powerup.activo:
                continue
                
            if self.mario.rect.colliderect(powerup.rect):
                if powerup.tipo == 'hongo':
                    self.mario.crecer()
                    self.puntuacion += 500
                    self.mensaje = "¡SUPER MARIO!"
                    self.mensaje_tiempo = 60
                elif powerup.tipo == 'flor':
                    self.mario.obtener_flor()
                    self.puntuacion += 1000
                    self.mensaje = "¡FIRE MARIO!"
                    self.mensaje_tiempo = 60
                self.nivel.powerups.remove(powerup)
                
        # Activar power-ups al golpear bloques
        for plataforma in self.nivel.plataformas:
            if hasattr(plataforma, 'golpeado') and plataforma.golpeado:
                plataforma.golpeado = False
                for powerup in self.nivel.powerups:
                    if not powerup.activo and abs(powerup.rect.x - plataforma.rect.x) < 50:
                        powerup.activar()
                        break
                        
        # Colisión con bandera
        if self.nivel.bandera and self.mario.rect.colliderect(self.nivel.bandera.rect):
            if not self.nivel.completado:
                self.nivel.completado = True
                bonus = self.tiempo * 10
                self.puntuacion += bonus
                self.mensaje = f"¡NIVEL COMPLETADO! +{bonus}"
                self.mensaje_tiempo = 120
                
        # Caída fuera del mapa
        if self.mario.rect.y > ALTO:
            self.vidas -= 1
            if self.vidas <= 0:
                self.game_over = True
            else:
                self.reiniciar_nivel()
                
    def actualizar(self):
        if self.game_over or self.pausa:
            return
            
        self.tiempo_contador += 1
        if self.tiempo_contador >= FPS:
            self.tiempo -= 1
            self.tiempo_contador = 0
            
        if self.tiempo <= 0:
            self.vidas -= 1
            if self.vidas <= 0:
                self.game_over = True
            else:
                self.reiniciar_nivel()
                
        if self.mensaje_tiempo > 0:
            self.mensaje_tiempo -= 1
            if self.mensaje_tiempo == 0:
                self.mensaje = ""
                
        if self.nivel.completado and self.mensaje_tiempo == 0:
            self.siguiente_nivel()
            
        self.mario.update(self.nivel.plataformas)
        self.camara.actualizar(self.mario)
        
        for enemigo in self.nivel.enemigos:
            enemigo.update(self.nivel.plataformas)
            
        for moneda in self.nivel.monedas:
            moneda.update()
            
        for powerup in self.nivel.powerups:
            powerup.update(self.nivel.plataformas)
            
        self.verificar_colisiones()
        
    def dibujar_hud(self):
        pygame.draw.rect(pantalla, NEGRO, (0, 0, ANCHO, 40))
        
        texto_puntos = self.fuente_pequena.render(f"PUNTOS: {self.puntuacion:06d}", True, BLANCO)
        pantalla.blit(texto_puntos, (10, 10))
        
        pygame.draw.circle(pantalla, AMARILLO, (250, 20), 8)
        texto_monedas = self.fuente_pequena.render(f"x {self.monedas_totales:03d}", True, BLANCO)
        pantalla.blit(texto_monedas, (265, 10))
        
        texto_nivel = self.fuente_pequena.render(f"NIVEL: {self.nivel_actual}-1", True, BLANCO)
        pantalla.blit(texto_nivel, (380, 10))
        
        texto_vidas = self.fuente_pequena.render(f"VIDAS:", True, BLANCO)
        pantalla.blit(texto_vidas, (530, 10))
        for i in range(self.vidas):
            pygame.draw.circle(pantalla, ROJO, (610 + i * 25, 20), 8)
            
        color_tiempo = ROJO if self.tiempo < 30 else BLANCO
        texto_tiempo = self.fuente_pequena.render(f"TIEMPO: {self.tiempo:03d}", True, color_tiempo)
        pantalla.blit(texto_tiempo, (680, 10))
        
        if self.mensaje_tiempo > 0:
            texto_mensaje = self.fuente.render(self.mensaje, True, AMARILLO)
            rect_mensaje = texto_mensaje.get_rect(center=(ANCHO // 2, 80))
            pantalla.blit(texto_mensaje, rect_mensaje)
        
    def dibujar(self):
        pantalla.fill(AZUL_CIELO)
        
        # Nubes con parallax
        for i in range(10):
            x = 100 + i * 400 - int(self.camara.x * 0.5)
            y = 80 + (i % 2) * 40
            if -100 < x < ANCHO + 100:
                pygame.draw.ellipse(pantalla, BLANCO, (x, y, 60, 30))
                pygame.draw.ellipse(pantalla, BLANCO, (x + 20, y - 10, 50, 30))
                pygame.draw.ellipse(pantalla, BLANCO, (x + 40, y, 60, 30))
        
        # Colinas con parallax
        for i in range(20):
            x = 200 * i - int(self.camara.x * 0.7)
            if -200 < x < ANCHO + 200:
                pygame.draw.ellipse(pantalla, VERDE, (x, 480, 200, 100))
        
        # Dibujar elementos del nivel
        for plataforma in self.nivel.plataformas:
            rect_camara = pygame.Rect(
                plataforma.rect.x - self.camara.x,
                plataforma.rect.y,
                plataforma.rect.width,
                plataforma.rect.height
            )
            if -100 < rect_camara.x < ANCHO + 100:
                plataforma_temp = Plataforma(rect_camara.x, rect_camara.y, rect_camara.width, rect_camara.height, plataforma.tipo)
                plataforma_temp.golpeado = plataforma.golpeado if hasattr(plataforma, 'golpeado') else False
                plataforma_temp.dibujar(pantalla)
            
        for moneda in self.nivel.monedas:
            if -100 < moneda.rect.x - self.camara.x < ANCHO + 100:
                moneda_temp = Moneda(moneda.rect.x - self.camara.x, moneda.rect.y)
                moneda_temp.animacion_frame = moneda.animacion_frame
                moneda_temp.dibujar(pantalla)
            
        for powerup in self.nivel.powerups:
            if powerup.activo and -100 < powerup.rect.x - self.camara.x < ANCHO + 100:
                powerup_temp = PowerUp(powerup.rect.x - self.camara.x, powerup.rect.y, powerup.tipo)
                powerup_temp.activo = True
                powerup_temp.dibujar(pantalla)
            
        for enemigo in self.nivel.enemigos:
            if enemigo.vivo and -100 < enemigo.rect.x - self.camara.x < ANCHO + 100:
                enemigo_temp = Enemigo(enemigo.rect.x - self.camara.x, enemigo.rect.y, enemigo.tipo)
                enemigo_temp.animacion_frame = enemigo.animacion_frame
                enemigo_temp.aplastado = enemigo.aplastado
                enemigo_temp.rect.height = enemigo.rect.height
                enemigo_temp.dibujar(pantalla)
            
        if self.nivel.bandera:
            if -100 < self.nivel.bandera.rect.x - self.camara.x < ANCHO + 100:
                bandera_temp = Bandera(self.nivel.bandera.rect.x - self.camara.x, self.nivel.bandera.rect.y)
                bandera_temp.dibujar(pantalla)
        
        # Mario
        mario_temp = Mario(self.mario.rect.x - self.camara.x, self.mario.rect.y)
        mario_temp.direccion = self.mario.direccion
        mario_temp.velocidad_x = self.mario.velocidad_x
        mario_temp.animacion_frame = self.mario.animacion_frame
        mario_temp.grande = self.mario.grande
        mario_temp.tiene_flor = self.mario.tiene_flor
        mario_temp.invencible = self.mario.invencible
        mario_temp.vivo = self.mario.vivo
        mario_temp.alto = self.mario.alto
        mario_temp.rect.height = self.mario.rect.height
        mario_temp.saltando = self.mario.saltando
        mario_temp.dibujar(pantalla)
        
        self.dibujar_hud()
        
        # Barra de progreso
        progreso = (self.mario.rect.x / self.nivel.ancho_mapa) * 100
        pygame.draw.rect(pantalla, NEGRO, (ANCHO // 2 - 102, 42, 204, 14))
        pygame.draw.rect(pantalla, VERDE, (ANCHO // 2 - 100, 44, int(200 * (progreso / 100)), 10))
        pygame.draw.rect(pantalla, BLANCO, (ANCHO // 2 - 100, 44, 200, 10), 2)
        
        if self.pausa:
            overlay = pygame.Surface((ANCHO, ALTO))
            overlay.set_alpha(128)
            overlay.fill(NEGRO)
            pantalla.blit(overlay, (0, 0))
            
            texto_pausa = self.fuente_grande.render("PAUSA", True, BLANCO)
            rect_pausa = texto_pausa.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
            pantalla.blit(texto_pausa, rect_pausa)
            
            texto_continuar = self.fuente_pequena.render("Presiona P para continuar", True, BLANCO)
            rect_continuar = texto_continuar.get_rect(center=(ANCHO // 2, ALTO // 2 + 20))
            pantalla.blit(texto_continuar, rect_continuar)
            
        if self.game_over:
            overlay = pygame.Surface((ANCHO, ALTO))
            overlay.set_alpha(180)
            overlay.fill(NEGRO)
            pantalla.blit(overlay, (0, 0))
            
            texto_gameover = self.fuente_grande.render("GAME OVER", True, ROJO)
            rect_gameover = texto_gameover.get_rect(center=(ANCHO // 2, ALTO // 2 - 80))
            pantalla.blit(texto_gameover, rect_gameover)
            
            texto_puntos_final = self.fuente.render(f"Puntuación Final: {self.puntuacion}", True, BLANCO)
            rect_puntos = texto_puntos_final.get_rect(center=(ANCHO // 2, ALTO // 2 - 20))
            pantalla.blit(texto_puntos_final, rect_puntos)
            
            texto_nivel_final = self.fuente_pequena.render(f"Nivel Alcanzado: {self.nivel_actual}-1", True, BLANCO)
            rect_nivel = texto_nivel_final.get_rect(center=(ANCHO // 2, ALTO // 2 + 20))
            pantalla.blit(texto_nivel_final, rect_nivel)
            
            texto_reiniciar = self.fuente_pequena.render("Presiona R para Reiniciar", True, AMARILLO)
            rect_reiniciar = texto_reiniciar.get_rect(center=(ANCHO // 2, ALTO // 2 + 60))
            pantalla.blit(texto_reiniciar, rect_reiniciar)
            
            texto_salir = self.fuente_pequena.render("Presiona ESC para Salir", True, AMARILLO)
            rect_salir = texto_salir.get_rect(center=(ANCHO // 2, ALTO // 2 + 90))
            pantalla.blit(texto_salir, rect_salir)
        
    def ejecutar(self):
        ejecutando = True
        
        # Pantalla de inicio
        mostrar_inicio = True
        while mostrar_inicio:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        mostrar_inicio = False
                    if evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        
            pantalla.fill(AZUL_CIELO)
            
            texto_titulo = self.fuente_grande.render("SUPER MARIO BROS", True, ROJO)
            rect_titulo = texto_titulo.get_rect(center=(ANCHO // 2, 100))
            pantalla.blit(texto_titulo, rect_titulo)
            
            texto_subtitulo = self.fuente.render("Edición 2005", True, BLANCO)
            rect_subtitulo = texto_subtitulo.get_rect(center=(ANCHO // 2, 160))
            pantalla.blit(texto_subtitulo, rect_subtitulo)
            
            controles = [
                "CONTROLES:",
                "",
                "← → o A D - Mover",
                "ESPACIO - Saltar",
                "P - Pausa",
                "R - Reiniciar Nivel",
                "",
                "OBJETIVOS:",
                "",
                "• Llega a la bandera para completar el nivel",
                "• Recolecta monedas para sumar puntos",
                "• Elimina enemigos saltando sobre ellos",
                "• Recoge power-ups para hacerte más fuerte",
                "• ¡Completa los 3 niveles!",
            ]
            
            y = 220
            for linea in controles:
                if linea.startswith("CONTROLES") or linea.startswith("OBJETIVOS"):
                    texto = self.fuente_pequena.render(linea, True, AMARILLO)
                elif linea.startswith("•"):
                    texto = self.fuente_pequena.render(linea, True, VERDE)
                else:
                    texto = self.fuente_pequena.render(linea, True, BLANCO)
                rect = texto.get_rect(center=(ANCHO // 2, y))
                pantalla.blit(texto, rect)
                y += 25
                
            texto_empezar = self.fuente.render("Presiona ENTER para Empezar", True, AMARILLO)
            rect_empezar = texto_empezar.get_rect(center=(ANCHO // 2, ALTO - 40))
            pantalla.blit(texto_empezar, rect_empezar)
            
            pygame.display.flip()
            reloj.tick(FPS)
        
        # Loop principal
        while ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                    
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        self.mario.saltar()
                    if evento.key == pygame.K_r:
                        if self.game_over:
                            self.reiniciar_juego()
                        else:
                            self.reiniciar_nivel()
                    if evento.key == pygame.K_p:
                        self.pausa = not self.pausa
                    if evento.key == pygame.K_ESCAPE:
                        ejecutando = False
                        
            self.actualizar()
            self.dibujar()
            pygame.display.flip()
            reloj.tick(FPS)
            
        pygame.quit()
        sys.exit()

# Ejecutar el juego
if __name__ == "__main__":
    juego = Juego()
    juego.ejecutar()