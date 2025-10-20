"""
Script de prueba para verificar que los controles funcionan.
"""

import pygame
import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.entities.mario import Mario
from src.utils.constantes import *

pygame.init()
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Test de Controles")
reloj = pygame.time.Clock()

mario = Mario(400, 300)
plataformas = []

print("=== TEST DE CONTROLES ===")
print("Mario creado:")
print(f"  - Vivo: {mario.vivo}")
print(f"  - Estado: {mario.estado}")
print(f"  - Posición: ({mario.rect.x}, {mario.rect.y})")
print("\nControles:")
print("  - Flechas o A/D: Mover")
print("  - ESPACIO: Saltar")
print("  - SHIFT: Correr")
print("  - ESC: Salir")
print("\nPresiona las teclas para probar...")

ejecutando = True
frame_count = 0

while ejecutando:
    reloj.tick(60)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                ejecutando = False
            elif evento.key == pygame.K_SPACE:
                print("ESPACIO presionado - Intentando saltar")
                mario.saltar()
    
    # Actualizar Mario
    mario.update(plataformas)
    
    # Mostrar info cada 60 frames (1 segundo)
    frame_count += 1
    if frame_count >= 60:
        teclas = pygame.key.get_pressed()
        teclas_presionadas = []
        if teclas[pygame.K_LEFT]: teclas_presionadas.append("LEFT")
        if teclas[pygame.K_RIGHT]: teclas_presionadas.append("RIGHT")
        if teclas[pygame.K_a]: teclas_presionadas.append("A")
        if teclas[pygame.K_d]: teclas_presionadas.append("D")
        if teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT]: teclas_presionadas.append("SHIFT")
        
        if teclas_presionadas:
            print(f"Teclas: {', '.join(teclas_presionadas)} | Pos: ({mario.rect.x:.0f}, {mario.rect.y:.0f}) | Vel: ({mario.velocidad_x:.1f}, {mario.velocidad_y:.1f})")
        frame_count = 0
    
    # Dibujar
    pantalla.fill(AZUL_CIELO)
    mario.dibujar(pantalla)
    
    # Mostrar posición en pantalla
    fuente = pygame.font.Font(None, 24)
    texto = fuente.render(f"Pos: ({mario.rect.x:.0f}, {mario.rect.y:.0f}) | Vel: ({mario.velocidad_x:.1f}, {mario.velocidad_y:.1f})", True, NEGRO)
    pantalla.blit(texto, (10, 10))
    
    pygame.display.flip()

pygame.quit()
print("\nTest finalizado.")
