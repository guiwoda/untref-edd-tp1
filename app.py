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

# Create the menu
menu.append_item(FnItem("Crear trayecto", crear_trayecto))
menu.append_item(FnItem("Agregar ciudad", agregar_ciudad))
menu.append_item(FnItem("Agregar ciudad intermedia", agregar_parada))
menu.append_item(FnItem("Concatenar trayectos", concatenar))
menu.append_item(FnItem("Comparar trayectos", comparar))

'''
# Create some items

# MenuItem is the base class for all items, it doesn't do anything when selected
menu_item = MenuItem("Menu Item")

# A FunctionItem runs a Python function when selected
function_item = FunctionItem("Call a Python function", input, ["Enter an input"])

# A CommandItem runs a console command
command_item = CommandItem("Run a console command",  "touch hello.txt")

# A SelectionMenu constructs a menu from a list of strings
selection_menu = SelectionMenu(["item1", "item2", "item3"])

# A SubmenuItem lets you add a menu (the selection_menu above, for example)
# as a submenu of another menu
submenu_item = SubmenuItem("Submenu item", selection_menu, menu)

# Once we're done creating them, we just add the items to the menu
menu.append_item(menu_item)
menu.append_item(function_item)
menu.append_item(command_item)
menu.append_item(submenu_item)
'''

menu.show()
