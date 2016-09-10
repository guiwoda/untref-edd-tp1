from config import *
import googlemaps

class Ruta:

    def __init__(self, origen, destino):
        self.origen = origen
        self.destino = destino

        try:
            ruta = gmaps.distance_matrix(origen, destino)
            self.distancia = ruta['rows'][0]['elements'][0]['distance']['value']
            self.tiempo = ruta['rows'][0]['elements'][0]['duration']['value']

        except:
            #Hay que ver como imprimimos excepciones vìa Menu
            print ""