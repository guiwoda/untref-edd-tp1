import unittest

from Ruta import Ruta
from Trayecto import Trayecto


class TrayectoTest(unittest.TestCase):

    def setUp(self):
        self.trayecto = Trayecto('Trayecto de prueba', Ruta('Buenos Aires', 'La Plata', '58 km', '1 hr'))
        self.trayecto.rutas.append(Ruta('La Plata', 'Bahia Blanca', '46 km', '4 hr'))

    def test_devuelve_la_ultima_ciudad(self):
        self.assertEqual('Bahia Blanca', self.trayecto.ultima_ciudad())

    def test_encuentra_una_ciudad(self):
        self.assertTrue(self.trayecto.ciudad_existe('La Plata'))
        self.assertFalse(self.trayecto.ciudad_existe('Cordoba'))

    def test_lista_las_ciudades_ordenadas(self):
        self.assertEqual(['Buenos Aires', 'La Plata', 'Bahia Blanca'], self.trayecto.obtener_ciudades())


if __name__ == '__main__':
    unittest.main()
