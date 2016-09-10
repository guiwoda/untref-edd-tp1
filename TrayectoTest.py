import unittest

from Ruta import Ruta
from Trayecto import Trayecto


class TrayectoTest(unittest.TestCase):

    def setUp(self):
        self.trayecto = Trayecto()

        self.trayecto.rutas.append(Ruta('Buenos Aires', 'La Plata'))
        self.trayecto.rutas.append(Ruta('La Plata', 'Bahia Blanca'))

    def test_devuelve_la_ultima_ciudad(self):
        self.assertEqual('Bahia Blanca', self.trayecto.ultima_ciudad())

    def test_encuentra_una_ciudad(self):
        self.assertTrue(self.trayecto.ciudad_existe('La Plata'))
        self.assertFalse(self.trayecto.ciudad_existe('Cordoba'))

if __name__ == '__main__':
    unittest.main()
