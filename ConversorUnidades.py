import math


class ConversorUnidades():
    @staticmethod
    def distancia_legible(distancia):
        """Convierte una distancia en metros a una distancia legible."""
        if 1000 > distancia:
            return '%s m' % distancia

        return '%s km' % round(distancia / 1000, 1)

    @staticmethod
    def tiempo_legible(tiempo):
        """Convierte un tiempo en segundos a un tiempo legible."""
        if tiempo > 3600 * 24:
            dias, horas = math.modf(tiempo / (3600 * 24))
            return '%s dias, %s hs' % (dias, horas)

        if tiempo > 3600:
            return '%s hs' % round(tiempo / 3600, 1)

        return '%s mins' % round(tiempo / 60, 1)