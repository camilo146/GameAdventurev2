"""
Sistema de gestión de niveles del juego.
"""

import pygame
from typing import List
from src.entities.plataforma import Plataforma
from src.entities.enemigo import Enemigo
from src.entities.powerup import PowerUp
from src.entities.moneda import Moneda
from src.entities.bandera import Bandera
from src.utils.constantes import TipoPowerUp, TipoEnemigo

class Nivel:
    """
    Clase que gestiona la estructura y contenido de un nivel.
    
    Attributes:
        numero (int): Número del nivel
        plataformas (List[Plataforma]): Lista de plataformas del nivel
        enemigos (List[Enemigo]): Lista de enemigos del nivel
        monedas (List[Moneda]): Lista de monedas del nivel
        powerups (List[PowerUp]): Lista de power-ups del nivel
        bandera (Bandera): Bandera de meta del nivel
        completado (bool): Si el nivel ha sido completado
        ancho_mapa (int): Ancho total del mapa
    """
    
    def __init__(self, numero: int):
        self.numero = numero
        self.plataformas: List[Plataforma] = []
        self.enemigos: List[Enemigo] = []
        self.monedas: List[Moneda] = []
        self.powerups: List[PowerUp] = []
        self.bandera: Bandera = None
        self.completado = False
        self.ancho_mapa = 3200
        self._crear_nivel()

    def _crear_nivel(self) -> None:
        """Crea la estructura del nivel según su número."""
        if self.numero == 1:
            self._crear_nivel_1()
        elif self.numero == 2:
            self._crear_nivel_2()
        else:
            self._crear_nivel_basico()
    
    def _crear_nivel_1(self) -> None:
        """Crea el primer nivel del juego."""
        # Área inicial - suelo sólido más largo
        for i in range(0, 480, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # PRIMER HUECO DE CAÍDA LIBRE (480-640) - Más pequeño y alcanzable
        
        # Plataforma después del primer hueco
        for i in range(640, 960, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # SEGUNDO HUECO DE CAÍDA LIBRE (960-1120) - Más pequeño
        
        # Área intermedia
        for i in range(1120, 1440, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # TERCER HUECO DE CAÍDA LIBRE (1440-1600) - Más pequeño
            
        # Área final extendida
        for i in range(1600, 3200, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # Plataformas elevadas accesibles desde el suelo
        self.plataformas.append(Plataforma(200, 450, 120, 20, 'normal'))
        self.plataformas.append(Plataforma(350, 350, 100, 20, 'nube'))
        
        # Plataformas para cruzar el primer hueco (más cerca del borde)
        self.plataformas.append(Plataforma(420, 480, 80, 20, 'normal'))  # Plataforma de lanzamiento
        self.plataformas.append(Plataforma(540, 450, 80, 20, 'metal'))   # Plataforma intermedia
        
        # Plataformas para cruzar el segundo hueco
        self.plataformas.append(Plataforma(900, 480, 80, 20, 'normal'))  # Plataforma de lanzamiento
        self.plataformas.append(Plataforma(1020, 420, 80, 20, 'nube'))   # Plataforma intermedia
        
        # Plataformas para cruzar el tercer hueco
        self.plataformas.append(Plataforma(1380, 480, 80, 20, 'normal')) # Plataforma de lanzamiento
        self.plataformas.append(Plataforma(1500, 450, 80, 20, 'metal'))  # Plataforma intermedia
        
        # Bloques con power-ups (correctamente posicionados sobre plataformas)
        # Bloque con hongo sobre la primera plataforma elevada (200, 450)
        bloque_hongo = Plataforma(240, 430, 20, 20, 'bloque')  # Justo sobre la plataforma normal
        bloque_hongo.tiene_powerup = True
        bloque_hongo.tipo_powerup = TipoPowerUp.HONGO
        self.plataformas.append(bloque_hongo)
        
        # Bloques decorativos en la misma área
        self.plataformas.append(Plataforma(260, 430, 20, 20, 'bloque'))
        
        # Bloque con flor sobre la segunda plataforma elevada (350, 350)
        bloque_flor = Plataforma(380, 330, 20, 20, 'bloque')  # Justo sobre la plataforma nube
        bloque_flor.tiene_powerup = True
        bloque_flor.tipo_powerup = TipoPowerUp.FLOR
        self.plataformas.append(bloque_flor)
        
        # Bloque con hongo sobre la plataforma de lanzamiento del primer hueco
        bloque_extra = Plataforma(450, 460, 20, 20, 'bloque')  # Sobre plataforma (420, 480)
        bloque_extra.tiene_powerup = True
        bloque_extra.tipo_powerup = TipoPowerUp.HONGO
        self.plataformas.append(bloque_extra)
        
        # Bloque sobre plataforma intermedia del segundo hueco
        bloque_segundo = Plataforma(1050, 400, 20, 20, 'bloque')  # Sobre plataforma nube (1020, 420)
        bloque_segundo.tiene_powerup = True
        bloque_segundo.tipo_powerup = TipoPowerUp.FLOR
        self.plataformas.append(bloque_segundo)
        
        # Bloque final con power-up
        bloque_final = Plataforma(1800, 530, 20, 20, 'bloque')  # Sobre suelo final
        bloque_final.tiene_powerup = True
        bloque_final.tipo_powerup = TipoPowerUp.HONGO
        self.plataformas.append(bloque_final)
        
        # Tubos ajustados a las nuevas posiciones
        self.plataformas.append(Plataforma(700, 470, 60, 80, 'tubo'))
        self.plataformas.append(Plataforma(1700, 470, 60, 80, 'tubo'))
        
        # Enemigos distribuidos por las áreas seguras
        self.enemigos.append(Enemigo(150, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(300, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(750, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(1250, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(1350, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(1800, 520, TipoEnemigo.KOOPA.value))
        
        # Monedas estratégicamente ubicadas
        # Monedas cerca de las plataformas elevadas
        for i in range(220, 300, 25):
            self.monedas.append(Moneda(i, 380))  # Sobre primera plataforma elevada
        for i in range(370, 430, 25):
            self.monedas.append(Moneda(i, 280))  # Sobre segunda plataforma elevada
        
        # Monedas flotantes cerca de los huecos de caída libre (más accesibles)
        self.monedas.append(Moneda(460, 420))   # Cerca del primer hueco
        self.monedas.append(Moneda(560, 380))   # Sobre plataforma intermedia del primer hueco
        
        self.monedas.append(Moneda(940, 420))   # Cerca del segundo hueco
        self.monedas.append(Moneda(1060, 350))  # Sobre plataforma intermedia del segundo hueco
        
        self.monedas.append(Moneda(1420, 420))  # Cerca del tercer hueco
        self.monedas.append(Moneda(1520, 380))  # Sobre plataforma intermedia del tercer hueco
        
        # Monedas adicionales en áreas seguras
        self.monedas.append(Moneda(100, 480))   # Área inicial
        self.monedas.append(Moneda(800, 480))   # Después del primer hueco
        self.monedas.append(Moneda(1300, 480))  # Después del segundo hueco
        self.monedas.append(Moneda(2000, 480))  # Área final
        
        # Power-ups que aparecen en el suelo (no desde bloques)
        self.powerups.append(PowerUp(1800, 520, TipoPowerUp.ESTRELLA))  # Estrella en el suelo
        
        # Bandera de meta
        self.bandera = Bandera(3100, 350)
    
    def _crear_nivel_2(self) -> None:
        """Crea el segundo nivel del juego (más difícil)."""
        # Suelo con puentes para atravesar huecos
        for i in range(0, 600, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # Puente de plataformas
        for i in range(600, 800, 40):
            self.plataformas.append(Plataforma(i, 500, 40, 20, 'normal'))
        
        for i in range(800, 1200, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # Sección de plataformas flotantes como puente
        for i in range(1200, 1600, 80):
            self.plataformas.append(Plataforma(i, 450, 60, 20, 'normal'))
            
        for i in range(1600, 2400, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # Puente final
        for i in range(2400, 2800, 60):
            self.plataformas.append(Plataforma(i, 480, 60, 20, 'normal'))
            
        for i in range(2800, 3200, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # Plataformas flotantes
        self.plataformas.append(Plataforma(650, 450, 100, 20, 'normal'))
        self.plataformas.append(Plataforma(1300, 400, 80, 20, 'normal'))
        self.plataformas.append(Plataforma(1450, 300, 80, 20, 'normal'))
        self.plataformas.append(Plataforma(1300, 200, 80, 20, 'normal'))
        self.plataformas.append(Plataforma(2500, 350, 120, 20, 'normal'))
        
        # Más bloques
        for i in range(1320, 1380, 20):
            bloque = Plataforma(i, 370, 20, 20, 'bloque')
            if i == 1340:  # Bloque con hongo
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.HONGO
            elif i == 1360:  # Bloque con flor
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
            self.plataformas.append(bloque)
        
        # Tubos más grandes
        self.plataformas.append(Plataforma(700, 390, 60, 160, 'tubo'))
        self.plataformas.append(Plataforma(2600, 350, 60, 200, 'tubo'))
        
        # Más enemigos
        self.enemigos.append(Enemigo(150, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(300, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(500, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(680, 420, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(900, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(1050, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(1350, 370, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(1700, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(1850, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(2000, 520, TipoEnemigo.KOOPA.value))
        
        # Monedas en lugares más difíciles
        self.monedas.append(Moneda(675, 400))
        for i in range(1320, 1380, 20):
            self.monedas.append(Moneda(i, 340))
        self.monedas.append(Moneda(1350, 150))
        for i in range(2520, 2600, 20):
            self.monedas.append(Moneda(i, 300))
        
        # Power-ups que aparecen en el suelo
        self.powerups.append(PowerUp(2100, 520, TipoPowerUp.ESTRELLA))  # Estrella en el suelo
        
        # Bandera
        self.bandera = Bandera(3100, 350)
    
    def _crear_nivel_basico(self) -> None:
        """Crea un nivel básico genérico."""
        # Suelo simple
        for i in range(0, 3200, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # Algunas plataformas
        self.plataformas.append(Plataforma(400, 450, 100, 20, 'normal'))
        self.plataformas.append(Plataforma(800, 350, 80, 20, 'normal'))
        
        # Algunos enemigos
        self.enemigos.append(Enemigo(300, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(600, 520, TipoEnemigo.KOOPA.value))
        
        # Algunas monedas
        self.monedas.append(Moneda(450, 400))
        self.monedas.append(Moneda(850, 300))
        
        # Power-up básico en el suelo
        self.powerups.append(PowerUp(1000, 520, TipoPowerUp.HONGO))
        
        # Bandera
        self.bandera = Bandera(3000, 350)
    
    def update(self) -> None:
        """Actualiza todos los elementos del nivel."""
        # Actualizar enemigos
        for enemigo in self.enemigos[:]:
            enemigo.update(self.plataformas)
            if not enemigo.vivo:
                self.enemigos.remove(enemigo)
        
        # Actualizar monedas
        for moneda in self.monedas:
            moneda.update()
        
        # Actualizar power-ups
        for powerup in self.powerups[:]:
            powerup.update(self.plataformas)
        
        # Actualizar bandera
        if self.bandera:
            self.bandera.update()
    
    def dibujar(self, superficie: pygame.Surface, camara) -> None:
        """
        Dibuja todos los elementos del nivel.
        
        Args:
            superficie: Superficie donde dibujar
            camara: Cámara para aplicar offset
        """
        # Dibujar plataformas
        for plataforma in self.plataformas:
            rect_camara = camara.aplicar_rect(plataforma.rect)
            if rect_camara.right > 0 and rect_camara.left < superficie.get_width():
                plataforma_temp = Plataforma(rect_camara.x, rect_camara.y, 
                                           rect_camara.width, rect_camara.height, 
                                           plataforma.tipo)
                plataforma_temp.golpeado = plataforma.golpeado
                plataforma_temp.dibujar(superficie)
        
        # Dibujar enemigos
        for enemigo in self.enemigos:
            rect_camara = camara.aplicar_rect(enemigo.rect)
            if rect_camara.right > 0 and rect_camara.left < superficie.get_width():
                # Crear una copia temporal para dibujar en la posición de cámara
                enemigo_temp = type(enemigo)(rect_camara.x, rect_camara.y, enemigo.tipo)
                enemigo_temp.rect = rect_camara
                enemigo_temp.vivo = enemigo.vivo
                enemigo_temp.aplastado = enemigo.aplastado
                enemigo_temp.animacion_frame = enemigo.animacion_frame
                enemigo_temp.particulas = enemigo.particulas
                enemigo_temp.dibujar(superficie)
        
        # Dibujar monedas
        for moneda in self.monedas:
            rect_camara = camara.aplicar_rect(moneda.rect)
            if rect_camara.right > 0 and rect_camara.left < superficie.get_width():
                moneda_temp = Moneda(rect_camara.x, rect_camara.y)
                moneda_temp.animacion_frame = moneda.animacion_frame
                moneda_temp.dibujar(superficie)
        
        # Dibujar power-ups
        for powerup in self.powerups:
            rect_camara = camara.aplicar_rect(powerup.rect)
            if rect_camara.right > 0 and rect_camara.left < superficie.get_width():
                powerup_temp = PowerUp(rect_camara.x, rect_camara.y, powerup.tipo)
                powerup_temp.activo = powerup.activo
                powerup_temp.animacion_frame = powerup.animacion_frame
                powerup_temp.tiempo_aparicion = powerup.tiempo_aparicion
                powerup_temp.particulas = powerup.particulas
                powerup_temp.dibujar(superficie)
        
        # Dibujar bandera
        if self.bandera:
            rect_camara = camara.aplicar_rect(self.bandera.rect)
            if rect_camara.right > 0 and rect_camara.left < superficie.get_width():
                bandera_temp = Bandera(rect_camara.x, rect_camara.y)
                bandera_temp.animacion_frame = self.bandera.animacion_frame
                bandera_temp.dibujar(superficie)
    
    def reiniciar(self) -> None:
        """Reinicia el nivel a su estado inicial."""
        self.__init__(self.numero)