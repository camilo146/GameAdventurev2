"""
Sistema de Debug y Detección de Bugs para Super Mario Bros 2005
Herramienta para identificar y diagnosticar problemas en tiempo real.
"""

import pygame
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.juego import Juego
from src.utils.constantes import *

class DebugOverlay:
    """Overlay de información de debug sobre el juego."""
    
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.fuente_pequena = pygame.font.Font(None, 18)
        self.fuente_titulo = pygame.font.Font(None, 24)
        self.mostrar = True
        self.modo = 'completo'  # 'completo', 'simple', 'oculto'
        self.logs = []
        self.max_logs = 10
        
    def log(self, mensaje):
        """Añade un mensaje al log."""
        self.logs.append(mensaje)
        if len(self.logs) > self.max_logs:
            self.logs.pop(0)
        print(f"[DEBUG] {mensaje}")
    
    def toggle_modo(self):
        """Cambia entre modos de visualización."""
        modos = ['completo', 'simple', 'oculto']
        idx = modos.index(self.modo)
        self.modo = modos[(idx + 1) % len(modos)]
        self.log(f"Modo debug: {self.modo}")
    
    def dibujar(self, juego):
        """Dibuja la información de debug."""
        if self.modo == 'oculto':
            return
        
        # Panel semi-transparente
        panel_ancho = 400 if self.modo == 'completo' else 250
        panel_alto = 450 if self.modo == 'completo' else 200
        panel = pygame.Surface((panel_ancho, panel_alto))
        panel.set_alpha(200)
        panel.fill((0, 0, 0))
        
        y_offset = 5
        
        # Título
        titulo = self.fuente_titulo.render("DEBUG MODE", True, AMARILLO)
        panel.blit(titulo, (5, y_offset))
        y_offset += 25
        
        # Información básica
        info_basica = [
            f"FPS: {int(juego.reloj.get_fps())}",
            f"Estado: {juego.estado.value}",
            f"Vidas: {juego.vidas}",
            f"Puntos: {juego.puntuacion}",
            f"Monedas: {juego.monedas}",
            f"Tiempo: {juego.tiempo}",
        ]
        
        for linea in info_basica:
            texto = self.fuente_pequena.render(linea, True, BLANCO)
            panel.blit(texto, (5, y_offset))
            y_offset += 18
        
        if self.modo == 'completo':
            # Separador
            pygame.draw.line(panel, BLANCO, (5, y_offset), (panel_ancho - 5, y_offset))
            y_offset += 5
            
            # Información de Mario
            mario = juego.mario
            info_mario = [
                f"MARIO:",
                f"  Pos: ({mario.rect.x:.0f}, {mario.rect.y:.0f})",
                f"  Vel: ({mario.velocidad_x:.1f}, {mario.velocidad_y:.1f})",
                f"  Estado: {mario.estado.value}",
                f"  Vivo: {mario.vivo}",
                f"  Saltando: {mario.saltando}",
                f"  Invencible: {mario.invencible}",
                f"  Corriendo: {mario.corriendo}",
            ]
            
            for linea in info_mario:
                color = VERDE if "MARIO:" in linea else BLANCO
                texto = self.fuente_pequena.render(linea, True, color)
                panel.blit(texto, (5, y_offset))
                y_offset += 18
            
            # Información del nivel
            nivel = juego.nivel_actual
            info_nivel = [
                f"NIVEL:",
                f"  Número: {nivel.numero}",
                f"  Plataformas: {len(nivel.plataformas)}",
                f"  Enemigos: {len([e for e in nivel.enemigos if e.vivo])}",
                f"  Monedas: {len(nivel.monedas)}",
                f"  Power-ups: {len(nivel.powerups)}",
            ]
            
            for linea in info_nivel:
                color = AMARILLO if "NIVEL:" in linea else BLANCO
                texto = self.fuente_pequena.render(linea, True, color)
                panel.blit(texto, (5, y_offset))
                y_offset += 18
            
            # Sistema de muerte
            if juego.esperando_reinicio:
                texto = self.fuente_pequena.render(f"ESPERANDO REINICIO: {juego.muerte_timer}/{juego.muerte_delay}", True, ROJO)
                panel.blit(texto, (5, y_offset))
                y_offset += 18
        
        # Logs recientes
        if self.logs:
            pygame.draw.line(panel, BLANCO, (5, y_offset), (panel_ancho - 5, y_offset))
            y_offset += 5
            texto = self.fuente_pequena.render("LOGS:", True, AMARILLO)
            panel.blit(texto, (5, y_offset))
            y_offset += 18
            
            for log in self.logs[-5:]:
                texto = self.fuente_pequena.render(log[:45], True, (200, 200, 200))
                panel.blit(texto, (5, y_offset))
                y_offset += 16
        
        # Controles
        y_offset = panel_alto - 40
        controles = [
            "F1: Toggle Debug | F2: Bugs",
            "F3: Reiniciar | ESC: Salir"
        ]
        for linea in controles:
            texto = self.fuente_pequena.render(linea, True, (150, 150, 150))
            panel.blit(texto, (5, y_offset))
            y_offset += 16
        
        self.pantalla.blit(panel, (10, 10))


