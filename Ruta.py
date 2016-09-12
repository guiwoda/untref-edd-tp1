import math

class Ruta:

    def __init__(self, origen, destino, distancia, tiempo):
        self.origen = origen
        self.destino = destino
        self.distancia = distancia
        self.tiempo = tiempo

    def __str__(self):
        return '%s - %s\n%s\n%s\n' % (self.origen, self.destino, self.distancia_legible(), self.tiempo_legible())

    def distancia_legible(self):
        if (1000 > self.distancia):
            return '%s m' % self.distancia

        return '%s km' % round(self.distancia / 1000, 1)

    def tiempo_legible(self):
        if self.tiempo > 3600 * 24:
            dias, horas = math.modf(self.tiempo / (3600 * 24))
            return '%s dias, %s hs' % (dias, horas)

        if self.tiempo > 3600:
            return '%s hs' % round(self.tiempo / 3600, 1)

        return '%s mins' % round(self.tiempo / 60, 1)