from time import sleep

from cursesmenu import *
from cursesmenu.items import *

from MessageException import MessageException
from MotorDeRutas import MotorDeRutas

motor = MotorDeRutas()
menu = CursesMenu("Estructura de datos - TP 1 | Guido Contreras Woda - Teresa Alberto", "Opciones:")

def FnItem(title, func):
    return FunctionItem(title, do_wait(func))

def do_wait(func, wait=3):
    def do():
        try:
            print(func())
            sleep(wait)
        except MessageException as e:
            print(e.message)
            sleep(wait)
            do()
    return do

def crear_trayecto():
    nombre = input('Ingrese nombre del trayecto: ')
    origen = input('Ciudad origen? ')
    destino = input('Ciudad destino? ')

    motor.crear_trayecto(origen, destino, nombre)

    return "Trayecto [%s] creado." % nombre

def agregar_ciudad():
    if not motor.trayectos:
        return "No hay trayectos disponibles."

    trayecto = input('Ingrese nombre del trayecto: ')
    ciudad = input('Ciudad a agregar? ')

    motor.agregar_ciudad(trayecto, ciudad)

    return "Ciudad [%s] agregada a [%s]" % (ciudad, trayecto)

def agregar_parada():
    if not motor.trayectos:
        return "No hay trayectos disponibles."

    trayecto = input('Ingrese nombre del trayecto: ')
    existente = input('Ciudad existente del trayecto? ')
    parada = input('Ciudad a agregar? ')

    motor.agregar_parada(trayecto, existente, parada)

    return "Ciudad [%s] agregada antes de [%s] a [%s]" % (parada, existente, trayecto)

def concatenar():
    if len(motor.trayectos) < 2:
        return "No hay suficientes trayectos disponibles."

    inicial = input('Ingrese trayecto inicial: ')
    final = input('Ingrese trayecto final: ')

    motor.concatenar(inicial, final)

    return "Trayectos [%s] concatenado al final de [%s]." % (final, inicial)

def comparar():
    if len(motor.trayectos) < 2:
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

    return mensajes[motor.comparar(a, b, tipo[0])] % (a, b)

def mostrar():
    if not motor.trayectos:
        return "No hay trayectos disponibles."

    trayecto = input('Ingrese trayecto: ')

    return motor.mostrar(trayecto)

def mostrar_rutas():
    if not motor.trayectos:
        return "No hay trayectos disponibles."

    trayecto = input('Ingrese trayecto: ')

    return motor.mostrar_rutas(trayecto)

def listar():
    return str(motor.listar()) if motor.trayectos else "No hay trayectos."

def guardar():
    trayecto = input('Trayecto a guardar? (Enter para guardar todo) ')
    motor.guardar(trayecto)

    return "Trayecto%s guardado%s" % ((" ["+trayecto+"]", "") if trayecto else ("s","s"))

def cargar():
    motor.cargar_de_disco()

    return "Trayectos cargados: %s" % motor.trayectos

def salir():
    if not motor.esta_guardado():
        motor.guardar()
    return "Adios"

# Create the menu
menu.append_item(FnItem("Crear trayecto", crear_trayecto))
menu.append_item(FnItem("Agregar ciudad", agregar_ciudad))
menu.append_item(FnItem("Agregar ciudad intermedia", agregar_parada))
menu.append_item(FnItem("Concatenar trayectos", concatenar))
menu.append_item(FnItem("Comparar trayectos", comparar))
menu.append_item(FnItem("Mostrar trayecto", mostrar))
menu.append_item(FnItem("Mostrar rutas", mostrar_rutas))
menu.append_item(FnItem("Listar", listar))
menu.append_item(FnItem("Guardar", guardar))
menu.append_item(FnItem("Cargar de disco", cargar))
menu.append_item(FnItem("Salir", salir))
menu.show_exit_option = False

menu.show()
