"""
Script de debug más detallado para verificar el update de Mario.
"""

import pygame
import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.entities.mario import Mario
from src.entities.plataforma import Plataforma
from src.utils.constantes import *

pygame.init()
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Debug Mario Update")
reloj = pygame.time.Clock()

mario = Mario(100, 400)

# Crear una plataforma de suelo
plataformas = [Plataforma(0, 550, 800, 50, 'suelo')]

print("=== DEBUG MARIO UPDATE ===")
print(f"Mario inicial - Vivo: {mario.vivo}, Estado: {mario.estado}")
print(f"Posición: ({mario.rect.x}, {mario.rect.y})")
print("\nControles: Flechas o A/D para mover")

ejecutando = True
frame = 0

while ejecutando:
    reloj.tick(60)
    frame += 1
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                ejecutando = False
            elif evento.key == pygame.K_SPACE:
                mario.saltar()
    
    # Antes del update
    pos_antes = (mario.rect.x, mario.rect.y)
    vel_antes = (mario.velocidad_x, mario.velocidad_y)
    
    # Actualizar Mario
    mario.update(plataformas)
    
    # Después del update
    pos_despues = (mario.rect.x, mario.rect.y)
    vel_despues = (mario.velocidad_x, mario.velocidad_y)
    
    # Mostrar cada 60 frames si hubo cambios
    if frame % 60 == 0 or pos_antes != pos_despues or vel_antes != vel_despues:
        teclas = pygame.key.get_pressed()
        print(f"\nFrame {frame}:")
        print(f"  Teclas: LEFT={teclas[pygame.K_LEFT]}, RIGHT={teclas[pygame.K_RIGHT]}, A={teclas[pygame.K_a]}, D={teclas[pygame.K_d]}")
        print(f"  Vivo: {mario.vivo}, Estado: {mario.estado}")
        print(f"  Pos antes: {pos_antes} -> después: {pos_despues}")
        print(f"  Vel antes: {vel_antes} -> después: {vel_despues}")
        print(f"  Saltando: {mario.saltando}")
    
    # Dibujar
    pantalla.fill(AZUL_CIELO)
    
    # Dibujar plataformas
    for plat in plataformas:
        plat.dibujar(pantalla)
    
    # Dibujar Mario
    mario.dibujar(pantalla)
    
    # Info en pantalla
    fuente = pygame.font.Font(None, 20)
    info = [
        f"Pos: ({mario.rect.x:.0f}, {mario.rect.y:.0f})",
        f"Vel: ({mario.velocidad_x:.1f}, {mario.velocidad_y:.1f})",
        f"Vivo: {mario.vivo}, Estado: {mario.estado.value}",
        f"Saltando: {mario.saltando}"
    ]
    
    for i, linea in enumerate(info):
        texto = fuente.render(linea, True, NEGRO)
        pantalla.blit(texto, (10, 10 + i * 20))
    
    pygame.display.flip()

pygame.quit()
print("\nDebug finalizado.")
