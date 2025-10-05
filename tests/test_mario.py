"""
Tests unitarios para el juego Mario.
"""

import unittest
import pygame
import sys
import os

# Agregar el directorio padre al path para importar modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.entities.mario import Mario
from src.entities.plataforma import Plataforma
from src.utils.constantes import EstadoMario, TipoPowerUp
from src.utils.particulas import SistemaParticulas, Particula

class TestMario(unittest.TestCase):
    """Tests para la clase Mario."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        pygame.init()
        self.mario = Mario(100, 100)
    
    def tearDown(self):
        """Limpieza después de cada test."""
        pygame.quit()
    
    def test_inicializacion_mario(self):
        """Prueba que Mario se inicialice correctamente."""
        self.assertEqual(self.mario.rect.x, 100)
        self.assertEqual(self.mario.rect.y, 100)
        self.assertEqual(self.mario.estado, EstadoMario.PEQUENO)
        self.assertTrue(self.mario.vivo)
        self.assertFalse(self.mario.saltando)
        self.assertEqual(self.mario.direccion, 'derecha')
    
    def test_salto_mario(self):
        """Prueba que Mario pueda saltar correctamente."""
        self.mario.saltar()
        self.assertTrue(self.mario.saltando)
        self.assertLess(self.mario.velocidad_y, 0)
    
    def test_powerup_hongo(self):
        """Prueba que el power-up de hongo funcione correctamente."""
        estado_inicial = self.mario.estado
        self.mario.obtener_powerup(TipoPowerUp.HONGO)
        
        if estado_inicial == EstadoMario.PEQUENO:
            self.assertEqual(self.mario.estado, EstadoMario.GRANDE)
    
    def test_powerup_flor(self):
        """Prueba que el power-up de flor funcione correctamente."""
        self.mario.obtener_powerup(TipoPowerUp.FLOR)
        self.assertEqual(self.mario.estado, EstadoMario.FUEGO)
    
    def test_dano_mario_pequeno(self):
        """Prueba que Mario pequeño muera al recibir daño."""
        self.mario.estado = EstadoMario.PEQUENO
        resultado = self.mario.recibir_dano()
        self.assertTrue(resultado)  # Debe morir
        self.assertEqual(self.mario.estado, EstadoMario.MURIENDO)
    
    def test_dano_mario_grande(self):
        """Prueba que Mario grande se vuelva pequeño al recibir daño."""
        self.mario.estado = EstadoMario.GRANDE
        resultado = self.mario.recibir_dano()
        self.assertFalse(resultado)  # No debe morir
        self.assertEqual(self.mario.estado, EstadoMario.PEQUENO)
    
    def test_invencibilidad(self):
        """Prueba que la invencibilidad funcione correctamente."""
        self.mario.invencible = 60
        resultado = self.mario.recibir_dano()
        self.assertFalse(resultado)  # No debe recibir daño
        self.assertTrue(self.mario.es_invencible())

class TestPlataforma(unittest.TestCase):
    """Tests para la clase Plataforma."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        pygame.init()
        self.plataforma = Plataforma(0, 100, 100, 20, 'normal')
    
    def tearDown(self):
        """Limpieza después de cada test."""
        pygame.quit()
    
    def test_inicializacion_plataforma(self):
        """Prueba que la plataforma se inicialice correctamente."""
        self.assertEqual(self.plataforma.rect.x, 0)
        self.assertEqual(self.plataforma.rect.y, 100)
        self.assertEqual(self.plataforma.rect.width, 100)
        self.assertEqual(self.plataforma.rect.height, 20)
        self.assertEqual(self.plataforma.tipo, 'normal')
        self.assertFalse(self.plataforma.golpeado)

