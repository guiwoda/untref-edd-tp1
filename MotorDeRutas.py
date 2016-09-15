import pickle
from os import listdir

from os.path import isfile

from RutaException import RutaException
from TrayectoException import TrayectoException
from config import *
import googlemaps
from Ruta import Ruta
from Trayecto import Trayecto


class MotorDeRutas:
    def __init__(self):
        self.trayectos = {}
        self.gmaps = googlemaps.Client(key=KEY)  # inicializa la app para consultar API

    def crear_trayecto(self, origen, destino, nombre):
        """Crear un trayecto a partir de dos ciudades.

        Dado el nombre de dos ciudades, debe buscar en la API de Google si hay un camino
        entre los puntos dados, y si no hay camino debe mostrar un mensaje de error.
        Origen y destino deben ser ciudades distintas. Además cada trayecto tiene un nombre
        que lo identifica.

        :type origen: str
        :type destino: str
        :type nombre: str
        :rtype: Trayecto
        """
        if nombre in self.trayectos:
            raise TrayectoException("El trayecto [%s] ya existe." % nombre)

        ruta = self.obtener_ruta(origen, destino)

        self.trayectos[nombre] = Trayecto(nombre, ruta)

        return self.trayectos[nombre]

    def obtener_ruta(self, origen, destino):
        """Obtiene una ruta entre dos ciudades.

        :type origen: str
        :type destino: str
        :rtype: Ruta
        :raise: RutaException si son la misma ciudad o no hay ruta posible entre las ciudades.
        """
        if origen == destino:
            raise RutaException.misma_ciudad()

        data = self.gmaps.distance_matrix(origen, destino)
        if data['rows'][0]['elements'][0]['status'] != 'OK':
            raise RutaException.ciudades_desconectadas(origen, destino)

        distancia = data['rows'][0]['elements'][0]['distance']['value']
        tiempo = data['rows'][0]['elements'][0]['duration']['value']

        return Ruta(origen, destino, distancia, tiempo)

    def agregar_ciudad(self, trayecto, ciudad):
        """Agregar una ciudad al final de un trayecto.

        Dado un trayecto y el nombre de una ciudad, debe agregar la ciudad al final del trayecto,
        si no es posible debe mostrar un mensaje de error.

        :type trayecto: str
        :type ciudad: str
        """
        trayecto = self.obtener_trayecto(trayecto)
        ruta = self.obtener_ruta(trayecto.ultima_ciudad(), ciudad)

        trayecto.agregar_ruta(ruta)

    def agregar_parada(self, trayecto, existente, parada):
        """Agregar una ciudad intermedia a un trayecto.

        Dado un trayecto, una ciudad que pertenece a ese trayecto y el nombre de otra ciudad,
        agregar la nueva ciudad antes de la ciudad que ya pertenece al trayecto.
        Para poder agregarla debe verificar que hay rutas para que el trayecto final sea válido.

        :type trayecto: str
        :type existente: str
        :type parada: str
        :type: Trayecto
        """
        trayecto = self.obtener_trayecto(trayecto)

        if not trayecto.ciudad_existe(existente):
            raise TrayectoException.ciudad_inexistente_en_trayecto(existente, trayecto)

        if trayecto.primera_ciudad() == existente:
            ruta_hacia_existente = self.obtener_ruta(parada, trayecto.primera_ciudad())
            trayecto.rutas = [ruta_hacia_existente] + trayecto.rutas
        else:
            ruta_actual = trayecto.obtener_ruta_con_destino_en(existente)

            ruta_hacia_parada = self.obtener_ruta(ruta_actual.origen, parada)
            ruta_hacia_existente = self.obtener_ruta(parada, existente)

            i = trayecto.rutas.index(ruta_actual)
            trayecto.rutas = trayecto.rutas[:i] + [ruta_hacia_parada, ruta_hacia_existente] + trayecto.rutas[i + 1:]

        trayecto.actualizar_totales()

        return trayecto

    def concatenar(self, inicial, final):
        """Concatenar dos trayectos.

        Dados dos trayectos cualquiera concatenarlos si existe una ruta entre la última ciudad del
        primer trayecto y la primera ciudad del segundo trayecto. En caso de error se debe mostrar un mensaje.

        :type inicial: str
        :type final: str
        :rtype: Trayecto
        """
        trayecto_inicial = self.obtener_trayecto(inicial)
        trayecto_final = self.obtener_trayecto(final)

        conexion = self.obtener_ruta(trayecto_inicial.ultima_ciudad(), trayecto_final.primera_ciudad())

        trayecto_inicial.rutas = trayecto_inicial.rutas + [conexion] + trayecto_final.rutas
        trayecto_inicial.actualizar_totales()

        return trayecto_inicial

    def comparar(self, trayecto, otroTrayecto, tipo):
        """Comparar dos trayectos.

        Dados dos trayectos los debe poder comparar por distancia y por tiempo, para lo cual se
        usarán los parámetros: "d" para comparar por distancias y "t" para comparar por tiempo.

        :type trayecto: str
        :type otroTrayecto: str
        :type tipo: str
        :rtype: int
        """
        if tipo == 'd':
            return self.comparar_distancias(trayecto, otroTrayecto)

        if tipo == 't':
            return self.comparar_tiempo(trayecto, otroTrayecto)

        raise IndexError("Tipo de comparación invalida. Usar 'd' para distancias o 't' para tiempo.")

    def mostrar(self, trayecto):
        """Mostrar un trayecto.

        Debe mostrar el nombre o identificador del trayecto y la lista ordenada de ciudades,
        la distancia total (suma de las rutas entre ciudades consecutivas) y tiempo total
        estimado de viaje (suma de los tiempos de cada ruta) con el siguiente formato:

            <nombre>: <ciudad1>, <ciudad2>,...,<ciudadn>
            distancia: <distancia en km> km
            tiempo estimado de viaje: <dias> días, <horas>, hs

        :type trayecto: str
        :rtype: str
        """
        return str(self.obtener_trayecto(trayecto))

    def mostrar_rutas(self, trayecto):
        """Mostrar rutas.

        Dado un trayecto debe mostrar todas las rutas que forman el trayecto con el siguiente formato:

            <origen 1> - <destino 1>
            <distancia en km> km
            <dias> días, <horas> hs
            <línea en blanco>
            <destino 1> - <destino 2>
            <distancia en km> km
            <dias> días, <horas> hs

        :type trayecto: str
        :rtype: str
        """
        trayecto = self.obtener_trayecto(trayecto)

        salida = ''
        for ruta in trayecto.rutas:
            salida += str(ruta) + '\n'

        return salida

    def listar(self):
        """Listar los trayectos calculados.

        Debe listar los nombres de los trayectos ya calculados que se encuentran en el sistema.

        :rtype: list
        """
        return [trayecto for trayecto in self.trayectos]

    def guardar(self, trayecto = ''):
        """Almacenar en disco los trayectos calculados.

        Debe permitir almacenar un trayecto dado su nombre o todos los trayectos si no se especifica
        un trayecto particular.

        :type trayecto: str
        """
        for nombre in self.trayectos:
            if not trayecto or trayecto == nombre:
                with open('trayectos/%s.p' % nombre, 'wb') as file:
                    pickle.dump(self.trayectos[nombre], file)

    def recuperar(self):
        """Recuperar de disco los trayectos almacenados.

        Debe recuperar todos los trayectos almacenados en disco.
        """
        self.trayectos = self.cargar_de_disco()

    def cargar_de_disco(self):
        """Carga de disco los trayectos y los devuelve.

        :rtype: dict
        """
        data = {}
        dir = 'trayectos'
        for archivo in listdir(dir):
            path = '%s/%s' % (dir, archivo)

            if isfile(path) and archivo[-2:] == '.p':
                with open(path, 'rb') as persistido:
                    data[archivo[:-2]] = pickle.load(persistido)

        return data

    def esta_guardado(self):
        """Verifica si todos los trayectos están persistidos en disco.

        :rtype: bool
        """
        if not self.trayectos:
            return True

        guardados = self.cargar_de_disco()

        for trayecto in self.trayectos:
            if trayecto not in guardados:
                return False

            if self.trayectos[trayecto] != guardados[trayecto]:
                return False

        return True

    def obtener_trayecto(self, nombre):
        """Obtiene un trayecto por nombre, o emite un error si no existe.

        :type nombre: str
        :rtype: Trayecto
        """
        if not nombre in self.trayectos:
            raise TrayectoException("El trayecto [%s] no existe" % nombre)

        return self.trayectos[nombre]

    def comparar_distancias(self, trayecto_a, trayecto_b):
        """Compara la distancia entre dos trayectos.

        Devuelve -1 si el primero es más corto que el segundo, 1 si es más largo y 0 si son iguales.

        :type trayecto_a: str
        :type trayecto_b: str
        :rtype: int
        """

        trayecto_a = self.obtener_trayecto(trayecto_a)
        trayecto_b = self.obtener_trayecto(trayecto_b)

        return (trayecto_a.distancia_total > trayecto_b.distancia_total) - (trayecto_a.distancia_total < trayecto_b.distancia_total)

    def comparar_tiempo(self, trayecto_a, trayecto_b):
        """Compara el tiempo entre dos trayectos.

        Devuelve -1 si el primero es más rápido que el segundo, 1 si es más lento y 0 si son iguales.

        :type trayecto_a: str
        :type trayecto_b: str
        :rtype: int
        """

        trayecto_a = self.obtener_trayecto(trayecto_a)
        trayecto_b = self.obtener_trayecto(trayecto_b)

        return (trayecto_a.tiempo_total > trayecto_b.tiempo_total) - (trayecto_a.tiempo_total < trayecto_b.tiempo_total)
