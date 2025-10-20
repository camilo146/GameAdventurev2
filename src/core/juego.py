"""
Clase principal del juego Super Mario Bros 2005.
"""

import pygame
import sys
from typing import Optional
from src.entities.mario import Mario
from src.entities.powerup import PowerUp
from src.entities.puerta import Puerta
from src.core.nivel import Nivel
from src.core.camara import Camara
from src.utils.constantes import *
from src.utils.constantes import ROSA, COLORES_QUIZ, CONFIGURACION_LLAVES
from src.utils.sonidos import gestor_sonidos
from src.utils.particulas import SistemaParticulas
from src.utils.quiz_manager import QuizManager

class Juego:
    """ 
    Clase principal que maneja toda la lógica del juego.
    
    Attributes:
        pantalla (pygame.Surface): Superficie principal de dibujo
        reloj (pygame.time.Clock): Reloj para controlar FPS
        mario (Mario): Personaje principal
        nivel_actual (Nivel): Nivel que se está jugando
        camara (Camara): Sistema de cámara
        estado (EstadoJuego): Estado actual del juego
        puntuacion (int): Puntuación del jugador
        vidas (int): Vidas restantes
        monedas (int): Monedas recolectadas
        tiempo (int): Tiempo restante
        particulas_globales (SistemaParticulas): Efectos globales
    """
    
    def __init__(self, pantalla: pygame.Surface, reloj: pygame.time.Clock):
        self.pantalla = pantalla
        self.reloj = reloj
        self.mario = Mario(50, 400)
        self.nivel_actual = Nivel(1)  # Comenzar desde el nivel 1
        self.camara = Camara(self.nivel_actual.ancho_mapa)
        self.estado = EstadoJuego.MENU
        
        # Estadísticas del juego
        self.puntuacion = 0
        self.vidas = 3
        self.monedas = 0
        self.tiempo = 400  # Tiempo en segundos
        self.tiempo_contador = 0
        
        # Efectos globales
        self.particulas_globales = SistemaParticulas()
        
        # Lista de bolas de fuego activas
        self.bolas_fuego = []
        
        # Sistema de quiz de inglés
        self.quiz_manager = QuizManager()
        self.quiz_manager.llaves_acumuladas = 0  # Comenzar sin llaves
        
        # Sistema de muerte con delay
        self.muerte_timer = 0
        self.muerte_delay = 20  # 0.33 segundos a 60 FPS - Reinicio ULTRA RÁPIDO ⚡⚡⚡
        self.esperando_reinicio = False
        
        # Fuente para texto
        self.fuente = pygame.font.Font(None, 36)
        self.fuente_pequena = pygame.font.Font(None, 24)
        
        # Control de pulsación de teclas (prevenir activaciones múltiples)
        self.tecla_e_presionada_anterior = False
        
        # Variables para el menú animado
        self.menu_tiempo = 0
        self.menu_opcion_seleccionada = 0  # 0 = Iniciar, 1 = Instrucciones, 2 = Salir
        self.menu_mostrar_instrucciones = False
        self.menu_particulas = []
        self.menu_scroll_instrucciones = 0  # Posición del scroll
        
        # Variables para los créditos finales
        self.creditos_scroll = 0
        self.creditos_tiempo = 0
        
        # Música de fondo (comentado temporalmente hasta tener archivos de audio)
        # gestor_sonidos.reproducir_musica('nivel.mp3', -1)
    
    def ejecutar(self) -> None:
        """Bucle principal del juego."""
        ejecutando = True
        
        while ejecutando:
            dt = self.reloj.tick(FPS)
            
            # Manejar eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                elif evento.type == pygame.KEYDOWN:
                    self._manejar_tecla(evento.key)
            
            # Actualizar según el estado
            if self.estado == EstadoJuego.MENU:
                self._actualizar_menu()
            elif self.estado == EstadoJuego.JUGANDO:
                self._actualizar_juego()
                # Siempre actualizar el quiz si está activo
                self.quiz_manager.update()
            elif self.estado == EstadoJuego.PAUSA:
                self._actualizar_pausa()
            elif self.estado == EstadoJuego.GAME_OVER:
                self._actualizar_game_over()
            elif self.estado == EstadoJuego.NIVEL_COMPLETADO:
                self._actualizar_nivel_completado()
            elif self.estado == EstadoJuego.JUEGO_COMPLETADO:
                self._actualizar_juego_completado()
            
            # Dibujar según el estado
            self.pantalla.fill(AZUL_CIELO)
            
            if self.estado == EstadoJuego.MENU:
                self._dibujar_menu()
            elif self.estado == EstadoJuego.JUGANDO:
                self._dibujar_juego()
            elif self.estado == EstadoJuego.PAUSA:
                self._dibujar_juego()
                self._dibujar_pausa()
            elif self.estado == EstadoJuego.GAME_OVER:
                self._dibujar_game_over()
            elif self.estado == EstadoJuego.NIVEL_COMPLETADO:
                self._dibujar_nivel_completado()
            elif self.estado == EstadoJuego.JUEGO_COMPLETADO:
                self._dibujar_juego_completado()
            
            pygame.display.flip()
    
    def _manejar_tecla(self, tecla: int) -> None:
        """
        Maneja las teclas presionadas.
        
        Args:
            tecla: Código de la tecla presionada
        """
        # Si el quiz está activo, que él maneje las teclas primero
        if self.quiz_manager.esta_activo():
            if self.quiz_manager.manejar_tecla(tecla):
                return  # La tecla fue manejada por el quiz
        
        if self.estado == EstadoJuego.MENU:
            if self.menu_mostrar_instrucciones:
                # Controles de scroll en instrucciones
                if tecla == pygame.K_UP or tecla == pygame.K_w:
                    self.menu_scroll_instrucciones = max(0, self.menu_scroll_instrucciones - 40)
                elif tecla == pygame.K_DOWN or tecla == pygame.K_s:
                    self.menu_scroll_instrucciones = min(ALTO * 5, self.menu_scroll_instrucciones + 40)  # Límite máximo igual a la superficie scrollable
                # Salir de instrucciones
                elif tecla == pygame.K_ESCAPE:
                    self.menu_mostrar_instrucciones = False
                    self.menu_scroll_instrucciones = 0  # Reset scroll
            else:
                # Navegación del menú
                if tecla == pygame.K_UP or tecla == pygame.K_w:
                    self.menu_opcion_seleccionada = (self.menu_opcion_seleccionada - 1) % 3
                elif tecla == pygame.K_DOWN or tecla == pygame.K_s:
                    self.menu_opcion_seleccionada = (self.menu_opcion_seleccionada + 1) % 3
                elif tecla == pygame.K_SPACE or tecla == pygame.K_RETURN:
                    # Ejecutar opción seleccionada
                    if self.menu_opcion_seleccionada == 0:
                        # Iniciar juego
                        self._iniciar_juego()
                    elif self.menu_opcion_seleccionada == 1:
                        # Mostrar instrucciones
                        self.menu_mostrar_instrucciones = True
                    elif self.menu_opcion_seleccionada == 2:
                        # Salir del juego
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
        elif self.estado == EstadoJuego.JUGANDO:
            if tecla == pygame.K_SPACE:
                self.mario.saltar()
            elif tecla == pygame.K_i:
                # Lanzar bola de fuego
                bola = self.mario.lanzar_fuego()
                if bola:
                    self.bolas_fuego.append(bola)
            elif tecla == pygame.K_p:
                self.estado = EstadoJuego.PAUSA
                gestor_sonidos.pausar_musica()
            elif tecla == pygame.K_r:
                self._reiniciar_nivel()
        elif self.estado == EstadoJuego.PAUSA:
            if tecla == pygame.K_p:
                self.estado = EstadoJuego.JUGANDO
                gestor_sonidos.reanudar_musica()
        elif self.estado == EstadoJuego.GAME_OVER:
            if tecla == pygame.K_SPACE or tecla == pygame.K_RETURN:
                self._reiniciar_juego()
        elif self.estado == EstadoJuego.NIVEL_COMPLETADO:
            if tecla == pygame.K_SPACE or tecla == pygame.K_RETURN:
                self._siguiente_nivel()
        elif self.estado == EstadoJuego.JUEGO_COMPLETADO:
            if tecla == pygame.K_SPACE or tecla == pygame.K_RETURN:
                self._reiniciar_juego()
    
    def _iniciar_juego(self) -> None:
        """Inicia una nueva partida."""
        self.estado = EstadoJuego.JUGANDO
        self.mario = Mario(50, 400)
        self.nivel_actual = Nivel(1)  # Comenzar desde el nivel 1
        self.muerte_timer = 0
        self.esperando_reinicio = False
        self.camara = Camara(self.nivel_actual.ancho_mapa)
        self.puntuacion = 0
        self.vidas = 3
        self.monedas = 0
        self.tiempo = 400
        self.quiz_manager.llaves_acumuladas = 0  # Comenzar sin llaves
        # gestor_sonidos.reproducir_musica('nivel.mp3', -1)
    
    def _actualizar_menu(self) -> None:
        """Actualiza el estado del menú."""
        import random
        self.particulas_globales.update()
        self.menu_tiempo += 0.1
        
        # Crear partículas flotantes de estrellas/monedas en el fondo
        if random.randint(0, 10) == 0:
            self.menu_particulas.append({
                'x': random.randint(0, ANCHO),
                'y': ALTO,
                'velocidad': random.uniform(0.5, 2),
                'size': random.randint(3, 8),
                'color': random.choice([AMARILLO, BLANCO, (255, 215, 0)])
            })
        
        # Actualizar partículas
        for particula in self.menu_particulas[:]:
            particula['y'] -= particula['velocidad']
            if particula['y'] < -10:
                self.menu_particulas.remove(particula)
    
    def _actualizar_juego(self) -> None:
        """Actualiza la lógica principal del juego."""
        # Si estamos esperando reinicio después de la muerte
        if self.esperando_reinicio:
            self.muerte_timer += 1
            self.particulas_globales.update()
            
            if self.muerte_timer >= self.muerte_delay:
                self.muerte_timer = 0
                self.esperando_reinicio = False
                
                if self.vidas <= 0:
                    self.estado = EstadoJuego.GAME_OVER
                    gestor_sonidos.detener_musica()
                else:
                    self._reiniciar_nivel()
            return
        
        # Actualizar tiempo
        self.tiempo_contador += 1
        if self.tiempo_contador >= FPS:  # 1 segundo
            self.tiempo -= 1
            self.tiempo_contador = 0
            
            if self.tiempo <= 0:
                self._mario_muere()
        
        # Actualizar Mario
        self.mario.update(self.nivel_actual.plataformas)
        
        # Actualizar nivel
        self.nivel_actual.update()
        
        # Actualizar efectos visuales de plataformas
        delta_time = 1.0 / FPS
        for plataforma in self.nivel_actual.plataformas:
            if hasattr(plataforma, 'actualizar'):
                plataforma.actualizar(delta_time)
        
        # Verificar bloques golpeados para liberar power-ups
        self._verificar_bloques_golpeados()
        
        # Actualizar cámara
        self.camara.actualizar(self.mario)
        
        # Actualizar partículas globales
        self.particulas_globales.update()
        
        # Actualizar bolas de fuego
        for bola in self.bolas_fuego[:]:
            bola.update(self.nivel_actual.plataformas)
            if not bola.viva:
                self.bolas_fuego.remove(bola)
        
        # Verificar colisiones de bolas de fuego con enemigos
        self._verificar_colisiones_bolas_fuego()
        
        # Verificar colisiones
        self._verificar_colisiones()
        
        # Verificar colisiones con puertas (sistema de quiz)
        self._verificar_colisiones_puertas()
        
        # Sistema de jefe final - Dragón (nivel 5)
        self._actualizar_sistema_dragon()
        
        # Verificar condiciones de fin
        self._verificar_condiciones()
    
    def _actualizar_pausa(self) -> None:
        """Actualiza el estado de pausa."""
        pass  # No hay actualizaciones durante la pausa
    
    def _actualizar_game_over(self) -> None:
        """Actualiza el estado de game over."""
        self.particulas_globales.update()
    
    def _actualizar_nivel_completado(self) -> None:
        """Actualiza el estado de nivel completado."""
        self.particulas_globales.update()
    
    def _actualizar_juego_completado(self) -> None:
        """Actualiza el estado de juego completado (princesa rescatada)."""
        self.particulas_globales.update()
    
    def _verificar_colisiones(self) -> None:
        """Verifica las colisiones entre entidades."""
        mario_rect = self.mario.rect
        
        # NO verificar colisiones si Mario está muriendo o muerto
        if not self.mario.vivo or self.mario.estado == EstadoMario.MURIENDO:
            return
        
        # Colisiones con enemigos
        for enemigo in self.nivel_actual.enemigos[:]:
            if mario_rect.colliderect(enemigo.rect) and enemigo.vivo and not enemigo.aplastado:
                if self.mario.es_invencible():
                    # Mario invencible elimina enemigo
                    puntos = enemigo.eliminar()
                    self.puntuacion += puntos
                    self.particulas_globales.crear_efecto(
                        enemigo.rect.centerx, enemigo.rect.centery, 'enemigo'
                    )
                # Verificar si Mario está cayendo sobre el enemigo (aplastamiento)
                # Mejorado: verificar que Mario viene desde arriba
                elif (self.mario.velocidad_y > 0 and 
                      self.mario.rect.bottom - self.mario.velocidad_y <= enemigo.rect.top + 10):
                    # Mario aplasta al enemigo (desde arriba)
                    puntos = enemigo.aplastar()
                    self.puntuacion += puntos
                    self.mario.velocidad_y = -10  # Rebote más fuerte
                    self.mario.rect.bottom = enemigo.rect.top  # Posicionar correctamente
                    self.particulas_globales.crear_efecto(
                        enemigo.rect.centerx, enemigo.rect.centery, 'enemigo'
                    )
                else:
                    # Mario recibe daño (colisión lateral)
                    murio = self.mario.recibir_dano()
                    
                    # Empujar a Mario hacia atrás para evitar contacto continuo
                    if not murio:
                        # Determinar dirección del empuje
                        if self.mario.rect.centerx < enemigo.rect.centerx:
                            # Mario está a la izquierda del enemigo, empujar a la izquierda
                            self.mario.rect.x -= 20
                            self.mario.velocidad_x = -3
                        else:
                            # Mario está a la derecha del enemigo, empujar a la derecha
                            self.mario.rect.x += 20
                            self.mario.velocidad_x = 3
                        
                        # Pequeño salto hacia arriba
                        self.mario.velocidad_y = -5
                        self.mario.saltando = True
                    else:
                        # Mario murió
                        self._mario_muere()
        
        # Colisiones con monedas
        for moneda in self.nivel_actual.monedas[:]:
            if mario_rect.colliderect(moneda.rect):
                puntos = moneda.recoger()
                self.puntuacion += puntos
                self.monedas += 1
                self.nivel_actual.monedas.remove(moneda)
                self.particulas_globales.crear_efecto(
                    moneda.rect.centerx, moneda.rect.centery, 'moneda'
                )
                
                # Vida extra cada 100 monedas
                if self.monedas % 100 == 0:
                    self.vidas += 1
        
        # Colisiones con power-ups
        for powerup in self.nivel_actual.powerups[:]:
            if mario_rect.colliderect(powerup.rect) and powerup.activo:
                self.mario.obtener_powerup(powerup.tipo)
                self.puntuacion += 1000
                self.nivel_actual.powerups.remove(powerup)
                self.particulas_globales.crear_efecto(
                    powerup.rect.centerx, powerup.rect.centery, 'powerup'
                )
        
        # Colisión con bandera (meta)
        if (self.nivel_actual.bandera and 
            mario_rect.colliderect(self.nivel_actual.bandera.rect)):
            self._nivel_completado()
        
        # Colisión con princesa (nivel 5 - final del juego)
        if (self.nivel_actual.princesa and 
            not self.nivel_actual.princesa.rescatada and
            mario_rect.colliderect(self.nivel_actual.princesa.get_rect())):
            self._rescatar_princesa()
    
    def _verificar_colisiones_bolas_fuego(self) -> None:
        """Verifica colisiones de las bolas de fuego con enemigos."""
        for bola in self.bolas_fuego[:]:
            if not bola.viva:
                continue
                
            for enemigo in self.nivel_actual.enemigos[:]:
                if enemigo.vivo and not enemigo.aplastado and bola.rect.colliderect(enemigo.rect):
                    # Eliminar enemigo
                    puntos = enemigo.eliminar()
                    self.puntuacion += puntos
                    
                    # Efectos visuales
                    self.particulas_globales.crear_efecto(
                        enemigo.rect.centerx, enemigo.rect.centery, 'fuego'
                    )
                    
                    # Eliminar bola de fuego
                    bola.eliminar()
                    if bola in self.bolas_fuego:
                        self.bolas_fuego.remove(bola)
                    break
    
    def _verificar_bloques_golpeados(self) -> None:
        """Verifica si algún bloque fue golpeado para liberar power-ups."""
        for plataforma in self.nivel_actual.plataformas:
            if (hasattr(plataforma, 'tiene_powerup') and 
                plataforma.tiene_powerup and 
                plataforma.golpeado and 
                not plataforma.powerup_liberado):
                
                # Liberar power-up desde el bloque
                powerup = PowerUp(plataforma.rect.centerx - 12, 
                                plataforma.rect.top - 24, 
                                plataforma.tipo_powerup, 
                                desde_bloque=True)
                self.nivel_actual.powerups.append(powerup)
                plataforma.powerup_liberado = True
                
                self.particulas_globales.crear_efecto(
                    plataforma.rect.centerx, plataforma.rect.top, 'powerup'
                )
    
    def _verificar_condiciones(self) -> None:
        """Verifica las condiciones de fin de nivel o muerte."""
        # Verificar caída al vacío
        if self.mario.rect.y > ALTO:
            if self.mario.estado == EstadoMario.MURIENDO:
                # Si Mario ya está muriendo y cayó al vacío, forzar reinicio inmediato
                if not self.esperando_reinicio:
                    self.esperando_reinicio = True
                    self.muerte_timer = self.muerte_delay  # Saltar directo al final del delay
            else:
                # Mario estaba vivo y cayó al vacío
                self._mario_muere()
        
        # Verificar límites del mapa (permitir movimiento completo)
        if self.mario.rect.x < 0:
            self.mario.rect.x = 0
        # Eliminar límite derecho - Mario puede avanzar por todo el nivel
    
    def _mario_muere(self) -> None:
        """Maneja la muerte de Mario."""
        # Prevenir múltiples llamadas a muerte
        # IMPORTANTE: verificar esperando_reinicio primero antes de descontar vida
        if self.esperando_reinicio:
            return
        
        # Descontar vida SIEMPRE (incluso si Mario ya está en estado MURIENDO)
        self.vidas -= 1
        
        # Solo cambiar estado y efectos si Mario no estaba muriendo antes
        if self.mario.estado != EstadoMario.MURIENDO:
            self.mario._cambiar_estado(EstadoMario.MURIENDO)
            self.particulas_globales.crear_explosion(
                self.mario.rect.centerx, self.mario.rect.centery, ROJO, 20
            )
            gestor_sonidos.reproducir_efecto('muerte')
        
        # Activar el sistema de espera sin bloquear
        self.esperando_reinicio = True
        self.muerte_timer = 0
    
    def _nivel_completado(self) -> None:
        """Maneja la finalización del nivel."""
        self.estado = EstadoJuego.NIVEL_COMPLETADO
        self.puntuacion += self.tiempo * 50  # Bonus por tiempo restante
        gestor_sonidos.reproducir_efecto('nivel_completado')
        
        # Efectos de celebración
        for i in range(20):
            self.particulas_globales.crear_explosion(
                self.nivel_actual.bandera.rect.centerx + (i * 10 - 100),
                self.nivel_actual.bandera.rect.centery,
                [AMARILLO, VERDE, ROJO, AZUL][i % 4], 5
            )
    
    def _rescatar_princesa(self) -> None:
        """Maneja el rescate de la princesa (final del juego)."""
        self.nivel_actual.princesa.rescatar()
        self.estado = EstadoJuego.JUEGO_COMPLETADO
        self.puntuacion += self.tiempo * 100  # Bonus GIGANTE por tiempo restante
        self.puntuacion += 10000  # Bonus especial por rescatar a la princesa
        gestor_sonidos.reproducir_efecto('nivel_completado')
        
        # ¡CELEBRACIÓN ÉPICA!
        for i in range(50):
            self.particulas_globales.crear_explosion(
                self.nivel_actual.princesa.x + (i * 8 - 200),
                self.nivel_actual.princesa.y,
                [AMARILLO, VERDE, ROJO, AZUL, ROSA][i % 5], 8
            )
    
    def _siguiente_nivel(self) -> None:
        """Pasa al siguiente nivel (máximo 5 niveles)."""
        # Si ya completó el nivel 5, no hay más niveles
        if self.nivel_actual.numero >= 5:
            return
        
        self.nivel_actual = Nivel(self.nivel_actual.numero + 1)
        self.camara = Camara(self.nivel_actual.ancho_mapa)
        self.mario = Mario(50, 400)
        self.estado = EstadoJuego.JUGANDO
        self.tiempo = 400
        # Limpiar puertas procesadas del quiz manager
        self.quiz_manager.nuevo_nivel()
        # gestor_sonidos.reproducir_musica('nivel.mp3', -1)
    
    def _reiniciar_nivel(self) -> None:
        """Reinicia el nivel actual."""
        self.mario = Mario(50, 400)
        self.nivel_actual.reiniciar()
        self.camara = Camara(self.nivel_actual.ancho_mapa)
        self.tiempo = 400
        self.tiempo_contador = 0
        self.muerte_timer = 0
        self.esperando_reinicio = False
        # Limpiar bolas de fuego
        self.bolas_fuego = []
        # Limpiar puertas procesadas del quiz manager
        self.quiz_manager.nuevo_nivel()
        self.particulas_globales.limpiar()
    
    def _reiniciar_juego(self) -> None:
        """Reinicia completamente el juego."""
        self.estado = EstadoJuego.MENU
        self.particulas_globales.limpiar()
        self.bolas_fuego = []  # Limpiar bolas de fuego
        self.vidas = 3
        self.puntuacion = 0
        self.monedas = 0
        self.muerte_timer = 0
        self.esperando_reinicio = False
    
    def _dibujar_menu(self) -> None:
        """Dibuja el menú principal con el estilo visual EXACTO del juego."""
        import math
        
        # Fondo azul cielo EXACTO como en el juego
        self.pantalla.fill(AZUL_CIELO)  # (92, 148, 252)
        
        # ===== COLORES EXACTOS DEL JUEGO =====
        COLOR_LADRILLO = (186, 85, 34)
        COLOR_HIERBA = (0, 168, 0)
        COLOR_BLOQUE = (218, 165, 32)
        
        # ===== MONTAÑAS VERDES CON DETALLES (estilo exacto del juego) =====
        # Montaña grande izquierda con textura (llega hasta el fondo)
        pygame.draw.polygon(self.pantalla, COLOR_HIERBA, [
            (0, ALTO), (120, ALTO - 300), (240, ALTO)
        ])
        # Detalles oscuros en la montaña (para dar profundidad)
        pygame.draw.polygon(self.pantalla, (0, 140, 0), [
            (0, ALTO), (30, ALTO - 150), (60, ALTO)
        ])
        pygame.draw.polygon(self.pantalla, (0, 140, 0), [
            (80, ALTO), (120, ALTO - 300), (160, ALTO)
        ])
        
        # Montaña grande derecha con textura (llega hasta el fondo)
        pygame.draw.polygon(self.pantalla, COLOR_HIERBA, [
            (560, ALTO), (680, ALTO - 320), (800, ALTO)
        ])
        # Detalles oscuros
        pygame.draw.polygon(self.pantalla, (0, 140, 0), [
            (600, ALTO), (680, ALTO - 320), (760, ALTO)
        ])
        
        # Montañas pequeñas adicionales (llegan hasta el fondo)
        pygame.draw.polygon(self.pantalla, (0, 140, 0), [
            (300, ALTO), (380, ALTO - 200), (460, ALTO)
        ])
        
        # ===== NUBES BLANCAS ESTILO PIXEL ART DEL JUEGO =====
        nubes_data = [(80, 80, 35), (320, 120, 28), (600, 90, 32)]
        for x_nube, y_nube, tamaño in nubes_data:
            # Nube con forma redondeada estilo NES
            pygame.draw.circle(self.pantalla, BLANCO, (x_nube, y_nube), tamaño)
            pygame.draw.circle(self.pantalla, BLANCO, (x_nube + tamaño, y_nube - 8), tamaño + 5)
            pygame.draw.circle(self.pantalla, BLANCO, (x_nube + tamaño * 2, y_nube), tamaño)
            pygame.draw.rect(self.pantalla, BLANCO, (x_nube - tamaño, y_nube, tamaño * 3, tamaño))
        
        # ===== LOGO PRINCIPAL =====
        # Rectángulo naranja de fondo con sombra
        rect_logo_fondo = pygame.Rect(ANCHO // 2 - 280, 80, 560, 140)
        # Sombra del rectángulo
        pygame.draw.rect(self.pantalla, (50, 50, 50), (rect_logo_fondo.x + 6, rect_logo_fondo.y + 6, rect_logo_fondo.width, rect_logo_fondo.height))
        pygame.draw.rect(self.pantalla, (248, 148, 88), rect_logo_fondo)  # Naranja
        pygame.draw.rect(self.pantalla, NEGRO, rect_logo_fondo, 5)  # Borde negro
        
        # Texto "SUPER" 
        fuente_super = pygame.font.Font(None, 56)
        texto_super = fuente_super.render("SUPER", True, (252, 216, 168))
        sombra_super = fuente_super.render("SUPER", True, NEGRO)
        rect_super = texto_super.get_rect(center=(ANCHO // 2, 115))
        self.pantalla.blit(sombra_super, (rect_super.x + 3, rect_super.y + 3))
        self.pantalla.blit(texto_super, rect_super)
        
        # Texto "MARIO BROS"
        fuente_mario = pygame.font.Font(None, 82)
        texto_mariobros = fuente_mario.render("MARIO BROS", True, (252, 216, 168))
        sombra_mariobros = fuente_mario.render("MARIO BROS", True, NEGRO)
        rect_mariobros = texto_mariobros.get_rect(center=(ANCHO // 2, 175))
        self.pantalla.blit(sombra_mariobros, (rect_mariobros.x + 4, rect_mariobros.y + 4))
        self.pantalla.blit(texto_mariobros, rect_mariobros)
        
        # Subtítulo con año
        fuente_sub = pygame.font.Font(None, 28)
        texto_sub = fuente_sub.render("Adventure Mario Version 2005", True, AMARILLO)
        rect_sub = texto_sub.get_rect(center=(ANCHO // 2, 235))
        self.pantalla.blit(texto_sub, rect_sub)
        
        # ===== BLOQUES DECORATIVOS (estilo EXACTO del juego) =====
        # Bloques de interrogación dorados con animación sutil
        for i, x_pos in enumerate([100, 220, 580, 700]):
            y_bloque = 260 + (i % 2) * 20 + int(3 * math.sin(self.menu_tiempo * 2 + i))
            # Bloque dorado base
            pygame.draw.rect(self.pantalla, COLOR_BLOQUE, (x_pos, y_bloque, 32, 32))
            # Borde oscuro para efecto 3D
            pygame.draw.rect(self.pantalla, (180, 140, 20), (x_pos, y_bloque, 32, 32), 2)
            # Detalles internos (como en el juego)
            pygame.draw.rect(self.pantalla, (240, 190, 50), (x_pos + 4, y_bloque + 4, 24, 24), 2)
            # Signo de interrogación blanco
            fuente_bloque = pygame.font.Font(None, 36)
            texto_interrogacion = fuente_bloque.render("?", True, BLANCO)
            rect_int = texto_interrogacion.get_rect(center=(x_pos + 16, y_bloque + 16))
            self.pantalla.blit(texto_interrogacion, rect_int)
        
        # ===== OPCIONES DEL MENÚ CON ESTILO DEL JUEGO =====
        if not self.menu_mostrar_instrucciones:
            fuente_opciones = pygame.font.Font(None, 44)
            
            # Estrella parpadeante como indicador
            if int(self.menu_tiempo * 2) % 2 == 0:
                indicador = "★"
            else:
                indicador = "✦"
            
            # Panel semi-transparente para las opciones
            panel_rect = pygame.Rect(ANCHO // 2 - 200, 315, 420, 150)
            panel_surface = pygame.Surface((420, 150))
            panel_surface.set_alpha(180)
            panel_surface.fill((40, 40, 80))
            self.pantalla.blit(panel_surface, (ANCHO // 2 - 200, 315))
            pygame.draw.rect(self.pantalla, AMARILLO, panel_rect, 4)
            
            # Opción 1: "INICIAR JUEGO"
            y_op1 = 335
            if self.menu_opcion_seleccionada == 0:
                texto_ind = fuente_opciones.render(indicador, True, AMARILLO)
                self.pantalla.blit(texto_ind, (ANCHO // 2 - 140, y_op1))
            texto_op1 = fuente_opciones.render("INICIAR JUEGO", True, BLANCO if self.menu_opcion_seleccionada != 0 else AMARILLO)
            self.pantalla.blit(texto_op1, (ANCHO // 2 - 100, y_op1))
            
            # Opción 2: "INSTRUCCIONES"
            y_op2 = 385
            if self.menu_opcion_seleccionada == 1:
                texto_ind = fuente_opciones.render(indicador, True, AMARILLO)
                self.pantalla.blit(texto_ind, (ANCHO // 2 - 140, y_op2))
            texto_op2 = fuente_opciones.render("INSTRUCCIONES", True, BLANCO if self.menu_opcion_seleccionada != 1 else AMARILLO)
            self.pantalla.blit(texto_op2, (ANCHO // 2 - 100, y_op2))
            
            # Opción 3: "SALIR"
            y_op3 = 435
            if self.menu_opcion_seleccionada == 2:
                texto_ind = fuente_opciones.render(indicador, True, AMARILLO)
                self.pantalla.blit(texto_ind, (ANCHO // 2 - 140, y_op3))
            texto_op3 = fuente_opciones.render("SALIR", True, BLANCO if self.menu_opcion_seleccionada != 2 else AMARILLO)
            self.pantalla.blit(texto_op3, (ANCHO // 2 - 100, y_op3))
            
            # Controles en la parte inferior
            fuente_ayuda = pygame.font.Font(None, 26)
            texto_ayuda = fuente_ayuda.render("↑↓ Navegar   ENTER Seleccionar", True, BLANCO)
            rect_ayuda = texto_ayuda.get_rect(center=(ANCHO // 2, ALTO - 60))
            self.pantalla.blit(texto_ayuda, rect_ayuda)
            
            # Suelo con ladrillos (estilo del juego)
            for i in range(0, ANCHO, 32):
                # Ladrillos
                pygame.draw.rect(self.pantalla, COLOR_LADRILLO, (i, ALTO - 32, 32, 32))
                pygame.draw.rect(self.pantalla, (140, 60, 20), (i, ALTO - 32, 32, 32), 2)
                # Patrón de ladrillos
                pygame.draw.line(self.pantalla, (140, 60, 20), (i, ALTO - 16), (i + 32, ALTO - 16), 2)
            
        else:
            # Pantalla de instrucciones con SCROLL
            # Fondo semi-transparente
            overlay = pygame.Surface((ANCHO, ALTO))
            overlay.set_alpha(200)
            overlay.fill((30, 30, 60))
            self.pantalla.blit(overlay, (0, 0))
            
            # Título de instrucciones (fijo, más arriba)
            fuente_titulo_inst = pygame.font.Font(None, 48)  # Título más pequeño
            titulo_inst = fuente_titulo_inst.render("📖 CÓMO JUGAR", True, AMARILLO)
            rect_titulo = titulo_inst.get_rect(center=(ANCHO // 2, 30))  # Más arriba
            self.pantalla.blit(titulo_inst, rect_titulo)
            
            # Área de scroll (crear superficie para contenido scrollable)
            scroll_surface = pygame.Surface((ANCHO - 20, ALTO * 5))  # Mucho más alto para soportar cualquier cantidad de texto
            scroll_surface.fill((30, 30, 60))
            
            # Instrucciones DETALLADAS con iconos
            fuente_inst = pygame.font.Font(None, 24)  # Reducido de 26 a 24
            fuente_titulo_seccion = pygame.font.Font(None, 30)  # Reducido de 32 a 30
            instrucciones = [
                "",
                "🎮 CONTROLES BÁSICOS:",
                "  ← → Flechas o A D  -  Mover",
                "  ↑ Flecha o W o ESPACIO  -  Saltar",
                "  I  -  Lanzar bola de fuego",
                "  SHIFT  -  Correr más rápido",
                "  P  -  Pausar el juego",
                "  R  -  Reiniciar nivel actual",
                "",
                "🎯 OBJETIVO PRINCIPAL:",
                "  Atraviesa 5 niveles llenos de desafíos,",
                "  responde preguntas de inglés sobre",
                "  WILL y GOING TO para abrir puertas,",
                "  derrota al dragón Bowser y rescata",
                "  a la Princesa Peach en el nivel 5.",
                "",
                "🚪 SISTEMA DE PUERTAS Y LLAVES:",
                "",
                "  📌 PUERTAS OBLIGATORIAS (Rojas):",
                "     • Bloquean el camino principal",
                "     • DEBES responder correctamente",
                "     • Al acercarte, aparece la pregunta",
                "     • Responde con teclas 1, 2, 3 o 4",
                "",
                "  🔑 LLAVES:",
                "     • Ganas 1 llave por respuesta CORRECTA",
                "     • Las llaves se acumulan entre niveles",
                "     • Cada puerta requiere 1 llave",
                "     • Contador visible arriba izquierda",
                "",
                "  ❌ RESPUESTAS INCORRECTAS:",
                "     • En puertas normales: NO ganas llave",
                "     • Con el dragón: Pierdes 1 vida",
                "     • Si llegas a 0 vidas: Game Over",
                "",
                "  ✅ RESPUESTAS CORRECTAS:",
                "     • +1 Llave automáticamente",
                "     • Puerta se abre",
                "     • +Puntos bonus",
                "     • Puedes continuar el nivel",
                "",
                "⚡ POWER-UPS TEMPORALES:",
                "  (¡Recolecta constantemente!)",
                "",
                "  🍄 Champiñón Rojo  -  Crecer 8 seg",
                "     • Mario grande aguanta 1 golpe",
                "     • Después de 8 seg vuelves pequeño",
                "     • ¡Busca más hongos para ventaja!",
                "",
                "  🌸 Flor de Fuego  -  Fuego 10 seg",
                "     • NO creces, solo ganas fuego",
                "     • Presiona I para lanzar bolas",
                "     • Las bolas eliminan enemigos",
                "     • Después de 10 seg pierdes poder",
                "",
                "  ⭐ Estrella  -  Invencible 8 seg",
                "     • Eliminas enemigos al tocarlos",
                "     • No recibes daño",
                "",
                "  🪙 Monedas  -  100 = 1 vida extra",
                "",
                "🔥 SISTEMA DE BOLAS DE FUEGO:",
                "  • Solo con poder de flor activo",
                "  • Presiona I para lanzar",
                "  • Rebotan en plataformas",
                "  • Eliminan enemigos al contacto",
                "  • Se autodestruyen tras un tiempo",
                "",
                "🐉 JEFE FINAL - DRAGÓN BOWSER:",
                "  (Nivel 5)",
                "",
                "  • Aparece antes de la princesa",
                "  • Tiene 5 puntos de vida (HP)",
                "  • Respuesta CORRECTA = -1 HP dragón",
                "  • Respuesta INCORRECTA = -1 vida Mario",
                "  • Derrota al dragón para rescatar",
                "",
                "📚 PREGUNTAS DE INGLÉS:",
                "  • Tema: WILL y GOING TO (futuro)",
                "  • Nivel 1-2: Preguntas básicas",
                "  • Nivel 3-4: Preguntas intermedias",
                "  • Nivel 5: Preguntas avanzadas",
                "  • Opciones se mezclan aleatoriamente",
                "",
                "💡 CONSEJOS ÚTILES:",
                "  • Lee las preguntas con calma",
                "  • Llaves NO se pierden entre niveles",
                "  • Usa SHIFT para saltar más lejos",
                "  • Evita enemigos saltando sobre ellos",
                "  • Guarda vidas para el dragón final",
                "  • Power-ups son TEMPORALES",
                "  • Usa bolas de fuego (I) a distancia",
                "",
                "🎖️ SISTEMA DE PROGRESIÓN:",
                "  Nivel 1 → 2 → 3 → 4 → 5",
                "  Cada nivel es más difícil",
                "",
                "",
                "↑↓ USA FLECHAS PARA SCROLL",
                "Presiona ESC para volver"
            ]
            
            y = 20
            for linea in instrucciones:
                # Determinar color según el tipo de línea
                if linea.startswith("🎮") or linea.startswith("🎯") or linea.startswith("⚡") or linea.startswith("�") or linea.startswith("🐲") or linea.startswith("📚") or linea.startswith("💡") or linea.startswith("🎖️"):
                    color = AMARILLO
                    fuente = fuente_titulo_seccion
                elif linea.startswith("  📌") or linea.startswith("  🔑") or linea.startswith("  ❌") or linea.startswith("  ✅"):
                    color = (100, 255, 100)  # Verde claro para subsecciones
                    fuente = fuente_inst
                elif linea.startswith("↑↓") or linea.startswith("Presiona"):
                    color = (200, 200, 200)
                    fuente = fuente_inst
                else:
                    color = BLANCO
                    fuente = fuente_inst
                
                texto = fuente.render(linea, True, color)
                if linea:
                    if linea.startswith("🎮") or linea.startswith("🎯") or linea.startswith("⚡") or linea.startswith("�") or linea.startswith("🐲") or linea.startswith("📚") or linea.startswith("💡") or linea.startswith("🎖️") or linea.startswith("↑↓") or linea.startswith("Presiona"):
                        # Centrar títulos
                        texto_rect = texto.get_rect(center=(scroll_surface.get_width() // 2, y))
                        scroll_surface.blit(texto, texto_rect)
                    else:
                        # Alinear a la izquierda con margen reducido
                        scroll_surface.blit(texto, (20, y))
                y += 28
            
            # Dibujar la superficie scrollable con el offset (contenedor MAXIMIZADO)
            self.pantalla.blit(scroll_surface, (10, 65), 
                             area=pygame.Rect(0, self.menu_scroll_instrucciones, 
                                            ANCHO - 20, ALTO - 75))
            
            # Barra de scroll visual
            if y > ALTO - 75:  # Si hay contenido scrolleable
                barra_alto = max(30, int((ALTO - 75) / y * (ALTO - 75)))
                barra_y = 65 + int(self.menu_scroll_instrucciones / y * (ALTO - 75))
                pygame.draw.rect(self.pantalla, (100, 100, 100), 
                               (ANCHO - 30, 65, 10, ALTO - 75), border_radius=5)
                pygame.draw.rect(self.pantalla, AMARILLO, 
                               (ANCHO - 30, barra_y, 10, barra_alto), border_radius=5)
        
        # Efectos de partículas
        self.particulas_globales.dibujar(self.pantalla)
    
    def _dibujar_juego(self) -> None:
        """Dibuja el juego principal."""
        # Dibujar fondo con parallax
        self._dibujar_fondo()
        
        # Dibujar nivel
        self.nivel_actual.dibujar(self.pantalla, self.camara)
        
        # Dibujar Mario
        pos_mario = self.camara.aplicar(self.mario)
        mario_temp = Mario(pos_mario[0], pos_mario[1])
        mario_temp.estado = self.mario.estado
        mario_temp.direccion = self.mario.direccion
        mario_temp.animacion_frame = self.mario.animacion_frame
        mario_temp.invencible = self.mario.invencible
        mario_temp.tiempo_transformacion = self.mario.tiempo_transformacion
        mario_temp.vivo = self.mario.vivo
        mario_temp.alto = self.mario.alto
        mario_temp.rect.height = self.mario.alto
        mario_temp.particulas = self.mario.particulas
        mario_temp.dibujar(self.pantalla)
        
        # Dibujar bolas de fuego
        for bola in self.bolas_fuego:
            bola.dibujar(self.pantalla, self.camara.x)
        
        # Dibujar partículas globales
        self.particulas_globales.dibujar(self.pantalla)
        
        # Dibujar HUD
        self._dibujar_hud()
        
        # Dibujar quiz (si está activo)
        self.quiz_manager.dibujar(self.pantalla)
    
    def _dibujar_fondo(self) -> None:
        """Dibuja el fondo estilo Mario Bros clásico con montañas mejoradas."""
        # Fondo azul cielo sólido como en Mario Bros
        self.pantalla.fill(AZUL_CIELO)
        
        # ===== MONTAÑAS VERDES CON TEXTURA Y PROFUNDIDAD (como el menú) =====
        COLOR_HIERBA = (0, 168, 0)
        COLOR_HIERBA_OSCURA = (0, 140, 0)
        offset_montanas = self.camara.x * 0.05  # Parallax lento para montañas
        
        # Obtener ancho del mapa de forma segura
        ancho_mapa = self.nivel.ancho_mapa if hasattr(self, 'nivel') and self.nivel else 3200
        
        # Montaña grande 1 (izquierda) - se repite con el parallax
        for base_x in range(-300, int(ancho_mapa + 300), 800):
            x_montaña = base_x - offset_montanas
            if -300 < x_montaña < ANCHO + 300:  # Solo dibujar si está visible
                # Montaña grande con textura (llega hasta el fondo)
                pygame.draw.polygon(self.pantalla, COLOR_HIERBA, [
                    (x_montaña, ALTO), 
                    (x_montaña + 180, ALTO - 320), 
                    (x_montaña + 360, ALTO)
                ])
                # Detalles oscuros en la montaña (sombras para dar profundidad)
                pygame.draw.polygon(self.pantalla, COLOR_HIERBA_OSCURA, [
                    (x_montaña, ALTO), 
                    (x_montaña + 40, ALTO - 160), 
                    (x_montaña + 80, ALTO)
                ])
                pygame.draw.polygon(self.pantalla, COLOR_HIERBA_OSCURA, [
                    (x_montaña + 120, ALTO), 
                    (x_montaña + 180, ALTO - 320), 
                    (x_montaña + 240, ALTO)
                ])
        
        # Montaña grande 2 (derecha) - patrón alternado
        for base_x in range(100, int(ancho_mapa + 300), 800):
            x_montaña = base_x - offset_montanas
            if -300 < x_montaña < ANCHO + 300:
                # Montaña grande con textura (llega hasta el fondo)
                pygame.draw.polygon(self.pantalla, COLOR_HIERBA, [
                    (x_montaña, ALTO), 
                    (x_montaña + 160, ALTO - 300), 
                    (x_montaña + 320, ALTO)
                ])
                # Detalles oscuros
                pygame.draw.polygon(self.pantalla, COLOR_HIERBA_OSCURA, [
                    (x_montaña + 60, ALTO), 
                    (x_montaña + 160, ALTO - 300), 
                    (x_montaña + 260, ALTO)
                ])
        
        # Montañas pequeñas adicionales (más variedad)
        for base_x in range(300, int(ancho_mapa + 300), 600):
            x_montaña = base_x - offset_montanas
            if -200 < x_montaña < ANCHO + 200:
                pygame.draw.polygon(self.pantalla, COLOR_HIERBA_OSCURA, [
                    (x_montaña, ALTO), 
                    (x_montaña + 100, ALTO - 220), 
                    (x_montaña + 200, ALTO)
                ])
        
        # ===== NUBES BLANCAS MEJORADAS =====
        offset_nubes = self.camara.x * 0.2
        for i in range(-300, int(ancho_mapa + 600), 350):
            x = i - offset_nubes
            if -150 < x < ANCHO + 150:  # Solo dibujar si está visible
                y = 80 + ((i // 350) % 3) * 40  # Altura variable
                tamaño = 30 + ((i // 350) % 2) * 6  # Tamaño variable
                
                # Nube estilo NES mejorada (como en el menú)
                pygame.draw.circle(self.pantalla, BLANCO, (int(x), int(y)), tamaño)
                pygame.draw.circle(self.pantalla, BLANCO, (int(x + tamaño), int(y - 8)), tamaño + 5)
                pygame.draw.circle(self.pantalla, BLANCO, (int(x + tamaño * 2), int(y)), tamaño)
                pygame.draw.rect(self.pantalla, BLANCO, (int(x - tamaño), int(y), tamaño * 3, tamaño))
    
    def _dibujar_hud(self) -> None:
        """Dibuja la interfaz de usuario estilo Mario Bros clásico."""
        # Fondo negro para el HUD como en Mario Bros original
        pygame.draw.rect(self.pantalla, NEGRO, (0, 0, ANCHO, 45))
        
        # Primera fila - Información principal del juego
        y_labels = 8
        y_valores = 25
        
        # SCORE (puntuación)
        texto_score_label = self.fuente_pequena.render("SCORE", True, BLANCO)
        self.pantalla.blit(texto_score_label, (15, y_labels))
        texto_score = self.fuente_pequena.render(f"{self.puntuacion:06d}", True, BLANCO)
        self.pantalla.blit(texto_score, (15, y_valores))
        
        # COINS (monedas)
        texto_coins_label = self.fuente_pequena.render("COINS", True, BLANCO)
        self.pantalla.blit(texto_coins_label, (140, y_labels))
        texto_coins = self.fuente_pequena.render(f"x{self.monedas:02d}", True, AMARILLO)
        self.pantalla.blit(texto_coins, (140, y_valores))
        
        # WORLD (mundo)
        texto_world_label = self.fuente_pequena.render("WORLD", True, BLANCO)
        self.pantalla.blit(texto_world_label, (250, y_labels))
        texto_world = self.fuente_pequena.render(f"1-{self.nivel_actual.numero}", True, BLANCO)
        self.pantalla.blit(texto_world, (250, y_valores))
        
        # TIME (tiempo)
        texto_time_label = self.fuente_pequena.render("TIME", True, BLANCO)
        self.pantalla.blit(texto_time_label, (360, y_labels))
        color_tiempo = BLANCO if self.tiempo > 100 else ROJO
        texto_time = self.fuente_pequena.render(f"{self.tiempo:03d}", True, color_tiempo)
        self.pantalla.blit(texto_time, (360, y_valores))
        
        # KEYS (llaves de quiz) - Solo si tiene llaves
        if self.quiz_manager.llaves_acumuladas > 0:
            texto_keys_label = self.fuente_pequena.render("KEYS", True, BLANCO)
            self.pantalla.blit(texto_keys_label, (470, y_labels))
            texto_keys = self.fuente_pequena.render(f"x{self.quiz_manager.llaves_acumuladas}", True, AMARILLO)
            self.pantalla.blit(texto_keys, (470, y_valores))
        
        # MARIO (estado de Mario) - Indicador visual
        texto_mario_label = self.fuente_pequena.render("MARIO", True, VERDE)
        self.pantalla.blit(texto_mario_label, (580, y_labels))
        
        # Estado visual de Mario
        if self.mario.estado == EstadoMario.FUEGO:
            estado_texto = "FIRE"
            color_estado = ROJO
        elif self.mario.estado == EstadoMario.GRANDE:
            estado_texto = "SUPER"
            color_estado = AMARILLO
        elif self.mario.estado == EstadoMario.INVENCIBLE:
            estado_texto = "STAR"
            color_estado = (255, 215, 0)
        else:
            estado_texto = "SMALL"
            color_estado = BLANCO
        
        texto_estado = self.fuente_pequena.render(estado_texto, True, color_estado)
        self.pantalla.blit(texto_estado, (580, y_valores))
        
        # LIVES (vidas) - Icono de corazón
        texto_lives_label = self.fuente_pequena.render("LIVES", True, BLANCO)
        self.pantalla.blit(texto_lives_label, (690, y_labels))
        texto_lives = self.fuente_pequena.render(f"x{self.vidas}", True, ROJO)
        self.pantalla.blit(texto_lives, (690, y_valores))
    
    def _dibujar_pausa(self) -> None:
        """Dibuja la pantalla de pausa."""
        # Fondo semi-transparente
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.set_alpha(128)
        overlay.fill(NEGRO)
        self.pantalla.blit(overlay, (0, 0))
        
        # Texto de pausa
        texto_pausa = self.fuente.render("PAUSA", True, BLANCO)
        texto_rect = texto_pausa.get_rect(center=(ANCHO // 2, ALTO // 2))
        self.pantalla.blit(texto_pausa, texto_rect)
        
        instruccion = self.fuente_pequena.render(
            "Presiona P para continuar", True, BLANCO
        )
        instruccion_rect = instruccion.get_rect(center=(ANCHO // 2, ALTO // 2 + 50))
        self.pantalla.blit(instruccion, instruccion_rect)
    
    def _dibujar_game_over(self) -> None:
        """Dibuja la pantalla de game over."""
        # Texto principal
        game_over = self.fuente.render("GAME OVER", True, ROJO)
        game_over_rect = game_over.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
        self.pantalla.blit(game_over, game_over_rect)
        
        # Puntuación final
        puntos_final = self.fuente_pequena.render(
            f"Puntuación Final: {self.puntuacion:06d}", True, BLANCO
        )
        puntos_rect = puntos_final.get_rect(center=(ANCHO // 2, ALTO // 2))
        self.pantalla.blit(puntos_final, puntos_rect)
        
        # Instrucción
        reiniciar = self.fuente_pequena.render(
            "Presiona ESPACIO para volver al menú", True, BLANCO
        )
        reiniciar_rect = reiniciar.get_rect(center=(ANCHO // 2, ALTO // 2 + 50))
        self.pantalla.blit(reiniciar, reiniciar_rect)
        
        # Efectos de partículas
        self.particulas_globales.dibujar(self.pantalla)
    
    def _dibujar_nivel_completado(self) -> None:
        """Dibuja la pantalla de nivel completado."""
        # Texto principal
        completado = self.fuente.render("¡NIVEL COMPLETADO!", True, VERDE)
        completado_rect = completado.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
        self.pantalla.blit(completado, completado_rect)
        
        # Bonus por tiempo
        bonus = self.tiempo * 50
        texto_bonus = self.fuente_pequena.render(
            f"Bonus por tiempo: {bonus}", True, AMARILLO
        )
        bonus_rect = texto_bonus.get_rect(center=(ANCHO // 2, ALTO // 2))
        self.pantalla.blit(texto_bonus, bonus_rect)
        
        # Instrucción
        continuar = self.fuente_pequena.render(
            "Presiona ESPACIO para continuar", True, BLANCO
        )
        continuar_rect = continuar.get_rect(center=(ANCHO // 2, ALTO // 2 + 50))
        self.pantalla.blit(continuar, continuar_rect)
        
        # Efectos de partículas
        self.particulas_globales.dibujar(self.pantalla)
    
    def _dibujar_juego_completado(self) -> None:
        """Dibuja la pantalla de créditos con scroll automático."""
        import math
        
        # Incrementar tiempo y scroll automático
        self.creditos_tiempo += 1
        self.creditos_scroll += 1.5  # Velocidad de scroll
        
        # Fondo degradado animado
        for y in range(0, ALTO, 2):
            color_r = max(0, min(255, int(20 + 30 * math.sin(self.creditos_tiempo * 0.02 + y * 0.01))))
            color_g = max(0, min(255, int(20 + 40 * math.sin(self.creditos_tiempo * 0.015 + y * 0.01))))
            color_b = max(0, min(255, int(80 + 60 * math.sin(self.creditos_tiempo * 0.01 + y * 0.01))))
            pygame.draw.line(self.pantalla, (color_r, color_g, color_b), (0, y), (ANCHO, y), 2)
        
        # Estrellas de fondo (partículas doradas)
        for i in range(20):
            x = (i * 40 + self.creditos_tiempo * 0.5) % ANCHO
            y = (i * 30) % ALTO
            brillo = int(155 + 100 * math.sin(self.creditos_tiempo * 0.1 + i))
            pygame.draw.circle(self.pantalla, (255, 255, brillo), (int(x), int(y)), 2)
        
        # Posición inicial de los créditos
        y_inicial = ALTO - self.creditos_scroll
        
        # ===== CRÉDITOS =====
        fuente_titulo = pygame.font.Font(None, 72)
        fuente_grande = pygame.font.Font(None, 52)
        fuente_mediana = pygame.font.Font(None, 38)
        fuente_pequena = pygame.font.Font(None, 28)
        
        y_pos = y_inicial
        
        # Título principal
        titulo = fuente_titulo.render("¡FELICIDADES!", True, AMARILLO)
        titulo_sombra = fuente_titulo.render("¡FELICIDADES!", True, NEGRO)
        titulo_rect = titulo.get_rect(center=(ANCHO // 2, y_pos))
        self.pantalla.blit(titulo_sombra, (titulo_rect.x + 3, titulo_rect.y + 3))
        self.pantalla.blit(titulo, titulo_rect)
        y_pos += 100
        
        # Subtítulo
        subtitulo = fuente_grande.render("Has rescatado a la Princesa Peach", True, ROSA)
        subtitulo_rect = subtitulo.get_rect(center=(ANCHO // 2, y_pos))
        self.pantalla.blit(subtitulo, subtitulo_rect)
        y_pos += 120
        
        # Estadísticas finales
        stats = [
            f"Puntuación Final: {self.puntuacion}",
            f"Monedas Recolectadas: {self.monedas}",
            f"Tiempo Total: {400 - self.tiempo}s",
            f"Vidas Restantes: {self.vidas}"
        ]
        for stat in stats:
            texto_stat = fuente_pequena.render(stat, True, VERDE)
            stat_rect = texto_stat.get_rect(center=(ANCHO // 2, y_pos))
            self.pantalla.blit(texto_stat, stat_rect)
            y_pos += 35
        
        y_pos += 80
        
        # ===== CRÉDITOS - DESARROLLADORES =====
        creditos_titulo = fuente_grande.render("CRÉDITOS", True, AMARILLO)
        creditos_titulo_rect = creditos_titulo.get_rect(center=(ANCHO // 2, y_pos))
        self.pantalla.blit(creditos_titulo, creditos_titulo_rect)
        y_pos += 100
        
        # Desarrolladores con roles
        desarrolladores = [
            ("DESARROLLADOR PRINCIPAL", "Camilo López Romero", AMARILLO),
            None,  # Espacio
            ("DESARROLLADOR", "Santiago Castañeda", BLANCO),
            None,
            ("DESARROLLADOR", "Juan Mantilla", BLANCO),
            None,
            ("DESARROLLADOR", "Froiland Hernández", BLANCO),
        ]
        
        for item in desarrolladores:
            if item is None:
                y_pos += 40
                continue
            
            rol, nombre, color_nombre = item
            
            # Rol
            texto_rol = fuente_pequena.render(rol, True, (200, 200, 200))
            rol_rect = texto_rol.get_rect(center=(ANCHO // 2, y_pos))
            self.pantalla.blit(texto_rol, rol_rect)
            y_pos += 35
            
            # Nombre con efecto brillante
            brillo = int(255 * abs(math.sin(self.creditos_tiempo * 0.05)))
            color_brillo = (min(255, color_nombre[0] + brillo // 3), 
                           min(255, color_nombre[1] + brillo // 3), 
                           min(255, color_nombre[2] + brillo // 3))
            texto_nombre = fuente_mediana.render(nombre, True, color_brillo)
            nombre_sombra = fuente_mediana.render(nombre, True, NEGRO)
            nombre_rect = texto_nombre.get_rect(center=(ANCHO // 2, y_pos))
            self.pantalla.blit(nombre_sombra, (nombre_rect.x + 2, nombre_rect.y + 2))
            self.pantalla.blit(texto_nombre, nombre_rect)
            y_pos += 60
        
        y_pos += 100
        
        # Agradecimientos
        agradecimientos = fuente_mediana.render("Gracias por jugar", True, VERDE)
        agradecimientos_rect = agradecimientos.get_rect(center=(ANCHO // 2, y_pos))
        self.pantalla.blit(agradecimientos, agradecimientos_rect)
        y_pos += 100
        
        # Año
        año = fuente_pequena.render("© 2025 - Super Mario Bros Adventure Edition", True, (150, 150, 150))
        año_rect = año.get_rect(center=(ANCHO // 2, y_pos))
        self.pantalla.blit(año, año_rect)
        y_pos += 150
        
        # Mensaje final
        if self.creditos_scroll > y_pos - ALTO + 100:
            final = fuente_grande.render("¡THE END!", True, AMARILLO)
            final_sombra = fuente_grande.render("¡THE END!", True, NEGRO)
            final_rect = final.get_rect(center=(ANCHO // 2, ALTO // 2))
            self.pantalla.blit(final_sombra, (final_rect.x + 3, final_rect.y + 3))
            self.pantalla.blit(final, final_rect)
            
            # Instrucción para salir
            salir = fuente_pequena.render("Presiona ESPACIO para volver al menú", True, BLANCO)
            salir_rect = salir.get_rect(center=(ANCHO // 2, ALTO // 2 + 60))
            if int(self.creditos_tiempo / 30) % 2 == 0:  # Parpadeo
                self.pantalla.blit(salir, salir_rect)
        
        # Efectos de partículas
        self.particulas_globales.dibujar(self.pantalla)
    
    def _dibujar_contador_llaves(self) -> None:
        """Dibuja el contador de llaves en el HUD."""
        # Posición para las llaves
        pos_x, pos_y = CONFIGURACION_LLAVES['posicion_contador']
        
        # Etiqueta KEYS
        texto_keys_label = self.fuente_pequena.render("KEYS", True, BLANCO)
        self.pantalla.blit(texto_keys_label, (pos_x - 60, 5))
        
        # Número de llaves
        llaves = self.quiz_manager.llaves_acumuladas
        texto_keys = self.fuente_pequena.render(f"{llaves:02d}", True, CONFIGURACION_LLAVES['color_contador'])
        self.pantalla.blit(texto_keys, (pos_x - 60, 20))
        
        # Icono de llave
        self._dibujar_icono_llave(pos_x - 30, 15)
        
    def _dibujar_icono_llave(self, x: int, y: int) -> None:
        """Dibuja un pequeño icono de llave."""
        color_llave = CONFIGURACION_LLAVES['color_llave']
        
        # Cuerpo de la llave (círculo)
        pygame.draw.circle(self.pantalla, color_llave, (x, y), 4)
        pygame.draw.circle(self.pantalla, NEGRO, (x, y), 4, 1)
        
        # Mango de la llave (línea)
        pygame.draw.line(self.pantalla, color_llave, (x + 4, y), (x + 12, y), 2)
        
        # Dientes de la llave
        pygame.draw.line(self.pantalla, color_llave, (x + 10, y), (x + 10, y + 3), 1)
        pygame.draw.line(self.pantalla, color_llave, (x + 12, y), (x + 12, y + 2), 1)
        
    def _verificar_colisiones_puertas(self) -> None:
        """Verifica las colisiones entre Mario y las puertas del nivel."""
        if not hasattr(self.nivel_actual, 'puertas'):
            return
            
        mario_rect = self.mario.rect
        
        # Obtener estado actual de la tecla E
        teclas = pygame.key.get_pressed()
        tecla_e_actual = teclas[pygame.K_e]
        
        # Detectar si E se acaba de presionar (no estaba presionada antes, pero ahora sí)
        tecla_e_recien_presionada = tecla_e_actual and not self.tecla_e_presionada_anterior
        
        for puerta in self.nivel_actual.puertas:
            if not puerta.abierta and mario_rect.colliderect(puerta.get_rect()):
                # Activar efecto de brillo cuando Mario está cerca
                puerta.activar_brillo()
                
                # Si Mario acaba de presionar E cerca de una puerta (solo una vez por pulsación)
                if tecla_e_recien_presionada:
                    self._intentar_abrir_puerta(puerta)
            else:
                puerta.desactivar_brillo()
        
        # Actualizar estado anterior de la tecla E
        self.tecla_e_presionada_anterior = tecla_e_actual
                
    def _intentar_abrir_puerta(self, puerta: Puerta) -> None:
        """
        Intenta abrir una puerta iniciando un quiz.
        
        Args:
            puerta: La puerta que se intenta abrir
        """
        if self.quiz_manager.esta_activo():
            return  # Ya hay un quiz activo
            
        # Verificar si se puede abrir la puerta
        if puerta.puede_intentar_abrir(self.quiz_manager.llaves_acumuladas):
            # Asignar referencia del nivel al quiz manager
            self.quiz_manager.nivel_actual = self.nivel_actual
            
            # Iniciar el quiz
            if self.quiz_manager.iniciar_quiz(puerta, self.nivel_actual.numero):
                # Quiz iniciado exitosamente
                pass
        else:
            # No tiene suficientes llaves - mostrar mensaje
            self._mostrar_mensaje_llaves_insuficientes(puerta.llaves_requeridas)
            
    def _mostrar_mensaje_llaves_insuficientes(self, llaves_necesarias: int) -> None:
        """Muestra un mensaje cuando no se tienen suficientes llaves."""
        # Agregar partículas rojas para indicar que no se puede abrir
        self.particulas_globales.crear_explosion(
            self.mario.rect.centerx, self.mario.rect.centery - 20,
            color=(255, 100, 100), cantidad=10
        )
    
    def _actualizar_sistema_dragon(self) -> None:
        """
        Actualiza el sistema del jefe final (dragón) en el nivel 5.
        Maneja la activación del dragón y el procesamiento de respuestas del quiz.
        """
        # Solo en el nivel 5
        if self.nivel_actual.numero != 5:
            return
        
        # Verificar si hay un dragón en el nivel
        if not hasattr(self.nivel_actual, 'dragon') or self.nivel_actual.dragon is None:
            return
        
        dragon = self.nivel_actual.dragon
        
        # Activar dragón cuando Mario se acerca
        if not dragon.activo and not dragon.derrotado:
            if dragon.esta_cerca_de_mario(self.mario.rect.x):
                dragon.activar()
                # Efecto visual de activación
                self.particulas_globales.crear_explosion(
                    dragon.rect.centerx, dragon.rect.centery,
                    color=(255, 0, 0), cantidad=30
                )
                
                # Iniciar batalla automáticamente con una pregunta
                self._iniciar_batalla_dragon()
        
        # Procesar respuestas del quiz cuando el dragón está activo
        if dragon.activo and not dragon.derrotado:
            if self.quiz_manager.hay_respuesta_pendiente():
                fue_correcta, hubo_respuesta = self.quiz_manager.obtener_y_marcar_respuesta()
                
                if hubo_respuesta:
                    if fue_correcta:
                        # ¡Mario ataca al dragón!
                        fue_derrotado = dragon.recibir_danio()
                        
                        # Efectos visuales de ataque
                        self.particulas_globales.crear_explosion(
                            dragon.rect.centerx, dragon.rect.centery,
                            color=(255, 215, 0), cantidad=20
                        )
                        
                        # Puntos bonus por dañar al dragón
                        self.puntuacion += 1000
                        
                        if fue_derrotado:
                            # ¡Dragón derrotado!
                            self.puntuacion += 5000  # Bonus por derrotar al jefe
                            
                            # Efecto visual épico de victoria
                            self.particulas_globales.crear_explosion(
                                dragon.rect.centerx, dragon.rect.centery,
                                color=(255, 215, 0), cantidad=50
                            )
                            
                            # Ahora Mario puede rescatar a la princesa
                            print("¡Dragón derrotado! ¡La princesa puede ser rescatada!")
                    else:
                        # ¡Respuesta incorrecta! Mario recibe daño del dragón
                        # El dragón lanza fuego (activar animación)
                        dragon.disparar_fuego()
                        
                        # Efecto visual de ataque del dragón
                        self.particulas_globales.crear_explosion(
                            self.mario.rect.centerx, self.mario.rect.centery,
                            color=(255, 140, 0), cantidad=15
                        )
                        
                        # Mario pierde una vida pero NO se reinicia el nivel
                        # Solo retrocede un poco
                        self.vidas -= 1
                        self.mario.rect.x -= 100  # Retrocede 100 píxeles
                        
                        # Si Mario se queda sin vidas, entonces sí muere
                        if self.vidas <= 0:
                            self._mario_muere()
                        else:
                            # Mario sigue vivo, puede intentar de nuevo
                            # Invulnerabilidad temporal de 8 segundos
                            self.mario.estado = EstadoMario.INVENCIBLE
                            self.mario.tiempo_power_up = 480  # 8 segundos de invencibilidad (60 FPS * 8)
                        
            # Iniciar nueva pregunta si el dragón sigue activo y no hay quiz activo
            if not self.quiz_manager.esta_activo() and dragon.vida_actual > 0:
                self._iniciar_batalla_dragon()
    
    def _iniciar_batalla_dragon(self) -> None:
        """
        Inicia una batalla contra el dragón mostrando una pregunta de quiz.
        """
        # Crear una puerta temporal para el sistema de quiz
        from src.entities.puerta import Puerta
        from src.utils.preguntas import TipoPuerta
        
        # Puerta temporal para la batalla del dragón (no se dibuja, solo para el quiz)
        puerta_temporal = Puerta(self.mario.rect.x, self.mario.rect.y, TipoPuerta.OBLIGATORIA, llaves_requeridas=0)
        
        # Asignar referencia del nivel al quiz manager
        self.quiz_manager.nivel_actual = self.nivel_actual
        
        # Iniciar el quiz con pregunta de nivel 5 (MIXTO AVANZADO)
        self.quiz_manager.iniciar_quiz(puerta_temporal, 5)
            
    def _procesar_respuesta_quiz(self, es_correcta: bool) -> None:
        """
        Procesa el resultado de una respuesta del quiz.
        
        Args:
            es_correcta: True si la respuesta fue correcta
        """
        if es_correcta:
            # Respuesta correcta: dar puntos bonus
            puntos_bonus = self.quiz_manager.get_puntos_bonus()
            self.puntuacion += puntos_bonus
            
            # Efectos de éxito
            for _ in range(20):
                self.particulas_globales.agregar_particula(
                    400, 300, color=AMARILLO, velocidad_y=-5, vida=60
                )
        else:
            # Respuesta incorrecta: perder vida
            self._perder_vida()
            
            # Efectos de error
            for _ in range(15):
                self.particulas_globales.agregar_particula(
                    400, 300, color=ROJO, velocidad_y=-3, vida=45
                )
                
    def _perder_vida(self) -> None:
        """Hace que Mario pierda una vida por respuesta incorrecta."""
        self.vidas -= 1
        
        if self.vidas <= 0:
            self.estado = EstadoJuego.GAME_OVER
        else:
            # Reiniciar la posición de Mario al inicio del nivel
            self.mario.rect.x = 50
            self.mario.rect.y = 400
            self.mario.velocidad_x = 0
            self.mario.velocidad_y = 0