class DetectorBugs:
    """Detecta bugs potenciales en tiempo real."""
    
    def __init__(self, debug_overlay):
        self.debug = debug_overlay
        self.bugs_detectados = []
        self.frame_count = 0
        
    def verificar(self, juego):
        """Verifica bugs potenciales cada cierto número de frames."""
        self.frame_count += 1
        
        if self.frame_count % 60 != 0:  # Verificar cada segundo
            return
        
        bugs_actuales = []
        
        # Bug 1: Mario fuera de los límites del nivel
        if juego.mario.rect.x < -100 or juego.mario.rect.x > juego.nivel_actual.ancho_mapa + 100:
            bugs_actuales.append("⚠ Mario fuera límites horizontales")
            self.debug.log(f"Bug: Mario en X={juego.mario.rect.x}")
        
        # Bug 2: Mario cayendo infinitamente
        if juego.mario.rect.y > ALTO + 200 and juego.mario.vivo:
            bugs_actuales.append("⚠ Mario cayendo infinitamente")
            self.debug.log(f"Bug: Mario en Y={juego.mario.rect.y}")
        
        # Bug 3: Velocidad excesiva
        if abs(juego.mario.velocidad_x) > 20 or abs(juego.mario.velocidad_y) > 30:
            bugs_actuales.append("⚠ Velocidad excesiva")
            self.debug.log(f"Bug: Vel=({juego.mario.velocidad_x}, {juego.mario.velocidad_y})")
        
        # Bug 4: Enemigos fuera del mapa
        for i, enemigo in enumerate(juego.nivel_actual.enemigos):
            if enemigo.rect.y > ALTO + 100 and enemigo.vivo:
                bugs_actuales.append(f"⚠ Enemigo {i} cayendo")
                self.debug.log(f"Bug: Enemigo {i} en Y={enemigo.rect.y}")
        
        # Bug 5: Estado inconsistente (muriendo pero vivo)
        if juego.mario.estado == EstadoMario.MURIENDO and juego.mario.vivo:
            bugs_actuales.append("⚠ Estado inconsistente (muriendo pero vivo)")
            self.debug.log("Bug: Mario muriendo pero vivo=True")
        
        # Bug 6: Esperando reinicio pero no en estado muriendo
        if juego.esperando_reinicio and juego.mario.estado != EstadoMario.MURIENDO:
            bugs_actuales.append("⚠ Esperando reinicio sin estar muriendo")
            self.debug.log(f"Bug: esperando_reinicio=True, estado={juego.mario.estado}")
        
        # Bug 7: Tiempo negativo
        if juego.tiempo < 0:
            bugs_actuales.append("⚠ Tiempo negativo")
            self.debug.log(f"Bug: Tiempo={juego.tiempo}")
        
        # Bug 8: Colisión continua con enemigo (solo si Mario está vivo y no muriendo)
        # NOTA: Es normal tener colisión momentánea sin invencibilidad, 
        # solo es bug si persiste cuando Mario debería estar invencible
        if juego.mario.vivo and juego.mario.estado != EstadoMario.MURIENDO:
            for enemigo in juego.nivel_actual.enemigos:
                if enemigo.vivo and not enemigo.aplastado and juego.mario.rect.colliderect(enemigo.rect):
                    # Solo es bug si Mario ya recibió daño recientemente (debería estar invencible)
                    if juego.mario.invencible <= 0 and juego.mario.estado != EstadoMario.INVENCIBLE:
                        # Verificar si es colisión desde arriba (aplastamiento válido)
                        es_aplastamiento = (juego.mario.velocidad_y > 0 and 
                                          juego.mario.rect.bottom - juego.mario.velocidad_y <= enemigo.rect.top + 10)
                        if not es_aplastamiento:
                            bugs_actuales.append("⚠ Colisión lateral sin invencibilidad")
                            self.debug.log(f"Bug: Colisión con enemigo {enemigo} sin invencibilidad activa")
        
        self.bugs_detectados = bugs_actuales
    
    def dibujar(self, pantalla):
        """Dibuja los bugs detectados."""
        if not self.bugs_detectados:
            return
        
        panel = pygame.Surface((400, min(300, 30 + len(self.bugs_detectados) * 25)))
        panel.set_alpha(220)
        panel.fill((100, 0, 0))
        
        fuente = pygame.font.Font(None, 20)
        titulo = fuente.render("BUGS DETECTADOS", True, (255, 255, 0))
        panel.blit(titulo, (10, 5))
        
        y = 30
        for bug in self.bugs_detectados:
            texto = fuente.render(bug, True, (255, 200, 200))
            panel.blit(texto, (10, y))
            y += 25
        
        pantalla.blit(panel, (ANCHO - 410, 10))


