class TrayectoException(BaseException):

    @staticmethod
    def ciudad_inexistente_en_trayecto(destinoIntermedio, trayecto):
        return TrayectoException("La ciudad %s no existe en el trayecto %s." % (destinoIntermedio, trayecto))