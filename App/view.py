"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________

taxi_file = 'taxi-trips-wrvz-psew-subset-small.csv'
initialStation = 0

recursionLimit = 20000

# ___________________________________________________
#  Menu principal
# ___________________________________________________

"""
Menu principal
"""


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de taxi-trips")
    print("3- Ruta corta segun horario ")
    print("4- Número de taxis")
    print("5- Número de compañias que al menos tienen un taxi inscrito")
    print("6- Top compañías")
    print("7- Top compañías (taxis)")
    print("0- Salir")
    print("*******************************************")


def optionTwo():
    print("\nCargando información de rutas de taxi en CHICAGO ....")
    controller.loadTrips(cont)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStops(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    print('El limite de recursion se ajusta a: ' + str(recursionLimit))

def optionThree():
    rta=controller.requerimiento_3(cont,id1,id2,inicio,final)
    if rta is not None:
        print('El camino mas corto entre estas dos community areas esta compuesto de ' + str(len(rta[0])) + ' trayectos :')
        for i in range(0,len(rta[0])):
            print('Desde la community area numero ' + str(rta[0][i]['vertexA']) + ' Hasta la community area numero ' + str(rta[0][i]['vertexB']))
        print('La hora recomendada para realizar este camino es : ' + str(rta[1]))
        print('El tiempo estimado para recorrer este camino en segundos es : ' + str(rta[2]))
def optionFour():
        a= controller.numtaxis(cont)
        print("El número total de taxis es de: ", a)
def optionFive():
        e=controller.companys(cont)
        print("El numero de compañías con un taxi inscrito es: "+str(e))
def optionSix():
        e=controller.topCompanies(cont,cantidad)
        print(e)
def optionSeven():
        e=controller.topCompaniesbyTaxis(cont,cantidad2)
        print(e)


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 3:
        id1=(input('Ingrese el id de la primera estación: '))
        id2=(input('Ingrese el id de la segunda estación: '))
        inicio= (input('Ingrese el limite inferior para la hora de la ruta (en formato "HH/MM/SS"): '))
        final= (input('Ingrese el limite superior para la hora de la ruta (en formato "HH/MM/SS"): '))
        executiontime = timeit.timeit(optionThree, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    elif int(inputs[0]) == 4:
        executiontime = timeit.timeit(optionFour, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    elif int(inputs[0]) == 5:
        executiontime = timeit.timeit(optionFive, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    elif int(inputs[0]) == 6:
        cantidad=int(input('Ingresa la cantidad de compañías que quieres ver en el top: '))
        executiontime = timeit.timeit(optionSix, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    elif int(inputs[0]) == 7:
        cantidad2=int(input("Ingresa la cantidad de compañías que quieres ver en el top: "))
        executiontime = timeit.timeit(optionSeven, number=1)
        print("Tiempo de ejecución: " + str(executiontime))


        
        


    else:
        sys.exit(0)
sys.exit(0)