class TestSistemaParticulas(unittest.TestCase):
    """Tests para el sistema de partículas."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        pygame.init()
        self.sistema = SistemaParticulas()
    
    def tearDown(self):
        """Limpieza después de cada test."""
        pygame.quit()
    
    def test_crear_efecto(self):
        """Prueba que se puedan crear efectos de partículas."""
        cantidad_inicial = self.sistema.cantidad_particulas()
        self.sistema.crear_efecto(100, 100, 'salto')
        cantidad_final = self.sistema.cantidad_particulas()
        self.assertGreater(cantidad_final, cantidad_inicial)
    
    def test_crear_explosion(self):
        """Prueba que se puedan crear explosiones."""
        cantidad_inicial = self.sistema.cantidad_particulas()
        self.sistema.crear_explosion(100, 100, (255, 0, 0), 10)
        cantidad_final = self.sistema.cantidad_particulas()
        self.assertEqual(cantidad_final - cantidad_inicial, 10)
    
    def test_limpiar_particulas(self):
        """Prueba que se puedan limpiar todas las partículas."""
        self.sistema.crear_efecto(100, 100, 'salto')
        self.assertGreater(self.sistema.cantidad_particulas(), 0)
        self.sistema.limpiar()
        self.assertEqual(self.sistema.cantidad_particulas(), 0)

class TestParticula(unittest.TestCase):
    """Tests para partículas individuales."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        pygame.init()
        self.particula = Particula(100, 100, 2, -3, (255, 0, 0), 60, 3)
    
    def tearDown(self):
        """Limpieza después de cada test."""
        pygame.quit()
    
    def test_inicializacion_particula(self):
        """Prueba que la partícula se inicialice correctamente."""
        self.assertEqual(self.particula.x, 100)
        self.assertEqual(self.particula.y, 100)
        self.assertEqual(self.particula.velocidad_x, 2)
        self.assertEqual(self.particula.velocidad_y, -3)
        self.assertEqual(self.particula.vida, 60)
        self.assertEqual(self.particula.tamaño, 3)
    
    def test_update_particula(self):
        """Prueba que la partícula se actualice correctamente."""
        x_inicial = self.particula.x
        y_inicial = self.particula.y
        vida_inicial = self.particula.vida
        
        resultado = self.particula.update()
        
        self.assertTrue(resultado)  # Debe seguir viva
        self.assertNotEqual(self.particula.x, x_inicial)
        self.assertNotEqual(self.particula.y, y_inicial)
        self.assertEqual(self.particula.vida, vida_inicial - 1)
    
    def test_muerte_particula(self):
        """Prueba que la partícula muera cuando se acabe su vida."""
        self.particula.vida = 1
        resultado = self.particula.update()
        self.assertFalse(resultado)  # Debe estar muerta

class TestIntegracion(unittest.TestCase):
    """Tests de integración entre componentes."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        pygame.init()
        self.mario = Mario(100, 400)
        self.plataforma = Plataforma(50, 450, 200, 20, 'normal')
    
    def tearDown(self):
        """Limpieza después de cada test."""
        pygame.quit()
    
    def test_colision_mario_plataforma(self):
        """Prueba que Mario colisione correctamente con plataformas."""
        # Simular caída de Mario
        self.mario.velocidad_y = 5
        self.mario.saltando = True
        
        # Actualizar con la plataforma
        self.mario.update([self.plataforma])
        
        # Mario debería estar sobre la plataforma
        self.assertEqual(self.mario.rect.bottom, self.plataforma.rect.top)
        self.assertFalse(self.mario.saltando)
        self.assertEqual(self.mario.velocidad_y, 0)

if __name__ == '__main__':
    # Configurar el entorno de pruebas
    suite = unittest.TestSuite()
    
    # Agregar todos los tests
    suite.addTest(unittest.makeSuite(TestMario))
    suite.addTest(unittest.makeSuite(TestPlataforma))
    suite.addTest(unittest.makeSuite(TestSistemaParticulas))
    suite.addTest(unittest.makeSuite(TestParticula))
    suite.addTest(unittest.makeSuite(TestIntegracion))
    
    # Ejecutar los tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Mostrar resumen
    print(f"\nTests ejecutados: {result.testsRun}")
    print(f"Fallos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    
    if result.failures:
        print("\nFallos:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nErrores:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    # Código de salida
    exit_code = 0 if result.wasSuccessful() else 1
    sys.exit(exit_code)