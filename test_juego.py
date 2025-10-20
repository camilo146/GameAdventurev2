"""
Test simplificado del juego completo.
"""
import pygame
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.juego import Juego
from src.utils.constantes import *

pygame.init()
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Test Mario")
reloj = pygame.time.Clock()

juego = Juego(pantalla, reloj)

print("Juego iniciado")
print(f"Estado inicial: {juego.estado}")
print("\nPresiona SPACE para iniciar")
print("Usa las FLECHAS o A/D para mover")
print("ESC para salir\n")

juego.ejecutar()

pygame.quit()
