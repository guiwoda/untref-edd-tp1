import unittest

from Ruta import Ruta
from Trayecto import Trayecto


class TrayectoTest(unittest.TestCase):

    def test_encuentra_una_ciudad(self):
        trayecto = Trayecto()

        ruta = Ruta('Buenos Aires', 'La Plata')
        trayecto.rutas.append(ruta)

        self.assertTrue(trayecto.ciudad_existe('La Plata'))
        self.assertFalse(trayecto.ciudad_existe('Cordoba'))

if __name__ == '__main__':
    unittest.main()