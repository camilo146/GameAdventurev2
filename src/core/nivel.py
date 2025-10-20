"""
Sistema de gestión de niveles del juego.
"""

import pygame
from typing import List, Optional
from src.entities.plataforma import Plataforma
from src.entities.enemigo import Enemigo
from src.entities.powerup import PowerUp
from src.entities.moneda import Moneda
from src.entities.bandera import Bandera
from src.entities.princesa import Princesa
from src.entities.puerta import Puerta
from src.entities.dragon import Dragon
from src.utils.constantes import TipoPowerUp, TipoEnemigo
from src.utils.preguntas import TipoPuerta, obtener_configuracion_nivel

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
        dragon (Dragon): Jefe final del nivel 5
        completado (bool): Si el nivel ha sido completado
        ancho_mapa (int): Ancho total del mapa
    """
    
    def __init__(self, numero: int):
        self.numero = numero
        self.plataformas: List[Plataforma] = []
        self.enemigos: List[Enemigo] = []
        self.monedas: List[Moneda] = []
        self.powerups: List[PowerUp] = []
        self.puertas: List[Puerta] = []  # Sistema de quiz de inglés
        self.bandera: Bandera = None
        self.princesa: Optional[Princesa] = None
        self.dragon: Optional[Dragon] = None  # Jefe final
        self.completado = False
        self.ancho_mapa = 3200
        self._crear_nivel()

    def _crear_nivel(self) -> None:
        """Crea la estructura del nivel según su número."""
        if self.numero == 1:
            self._crear_nivel_1()
        elif self.numero == 2:
            self._crear_nivel_2()
        elif self.numero == 3:
            self._crear_nivel_3()
        elif self.numero == 4:
            self._crear_nivel_4()
        elif self.numero == 5:
            self._crear_nivel_5()
        else:
            self._crear_nivel_basico()
            
        # Agregar puertas según el nivel
        if self.numero == 1:
            self._agregar_puertas_nivel_1()
        elif self.numero == 2:
            self._agregar_puertas_nivel_2()
        elif self.numero == 3:
            self._agregar_puertas_nivel_3()
        elif self.numero == 4:
            self._agregar_puertas_nivel_4()
        elif self.numero == 5:
            self._agregar_puertas_nivel_5()
    
    def _crear_nivel_1(self) -> None:
        """Crea el primer nivel del juego - Estilo Mario Bros clásico."""
        
        # === SUELO SÓLIDO (sin bloques) ===
        for i in range(0, 480, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # PRIMER HUECO DE CAÍDA LIBRE (480-640)
        
        for i in range(640, 960, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # SEGUNDO HUECO DE CAÍDA LIBRE (960-1120)
        
        for i in range(1120, 1440, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # TERCER HUECO DE CAÍDA LIBRE (1440-1600)
        
        for i in range(1600, 3200, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # === HILERAS DE PLATAFORMAS ELEVADAS CON BLOQUES INTEGRADOS ===
        # Estilo Mario Bros: hileras con ladrillos y bloques de interrogación mezclados
        
        # HILERA 1: Y=350 - Primera sección (con bloques de poderes)
        for i in range(200, 360, 40):
            if i == 240:  # Bloque de interrogación con HONGO
                bloque = Plataforma(i, 350, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.HONGO
                self.plataformas.append(bloque)
            elif i == 280:  # Bloque de interrogación con FLOR
                bloque = Plataforma(i, 350, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
                self.plataformas.append(bloque)
            else:  # Ladrillos normales
                self.plataformas.append(Plataforma(i, 350, 40, 40, 'normal'))
        
        # HILERA 2: Y=400 - Segunda sección más baja
        for i in range(500, 660, 40):
            if i == 580:  # Bloque de interrogación con ESTRELLA
                bloque = Plataforma(i, 400, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 400, 40, 40, 'metal'))
        
        # HILERA 3: Y=320 - Tercera sección elevada
        for i in range(800, 1000, 40):
            if i == 880:  # Bloque con HONGO
                bloque = Plataforma(i, 320, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.HONGO
                self.plataformas.append(bloque)
            elif i == 920:  # Bloque con FLOR
                bloque = Plataforma(i, 320, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 320, 40, 40, 'nube'))
        
        # HILERA 4: Y=380 - Cuarta sección intermedia
        for i in range(1200, 1400, 40):
            if i == 1280:  # Bloque con HONGO
                bloque = Plataforma(i, 380, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.HONGO
                self.plataformas.append(bloque)
            elif i == 1320:  # Bloque con ESTRELLA
                bloque = Plataforma(i, 380, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 380, 40, 40, 'normal'))
        
        # HILERA 5: Y=350 - Quinta sección 
        for i in range(1800, 2000, 40):
            if i == 1880:  # Bloque con FLOR
                bloque = Plataforma(i, 350, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 350, 40, 40, 'metal'))
        
        # HILERA 6: Y=400 - Sexta sección
        for i in range(2100, 2300, 40):
            if i == 2160:  # Bloque con HONGO
                bloque = Plataforma(i, 400, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.HONGO
                self.plataformas.append(bloque)
            elif i == 2200:  # Bloque con ESTRELLA
                bloque = Plataforma(i, 400, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 400, 40, 40, 'normal'))
        
        # HILERA 7: Y=320 - Séptima sección elevada
        for i in range(2400, 2640, 40):
            if i == 2480:  # Bloque con FLOR
                bloque = Plataforma(i, 320, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
                self.plataformas.append(bloque)
            elif i == 2560:  # Bloque con HONGO
                bloque = Plataforma(i, 320, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.HONGO
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 320, 40, 40, 'nube'))
        
        # HILERA 8: Y=380 - Octava sección final antes de la bandera
        for i in range(2800, 3000, 40):
            if i == 2880:  # Bloque con ESTRELLA
                bloque = Plataforma(i, 380, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            elif i == 2920:  # Bloque con FLOR
                bloque = Plataforma(i, 380, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 380, 40, 40, 'metal'))
        
        # Plataformas para cruzar huecos
        self.plataformas.append(Plataforma(520, 480, 80, 20, 'normal'))
        self.plataformas.append(Plataforma(1000, 480, 80, 20, 'metal'))
        self.plataformas.append(Plataforma(1500, 480, 80, 20, 'nube'))
        self.plataformas.append(Plataforma(2050, 480, 80, 20, 'normal'))
        self.plataformas.append(Plataforma(2350, 450, 80, 20, 'metal'))
        self.plataformas.append(Plataforma(2700, 480, 80, 20, 'nube'))
        
        # Tubos distribuidos por el nivel - TODOS ELIMINADOS PARA NO BLOQUEAR PUERTAS
        # self.plataformas.append(Plataforma(280, 470, 60, 80, 'tubo'))  # ELIMINADO - bloqueaba la puerta
        # self.plataformas.append(Plataforma(1700, 470, 60, 80, 'tubo'))  # ELIMINADO - bloqueaba acceso a puerta
        # self.plataformas.append(Plataforma(2300, 470, 60, 80, 'tubo'))  # ELIMINADO
        # self.plataformas.append(Plataforma(2900, 470, 60, 80, 'tubo'))  # ELIMINADO
        
        # Enemigos distribuidos por las áreas seguras
        self.enemigos.append(Enemigo(150, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(300, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(750, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(1250, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(1350, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(1800, 520, TipoEnemigo.KOOPA.value))
        # Enemigos en la segunda mitad del nivel (después de X=1905)
        self.enemigos.append(Enemigo(2000, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(2150, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(2350, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(2500, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(2650, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(2800, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(2950, 520, TipoEnemigo.GOOMBA.value))
        
        # Monedas estratégicamente ubicadas
        # Monedas cerca de las plataformas elevadas (primera mitad)
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
        
        # Monedas adicionales en áreas seguras (primera mitad)
        self.monedas.append(Moneda(100, 480))   # Área inicial
        self.monedas.append(Moneda(800, 480))   # Después del primer hueco
        self.monedas.append(Moneda(1300, 480))  # Después del segundo hueco
        
        # Monedas en la segunda mitad del nivel (después de X=1905)
        for i in range(1850, 1950, 25):
            self.monedas.append(Moneda(i, 280))  # Sobre hilera 5
        for i in range(2120, 2280, 25):
            self.monedas.append(Moneda(i, 330))  # Sobre hilera 6
        for i in range(2420, 2600, 25):
            self.monedas.append(Moneda(i, 250))  # Sobre hilera 7
        for i in range(2820, 2980, 25):
            self.monedas.append(Moneda(i, 310))  # Sobre hilera 8
        
        # Monedas en el suelo (segunda mitad)
        self.monedas.append(Moneda(2000, 480))
        self.monedas.append(Moneda(2200, 480))
        self.monedas.append(Moneda(2400, 480))
        self.monedas.append(Moneda(2600, 480))
        self.monedas.append(Moneda(2800, 480))
        self.monedas.append(Moneda(3000, 480))
        
        # Power-ups que aparecen en el suelo (no desde bloques)
        self.powerups.append(PowerUp(1800, 520, TipoPowerUp.ESTRELLA))  # Estrella en el suelo
        self.powerups.append(PowerUp(2500, 520, TipoPowerUp.HONGO))     # Hongo en el suelo
        
        # Bandera de meta
        self.bandera = Bandera(3100, 350)
        
        # Agregar puertas y barreras del nivel 1
        self._agregar_puertas_nivel_1()
        self._crear_barreras_puertas()
    
    def _crear_nivel_2(self) -> None:
        """Crea el segundo nivel del juego - Estilo Mario Bros (más difícil que nivel 1)."""
        
        # === SUELO SÓLIDO ===
        for i in range(0, 520, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # PRIMER HUECO MÁS GRANDE (520-720)
        
        for i in range(720, 1040, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # SEGUNDO HUECO MÁS GRANDE (1040-1280)
        
        for i in range(1280, 1600, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # TERCER HUECO MÁS GRANDE (1600-1840)
        
        for i in range(1840, 3200, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # === HILERAS DE PLATAFORMAS ELEVADAS CON BLOQUES INTEGRADOS ===
        # Nivel 2 tiene hileras más altas y desafiantes
        
        # HILERA 1: Y=380 - Primera sección baja
        for i in range(180, 340, 40):
            if i == 220:  # Bloque con FLOR
                bloque = Plataforma(i, 380, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
                self.plataformas.append(bloque)
            elif i == 260:  # Bloque con ESTRELLA
                bloque = Plataforma(i, 380, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 380, 40, 40, 'normal'))
        
        # HILERA 2: Y=300 - Segunda sección MÁS ALTA
        for i in range(480, 640, 40):
            if i == 520:  # Bloque con HONGO
                bloque = Plataforma(i, 300, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.HONGO
                self.plataformas.append(bloque)
            elif i == 560:  # Bloque con FLOR
                bloque = Plataforma(i, 300, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 300, 40, 40, 'metal'))
        
        # HILERA 3: Y=350 - Tercera sección intermedia
        for i in range(800, 1000, 40):
            if i == 840:  # Bloque con ESTRELLA
                bloque = Plataforma(i, 350, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            elif i == 880:  # Bloque con HONGO
                bloque = Plataforma(i, 350, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.HONGO
                self.plataformas.append(bloque)
            elif i == 920:  # Bloque con FLOR
                bloque = Plataforma(i, 350, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 350, 40, 40, 'nube'))
        
        # HILERA 4: Y=280 - Cuarta sección MUY ALTA
        for i in range(1100, 1260, 40):
            if i == 1140:  # Bloque con FLOR
                bloque = Plataforma(i, 280, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
                self.plataformas.append(bloque)
            elif i == 1180:  # Bloque con ESTRELLA
                bloque = Plataforma(i, 280, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 280, 40, 40, 'metal'))
        
        # HILERA 5: Y=360 - Quinta sección
        for i in range(1400, 1580, 40):
            if i == 1480:  # Bloque con HONGO
                bloque = Plataforma(i, 360, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.HONGO
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 360, 40, 40, 'normal'))
        
        # HILERA 6: Y=320 - Sexta sección elevada
        for i in range(1900, 2100, 40):
            if i == 1960:  # Bloque con FLOR
                bloque = Plataforma(i, 320, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
                self.plataformas.append(bloque)
            elif i == 2000:  # Bloque con ESTRELLA
                bloque = Plataforma(i, 320, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 320, 40, 40, 'nube'))
        
        # HILERA 7: Y=380 - Séptima sección
        for i in range(2200, 2400, 40):
            if i == 2280:  # Bloque con HONGO
                bloque = Plataforma(i, 380, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.HONGO
                self.plataformas.append(bloque)
            elif i == 2320:  # Bloque con FLOR
                bloque = Plataforma(i, 380, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 380, 40, 40, 'metal'))
        
        # HILERA 8: Y=300 - Octava sección alta final
        for i in range(2600, 2800, 40):
            if i == 2680:  # Bloque con ESTRELLA
                bloque = Plataforma(i, 300, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 300, 40, 40, 'normal'))
        
        # Plataformas para cruzar huecos (más difíciles que nivel 1)
        self.plataformas.append(Plataforma(580, 450, 60, 20, 'normal'))
        self.plataformas.append(Plataforma(1100, 420, 60, 20, 'metal'))
        self.plataformas.append(Plataforma(1680, 460, 60, 20, 'nube'))
        self.plataformas.append(Plataforma(2450, 440, 80, 20, 'metal'))
        
        # Tubos más grandes distribuidos
        self.plataformas.append(Plataforma(400, 430, 60, 120, 'tubo'))
        self.plataformas.append(Plataforma(1350, 410, 60, 140, 'tubo'))
        self.plataformas.append(Plataforma(2100, 390, 60, 160, 'tubo'))
        self.plataformas.append(Plataforma(2900, 430, 60, 120, 'tubo'))
        
        # Enemigos más numerosos (nivel difícil)
        self.enemigos.append(Enemigo(100, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(250, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(400, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(800, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(950, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(1100, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(1400, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(1550, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(1900, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(2050, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(2300, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(2450, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(2700, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(2900, 520, TipoEnemigo.GOOMBA.value))
        
        # Monedas en hileras elevadas
        for i in range(200, 320, 25):
            self.monedas.append(Moneda(i, 310))  # Sobre hilera 1
        for i in range(500, 620, 25):
            self.monedas.append(Moneda(i, 230))  # Sobre hilera 2
        for i in range(820, 980, 25):
            self.monedas.append(Moneda(i, 280))  # Sobre hilera 3
        for i in range(1120, 1240, 25):
            self.monedas.append(Moneda(i, 210))  # Sobre hilera 4
        for i in range(1920, 2080, 25):
            self.monedas.append(Moneda(i, 250))  # Sobre hilera 6
        for i in range(2220, 2380, 25):
            self.monedas.append(Moneda(i, 310))  # Sobre hilera 7
        
        # Monedas en el suelo
        self.monedas.append(Moneda(150, 480))
        self.monedas.append(Moneda(700, 480))
        self.monedas.append(Moneda(1250, 480))
        self.monedas.append(Moneda(1800, 480))
        self.monedas.append(Moneda(2400, 480))
        self.monedas.append(Moneda(2800, 480))
        
        # Power-ups en el suelo
        self.powerups.append(PowerUp(1200, 520, TipoPowerUp.ESTRELLA))
        self.powerups.append(PowerUp(2200, 520, TipoPowerUp.HONGO))
        
        # Bandera de meta
        self.bandera = Bandera(3100, 350)
        
        # Agregar puertas y barreras del nivel 2
        self._agregar_puertas_nivel_2()
        self._crear_barreras_puertas()
    
    def _crear_nivel_3(self) -> None:
        """Crea el tercer nivel del juego - Estilo Mario Bros (MUY difícil)."""
        
        # === SUELO SÓLIDO CON HUECOS MUY GRANDES ===
        for i in range(0, 440, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # HUECO GIGANTE 1 (440-760)
        
        for i in range(760, 1000, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # HUECO GIGANTE 2 (1000-1360)
        
        for i in range(1360, 1600, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # HUECO GIGANTE 3 (1600-2000)
        
        for i in range(2000, 3200, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # === HILERAS DE PLATAFORMAS ELEVADAS CON BLOQUES INTEGRADOS ===
        # Nivel 3: MUY desafiante con plataformas muy altas y patrones complejos
        
        # HILERA 1: Y=420 - Primera sección muy baja (accesible)
        for i in range(160, 360, 40):
            if i == 200:  # Bloque con ESTRELLA
                bloque = Plataforma(i, 420, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            elif i == 280:  # Bloque con FLOR
                bloque = Plataforma(i, 420, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 420, 40, 40, 'metal'))
        
        # HILERA 2: Y=260 - Segunda sección MUY ALTA
        for i in range(440, 640, 40):
            if i == 480:  # Bloque con HONGO
                bloque = Plataforma(i, 260, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.HONGO
                self.plataformas.append(bloque)
            elif i == 520:  # Bloque con FLOR
                bloque = Plataforma(i, 260, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
                self.plataformas.append(bloque)
            elif i == 560:  # Bloque con ESTRELLA
                bloque = Plataforma(i, 260, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 260, 40, 40, 'nube'))
        
        # HILERA 3: Y=380 - Tercera sección intermedia
        for i in range(800, 960, 40):
            if i == 840:  # Bloque con FLOR
                bloque = Plataforma(i, 380, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
                self.plataformas.append(bloque)
            elif i == 880:  # Bloque con HONGO
                bloque = Plataforma(i, 380, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.HONGO
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 380, 40, 40, 'normal'))
        
        # HILERA 4: Y=240 - Cuarta sección EXTREMADAMENTE ALTA
        for i in range(1080, 1280, 40):
            if i == 1120:  # Bloque con ESTRELLA
                bloque = Plataforma(i, 240, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            elif i == 1160:  # Bloque con FLOR
                bloque = Plataforma(i, 240, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
                self.plataformas.append(bloque)
            elif i == 1200:  # Bloque con HONGO
                bloque = Plataforma(i, 240, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.HONGO
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 240, 40, 40, 'metal'))
        
        # HILERA 5: Y=360 - Quinta sección
        for i in range(1400, 1560, 40):
            if i == 1480:  # Bloque con FLOR
                bloque = Plataforma(i, 360, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 360, 40, 40, 'nube'))
        
        # HILERA 6: Y=280 - Sexta sección alta
        for i in range(1720, 1920, 40):
            if i == 1760:  # Bloque con ESTRELLA
                bloque = Plataforma(i, 280, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            elif i == 1800:  # Bloque con HONGO
                bloque = Plataforma(i, 280, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.HONGO
                self.plataformas.append(bloque)
            elif i == 1840:  # Bloque con FLOR
                bloque = Plataforma(i, 280, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 280, 40, 40, 'normal'))
        
        # HILERA 7: Y=340 - Séptima sección
        for i in range(2100, 2300, 40):
            if i == 2160:  # Bloque con HONGO
                bloque = Plataforma(i, 340, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.HONGO
                self.plataformas.append(bloque)
            elif i == 2200:  # Bloque con ESTRELLA
                bloque = Plataforma(i, 340, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 340, 40, 40, 'metal'))
        
        # HILERA 8: Y=260 - Octava sección muy alta
        for i in range(2400, 2600, 40):
            if i == 2480:  # Bloque con FLOR
                bloque = Plataforma(i, 260, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 260, 40, 40, 'nube'))
        
        # HILERA 9: Y=380 - Novena sección intermedia
        for i in range(2700, 2900, 40):
            if i == 2760:  # Bloque con HONGO
                bloque = Plataforma(i, 380, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.HONGO
                self.plataformas.append(bloque)
            elif i == 2800:  # Bloque con ESTRELLA
                bloque = Plataforma(i, 380, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 380, 40, 40, 'metal'))
        
        # Plataformas pequeñas para cruzar huecos gigantes (MUY difíciles)
        self.plataformas.append(Plataforma(520, 420, 50, 20, 'normal'))
        self.plataformas.append(Plataforma(640, 380, 50, 20, 'metal'))
        self.plataformas.append(Plataforma(1120, 400, 50, 20, 'nube'))
        self.plataformas.append(Plataforma(1240, 360, 50, 20, 'normal'))
        self.plataformas.append(Plataforma(1720, 440, 60, 20, 'metal'))
        self.plataformas.append(Plataforma(1880, 420, 60, 20, 'nube'))
        
        # Tubos muy grandes distribuidos
        # self.plataformas.append(Plataforma(350, 350, 60, 200, 'tubo'))  # ELIMINADO: Bloqueaba acceso a puerta
        # self.plataformas.append(Plataforma(900, 390, 60, 160, 'tubo'))  # ELIMINADO: Bloqueaba acceso a puerta (X=900)
        self.plataformas.append(Plataforma(1500, 380, 60, 170, 'tubo'))
        self.plataformas.append(Plataforma(2050, 390, 60, 160, 'tubo'))
        self.plataformas.append(Plataforma(2650, 410, 60, 140, 'tubo'))
        
        # Enemigos MUY numerosos (nivel extremo)
        self.enemigos.append(Enemigo(80, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(180, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(280, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(380, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(800, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(900, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(950, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(1400, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(1500, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(2050, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(2150, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(2250, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(2450, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(2550, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(2750, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(2850, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(2950, 520, TipoEnemigo.KOOPA.value))
        
        # Monedas en hileras elevadas
        for i in range(180, 340, 25):
            self.monedas.append(Moneda(i, 350))  # Sobre hilera 1
        for i in range(460, 620, 25):
            self.monedas.append(Moneda(i, 190))  # Sobre hilera 2
        for i in range(820, 940, 25):
            self.monedas.append(Moneda(i, 310))  # Sobre hilera 3
        for i in range(1100, 1260, 25):
            self.monedas.append(Moneda(i, 170))  # Sobre hilera 4
        for i in range(1420, 1540, 25):
            self.monedas.append(Moneda(i, 290))  # Sobre hilera 5
        for i in range(1740, 1900, 25):
            self.monedas.append(Moneda(i, 210))  # Sobre hilera 6
        for i in range(2120, 2280, 25):
            self.monedas.append(Moneda(i, 270))  # Sobre hilera 7
        for i in range(2420, 2580, 25):
            self.monedas.append(Moneda(i, 190))  # Sobre hilera 8
        for i in range(2720, 2880, 25):
            self.monedas.append(Moneda(i, 310))  # Sobre hilera 9
        
        # Monedas en el suelo
        self.monedas.append(Moneda(100, 480))
        self.monedas.append(Moneda(350, 480))
        self.monedas.append(Moneda(850, 480))
        self.monedas.append(Moneda(1450, 480))
        self.monedas.append(Moneda(2100, 480))
        self.monedas.append(Moneda(2500, 480))
        self.monedas.append(Moneda(2900, 480))
        
        # Power-ups en el suelo
        self.powerups.append(PowerUp(800, 520, TipoPowerUp.ESTRELLA))
        self.powerups.append(PowerUp(1600, 520, TipoPowerUp.HONGO))
        self.powerups.append(PowerUp(2400, 520, TipoPowerUp.FLOR))
        
        # Bandera de meta
        self.bandera = Bandera(3100, 350)
        
        # Agregar puertas y barreras del nivel 3
        self._agregar_puertas_nivel_3()
        self._crear_barreras_puertas()
    
    def _crear_nivel_4(self) -> None:
        """Crea el cuarto nivel del juego - Castillo del mal (penúltimo nivel)."""
        
        # === SUELO SÓLIDO CON LAVA (huecos mortales) ===
        for i in range(0, 400, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # FOSO DE LAVA 1 (400-680)
        
        for i in range(680, 960, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # FOSO DE LAVA 2 (960-1320)
        
        for i in range(1320, 1680, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # FOSO DE LAVA 3 (1680-2080)
        
        for i in range(2080, 3200, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # === HILERAS DE PLATAFORMAS DE CASTILLO ===
        # Ambiente oscuro y peligroso
        
        # HILERA 1: Y=400 - Torres del castillo
        for i in range(140, 340, 40):
            if i == 180:
                bloque = Plataforma(i, 400, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
                self.plataformas.append(bloque)
            elif i == 220:
                bloque = Plataforma(i, 400, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 400, 40, 40, 'castillo'))
        
        # HILERA 2: Y=280 - Plataformas altas
        for i in range(420, 660, 40):
            if i == 460:
                bloque = Plataforma(i, 280, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.HONGO
                self.plataformas.append(bloque)
            elif i == 540:
                bloque = Plataforma(i, 280, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
                self.plataformas.append(bloque)
            elif i == 580:
                bloque = Plataforma(i, 280, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 280, 40, 40, 'castillo'))
        
        # HILERA 3: Y=360 - Pasarelas del castillo
        for i in range(740, 940, 40):
            if i == 800:
                bloque = Plataforma(i, 360, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            elif i == 840:
                bloque = Plataforma(i, 360, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.HONGO
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 360, 40, 40, 'castillo'))
        
        # HILERA 4: Y=240 - Torres más altas
        for i in range(1040, 1280, 40):
            if i == 1120:
                bloque = Plataforma(i, 240, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
                self.plataformas.append(bloque)
            elif i == 1160:
                bloque = Plataforma(i, 240, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 240, 40, 40, 'castillo'))
        
        # HILERA 5: Y=340 - Plataformas intermedias
        for i in range(1380, 1640, 40):
            if i == 1500:
                bloque = Plataforma(i, 340, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.HONGO
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 340, 40, 40, 'castillo'))
        
        # HILERA 6: Y=260 - Torres finales
        for i in range(1800, 2040, 40):
            if i == 1880:
                bloque = Plataforma(i, 260, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            elif i == 1920:
                bloque = Plataforma(i, 260, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 260, 40, 40, 'castillo'))
        
        # HILERA 7: Y=380 - Recta final
        for i in range(2200, 2500, 40):
            if i == 2320:
                bloque = Plataforma(i, 380, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.HONGO
                self.plataformas.append(bloque)
            elif i == 2400:
                bloque = Plataforma(i, 380, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 380, 40, 40, 'castillo'))
        
        # HILERA 8: Y=300 - Antes de la meta
        for i in range(2700, 2900, 40):
            if i == 2760:
                bloque = Plataforma(i, 300, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 300, 40, 40, 'castillo'))
        
        # Plataformas pequeñas sobre fosos de lava
        self.plataformas.append(Plataforma(480, 400, 40, 20, 'metal'))
        self.plataformas.append(Plataforma(560, 360, 40, 20, 'metal'))
        self.plataformas.append(Plataforma(1080, 380, 40, 20, 'metal'))
        self.plataformas.append(Plataforma(1180, 340, 40, 20, 'metal'))
        self.plataformas.append(Plataforma(1800, 420, 50, 20, 'metal'))
        self.plataformas.append(Plataforma(1960, 400, 50, 20, 'metal'))
        
        # MUCHOS enemigos (nivel muy difícil)
        self.enemigos.append(Enemigo(120, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(200, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(280, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(350, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(720, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(800, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(880, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(1350, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(1450, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(1550, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(1620, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(2100, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(2200, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(2300, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(2450, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(2600, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(2750, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(2900, 520, TipoEnemigo.GOOMBA.value))
        
        # Monedas
        for i in range(160, 320, 25):
            self.monedas.append(Moneda(i, 330))
        for i in range(440, 640, 25):
            self.monedas.append(Moneda(i, 210))
        for i in range(760, 920, 25):
            self.monedas.append(Moneda(i, 290))
        for i in range(1060, 1260, 25):
            self.monedas.append(Moneda(i, 170))
        for i in range(1400, 1620, 25):
            self.monedas.append(Moneda(i, 270))
        for i in range(1820, 2020, 25):
            self.monedas.append(Moneda(i, 190))
        for i in range(2220, 2480, 25):
            self.monedas.append(Moneda(i, 310))
        
        # Power-ups en el suelo
        self.powerups.append(PowerUp(700, 520, TipoPowerUp.ESTRELLA))
        self.powerups.append(PowerUp(1400, 520, TipoPowerUp.FLOR))
        self.powerups.append(PowerUp(2300, 520, TipoPowerUp.ESTRELLA))
        
        # Bandera
        self.bandera = Bandera(3100, 350)
        
        # Agregar puertas y barreras del nivel 4
        self._agregar_puertas_nivel_4()
        self._crear_barreras_puertas()
    
    def _crear_nivel_5(self) -> None:
        """Crea el quinto nivel del juego - ¡RESCATE DE LA PRINCESA! (nivel final)."""
        
        # === SUELO DEL CASTILLO FINAL ===
        for i in range(0, 360, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # FOSO FINAL 1 (360-640)
        
        for i in range(640, 1000, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # FOSO FINAL 2 (1000-1400)
        
        for i in range(1400, 1800, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # FOSO FINAL 3 (1800-2240)
        
        for i in range(2240, 3200, 40):
            self.plataformas.append(Plataforma(i, 550, 40, 50, 'suelo'))
        
        # === TORRE DEL CASTILLO DONDE ESTÁ LA PRINCESA ===
        
        # HILERA 1: Y=420 - Entrada del castillo
        for i in range(120, 320, 40):
            if i == 160:
                bloque = Plataforma(i, 420, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            elif i == 240:
                bloque = Plataforma(i, 420, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 420, 40, 40, 'castillo_final'))
        
        # HILERA 2: Y=260 - Torres altas del castillo
        for i in range(400, 620, 40):
            if i == 460:
                bloque = Plataforma(i, 260, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.HONGO
                self.plataformas.append(bloque)
            elif i == 500:
                bloque = Plataforma(i, 260, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            elif i == 540:
                bloque = Plataforma(i, 260, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 260, 40, 40, 'castillo_final'))
        
        # HILERA 3: Y=380 - Escaleras del castillo
        for i in range(700, 960, 40):
            if i == 780:
                bloque = Plataforma(i, 380, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            elif i == 860:
                bloque = Plataforma(i, 380, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.HONGO
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 380, 40, 40, 'castillo_final'))
        
        # HILERA 4: Y=220 - Sala alta del castillo
        for i in range(1060, 1360, 40):
            if i == 1140:
                bloque = Plataforma(i, 220, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
                self.plataformas.append(bloque)
            elif i == 1220:
                bloque = Plataforma(i, 220, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            elif i == 1300:
                bloque = Plataforma(i, 220, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.HONGO
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 220, 40, 40, 'castillo_final'))
        
        # HILERA 5: Y=340 - Camino hacia la torre
        for i in range(1500, 1760, 40):
            if i == 1620:
                bloque = Plataforma(i, 340, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 340, 40, 40, 'castillo_final'))
        
        # HILERA 6: Y=240 - Torre de la princesa (parte baja)
        for i in range(1920, 2200, 40):
            if i == 2000:
                bloque = Plataforma(i, 240, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.FLOR
                self.plataformas.append(bloque)
            elif i == 2080:
                bloque = Plataforma(i, 240, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 240, 40, 40, 'castillo_final'))
        
        # HILERA 7: Y=360 - Plataforma hacia la princesa
        for i in range(2340, 2600, 40):
            if i == 2460:
                bloque = Plataforma(i, 360, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.HONGO
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 360, 40, 40, 'castillo_final'))
        
        # HILERA 8: Y=280 - Torre final (donde está la princesa)
        for i in range(2700, 2940, 40):
            if i == 2780:
                bloque = Plataforma(i, 280, 40, 40, 'bloque')
                bloque.tiene_powerup = True
                bloque.tipo_powerup = TipoPowerUp.ESTRELLA
                self.plataformas.append(bloque)
            else:
                self.plataformas.append(Plataforma(i, 280, 40, 40, 'castillo_final'))
        
        # Plataformas flotantes sobre fosos
        self.plataformas.append(Plataforma(440, 400, 40, 20, 'castillo_final'))
        self.plataformas.append(Plataforma(520, 360, 40, 20, 'castillo_final'))
        self.plataformas.append(Plataforma(1120, 380, 50, 20, 'castillo_final'))
        self.plataformas.append(Plataforma(1260, 340, 50, 20, 'castillo_final'))
        self.plataformas.append(Plataforma(1960, 420, 60, 20, 'castillo_final'))
        self.plataformas.append(Plataforma(2120, 400, 60, 20, 'castillo_final'))
        
        # JEFE FINAL: Enemigos MUY numerosos
        self.enemigos.append(Enemigo(100, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(180, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(250, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(320, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(680, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(760, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(840, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(920, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(1440, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(1520, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(1600, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(1720, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(2280, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(2360, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(2440, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(2520, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(2640, 520, TipoEnemigo.GOOMBA.value))
        self.enemigos.append(Enemigo(2800, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(2900, 520, TipoEnemigo.KOOPA.value))
        self.enemigos.append(Enemigo(2980, 520, TipoEnemigo.GOOMBA.value))
        
        # Monedas finales
        for i in range(140, 300, 25):
            self.monedas.append(Moneda(i, 350))
        for i in range(420, 600, 25):
            self.monedas.append(Moneda(i, 190))
        for i in range(720, 940, 25):
            self.monedas.append(Moneda(i, 310))
        for i in range(1080, 1340, 25):
            self.monedas.append(Moneda(i, 150))
        for i in range(1520, 1740, 25):
            self.monedas.append(Moneda(i, 270))
        for i in range(1940, 2180, 25):
            self.monedas.append(Moneda(i, 170))
        for i in range(2360, 2580, 25):
            self.monedas.append(Moneda(i, 290))
        for i in range(2720, 2920, 25):
            self.monedas.append(Moneda(i, 210))
        
        # Power-ups finales
        self.powerups.append(PowerUp(600, 520, TipoPowerUp.ESTRELLA))
        self.powerups.append(PowerUp(1300, 520, TipoPowerUp.FLOR))
        self.powerups.append(PowerUp(2100, 520, TipoPowerUp.ESTRELLA))
        
        # ¡JEFE FINAL - DRAGÓN BOWSER! (antes de la princesa)
        self.dragon = Dragon(2900, 430)  # Posicionado antes de la princesa
        
        # ¡LA PRINCESA PEACH! (al final del nivel)
        self.princesa = Princesa(3050, 510)
        
        # Bandera (junto a la princesa)
        self.bandera = Bandera(3100, 350)
        
        # Agregar puertas y barreras del nivel 5
        self._agregar_puertas_nivel_5()
        self._crear_barreras_puertas()
    
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
        
        # Agregar puertas y barreras del nivel 5
        self._agregar_puertas_nivel_5()
        self._crear_barreras_puertas()
    
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
        
        # Actualizar princesa
        if self.princesa:
            self.princesa.update()
            
        # Actualizar dragón (jefe final)
        if self.dragon:
            self.dragon.update(1/60)  # Asumiendo 60 FPS
            
        # Actualizar puertas
        for puerta in self.puertas:
            puerta.update()
    
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
        
        # Dibujar dragón (jefe final del nivel 5)
        if self.dragon:
            self.dragon.dibujar(superficie, camara.x)
        
        # Dibujar princesa (nivel 5)
        if self.princesa:
            self.princesa.dibujar(superficie, camara.x)
        
        # Dibujar puertas
        for puerta in self.puertas:
            puerta.dibujar(superficie, camara.x)
    
    # ==================== MÉTODOS PARA PUERTAS DE QUIZ ====================
    
    def _agregar_puertas_nivel_1(self) -> None:
        """Agrega puertas de quiz para el nivel 1 - Introducción a 'going to'."""
        # Puertas a Y=470 (justo sobre el suelo)
        puerta1 = Puerta(460, 470, TipoPuerta.OBLIGATORIA, llaves_requeridas=0)
        self.puertas.append(puerta1)
        
        puerta2 = Puerta(940, 470, TipoPuerta.OBLIGATORIA, llaves_requeridas=0)
        self.puertas.append(puerta2)
        
        puerta3 = Puerta(2800, 470, TipoPuerta.LLAVE_ESPECIAL, llaves_requeridas=0)
        self.puertas.append(puerta3)
        
        puerta4 = Puerta(1800, 270, TipoPuerta.OPCIONAL_SECRETA, llaves_requeridas=0)
        self.puertas.append(puerta4)
        
    def _agregar_puertas_nivel_2(self) -> None:
        """Agrega puertas de quiz para el nivel 2 - 'Going to' intermedio."""
        self.puertas.append(Puerta(800, 470, TipoPuerta.OBLIGATORIA, llaves_requeridas=0))
        self.puertas.append(Puerta(1600, 200, TipoPuerta.OPCIONAL_BONUS, llaves_requeridas=0))
        self.puertas.append(Puerta(2400, 470, TipoPuerta.LLAVE_ESPECIAL, llaves_requeridas=1))
        
    def _agregar_puertas_nivel_3(self) -> None:
        """Agrega puertas de quiz para el nivel 3 - Introducción a 'will'."""
        self.puertas.append(Puerta(400, 470, TipoPuerta.OBLIGATORIA, llaves_requeridas=1))
        self.puertas.append(Puerta(900, 470, TipoPuerta.OBLIGATORIA, llaves_requeridas=1))
        self.puertas.append(Puerta(2500, 470, TipoPuerta.LLAVE_ESPECIAL, llaves_requeridas=2))
        
    def _agregar_puertas_nivel_4(self) -> None:
        """Agrega puertas de quiz para el nivel 4 - 'Will' intermedio en castillo."""
        self.puertas.append(Puerta(320, 470, TipoPuerta.OBLIGATORIA, llaves_requeridas=2))
        self.puertas.append(Puerta(1600, 470, TipoPuerta.OBLIGATORIA, llaves_requeridas=2))
        self.puertas.append(Puerta(1200, 180, TipoPuerta.OPCIONAL_SECRETA, llaves_requeridas=1))
        self.puertas.append(Puerta(2600, 470, TipoPuerta.LLAVE_ESPECIAL, llaves_requeridas=3))
        
    def _agregar_puertas_nivel_5(self) -> None:
        """Agrega puertas de quiz para el nivel 5 - Mixto avanzado antes de la princesa."""
        # Puertas principales con barreras que bloquean el progreso
        # Ajustadas para estar en zonas con suelo sólido
        
        # Puerta 1: En la primera zona sólida (0-360)
        self.puertas.append(Puerta(200, 470, TipoPuerta.OBLIGATORIA, llaves_requeridas=1))
        
        # Puerta 2: En la segunda zona sólida (640-1000)
        self.puertas.append(Puerta(800, 470, TipoPuerta.OBLIGATORIA, llaves_requeridas=2))
        
        # Puerta 3: En la tercera zona sólida (1400-1800)
        self.puertas.append(Puerta(1600, 470, TipoPuerta.OBLIGATORIA, llaves_requeridas=2))
        
        # Puerta 4: En la cuarta zona sólida (2240-3200)
        self.puertas.append(Puerta(2400, 470, TipoPuerta.OBLIGATORIA, llaves_requeridas=3))
        
        # PUERTA FINAL antes del dragón y la princesa
        self.puertas.append(Puerta(2800, 470, TipoPuerta.OBLIGATORIA, llaves_requeridas=4))
        
        # Puerta especial en área elevada (bonus)
        self.puertas.append(Puerta(1600, 200, TipoPuerta.OPCIONAL_BONUS, llaves_requeridas=1))
        
    def _crear_barreras_puertas(self):
        """Crea barreras invisibles que bloquean el paso hasta que se abran las puertas."""
        from src.entities.plataforma import Plataforma
        
        # Crear barreras para TODAS las puertas que bloquean el camino (obligatorias y de llave especial)
        for i, puerta in enumerate(self.puertas):
            if puerta.tipo == TipoPuerta.OBLIGATORIA or puerta.tipo == TipoPuerta.LLAVE_ESPECIAL:
                self._crear_barrera_individual(puerta, i)
                
    def _crear_barrera_individual(self, puerta, puerta_id):
        """Crea una barrera individual para una puerta específica."""
        from src.entities.plataforma import Plataforma
        
        # Determinar el área a bloquear basándose en la posición de la puerta
        barrera_x = puerta.rect.x + 60  # Justo después de la puerta
        barrera_ancho = 120  # Ancho de la barrera
        
        # Crear barrera EXTREMADAMENTE ALTA que cubra toda la pantalla
        for x in range(barrera_x, barrera_x + barrera_ancho, 40):
            for y in range(0, 600, 40):  # Desde la parte superior (Y=0) hasta el suelo (Y=600)
                barrera = Plataforma(x, y, 40, 40, 'barrera')
                barrera.es_barrera_puerta = True
                barrera.puerta_asociada_id = puerta_id
                self.plataformas.append(barrera)
            
    def remover_barrera_puerta(self, puerta_id: int):
        """
        Remueve las barreras asociadas a una puerta específica.
        
        Args:
            puerta_id: ID de la puerta que se abrió
        """
        # Remover todas las plataformas que son barreras de esta puerta
        self.plataformas = [p for p in self.plataformas 
                           if not (hasattr(p, 'es_barrera_puerta') and 
                                  hasattr(p, 'puerta_asociada_id') and
                                  p.puerta_asociada_id == puerta_id)]
    
    def reiniciar(self) -> None:
        """Reinicia el nivel a su estado inicial."""
        self.__init__(self.numero)