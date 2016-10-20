from time import sleep

from cursesmenu import *
from cursesmenu.items import *

from MessageException import MessageException
from MotorDeRutas import MotorDeRutas


class App:

    def __init__(self, motor, menu):
        '''
        :type motor: MotorDeRutas
        :type menu: CursesMenu
        '''
        self.motor = motor
        self.menu = menu

    def __create_function_item(self, title, func):
        return FunctionItem(title, self.__do_wait(func))

    def __do_wait(self, func, wait=3):
        def _do():
            try:
                print(func())
                sleep(wait)
            except MessageException as e:
                print(e.message)
                sleep(wait)
                _do()
        return _do

    def __crear_trayecto(self):
        nombre = input('Ingrese nombre del trayecto: ')
        origen = input('Ciudad origen? ')
        destino = input('Ciudad destino? ')

        self.motor.crear_trayecto(origen, destino, nombre)

        return "Trayecto [%s] creado." % nombre

    def __agregar_ciudad(self):
        if not self.motor.trayectos:
            return "No hay trayectos disponibles."

        trayecto = input('Ingrese nombre del trayecto: ')
        ciudad = input('Ciudad a agregar? ')

        self.motor.agregar_ciudad(trayecto, ciudad)

        return "Ciudad [%s] agregada a [%s]" % (ciudad, trayecto)

    def __agregar_parada(self):
        if not self.motor.trayectos:
            return "No hay trayectos disponibles."

        trayecto = input('Ingrese nombre del trayecto: ')
        existente = input('Ciudad existente del trayecto? ')
        parada = input('Ciudad a agregar? ')

        self.motor.agregar_parada(trayecto, existente, parada)

        return "Ciudad [%s] agregada antes de [%s] a [%s]" % (parada, existente, trayecto)

    def __concatenar(self):
        if len(self.motor.trayectos) < 2:
            return "No hay suficientes trayectos disponibles."

        inicial = input('Ingrese trayecto inicial: ')
        final = input('Ingrese trayecto final: ')

        self.motor.concatenar(inicial, final)

        return "Trayectos [%s] concatenado al final de [%s]." % (final, inicial)

    def __comparar(self):
        if len(self.motor.trayectos) < 2:
            return "No hay suficientes trayectos disponibles."

        a = input('Ingrese trayecto: ')
        b = input('Ingrese trayecto a comparar: ')
        options = ['distancia', 'tiempo']
        tipo = options[SelectionMenu.get_selection(options, 'Como comparo?', exit_option=False)]

        mensajes = {
            -1: '%s es menor que %s',
            0:  '%s y %s son iguales',
            1:  '%s es mayor que %s',
        }

        return mensajes[self.motor.comparar(a, b, tipo[0])] % (a, b)

    def __mostrar(self):
        if not self.motor.trayectos:
            return "No hay trayectos disponibles."

        trayecto = input('Ingrese trayecto: ')

        return self.motor.mostrar(trayecto)

    def __mostrar_rutas(self):
        if not self.motor.trayectos:
            return "No hay trayectos disponibles."

        trayecto = input('Ingrese trayecto: ')

        return self.motor.mostrar_rutas(trayecto)

    def __listar(self):
        return str(self.motor.listar()) if self.motor.trayectos else "No hay trayectos."

    def __guardar(self):
        trayecto = input('Trayecto a guardar? (Enter para guardar todo) ')
        self.motor.guardar(trayecto)

        return "Trayecto%s guardado%s" % ((" ["+trayecto+"]", "") if trayecto else ("s", "s"))

    def __cargar(self):
        self.motor.recuperar()

        return "Trayectos cargados: %s" % str(self.motor.listar())

    def __salir(self):
        if not self.motor.esta_guardado():
            self.motor.guardar()
        return "Adios"

    def main(self):
        self.menu.append_item(self.__create_function_item("Crear trayecto", self.__crear_trayecto))
        self.menu.append_item(self.__create_function_item("Agregar ciudad", self.__agregar_ciudad))
        self.menu.append_item(self.__create_function_item("Agregar ciudad intermedia", self.__agregar_parada))
        self.menu.append_item(self.__create_function_item("Concatenar trayectos", self.__concatenar))
        self.menu.append_item(self.__create_function_item("Comparar trayectos", self.__comparar))
        self.menu.append_item(self.__create_function_item("Mostrar trayecto", self.__mostrar))
        self.menu.append_item(self.__create_function_item("Mostrar rutas", self.__mostrar_rutas))
        self.menu.append_item(self.__create_function_item("Listar", self.__listar))
        self.menu.append_item(self.__create_function_item("Guardar", self.__guardar))
        self.menu.append_item(self.__create_function_item("Cargar de disco", self.__cargar))
        self.menu.append_item(MenuItem("Salir", should_exit=True))
        self.menu.show_exit_option = False
        self.menu.show()

if __name__ == '__main__':
    App(MotorDeRutas(), CursesMenu("Estructura de datos - TP 1 | Guido Contreras Woda - Teresa Alberto", "Opciones:")).main()
