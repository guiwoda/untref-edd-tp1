from ConversorUnidades import ConversorUnidades


class Ruta:

    def __init__(self, origen, destino, distancia, tiempo):
        self.origen = origen
        self.destino = destino
        self.distancia = distancia
        self.tiempo = tiempo

    def __str__(self):
        return '%s - %s\n%s\n%s\n' % (self.origen, self.destino, ConversorUnidades.distancia_legible(self.distancia), ConversorUnidades.tiempo_legible(self.tiempo))

    def __eq__(self, other):
        return self.origen == other.origen and self.destino == other.destino