"""
Archivos de configuración del proyecto.
"""

# Este archivo contiene las configuraciones y documentación del proyecto

# Contenido para requirements.txt
REQUIREMENTS_TXT = """pygame>=2.5.0
typing-extensions>=4.0.0"""

# Contenido para README.md
README_MD = """# Super Mario Bros 2005

Un juego de plataformas inspirado en Super Mario Bros desarrollado en Python con Pygame.

## Características

### Jugabilidad
- Movimiento fluido de Mario con física realista
- Sistema de saltos con diferentes alturas
- Colisiones precisas con plataformas y enemigos
- Power-ups: Hongos, Flores de Fuego y Estrellas
- Sistema de vidas y puntuación
- Múltiples niveles con dificultad progresiva

### Efectos Visuales
- Sistema de partículas para efectos especiales
- Animaciones suaves para personajes
- Efectos de transformación de Mario
- Parallax scrolling para fondos
- Interfaz de usuario completa

### Audio
- Efectos de sonido para acciones (salto, monedas, power-ups)
- Música de fondo atmosférica
- Sistema de volumen configurable

### Estados de Mario
- **Pequeño**: Estado inicial, muere en un golpe
- **Grande**: Puede romper bloques, se vuelve pequeño al recibir daño
- **Fuego**: Puede lanzar bolas de fuego
- **Invencible**: Temporalmente inmune al daño

## Instalación

1. Asegúrate de tener Python 3.8+ instalado
2. Instala las dependencias:
   ```bash
   pip install pygame>=2.5.0
   ```
3. Ejecutar el juego:
   ```bash
   python main.py
   ```

## Controles

- **Flechas/WASD**: Movimiento
- **Espacio**: Saltar
- **Shift**: Correr
- **P**: Pausa
- **R**: Reiniciar nivel
- **Esc**: Salir al menú

## Estructura del Proyecto

```
Gamepy/
├── src/
│   ├── entities/          # Clases de entidades del juego
│   │   ├── mario.py       # Personaje principal
│   │   ├── enemigo.py     # Enemigos (Goombas, Koopas)
│   │   ├── plataforma.py  # Plataformas y bloques
│   │   ├── powerup.py     # Power-ups coleccionables
│   │   ├── moneda.py      # Monedas
│   │   └── bandera.py     # Bandera de meta
│   ├── core/              # Lógica central del juego
│   │   ├── juego.py       # Clase principal del juego
│   │   ├── nivel.py       # Gestión de niveles
│   │   └── camara.py      # Sistema de cámara
│   ├── utils/             # Utilidades y herramientas
│   │   ├── constantes.py  # Constantes del juego
│   │   ├── particulas.py  # Sistema de partículas
│   │   └── sonidos.py     # Gestión de audio
│   └── assets/            # Resources del juego
│       ├── sprites/       # Imágenes y sprites
│       └── sonidos/       # Archivos de audio
├── tests/                 # Tests unitarios
└── main.py               # Punto de entrada
```

## Desarrollo

### Ejecutar Tests
```bash
python -m pytest tests/ -v
```

### Agregar Nuevos Niveles
Los niveles se definen en `src/core/nivel.py`. Cada nivel especifica:
- Posiciones de plataformas
- Ubicación de enemigos
- Power-ups disponibles
- Posición de la meta

### Agregar Nuevos Enemigos
1. Crear clase en `src/entities/`
2. Heredar de `pygame.sprite.Sprite`
3. Implementar lógica de movimiento y colisión
4. Agregar al sistema de niveles

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -am 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crea un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para detalles.

## Créditos

- Desarrollado con Python y Pygame
- Inspirado en el clásico Super Mario Bros de Nintendo
- Assets y sonidos de dominio público
"""

# Crear archivo de configuración para development
SETUP_CONFIG = """
"""
Setup configuration for Mario Bros game.
"""

from setuptools import setup, find_packages

setup(
    name="mario-bros-2005",
    version="1.0.0",
    description="Un juego de plataformas inspirado en Super Mario Bros",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Game Developer",
    author_email="developer@mariobros.com",
    url="https://github.com/usuario/mario-bros-2005",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pygame>=2.5.0",
        "typing-extensions>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ]
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Games/Entertainment :: Arcade",
    ],
    entry_points={
        "console_scripts": [
            "mario-bros=main:main",
        ],
    },
)
"""