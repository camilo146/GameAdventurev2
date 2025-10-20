"""
Test de Bugs Específicos - Super Mario Bros 2005
Script para probar y reproducir bugs conocidos o potenciales.
"""

import pygame
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.entities.mario import Mario
from src.entities.plataforma import Plataforma
from src.entities.enemigo import Enemigo
from src.utils.constantes import *

def test_colision_enemigo():
    """Test de colisión con enemigos."""
    print("\n" + "="*60)
    print("TEST 1: Colisión con Enemigos")
    print("="*60)
    
    pygame.init()
    pantalla = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Test: Colisión Enemigos")
    reloj = pygame.time.Clock()
    
    # Crear Mario y enemigo
    mario = Mario(300, 400)
    enemigo = Enemigo(350, 400, 'goomba')
    plataformas = [Plataforma(0, 550, 800, 50, 'suelo')]
    
    print(f"Mario inicial: Pos=({mario.rect.x}, {mario.rect.y}), Vivo={mario.vivo}")
    print(f"Enemigo: Pos=({enemigo.rect.x}, {enemigo.rect.y}), Vivo={enemigo.vivo}")
    print("\nInstrucciones:")
    print("  - Mario debería empujarse hacia atrás al tocar el enemigo")
    print("  - Usa DERECHA para mover a Mario hacia el enemigo")
    print("  - ESC para salir y continuar con siguiente test")
    
    ejecutando = True
    colisiones = 0
    
    while ejecutando:
        reloj.tick(60)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                ejecutando = False
        
        # Actualizar
        mario.update(plataformas)
        enemigo.update(plataformas)
        
        # Verificar colisión
        if mario.rect.colliderect(enemigo.rect) and enemigo.vivo:
            colisiones += 1
            if colisiones % 60 == 0:  # Cada segundo
                print(f"⚠ Colisión detectada! Total: {colisiones//60}s")
                print(f"   Mario invencible: {mario.invencible}")
                print(f"   Mario estado: {mario.estado}")
        
        # Dibujar
        pantalla.fill(AZUL_CIELO)
        for plat in plataformas:
            plat.dibujar(pantalla)
        mario.dibujar(pantalla)
        enemigo.dibujar(pantalla)
        
        # Info
        fuente = pygame.font.Font(None, 20)
        info = [
            f"Colisiones: {colisiones//60}s",
            f"Mario invencible: {mario.invencible}",
            f"Mario estado: {mario.estado.value}",
            f"Presiona ESC para siguiente test"
        ]
        for i, linea in enumerate(info):
            texto = fuente.render(linea, True, NEGRO)
            pantalla.blit(texto, (10, 10 + i * 20))
        
        pygame.display.flip()
    
    pygame.quit()
    print(f"\n✓ Test completado. Colisiones totales: {colisiones//60}s")
    return colisiones == 0  # Debería ser 0 si el empuje funciona


def test_caida_vacio():
    """Test de caída al vacío."""
    print("\n" + "="*60)
    print("TEST 2: Caída al Vacío")
    print("="*60)
    
    pygame.init()
    pantalla = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Test: Caída al Vacío")
    reloj = pygame.time.Clock()
    
    mario = Mario(400, 100)
    plataformas = []  # Sin plataformas, caída libre
    
    print(f"Mario inicial: Y={mario.rect.y}, Vivo={mario.vivo}")
    print("\nInstrucciones:")
    print("  - Mario debería morir al caer debajo de Y=600")
    print("  - Observa si el estado cambia a MURIENDO")
    print("  - ESC para salir")
    
    ejecutando = True
    frames = 0
    muerte_detectada = False
    
    while ejecutando and frames < 300:  # Máximo 5 segundos
        reloj.tick(60)
        frames += 1
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                ejecutando = False
        
        mario.update(plataformas)
        
        # Verificar muerte
        if mario.rect.y > ALTO:
            if not muerte_detectada:
                print(f"\n✓ Mario pasó Y={ALTO}")
                print(f"   Estado: {mario.estado}")
                print(f"   Vivo: {mario.vivo}")
                muerte_detectada = True
        
        # Dibujar
        pantalla.fill(AZUL_CIELO)
        
        # Línea de muerte
        pygame.draw.line(pantalla, ROJO, (0, ALTO), (800, ALTO), 3)
        
        if mario.rect.y < ALTO + 100:
            mario.dibujar(pantalla)
        
        # Info
        fuente = pygame.font.Font(None, 20)
        info = [
            f"Mario Y: {mario.rect.y:.0f}",
            f"Velocidad Y: {mario.velocidad_y:.1f}",
            f"Estado: {mario.estado.value}",
            f"Vivo: {mario.vivo}",
            f"Frames: {frames}/300"
        ]
        for i, linea in enumerate(info):
            color = ROJO if mario.rect.y > ALTO else NEGRO
            texto = fuente.render(linea, True, color)
            pantalla.blit(texto, (10, 10 + i * 20))
        
        pygame.display.flip()
    
    pygame.quit()
    print(f"\n✓ Test completado.")
    print(f"   Muerte detectada: {muerte_detectada}")
    print(f"   Estado final: {mario.estado}")
    return muerte_detectada


