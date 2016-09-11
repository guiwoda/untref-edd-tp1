import unittest

from MotorDeRutas import MotorDeRutas
from RutaException import RutaException
from TrayectoException import TrayectoException
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

    def test_agrega_ciudad_a_trayecto(self):
        trayecto = self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'bs_as_la_plata')
        self.motor.agregar_ciudad(trayecto, 'Quilmes')

        print('test_agrega_ciudad_a_trayecto ')
        for ruta in trayecto.rutas:
            print ('Ruta => Origen: ', ruta.origen, 'Destino: ', ruta.destino)
        #Lo hice re cabeza
        self.assertTrue(True if trayecto.nombre in self.motor.trayectos else False)

    def test_falla_cuando_la_ciudad_no_existe_en_trayecto(self):
        with self.assertRaises(TrayectoException):
            trayecto = self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'bs_as_la_plata')
            self.motor.agregar_parada(trayecto, 'Tandil', 'Quilmes')

    def test_agrega_parada_a_trayecto(self):
        trayecto = self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'bs_as_la_plata')
        self.motor.agregar_ciudad(trayecto, 'Tandil')
        self.motor.agregar_parada(trayecto, 'La Plata', 'Quilmes')

    def test_concatena_trayectos(self):
        trayectoInicial = self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'trayecto_inicial')
        trayectoFinal = self.motor.crear_trayecto('Quilmes', 'Tandil', 'trayecto_final')
        self.motor.concatenar(trayectoInicial, trayectoFinal)

        print('test_concatena_trayectos ')
        for ruta in trayectoInicial.rutas:
            print ('Ruta => Origen: ', ruta.origen, 'Destino: ', ruta.destino)

        self.assertTrue(len(trayectoInicial.rutas) == 3)

    '''
    def test_muestra_trayectos(self):
        self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'bs_as_la_plata')

        self.assertEqual(bs_as_la_plata: Buenos Aires, La Plata
distancia: 58158
tiempo estimado de viaje: 3366,
            self.motor.mostrar('bs_as_la_plata')
        )
    '''
if __name__ == '__main__':
    unittest.main()
