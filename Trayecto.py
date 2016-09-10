from Ruta import *


class Trayecto:

    def __init__(self, nombre, ruta):
        self.nombre = nombre
        self.rutas = ['ruta']
        self.distaciaTotal = ruta.distancia
        self.tiempoTotal = ruta.tiempo

    def ultima_ciudad(self):
        return self.rutas[-1].destino

    def ciudad_existe(self, ciudad):
        return [ruta for ruta in self.rutas if ruta.origen == ciudad or ruta.destino == ciudad]
