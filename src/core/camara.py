from src.utils.constantes import ANCHO

class Camara:
    def __init__(self, ancho_mapa):
        self.x = 0
        self.ancho_mapa = ancho_mapa
        
    def actualizar(self, objetivo):
        self.x = objetivo.rect.x - ANCHO // 3
        
        if self.x < 0:
            self.x = 0
        if self.x > self.ancho_mapa - ANCHO:
            self.x = self.ancho_mapa - ANCHO