def test_controles():
    """Test de respuesta de controles."""
    print("\n" + "="*60)
    print("TEST 3: Controles")
    print("="*60)
    
    pygame.init()
    pantalla = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Test: Controles")
    reloj = pygame.time.Clock()
    
    mario = Mario(400, 400)
    plataformas = [Plataforma(0, 550, 800, 50, 'suelo')]
    
    print("Instrucciones:")
    print("  - Presiona FLECHAS/A/D para mover")
    print("  - SPACE para saltar")
    print("  - SHIFT para correr")
    print("  - Verifica que Mario responde correctamente")
    print("  - ESC para finalizar test")
    
    ejecutando = True
    movimientos_detectados = {'izq': 0, 'der': 0, 'salto': 0, 'correr': 0}
    
    while ejecutando:
        reloj.tick(60)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                ejecutando = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                mario.saltar()
                movimientos_detectados['salto'] += 1
        
        pos_antes = mario.rect.x
        mario.update(plataformas)
        pos_despues = mario.rect.x
        
        # Detectar movimientos
        if pos_despues < pos_antes:
            movimientos_detectados['izq'] += 1
        elif pos_despues > pos_antes:
            movimientos_detectados['der'] += 1
        
        if mario.corriendo:
            movimientos_detectados['correr'] += 1
        
        # Dibujar
        pantalla.fill(AZUL_CIELO)
        for plat in plataformas:
            plat.dibujar(pantalla)
        mario.dibujar(pantalla)
        
        # Info
        fuente = pygame.font.Font(None, 20)
        info = [
            "TEST DE CONTROLES",
            f"Movimientos izquierda: {movimientos_detectados['izq']}",
            f"Movimientos derecha: {movimientos_detectados['der']}",
            f"Saltos: {movimientos_detectados['salto']}",
            f"Frames corriendo: {movimientos_detectados['correr']}",
            "",
            "Presiona ESC para finalizar"
        ]
        for i, linea in enumerate(info):
            color = VERDE if i == 0 else NEGRO
            texto = fuente.render(linea, True, color)
            pantalla.blit(texto, (10, 10 + i * 20))
        
        pygame.display.flip()
    
    pygame.quit()
    
    print(f"\n✓ Test completado.")
    print(f"   Movimientos izquierda: {movimientos_detectados['izq']}")
    print(f"   Movimientos derecha: {movimientos_detectados['der']}")
    print(f"   Saltos: {movimientos_detectados['salto']}")
    print(f"   Frames corriendo: {movimientos_detectados['correr']}")
    
    tiene_movimiento = any(movimientos_detectados[k] > 0 for k in ['izq', 'der', 'salto'])
    return tiene_movimiento


def main():
    """Ejecuta todos los tests."""
    print("\n" + "="*60)
    print("  SUITE DE TESTS DE BUGS")
    print("  Super Mario Bros 2005")
    print("="*60)
    print("\nSe ejecutarán 3 tests secuenciales:")
    print("  1. Colisión con enemigos")
    print("  2. Caída al vacío")
    print("  3. Respuesta de controles")
    print("\nPresiona ENTER para comenzar...")
    input()
    
    resultados = {}
    
    # Test 1
    try:
        resultados['colision'] = test_colision_enemigo()
    except Exception as e:
        print(f"❌ Error en test de colisión: {e}")
        resultados['colision'] = False
    
    # Test 2
    try:
        resultados['caida'] = test_caida_vacio()
    except Exception as e:
        print(f"❌ Error en test de caída: {e}")
        resultados['caida'] = False
    
    # Test 3
    try:
        resultados['controles'] = test_controles()
    except Exception as e:
        print(f"❌ Error en test de controles: {e}")
        resultados['controles'] = False
    
    # Resumen
    print("\n" + "="*60)
    print("  RESUMEN DE TESTS")
    print("="*60)
    for nombre, resultado in resultados.items():
        estado = "✓ PASS" if resultado else "❌ FAIL"
        print(f"  {nombre.upper()}: {estado}")
    
    total = sum(resultados.values())
    print(f"\nTests aprobados: {total}/{len(resultados)}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
