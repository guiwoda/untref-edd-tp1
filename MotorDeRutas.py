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

        #aca debería ir otro try?

        data = self.gmaps.distance_matrix(origen, destino)

        if data['rows'][0]['elements'][0]['status'] != 'OK':
            raise RutaException.ciudades_desconectadas(origen, destino)

        distancia = data['rows'][0]['elements'][0]['distance']['value']
        tiempo = data['rows'][0]['elements'][0]['duration']['value']
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

        ruta = Ruta(self.trayectos[trayecto].ultima_ciudad(), ciudad)

        self.trayectos[trayecto].rutas.append(ruta)

    def agregar_parada(self, trayecto, antesDeCiudad, parada):
        '''
        Agregar una ciudad intermedia a un trayecto: Dado un trayecto, una ciudad que
        pertenece a ese trayecto y el nombre de otra ciudad, agregar la nueva ciudad antes
        de la ciudad que ya pertenece al trayecto. Para poder agregarla debe vericar que
        hay rutas para que el trayecto nal sea válido.
        :return:
        '''

if __name__ == '__main__':
    motor = MotorDeRutas()

