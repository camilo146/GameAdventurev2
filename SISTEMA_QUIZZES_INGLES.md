# Sistema de Quizzes en Inglés - Mario Adventure

## 📚 Descripción General

El juego ahora incluye un sistema educativo completo de quizzes en inglés enfocado en la gramática de "will" vs "going to". Los jugadores deben responder preguntas correctamente para abrir puertas y progresar en el juego.

## 🚪 Tipos de Puertas

### 1. **Puertas Obligatorias** (Café/Marrón)
- **Función**: Bloquean el camino principal del nivel
- **Ubicación**: En rutas críticas que el jugador debe atravesar
- **Requisito**: Responder quiz correctamente
- **Penalización**: Perder 1 vida por respuesta incorrecta

### 2. **Puertas Opcionales Secretas** (Morado/Púrpura)
- **Función**: Acceso a áreas secretas con bonus
- **Ubicación**: Caminos alternativos o áreas ocultas
- **Requisito**: Responder quiz correctamente
- **Recompensa**: Acceso a power-ups especiales

### 3. **Puertas Opcionales Bonus** (Verde)
- **Función**: Acceso a recompensas adicionales
- **Ubicación**: Áreas de bonus visibles
- **Requisito**: Llaves acumuladas + quiz correcto
- **Recompensa**: Monedas y power-ups extra

### 4. **Puertas de Llave Especial** (Naranja)
- **Función**: Otorgan llaves al completar el quiz
- **Ubicación**: Distribuidas estratégicamente
- **Requisito**: Solo responder quiz correctamente
- **Recompensa**: +1 llave para abrir otras puertas

## 🔑 Sistema de Llaves

- **Acumulación**: Las llaves se obtienen de puertas especiales naranjas
- **Uso**: Requeridas para abrir puertas bonus verdes
- **Visualización**: Contador en la esquina superior derecha de la pantalla
- **Estrategia**: Planifica qué puertas abrir según tus llaves disponibles

## 🎯 Preguntas del Quiz

### Contenido Educativo
- **Tema**: Diferencias entre "will" y "going to"
- **Niveles**: 5 dificultades progresivas
- **Cantidad**: 40+ preguntas únicas con explicaciones

### Estructura de Dificultad por Nivel:
1. **Nivel 1-2**: Conceptos básicos de "going to"
2. **Nivel 3**: Conceptos básicos de "will"
3. **Nivel 4**: Usos intermedios y comparaciones
4. **Nivel 5**: Preguntas mixtas avanzadas

### Formato de Preguntas:
- 4 opciones de respuesta múltiple
- Explicación detallada tras cada respuesta
- Feedback visual (verde=correcto, rojo=incorrecto)

## 🎮 Controles

### Interacción con Puertas:
- **E**: Acercarse a una puerta e interactuar para iniciar quiz
- **1, 2, 3, 4**: Seleccionar respuesta durante el quiz
- **Espacio**: Continuar después de ver la explicación

### Indicadores Visuales:
- **Brillo**: Las puertas brillan cuando Mario está cerca
- **Color**: Cada tipo de puerta tiene un color distintivo
- **Símbolos**: Iconos indican el tipo de puerta y llaves requeridas

## 📊 Distribución de Puertas por Nivel

### Nivel 1 (Tutorial)
- 1 Puerta Obligatoria (introducción básica)
- 2 Puertas Opcionales (práctica)
- 1 Puerta de Llave (primera llave)

### Nivel 2 (Desarrollo)
- 1 Puerta Obligatoria (progresión)
- 1 Puerta Bonus (uso de llaves)
- 1 Puerta de Llave (segunda llave)

### Nivel 3 (Desafío)
- 2 Puertas Obligatorias (desafío aumentado)
- 1 Puerta de Llave (tercera llave)

### Nivel 4 (Maestría)
- 2 Puertas Obligatorias (dominio requerido)
- 1 Puerta Secreta (bonus avanzado)
- 1 Puerta de Llave (cuarta llave)

### Nivel 5 (Experto)
- 1 Puerta Obligatoria (demostración final)
- 3 Puertas Bonus (uso estratégico de llaves)

## 🎨 Efectos Visuales

### Animaciones:
- **Apertura de puertas**: Animación suave de 60 frames
- **Partículas de éxito**: Explosión verde al responder correctamente
- **Feedback de error**: Efecto visual rojo para respuestas incorrectas
- **Brillo de proximidad**: Aura dorada cuando Mario se acerca

### Interfaz de Quiz:
- **Popup centralizado**: Ventana semitransparente
- **Texto claramente legible**: Fondo negro con texto blanco
- **Opciones numeradas**: 1-4 para fácil selección
- **Animaciones de transición**: Efectos suaves entre estados

## 📈 Sistema de Estadísticas

El juego rastrea:
- Respuestas correctas e incorrectas
- Llaves acumuladas totales
- Puertas abiertas por tipo
- Progreso educativo por nivel

## 🔧 Configuración Técnica

### Archivos Principales:
- `src/utils/preguntas.py`: Base de datos de preguntas
- `src/entities/puerta.py`: Lógica de puertas
- `src/utils/quiz_manager.py`: Control del sistema de quiz
- `src/core/juego.py`: Integración principal
- `src/core/nivel.py`: Distribución de puertas por nivel

### Constantes Configurables:
- Colores de interfaz
- Velocidad de animaciones
- Posición del contador de llaves
- Tiempo de mostrar explicaciones

## 🎯 Objetivos Educativos

### Aprendizaje Progresivo:
1. **Reconocimiento**: Identificar cuándo usar cada forma
2. **Aplicación**: Usar correctamente en contexto
3. **Distinción**: Diferenciar matices entre "will" y "going to"
4. **Maestría**: Aplicar en situaciones complejas

### Motivación Gamificada:
- Progresión bloqueada por conocimiento
- Recompensas por respuestas correctas
- Penalizaciones que motivan el aprendizaje
- Sistema de llaves que fomenta la exploración educativa

## 🚀 Cómo Jugar

1. **Explora el nivel** hasta encontrar una puerta
2. **Acércate** y presiona **E** para interactuar
3. **Lee la pregunta** cuidadosamente
4. **Selecciona tu respuesta** con las teclas 1-4
5. **Aprende de la explicación** sin importar si acertaste
6. **Usa las llaves** estratégicamente para puertas bonus
7. **Progresa** aplicando tu conocimiento de inglés

¡El conocimiento es tu llave para la aventura! 🗝️📚✨