from ConversorUnidades import ConversorUnidades
from Ruta import Ruta

class Trayecto:

    def __init__(self, nombre, ruta):
        self.nombre = nombre
        self.rutas = [ruta]
        self.distaciaTotal = ruta.distancia
        self.tiempoTotal = ruta.tiempo

    def ultima_ciudad(self):
        '''
        Devuelve la última ciudad de este trayecto.
        :return: string
        '''
        return self.rutas[-1].destino

    def ciudad_existe(self, ciudad):
        '''
        Verifica si existe la ciudad en este trayecto.
        :param ciudad: string
        :return: boolean
        '''
        return [ruta for ruta in self.rutas if ruta.origen == ciudad or ruta.destino == ciudad]

    def obtener_ruta_con_destino_en(self, ciudad):
        '''
        Verifica si existe la ciudad en este trayecto.
        :param ciudad: string
        :return: ruta
        '''
        for ruta in self.rutas:
            if ruta.destino == ciudad:
                return ruta
            elif self.rutas[0].origen == ciudad:
                return self.rutas[0]

    def obtener_ciudades(self):
        return [ruta.origen for ruta in self.rutas] + [self.rutas[-1].destino]

    def __str__(self):
        salida = self.nombre + ': '

        for ruta in self.rutas:
            salida += ruta.origen + ', '

        salida += self.ultima_ciudad() + '\n'

        salida += 'distancia: ' + ConversorUnidades.distancia_legible(self.distaciaTotal) + '\n'
        salida += 'tiempo estimado de viaje: ' + ConversorUnidades.tiempo_legible(self.tiempoTotal)

        return salida

    def primera_ciudad(self):
        return self.rutas[0].origen

    def agregar_ruta(self, ruta):
        """Agrega una ruta al trayecto.

        :type ruta: Ruta
        """
        self.rutas.append(ruta)

        self.actualizar_totales()

    def actualizar_totales(self):
        """Actualiza los totales de distancia y tiempo."""
        self.tiempoTotal = 0
        self.distaciaTotal = 0

        for ruta in self.rutas:
            self.tiempoTotal += ruta.tiempo
            self.distaciaTotal += ruta.distancia

    def __eq__(self, other):
        return self.nombre == other.nombre and self.rutas == other.rutas