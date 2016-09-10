import unittest

from MotorDeRutas import MotorDeRutas
from RutaException import RutaException
from Trayecto import Trayecto


class MotorDeRutasTest(unittest.TestCase):

    def setUp(self):
        self.motor = MotorDeRutas()

    def test_crea_trayectos_nuevos(self):
        trayecto = self.motor.crear_trayecto('Ushuaia, Argentina', 'La Quiaca, Argentina', 'De Ushuaia a La Quiaca')

        self.assertIsInstance(trayecto, Trayecto)

    def test_falla_cuando_el_trayecto_no_existe(self):
        with self.assertRaises(RutaException):
            self.motor.crear_trayecto('Buenos Aires, Argentina', 'Reykjavik, Islandia', 'islandia')

    def test_muestra_trayectos(self):
        self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'bs_as_la_plata')

        self.assertEqual('''bs_as_la_plata: Buenos Aires, La Plata
distancia: 58158
tiempo estimado de viaje: 3366''',
            self.motor.mostrar('bs_as_la_plata')
        )

if __name__ == '__main__':
    unittest.main()
