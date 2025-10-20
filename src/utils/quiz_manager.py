"""
Gestor del sistema de quiz de inglés.
Maneja preguntas, respuestas, llaves y estadísticas.
"""

import pygame
import random
from typing import Dict, List, Optional, Tuple
from src.utils.preguntas import (
    TipoPregunta, TipoPuerta, obtener_pregunta_aleatoria, 
    validar_respuesta, obtener_configuracion_nivel
)

class EstadoQuiz:
    INACTIVO = "inactivo"
    MOSTRANDO_PREGUNTA = "mostrando_pregunta"
    RESPUESTA_CORRECTA = "respuesta_correcta"
    RESPUESTA_INCORRECTA = "respuesta_incorrecta"
    ANIMACION_EXITO = "animacion_exito"
    ANIMACION_ERROR = "animacion_error"

class QuizManager:
    def __init__(self):
        """Inicializa el gestor de quiz."""
        self.estado = EstadoQuiz.INACTIVO
        self.pregunta_actual = None
        self.puerta_actual = None
        self.respuesta_seleccionada = -1
        
        # Sistema de llaves
        self.llaves_acumuladas = 0
        self.llaves_gastadas = 0
        
        # Sistema para prevenir múltiples quizzes en la misma puerta
        self.puertas_procesadas = set()  # IDs de puertas ya procesadas correctamente
        
        # Sistema para jefe final (dragón)
        self.ultima_respuesta_correcta = False
        self.ultima_respuesta_procesada = True  # Flag para saber si ya se procesó
        
        # Estadísticas del jugador
        self.preguntas_correctas = 0
        self.preguntas_incorrectas = 0
        self.preguntas_totales = 0
        self.racha_actual = 0
        self.mejor_racha = 0
        
        # Estadísticas por nivel
        self.estadisticas_nivel = {}
        
        # Timers para animaciones
        self.tiempo_animacion = 0
        self.tiempo_mostrando_resultado = 0
        
        # Colores y efectos
        self.color_fondo_overlay = (0, 0, 0, 180)
        self.color_pregunta = (255, 255, 255)
        self.color_opcion_normal = (200, 200, 200)
        self.color_opcion_hover = (255, 255, 100)
        self.color_opcion_seleccionada = (100, 255, 100)
        self.color_opcion_correcta = (0, 255, 0)
        self.color_opcion_incorrecta = (255, 100, 100)
        
        # Fuentes (se inicializarán cuando sea necesario)
        self.font_pregunta = None
        self.font_opciones = None
        self.font_titulo = None
        self.font_estadisticas = None
        
    def inicializar_fuentes(self):
        """Inicializa las fuentes para el texto."""
        if self.font_pregunta is None:
            pygame.font.init()
            self.font_titulo = pygame.font.Font(None, 36)
            self.font_pregunta = pygame.font.Font(None, 24)
            self.font_opciones = pygame.font.Font(None, 20)
            self.font_estadisticas = pygame.font.Font(None, 18)
            
    def iniciar_quiz(self, puerta, nivel: int):
        """
        Inicia un quiz para una puerta específica.
        
        Args:
            puerta: La puerta que activó el quiz
            nivel: Nivel actual del juego
        """
        if self.estado != EstadoQuiz.INACTIVO:
            return False
            
        # Verificar si esta puerta ya fue procesada correctamente
        puerta_id = id(puerta)
        if puerta_id in self.puertas_procesadas:
            return False  # Ya se respondió correctamente esta puerta
            
        # Verificar si la puerta está abierta
        if puerta.abierta:
            return False  # La puerta ya está abierta
            
        self.puerta_actual = puerta
        self.pregunta_actual = obtener_pregunta_aleatoria(nivel, puerta.tipo)
        self.estado = EstadoQuiz.MOSTRANDO_PREGUNTA
        self.respuesta_seleccionada = -1
        self.tiempo_animacion = 0
        self.tiempo_mostrando_resultado = 0
        
        # Mostrar la respuesta correcta en consola para testing
        if self.pregunta_actual:
            pregunta, opciones, respuesta_correcta, explicacion = self.pregunta_actual
            print(f"\n🎯 PREGUNTA: {pregunta}")
            print(f"✅ RESPUESTA CORRECTA: {opciones[respuesta_correcta]}")
            print(f"📝 Opciones: {opciones}")
            print(f"💡 Presiona la tecla {respuesta_correcta + 1} para la respuesta correcta")
            print(f"📖 Explicación: {explicacion}\n")
        
        # Inicializar fuentes si es necesario
        self.inicializar_fuentes()
        
        return True
        
    def seleccionar_opcion(self, indice: int):
        """
        Selecciona una opción de respuesta.
        
        Args:
            indice: Índice de la opción seleccionada (0-3)
        """
        if self.estado != EstadoQuiz.MOSTRANDO_PREGUNTA:
            return
            
        if 0 <= indice <= 3:
            self.respuesta_seleccionada = indice
            self._procesar_respuesta()
            
    def _procesar_respuesta(self):
        """Procesa la respuesta seleccionada y actualiza estadísticas."""
        if self.pregunta_actual is None:
            return
            
        es_correcta = validar_respuesta(self.pregunta_actual, self.respuesta_seleccionada)
        self._respuesta_fue_correcta = es_correcta
        
        # Sistema para jefe final (dragón)
        self.ultima_respuesta_correcta = es_correcta
        self.ultima_respuesta_procesada = False  # Marcar como pendiente de procesar
        
        # Actualizar estadísticas
        self.preguntas_totales += 1
        
        if es_correcta:
            self.preguntas_correctas += 1
            self.racha_actual += 1
            self.mejor_racha = max(self.mejor_racha, self.racha_actual)
            self.estado = EstadoQuiz.RESPUESTA_CORRECTA
            
            # Abrir la puerta
            if self.puerta_actual:
                # Marcar esta puerta como procesada correctamente
                puerta_id = id(self.puerta_actual)
                self.puertas_procesadas.add(puerta_id)
                
                # Abrir la puerta
                self.puerta_actual.abrir()
                
                # Remover barreras asociadas a esta puerta
                if hasattr(self, 'nivel_actual') and self.nivel_actual:
                    for i, puerta in enumerate(self.nivel_actual.puertas):
                        if puerta == self.puerta_actual:
                            self.nivel_actual.remover_barrera_puerta(i)
                            break
                
                # Otorgar llave si es una puerta especial
                if self.puerta_actual.tipo == TipoPuerta.LLAVE_ESPECIAL:
                    self.llaves_acumuladas += 1
                    
        else:
            self.preguntas_incorrectas += 1
            self.racha_actual = 0
            self.estado = EstadoQuiz.RESPUESTA_INCORRECTA
            
        self.tiempo_mostrando_resultado = 0
        
    def update(self):
        """Actualiza el estado del quiz."""
        if self.estado == EstadoQuiz.INACTIVO:
            return
            
        self.tiempo_animacion += 1
        
        if self.estado in [EstadoQuiz.RESPUESTA_CORRECTA, EstadoQuiz.RESPUESTA_INCORRECTA]:
            self.tiempo_mostrando_resultado += 1
            
            # Mostrar resultado por 2 segundos
            if self.tiempo_mostrando_resultado >= 120:  # 2 segundos a 60 FPS
                if self.estado == EstadoQuiz.RESPUESTA_CORRECTA:
                    self.estado = EstadoQuiz.ANIMACION_EXITO
                else:
                    self.estado = EstadoQuiz.ANIMACION_ERROR
                self.tiempo_animacion = 0
                
        elif self.estado in [EstadoQuiz.ANIMACION_EXITO, EstadoQuiz.ANIMACION_ERROR]:
            # Animación dura 1 segundo
            if self.tiempo_animacion >= 60:
                self._finalizar_quiz()
                
    def _finalizar_quiz(self):
        """Finaliza el quiz y retorna al estado inactivo."""
        # La puerta ya se abrió en _procesar_respuesta(), solo limpiamos el estado
        self.estado = EstadoQuiz.INACTIVO
        self.pregunta_actual = None
        self.puerta_actual = None
        self.respuesta_seleccionada = -1
        self.tiempo_animacion = 0
        self.tiempo_mostrando_resultado = 0
        
    def esta_activo(self) -> bool:
        """Verifica si el quiz está activo."""
        return self.estado != EstadoQuiz.INACTIVO
        
    def get_precision(self) -> float:
        """Obtiene el porcentaje de precisión del jugador."""
        if self.preguntas_totales == 0:
            return 0.0
        return (self.preguntas_correctas / self.preguntas_totales) * 100
        
    def nuevo_nivel(self):
        """Limpia el estado al cambiar de nivel."""
        self.puertas_procesadas.clear()  # Limpiar puertas procesadas del nivel anterior
        
    def get_puntos_bonus(self) -> int:
        """Calcula puntos bonus basados en el rendimiento."""
        puntos = 0
        
        # Puntos por respuesta correcta
        puntos += self.preguntas_correctas * 100
        
        # Bonus por racha
        if self.racha_actual >= 3:
            puntos += self.racha_actual * 50
            
        # Bonus por precisión alta
        precision = self.get_precision()
        if precision >= 90:
            puntos += 500
        elif precision >= 75:
            puntos += 250
            
        return puntos
        
    def dibujar(self, superficie: pygame.Surface):
        """
        Dibuja la interfaz del quiz.
        
        Args:
            superficie: Superficie donde dibujar
        """
        if self.estado == EstadoQuiz.INACTIVO:
            return
            
        self.inicializar_fuentes()
        
        # Overlay semi-transparente
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        superficie.blit(overlay, (0, 0))
        
        if self.estado == EstadoQuiz.MOSTRANDO_PREGUNTA:
            self._dibujar_pregunta(superficie)
        elif self.estado in [EstadoQuiz.RESPUESTA_CORRECTA, EstadoQuiz.RESPUESTA_INCORRECTA]:
            self._dibujar_resultado(superficie)
        elif self.estado == EstadoQuiz.ANIMACION_EXITO:
            self._dibujar_animacion_exito(superficie)
        elif self.estado == EstadoQuiz.ANIMACION_ERROR:
            self._dibujar_animacion_error(superficie)
            
    def _dibujar_pregunta(self, superficie: pygame.Surface):
        """Dibuja la pregunta y las opciones."""
        if not self.pregunta_actual:
            return
            
        pregunta, opciones, _, _ = self.pregunta_actual
        
        # Fondo de la pregunta
        rect_pregunta = pygame.Rect(100, 150, 600, 300)
        pygame.draw.rect(superficie, (50, 50, 70), rect_pregunta)
        pygame.draw.rect(superficie, (255, 255, 255), rect_pregunta, 3)
        
        # Título
        titulo = self.font_titulo.render("English Question", True, (255, 255, 100))
        titulo_rect = titulo.get_rect(center=(400, 180))
        superficie.blit(titulo, titulo_rect)
        
        # Pregunta
        pregunta_text = self.font_pregunta.render(pregunta, True, self.color_pregunta)
        pregunta_rect = pregunta_text.get_rect(center=(400, 220))
        superficie.blit(pregunta_text, pregunta_rect)
        
        # Opciones
        opciones_labels = ["A)", "B)", "C)", "D)"]
        for i, (label, opcion) in enumerate(zip(opciones_labels, opciones)):
            y_pos = 260 + i * 40
            
            # Color de la opción
            if i == self.respuesta_seleccionada:
                color = self.color_opcion_seleccionada
            else:
                color = self.color_opcion_normal
                
            # Fondo de la opción
            rect_opcion = pygame.Rect(120, y_pos - 5, 560, 30)
            pygame.draw.rect(superficie, (80, 80, 100), rect_opcion)
            if i == self.respuesta_seleccionada:
                pygame.draw.rect(superficie, color, rect_opcion, 2)
                
            # Texto de la opción
            texto_opcion = f"{label} {opcion}"
            opcion_text = self.font_opciones.render(texto_opcion, True, color)
            superficie.blit(opcion_text, (130, y_pos))
            
        # Instrucciones
        instruccion = self.font_estadisticas.render("Press 1, 2, 3, or 4 to select your answer", True, (200, 200, 200))
        instruccion_rect = instruccion.get_rect(center=(400, 420))
        superficie.blit(instruccion, instruccion_rect)
        
        # Estadísticas del jugador
        self._dibujar_estadisticas_pequenas(superficie)
        
    def _dibujar_resultado(self, superficie: pygame.Surface):
        """Dibuja el resultado de la respuesta."""
        if not self.pregunta_actual:
            return
            
        pregunta, opciones, respuesta_correcta, explicacion = self.pregunta_actual
        es_correcta = self.estado == EstadoQuiz.RESPUESTA_CORRECTA
        
        # Fondo
        rect_resultado = pygame.Rect(100, 150, 600, 300)
        color_fondo = (50, 100, 50) if es_correcta else (100, 50, 50)
        pygame.draw.rect(superficie, color_fondo, rect_resultado)
        pygame.draw.rect(superficie, (255, 255, 255), rect_resultado, 3)
        
        # Título del resultado
        titulo = "¡CORRECT!" if es_correcta else "INCORRECT"
        color_titulo = (0, 255, 0) if es_correcta else (255, 100, 100)
        titulo_text = self.font_titulo.render(titulo, True, color_titulo)
        titulo_rect = titulo_text.get_rect(center=(400, 180))
        superficie.blit(titulo_text, titulo_rect)
        
        # Mostrar la respuesta correcta
        respuesta_correcta_text = f"Correct answer: {opciones[respuesta_correcta]}"
        respuesta_text = self.font_opciones.render(respuesta_correcta_text, True, (255, 255, 255))
        respuesta_rect = respuesta_text.get_rect(center=(400, 220))
        superficie.blit(respuesta_text, respuesta_rect)
        
        # Explicación
        if explicacion:
            explicacion_lines = self._dividir_texto(explicacion, 70)
            for i, linea in enumerate(explicacion_lines):
                exp_text = self.font_estadisticas.render(linea, True, (200, 200, 200))
                exp_rect = exp_text.get_rect(center=(400, 260 + i * 20))
                superficie.blit(exp_text, exp_rect)
                
        # Consecuencias
        if es_correcta:
            if self.puerta_actual and self.puerta_actual.tipo == TipoPuerta.LLAVE_ESPECIAL:
                bonus_text = "Door opened! You earned a KEY!"
            else:
                bonus_text = "Door opened! +100 points!"
        else:
            bonus_text = "You lost 1 life! Try again!"
            
        bonus_render = self.font_opciones.render(bonus_text, True, (255, 255, 100))
        bonus_rect = bonus_render.get_rect(center=(400, 350))
        superficie.blit(bonus_render, bonus_rect)
        
    def _dibujar_animacion_exito(self, superficie: pygame.Surface):
        """Dibuja la animación de éxito."""
        # Efecto de partículas doradas
        for _ in range(20):
            x = random.randint(100, 700)
            y = random.randint(100, 500)
            size = random.randint(2, 6)
            alpha = random.randint(100, 255)
            
            # Crear superficie para la partícula con transparencia
            particula = pygame.Surface((size*2, size*2))
            particula.set_alpha(alpha)
            pygame.draw.circle(particula, (255, 215, 0), (size, size), size)
            superficie.blit(particula, (x, y))
            
        # Texto de éxito pulsante
        intensidad = abs(30 - (self.tiempo_animacion % 60)) / 30.0
        color_g = int(255 * intensidad)
        color_exito = (255, color_g, 0)
        
        exito_text = self.font_titulo.render("EXCELLENT!", True, color_exito)
        exito_rect = exito_text.get_rect(center=(400, 300))
        superficie.blit(exito_text, exito_rect)
        
    def _dibujar_animacion_error(self, superficie: pygame.Surface):
        """Dibuja la animación de error."""
        # Efecto de vibración
        offset_x = random.randint(-5, 5) if self.tiempo_animacion < 30 else 0
        offset_y = random.randint(-3, 3) if self.tiempo_animacion < 30 else 0
        
        # Texto de error con efecto
        error_text = self.font_titulo.render("TRY HARDER!", True, (255, 100, 100))
        error_rect = error_text.get_rect(center=(400 + offset_x, 300 + offset_y))
        superficie.blit(error_text, error_rect)
        
        # Líneas rojas intermitentes
        if self.tiempo_animacion % 20 < 10:
            pygame.draw.line(superficie, (255, 0, 0), (150, 250), (650, 250), 3)
            pygame.draw.line(superficie, (255, 0, 0), (150, 350), (650, 350), 3)
            
    def _dibujar_estadisticas_pequenas(self, superficie: pygame.Surface):
        """Dibuja estadísticas pequeñas en la esquina."""
        # Fondo para las estadísticas
        rect_stats = pygame.Rect(600, 50, 180, 80)
        pygame.draw.rect(superficie, (30, 30, 50), rect_stats)
        pygame.draw.rect(superficie, (255, 255, 255), rect_stats, 1)
        
        # Estadísticas
        stats_lines = [
            f"Keys: {self.llaves_acumuladas}",
            f"Streak: {self.racha_actual}",
            f"Accuracy: {self.get_precision():.1f}%",
            f"Questions: {self.preguntas_totales}"
        ]
        
        for i, linea in enumerate(stats_lines):
            text = self.font_estadisticas.render(linea, True, (255, 255, 255))
            superficie.blit(text, (610, 60 + i * 15))
            
    def _dividir_texto(self, texto: str, max_chars: int) -> List[str]:
        """Divide un texto en líneas de longitud máxima."""
        palabras = texto.split()
        lineas = []
        linea_actual = ""
        
        for palabra in palabras:
            if len(linea_actual + " " + palabra) <= max_chars:
                if linea_actual:
                    linea_actual += " " + palabra
                else:
                    linea_actual = palabra
            else:
                if linea_actual:
                    lineas.append(linea_actual)
                linea_actual = palabra
                
        if linea_actual:
            lineas.append(linea_actual)
            
        return lineas
        
    def manejar_tecla(self, tecla: int) -> bool:
        """
        Maneja las teclas presionadas durante el quiz.
        
        Args:
            tecla: Código de la tecla presionada
            
        Returns:
            True si la tecla fue manejada, False si no
        """
        if self.estado != EstadoQuiz.MOSTRANDO_PREGUNTA:
            return False
            
        # Teclas 1, 2, 3, 4 para seleccionar opciones
        if pygame.K_1 <= tecla <= pygame.K_4:
            self.seleccionar_opcion(tecla - pygame.K_1)
            return True
            
        # Teclas del keypad numérico (K_KP1, no KP_1)
        elif pygame.K_KP1 <= tecla <= pygame.K_KP4:
            self.seleccionar_opcion(tecla - pygame.K_KP1)
            return True
            
        return False
        
    def hay_respuesta_pendiente(self) -> bool:
        """
        Verifica si hay una respuesta pendiente de procesar por el sistema del dragón.
        
        Returns:
            True si hay una respuesta pendiente
        """
        return not self.ultima_respuesta_procesada
    
    def obtener_y_marcar_respuesta(self) -> Tuple[bool, bool]:
        """
        Obtiene la última respuesta y la marca como procesada.
        
        Returns:
            Tuple (fue_correcta, hubo_respuesta)
        """
        if self.ultima_respuesta_procesada:
            return (False, False)
        
        self.ultima_respuesta_procesada = True
        return (self.ultima_respuesta_correcta, True)
        
    def obtener_estado_para_guardado(self) -> Dict:
        """Obtiene el estado del quiz para guardar en el archivo de save."""
        return {
            "llaves_acumuladas": self.llaves_acumuladas,
            "llaves_gastadas": self.llaves_gastadas,
            "preguntas_correctas": self.preguntas_correctas,
            "preguntas_incorrectas": self.preguntas_incorrectas,
            "preguntas_totales": self.preguntas_totales,
            "mejor_racha": self.mejor_racha,
            "estadisticas_nivel": self.estadisticas_nivel
        }
        
    def cargar_estado(self, datos: Dict):
        """Carga el estado del quiz desde un archivo de save."""
        self.llaves_acumuladas = datos.get("llaves_acumuladas", 0)
        self.llaves_gastadas = datos.get("llaves_gastadas", 0)
        self.preguntas_correctas = datos.get("preguntas_correctas", 0)
        self.preguntas_incorrectas = datos.get("preguntas_incorrectas", 0)
        self.preguntas_totales = datos.get("preguntas_totales", 0)
        self.mejor_racha = datos.get("mejor_racha", 0)
        self.estadisticas_nivel = datos.get("estadisticas_nivel", {})