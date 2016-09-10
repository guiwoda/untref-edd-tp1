from config import *
import googlemaps

class MotorDeRutas:

    def __init__(self):
        self.trayectos = []
        gmaps=googlemaps.Client(key=KEY) #inicializa la app para consultar API


    def crear_trayecto(self, origen, destino, nombre):
        '''
        Crear un trayecto a partir de dos ciudades: Dado el nombre de dos ciudades, debe
        buscar en la API de Google si hay un camino entre los puntos dados, y si no hay
        camino debe mostrar un mensaje de error. Origen y destino deben ser ciudades
        distintas. Además cada trayecto tiene un nombre que lo identifica.
        :return: Trayecto
        '''
       #try:
        if origen != destino:
            #aca debería ir otro try
            ruta = Ruta(origen, destino)
            trayecto = Trayecto(nombre, ruta)
            trayectos.append(trayecto)

        #except:
            #print "Misma ciudad de origen y destino"

    def agregar_ciudad(self, trayecto, ciudad):
        '''
        Agregar una ciudad al nal de un trayecto: Dado un trayecto y el nombre de una
        ciudad, debe agregar la ciudad al final del trayecto, si no es posible debe mostrar
        un mensaje de error.
        :param trayecto:
        :return:
        '''

    def agregar_parada(self, trayecto, antesDeCiudad, parada):
        '''
        Agregar una ciudad intermedia a un trayecto: Dado un trayecto, una ciudad que
        pertenece a ese trayecto y el nombre de otra ciudad, agregar la nueva ciudad antes
        de la ciudad que ya pertenece al trayecto. Para poder agregarla debe vericar que
        hay rutas para que el trayecto nal sea válido.
        :return:
        '''
