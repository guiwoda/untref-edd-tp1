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
        with vcr.use_cassette('fixtures/test_crea_trayectos_nuevos.yaml'):
            trayecto = self.motor.crear_trayecto('Ushuaia, Argentina', 'La Quiaca, Argentina', 'De Ushuaia a La Quiaca')

            self.assertIsInstance(trayecto, Trayecto)

    def test_falla_cuando_el_trayecto_no_existe(self):
        with vcr.use_cassette('fixtures/test_falla_cuando_el_trayecto_no_existe.yaml'):
            with self.assertRaises(RutaException):
                self.motor.crear_trayecto('Buenos Aires, Argentina', 'Reykjavik, Islandia', 'islandia')

    def test_agrega_ciudad_a_trayecto(self):
        with vcr.use_cassette('fixtures/test_agrega_ciudad_a_trayecto.yaml'):
            trayecto = self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'bs_as_la_plata')
            distancia = trayecto.distancia_total
            tiempo = trayecto.tiempo_total

            self.motor.agregar_ciudad(trayecto.nombre, 'Quilmes')

            self.assertEqual('Quilmes', trayecto.ultima_ciudad())
            self.assertGreater(trayecto.distancia_total, distancia)
            self.assertGreater(trayecto.tiempo_total, tiempo)

    def test_falla_cuando_la_ciudad_no_existe_en_trayecto(self):
        with vcr.use_cassette('fixtures/test_falla_cuando_la_ciudad_no_existe_en_trayecto.yaml'):
            trayecto = self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'bs_as_la_plata')

            with self.assertRaises(TrayectoException):
                self.motor.agregar_parada(trayecto.nombre, 'Tandil', 'Quilmes')

    def test_agrega_parada_a_trayecto(self):
        with vcr.use_cassette('fixtures/test_agrega_parada_a_trayecto.yaml'):
            trayecto = self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'bs_as_la_plata')
            self.motor.agregar_ciudad(trayecto.nombre, 'Tandil')

            distancia = trayecto.distancia_total
            tiempo = trayecto.tiempo_total

            self.motor.agregar_parada(trayecto.nombre, 'La Plata', 'Quilmes')

            self.assertEqual(['Buenos Aires', 'Quilmes', 'La Plata', 'Tandil'], trayecto.obtener_ciudades())
            self.assertGreater(trayecto.distancia_total, distancia)
            self.assertGreater(trayecto.tiempo_total, tiempo)
    def test_agrega_parada_antes_de_la_primera_ciudad_al_trayecto(self):
        with vcr.use_cassette('fixtures/test_agrega_parada_antes_de_la_primera_ciudad_al_trayecto.yaml'):
            trayecto = self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'bs_as_la_plata')
            self.motor.agregar_ciudad(trayecto.nombre, 'Tandil')

            distancia = trayecto.distancia_total
            tiempo = trayecto.tiempo_total

            self.motor.agregar_parada(trayecto.nombre, 'Buenos Aires', 'Quilmes')

            self.assertEqual(['Quilmes', 'Buenos Aires', 'La Plata', 'Tandil'], trayecto.obtener_ciudades())
            self.assertGreater(trayecto.distancia_total, distancia)
            self.assertGreater(trayecto.tiempo_total, tiempo)
    def test_concatena_trayectos(self):
        with vcr.use_cassette('fixtures/test_concatena_trayectos.yaml'):
            trayecto_inicial = self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'trayecto_inicial')
            trayecto_final = self.motor.crear_trayecto('Quilmes', 'Tandil', 'trayecto_final')
            self.motor.concatenar(trayecto_inicial.nombre, trayecto_final.nombre)

            self.assertEqual(['Buenos Aires', 'La Plata', 'Quilmes', 'Tandil'], trayecto_inicial.obtener_ciudades())

    def test_obtiene_trayectos_por_nombre(self):
        with vcr.use_cassette('fixtures/test_obtiene_trayectos_por_nombre.yaml'):
            trayecto = self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'bs_as_la_plata')

            self.assertEqual(trayecto, self.motor.obtener_trayecto(trayecto.nombre))

    def test_obtiene_rutas_entre_dos_ciudades(self):
        with vcr.use_cassette('fixtures/test_obtiene_rutas_entre_dos_ciudades.yaml'):
            ruta = self.motor.obtener_ruta('Buenos Aires', 'La Plata')

            self.assertIsInstance(ruta, Ruta)
    def test_falla_al_obtener_rutas_entre_dos_ciudades_desconectadas(self):
        with vcr.use_cassette('fixtures/test_falla_al_obtener_rutas_entre_dos_ciudades_desconectadas.yaml'):
            with self.assertRaises(RutaException):
                self.motor.obtener_ruta('Buenos Aires, Argentina', 'Reykjavik, Islandia')

    def test_muestra_trayectos(self):
        with vcr.use_cassette('fixtures/test_muestra_trayectos.yaml'):
            self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'bs_as_la_plata')

            self.assertEqual(
'''bs_as_la_plata: Buenos Aires, La Plata
distancia: 58.2 km
tiempo estimado de viaje: 56.1 mins''',
                self.motor.mostrar('bs_as_la_plata'))

    def test_compara_trayectos_por_distancia(self):
        with vcr.use_cassette('fixtures/test_compara_trayectos_por_distancia.yaml'):
            buenos_aires_la_plata = self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'buenos_aires_la_plata')
            quilmes_tandil        = self.motor.crear_trayecto('Quilmes',      'Tandil',   'quilmes_tandil')

            self.assertEqual(0,  self.motor.comparar(buenos_aires_la_plata.nombre, buenos_aires_la_plata.nombre, 'd'))
            self.assertEqual(-1, self.motor.comparar(buenos_aires_la_plata.nombre, quilmes_tandil.nombre, 'd'))
            self.assertEqual(1,  self.motor.comparar(quilmes_tandil.nombre,        buenos_aires_la_plata.nombre, 'd'))

    def test_compara_trayectos_por_tiempo(self):
        with vcr.use_cassette('fixtures/test_compara_trayectos_por_tiempo.yaml'):
            buenos_aires_la_plata = self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'buenos_aires_la_plata')
            quilmes_tandil        = self.motor.crear_trayecto('Quilmes',      'Tandil',   'quilmes_tandil')

            self.assertEqual(0,  self.motor.comparar(buenos_aires_la_plata.nombre, buenos_aires_la_plata.nombre, 't'))
            self.assertEqual(-1, self.motor.comparar(buenos_aires_la_plata.nombre, quilmes_tandil.nombre, 't'))
            self.assertEqual(1,  self.motor.comparar(quilmes_tandil.nombre,        buenos_aires_la_plata.nombre, 't'))

    def test_muestra_rutas_de_un_trayecto(self):
        with vcr.use_cassette('fixtures/test_muestra_rutas_de_un_trayecto.yaml'):
            trayecto = self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'bs_as_la_plata')
            self.motor.agregar_ciudad(trayecto.nombre, 'La Quiaca')

            self.assertEqual(
                '''Buenos Aires - La Plata
58.2 km
56.1 mins

La Plata - La Quiaca
1831.0 km
21.0 hs

''',
                 self.motor.mostrar_rutas(trayecto.nombre)
            )

    def test_muestra_trayectos_disponibles(self):
        with vcr.use_cassette('fixtures/test_muestra_trayectos_disponibles.yaml'):
            self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'tray_a')
            self.motor.crear_trayecto('Quilmes', 'Tandil', 'tray_b')

            self.assertEqual({'tray_a', 'tray_b'}, set(self.motor.listar()))

    def test_persiste_los_trayectos(self):
        with vcr.use_cassette('fixtures/test_persiste_los_trayectos.yaml'):
            self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'tray_a')
            self.motor.crear_trayecto('Quilmes', 'Tandil', 'tray_b')

            self.motor.guardar()

            self.motor = MotorDeRutas()
            self.motor.recuperar()

            self.assertEqual({'tray_a', 'tray_b'}, set(self.motor.listar()))

    def test_sabe_si_hay_cambios_sin_guardar(self):
        with vcr.use_cassette('fixtures/test_sabe_si_hay_cambios_sin_guardar.yaml'):
            self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'algo_nuevo')

            self.assertFalse(self.motor.esta_guardado())

    def test_sabe_si_hay_cambios_guardados(self):
        with vcr.use_cassette('fixtures/test_sabe_si_hay_cambios_guardados.yaml'):
            self.motor.crear_trayecto('Buenos Aires', 'La Plata', 'tray_a')
            self.motor.guardar('tray_a')

            self.assertTrue(self.motor.esta_guardado())

if __name__ == '__main__':
    unittest.main()
