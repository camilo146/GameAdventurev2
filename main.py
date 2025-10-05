"""
Archivo principal para ejecutar el juego Super Mario Bros 2005.
"""

import pygame
import sys
import os

# Agregar el directorio src al path para las importaciones
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.juego import Juego
from src.utils.constantes import ANCHO, ALTO, FPS
from src.utils.sonidos import gestor_sonidos

def main():
    """
    Función principal que inicializa y ejecuta el juego.
    """
    try:
        # Inicializar pygame
        pygame.init()
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Configurar la pantalla
        pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Super Mario Bros 2005")
        
        # Configurar el reloj para controlar FPS
        reloj = pygame.time.Clock()
        
        # Crear e inicializar el juego
        juego = Juego(pantalla, reloj)
        
        # Ejecutar el juego
        juego.ejecutar()
        
    except pygame.error as e:
        print(f"Error de Pygame: {e}")
        return 1
    except KeyboardInterrupt:
        print("\nJuego interrumpido por el usuario")
        return 0
    except Exception as e:
        print(f"Error inesperado: {e}")
        return 1
    finally:
        # Limpiar recursos
        gestor_sonidos.cleanup()
        pygame.quit()
        
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)