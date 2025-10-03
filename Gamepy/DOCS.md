# Documentación Técnica 📚

## Estructura del Código

### Clase Principal: ImageVocabularyGame

#### Atributos Principales
- `score`: Puntuación del jugador
- `lives`: Vidas restantes
- `level`: Nivel actual
- `used_words`: Conjunto de palabras ya utilizadas
- `vocabulary`: Diccionario de palabras y sus propiedades

#### Métodos Principales

1. **Inicialización y Configuración**
   - `__init__()`: Inicializa el juego y sus atributos
   - `setup_window()`: Configura la ventana principal
   - `create_start_screen()`: Crea la pantalla inicial

2. **Gestión del Juego**
   - `start_game()`: Inicia una nueva partida
   - `new_round()`: Inicia una nueva ronda
   - `check_answer()`: Verifica las respuestas
   - `level_up()`: Maneja el cambio de nivel

3. **Sistema de Palabras**
   - `get_available_words()`: Obtiene palabras disponibles del nivel
   - `used_words`: Evita repetición de palabras ya usadas
   - `available_words_current_level`: Gestiona palabras del nivel actual

4. **Interfaz de Usuario**
   - `create_modern_button()`: Crea botones con diseño moderno
   - `create_heart_display()`: Muestra indicadores de vida
   - `show_feedback()`: Muestra retroalimentación al usuario

## Sistema de Niveles

| Nivel | Opciones | Tiempo | Nombre |
|-------|----------|---------|--------|
| 1 | 3 | - | Principiante |
| 2 | 4 | - | Fácil |
| 3 | 5 | 15s | Intermedio |
| 4 | 6 | 12s | Avanzado |
| 5 | 8 | 10s | Experto |

## Manejo de Eventos

- Gestión de clicks en botones
- Sistema de temporizador
- Eventos de scroll
- Efectos hover en botones

## Paleta de Colores

```python
colors = {
    'primary': '#667eea',      # Azul suave
    'primary_dark': '#5a6fd8', # Azul más oscuro
    'secondary': '#764ba2',    # Púrpura suave
    'accent': '#f093fb',       # Rosa pastel
    # ...etc
}
```
