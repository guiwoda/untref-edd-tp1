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
