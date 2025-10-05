"""
Clase principal del juego Super Mario Bros 2005.
"""

import pygame
import sys
from typing import Optional
from src.entities.mario import Mario
from src.entities.powerup import PowerUp
from src.core.nivel import Nivel
from src.core.camara import Camara
from src.utils.constantes import *
from src.utils.sonidos import gestor_sonidos
from src.utils.particulas import SistemaParticulas

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
        self.nivel_actual = Nivel(1)
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
        
        # Fuente para texto
        self.fuente = pygame.font.Font(None, 36)
        self.fuente_pequena = pygame.font.Font(None, 24)
        
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
            elif self.estado == EstadoJuego.PAUSA:
                self._actualizar_pausa()
            elif self.estado == EstadoJuego.GAME_OVER:
                self._actualizar_game_over()
            elif self.estado == EstadoJuego.NIVEL_COMPLETADO:
                self._actualizar_nivel_completado()
            
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
            
            pygame.display.flip()
    
    def _manejar_tecla(self, tecla: int) -> None:
        """
        Maneja las teclas presionadas.
        
        Args:
            tecla: Código de la tecla presionada
        """
        if self.estado == EstadoJuego.MENU:
            if tecla == pygame.K_SPACE or tecla == pygame.K_RETURN:
                self._iniciar_juego()
        elif self.estado == EstadoJuego.JUGANDO:
            if tecla == pygame.K_SPACE:
                self.mario.saltar()
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
    
    def _iniciar_juego(self) -> None:
        """Inicia una nueva partida."""
        self.estado = EstadoJuego.JUGANDO
        self.mario = Mario(50, 400)
        self.nivel_actual = Nivel(1)
        self.camara = Camara(self.nivel_actual.ancho_mapa)
        self.puntuacion = 0
        self.vidas = 3
        self.monedas = 0
        self.tiempo = 400
        # gestor_sonidos.reproducir_musica('nivel.mp3', -1)
    
    def _actualizar_menu(self) -> None:
        """Actualiza el estado del menú."""
        self.particulas_globales.update()
    
    def _actualizar_juego(self) -> None:
        """Actualiza la lógica principal del juego."""
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
        
        # Verificar colisiones
        self._verificar_colisiones()
        
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
    
    def _verificar_colisiones(self) -> None:
        """Verifica las colisiones entre entidades."""
        mario_rect = self.mario.rect
        
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
                elif (self.mario.velocidad_y > 0 and 
                      self.mario.rect.bottom <= enemigo.rect.top + 15 and
                      self.mario.rect.centerx >= enemigo.rect.left - 10 and
                      self.mario.rect.centerx <= enemigo.rect.right + 10):
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
                    if self.mario.recibir_dano():
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
        # Verificar caída (muerte más rápida cuando cae al vacío)
        if self.mario.rect.y > ALTO + 50:  # Muerte más rápida al caer
            self._mario_muere()
        
        # Verificar límites del mapa (permitir movimiento completo)
        if self.mario.rect.x < 0:
            self.mario.rect.x = 0
        # Eliminar límite derecho - Mario puede avanzar por todo el nivel
    
    def _mario_muere(self) -> None:
        """Maneja la muerte de Mario."""
        self.vidas -= 1
        self.particulas_globales.crear_explosion(
            self.mario.rect.centerx, self.mario.rect.centery, ROJO, 20
        )
        
        if self.vidas <= 0:
            self.estado = EstadoJuego.GAME_OVER
            gestor_sonidos.detener_musica()
        else:
            self._reiniciar_nivel()
    
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
    
    def _siguiente_nivel(self) -> None:
        """Pasa al siguiente nivel."""
        self.nivel_actual = Nivel(self.nivel_actual.numero + 1)
        self.camara = Camara(self.nivel_actual.ancho_mapa)
        self.mario = Mario(50, 400)
        self.estado = EstadoJuego.JUGANDO
        self.tiempo = 400
        # gestor_sonidos.reproducir_musica('nivel.mp3', -1)
    
    def _reiniciar_nivel(self) -> None:
        """Reinicia el nivel actual."""
        self.mario = Mario(50, 400)
        self.nivel_actual.reiniciar()
        self.camara = Camara(self.nivel_actual.ancho_mapa)
        self.tiempo = 400
        self.tiempo_contador = 0
    
    def _reiniciar_juego(self) -> None:
        """Reinicia completamente el juego."""
        self.estado = EstadoJuego.MENU
        self.particulas_globales.limpiar()
    
    def _dibujar_menu(self) -> None:
        """Dibuja el menú principal."""
        # Título
        titulo = self.fuente.render("SUPER MARIO BROS 2005", True, BLANCO)
        titulo_rect = titulo.get_rect(center=(ANCHO // 2, 150))
        self.pantalla.blit(titulo, titulo_rect)
        
        # Instrucciones
        instrucciones = [
            "PRESIONA ESPACIO PARA EMPEZAR",
            "",
            "CONTROLES:",
            "Flechas/WASD - Mover",
            "Espacio - Saltar",
            "Shift - Correr",
            "P - Pausa",
            "R - Reiniciar nivel"
        ]
        
        y = 250
        for linea in instrucciones:
            texto = self.fuente_pequena.render(linea, True, BLANCO)
            texto_rect = texto.get_rect(center=(ANCHO // 2, y))
            self.pantalla.blit(texto, texto_rect)
            y += 30
        
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
        
        # Dibujar partículas globales
        self.particulas_globales.dibujar(self.pantalla)
        
        # Dibujar HUD
        self._dibujar_hud()
    
    def _dibujar_fondo(self) -> None:
        """Dibuja el fondo estilo Mario Bros clásico."""
        # Fondo azul cielo sólido como en Mario Bros
        self.pantalla.fill(AZUL_CIELO)
        
        # Nubes estilo Mario Bros (formas más pixeladas)
        offset_nubes = self.camara.x * 0.2
        for i in range(-200, ANCHO + 400, 200):
            x = (i - offset_nubes) % (ANCHO + 600) - 200
            y = 100 + (i % 3) * 30  # Altura variable
            
            # Nube estilo pixel art como en Mario Bros
            # Círculo central grande
            pygame.draw.circle(self.pantalla, BLANCO, (int(x + 40), int(y + 20)), 16)
            # Círculos laterales
            pygame.draw.circle(self.pantalla, BLANCO, (int(x + 15), int(y + 25)), 12)
            pygame.draw.circle(self.pantalla, BLANCO, (int(x + 65), int(y + 25)), 12)
            # Círculos superiores
            pygame.draw.circle(self.pantalla, BLANCO, (int(x + 25), int(y + 10)), 8)
            pygame.draw.circle(self.pantalla, BLANCO, (int(x + 55), int(y + 10)), 8)
        
        # Colinas verdes distantes (como las colinas en algunos niveles de Mario)
        offset_colinas = self.camara.x * 0.1
        for i in range(-400, ANCHO + 400, 300):
            x = (i - offset_colinas) % (ANCHO + 800) - 400
            # Colina simple y redondeada
            puntos = [
                (x, ALTO),
                (x, 480),
                (x + 50, 460),
                (x + 100, 450),
                (x + 150, 460),
                (x + 200, 480),
                (x + 200, ALTO)
            ]
            pygame.draw.polygon(self.pantalla, (0, 140, 0), puntos)
    
    def _dibujar_hud(self) -> None:
        """Dibuja la interfaz de usuario estilo Mario Bros clásico."""
        # Fondo negro para el HUD como en Mario Bros original
        pygame.draw.rect(self.pantalla, NEGRO, (0, 0, ANCHO, 40))
        
        # SCORE (como en Mario Bros original)
        texto_score_label = self.fuente_pequena.render("SCORE", True, BLANCO)
        self.pantalla.blit(texto_score_label, (20, 5))
        texto_score = self.fuente_pequena.render(f"{self.puntuacion:06d}", True, BLANCO)
        self.pantalla.blit(texto_score, (20, 20))
        
        # COINS (monedas como en Mario Bros)
        texto_coins_label = self.fuente_pequena.render("COINS", True, BLANCO)
        self.pantalla.blit(texto_coins_label, (200, 5))
        texto_coins = self.fuente_pequena.render(f"{self.monedas:02d}", True, BLANCO)
        self.pantalla.blit(texto_coins, (200, 20))
        
        # WORLD (mundo - estático)
        texto_world_label = self.fuente_pequena.render("WORLD", True, BLANCO)
        self.pantalla.blit(texto_world_label, (350, 5))
        texto_world = self.fuente_pequena.render("1-1", True, BLANCO)
        self.pantalla.blit(texto_world, (350, 20))
        
        # TIME (tiempo como en Mario Bros original)
        texto_time_label = self.fuente_pequena.render("TIME", True, BLANCO)
        self.pantalla.blit(texto_time_label, (500, 5))
        color_tiempo = BLANCO if self.tiempo > 100 else ROJO
        texto_time = self.fuente_pequena.render(f"{self.tiempo:03d}", True, color_tiempo)
        self.pantalla.blit(texto_time, (500, 20))
        
        # LIVES (vidas en la esquina superior derecha)
        texto_lives_label = self.fuente_pequena.render("LIVES", True, BLANCO)
        self.pantalla.blit(texto_lives_label, (ANCHO - 80, 5))
        texto_lives = self.fuente_pequena.render(f"{self.vidas}", True, BLANCO)
        self.pantalla.blit(texto_lives, (ANCHO - 50, 20))
        
        # Nivel
        texto_nivel = self.fuente_pequena.render(
            f"NIVEL: {self.nivel_actual.numero}", True, BLANCO
        )
        self.pantalla.blit(texto_nivel, (550, 10))
        
        # Estado de Mario
        estado_texto = ""
        if self.mario.estado == EstadoMario.PEQUENO:
            estado_texto = "MARIO"
        elif self.mario.estado == EstadoMario.GRANDE:
            estado_texto = "SUPER"
        elif self.mario.estado == EstadoMario.FUEGO:
            estado_texto = "FUEGO"
        elif self.mario.estado == EstadoMario.INVENCIBLE:
            estado_texto = "ESTRELLA"
            
        texto_estado = self.fuente_pequena.render(estado_texto, True, VERDE)
        self.pantalla.blit(texto_estado, (650, 10))
        
        # Instrucciones básicas
        instrucciones = self.fuente_pequena.render(
            "ESPACIO: Saltar | SHIFT: Correr | P: Pausa", True, BLANCO
        )
        self.pantalla.blit(instrucciones, (10, 35))
    
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