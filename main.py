import pygame
import sys
from src.core.juego import Juego
from src.utils.constantes import ANCHO, ALTO, FPS

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Super Mario Bros 2005")
    reloj = pygame.time.Clock()
    
    juego = Juego(pantalla, reloj)
    juego.ejecutar()

if __name__ == "__main__":
    main()
