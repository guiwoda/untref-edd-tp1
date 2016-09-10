class RutaException(BaseException):

    @staticmethod
    def ciudades_desconectadas(origen, destino):
        return RutaException("La ciudades %s y %s no tienen ruta entre ellas." % (origen, destino))

    @staticmethod
    def misma_ciudad():
        return RutaException("No se puede construir una ruta hacia la misma ciudad")


if __name__ == '__main__':
    print(RutaException.ciudades_desconectadas('Buenos Aires', 'New York'))