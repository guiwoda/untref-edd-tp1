import functools


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

    def __str__(self):
        salida = self.nombre + ': '

        for ruta in self.rutas:
            salida += ruta.origen + ', '

        salida += self.ultima_ciudad() + '\n'

        salida += 'distancia: ' + str(self.distaciaTotal) + '\n'
        salida += 'tiempo estimado de viaje: ' + str(self.tiempoTotal)

        return salida

