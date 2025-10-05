"""
Constantes y configuración global del juego.
Contiene todas las constantes utilizadas en el proyecto.
"""

import pygame
import os
from enum import Enum
from typing import Tuple

# Rutas del proyecto
GAME_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS_DIR = os.path.join(GAME_DIR, "src", "assets")
SPRITES_DIR = os.path.join(ASSETS_DIR, "sprites")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sonidos")

# Dimensiones de pantalla
ANCHO = 800
ALTO = 600
FPS = 60

# Física del juego
GRAVEDAD = 0.8
VELOCIDAD_JUGADOR = 5
FUERZA_SALTO = 15
FRICCION = 0.85

# Colores principales - Estilo Mario Bros clásico
AZUL_CIELO = (92, 148, 252)  # Azul cielo como en el Mario original
# Colores estilo Mario Bros clásico
MARRON = (139, 69, 19)
MARRON_LADRILLO = (186, 85, 34)  # Color ladrillos como en Mario original
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 215, 0)
AMARILLO_BLOQUE = (218, 165, 32)  # Color bloques ? como en Mario original
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 200, 0)
VERDE_HIERBA = (0, 168, 0)  # Verde hierba como en Mario original
NARANJA = (255, 140, 0)
NARANJA_BLOQUE = (218, 85, 34)  # Color bloques naranjas como en Mario original
VERDE_TUBO = (0, 168, 0)
GRIS = (128, 128, 128)

# Estados de Mario
class EstadoMario(Enum):
    """Enumeración de estados posibles de Mario"""
    PEQUENO = "pequeno"
    GRANDE = "grande"
    FUEGO = "fuego"
    INVENCIBLE = "invencible"
    MURIENDO = "muriendo"

# Estados del juego
class EstadoJuego(Enum):
    """Enumeración de estados del juego"""
    MENU = "menu"
    JUGANDO = "jugando"
    PAUSA = "pausa"
    GAME_OVER = "game_over"
    NIVEL_COMPLETADO = "nivel_completado"

# Tipos de enemigos
class TipoEnemigo(Enum):
    """Enumeración de tipos de enemigos"""
    GOOMBA = "goomba"
    KOOPA = "koopa"

# Tipos de power-ups
class TipoPowerUp(Enum):
    """Enumeración de tipos de power-ups"""
    HONGO = "hongo"
    FLOR = "flor"
    ESTRELLA = "estrella"

# Sonidos del juego
SONIDOS = {
    'salto': 'salto.wav',
    'moneda': 'moneda.wav',
    'powerup': 'powerup.wav',
    'enemigo': 'enemigo.wav',
    'muerte': 'muerte.wav',
    'nivel_completado': 'nivel_completado.wav'
}

# Configuración de partículas
PARTICULAS_CONFIG = {
    'salto': {'cantidad': 5, 'color': BLANCO, 'velocidad': 3},
    'moneda': {'cantidad': 8, 'color': AMARILLO, 'velocidad': 4},
    'enemigo': {'cantidad': 10, 'color': GRIS, 'velocidad': 5},
    'powerup': {'cantidad': 12, 'color': VERDE, 'velocidad': 3}
}

def init_directories():
    """Crea los directorios necesarios si no existen."""
    directories = [ASSETS_DIR, SPRITES_DIR, SOUNDS_DIR]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

# Inicializar directorios al importar
init_directories()