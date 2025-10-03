# GameAdventurev2
Game
📝 Documentación del Proyecto
✨ English Adventure - Juego Interactivo de Vocabulario en Inglés (Tkinter)
📌 Descripción General

English Adventure es un juego educativo desarrollado en Python utilizando la biblioteca Tkinter. Su objetivo es ayudar a los usuarios a aprender vocabulario en inglés mediante imágenes (emojis) y selección múltiple. El diseño está orientado a ser visual, amigable y progresivo por niveles, con un sistema de puntos, vidas y temporizador para mantener la motivación.

🚀 Características Principales
Característica	Descripción
✅ Sistema de niveles	Desde Principiante (1) hasta Experto (5)
✅ Vidas con diseño visual (corazones)	El jugador pierde al quedarse sin vidas
✅ Temporizador opcional por nivel	Niveles avanzados tienen límite de tiempo
✅ Retroalimentación emergente	Mensajes positivos y errores con ventana flotante
✅ Progreso visual	Barra de puntuación y preguntas respondidas
✅ Reutilización controlada de palabras	No repite palabras correctas hasta agotar el nivel
🧱 Estructura de la Clase Principal

La clase central del juego es:

class ImageVocabularyGame:


A continuación, se documentan los componentes principales:

🔧 Atributos Principales
Atributo	Tipo	Descripción
self.score	int	Puntuación actual del jugador
self.lives	int	Número de vidas restantes
self.level	int	Nivel actual del jugador
self.questions_answered	int	Contador de preguntas correctas
self.vocabulary	dict	Base de datos de palabras con emoji, traducción y nivel
self.level_config	dict	Configuración de cada nivel (opciones y tiempo)
self.game_active	bool	Indica si el juego está en curso
🔁 Flujo Principal del Juego
flowchart TD
A[Inicio] --> B[Pantalla Principal]
B --> |Click en Comenzar| C[Generar Nueva Ronda]
C --> D[Mostrar Emoji + Opciones]
D -->|Respuesta Correcta| E[Sumar puntos + Avanzar]
D -->|Incorrecta o Tiempo| F[Restar Vida]
F -->|Vidas > 0| C
F -->|Vidas = 0| G[Game Over]
E -->|Preguntas >= Límite| H[Subir de Nivel]
H --> C

🧩 Funciones Clave
Función	Rol
create_start_screen()	Dibuja la pantalla inicial del juego
start_game()	Activa la primera ronda
new_round()	Selecciona nueva palabra y muestra opciones
check_answer()	Valida respuesta del jugador
level_up()	Sube de nivel con bonuses
game_over()	Finaliza el juego y ofrece reinicio
🎨 Interfaz Gráfica (Tkinter)

El juego utiliza múltiples componentes de Tkinter:

Elemento	Uso
Canvas + Scrollbar	Scroll vertical en ventana principal
Buttons	Opciones y controles de juego
Toplevel	Ventanas emergentes de feedback
Frames	Organización visual modular
📚 Base de Datos de Vocabulario

Cada palabra del juego tiene esta estructura:

"hunt": {"emoji": "🏹", "spanish": "cazar", "level": 4}


Esto permite:

✅ Filtrar por nivel
✅ Mostrar imagen (emoji)
✅ Mostrar traducción si el usuario falla

▶️ Ejecución del Juego

Se inicia desde:

if __name__ == "__main__":
    game = ImageVocabularyGame()
    game.run()
