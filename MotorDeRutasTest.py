import unittest
import vcr

from MotorDeRutas import MotorDeRutas
from Ruta import Ruta
from RutaException import RutaException
from TrayectoException import TrayectoException
from Trayecto import Trayecto


class MotorDeRutasTest(unittest.TestCase):

    def setUp(self):
        self.motor = MotorDeRutas()

    def test_crea_trayectos_nuevos(self):
        with vcr.use_cassette('fixtures/ushuaia_la_quiaca.yaml'):
            trayecto = self.motor.crear_trayecto('Ushuaia, Argentina', 'La Quiaca, Argentina', 'De Ushuaia a La Quiaca')

            self.assertIsInstance(trayecto, Trayecto)

    def test_falla_cuando_el_trayecto_no_existe(self):
        with vcr.use_cassette('fixtures/bs_as_reykjavik.yaml'):
            with self.assertRaises(RutaException):
                self.motor.crear_trayecto('Buenos Aires, Argentina', 'Reykjavik, Islandia', 'islandia')

    def test_agrega_ciudad_a_trayecto(self):
        with vcr.use_cassette('fixtures/bs_as_la_plata.yaml'):
            trayecto = self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'bs_as_la_plata')
            self.motor.agregar_ciudad(trayecto.nombre, 'Quilmes')

            self.assertTrue(trayecto.nombre in self.motor.trayectos)

    def test_falla_cuando_la_ciudad_no_existe_en_trayecto(self):
        with vcr.use_cassette('fixtures/bs_as_la_plata.yaml'):
            trayecto = self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'bs_as_la_plata')

            with self.assertRaises(TrayectoException):
                self.motor.agregar_parada(trayecto.nombre, 'Tandil', 'Quilmes')

    def test_agrega_parada_a_trayecto(self):
        with vcr.use_cassette('fixtures/bs_as_la_plata_quilmes.yaml'):
            trayecto = self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'bs_as_la_plata')
            self.motor.agregar_ciudad(trayecto.nombre, 'Tandil')
            self.motor.agregar_parada(trayecto.nombre, 'La Plata', 'Quilmes')

            self.assertEqual(['Buenos Aires', 'Quilmes', 'La Plata', 'Tandil'], trayecto.obtener_ciudades())
    def test_concatena_trayectos(self):
        with vcr.use_cassette('fixtures/bs_as_la_plata_quilmes_tandil.yaml'):
            trayectoInicial = self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'trayecto_inicial')
            trayectoFinal = self.motor.crear_trayecto('Quilmes', 'Tandil', 'trayecto_final')
            self.motor.concatenar(trayectoInicial.nombre, trayectoFinal.nombre)

            self.assertEqual(['Buenos Aires', 'La Plata', 'Quilmes', 'Tandil'], trayectoInicial.obtener_ciudades())

    def test_obtiene_trayectos_por_nombre(self):
        with vcr.use_cassette('fixtures/bs_as_la_plata.yaml'):
            trayecto = self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'bs_as_la_plata')

            self.assertEqual(trayecto, self.motor.obtener_trayecto(trayecto.nombre))

    def test_obtiene_rutas_entre_dos_ciudades(self):
        with vcr.use_cassette('fixtures/bs_as_la_plata.yaml'):
            ruta = self.motor.obtener_ruta('Buenos Aires', 'La Plata')

            self.assertIsInstance(ruta, Ruta)
    def test_falla_al_obtener_rutas_entre_dos_ciudades_desconectadas(self):
        with vcr.use_cassette('fixtures/bs_as_reykjavik.yaml'):
            with self.assertRaises(RutaException):
                self.motor.obtener_ruta('Buenos Aires, Argentina', 'Reykjavik, Islandia')

    def test_muestra_trayectos(self):
        with vcr.use_cassette('fixtures/bs_as_la_plata.yaml'):
            self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'bs_as_la_plata')

            self.assertEqual(
'''bs_as_la_plata: Buenos Aires, La Plata
distancia: 58158
tiempo estimado de viaje: 3366''',
                self.motor.mostrar('bs_as_la_plata'))

    def test_compara_trayectos_por_distancia(self):
        with vcr.use_cassette('fixtures/bs_as_la_plata_quilmes_tandil.yaml'):
            buenos_aires_la_plata = self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'buenos_aires_la_plata')
            quilmes_tandil        = self.motor.crear_trayecto('Quilmes',      'Tandil',   'quilmes_tandil')

            self.assertEqual(0,  self.motor.comparar(buenos_aires_la_plata.nombre, buenos_aires_la_plata.nombre, 'd'))
            self.assertEqual(-1, self.motor.comparar(buenos_aires_la_plata.nombre, quilmes_tandil.nombre, 'd'))
            self.assertEqual(1,  self.motor.comparar(quilmes_tandil.nombre,        buenos_aires_la_plata.nombre, 'd'))

    def test_compara_trayectos_por_tiempo(self):
        with vcr.use_cassette('fixtures/bs_as_la_plata_quilmes_tandil.yaml'):
            buenos_aires_la_plata = self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'buenos_aires_la_plata')
            quilmes_tandil        = self.motor.crear_trayecto('Quilmes',      'Tandil',   'quilmes_tandil')

            self.assertEqual(0,  self.motor.comparar(buenos_aires_la_plata.nombre, buenos_aires_la_plata.nombre, 't'))
            self.assertEqual(-1, self.motor.comparar(buenos_aires_la_plata.nombre, quilmes_tandil.nombre, 't'))
            self.assertEqual(1,  self.motor.comparar(quilmes_tandil.nombre,        buenos_aires_la_plata.nombre, 't'))

if __name__ == '__main__':
    unittest.main()
