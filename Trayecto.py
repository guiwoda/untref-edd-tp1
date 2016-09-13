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

        '''def ciudad_existe_en_trayecto(self, ciudad):
        for ruta in self.rutas:
            if ruta.origen == ciudad or ruta.destino == ciudad:
                return True
        else:
            return False
        '''

    def obtener_ruta_con_destino_en(self, ciudad):
        '''
        Verifica si existe la ciudad en este trayecto.
        :param ciudad: string
        :return: ruta
        '''
        for ruta in self.rutas:
            if ruta.destino == ciudad:
                return ruta
            else:
                #este caso sólo se da con existente como origen
                return self.rutas[0]

    def obtener_ciudades(self):
        return [ruta.origen for ruta in self.rutas] + [self.rutas[-1].destino]

    def __str__(self):
        salida = self.nombre + ': '

        for ruta in self.rutas:
            salida += ruta.origen + ', '

        salida += self.ultima_ciudad() + '\n'
        #Formato dístancia y tiempo
        dias = int(self.tiempoTotal / 24 / 60 / 60)
        self.tiempoTotal = self.tiempoTotal - dias * 24 * 60 * 60
        horas = int(self.tiempoTotal / 60 / 60)
        self.tiempoTotal = self.tiempoTotal - horas * 60 * 60
        minutos = int(self.tiempoTotal / 60)

        salida += 'distancia: {0:8.4f} km'.format(self.distaciaTotal/1000000) + '\n'
        salida += 'tiempo estimado de viaje: {0:2d} dias, {1:2d} horas, {2:2d} min'.format(dias, horas, minutos) + '\n'

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