def main():
    """Función principal del modo debug."""
    pygame.init()
    pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
    
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Super Mario Bros 2005 - DEBUG MODE")
    reloj = pygame.time.Clock()
    
    # Crear juego
    juego = Juego(pantalla, reloj)
    
    # Crear sistemas de debug
    debug_overlay = DebugOverlay(pantalla)
    detector_bugs = DetectorBugs(debug_overlay)
    
    debug_overlay.log("Sistema de debug iniciado")
    debug_overlay.log("F1: Toggle modo debug")
    debug_overlay.log("F2: Mostrar/ocultar bugs")
    debug_overlay.log("F3: Reiniciar nivel")
    
    mostrar_bugs = True
    ejecutando = True
    
    print("\n" + "="*60)
    print("  SUPER MARIO BROS 2005 - MODO DEBUG")
    print("="*60)
    print("\nControles especiales:")
    print("  F1 - Cambiar modo debug (completo/simple/oculto)")
    print("  F2 - Mostrar/ocultar detector de bugs")
    print("  F3 - Reiniciar nivel")
    print("  F4 - Dar vida extra")
    print("  F5 - Añadir 1000 puntos")
    print("  ESC - Salir\n")
    print("Controles del juego:")
    print("  SPACE - Saltar (en menú: iniciar)")
    print("  FLECHAS o A/D - Mover")
    print("  SHIFT - Correr")
    print("  P - Pausar")
    print("="*60 + "\n")
    
    while ejecutando:
        dt = reloj.tick(FPS)
        
        # Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_F1:
                    debug_overlay.toggle_modo()
                elif evento.key == pygame.K_F2:
                    mostrar_bugs = not mostrar_bugs
                    debug_overlay.log(f"Detector bugs: {'ON' if mostrar_bugs else 'OFF'}")
                elif evento.key == pygame.K_F3:
                    if juego.estado == EstadoJuego.JUGANDO:
                        juego._reiniciar_nivel()
                        debug_overlay.log("Nivel reiniciado")
                elif evento.key == pygame.K_F4:
                    juego.vidas += 1
                    debug_overlay.log(f"Vida añadida. Total: {juego.vidas}")
                elif evento.key == pygame.K_F5:
                    juego.puntuacion += 1000
                    debug_overlay.log(f"Puntos añadidos. Total: {juego.puntuacion}")
                else:
                    juego._manejar_tecla(evento.key)
        
        # Actualizar según el estado
        if juego.estado == EstadoJuego.MENU:
            juego._actualizar_menu()
        elif juego.estado == EstadoJuego.JUGANDO:
            juego._actualizar_juego()
            # Detectar bugs
            if mostrar_bugs:
                detector_bugs.verificar(juego)
        elif juego.estado == EstadoJuego.PAUSA:
            juego._actualizar_pausa()
        elif juego.estado == EstadoJuego.GAME_OVER:
            juego._actualizar_game_over()
        elif juego.estado == EstadoJuego.NIVEL_COMPLETADO:
            juego._actualizar_nivel_completado()
        
        # Dibujar según el estado
        pantalla.fill(AZUL_CIELO)
        
        if juego.estado == EstadoJuego.MENU:
            juego._dibujar_menu()
        elif juego.estado == EstadoJuego.JUGANDO:
            juego._dibujar_juego()
        elif juego.estado == EstadoJuego.PAUSA:
            juego._dibujar_juego()
            juego._dibujar_pausa()
        elif juego.estado == EstadoJuego.GAME_OVER:
            juego._dibujar_game_over()
        elif juego.estado == EstadoJuego.NIVEL_COMPLETADO:
            juego._dibujar_nivel_completado()
        
        # Dibujar overlays de debug
        debug_overlay.dibujar(juego)
        
        if mostrar_bugs:
            detector_bugs.dibujar(pantalla)
        
        pygame.display.flip()
    
    pygame.quit()
    print("\nModo debug finalizado.")
    print(f"Bugs detectados durante la sesión: {len(detector_bugs.bugs_detectados)}")


if __name__ == "__main__":
    main()
