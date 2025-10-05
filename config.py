import os

# Rutas
GAME_DIR = os.path.dirname(os.path.abspath(__file__))
SPRITES_DIR = os.path.join(GAME_DIR, "sprites")
SOUNDS_DIR = os.path.join(GAME_DIR, "sonidos")

# Asegurar que las carpetas existan
def init_directories():
    directories = [SPRITES_DIR, SOUNDS_DIR]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

# Crear carpetas necesarias al importar
init_directories()
