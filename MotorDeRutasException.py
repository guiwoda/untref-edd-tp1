from MessageException import MessageException


class MotorDeRutasException(MessageException):

    @staticmethod
    def nombre_de_trayecto_duplicado(trayecto):
        return MotorDeRutasException("El nombre de Trayecto: %s ya fue utilizado previamente." % (trayecto.nombre))