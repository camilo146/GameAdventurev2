import pygame
import os

# Rutas
GAME_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS_DIR = os.path.join(GAME_DIR, "src", "assets")
SPRITES_DIR = os.path.join(ASSETS_DIR, "sprites")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sonidos")

# Dimensiones
ANCHO = 800
ALTO = 600
FPS = 60

# Física
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

# Crear directorios necesarios
def init_directories():
    for directory in [ASSETS_DIR, SPRITES_DIR, SOUNDS_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)

init_directories()
