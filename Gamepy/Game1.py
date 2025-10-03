import tkinter as tk
from tkinter import messagebox
import random

class ImageVocabularyGame:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.max_lives = 3
        self.level = 1
        self.questions_answered = 0
        self.questions_per_level = 5
        self.current_word = None
        self.game_active = False
        self.used_words = set()  # Conjunto para palabras usadas
        self.available_words_current_level = []  # Lista de palabras disponibles para el nivel actual
        
        # Paleta de colores moderna y relajante
        self.colors = {
            'primary': '#667eea',      # Azul suave
            'primary_dark': '#5a6fd8', # Azul más oscuro
            'secondary': '#764ba2',    # Púrpura suave
            'accent': '#f093fb',       # Rosa pastel
            'background': '#f8fafc',   # Blanco humo
            'surface': '#ffffff',      # Blanco puro
            'success': '#10b981',      # Verde esmeralda
            'error': '#ef4444',        # Rojo coral
            'warning': '#f59e0b',      # Naranja dorado
            'text_primary': '#1e293b', # Gris oscuro
            'text_secondary': '#64748b', # Gris medio
            'border': '#e2e8f0',       # Gris claro
            'shadow': '#00000010'      # Sombra sutil
        }
        
        # Configuración de niveles
        self.level_config = {
            1: {"options": 3, "time": None, "name": "Principiante", "color": "#10b981"},
            2: {"options": 4, "time": None, "name": "Fácil", "color": "#3b82f6"},
            3: {"options": 5, "time": 15, "name": "Intermedio", "color": "#8b5cf6"},
            4: {"options": 6, "time": 12, "name": "Avanzado", "color": "#f59e0b"},
            5: {"options": 8, "time": 10, "name": "Experto", "color": "#ef4444"}
        }
        self.max_level = 5
        
        self.timer_active = False
        self.time_left = 0
        
        # Base de datos de vocabulario
        self.vocabulary = {
  
            
            
            # Going to - Actividades
            "hunt": {"emoji": "🏹", "spanish": "cazar", "level": 4},
            "sleep": {"emoji": "😴", "spanish": "dormir", "level": 4},
            "eat": {"emoji": "🍖", "spanish": "comer", "level": 4},
            "run": {"emoji": "🏃", "spanish": "correr", "level": 4},
            "swim": {"emoji": "🏊", "spanish": "nadar", "level": 4},
            
            # Going to - Planes
            "travel": {"emoji": "✈️", "spanish": "viajar", "level": 5},
            "explore": {"emoji": "🔍", "spanish": "explorar", "level": 5},
            "study": {"emoji": "📚", "spanish": "estudiar", "level": 5},
            "visit": {"emoji": "👋", "spanish": "visitar", "level": 5},
            "watch": {"emoji": "👀", "spanish": "observar", "level": 5},
            
            # Going to - Tiempo
            "tomorrow": {"emoji": "📅", "spanish": "mañana", "level": 1},
            "tonight": {"emoji": "🌙", "spanish": "esta noche", "level": 1},
            "later": {"emoji": "⏰", "spanish": "más tarde", "level": 2},
            "weekend": {"emoji": "📆", "spanish": "fin de semana", "level": 2},
            "soon": {"emoji": "🔜", "spanish": "pronto", "level": 3},
        }
        
        self.setup_window()
        self.create_start_screen()
        
    def setup_window(self):
        self.root = tk.Tk()
        self.root.title("✨ English Adventure - Learning Made Beautiful")
        self.root.geometry("900x800")  # Aumentado el alto
        self.root.configure(bg=self.colors['background'])
        self.root.resizable(False, False)
        
        # Aplicar estilo moderno a la ventana
        try:
            self.root.attributes('-alpha', 0.98)
        except:
            pass
        
        self.center_window()

    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        window_width = 900
        window_height = 800  # Ajustado para coincidir con geometry
        
        # Asegurarse de que la ventana quepa en la pantalla
        if window_height > screen_height:
            window_height = screen_height - 100
            
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        
        if y < 0:
            y = 0
            
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_modern_button(self, parent, text, command, bg_color=None, width=None, height=None):
        """Crear botón con diseño moderno"""
        if bg_color is None:
            bg_color = self.colors['primary']
            
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 11, "normal"),
            bg=bg_color,
            fg="white",
            activebackground=self.colors['primary_dark'],
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        
        if width:
            btn.config(width=width)
        if height:
            btn.config(height=height)
            
        # Efectos hover simulados
        def on_enter(e):
            btn.config(bg=self.colors['primary_dark'])
        def on_leave(e):
            btn.config(bg=bg_color)
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
            
    def create_heart_display(self, parent, is_full=True):
        """Crear indicador de vida moderno"""
        heart_frame = tk.Frame(parent, bg=self.colors['surface'], width=35, height=30)
        heart_frame.pack_propagate(False)
        
        heart_color = self.colors['error'] if is_full else self.colors['border']
        heart_symbol = "💖" if is_full else "🤍"
        
        heart_label = tk.Label(
            heart_frame,
            text=heart_symbol,
            font=("Segoe UI Emoji", 16),
            bg=self.colors['surface'],
            fg=heart_color
        )
        heart_label.pack(expand=True)
        return heart_frame
            
    def create_start_screen(self):
        self.clear_window()
        
        # Canvas principal con dimensiones fijas
        main_canvas = tk.Canvas(
            self.root,
            bg=self.colors['background'],
            width=880,  # Ancho ajustado para el scrollbar
            height=780,  # Alto ajustado
            highlightthickness=0
        )
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        
        # Frame principal dentro del canvas
        main_frame = tk.Frame(main_canvas, bg=self.colors['background'])
        main_frame.configure(width=880)  # Ancho fijo
        
        # Container principal con padding
        main_container = tk.Frame(main_frame, bg=self.colors['background'])
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Configurar scroll y eventos
        def on_frame_configure(event):
            main_canvas.configure(scrollregion=main_canvas.bbox("all"))
            # Asegurar que el ancho del frame sea correcto
            canvas_width = main_canvas.winfo_width()
            main_canvas.itemconfig(frame_window, width=canvas_width)
        
        main_frame.bind("<Configure>", on_frame_configure)
        
        # Crear ventana en el canvas con ancho específico
        frame_window = main_canvas.create_window(
            (0, 0),
            window=main_frame,
            anchor="nw",
            width=880  # Ancho fijo
        )
        
        # Configurar scrollbar
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar elementos
        scrollbar.pack(side="right", fill="y")
        main_canvas.pack(side="left", fill="both", expand=True)
        
        # Configurar scroll con el mouse
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # A partir de aquí continúa el código original del contenido
        # Header con gradiente simulado
        header_frame = tk.Frame(main_container, bg=self.colors['surface'], height=120)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Título principal
        title_frame = tk.Frame(header_frame, bg=self.colors['surface'])
        title_frame.pack(expand=True)
        
        title_label = tk.Label(
            title_frame,
            text="✨ English Adventure",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['primary']
        )
        title_label.pack(pady=(20, 5))
        
        subtitle_label = tk.Label(
            title_frame,
            text="Aprende inglés de forma divertida",
            font=("Segoe UI", 12),
            bg=self.colors['surface'],
            fg=self.colors['text_secondary']
        )
        subtitle_label.pack()
        
        # Información del nivel actual
        level_info = self.level_config.get(self.level, self.level_config[1])
        level_color = level_info.get('color', self.colors['primary'])
        
        level_badge = tk.Frame(header_frame, bg=level_color, height=40)
        level_badge.pack(fill="x", padx=20, pady=(10, 20))
        level_badge.pack_propagate(False)
        
        level_text = f"Nivel {self.level}: {level_info['name']}"
        level_label = tk.Label(
            level_badge,
            text=level_text,
            font=("Segoe UI", 14, "bold"),
            bg=level_color,
            fg="white"
        )
        level_label.pack(expand=True)
        
        # Card de juego principal
        game_card = tk.Frame(main_container, bg=self.colors['surface'], relief="flat")
        game_card.pack(fill="both", expand=True, pady=(0, 20))
        
        # Área de imagen
        image_section = tk.Frame(game_card, bg=self.colors['surface'])
        image_section.pack(fill="x", pady=30)
        
        # Container de imagen con sombra simulada
        image_container = tk.Frame(image_section, bg=self.colors['background'], width=140, height=140)
        image_container.pack()
        image_container.pack_propagate(False)
        
        self.image_frame = tk.Frame(
            image_container,
            bg=self.colors['surface'],
            width=130,
            height=130,
            relief="flat"
        )
        self.image_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.image_frame.pack_propagate(False)
        
        self.image_label = tk.Label(
            self.image_frame,
            text="❓",
            font=("Segoe UI Emoji", 60),
            bg=self.colors['surface'],
            fg=self.colors['text_secondary']
        )
        self.image_label.pack(expand=True)
        
        # Panel de vidas moderno
        lives_section = tk.Frame(game_card, bg=self.colors['surface'])
        lives_section.pack(pady=20)
        
        lives_title = tk.Label(
            lives_section,
            text="Vidas",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['text_primary']
        )
        lives_title.pack()
        
        self.lives_container = tk.Frame(lives_section, bg=self.colors['surface'])
        self.lives_container.pack(pady=(10, 0))
        
        self.update_lives_display()
        
        # Botón de inicio moderno
        button_section = tk.Frame(game_card, bg=self.colors['surface'])
        button_section.pack(pady=30)
        
        self.start_button = self.create_modern_button(
            button_section,
            "🚀 Comenzar Aventura",
            self.start_game,
            self.colors['primary'],
            width=20,
            height=2
        )
        self.start_button.pack()
        
        # Timer (inicialmente oculto)
        self.timer_label = tk.Label(
            game_card,
            text="",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors['surface'],
            fg=self.colors['warning']
        )
        
        # Área de juego
        self.game_area = tk.Frame(game_card, bg=self.colors['surface'])
        self.game_area.pack(fill="both", expand=True,)
        
        # Panel de estadísticas inferior
        stats_panel = tk.Frame(main_container, bg=self.colors['surface'], height=100)  # Aumentado el alto
        stats_panel.pack(fill="x", pady=(0, 20), padx=20)  # Añadido padding
        stats_panel.pack_propagate(False)
        
        stats_inner = tk.Frame(stats_panel, bg=self.colors['surface'])
        stats_inner.pack(expand=True, fill="both", padx=50, pady=10)  # Aumentado padding
        
        # Score y Progreso con más espacio
        score_frame = tk.Frame(stats_inner, bg=self.colors['surface'], width=200, height=80)  # Aumentado tamaño
        score_frame.pack(side="left", expand=True, anchor="center", padx=20)
        score_frame.pack_propagate(False)
        
        tk.Label(
            score_frame,
            text="Puntos",
            font=("Segoe UI", 12),  # Aumentado tamaño de fuente
            bg=self.colors['surface'],
            fg=self.colors['text_secondary']
        ).pack(pady=(5,0))
        
        self.score_label = tk.Label(
            score_frame,
            text=str(self.score),
            font=("Segoe UI", 18, "bold"),  # Aumentado tamaño de fuente
            bg=self.colors['surface'],
            fg=self.colors['success']
        )
        self.score_label.pack()
        
        # Progreso - Ajustado el espacio y tamaño
        progress_frame = tk.Frame(stats_inner, bg=self.colors['surface'], width=200, height=80)  # Aumentado tamaño
        progress_frame.pack(side="right", expand=True, anchor="center", padx=20)
        progress_frame.pack_propagate(False)
        
        tk.Label(
            progress_frame,
            text="Progreso",
            font=("Segoe UI", 12),  # Aumentado tamaño de fuente
            bg=self.colors['surface'],
            fg=self.colors['text_secondary']
        ).pack(pady=(5,0))
        
        self.progress_label = tk.Label(
            progress_frame,
            text=f"{self.questions_answered}/{self.questions_per_level}",
            font=("Segoe UI", 18, "bold"),  # Aumentado tamaño de fuente
            bg=self.colors['surface'],
            fg=self.colors['primary']
        )
        self.progress_label.pack()
        
    def update_lives_display(self):
        # Limpiar contenedor de vidas
        for widget in self.lives_container.winfo_children():
            widget.destroy()
            
        # Crear indicadores de vida
        for i in range(self.max_lives):
            is_full = i < self.lives
            heart = self.create_heart_display(self.lives_container, is_full)
            heart.pack(side="left", padx=3)
        
    def get_available_words(self):
        """Obtener palabras disponibles según el nivel actual excluyendo las ya usadas"""
        if not self.available_words_current_level:
            # Si no hay palabras disponibles, obtener todas las del nivel actual
            self.available_words_current_level = [
                word for word, data in self.vocabulary.items()
                if data["level"] <= self.level and word not in self.used_words
            ]
            # Si se agotaron todas las palabras del nivel, reiniciar
            if not self.available_words_current_level:
                self.used_words.clear()
                self.available_words_current_level = [
                    word for word, data in self.vocabulary.items()
                    if data["level"] <= self.level
                ]
        return self.available_words_current_level

    def start_game(self):
        if not self.game_active:
            self.game_active = True
            self.start_button.config(
                text="🎮 Jugando...",
                bg=self.colors['text_secondary'],
                state="disabled"
            )
            print(f"🎮 Iniciando juego - Nivel {self.level}, Preguntas: {self.questions_answered}")
            self.new_round()
        
    def new_round(self):
        if self.lives <= 0:
            self.game_over()
            return
            
        if self.questions_answered >= self.questions_per_level:
            self.level_up()
            return
        
        # Obtener palabras disponibles y seleccionar una al azar    
        available_words = self.get_available_words()
        self.current_word = random.choice(available_words)
        
        # Remover la palabra seleccionada de las disponibles
        self.available_words_current_level.remove(self.current_word)
        
        current_data = self.vocabulary[self.current_word]
        self.image_label.config(text=current_data["emoji"], font=("Segoe UI Emoji", 80))
        
        # Configurar opciones del nivel
        level_config = self.level_config.get(self.level, self.level_config[1])
        num_options = level_config["options"]
        
        # Generar opciones incorrectas excluyendo palabras ya usadas
        wrong_options = [w for w in self.get_available_words() if w != self.current_word]
        
        if len(wrong_options) < num_options - 1:
            # Si no hay suficientes opciones, incluir también palabras ya usadas
            all_level_words = [w for w, d in self.vocabulary.items() 
                             if d["level"] <= self.level and w != self.current_word]
            wrong_options.extend(all_level_words)
            wrong_options = list(set(wrong_options))  # Eliminar duplicados
            
        selected_wrong = random.sample(wrong_options, min(num_options - 1, len(wrong_options)))
        options = [self.current_word] + selected_wrong
        random.shuffle(options)
        
        self.create_option_buttons(options)
        
        if level_config["time"]:
            self.start_timer(level_config["time"])
            
    def create_option_buttons(self, options):
        # Limpiar área de juego
        for widget in self.game_area.winfo_children():
            widget.destroy()
            
        self.answer_buttons = []
        
        # Container para botones con scroll
        buttons_container = tk.Frame(self.game_area, bg=self.colors['surface'])
        buttons_container.pack(expand=True, fill="both", padx=20, pady=10)
        
        # Calcular disposición
        num_options = len(options)
        if num_options <= 4:
            cols = 2
            button_width = 16
        elif num_options <= 6:
            cols = 2
            button_width = 16
        else:
            cols = 3
            button_width = 12
            
        # Frame para la cuadrícula de botones con más espacio
        grid_frame = tk.Frame(buttons_container, bg=self.colors['surface'])
        grid_frame.pack(expand=True, pady=20)  # Aumentado padding
        
        for i, option in enumerate(options):
            row = i // cols
            col = i % cols
            
            # Crear botón moderno
            btn = tk.Button(
                grid_frame,
                text=option.capitalize(),
                font=("Segoe UI", 12, "normal"),  # Aumentado tamaño de fuente
                width=button_width,
                height=2,
                bg=self.colors['surface'],
                fg=self.colors['text_primary'],
                activebackground=self.colors['primary'],
                activeforeground="white",
                relief="solid",
                bd=1,
                borderwidth=2,
                command=lambda word=option: self.check_answer(word),
                cursor="hand2"
            )
            
            # Efectos hover
            def on_enter(e, button=btn):
                button.config(bg=self.colors['primary'], fg="white", borderwidth=0)
            def on_leave(e, button=btn):
                button.config(bg=self.colors['surface'], fg=self.colors['text_primary'], borderwidth=2)
                
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            
            btn.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")  # Aumentado padding
            self.answer_buttons.append(btn)
            
        # Configurar grid
        for i in range(cols):
            grid_frame.grid_columnconfigure(i, weight=1)
            
    def start_timer(self, seconds):
        self.timer_active = True
        self.time_left = seconds
        self.timer_label.pack(before=self.game_area, pady=(0, 10))
        self.update_timer()
        
    def update_timer(self):
        if self.timer_active and self.time_left > 0:
            self.timer_label.config(text=f"⏱️ {self.time_left}s")
            if self.time_left <= 5:
                self.timer_label.config(fg=self.colors['error'])
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        elif self.timer_active and self.time_left <= 0:
            self.timer_label.config(text="⏰ ¡Tiempo agotado!")
            self.time_up()
            
    def time_up(self):
        self.timer_active = False
        self.lives -= 1
        self.update_lives_display()
        correct_spanish = self.vocabulary[self.current_word]["spanish"]
        self.show_feedback(f"⏰ ¡Se acabó el tiempo!\n\nLa respuesta era: {self.current_word}\n({correct_spanish})", self.colors['warning'])
        
        if self.lives > 0:
            self.root.after(2500, self.continue_game)
        else:
            self.root.after(2500, self.game_over)
            
    def check_answer(self, selected_word):
        self.timer_active = False
        self.timer_label.pack_forget()
        
        if selected_word == self.current_word:
            # Respuesta correcta
            points = 10 * self.level
            self.score += points
            self.questions_answered += 1
            self.used_words.add(selected_word)  # Marcar como usada solo si es correcta
            
            self.update_stats_display()
            self.show_feedback(f"¡Excelente! ✨\n\n+{points} puntos", self.colors['success'])
            self.root.after(1500, self.continue_game)
        else:
            # Respuesta incorrecta
            self.lives -= 1
            self.update_lives_display()
            correct_spanish = self.vocabulary[self.current_word]["spanish"]
            self.show_feedback(f"¡Ups! 😅\n\nLa respuesta era: {self.current_word}\n({correct_spanish})", self.colors['error'])
            
            if self.lives > 0:
                self.root.after(2500, self.continue_game)
            else:
                self.root.after(2500, self.game_over)
                
    def continue_game(self):
        self.new_round()
        
    def level_up(self):
        if self.level >= self.max_level:
            self.max_level_reached()
            return
            
        self.level += 1
        self.questions_answered = 0
        self.used_words.clear()  # Limpiar palabras usadas al subir de nivel
        self.available_words_current_level = []  # Reiniciar palabras disponibles
        
        # Bonus por subir de nivel
        bonus = 50 * self.level
        self.score += bonus
        
        # Recuperar una vida
        if self.lives < self.max_lives:
            self.lives += 1
            
        level_name = self.level_config.get(self.level, {"name": "Master"})["name"]
        
        self.game_active = False
        
        messagebox.showinfo("¡Nivel Completado! 🎉", 
                          f"✨ ¡Felicitaciones!\n\n"
                          f"Has alcanzado el Nivel {self.level}: {level_name}\n\n"
                          f"🎁 Bonus: +{bonus} puntos\n"
                          f"💖 ¡Vida recuperada!\n\n"
                          f"📊 Puntuación total: {self.score}")
        
        self.create_start_screen()
        self.root.after(500, self.start_game)
    
    def max_level_reached(self):
        """Cuando el jugador completa el nivel 5"""
        final_bonus = 200
        self.score += final_bonus
        
        messagebox.showinfo("¡Juego Completado! 🏆", 
                          f"🌟 ¡Increíble logro!\n\n"
                          f"¡Has completado todos los niveles!\n"
                          f"Eres un verdadero experto en inglés\n\n"
                          f"🎁 Bonus final: +{final_bonus} puntos\n"
                          f"🏆 Puntuación final: {self.score}")
        
        result = messagebox.askquestion("¿Nueva aventura?", 
                                      "¿Quieres comenzar una nueva aventura desde el nivel 1?")
        if result == 'yes':
            self.reset_game()
        else:
            self.root.quit()
        
    def update_stats_display(self):
        self.score_label.config(text=str(self.score))
        self.progress_label.config(text=f"{self.questions_answered}/{self.questions_per_level}")
        
    def show_feedback(self, message, color):
        # Deshabilitar todos los botones
        for btn in self.answer_buttons:
            btn.config(state="disabled", bg=self.colors['border'], fg=self.colors['text_secondary'])
            
        try:
            # Crear ventana de feedback moderna
            feedback_window = tk.Toplevel(self.root)
            feedback_window.title("Resultado")
            feedback_window.geometry("380x220")
            feedback_window.configure(bg=self.colors['background'])
            feedback_window.resizable(False, False)
            
            # Centrar ventana
            x = self.root.winfo_x() + 170
            y = self.root.winfo_y() + 250
            feedback_window.geometry(f"380x220+{x}+{y}")
            
            # Aplicar transparencia
            try:
                feedback_window.attributes('-alpha', 0.95)
            except:
                pass
            
            # Container principal
            container = tk.Frame(feedback_window, bg=self.colors['surface'], relief="flat")
            container.pack(fill="both", expand=True, padx=15, pady=15)
            
            # Área de mensaje
            message_frame = tk.Frame(container, bg=color, height=120)
            message_frame.pack(fill="x", pady=(0, 15))
            message_frame.pack_propagate(False)
            
            label = tk.Label(
                message_frame,
                text=message,
                font=("Segoe UI", 12, "normal"),
                bg=color,
                fg="white",
                wraplength=340,
                justify="center"
            )
            label.pack(expand=True)
            
            # Barra de progreso simulada
            progress_frame = tk.Frame(container, bg=self.colors['border'], height=6)
            progress_frame.pack(fill="x")
            
            progress_bar = tk.Frame(progress_frame, bg=color, height=6)
            progress_bar.pack(side="left", fill="y")
            
            # Animación de progreso
            def animate_progress(width=0):
                if width <= 380:
                    progress_bar.config(width=width)
                    feedback_window.after(10, lambda: animate_progress(width + 8))
                    
            animate_progress()
            
            # Cerrar automáticamente
            def safe_destroy():
                try:
                    if feedback_window.winfo_exists():
                        feedback_window.destroy()
                except tk.TclError:
                    pass
            
            if "Excelente" in message:
                feedback_window.after(1500, safe_destroy)
            else:
                feedback_window.after(2500, safe_destroy)
                
        except tk.TclError as e:
            print(f"Error en ventana de feedback: {e}")
            
    def game_over(self):
        self.game_active = False
        self.timer_active = False
        
        # Calcular estadísticas finales
        total_questions = (self.level - 1) * self.questions_per_level + self.questions_answered
        
        result = messagebox.askquestion("¡Game Over! 💫", 
                                      f"🌙 Fin de la aventura\n\n"
                                      f"📈 Nivel alcanzado: {self.level}\n"
                                      f"🎯 Puntuación final: {self.score}\n"
                                      f"❓ Preguntas respondidas: {total_questions}\n\n"
                                      f"¿Quieres comenzar una nueva aventura?")
        
        if result == 'yes':
            self.reset_game()
        else:
            self.root.quit()
            
    def reset_game(self):
        """Reinicia el juego a su estado inicial"""
        self.score = 0
        self.lives = 3
        self.level = 1
        self.questions_answered = 0
        self.current_word = None
        self.game_active = False
        self.timer_active = False
        self.used_words.clear()  # Limpiar palabras usadas al reiniciar
        self.available_words_current_level = []
        self.create_start_screen()
        
    def run(self):
        """Ejecuta el juego con manejo de errores mejorado"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n✨ ¡Gracias por jugar! Hasta pronto 👋")
        except Exception as e:
            print(f"Error durante el juego: {e}")
        finally:
            try:
                self.root.quit()
            except:
                pass

# Ejecutar el juego
if __name__ == "__main__":
    try:
        print("✨ Iniciando English Adventure...")
        print("Una experiencia de aprendizaje moderna y relajante")
        print("Presiona Ctrl+C para salir en cualquier momento")
        game = ImageVocabularyGame()
        game.run()
    except Exception as e:
        print(f"Error al iniciar el juego: {e}")
        print("Asegúrate de tener tkinter instalado")
    except KeyboardInterrupt:
        print("\n🌟 ¡Hasta luego! Que tengas un buen día 👋")