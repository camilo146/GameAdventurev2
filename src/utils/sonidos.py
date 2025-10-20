"""
Sistema de gestión de sonidos para el juego.
"""

import pygame
import os
from typing import Dict, Optional
from src.utils.constantes import SOUNDS_DIR, SONIDOS

class GestorSonidos:
    """
    Sistema centralizado para manejar todos los sonidos del juego.
    
    Attributes:
        sonidos (Dict[str, pygame.mixer.Sound]): Diccionario de sonidos cargados
        musica_actual (str): Nombre de la música actualmente reproduciéndose
        volumen_efectos (float): Volumen de efectos de sonido (0.0 - 1.0)
        volumen_musica (float): Volumen de música (0.0 - 1.0)
        habilitado (bool): Si el sonido está habilitado
    """
    
    def __init__(self):
        self.sonidos: Dict[str, pygame.mixer.Sound] = {}
        self.musica_actual: Optional[str] = None
        self.volumen_efectos = 0.7
        self.volumen_musica = 0.5
        self.habilitado = True
        
        # Inicializar mixer de pygame
        try:
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
            pygame.mixer.init()
            self._cargar_sonidos()
        except pygame.error as e:
            print(f"Error inicializando el sistema de sonido: {e}")
            self.habilitado = False
    
    def _cargar_sonidos(self) -> None:
        """Carga todos los archivos de sonido disponibles."""
        for nombre, archivo in SONIDOS.items():
            ruta_completa = os.path.join(SOUNDS_DIR, archivo)
            try:
                if os.path.exists(ruta_completa):
                    sonido = pygame.mixer.Sound(ruta_completa)
                    sonido.set_volume(self.volumen_efectos)
                    self.sonidos[nombre] = sonido
                else:
                    # Silenciosamente omitir archivos faltantes en lugar de mostrar error
                    pass
            except pygame.error as e:
                # Silenciosamente omitir errores de carga
                pass
    
    def reproducir_efecto(self, nombre: str, loops: int = 0) -> None:
        """
        Reproduce un efecto de sonido.
        
        Args:
            nombre: Nombre del efecto de sonido
            loops: Número de repeticiones (0 = una vez, -1 = infinito)
        """
        if not self.habilitado or nombre not in self.sonidos:
            return
            
        try:
            self.sonidos[nombre].play(loops)
        except pygame.error as e:
            print(f"Error reproduciendo efecto {nombre}: {e}")
    
    def cargar_musica(self, archivo: str) -> bool:
        """
        Carga un archivo de música de fondo.
        
        Args:
            archivo: Nombre del archivo de música
            
        Returns:
            bool: True si se cargó correctamente, False en caso contrario
        """
        if not self.habilitado:
            return False
            
        ruta_completa = os.path.join(SOUNDS_DIR, archivo)
        try:
            if os.path.exists(ruta_completa):
                pygame.mixer.music.load(ruta_completa)
                pygame.mixer.music.set_volume(self.volumen_musica)
                return True
            else:
                # Silenciosamente omitir archivos faltantes
                return False
        except pygame.error as e:
            # Silenciosamente omitir errores de carga
            return False
    
    def reproducir_musica(self, archivo: str, loops: int = -1, fade_in: int = 0) -> None:
        """
        Reproduce música de fondo.
        
        Args:
            archivo: Nombre del archivo de música
            loops: Número de repeticiones (-1 = infinito)
            fade_in: Tiempo de fade in en milisegundos
        """
        if not self.habilitado:
            return
            
        if self.cargar_musica(archivo):
            try:
                if fade_in > 0:
                    pygame.mixer.music.fadeout(fade_in)
                    pygame.mixer.music.play(loops, fade_ms=fade_in)
                else:
                    pygame.mixer.music.play(loops)
                self.musica_actual = archivo
            except pygame.error as e:
                print(f"Error reproduciendo música {archivo}: {e}")
    
    def pausar_musica(self) -> None:
        """Pausa la música de fondo."""
        if self.habilitado:
            pygame.mixer.music.pause()
    
    def reanudar_musica(self) -> None:
        """Reanuda la música de fondo."""
        if self.habilitado:
            pygame.mixer.music.unpause()
    
    def detener_musica(self, fade_out: int = 0) -> None:
        """
        Detiene la música de fondo.
        
        Args:
            fade_out: Tiempo de fade out en milisegundos
        """
        if self.habilitado:
            if fade_out > 0:
                pygame.mixer.music.fadeout(fade_out)
            else:
                pygame.mixer.music.stop()
            self.musica_actual = None
    
    def establecer_volumen_efectos(self, volumen: float) -> None:
        """
        Establece el volumen de los efectos de sonido.
        
        Args:
            volumen: Volumen entre 0.0 y 1.0
        """
        self.volumen_efectos = max(0.0, min(1.0, volumen))
        for sonido in self.sonidos.values():
            sonido.set_volume(self.volumen_efectos)
    
    def establecer_volumen_musica(self, volumen: float) -> None:
        """
        Establece el volumen de la música.
        
        Args:
            volumen: Volumen entre 0.0 y 1.0
        """
        self.volumen_musica = max(0.0, min(1.0, volumen))
        if self.habilitado:
            pygame.mixer.music.set_volume(self.volumen_musica)
    
    def alternar_sonido(self) -> bool:
        """
        Alterna el estado del sonido (habilitado/deshabilitado).
        
        Returns:
            bool: Nuevo estado del sonido
        """
        self.habilitado = not self.habilitado
        if not self.habilitado:
            self.detener_musica()
            pygame.mixer.stop()
        return self.habilitado
    
    def cleanup(self) -> None:
        """Limpia todos los recursos de sonido."""
        if self.habilitado:
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            self.sonidos.clear()

# Instancia global del gestor de sonidos
gestor_sonidos = GestorSonidos()