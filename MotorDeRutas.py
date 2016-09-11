from RutaException import RutaException
from config import *
import googlemaps
from Ruta import Ruta
from Trayecto import Trayecto

class MotorDeRutas:

    def __init__(self):
        self.trayectos = {}
        self.gmaps = googlemaps.Client(key=KEY) #inicializa la app para consultar API


    def crear_trayecto(self, origen, destino, nombre):
        '''
        Crear un trayecto a partir de dos ciudades: Dado el nombre de dos ciudades, debe
        buscar en la API de Google si hay un camino entre los puntos dados, y si no hay
        camino debe mostrar un mensaje de error. Origen y destino deben ser ciudades
        distintas. Además cada trayecto tiene un nombre que lo identifica.
        :return: Trayecto
        '''
        if origen == destino:
            raise RutaException.misma_ciudad()

        data = self.gmaps.distance_matrix(origen, destino)

        if data['rows'][0]['elements'][0]['status'] != 'OK':
            raise RutaException.ciudades_desconectadas(origen, destino)

        distancia, tiempo = self.calcular_distancia_tiempo(data)
        ruta = Ruta(origen, destino, distancia, tiempo)

        self.trayectos[nombre] = Trayecto(nombre, ruta)

        return self.trayectos[nombre]


    def agregar_ciudad(self, trayecto, ciudad):
        '''
        Agregar una ciudad al final de un trayecto: Dado un trayecto y el nombre de una
        ciudad, debe agregar la ciudad al final del trayecto, si no es posible debe mostrar
        un mensaje de error.
        :param trayecto:
        :param ciudad:
        :return:
        '''
        if trayecto not in self.trayectos.keys():
            raise IndexError('Trayecto no encontrado.')

        data = self.gmaps.distance_matrix(self.trayectos[trayecto].ultima_ciudad(), ciudad)

        if data['rows'][0]['elements'][0]['status'] != 'OK':
            raise RutaException.ciudades_desconectadas(self.trayectos[trayecto].ultima_ciudad(), ciudad)

        distancia, tiempo = (self.calcular_distancia_tiempo(data))
        ruta = Ruta(self.trayectos[trayecto].ultima_ciudad(), ciudad, distancia, tiempo)

        self.trayectos[trayecto].rutas.append(ruta)

    def agregar_parada(self, trayecto, destinoIntermedio, parada):
        '''
        Agregar una ciudad intermedia a un trayecto: Dado un trayecto, una ciudad que
        pertenece a ese trayecto y el nombre de otra ciudad, agregar la nueva ciudad antes
        de la ciudad que ya pertenece al trayecto. Para poder agregarla debe vericar que
        hay rutas para que el trayecto nal sea válido.
        :return:
        '''
        if trayecto not in self.trayectos.keys():
            raise IndexError('Trayecto no encontrado.')
        data = self.gmaps.distance_matrix(parada, destinoIntermedio)

        if data['rows'][0]['elements'][0]['status'] != 'OK':
            raise RutaException.ciudades_desconectadas(parada, destinoIntermedio)

        distancia, tiempo = (self.calcular_distancia_tiempo(data))
        ruta = Ruta(parada, destinoIntermedio, distancia, tiempo)

        self.trayectos[trayecto].rutas.append(ruta)
        #concatenar listas con + e indices y slides y crear nueva lista

    def concatenar(self, trayectoInicial, trayectoFinal):
        '''
        Concatenar dos trayectos: Dados dos trayectos cualquiera concatenarlos si existe
        una ruta entre la última ciudad del primer trayecto y la primera ciudad del segundo
        trayecto. En caso de error se debe mostrar un mensaje.
        :param trayectoInicial:
        :param trayectoFinal:
        :return:
        '''

    def comparar(self, trayecto, otroTrayecto):
        '''
        Comparar dos trayectos: Dados dos trayectos los debe poder comparar por distan-
        cia y por tiempo, para lo cual se usarán los parámetros: "d" para comparar por
        distancias y "t" para comparar por tiempo.
        :param trayecto:
        :param otroTrayecto:
        :return:
        '''

    def mostrar(self, trayecto):
        '''
        Mostrar un trayecto: Debe mostrar el nombre o identificador del trayecto y la
        lista ordenada de ciudades, la distancia total (suma de las rutas entre ciudades
        consecutivas) y tiempo total estimado de viaje (suma de los tiempos de cada ruta)
        con el siguiente formato:
            <nombre>: <ciudad1>, <ciudad2>,...,<ciudadn>
            distancia: <distancia en km> km
            tiempo estimado de viaje: <dias> días, <horas>, hs
        :param trayecto:
        :return:
        '''
        if not trayecto in self.trayectos.keys():
            raise KeyError("El trayecto %s no existe" % trayecto)

        return str(self.trayectos[trayecto])

    def mostrar_rutas(self, trayecto):
        '''
        Mostrar rutas: Dado un trayecto debe mostrar todas las rutas que forman el trayecto
        con el siguiente formato:
            <origen 1> - <destino 1>
            <distancia en km> km
            <dias> días, <horas> hs
            <línea en blanco>
            <destino 1> - <destino 2>
            <distancia en km> km
            <dias> días, <horas> hs
        :param trayecto:
        :return:
        '''

    def listar(self):
        '''
        Listar los trayectos calculados: Debe listar los nombres de los trayectos ya calculados
        que se encuentran en el sistema.
        :return:
        '''

    def guardar(self):
        '''
        Almacenar en disco los trayectos calculados: Debe permitir almacenar un trayecto
        dado su nombre o todos los trayectos si no se especica un trayecto particular.
        :return:
        '''

    def recuperar(self):
        '''
        Recuperar de disco los trayectos almacenados: Debe recuperar todos los trayectos
        almacenados en disco
        :return:
        '''

    def esta_guardado(self):
        '''
        Verifica si todos los trayectos están persistidos en disco.
        :return: bool
        '''

    def calcular_distancia_tiempo(self, data):
        distancia = data['rows'][0]['elements'][0]['distance']['value']
        tiempo = data['rows'][0]['elements'][0]['duration']['value']
        return distancia, tiempo

        '''def verificar_ruta(self, origen, destino):
        #Agregar Try que chequee ruta
        data = self.gmaps.distance_matrix(ultima_ciudad, ciudad)
        distancia, tiempo = calcular_distancia_tiempo(data)
        ruta = Ruta(self.trayectos[trayecto].origen, destino, distancia, tiempo)
        return ruta'''


if __name__ == '__main__':
    motor = MotorDeRutas()

