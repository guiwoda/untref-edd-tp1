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

        distancia, tiempo = self.calcular_distancia_tiempo(data)
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

        trayecto.rutas.append(ruta)

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

        rutaActual = trayecto.obtener_ruta_con_destino_en(existente)

        rutaHaciaParada = self.obtener_ruta(rutaActual.origen, parada)
        rutaHaciaExistente = self.obtener_ruta(parada, existente)

        posicion = trayecto.rutas.index(rutaActual)

        trayecto.rutas = trayecto.rutas[:posicion] + [rutaHaciaParada, rutaHaciaExistente] + trayecto.rutas[posicion + 1:]
        return trayecto

    def concatenar(self, inicial, final):
        """Concatenar dos trayectos.

        Dados dos trayectos cualquiera concatenarlos si existe una ruta entre la última ciudad del
        primer trayecto y la primera ciudad del segundo trayecto. En caso de error se debe mostrar un mensaje.

        :type inicial: str
        :type final: str
        :rtype: Trayecto
        """
        trayectoInicial = self.obtener_trayecto(inicial)
        trayectoFinal = self.obtener_trayecto(final)

        conexion = self.obtener_ruta(trayectoInicial.ultima_ciudad(), trayectoFinal.primera_ciudad())

        trayectoInicial.rutas = trayectoInicial.rutas + [conexion] + trayectoFinal.rutas

        return trayectoInicial

    def comparar(self, trayecto, otroTrayecto, tipo):
        """Comparar dos trayectos.

        Dados dos trayectos los debe poder comparar por distancia y por tiempo, para lo cual se
        usarán los parámetros: "d" para comparar por distancias y "t" para comparar por tiempo.

        :type trayecto: str
        :type otroTrayecto: str
        :type tipo: str
        :rtype: int
        """

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

    def listar(self):
        """Listar los trayectos calculados.

        Debe listar los nombres de los trayectos ya calculados que se encuentran en el sistema.

        :rtype: list
        """

    def guardar(self, trayecto = ''):
        """Almacenar en disco los trayectos calculados.

        Debe permitir almacenar un trayecto dado su nombre o todos los trayectos si no se especifica
        un trayecto particular.

        :type trayecto: str
        """

    def recuperar(self):
        """Recuperar de disco los trayectos almacenados.

        Debe recuperar todos los trayectos almacenados en disco.
        """

    def esta_guardado(self):
        """Verifica si todos los trayectos están persistidos en disco.

        :rtype: bool
        """

    def calcular_distancia_tiempo(self, data):
        """Calcula distancia y tiempo en base a un mensaje de la `distance_matrix` de Google Maps.

        :type data: dict
        :rtype: tuple
        """
        distancia = data['rows'][0]['elements'][0]['distance']['value']
        tiempo = data['rows'][0]['elements'][0]['duration']['value']
        return distancia, tiempo

    def obtener_trayecto(self, nombre):
        """Obtiene un trayecto por nombre, o emite un error si no existe.

        :type nombre: str
        :rtype: Trayecto
        """
        if not nombre in self.trayectos:
            raise KeyError("El trayecto [%s] no existe" % nombre)

        return self.trayectos[nombre]
