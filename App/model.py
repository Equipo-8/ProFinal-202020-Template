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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from datetime import datetime
assert config
from DISClib.DataStructures import mapentry as me 
"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------
def newAnalyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
                    'stops': None,
                    'connections': None,
                    'nameverteces': None,
                    'dates_paths':None,
                    'paths': None,
                    'company':None
                    }

        analyzer['stops'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)
        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)
        analyzer['nameverteces'] = m.newMap(numelements=2000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds) 
        analyzer['dates_paths'] = m.newMap(numelements=1000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)
        analyzer['dates_paths'] = m.newMap(numelements=1000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)
        analyzer['company'] = m.newMap(numelements=1000,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)                             
                                                     
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')



# Funciones para agregar informacion al grafo
def addTrip(analyzer, trip):
    try:
        weight = trip['trip_seconds']
        if weight == '' :
            weight = 0
        origin= trip['pickup_community_area']
        destination= trip['dropoff_community_area']
        weight= float(weight)       
        name= trip['trip_id']
        start= getDateTimeTaxiTrip(trip)[1]
        if not (origin==destination):
            addStation(analyzer, origin)
            addStation(analyzer, destination)
            addConnection(analyzer, origin, destination, weight)
            addDatesbypath(analyzer,origin,destination,weight,start,name)
            addCompany(analyzer,trip)
            
    except Exception as exp:
        error.reraise(exp, 'model:addTrip')

def addStation(analyzer, stationid):
    """
    Adiciona una estación como un vertice del grafo
    """
    if not gr.containsVertex(analyzer['connections'], stationid):
            gr.insertVertex(analyzer['connections'], stationid)
    return analyzer

def addConnection(analyzer,origin,destination,weight):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, weight)
    return analyzer

def addDatesbypath(analyzer,v1,v2,weight,start,trip_id):
    edge= {'vertexA':v1,'vertexB':v2,'weight':weight}
    value= {}
    value[trip_id]= edge
    key= start
    if not m.contains(analyzer['dates_paths'],key):
        m.put(analyzer['dates_paths'],key,value)
    else: 
        x = m.get(analyzer['dates_paths'],key)
        x['value'][trip_id]= edge
    return analyzer

def addCompany(analyzer,trip):
    company= trip["company"]
    taxi= trip["taxi_id"]
    existcomapany= mp.contains(analyzer["company"], company)
    if existcompany:
        entry= mp.get(analyzer["company"], company)
        if  not taxi in entry:
            entry = entry.append(taxi)    
            mp.put(analyzer["company"],company, entry)
    else:
        m.put(analyzer["company"],company,[taxi])











# ==============================
# Funciones de consulta
# ==============================


def requerimiento_3(analyzer,com1,com2,inicio,final):
    inicio= convert_to_datetime(inicio)
    final= convert_to_datetime(final)
    minimumCostPaths(analyzer,com1)
    path= minimumCostPath(analyzer,com2)
    size= st.size(path)
    for i in range(0,size):
        arco= st.pop(path)
        print(arco)
        keys= mp.keySet(analyzer['dates_paths'])
        for i in range(0,lt.size(keys)):
            date= lt.getElement(keys,i)
            if date >= inicio and date <= final :
                print(date)
                arcs= mp.get(analyzer['dates_paths'],date)['value']
                for j in arcs.values():
                    if j['vertexA']== arco['vertexA'] and j['vertexB'] == arco['vertexB']:
                        print(j)
                    
                
    return 'chupelo'



def companys(analyzer):
    cantcompanies = mp.keySet(analyzer["company"])
    lt.size(cantcompanies)

def taxis(analyzer):
    lsttaxis= mp.valueSet(analyzer["company"])
    iterator=it.newIterator(lsttaxis)
    while (it.hasNext(iterator)):
        nextvalue= it.next(iterator)
        size= len(nextvalue)









































def minimumCostPaths(analyzer, initialStation):
    """
    Calcula los caminos de costo mínimo desde la estacion initialStation
    a todos los demas vertices del grafo
    """
    analyzer['paths'] = djk.Dijkstra(analyzer['connections'], initialStation)
    return analyzer


def hasPath(analyzer, destStation):
    """
    Indica si existe un camino desde la estacion inicial a la estación destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    return djk.hasPathTo(analyzer['paths'], destStation)


def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    path = djk.pathTo(analyzer['paths'], destStation)
    return path


def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])


# ==============================
# Funciones Helper
# ==============================


def getDateTimeTaxiTrip(taxitrip):

    """

    Recibe la informacion de un servicio de taxi leido del archivo de datos (parametro).

    Retorna de forma separada la fecha (date) y el tiempo (time) del dato 'trip_start_timestamp'

    Los datos date se pueden comparar con <, >, <=, >=, ==, !=

    Los datos time se pueden comparar con <, >, <=, >=, ==, !=

    """

    tripstartdate = taxitrip['trip_start_timestamp']
    taxitripdatetime = datetime.strptime(tripstartdate, '%Y-%m-%dT%H:%M:%S.%f')
    return taxitripdatetime.date(), taxitripdatetime.time()

def convert_to_datetime(date):
    comp= '09/19/18 '
    fecha= comp + date
    fecha= datetime.strptime(fecha,'%m/%d/%y %H:%M:%S')
    time= fecha.time()
    return time
# ==============================
# Funciones de Comparacion
# ==============================

def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    stop= (stop)
    stopcode= (stopcode)
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

