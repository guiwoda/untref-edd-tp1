from Ruta import *


class Trayecto:

    def __init__(self):
        self.rutas = []
        self.distaciaTotal = 0
        self.tiempoTotal = 0

    def ultima_ciudad(self):
        return self.rutas[-1].destino

    def ciudad_existe(self, ciudad):
        return [ruta for ruta in self.rutas if ruta.origen == ciudad or ruta.destino == ciudad]
